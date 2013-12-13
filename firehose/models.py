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
from django.db import models
import django.contrib.auth.models
from django.db.models import Q
from django.utils.timezone import now

class Client(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Project(models.Model):
    HOLD_PHASE = 0
    ANALYSIS_PHASE = 10
    #DESIGN_PHASE = 20
    ESTIMATION_PHASE = 30
    IMPLEMENTATION_PHASE = 40
    COMPLETE_PHASE = 50
    PHASE_CHOICES = (
        (HOLD_PHASE, 'On Hold'),
        (ANALYSIS_PHASE, 'Analysis Phase'),
        #(DESIGN_PHASE, 'Design Phase'),
        (ESTIMATION_PHASE, 'Estimation Phase'),
        (IMPLEMENTATION_PHASE, 'Implementation Phase'),
        (COMPLETE_PHASE, 'Complete'),
    )
    client = models.ForeignKey(Client)
    name = models.CharField(max_length=50)
    launch_date = models.DateField(blank=True, null=True)
    phase = models.IntegerField(choices=PHASE_CHOICES, default=HOLD_PHASE)

    def unclaimed_issue_count(self):
        open_issues = Issue.objects.filter(deliverable__in=self.deliverable_set.all(), is_verified=False).exclude(priority=Issue.INFORMATION_PRIORITY)
        unassigned_open_issues = open_issues.filter(assignee__isnull=True)
        return unassigned_open_issues.count()

    def __unicode__(self):
        return u'{0} / {1}'.format(self.client, self.name)

    class Meta:
        ordering = ['client', 'name']

class Deliverable(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    commitment = models.DateField(blank=True, null=True)
    order = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{0} / {1}'.format(self.project, self.name)

    class Meta:
        ordering = ['order',]

class WorkType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Task(models.Model):
    work_type = models.ForeignKey(WorkType, null=True)
    deliverable = models.ForeignKey(Deliverable)
    description = models.CharField(max_length=150)
    estimated_hours = models.DecimalField(null=True, max_digits=4, decimal_places=2)
    order = models.IntegerField()
    creator = models.ForeignKey(django.contrib.auth.models.User, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def is_complete(self):
        return self.assignment_set.filter(is_complete=True).exists()

    @property
    def assignee(self):
        assignments = self.assignment_set.filter(Q(is_complete=True) | Q(sprint=Sprint.current())).order_by('-sprint__end_date')[:1]
        return assignments[0].worker if assignments else None

    @property
    def note(self):
        assignments = self.assignment_set.order_by('-sprint__end_date')[:1]
        return assignments[0].note if assignments else None

    def is_claimable(self, user):
        is_assigned = self.assignment_set.filter(sprint=Sprint.current()).exists()
        return not is_assigned and not self.is_complete and user.worker and self.work_type in [skill.work_type for skill in user.worker.skill_set.all()]

    def is_releasable(self, user):
        is_assigned = self.assignment_set.filter(sprint=Sprint.current()).exists()
        return is_assigned and not self.is_complete and self.assignee.user == user

    def __unicode__(self):
        return u'{0} / {1}'.format(self.deliverable, self.description)

class Sprint(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    @classmethod
    def current(cls):
        return cls.objects.get(start_date__lte=now().date(), end_date__gte=now().date())

    @classmethod
    def current_and_future(cls):
        return cls.objects.filter(end_date__gte=now().date())

    @classmethod
    def previous(cls, sprint_id):
        sprint = cls.objects.get(id=sprint_id)
        try:
            return cls.objects.filter(end_date__lte=sprint.start_date).order_by('-end_date')[0]
        except IndexError:
            raise Sprint.DoesNotExist

    def __unicode__(self):
        return u'{0} to {1}'.format(self.start_date, self.end_date)

class Worker(models.Model):
    user = models.OneToOneField(django.contrib.auth.models.User)

    def __unicode__(self):
        return unicode(self.user)

class Skill(models.Model):
    work_type = models.ForeignKey(WorkType)
    worker = models.ForeignKey(Worker)

    def __unicode__(self):
        return u'{0} can perform {1} work'.format(self.worker, self.work_type)

class Capacity(models.Model):
    worker = models.ForeignKey(Worker)
    sprint = models.ForeignKey(Sprint)
    hours = models.IntegerField()

    def __unicode__(self):
        return u'{0} is available in sprint {1} for {2} hours'.format(self.worker, self.sprint, self.hours)

    class Meta:
        verbose_name_plural = "Capacities"

class Allocation(models.Model):
    project = models.ForeignKey(Project)
    capacity = models.ForeignKey(Capacity)
    work_type = models.ForeignKey(WorkType)
    hours = models.IntegerField()

    def __unicode__(self):
        return u'{0} is allocated for {1} hours of {2} work for the "{3}" project'.format(self.capacity.worker, self.hours, self.work_type, self.project)

class Assignment(models.Model):
    task = models.ForeignKey(Task)
    sprint = models.ForeignKey(Sprint)
    worker = models.ForeignKey(Worker)
    is_complete = models.BooleanField()
    note = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_checkable(self, user):
        return self.worker.user == user and self.sprint == Sprint.current()

    def __unicode__(self):
        verb = 'has completed' if self.is_complete else 'is assigned to'
        return u'{0} {1} "{2}" in sprint {3}'.format(self.worker, verb, self.task, self.sprint)

    class Meta:
        unique_together = ('task', 'sprint')

class Issue(models.Model):
    BLOCKER_PRIORITY = 0
    BUG_PRIORITY = 10
    TODO_PRIORITY = 12
    CHANGE_PRIORITY = 15
    ENHANCEMENT_PRIORITY = 20
    INFORMATION_PRIORITY = 30
    PRIORITY_CHOICES = (
        ('', ''),
        (BLOCKER_PRIORITY, 'Blocker'),
        (BUG_PRIORITY, 'Bug'),
        (TODO_PRIORITY, 'Todo'),
        (CHANGE_PRIORITY, 'Change'),
        (ENHANCEMENT_PRIORITY, 'Enhancement'),
        (INFORMATION_PRIORITY, 'Information'),
    )
    reporter = models.ForeignKey(django.contrib.auth.models.User, related_name='reported_issue')
    deliverable = models.ForeignKey(Deliverable)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=PRIORITY_CHOICES[0][0])
    description = models.TextField()
    is_resolved = models.BooleanField()
    assignee = models.ForeignKey(django.contrib.auth.models.User, blank=True, null=True, related_name='assigned_issue')
    is_verified = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_checked(self, user):
        return (self.reporter == user and self.is_verified) or (self.assignee == user and self.is_resolved)

    def is_checkable(self, user):
        return self.priority != Issue.INFORMATION_PRIORITY and (self.reporter == user or (self.assignee == user and not self.is_verified))

    def is_claimable(self):
        return self.priority != Issue.INFORMATION_PRIORITY and not self.assignee and not self.is_verified

    def is_releasable(self, user):
        return self.assignee == user and not self.is_resolved and not self.is_verified

    def can_reopen(self, user):
        return self.reporter == user and self.is_resolved and not self.is_verified

    def __unicode__(self):
        status = u'Resolved' if self.is_resolved else 'Unresolved'
        return u'{0} {1} on {2}'.format(status, self.get_priority_display(), self.deliverable)


class IssueComment(models.Model):
    issue = models.ForeignKey(Issue)
    creator = models.ForeignKey(django.contrib.auth.models.User)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'Comment created by {0} on {1}'.format(self.creator, self.created)


class ProjectSubscription(models.Model):
    project = models.ForeignKey(Project)
    subscriber = models.ForeignKey(django.contrib.auth.models.User)

    def __unicode__(self):
        return u'{0} is subscribed to {1}'.format(self.subscriber, self.project)

    class Meta:
        unique_together = ('project', 'subscriber')
