function showReplies(postId, commentId) {
    var element = document.getElementById("comment-container-" + postId + "-" + commentId);
    var btn = document.getElementById("btn-comment-container-" + postId + "-" + commentId);

    if (!element.hidden) {
        btn.innerHTML = "Show replies";
        btn.style.backgroundColor = "rgb(0, 0, 0)"
        btn.style.color = "rgb(220, 242, 191)"
        element.hidden = true;
    } else {
        btn.innerHTML = "Close replies";
        btn.style.backgroundColor = "rgb(220, 242, 191)"
        btn.style.color = "rgb(0, 0, 0)"
        element.hidden = false;
    }
}

function showComments(postId) {
    var element = document.getElementById("comment-container-" + postId);
    var btn = document.getElementById("btn-comment-container-" + postId);

    if (!element.hidden) {
        btn.innerHTML = "Show comments";
        btn.style.backgroundColor = "rgb(0, 0, 0)"
        btn.style.color = "rgb(220, 242, 191)"
        element.hidden = true;
    } else {
        btn.innerHTML = "Close comments";
        btn.style.backgroundColor = "rgb(220, 242, 191)"
        btn.style.color = "rgb(0, 0, 0)"

        element.hidden = false;
    }
}

