document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("comment-form").addEventListener("submit", function(e) {
        e.preventDefault();

        let formData = new FormData(this);
        fetch("{% url 'task-comment' task.id %}", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                let commentSection = document.getElementById("comment-list");
                let newComment = document.createElement("li");
                newComment.innerHTML = `<strong>${data.user}</strong>: ${data.text} <br><small>${data.created_at}</small>`;
                commentSection.prepend(newComment);
                document.getElementById("comment-form").reset();
            }
        })
        .catch(error => console.error("Error:", error));
    });

    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", function () {
            let commentId = this.getAttribute("data-comment-id");
            let taskId = this.getAttribute("data-task-id");
            let newText = prompt("Enter new comment text:");

            if (newText) {
                let url = `/task/${taskId}/comment/${commentId}/edit/`;

                
                fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({text: newText})
                })

                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        let commentElement = document.querySelector(`#comment-${commentId}`);
                        commentElement.querySelector(".comment-text").textContent = data.text;
                    } else {
                        alert("Помилка редагування");
                    }
                })
                .catch(error => console.error("Fetch error:", error));

            }
        })
    })

    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function () {
            let commentId = this.getAttribute("data-comment-id");
            let taskId = this.getAttribute("data-task-id");
        
            let confirmDelete = confirm("Are you sure you want to delete this comment?");
            if (!confirmDelete) return;

            let url = `/task/${taskId}/comment/${commentId}/delete/`;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json"
                }
            })

            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    let commentElement = document.querySelector(`#comment-${commentId}`);
                    commentElement.remove();
                } else {
                    alert("Помилка видалення!");
                }
            })
            .catch(error => console.error("Fetch error:", error));
            
        })
    })

    document.querySelectorAll(".like-btn").forEach(button => {
        button.addEventListener("click",  function () {
            let commentId = this.getAttribute("data-comment-id");
            let taskId = this.getAttribute("data-task-id");

            let url = `/task/${taskId}/comment/${commentId}/like`;

            
            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json"
                }
            })


            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    let likeCount = document.querySelector(`#like-count-${commentId}`);
                    likeCount.textContent = data.likes;
                }
            })
                
        })
    });
    

   document.querySelectorAll(".dislike-btn").forEach(button => {
        button.addEventListener("click", async function () {
            let commentId = this.getAttribute("data-comment-id");
            let taskId = this.getAttribute("data-task-id");

            let url = `/task/${taskId}/comment/${commentId}/dislike`;

            try {
                let response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    },
                    body: JSON.stringify({})
                })

                if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

                let data = await response.json();
                document.getElementById(`dislike-count-${commentId}`).  innerHTML = data.dislikes;
            
            } catch (error) {
                console.error("Fetch error:", error);
            }
        });
   });

});