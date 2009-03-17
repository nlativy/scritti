from django.db import models
import datetime

class Post(models.Model):
    subject = models.CharField(max_length=256)
    body = models.TextField()
    pub_date = models.DateTimeField('publication date')

    def __unicode__(self):
        return self.subject
