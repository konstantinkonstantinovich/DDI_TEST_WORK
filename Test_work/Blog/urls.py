from django.urls import path

from . import views

app_name = 'Blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginForm.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.RegistrationForm.as_view(), name='registration'),
    path('post/list/', views.PostListView.as_view(), name="post-list"),
    path('post/create/', views.PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/detail/', views.PostDetailView.as_view(), name="post-detail"),
    path('search/', views.SearchResultView.as_view(), name='search_results'),
    path('post/<int:post_id>/detail/comment/<int:comment_id>/', views.CommentCreateFrom, name="comment-create")
]
