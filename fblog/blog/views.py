from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.views import View

from .forms import PostForm, CommentForm, LoginForm
from .models import Post, Comment

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import ListView, RedirectView, TemplateView


def get_comments(comments):
    class PyComment():
        def __init__(self, id, user=None, post_id = None, parent_id=None, content=None):
            self.id = id
            self.post_id = post_id
            self.parent_id = parent_id
            self.user = user
            self.children = []
            self.content = content

    def convert(comment: Comment):
        return PyComment(
            comment.id,
            comment.user.username,
            comment.post_id if comment.post_id else None,
            comment.parent.id if comment.parent else None,
            comment.content,
        )

    py_comments = []
    comment_dict = {}

    for comment in comments:
        py_comment = convert(comment)
        py_comments.append(py_comment)
        comment_dict[comment.id] = py_comment

    for comment in py_comments:
        if comment.parent_id:
            parent = comment_dict.get(comment.parent_id)
            if parent:
                parent.children.append(comment)

    root_comments = [c for c in py_comments if c.parent_id is None]
    return {'root_comments': root_comments, 'comments': py_comments}


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.all()
        result = get_comments(comments)
        form = CommentForm()

        context['root_comments'] = result.get('root_comments')
        context['comments'] = result.get('comments')
        context['form'] = form
        context['redirect_to'] = reverse('view_post')

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
        form = UserCreationForm()
        return render(request, 'blog/register.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("view_post")
        return self.get(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.all()

        context["user"] = self.request.user
        context["form"] = PostForm()
        context["comment_form"] = CommentForm()
        result = get_comments(comments)

        context["comments"] = result.get('comments')
        context["root_comments"] = result.get('root_comments')
        context["redirect_to"] = reverse('profile')

        return context