from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("api/posts/", views.posts_list, name="posts-list"),
    path("api/posts/<int:pk>", views.post_detail, name="post-detail"),
]