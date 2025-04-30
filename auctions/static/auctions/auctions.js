document.addEventListener("DOMContentLoaded", () => {
    setupWatchlistButtons();
    setupBidForm();
    setupLikeButton();
    setupCommentForm();
});

// Toggle watchlist
function setupWatchlistButtons() {
    document.querySelectorAll(".watchlist-button").forEach(button => {
        button.onclick = () => {
            const title = button.dataset.listing;

            fetch(`/watch/${title}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                button.classList.toggle("btn-secondary", data.watchlist);
                button.classList.toggle("btn-outline-secondary", !data.watchlist);
                button.textContent = data.watchlist ? "- Watchlist" : "+ Watchlist";
            });
        };
    });
}

// Submit bid
function setupBidForm() {
    const bidForm = document.querySelector("#bid-form");
    if (!bidForm) return;

    bidForm.onsubmit = e => {
        e.preventDefault();

        const input = document.querySelector("#bid-input");
        const bid = parseFloat(input.value);
        const title = bidForm.dataset.listing;
        const message = document.querySelector("#bid-message");

        if (isNaN(bid)) {
            message.innerText = "Please enter a valid number";
            message.className = "alert alert-danger";
            return;
        }

        fetch(`/bid/${title}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({ bid: bid.toString() })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || 'Bid failed');
                });
            }
            return response.json();
        })
        .then(data => {
            message.innerText = data.message;
            message.className = `alert ${data.success ? "alert-success" : "alert-danger"}`;

            if (data.success) {
                document.querySelector("#current-price").innerText = `$${data.new_price}`;
                document.querySelector("#bid-count").innerText = `${data.bid_count} bid(s) so far.`;
                input.value = ""; // Clear the input field
            }
        })
        .catch(error => {
            message.innerText = error.message || "An error occurred. Please try again.";
            message.className = "alert alert-danger";
        });
    };
}

// Toggle like
function setupLikeButton() {
    const likeButton = document.querySelector("#like-button");
    if (!likeButton) return;

    likeButton.onclick = () => {
        const listingId = likeButton.dataset.listingId;

        fetch(`/like/${listingId}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            document.querySelector("#like-count").innerText = data.likes_count;
            const icon = likeButton.querySelector("i");

            likeButton.classList.toggle("btn-danger", data.liked);
            likeButton.classList.toggle("btn-outline-danger", !data.liked);
            icon.className = data.liked ? "bi bi-heart-fill" : "bi bi-heart";
        });
    };
}

// Submit comment
function setupCommentForm() {
    const commentForm = document.querySelector("#comment-form");
    if (!commentForm) return;

    commentForm.onsubmit = e => {
        e.preventDefault();

        const commentText = document.querySelector("#comment-input").value;
        const title = commentForm.dataset.listing;

        fetch(`/comment/${title}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            body: new URLSearchParams({ comment: commentText })
        })
        .then(res => res.json())
        .then(data => {
            if (data.username && data.comment) {
                const commentSection = document.querySelector("#comments-section");
                const newComment = document.createElement("div");
                newComment.innerHTML = `
                    <h5 style="color:blue;">${data.username}</h5>
                    <p>${data.comment}</p>
                    <hr>
                `;
                commentSection.prepend(newComment);
                document.querySelector("#comment-input").value = "";
            }
        });
    };
}

// Utility: get CSRF token
function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}
