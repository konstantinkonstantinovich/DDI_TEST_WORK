from django.urls import path

from . import views

app_name = 'Blog'

urlpatterns = [
    path('', views.index, name='index'),
]
