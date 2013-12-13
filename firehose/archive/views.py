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
from itertools import groupby
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from firehose.archive.utils import task_to_dict, issue_to_dict
from firehose.models import Project, Issue
from django.contrib.auth.decorators import login_required


@login_required
def _my_current_clients(request):
    my_current_projects = Project.objects.filter(phase=Project.COMPLETE_PHASE)
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
    context = {
        'clients': _my_current_clients(request)
    }
    return render(request, 'archive/index.html', context)


@login_required
@require_http_methods(['GET'])
def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    tasks = [task for deliverable in project.deliverable_set.all() for task in deliverable.task_set.all()]

    context = {
        'Issue': Issue,
        'clients': _my_current_clients(request),
        'project': project,
        'deliverables': [
            {
                'id': deliverable.id,
                'name': deliverable.name,
                'description': deliverable.description,
                'tasks': [task_to_dict(task) for task in deliverable.task_set.order_by('order')],
                'issues': [issue_to_dict(issue, request.user) for issue in deliverable.issue_set.order_by('created')],
                } for deliverable in project.deliverable_set.order_by('order')
        ],
        }

    return render(request, 'archive/project.html', context)
