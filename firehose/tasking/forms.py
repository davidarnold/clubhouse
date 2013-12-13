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
from django.forms.models import modelformset_factory
from firehose.models import *

class TaskModelForm(forms.ModelForm):
    def clean_estimated_hours(self):
        # Enforce positive (and non-zero) numbers
        if self.cleaned_data['estimated_hours'] <= 0:
            self.cleaned_data['estimated_hours'] = Decimal('0.01')

        return self.cleaned_data['estimated_hours']

    class Meta:
        model = Task
        fields = ('work_type', 'deliverable', 'description', 'estimated_hours', 'order')
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'span12'
            }),
            'deliverable': forms.HiddenInput(attrs={
                'class': 'deliverable'
            }),
            'estimated_hours': forms.TextInput(attrs={
                'class': 'span2'
            }),
            'order': forms.HiddenInput(attrs={
                'data-field': 'order'
            })
        }

TaskModelFormSet = modelformset_factory(Task, form=TaskModelForm, can_delete=True, extra=0)

def add_fields(self, form, index):
    super(TaskModelFormSet, self).add_fields(form, index)
    form.fields[forms.formsets.DELETION_FIELD_NAME].widget = forms.HiddenInput(attrs={ 'data-field': 'delete' })

TaskModelFormSet.add_fields = add_fields
