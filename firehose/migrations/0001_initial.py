# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table('firehose_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('firehose', ['Client'])

        # Adding model 'ProjectTemplate'
        db.create_table('firehose_projecttemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('firehose', ['ProjectTemplate'])

        # Adding model 'Project'
        db.create_table('firehose_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Client'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('commitment', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('firehose', ['Project'])

        # Adding model 'DeliverableTemplate'
        db.create_table('firehose_deliverabletemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.ProjectTemplate'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('firehose', ['DeliverableTemplate'])

        # Adding model 'Deliverable'
        db.create_table('firehose_deliverable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Project'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('commitment', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('deliverable_template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.DeliverableTemplate'], null=True, blank=True)),
        ))
        db.send_create_signal('firehose', ['Deliverable'])

        # Adding model 'WorkType'
        db.create_table('firehose_worktype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('firehose', ['WorkType'])

        # Adding model 'TaskTemplate'
        db.create_table('firehose_tasktemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('work_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.WorkType'])),
            ('deliverable_template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.DeliverableTemplate'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('estimated_hours', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('firehose', ['TaskTemplate'])

        # Adding model 'Task'
        db.create_table('firehose_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('work_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.WorkType'])),
            ('deliverable', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Deliverable'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('estimated_hours', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('firehose', ['Task'])

        # Adding model 'Sprint'
        db.create_table('firehose_sprint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('firehose', ['Sprint'])

        # Adding model 'Worker'
        db.create_table('firehose_worker', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('firehose', ['Worker'])

        # Adding model 'Skill'
        db.create_table('firehose_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('work_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.WorkType'])),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Worker'])),
        ))
        db.send_create_signal('firehose', ['Skill'])

        # Adding model 'Capacity'
        db.create_table('firehose_capacity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Worker'])),
            ('sprint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Sprint'])),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('firehose', ['Capacity'])

        # Adding model 'Allocation'
        db.create_table('firehose_allocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Project'])),
            ('capacity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Capacity'])),
            ('work_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.WorkType'])),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('firehose', ['Allocation'])

        # Adding model 'Assignment'
        db.create_table('firehose_assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Task'])),
            ('sprint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Sprint'])),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Worker'])),
            ('is_complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('firehose', ['Assignment'])

        # Adding model 'Blocker'
        db.create_table('firehose_blocker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.Assignment'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('is_cleared', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('firehose', ['Blocker'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table('firehose_client')

        # Deleting model 'ProjectTemplate'
        db.delete_table('firehose_projecttemplate')

        # Deleting model 'Project'
        db.delete_table('firehose_project')

        # Deleting model 'DeliverableTemplate'
        db.delete_table('firehose_deliverabletemplate')

        # Deleting model 'Deliverable'
        db.delete_table('firehose_deliverable')

        # Deleting model 'WorkType'
        db.delete_table('firehose_worktype')

        # Deleting model 'TaskTemplate'
        db.delete_table('firehose_tasktemplate')

        # Deleting model 'Task'
        db.delete_table('firehose_task')

        # Deleting model 'Sprint'
        db.delete_table('firehose_sprint')

        # Deleting model 'Worker'
        db.delete_table('firehose_worker')

        # Deleting model 'Skill'
        db.delete_table('firehose_skill')

        # Deleting model 'Capacity'
        db.delete_table('firehose_capacity')

        # Deleting model 'Allocation'
        db.delete_table('firehose_allocation')

        # Deleting model 'Assignment'
        db.delete_table('firehose_assignment')

        # Deleting model 'Blocker'
        db.delete_table('firehose_blocker')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'firehose.allocation': {
            'Meta': {'object_name': 'Allocation'},
            'capacity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Capacity']"}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Project']"}),
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.WorkType']"})
        },
        'firehose.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sprint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Sprint']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Task']"}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Worker']"})
        },
        'firehose.blocker': {
            'Meta': {'object_name': 'Blocker'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Assignment']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cleared': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'firehose.capacity': {
            'Meta': {'object_name': 'Capacity'},
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sprint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Sprint']"}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Worker']"})
        },
        'firehose.client': {
            'Meta': {'object_name': 'Client'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'firehose.deliverable': {
            'Meta': {'object_name': 'Deliverable'},
            'commitment': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deliverable_template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.DeliverableTemplate']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Project']"})
        },
        'firehose.deliverabletemplate': {
            'Meta': {'object_name': 'DeliverableTemplate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'project_template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.ProjectTemplate']", 'null': 'True', 'blank': 'True'})
        },
        'firehose.project': {
            'Meta': {'object_name': 'Project'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Client']"}),
            'commitment': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'firehose.projecttemplate': {
            'Meta': {'object_name': 'ProjectTemplate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'firehose.skill': {
            'Meta': {'object_name': 'Skill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.WorkType']"}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Worker']"})
        },
        'firehose.sprint': {
            'Meta': {'object_name': 'Sprint'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'firehose.task': {
            'Meta': {'object_name': 'Task'},
            'deliverable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.Deliverable']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'estimated_hours': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.WorkType']"})
        },
        'firehose.tasktemplate': {
            'Meta': {'object_name': 'TaskTemplate'},
            'deliverable_template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.DeliverableTemplate']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'estimated_hours': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.WorkType']"})
        },
        'firehose.worker': {
            'Meta': {'object_name': 'Worker', '_ormbases': ['auth.User']},
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'firehose.worktype': {
            'Meta': {'object_name': 'WorkType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['firehose']
