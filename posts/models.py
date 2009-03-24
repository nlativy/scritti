import datetime

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User

from tagging.fields import TagField
from tagging.models import Tag

from django_whoosh.managers import WhooshManager

from utils import markdown_pygment

class Post(models.Model):
    title = models.CharField(max_length=128)
    title.help_text = "The title of this post"
    slug = models.SlugField(max_length=128, unique=True)
    slug.help_text = "The human readable identifier that makes up the post URL, generated from the title"
    body = models.TextField()
    body.help_text = "The body of the post, markdown syntax may be used"
    body_html = models.TextField(editable=False, blank=True)
    author = models.ForeignKey(User) 
    author.help_text = "The author of the post"
    pub_date = models.DateTimeField('publication date', null=True)
    pub_date.help_text = "The date this post was published, set automatically"
    tags = TagField()
    tags.help_text = "A space seperated set of tags"
    published = models.BooleanField('publish', default=False)
    published.help_text = "Publish this post to the site, if false it is saved as a draft"
    allow_comments = models.BooleanField('allow comments', default=True)
    allow_comments.help_text = "Permit comments on this post"
    is_page = models.BooleanField('Page', default=False)
    is_page.help_text = "If true this will be published as a page rather than a blog post"

    objects = WhooshManager('body', fields=['title', 'body'])

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def beforeSave(self):
        if (not self.pub_date and self.published):
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
