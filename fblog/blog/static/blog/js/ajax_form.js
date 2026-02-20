document.addEventListener("submit", function(e) {
    if (!e.target.classList.contains('ajax-form')) {
        return;
    }

    e.preventDefault();

    const submitButtons = e.target.querySelectorAll('button[type="submit"], input[type="submit"]');
    submitButtons.forEach(btn => {
        btn.disabled = true;
    });

    const formData = new FormData(e.target);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    if (!csrftoken) {
        console.error('CSRF token not found');
        submitButtons.forEach(btn => btn.disabled = false);
        return;
    }

    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(e.target.action, {
        method: "POST",
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success) {
            const formType = e.target.dataset.type;

            if (formType === "post") {
                const container = document.getElementById("post-container");
                if (container) {
                    container.insertAdjacentHTML("afterbegin", data.html);
                }
            }
            else if (formType === "comment") {
                const parentId = e.target.dataset.parentId;
                const postId = e.target.dataset.postId;
                const commentId = e.target.dataset.commentId;

                if (parentId === "" || parentId) {
                    const container = document.getElementById(`comment-container-${postId}-${commentId}`);
                    const btn = document.getElementById(`btn-comment-container-${postId}-${commentId}`);
                    btn.hidden = false;
                    if (container) {
                        container.insertAdjacentHTML("beforeend", data.html);
                    }
                }
                else if (parentId === undefined) {
                    console.log(postId);
                    const container = document.getElementById(`comment-container-${postId}`);
                    const btn = document.getElementById(`btn-comment-container-${postId}`);
                    btn.hidden = false;
                    if (container) {
                        container.insertAdjacentHTML("beforeend", data.html);
                    }
                }
            }
            e.target.reset();
        }
    });
});