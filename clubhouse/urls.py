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
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import *
from django.views.generic import TemplateView
import firehose.analysis.urls
import firehose.archive.urls
import firehose.assignment.urls
import firehose.implementation.urls
import firehose.monitoring.urls
import firehose.tasking.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

def dynamic_index(request):
    if request.user.is_authenticated():
        group_names = [group.name for group in request.user.groups.all()]
        if 'analyst' in group_names:
            return HttpResponseRedirect(reverse('analysis-index'))
        elif 'manager' in group_names:
            return HttpResponseRedirect(reverse('tasking-index'))
        elif 'worker' in group_names:
            return HttpResponseRedirect(reverse('implementation-index'))
        else:
            raise NotImplementedError()
    else:
        return HttpResponseRedirect(reverse('login'))

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, { 'next_page': '/' }, name='logout'),

    url(r'^$', dynamic_index),
    url(r'^analysis/', include(firehose.analysis.urls)),
    url(r'^archive/', include(firehose.archive.urls)),
    url(r'^assignment/', include(firehose.assignment.urls)),
    url(r'^implementation/', include(firehose.implementation.urls)),
    url(r'^monitoring/', include(firehose.monitoring.urls)),
    url(r'^tasking/', include(firehose.tasking.urls)),
    url(r'^i-hate-this-hacker-crap/', TemplateView.as_view(template_name="i-hate-this-hacker-crap.html"), name='hacker')
)
