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