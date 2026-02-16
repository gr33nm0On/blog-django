from idlelib.query import Query

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, QueryDict
from django.shortcuts import render, redirect, reverse, render
from django.views import View

from .forms import PostForm, CommentForm, LoginForm, RegisterForm
from .models import Post, Comment

from django.contrib.auth.models import User

from django.views.generic import ListView, RedirectView, TemplateView
from .service import get_comments
from django.core.paginator import Paginator
from django.template.loader import render_to_string

def get_paginated_posts(page_number, per_page=3, filter=None):
    if filter:
        posts = Post.objects.filter(**filter).order_by('-id')
    else:
        posts = Post.objects.order_by('-id')
    paginator = Paginator(posts, per_page)
    return paginator.get_page(page_number)

def load_posts(request):
    page_number = request.GET.get('page', 1)

    page_obj = get_paginated_posts(page_number)

    form = CommentForm()

    html = render_to_string(
        "blog/posts.html",
        {"posts": page_obj.object_list, "form": form},
    )

    return JsonResponse({
        "html": html,
        "has_next": page_obj.has_next()
    })

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

class ViewPostListView(ListView):
    model = Post
    template_name = 'blog/view_post.html'
    context_object_name = 'posts'

    def get_queryset(self):
        page_obj = get_paginated_posts(1)
        return page_obj.object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.all()
        result = get_comments(comments)
        form = CommentForm()

        context['root_comments'] = result.get('root_comments')
        context['comments'] = result.get('comments')
        context['form'] = form
        context['redirect_to'] = reverse('view_post')
        context['user'] = self.request.user

        return context

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

class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'posts'

    def get_queryset(self, **kwargs):
        user = User.objects.get(id=self.kwargs.get('id'))
        posts = get_paginated_posts(1, filter={"user": user})
        py_posts = []

        class PyPost:
            def __init__(self, **kwargs):
                self.id = kwargs['id']
                self.title = kwargs['title']
                self.content = kwargs['content']
                self.user = kwargs['user']
                self.comments = kwargs['comments']

        for post in posts:
            comments = get_comments(Comment.objects.filter(post_id=post.id)).get("root_comments")
            config = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "user": post.user,
                "comments": comments,
            }
            py_posts.append(PyPost(**config))
        return py_posts

    def get_context_data(self, **kwargs):
        owner = User.objects.get(id=self.kwargs.get('id'))
        context = super().get_context_data(**kwargs)

        context["user"] = self.request.user
        context["owner"] = owner
        context["form"] = PostForm()
        context["comment_form"] = CommentForm()
        context["redirect_to"] = self.request.path

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