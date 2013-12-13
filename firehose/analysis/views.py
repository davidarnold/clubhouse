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
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from firehose.analysis.forms import *
from firehose.models import Deliverable
from itertools import groupby
from django.contrib.auth.decorators import login_required

@login_required
def _my_current_clients(request):
    my_current_projects = Project.objects.filter(phase=Project.ANALYSIS_PHASE)
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
    return render(request, 'analysis/index.html', {
        'clients': _my_current_clients(request),
    })

@login_required
@require_http_methods(['GET'])
def empty_deliverable(request):
    formset = DeliverableModelFormSet(queryset=Deliverable.objects.none())

    return render(request, 'analysis/deliverable.html', {
        'form': formset.empty_form
    })

@login_required
@require_http_methods(['GET', 'POST'])
def format_deliverables(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    return render(request, 'analysis/format-deliverables.html', {
        'project': project,
        'deliverables': project.deliverable_set.order_by('order')
    })

@login_required
@require_http_methods(['GET', 'POST'])
def deliverables(request, project_id):
    if not request.user.groups.filter(name='analyst').exists():
        return HttpResponseRedirect(reverse('hacker'))

    project = get_object_or_404(Project, pk=project_id)
    if project.phase != Project.ANALYSIS_PHASE:
        return HttpResponseRedirect(reverse('hacker'))

    if request.method == 'GET':
        formset = DeliverableModelFormSet(queryset=project.deliverable_set.order_by('order'))
    else:
        formset = DeliverableModelFormSet(request.POST)

        if formset.is_valid():
            instances = formset.save(commit=False)

            for instance in instances:
                if not instance.project_id:
                    instance.project_id = project_id

                instance.save()

            return HttpResponseRedirect(reverse(deliverables, args=(project_id,)))
        else:
            # Sort the forms for display and fall through to the render below
            formset.forms.sort(key=lambda form: int(form.data[form.prefix + '-order']))

    return render(request, 'analysis/deliverables.html', {
        'clients': _my_current_clients(request),
        'project': project,
        'formset': formset,
    })


