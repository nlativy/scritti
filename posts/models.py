import datetime

from django.db import models
from django.db.models import permalink

from tagging.fields import TagField
from tagging.models import Tag

from utils import markdown_pygment

class Post(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    body = models.TextField()
    body_html = models.TextField(editable=False, blank=True)
    pub_date = models.DateTimeField('publication date')
    tags = TagField()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def beforeSave(self):
        if (not self.pub_date):
            self.pub_date = datetime.datetime.now()

        self.body_html = markdown_pygment(self.body)

    def save(self):
        self.beforeSave()
        super(Post, self).save()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('post_view', [str(self.slug)])
    get_absolute_url = permalink(get_absolute_url)
