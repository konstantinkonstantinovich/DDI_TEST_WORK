from django.urls import path

from . import views

app_name = 'Blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginForm.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.RegistrationForm.as_view(), name='registration'),
]
