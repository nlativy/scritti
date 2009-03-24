from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.list_detail import object_list
from django.conf import settings

from scritti.posts.models import Post

from tagging.models import Tag, TaggedItem

def get_published_posts():
    return Post.objects.filter(published=True, is_page=False).order_by('-pub_date')

def get_published_pages():
    return Post.objects.filter(published=True, is_page=True)

def index(request, page=1):
    post_list = get_published_posts().order_by('-pub_date')
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response('posts/post_list.html', {'posts': posts}, RequestContext(request))

def render_post(request, post, preview=False):
    return render_to_response('posts/detail.html', {'post': post, 'preview': preview}, RequestContext(request))

@staff_member_required
def preview(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, published=False)
    return render_post(request, post, preview=True)

def detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, published=True)
    return render_post(request, post)

# Legacy URL handler
def detail_date(request, post_slug, year, month, day):
    post = get_object_or_404(Post, slug=post_slug, published=True)
    if post.pub_date.year == int(year) and post.pub_date.month == int(month) and post.pub_date.day == int(day):
        return render_to_response('posts/detail.html', {'post': post, 'legacy_url': True}, RequestContext(request))
    else:
        raise Http404

def search(request, page=1):
    query_text = request.GET.get('q', None)
    post_list = Post.objects.query(query_text).filter(published=True)
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response('posts/search_results.html', {'posts': posts, 'query': query_text}, RequestContext(request))

def tagged(request, tag_name, page=1):
    tags = Tag.objects.get(name=tag_name)
    post_list = TaggedItem.objects.get_by_model(Post, tags).filter(published=True).order_by('-pub_date')
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response('posts/tag_post_list.html', {'posts': posts, 'tag': tag_name}, RequestContext(request))
