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
from django.conf.urls import patterns, url
import firehose.implementation.views

urlpatterns = patterns('',
    url(r'^$', firehose.implementation.views.index, name='implementation-index'),
    url(r'^worker/(\d+)/$', firehose.implementation.views.summary, name='implementation-summary'),
    url(r'^project/(\d+)/$', firehose.implementation.views.assignments, name='implementation-assignments'),
    url(r'^assignment/checked/$', firehose.implementation.views.assignment_checked, name='implementation-assignment-checked'),
    url(r'^assignment/release/$', firehose.implementation.views.assignment_release, name='implementation-assignment-release'),
    url(r'^assignment/(\d+)/note/$', firehose.implementation.views.assignment_note, name='implementation-assignment-note'),
    url(r'^issue/(\d+)/$', firehose.implementation.views.issue, name='implementation-issue'),
    url(r'^issue/checked/$', firehose.implementation.views.issue_checked, name='implementation-issue-checked'),
    url(r'^issue/action/$', firehose.implementation.views.issue_action, name='implementation-issue-action'),
    url(r'^issue/(\d+)/comment/$', firehose.implementation.views.issue_comment, name='implementation-issue-comment'),
    url(r'^task/(\d+)/$', firehose.implementation.views.task, name='implementation-task'),
    url(r'^task/claim/$', firehose.implementation.views.task_claim, name='implementation-task-claim'),
)
