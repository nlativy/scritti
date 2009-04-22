from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.list_detail import object_list
from django.conf import settings
from django.core.urlresolvers import reverse

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
    return HttpResponseRedirect(reverse('post_view', args=[post_slug]))

def search(request, page=1):
    from whoosh.support.pyparsing import ParseException
    error = None
    before_error = None
    after_error = None
    posts = []

    query_text = request.GET.get('q', None)
    try:
        post_list = Post.objects.query(query_text).filter(published=True)
    except ParseException, e:
        before_error = query_text[:e.col]
        error = query_text[e.col]
        if e.col < len(query_text):
            after_error = query_text[e.col+1:]
    
    if not error:
        paginator = Paginator(post_list, settings.POSTS_PER_PAGE)

        try:
            posts = paginator.page(page)
        except (EmptyPage, InvalidPage):
            posts = paginator.page(paginator.num_pages)

    vars = {
             'posts': posts,
             'query': query_text,
             'parse_error': error,
             'before_error': before_error,
             'after_error': after_error
           }
    return render_to_response('posts/search_results.html', vars, RequestContext(request))

def tagged(request, tag_name, page=1):
    tags = Tag.objects.get(name=tag_name)
    post_list = TaggedItem.objects.get_by_model(Post, tags).filter(published=True).order_by('-pub_date')
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response('posts/tag_post_list.html', {'posts': posts, 'tag': tag_name}, RequestContext(request))
