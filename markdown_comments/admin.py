from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from scritti.markdown_comments import MarkdownComment

class MarkdownCommentsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk', 'site')}
        ),
        (_('Content'),
           {'fields': ('user', 'user_name', 'user_email', 'user_url', 'comment')}
        ),
        (_('Metadata'),
           {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed', 'is_spam')}
        ),
     )

    list_display = ('name', 'content_type', 'object_pk', 'ip_address', 'submit_date', 'is_public', 'is_removed', 'is_spam')
    list_filter = ('submit_date', 'site', 'is_public', 'is_removed', 'is_spam')
    date_hierarchy = 'submit_date'
    ordering = ('-submit_date',)
    search_fields = ('comment', 'user__username', 'user_name', 'user_email', 'user_url', 'ip_address')

admin.site.register(MarkdownComment, MarkdownCommentsAdmin)
