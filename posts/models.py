from django.db import models
from django.db.models import permalink
import datetime

class Post(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    body = models.TextField()
    pub_date = models.DateTimeField('publication date')

    def beforeSave(self):
        if (not self.pub_date):
            self.pub_date = datetime.datetime.now()

    def save(self):
        self.beforeSave()
        super(Post, self).save()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('post_view', [str(self.slug)])
    get_absolute_url = permalink(get_absolute_url)
