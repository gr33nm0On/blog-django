document.addEventListener("DOMContentLoaded", function() {
        let page = 2;
        const btn = document.getElementById("load-more");
        const container = document.getElementById("post-container");

        btn.addEventListener("click", function() {
            fetch(`/post/load/?page=${page}`)
                .then(
                    function(response) { return response.json(); }
                )
                .then(function(data) {
                    container.insertAdjacentHTML("beforeend", data.html);
                    if (!data.has_next) {
                        btn.style.display = "none";
                    }
                    page++;
                }
                );
        });
    });