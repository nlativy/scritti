from scritti.links.models import Link
from django.contrib import admin

class LinkAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Link',        {'fields': ['name', 'url']}),
            ('Metadata',    {'fields': ['title', 'rel']}),
        ]
    list_display = ('name', 'url')

admin.site.register(Link, LinkAdmin)
