from scritti.posts.models import Post
from scritti.posts.views import get_published_posts, get_published_pages

def recent_posts(request):
    recent = get_published_posts().order_by('-pub_date')[:5]
    return {'recent_posts': recent}

def pages(request):
    pages = get_published_pages()
    return {'pages': pages}
