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
import models
from django.contrib import admin

admin.site.register(models.Client)
admin.site.register(models.Project)
admin.site.register(models.Deliverable)
admin.site.register(models.WorkType)
admin.site.register(models.Task)
admin.site.register(models.Sprint)
admin.site.register(models.Worker)
admin.site.register(models.Skill)
admin.site.register(models.Capacity)
admin.site.register(models.Allocation)
admin.site.register(models.Assignment)
admin.site.register(models.Issue)
admin.site.register(models.ProjectSubscription)
