from django import forms
from django.contrib.comments.forms import CommentForm
from scritti.markdown_comments.models import MarkdownComment

class MarkdownCommentForm(CommentForm):
    
    def get_comment_model(self):
        return MarkdownComment

    def get_comment_create_data(self):
        return super(MarkdownCommentForm, self).get_comment_create_data()
