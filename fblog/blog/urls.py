from django.urls import path, include
from .views import *

urlpatterns = [
    path('post/create', CreatePostView.as_view(), name='create_post'),
    path('post/', ViewPostListView.as_view(), name='view_post'),
    path('comment/add', CreateCommentView.as_view(), name='add_comment'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('profile/<int:id>', ProfileView.as_view(), name='profile'),
    path('logout', LogoutView.as_view(), name='logout'),
]