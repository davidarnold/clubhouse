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
import logging
from django.core.urlresolvers import reverse
from django.db.models import Q, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from firehose.implementation.forms import *
from firehose.implementation.utils import issue_to_dict, task_to_dict
from firehose.models import Assignment, Sprint
from firehose.utils import Progress, render_to_mail
from itertools import groupby
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)


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
    worker_id = request.user.worker.id
    return HttpResponseRedirect(reverse(summary, args=(worker_id,)))

@login_required
@require_http_methods(['GET'])
def summary(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    sprint = Sprint.current()
    assignments = Assignment.objects.filter(sprint_id=sprint.id, worker_id=worker_id, is_complete=False, task__deliverable__project__phase=Project.IMPLEMENTATION_PHASE)

    def assignment_sort_key(assignment):
        return assignment.task.deliverable.project.client.name, assignment.task.deliverable.project.name, assignment.task.deliverable.order, assignment.task.deliverable.id
    def assignment_project_group_key(assignment):
        return assignment.task.deliverable.project
    def assignment_deliverable_group_key(assignment):
        return assignment.task.deliverable

    projects = []
    for project, assignments_iterator in groupby(sorted(assignments, key=assignment_sort_key), assignment_project_group_key):
        assignments = list(assignments_iterator)
        deliverables = []
        for deliverable, assignments_iterator in groupby(sorted(assignments, key=assignment_sort_key), assignment_deliverable_group_key):
            deliverables.append({
                'id': deliverable.id,
                'name': deliverable.name,
                'tasks': [task_to_dict(assignment.task, assignment, request.user) for assignment in assignments_iterator],
            })
        projects.append({
            'id': project.id,
            'name': unicode(project),
            'deliverables': deliverables,
        })

    my_issues = Issue.objects.filter(Q(reporter=worker.user) | Q(assignee=worker.user, is_resolved=False))
    my_open_issues = my_issues.filter(is_verified=False, deliverable__project__phase=Project.IMPLEMENTATION_PHASE).exclude(priority=Issue.INFORMATION_PRIORITY)

    def issue_sort_key(issue):
        return issue.deliverable.project.client.name, issue.deliverable.project.client.id,\
            issue.deliverable.project.name, issue.deliverable.project.id,\
            issue.deliverable.order, issue.deliverable.id,\
            issue.created, issue.id
    def issue_project_group_key(issue):
        return issue.deliverable.project
    def issue_deliverable_group_key(issue):
        return issue.deliverable

    for project, deliverable_issues_iterator in groupby(sorted(my_open_issues, key=issue_sort_key), issue_project_group_key):
        deliverable_issues = list(deliverable_issues_iterator)
        deliverables = []
        for deliverable, issues_iterator in groupby(deliverable_issues, issue_deliverable_group_key):
            issues = list(issues_iterator)
            deliverables.append({
                'id': deliverable.id,
                'name': deliverable.name,
                'issues': [issue_to_dict(issue, request.user) for issue in issues],
            })
        existing_projects = [existing_project for existing_project in projects if existing_project['id'] == project.id]
        existing_project = existing_projects[0] if existing_projects else None
        if not existing_project:
            projects.append({
                'id': project.id,
                'name': unicode(project),
                'deliverables': deliverables,
            })
        else:
            for deliverable in deliverables:
                existing_deliverables = [existing_deliverable for existing_deliverable in existing_project['deliverables'] if existing_deliverable['id'] == deliverable['id']]
                existing_deliverable = existing_deliverables[0] if existing_deliverables else None
                if not existing_deliverable:
                    existing_project['deliverables'].append({
                        'id': deliverable['id'],
                        'name': deliverable['name'],
                        'issues': deliverable['issues'],
                    })
                else:
                    existing_deliverable['issues'] = deliverable['issues']


    context = {
        'Issue': Issue,
        'clients': _my_current_clients(request),
        'current_sprint': sprint,
        'worker_name': worker.user.first_name,
        'worker_selection_form': WorkerSelectionForm(initial={ 'worker': worker }),
        'projects': projects,
    }

    return render(request, 'implementation/summary.html', context)

@login_required
@require_http_methods(['GET'])
def assignments(request, project_id):
    worker_id = request.user.worker.id
    sprint = Sprint.current()

    project = get_object_or_404(Project, pk=project_id)
    if project.phase != Project.IMPLEMENTATION_PHASE:
        return HttpResponseRedirect(reverse('hacker'))

    tasks = [task for deliverable in project.deliverable_set.all() for task in deliverable.task_set.all()]
    assignments = Assignment.objects.filter(sprint_id=sprint.id, worker_id=worker_id, task_id__in=tasks)

    def get_assignment(task):
        matches = [assignment for assignment in assignments if assignment.task == task]
        return matches[0] if matches else None

    def get_tags(deliverable):
        tags = []
        tags.append('deliverable-' + str(deliverable.id))
        if any(1 for task in deliverable.task_set.all() if get_assignment(task)):
            tags.append('mine')
        if any(1 for task in deliverable.task_set.all() if not task.is_complete):
            tags.append('incomplete')
        return tags

    context = {
        'Issue': Issue,
        'clients': _my_current_clients(request),
        'project': project,
        'deliverables': [
            {
                'id': deliverable.id,
                'name': deliverable.name,
                'description': deliverable.description,
                'tasks': [task_to_dict(task, get_assignment(task), request.user) for task in deliverable.task_set.order_by('order')],
                'issues': [issue_to_dict(issue, request.user) for issue in deliverable.issue_set.order_by('created')],
                'tags': get_tags(deliverable),
            } for deliverable in project.deliverable_set.order_by('order')
        ],
    }

    return render(request, 'implementation/assignments.html', context)

@login_required
@require_http_methods(['GET'])
def project(request, project_id):
    worker_id = request.user.worker.id
    sprint = Sprint.current()

    project = get_object_or_404(Project, pk=project_id)
    if project.phase != Project.IMPLEMENTATION_PHASE:
        return HttpResponseRedirect(reverse('hacker'))

    tasks = [task for deliverable in project.deliverable_set.all() for task in deliverable.task_set.all()]
    assignments = Assignment.objects.filter(sprint_id=sprint.id, worker_id=worker_id, task_id__in=tasks)

    def get_assignment(task):
        matches = [assignment for assignment in assignments if assignment.task == task]
        return matches[0] if matches else None

    def get_tags(deliverable):
        tags = []
        tags.append('deliverable-' + str(deliverable.id))
        # TODO: add "mine" tag based on issues as well
        if any(1 for task in deliverable.task_set.all() if get_assignment(task)):
            tags.append('mine')
        if any(1 for task in deliverable.task_set.all() if not task.is_complete):
            tags.append('incomplete')
        return tags

    context = {
        'Issue': Issue,
        'project': project,
        'is_subscribed': ProjectSubscription.objects.filter(project=project, subscriber=request.user).exists(),
        'deliverables': [
            {
                'id': deliverable.id,
                'name': deliverable.name,
                'tasks': [
                    task_to_dict(task, get_assignment(task), request.user)
                    for task in deliverable.task_set.order_by('order')
                    if not task.is_complete
                ],
                'issues': [
                    issue_to_dict(issue, request.user)
                    for issue in deliverable.issue_set.order_by('created')
                    if issue.is_verified == False and issue.priority != Issue.INFORMATION_PRIORITY
                ],
                'tags': get_tags(deliverable),
            } for deliverable in project.deliverable_set.order_by('order')
        ],
    }

    return render(request, 'implementation/project.html', context)

@login_required
@require_http_methods(['GET'])
def project_deliverable(request, project_id, deliverable_id):
    worker_id = request.user.worker.id
    sprint = Sprint.current()

    project = get_object_or_404(Project, pk=project_id)
    if project.phase != Project.IMPLEMENTATION_PHASE:
        return HttpResponseRedirect(reverse('hacker'))

    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)

    tasks = [task for task in deliverable.task_set.all()]
    assignments = Assignment.objects.filter(sprint_id=sprint.id, worker_id=worker_id, task_id__in=tasks)

    def get_assignment(task):
        matches = [assignment for assignment in assignments if assignment.task == task]
        return matches[0] if matches else None

    context = {
        'Issue': Issue,
        'project': project,
        'deliverable': {
            'id': deliverable.id,
            'name': deliverable.name,
            'description': deliverable.description,
            'tasks': [task_to_dict(task, get_assignment(task), request.user) for task in deliverable.task_set.order_by('order')],
            'issues': [issue_to_dict(issue, request.user) for issue in deliverable.issue_set.order_by('created')],
        },
    }

    return render(request, 'implementation/project_deliverable.html', context)

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def assignment_checked(request):
    assignment_id = request.POST['assignment_id']
    checked = request.POST['checked'] == 'true'

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if assignment.worker.user == request.user:
        assignment.is_complete = checked
        assignment.save()

    context = {
        'task': task_to_dict(assignment.task, assignment, request.user),
    }

    return render(request, 'implementation/_assignment.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def assignment_note(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == 'GET':
        form = AssignmentNoteForm(initial={
            'note': assignment.note,
        })
        status = 200
    else:
        form = AssignmentNoteForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            status = 201

            context = {
                'task': task_to_dict(assignment.task, assignment, request.user),
            }

            return render(request, 'implementation/_assignment.html', context, status=status)
        else:
            # Fall through to the render below
            status = 422

    context = {
        'assignment_id': assignment.id,
        'form': form,
    }

    return render(request, 'implementation/_assignment_note_form.html', context, status=status)

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def assignment_release(request):
    assignment_id = request.POST['assignment_id']
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if assignment.task.is_releasable(request.user):
        task = assignment.task
        assignment.delete()
        context = {
            'task': task_to_dict(task, None, request.user),
        }
        return render(request, 'implementation/_task_row.html', context)
    else:
        context = {
            'task': task_to_dict(assignment.task, assignment, request.user),
        }
        return render(request, 'implementation/_assignment.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def issue(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)

    if request.method == 'GET':
        form = IssueForm(initial={
            'reporter': request.user,
            'deliverable': deliverable,
        })
        status = 200
    else:
        form = IssueForm(request.POST)
        if form.is_valid():
            form.save()
            # Send the notifications
            try:
                issue = form.instance

                if issue.assignee:
                    to_set = set((issue.assignee,)) - set((request.user,))
                    to_list = [user.email for user in to_set if user]
                    subject = 'New {0} assigned to you in {1}'
                else:
                    subscriptions = deliverable.project.projectsubscription_set.all()
                    to_set = set([subscription.subscriber for subscription in subscriptions]) - set((request.user,))
                    to_list = [user.email for user in to_set if user]
                    subject = 'New {0} in {1}'

                if to_list:
                    dictionary = {
                        'issue': issue,
                    }
                    render_to_mail(
                        request,
                        'mail/new-issue.html',
                        dictionary,
                        subject.format(issue.get_priority_display(), issue.deliverable.project),
                        to_list
                    )
            except Exception:
                # Meh, we tried
                logger.exception('Failed to send new issue mail')

            status = 201
            context = {
                'Issue': Issue,
                'issue': issue_to_dict(form.instance, request.user),
            }
            return render(request, 'implementation/_issue_row.html', context, status=status)
        else:
            # Fall through to the render below
            status = 422

    context = {
        'form': form,
    }

    return render(request, 'implementation/_issue_form.html', context, status=status)

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def issue_checked(request):
    issue_id = request.POST['issue_id']
    checked = request.POST['checked'] == 'true'

    issue = get_object_or_404(Issue, pk=issue_id)
    if issue.reporter == request.user:
        issue.is_verified = checked
        issue.save()
    if issue.assignee == request.user:
        issue.is_resolved = checked
        issue.save()

    context = {
        'Issue': Issue,
        'issue': issue_to_dict(issue, request.user),
    }

    return render(request, 'implementation/_issue_row.html', context)

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def issue_action(request):
    issue_id = request.POST['issue_id']
    action = request.POST['action']

    issue = get_object_or_404(Issue, pk=issue_id)
    if action == 'claim' and issue.is_claimable():
        issue.assignee = request.user
        issue.save()
    elif action == 'release' and issue.is_releasable(request.user):
        issue.assignee = None
        issue.save()
    elif action == 'reopen' and issue.can_reopen(request.user):
        if issue.is_verified:
            issue.is_verified = False
            issue.save()
        elif issue.is_resolved:
            issue.is_resolved = False
            issue.save()

    context = {
        'Issue': Issue,
        'issue': issue_to_dict(issue, request.user),
    }

    return render(request, 'implementation/_issue_row.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def issue_comment(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)

    if request.method == 'GET':
        form = IssueCommentForm(initial={
            'creator': request.user,
            'issue': issue,
        })
        status = 200
    else:
        form = IssueCommentForm(request.POST)
        if form.is_valid():
            form.save()
            status = 201

            # Send the notifications
            try:
                comment = form.instance
                to_set = set((comment.issue.reporter, comment.issue.assignee))
                if not comment.issue.assignee:
                    subscriptions = comment.issue.deliverable.project.projectsubscription_set.all()
                    to_set |= set([subscription.subscriber for subscription in subscriptions])

                to_set -= set((request.user,))
                to_list = [user.email for user in to_set if user]
                dictionary = {
                    'comment': comment,
                }
                render_to_mail(
                    request,
                    'mail/new-comment.html',
                    dictionary,
                    'New Comment on {0}'.format(comment.issue.deliverable.project),
                    to_list
                )
            except Exception:
                # Meh, we tried
                logger.exception('Failed to send new comment mail')

            context = {
                'Issue': Issue,
                'issue': issue_to_dict(form.instance.issue, request.user),
            }
            return render(request, 'implementation/_issue_row.html', context, status=status)
        else:
            # Fall through to the render below
            status = 422

    context = {
        'form': form,
    }

    return render(request, 'implementation/_issue_comment_form.html', context, status=status)

@login_required
@require_http_methods(['GET', 'POST'])
def task(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)

    if request.method == 'GET':
        form = TaskForm(request.user.worker, initial={
            'creator': request.user,
            'deliverable': deliverable,
            'order': (Task.objects.filter(deliverable=deliverable).aggregate(Max('order'))['order__max'] or 0) + 1,
        })
        status = 200
    else:
        form = TaskForm(request.user.worker, request.POST)
        if form.is_valid():
            form.save()
            status = 201
            context = {
                'task': task_to_dict(form.instance, None, request.user),
            }
            return render(request, 'implementation/_task_row.html', context, status=status)
        else:
            # Fall through to the render below
            status = 422

    context = {
        'form': form,
    }

    return render(request, 'implementation/_task_form.html', context, status=status)

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def task_claim(request):
    task_id = request.POST['task_id']
    task = get_object_or_404(Task, pk=task_id)

    if task.is_claimable(request.user):
        sprint = Sprint.current()
        assignment = Assignment(task=task, sprint=sprint, worker=request.user.worker)
        assignment.save()
    else:
        assignment = None

    context = {
        'task': task_to_dict(task, assignment, request.user),
    }
    return render(request, 'implementation/_assignment.html' if assignment else 'implementation/_task_row.html', context)
