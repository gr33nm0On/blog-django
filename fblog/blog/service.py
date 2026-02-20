from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .forms import CommentForm
from .models import Post


def get_comments(comments):
    root_comments = []
    comment_dict = {}

    for comment in comments:
        comment_dict[comment.id] = comment
        comment.children = []

    for comment in comments:
        if comment.parent_id:
            parent = comment_dict.get(comment.parent.id)
            if parent:
                parent.children.append(comment)
        else:
            root_comments.append(comment)

    return root_comments


def get_paginated_posts(page_number, per_page=3, filter_dict=None):
    queryset = Post.objects.all()
    if filter_dict:
        queryset = queryset.filter(**filter_dict)
    queryset = queryset.select_related('user').order_by('-id')
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)

def load_posts(request):
    page_number = request.GET.get('page', 1)

    page_obj = get_paginated_posts(page_number)

    comment_form = CommentForm()

    html = render_to_string(
        "blog/posts.html",
        {"posts": page_obj.object_list, "comment_form": comment_form},
    )

    return JsonResponse({
        "html": html,
        "has_next": page_obj.has_next()
    })