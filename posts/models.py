from django.db import models
from django.db.models import permalink
import datetime

class Post(models.Model):
    subject = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    body = models.TextField()
    pub_date = models.DateTimeField('publication date')

    def __unicode__(self):
        return self.subject

    def get_absolute_url(self):
        return ('post_view', [str(self.slug)])
    get_absolute_url = permalink(get_absolute_url)
