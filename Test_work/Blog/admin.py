from django.contrib import admin
from .models import Post, Comment
# Register your models here.


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "image", "publishing_date", "author", "description"]
    fields = ["title", "content", "image", "author", "description"]
    list_filter = ['author', 'title']


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "comment", "pub_date", "parent", "active"]
    fields = ["post", "author", "comment", "parent", "active"]
    list_filter = ['post']
