# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'shorturl_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'shorturl', ['User'])

        # Adding model 'URL'
        db.create_table(u'shorturl_url', (
            ('id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True)),
            ('clicks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shorturl.User'], null=True)),
        ))
        db.send_create_signal(u'shorturl', ['URL'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'shorturl_user')

        # Deleting model 'URL'
        db.delete_table(u'shorturl_url')


    models = {
        u'shorturl.url': {
            'Meta': {'object_name': 'URL'},
            'clicks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shorturl.User']", 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'})
        },
        u'shorturl.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['shorturl']