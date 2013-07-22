from django.db import models
from URLconvert import itou

# Create your models here.
class Shorturl(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    url = models.CharField(max_length=2048, null=True)
    clicks = models.IntegerField(default=0)

    def __unicode__(self):
        return "id {0} (#{1}) pointing to {2}".format(
            itou(self.id),
            self.id,
            self.url)