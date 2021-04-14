from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):

    title = models.CharField(max_length=255, help_text="Enter a title of post")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, verbose_name="Post description", help_text="Enter a short description")
    content = models.TextField(verbose_name="Post content")
    image = models.ImageField(upload_to='static/images', blank=True)
    publishing_date = models.DateTimeField(verbose_name="Pub date", auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='copy', on_delete=models.CASCADE)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.comment
