function showCommentComments(id) {
    var element = document.getElementById("comment-comments-list-container-" + id);
    var btn = document.getElementById("btn-comment-comments-list-container-" + id);
    if (element.style.display === "none" || element.style.display === "") {
        btn.innerHTML = "Close comments";
        element.style.display = "block";
    } else {
        btn.innerHTML = "Show comments";
        element.style.display = "none";
    }
}

function showComments(id) {
    var element = document.getElementById("comments-list-container-" + id);
    var btn = document.getElementById("btn-comments-list-container-" + id);
    if (element.style.display === "none" || element.style.display === "") {
        btn.innerHTML = "Close comments";
        element.style.display = "block";
    } else {
        btn.innerHTML = "Show comments";
        element.style.display = "none";
    }
}