from .models import Comment


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
            comment.user,
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