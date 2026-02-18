from plistlib import loads

from django.urls import path, include

from .service import load_posts
from .views import *

urlpatterns = [
    path('post/create', CreatePostView.as_view(), name='create_post'),
    path('post/', ViewPostListView.as_view(), name='view_post'),
    path('comment/add', CreateCommentView.as_view(), name='add_comment'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('profile/<int:id>', ProfileView.as_view(), name='profile'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('post/load/', load_posts, name='load_posts'),
    path('like/post/<int:post_id>/<int:user_id>', post_like, name='like'),
]