# -*- coding: utf-8 -*-
#
# Copyright © 2012-2013 Kimmo Parviainen-Jalanko <k@77.fi>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from utils import itou

class User(AbstractBaseUser):
    username = models.CharField(max_length=255)
    email = models.EmailField()

class URL(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    url = models.CharField(max_length=2048, null=True)
    clicks = models.IntegerField(default=0)
    owner = models.ForeignKey('shorturl.User', null=True)

    def __unicode__(self):
        return "id {0} (#{1}) pointing to {2}".format(
            itou(self.id),
            self.id,
            self.url)
    @property
    def short(self):
        return itou(self.pk)

# Magic number for '100' is 4761
def get_free_id(min_limit=4760):
    _SQL = '''SELECT  MIN(id) + 1 as id
            FROM    shorturl_url mo
            WHERE   id > {0} AND NOT EXISTS
                    (
                    SELECT  NULL
                    FROM    shorturl_url mi
                    WHERE   mi.id = mo.id + 1)'''.format(min_limit)
    return URL.objects.raw(_SQL)[0].pk
