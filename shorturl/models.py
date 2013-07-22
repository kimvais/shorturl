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