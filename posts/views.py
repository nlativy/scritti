from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world! You are at the post index.")

def detail(request, post_slug):
    return HttpResponse("Hello, you're looking at the post with slug: %s." % post_slug)
