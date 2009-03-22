from scritti.posts.models import Post

def recent_posts(request):
    recent = Post.objects.filter(published=True).order_by('-pub_date')[:5]
    return {'recent_posts': recent}
