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
from decimal import Decimal
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
from firehose.models import *

class WorkerSelectionForm(forms.Form):
    worker = forms.ModelChoiceField(
        queryset=Worker.objects.order_by('user__username'),
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'pull-right',
            },
        )
    )

class AssignmentNoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignmentNoteForm, self).__init__(*args, **kwargs)
        self.fields['note'].label = ''

    class Meta:
        model = Assignment
        fields = (
            'note',
        )

class IssueForm(forms.ModelForm):
    class UserChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.get_full_name()

    assignee = UserChoiceField(
        queryset=User.objects.filter(is_active=1, id__gt=1).order_by('first_name', 'last_name'),
        empty_label='Anyone',
        required=False
    )

    class Meta:
        model = Issue
        fields = (
            'reporter',
            'deliverable',
            'priority',
            'assignee',
            'description',
        )
        widgets = {
            'reporter': forms.HiddenInput(),
            'deliverable': forms.HiddenInput(),
        }

class IssueCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IssueCommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = ''

    class Meta:
        model = IssueComment
        fields = (
            'creator',
            'issue',
            'body',
        )
        widgets = {
            'creator': forms.HiddenInput(),
            'issue': forms.HiddenInput(),
        }

class TaskForm(forms.ModelForm):
    def __init__(self, worker, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['work_type'].queryset = WorkType.objects.filter(id__in=[skill.work_type_id for skill in worker.skill_set.all()])

    def clean_estimated_hours(self):
        # Enforce positive (and non-zero) numbers
        if self.cleaned_data['estimated_hours'] <= 0:
            self.cleaned_data['estimated_hours'] = Decimal('0.01')

        return self.cleaned_data['estimated_hours']

    class Meta:
        model = Task
        fields = (
            'creator',
            'deliverable',
            'work_type',
            'description',
            'estimated_hours',
            'order',
        )
        widgets = {
            'creator': forms.HiddenInput(),
            'deliverable': forms.HiddenInput(),
            'order': forms.HiddenInput(),
        }
