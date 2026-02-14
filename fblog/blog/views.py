from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse

from .forms import PostForm, CommentForm, LoginForm
from .models import Post, Comment

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


@login_required(login_url='/login')
def create_post(request):
    redirect_to = request.POST.get('redirect_to') or None
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            config = {
                "title": form.cleaned_data['title'],
                "content": form.cleaned_data['content'],
                "user": request.user,
            }
            Post.objects.create(**config)
    form = PostForm()
    if redirect_to:
        return redirect(redirect_to)
    return render(request, 'blog/create_post.html', {'form': form})


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

def view_post(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()

    form = CommentForm()
    result = get_comments(comments)

    comments = result.get('comments')
    root_comments = result.get('root_comments')

    return render(request, 'blog/view_post.html', {
        'posts': posts,
        'comments': comments,
        'root_comments': root_comments,
        'form': form
    })

@login_required(login_url='login')
def add_comment(request):
    redirect_to = request.POST.get('redirect_to') or None
    if request.method == "POST":
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
    if redirect_to:
        return redirect(redirect_to)
    return redirect("view_post")


def login_user(request):
    if request.method == "POST":
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
    form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("view_post")
    form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required(login_url='/login')
def profile(request):
    posts = Post.objects.filter(user=request.user)
    comments = Comment.objects.all()

    user = request.user
    form = PostForm()
    comment_form = CommentForm()
    result = get_comments(comments)

    comments = result.get('comments')
    root_comments = result.get('root_comments')

    return render(request, 'blog/profile.html', {
        'posts': posts,
        'comments': comments,
        'root_comments': root_comments,
        'form': form,
        'user': user,
        'comment_form': comment_form,
        'redirect_to': reverse('profile'),
    })