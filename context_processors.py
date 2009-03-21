from django.template import Context

def properties(request):
    from django.conf import settings
    return {'site_name': settings.SITE_NAME,
            'site_author': settings.SITE_AUTHOR,
            'media_url': settings.MEDIA_URL,
            'site_url': settings.SITE_URL}
