from django.contrib.sitemaps import Sitemap
from scritti.posts.models import Post

class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.pub_date
