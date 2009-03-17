from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from scritti.posts.models import Post

def index(request):
    latest_posts = Post.objects.all().order_by('-pub_date')[:5]
    return render_to_response('posts/index.html', {'latest_posts': latest_posts})

def detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    return render_to_response('posts/detail.html', {'post': post})
