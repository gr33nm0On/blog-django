from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import PostForm, CommentForm, LoginForm, RegisterForm
from .models import Post, Comment

from django.contrib.auth.models import User

from django.views.generic import ListView
from .service import get_comments, get_paginated_posts



class AbstractPostView(ListView):
    def get_queryset(self, filter_dict=None, **kwargs):
        if filter_dict:
            posts = get_paginated_posts(
                page_number=1,
                per_page=3,
                filter_dict=filter_dict
            )
        else:
            posts = get_paginated_posts(1)
        py_posts = []

        class PyPost:
            def __init__(self, **kwargs):
                self.id = kwargs['id']
                self.title = kwargs['title']
                self.content = kwargs['content']
                self.user = kwargs['user']
                self.comments = kwargs['comments']

        for post in posts:
            comments = get_comments(Comment.objects.filter(post_id=post.id))
            config = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "user": post.user,
                "comments": comments,
            }
            py_posts.append(PyPost(**config))
        return py_posts

    def get_context_data(self, add_context=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if add_context:
            for key, value in add_context.items():
                context[key] = value

        context["user"] = self.request.user
        context["form"] = PostForm()
        context["comment_form"] = CommentForm()
        context["redirect_to"] = self.request.path

        return context


class CreatePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        redirect_to = request.POST.get('redirect_to')
        form = PostForm(request.POST)
        if form.is_valid():
            config = {
                "title": form.cleaned_data['title'],
                "content": form.cleaned_data['content'],
                "user": request.user,
            }
            Post.objects.create(**config)
        return redirect(redirect_to)

class ViewPostListView(AbstractPostView):
    model = Post
    template_name = 'blog/view_post.html'
    context_object_name = 'posts'

class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        redirect_to = request.POST.get('redirect_to')
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(id=request.POST['post_id'])
            content = form.cleaned_data['content']
            user = request.user
            if request.POST.get('reply_to'):
                parent = Comment.objects.get(id=request.POST['reply_to'])
            else:
                parent = None
            config = {
                "post": post,
                "content": content,
                "parent": parent,
                "user": user,
            }
            Comment.objects.create(**config)
        return redirect(redirect_to)

class ProfileView(AbstractPostView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'posts'

    def get_queryset(self, **kwargs):
        user_id = self.kwargs.get('id')
        return super().get_queryset(
            filter_dict={"user_id": user_id},
            **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owner"] = User.objects.get(id=self.kwargs.get('id'))
        return context






class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            config = {
                "username": form.cleaned_data['username'],
                "password": form.cleaned_data['password']
            }
            user = authenticate(request, **config)
            if user:
                login(request, user)
                return redirect("view_post")
        return self.get(request, *args, **kwargs)

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'blog/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("view_post")
        return self.get(request, *args, **kwargs)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('view_post')