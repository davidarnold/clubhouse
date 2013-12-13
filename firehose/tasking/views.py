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
import datetime
from itertools import groupby

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from firehose.tasking.forms import *
from firehose.models import Task
from django.contrib.auth.decorators import login_required

@login_required
def _my_current_clients(request):
    my_current_projects = Project.objects.filter(phase__in=[Project.ESTIMATION_PHASE, Project.IMPLEMENTATION_PHASE])
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
    return render(request, 'tasking/index.html', {
        'clients': _my_current_clients(request)
    })

@login_required
@require_http_methods(['GET'])
def empty_task(request):
    formset = TaskModelFormSet(queryset=Task.objects.none())

    return render(request, 'tasking/task.html', {
        'form': formset.empty_form
    })

@login_required
def _tasks_base(request, project, deliverables, open_tasks, closed_tasks):
    if request.method == 'GET':
        formset = TaskModelFormSet(queryset=open_tasks)
    else:
        formset = TaskModelFormSet(request.POST)

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                if not instance.id:
                    instance.creator = request.user
                instance.save()
            return HttpResponseRedirect(reverse(tasks, args=(project.id,)))
        else:
            # Sort the forms for display and fall through to the render below
            formset.forms.sort(key=lambda form: int(form.data[form.prefix + '-order']))

    def tasks_for_deliverable(deliverable):
        return [task for task in closed_tasks if task.deliverable == deliverable]

    def task_forms_for_deliverable(deliverable):
        return [form for form in formset.forms if long(form['deliverable'].value()) == deliverable.id]

    context = {
        'clients': _my_current_clients(request),
        'project': project,
        'formset': formset,
        'deliverables': [
            {
                'id': deliverable.id,
                'name': deliverable.name,
                'description': deliverable.description,
                'tasks': [
                    {
                        'id': task.id,
                        'is_complete': task.is_complete,
                        'assignee': task.assignee,
                        'estimated_hours': task.estimated_hours,
                        'description': task.description,
                    } for task in tasks_for_deliverable(deliverable)
                ],
                'task_forms': task_forms_for_deliverable(deliverable),
            } for deliverable in deliverables
        ],
        'task_order_offset': len(closed_tasks),
    }

    return render(request, 'tasking/tasks.html', context)

@login_required
def _tasks_tasking(request, project):
    deliverables = project.deliverable_set.order_by('order')
    all_tasks = Task.objects.filter(deliverable_id__in=deliverables).order_by('order')

    open_tasks = all_tasks
    closed_tasks = Task.objects.none()

    return _tasks_base(request, project, deliverables, open_tasks, closed_tasks)

@login_required
def _tasks_implementation(request, project):
    deliverables = project.deliverable_set.order_by('order')
    all_tasks = Task.objects.filter(deliverable_id__in=deliverables).order_by('order')

    fifteen_minutes = datetime.timedelta(0, 15 * 60)
    cutoff = timezone.now() - fifteen_minutes

    open_tasks = all_tasks.filter(created__gt=cutoff)
    closed_tasks = all_tasks.filter(created__lte=cutoff)

    return _tasks_base(request, project, deliverables, open_tasks, closed_tasks)

@login_required
@require_http_methods(['GET', 'POST'])
def tasks(request, project_id):
    if not request.user.groups.filter(name='manager').exists():
        return HttpResponseRedirect(reverse('hacker'))

    project = get_object_or_404(Project, pk=project_id)

    if project.phase == Project.ESTIMATION_PHASE:
        return _tasks_tasking(request, project)
    elif project.phase == Project.IMPLEMENTATION_PHASE:
        return _tasks_implementation(request, project)
    else:
        return HttpResponseRedirect(reverse('hacker'))

