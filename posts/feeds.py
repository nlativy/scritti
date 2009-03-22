from scritti.posts.models import Post
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.conf import settings

class RssPostFeed(Feed):
    title = settings.SITE_NAME
    link = settings.SITE_URL
    description = "Updates from %s" % settings.SITE_NAME

    def items(self):
        return Post.objects.filter(published=True).order_by('-pub_date')[:5]

    def item_pubdate(self, item):
        return item.pub_date

    def item_author_name(self, item):
        return "%s %s" % (item.author.first_name, item.author.last_name)

    def item_categories(self, item):
        return item.tags.split(" ")
