document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('[id^="btn-like-"]').forEach(btn => {
        const postId = btn.dataset.postId; // data-post-id
        const userId = btn.dataset.userId; // data-user-id

        btn.addEventListener("click", function() {
            fetch(`/like/post/${postId}/${userId}`)
                .then(response => response.json())
                .then(data => {
                    label = document.getElementById('label-post-like-' + postId)
                    if (data.liked) {
                        btn.innerHTML = "unlike";
                        label.innerHTML = parseInt(label.innerHTML, 10) + 1
                    }
                    else {
                        btn.innerHTML = "like";
                        label.innerHTML = parseInt(label.innerHTML, 10) - 1
                    }
                });
        });
    });
});