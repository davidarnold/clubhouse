#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the License in the included LICENSE.txt
# or http://opensource.org/licenses/CDDL-1.0
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When modifying Covered Code, update the affected files' copyright
# notice with the current year and add your name to its contributors
# list.
#
# Copyright 2012-2013 Clubhouse Contributors
#
# File contributors: David Arnold
#
from collections import defaultdict
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from firehose.implementation.utils import issue_to_dict
from firehose.models import Project, Issue, Task, ProjectSubscription
from itertools import groupby
from firehose.utils import Progress
from django.contrib.auth.decorators import login_required

@login_required
def _my_current_clients(request):
    my_current_projects = Project.objects.filter(phase=Project.IMPLEMENTATION_PHASE)
    def sort_key(project):
        return project.client.name, project.name
    def group_key(project):
        return project.client.name
    return [
        {
            'name': client_name,
            'project_set': {
                'all': list(projects)
            }
        } for client_name, projects in groupby(sorted(my_current_projects, key=sort_key), group_key)
    ]

@login_required
@require_http_methods(['GET'])
def index(request):
    projects = Project.objects.filter(phase=Project.IMPLEMENTATION_PHASE, launch_date__isnull=False).order_by('launch_date')

    def project_sort_key(project):
        return project.launch_date, project.client.name, project.name
    def project_group_key(project):
        return project.launch_date

    launch_date_projects = []
    for launch_date, projects in groupby(sorted(projects, key=project_sort_key), project_group_key):
        project_progresses = []
        for project in projects:
            tasks = Task.objects.filter(deliverable__in=project.deliverable_set.all())
            progress = Progress()
            for task in tasks:
                progress.add(task)
            project_progresses.append({
                'id': project.id,
                'name': unicode(project),
                'progress': progress,
            })
        launch_date_projects.append({
            'launch_date': launch_date,
            'projects': project_progresses,
        })

    context = {
        'clients': _my_current_clients(request),
        'launch_date_projects': launch_date_projects,
    }
    return render(request, 'monitoring/index.html', context)

@login_required
@require_http_methods(['GET'])
def dashboard(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    deliverables = project.deliverable_set.all()

    open_issues = Issue.objects.filter(deliverable__in=deliverables, is_verified=False).exclude(priority=Issue.INFORMATION_PRIORITY)

    def issue_sort_key(issue):
        return issue.deliverable.order, issue.deliverable.id, issue.is_resolved, issue.priority, issue.created
    def issue_group_key(issue):
        return issue.deliverable

    deliverable_issues = []
    for deliverable, issues in groupby(sorted(open_issues, key=issue_sort_key), issue_group_key):
        deliverable_issues.append({
            'id': deliverable.id,
            'name': deliverable.name,
            'issues': [issue_to_dict(issue, request.user) for issue in issues],
        })

    tasks = [task for deliverable in deliverables for task in deliverable.task_set.all()]

    progress = Progress()
    breakdown = defaultdict(Progress)
    for task in tasks:
        progress.add(task)
        breakdown[task.work_type].add(task)
    overall_progress = {
        'complete_hours': progress.complete_hours,
        'total_hours': progress.total_hours,
        'percent': progress.percent,
        'breakdown': sorted(breakdown.items(), key=lambda item: item[0].name if item[0] else None),
    }

    assignments = [assignment for task in tasks for assignment in task.assignment_set.all()]

    def assignment_sort_key(assignment):
        return assignment.sprint.end_date
    def assignment_group_key(assignment):
        return assignment.sprint

    sprint_progress = []
    for sprint, associated_assignments in groupby(sorted(assignments, key=assignment_sort_key, reverse=True), assignment_group_key):
        progress = Progress()
        breakdown = defaultdict(Progress)
        for assignment in associated_assignments:
            progress.add(assignment.task, assignment=assignment)
            breakdown[assignment.worker].add(assignment.task, assignment=assignment)
        sprint_progress.append({
            'name': unicode(sprint),
            'complete_hours': progress.complete_hours,
            'total_hours': progress.total_hours,
            'percent': progress.percent,
            'breakdown': sorted(breakdown.items(), key=lambda item: item[0].user.get_full_name()),
        })

    def task_sort_key(task):
        return task.deliverable.order, task.deliverable.id, task.order
    def task_group_key(task):
        return task.deliverable

    deliverable_progress = []
    for deliverable, associated_tasks in groupby(sorted(tasks, key=task_sort_key), task_group_key):
        progress = Progress()
        tasks = []
        for task in associated_tasks:
            progress.add(task)
            tasks.append({
                'id': task.id,
                'is_complete': task.is_complete,
                'assignee': task.assignee,
                'estimated_hours': task.estimated_hours,
                'description': task.description,
            })
        deliverable_progress.append({
            'id': deliverable.id,
            'name': deliverable.name,
            'complete_hours': progress.complete_hours,
            'total_hours': progress.total_hours,
            'percent': progress.percent,
            'tasks': tasks,
        })

    context = {
        'Issue': Issue,
        'clients': _my_current_clients(request),
        'project': project,
        'is_subscribed': ProjectSubscription.objects.filter(project=project, subscriber=request.user).exists(),
        'deliverable_issues': deliverable_issues,
        'overall_progress': overall_progress,
        'sprint_progress': sprint_progress,
        'deliverable_progress': deliverable_progress,
    }

    return render(request, 'monitoring/dashboard.html', context)

@login_required
@require_http_methods(['POST'])
def subscribe(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not ProjectSubscription.objects.filter(project=project, subscriber=request.user).exists():
        ProjectSubscription(project=project, subscriber=request.user).save()

    return HttpResponseRedirect(reverse(dashboard, args=(project_id,)))

@login_required
@require_http_methods(['POST'])
def unsubscribe(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    ProjectSubscription.objects.filter(project=project, subscriber=request.user).delete()

    return HttpResponseRedirect(reverse(dashboard, args=(project_id,)))
