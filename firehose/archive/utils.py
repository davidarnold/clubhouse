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
def issue_to_dict(issue, user):
    return {
        'id': issue.id,
        'is_checked': False,
        'is_checkable': False,
        'is_resolved': issue.is_resolved,
        'is_verified': issue.is_verified,
        'reporter': issue.reporter,
        'assignee': issue.assignee,
        'created': issue.created,
        'updated': issue.updated,
        'priority': issue.priority,
        'get_priority_display': issue.get_priority_display(),
        'description': issue.description,
        'is_claimable': False,
        'is_releasable': False,
        'can_reopen': False,
        'comments': [{
            'id': comment.id,
            'creator': comment.creator,
            'body': comment.body,
            'created': comment.created,
            'updated': comment.updated,
        } for comment in issue.issuecomment_set.order_by('created')],
        'can_comment': False,
    }


def task_to_dict(task):
    return {
        'id': task.id,
        'is_complete': task.is_complete,
        'note': task.note,
        'estimated_hours': task.estimated_hours,
        'description': task.description,
        'assignee': task.assignee,
    }
