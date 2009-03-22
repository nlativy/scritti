from django.conf.urls.defaults import *
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^scritti/', include('scritti.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^$', 'scritti.posts.views.index'),
    url(r'^page/(?P<page>\d+)$', 'scritti.posts.views.index', name='index_page'),
    url(r'^search/$', 'scritti.posts.views.search', name='search_view'),
    url(r'^articles/(?P<post_slug>.*)/$', 'scritti.posts.views.detail', name='post_view'),
    url(r'^tag/(?P<tag_name>.*)/$', 'scritti.posts.views.tagged', name="tag_view"),
    url(r'^tag/(?P<tag_name>.*)/(?P<page>\d+)$', 'scritti.posts.views.tagged', name="tag_page"),
)

if settings.DEBUG:
    media_path = os.path.join(settings.SITE_ROOT, 'site_media/')
    urlpatterns += patterns('',
            (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_path}),
        )
