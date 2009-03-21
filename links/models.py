from django.db import models

class Link(models.Model):
    name = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    rel = models.CharField(max_length=64)
    url = models.URLField()

    def __unicode__(self):
        return self.name
