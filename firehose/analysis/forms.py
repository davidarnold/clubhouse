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
from django.forms.models import modelformset_factory
from firehose.models import *

class DeliverableModelForm(forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = ('name', 'description', 'order')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'span6'
            }),
            'order': forms.HiddenInput(attrs={
                'data-field': 'order'
            })
        }

DeliverableModelFormSet = modelformset_factory(Deliverable, form=DeliverableModelForm, can_delete=True, extra=0)

def add_fields(self, form, index):
    super(DeliverableModelFormSet, self).add_fields(form, index)
    form.fields[forms.formsets.DELETION_FIELD_NAME].widget = forms.HiddenInput(attrs={ 'data-field': 'delete' })

DeliverableModelFormSet.add_fields = add_fields
