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
        'is_checked': issue.is_checked(user),
        'is_checkable': issue.is_checkable(user),
        'is_resolved': issue.is_resolved,
        'is_verified': issue.is_verified,
        'reporter': issue.reporter,
        'assignee': issue.assignee,
        'created': issue.created,
        'updated': issue.updated,
        'priority': issue.priority,
        'get_priority_display': issue.get_priority_display(),
        'description': issue.description,
        'is_claimable': issue.is_claimable(),
        'is_releasable': issue.is_releasable(user),
        'can_reopen': issue.can_reopen(user),
        'comments': [{
            'id': comment.id,
            'creator': comment.creator,
            'body': comment.body,
            'created': comment.created,
            'updated': comment.updated,
        } for comment in issue.issuecomment_set.order_by('created')],
        'can_comment': True,
    }

def task_to_dict(task, assignment, user):
    return {
        'id': task.id,
        'is_complete': task.is_complete,
        'is_checkable': assignment and assignment.is_checkable(user),
        'note': task.note,
        'estimated_hours': task.estimated_hours,
        'description': task.description,
        'is_claimable': task.is_claimable(user),
        'is_releasable': task.is_releasable(user),
        'assignee': task.assignee,
        'assignment': assignment,
        'work_type': task.work_type,
    }
