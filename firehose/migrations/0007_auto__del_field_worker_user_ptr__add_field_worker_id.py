# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Worker.user_ptr'
        db.delete_column('firehose_worker', 'user_ptr_id')

        # Adding field 'Worker.id'
        db.add_column('firehose_worker', 'id',
                      self.gf('django.db.models.fields.AutoField')(default=None, primary_key=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Worker.user_ptr'
        db.add_column('firehose_worker', 'user_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['auth.User'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Worker.id'
        db.delete_column('firehose_worker', 'id')


    models = {
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
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'estimated_hours': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['firehose.WorkType']", 'null': 'True', 'blank': 'True'})
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
            'Meta': {'object_name': 'Worker'},
            'dummy': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'firehose.worktype': {
            'Meta': {'object_name': 'WorkType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['firehose']
