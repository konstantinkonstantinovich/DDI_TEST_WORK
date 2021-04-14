from django.contrib import admin
from .models import Post
# Register your models here.


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "image", "publishing_date", "author", "description"]
    fields = ["title", "content", "image", "author", "description"]
    list_filter = ['author', 'title']
