from django.db import models

class Link(models.Model):
    name = models.CharField(max_length=64)
    name.help_text = "The name of the link to be used as the link text"
    title = models.CharField(max_length=128)
    title.help_text = "The title field of the hyperlink, will be visible as a tooltip"
    rel = models.CharField(max_length=64)
    rel.help_text = "The relationship of this link, set to 'me' for links to your other web pages" 
    url = models.URLField()
    url.help_text = "The full URL that the link points to"

    def __unicode__(self):
        return self.name
