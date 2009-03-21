from scritti.links.models import Link

def links(request):
    links = Link.objects.all()
    return {'external_links': links}
