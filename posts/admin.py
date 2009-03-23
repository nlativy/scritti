from scritti.posts.models import Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Post',                {'fields': ['title', 'body']}),
            #('Date information',    {'fields': ['pub_date'], 'classes': ['collapse']}),
            ('Meta',                {'fields': ['slug', 'tags', 'author']}),
            ('Publish',             {'fields': ['published']}),
        ]
    list_display = ('title', 'pub_date', 'published', 'tags')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
