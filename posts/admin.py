from scritti.posts.models import Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Post',                {'fields': ['title', 'body']}),
            ('Date information',    {'fields': ['pub_date'], 'classes': ['collapse']}),
            ('Slug',                {'fields': ['slug']}),
        ]
    list_display = ('title', 'pub_date')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
