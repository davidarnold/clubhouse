# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Task.description'
        db.alter_column('firehose_task', 'description', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Task.work_type'
        db.alter_column('firehose_task', 'work_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firehose.WorkType'], null=True))

        # Changing field 'Task.estimated_hours'
        db.alter_column('firehose_task', 'estimated_hours', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

    def backwards(self, orm):

        # Changing field 'Task.description'
        db.alter_column('firehose_task', 'description', self.gf('django.db.models.fields.CharField')(default='', max_length=150))

        # User chose to not deal with backwards NULL issues for 'Task.work_type'
        raise RuntimeError("Cannot reverse this migration. 'Task.work_type' and its values cannot be restored.")

        # Changing field 'Task.estimated_hours'
        db.alter_column('firehose_task', 'estimated_hours', self.gf('django.db.models.fields.IntegerField')(null=True))

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
            'Meta': {'ordering': "['order']", 'object_name': 'Deliverable'},
            'commitment': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deliverable_template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.DeliverableTemplate']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'estimated_hours': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.WorkType']", 'null': 'True'})
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
