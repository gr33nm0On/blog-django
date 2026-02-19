document.addEventListener("submit", function(e) {
    if (e.target.classList.contains('ajax-form')) {
        e.preventDefault();

        const formData = new FormData(e.target);

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        formData.append('csrfmiddlewaretoken', csrftoken);

        fetch(e.target.action, {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (e.target.dataset.type === "post") {
                    const container = document.getElementById("post-container");
                    container.insertAdjacentHTML("afterbegin", data.html);
                }
                else if (e.target.dataset.type === "comment") {
                    const container = document.getElementById(`comment-container-${e.target.dataset.postId}`);
                    container.innerHTML = data.html;
                }
                e.target.reset();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});