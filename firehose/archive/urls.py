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
import firehose.archive.views

urlpatterns = patterns('',
    url(r'^$', firehose.archive.views.index, name='archive-index'),
    url(r'^project/(\d+)/$', firehose.archive.views.project, name='archive-project'),
)
