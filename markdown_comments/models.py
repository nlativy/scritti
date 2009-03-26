from django.db import models
from django.conf import settings
from django.contrib.comments.models import Comment

from utils import markdown_pygment

class MarkdownComment(Comment):
    comment_html = models.TextField(editable=False, blank=True)
    is_spam = models.BooleanField('Spam', default=False)
    is_spam.help_text = 'Is the comment spam, set by akismet on submission'

    def spam_check(self):
        from akismet import Akismet
        a = Akismet(settings.WORDPRESS_API_KEY, blog_url=settings.SITE_URL)
        akismet_data = {}
        akismet_data['user_ip'] = self.ip_address
        # TODO: get request data
        #akismet_data['user_agent'] = request.META['HTTP_USER_AGENT']
        akismet_data['user_agent'] = ''
        akismet_data['comment_author'] = self.name
        akismet_data['comment_author_email'] = self.email
        akismet_data['comment_author_url'] = self.url
        akismet_data['comment_type'] = 'comment'

        self.is_spam = a.comment_check(self.comment, akismet_data)

        # hide spam comments
        self.is_public = not self.is_spam

    def save(self):
        # Spam check new comments
        if not self.comment_html:
            self.spam_check()

        self.comment_html = markdown_pygment(self.comment, stripimg=True)
        super(MarkdownComment, self).save()
