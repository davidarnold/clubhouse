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
from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from forms import *
from firehose.models import Assignment, Sprint
from itertools import groupby
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
    context = {
        'clients': _my_current_clients(request)
    }
    return render(request, 'assignment/index.html', context)

@login_required
@require_http_methods(['GET'])
def current_sprint(request, project_id):
    current_sprint = Sprint.current()
    return HttpResponseRedirect(reverse(assignments, args=(project_id, current_sprint.id)))

@login_required
def _prepare_assignment_form(request, form):
    task = Task.objects.get(id=form['task'].value())
    if task.work_type:
        workers = Worker.objects.filter(skill__work_type=task.work_type)
    else:
        workers = Worker.objects.all()
    form.fields['worker'].queryset = workers
    return form

@login_required
@require_http_methods(['GET'])
def empty_assignment(request, task_id):
    formset = AssignmentModelFormSet(queryset=Task.objects.none())
    form = formset.empty_form
    form.fields['task'].initial = task_id
    form.fields[forms.formsets.DELETION_FIELD_NAME].initial = True
    _prepare_assignment_form(request, form)

    return render(request, 'assignment/assignment.html', {
        'form': form
    })

@login_required
@require_http_methods(['GET', 'POST'])
def roll_forward(request, project_id, sprint_id):
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    count = 0

    try:
        previous_sprint = Sprint.previous(sprint_id)
        incomplete_assignments = previous_sprint.assignment_set.filter(is_complete=False, task__deliverable__project_id=project_id)
        for old_assignment in incomplete_assignments:
            matches = Assignment.objects.filter(task=old_assignment.task, sprint=sprint)
            if not matches.exists():
                new_assignment = Assignment(
                    task=old_assignment.task,
                    sprint=sprint,
                    worker=old_assignment.worker,
                    is_complete=False,
                    note=old_assignment.note,
                )
                new_assignment.save()
                count += 1
    except Sprint.DoesNotExist:
        # Do nothing. No big deal
        pass

    messages.success(request, '{0} incomplete assignments rolled forward'.format(count))
    return HttpResponseRedirect(reverse(assignments, args=(project_id, sprint_id)))

@login_required
@require_http_methods(['GET', 'POST'])
def assignments(request, project_id, sprint_id):
    if not request.user.groups.filter(name='manager').exists():
        return HttpResponseRedirect(reverse('hacker'))

    project = get_object_or_404(Project, pk=project_id)
    sprint = get_object_or_404(Sprint, pk=sprint_id)

    if request.method == 'GET':
        tasks = [task for deliverable in project.deliverable_set.all() for task in deliverable.task_set.all()]
        queryset = Assignment.objects.filter(task_id__in=tasks, sprint_id=sprint.id, is_complete=False)
        formset = AssignmentModelFormSet(queryset=queryset)
    else:
        formset = AssignmentModelFormSet(request.POST)

        if formset.is_valid():
            # Save and redirect
            formset.save()
            return HttpResponseRedirect(reverse(assignments, args=(project_id, sprint.id)))
        else:
            # Fall through to the render below
            pass

    def get_assignment_form(task):
        forms = [form for form in formset if long(form['task'].value()) == task.id]
        return _prepare_assignment_form(request, forms[0]) if forms else None

    context = {
        'clients': _my_current_clients(request),
        'project': project,
        'sprint': sprint,
        'sprint_selection_form': SprintSelectionForm(initial={ 'sprint': sprint }),
        'formset': formset,
        'deliverables': [
            {
                'name': deliverable.name,
                'description': deliverable.description,
                'tasks': [
                    {
                        'id': task.id,
                        'work_type_name': task.work_type.name if task.work_type else None,
                        'is_complete': task.is_complete,
                        'assignee': task.assignee,
                        'estimated_hours': task.estimated_hours,
                        'description': task.description,
                        'assignment_form': get_assignment_form(task),
                    } for task in deliverable.task_set.order_by('order')
                ],
            } for deliverable in project.deliverable_set.order_by('order')
        ],
    }

    return render(request, 'assignment/assignments.html', context)
