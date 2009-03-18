from django.template import Context

def site_name(request):
    from django.conf import settings
    return {'site_name': settings.SITE_NAME}
