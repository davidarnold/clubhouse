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
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class Progress(object):
    def __init__(self):
        self.total_hours = 0
        self.complete_hours = 0

    @property
    def percent(self):
        return Decimal(0) if self.total_hours == 0 else Decimal(100) * self.complete_hours / self.total_hours

    def add(self, task, assignment=None):
        if assignment is not None:
            if assignment.is_complete:
                self.complete_hours += task.estimated_hours
        elif task.is_complete:
            self.complete_hours += task.estimated_hours
        self.total_hours += task.estimated_hours

def render_to_mail(request, template_name, dictionary, subject, to_list, cc_list=None, bcc_list=None, attachments=None, html_content=True):
    """
    Renders the specified template (with an optional dictionary of values) into the body of an email,
    then sends with the given subject to the recipients.
    """
    scheme = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    dictionary['BASE_URL'] = '{0}://{1}'.format(scheme, host)
    dictionary['SUBJECT'] = subject
    body = render_to_string(template_name, dictionary)
    message = EmailMessage(subject=subject, body=body, to=to_list, cc=cc_list, bcc=bcc_list, attachments=attachments)
    if html_content:
        message.content_subtype = 'html'
    message.send()
