from django.urls import path, include
from .views import *

urlpatterns = [
    path('post/create', create_post, name='create_post'),
    path('post/', view_post, name='view_post'),
    path('comment/add', add_comment, name='add_comment'),
    path('register', register_user, name='register'),
    path('login', login_user, name='login'),
    path('profile', profile, name='profile'),
]