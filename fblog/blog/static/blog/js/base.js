function showCommentComments(id) {
    var element = document.getElementById("comment-comments-list-container-" + id);
    var btn = document.getElementById("btn-comment-comments-list-container-" + id);
    if (element.style.display === "none" || element.style.display === "") {
        btn.innerHTML = "Close replies";
        btn.style.backgroundColor = "rgb(220, 242, 191)"
        btn.style.color = "rgb(0, 0, 0)"
        element.style.display = "block";
    } else {
        btn.innerHTML = "Show replies";
        btn.style.backgroundColor = "rgb(0, 0, 0)"
        btn.style.color = "rgb(220, 242, 191)"
        element.style.display = "none";
    }
}

function showComments(id) {
    var element = document.getElementById("comments-list-container-" + id);
    var btn = document.getElementById("btn-comments-list-container-" + id);
    if (element.style.display === "none" || element.style.display === "") {
        btn.innerHTML = "Close comments";
        btn.style.backgroundColor = "rgb(220, 242, 191)"
        btn.style.color = "rgb(0, 0, 0)"
        element.style.display = "block";
    } else {
        btn.innerHTML = "Show comments";
        btn.style.backgroundColor = "rgb(0, 0, 0)"
        btn.style.color = "rgb(220, 242, 191)"
        element.style.display = "none";
    }
}

