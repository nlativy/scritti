from scritti.markdown_comments.models import MarkdownComment
from scritti.markdown_comments.forms import MarkdownCommentForm
from django.core import urlresolvers

def get_model():
    return MarkdownComment

def get_form():
    return MarkdownCommentForm

def get_form_target():
    return urlresolvers.reverse("django.contrib.comments.views.comments.post_comment") 
