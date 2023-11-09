from django.contrib import admin
from .models import Follow, Post, Stream, Tag, Likes, Comment

# Register your models here.

admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Stream)
admin.site.register(Tag)
admin.site.register(Likes)
admin.site.register(Comment)