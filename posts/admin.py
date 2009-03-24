from scritti.posts.models import Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Post',                {'fields': ['title', 'body']}),
            #('Date information',    {'fields': ['pub_date'], 'classes': ['collapse']}),
            ('Meta',                {'fields': ['slug', 'tags', 'author']}),
            ('Publication',         {'fields': ['published', 'allow_comments', 'is_page']}),
        ]
    list_display = ('title', 'pub_date', 'published', 'allow_comments', 'is_page', 'tags')
    list_filter = ('published', 'is_page', 'pub_date')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body', 'tags')
    ordering = ('-pub_date',)
    date_hierarchy = 'pub_date'

admin.site.register(Post, PostAdmin)
