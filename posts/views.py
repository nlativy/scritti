from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.list_detail import object_list
from django.conf import settings

from scritti.posts.models import Post

from tagging.models import Tag, TaggedItem

def index(request, page=1):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response('posts/post_list.html', {'posts': posts}, RequestContext(request))

def detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    return render_to_response('posts/detail.html', {'post': post}, RequestContext(request))

def tagged(request, tag_name, page=1):
    tags = Tag.objects.get(name=tag_name)
    post_list = TaggedItem.objects.get_by_model(Post, tags).order_by('-pub_date')
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response('posts/tag_post_list.html', {'posts': posts, 'tag': tag_name}, RequestContext(request))
