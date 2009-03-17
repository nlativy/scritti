from scritti.posts.models import Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Post',                {'fields': ['subject', 'body']}),
            ('Date information',    {'fields': ['pub_date'], 'classes': ['collapse']}),
            ('Slug',                {'fields': ['slug']}),
        ]
    list_display = ('subject', 'pub_date')

admin.site.register(Post, PostAdmin)
