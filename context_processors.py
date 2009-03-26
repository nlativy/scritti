from django.template import Context
from django.conf import settings
import twitter

def properties(request):
    return {'site_name': settings.SITE_NAME,
            'site_author': settings.SITE_AUTHOR,
            'site_url': settings.SITE_URL}

def tweets(request):
    api = twitter.Api()
    tweets = api.GetUserTimeline(settings.TWITTER_USER)[:settings.NUMBER_OF_TWEETS]
    return {'tweets': tweets,
            'twitter_url': "http://twitter.com/%s" % settings.TWITTER_USER}
