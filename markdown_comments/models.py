from django.db import models
from django.contrib.comments.models import Comment

from utils import markdown_pygment

class MarkdownComment(Comment):
    comment_html = models.TextField(editable=False, blank=True)

    def save(self):
        # If comment is new, don't make if public at first
        # if not self.comment_html:
        #     self.is_public = False

        self.comment_html = markdown_pygment(self.comment, stripimg=True)
        super(MarkdownComment, self).save()
