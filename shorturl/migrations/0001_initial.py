# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shorturl'
        db.create_table(u'shorturl_shorturl', (
            ('id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('clicks', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'shorturl', ['Shorturl'])


    def backwards(self, orm):
        # Deleting model 'Shorturl'
        db.delete_table(u'shorturl_shorturl')


    models = {
        u'shorturl.shorturl': {
            'Meta': {'object_name': 'Shorturl'},
            'clicks': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        }
    }

    complete_apps = ['shorturl']