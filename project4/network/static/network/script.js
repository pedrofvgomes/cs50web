document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.post h4').forEach(element => {
        element.addEventListener('click', function () {
            window.location.href = element.textContent;
        });
    });

    const postsContainer = document.getElementById('posts'); // Change this to the actual ID of the posts container

    postsContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('edit')) {
            let post = event.target.parentElement;
            const postContent = post.querySelector('p').textContent;
            post.querySelector('p').outerHTML = `
                <textarea name="text" id="text" maxlength="280"
                style="width: 100%; resize: none;" rows="3" spellcheck="false">${postContent}</textarea>
                <a class="btn btn-sm btn-outline-primary save">Save</a>
            `;

            const saveButton = post.querySelector('.save');
            saveButton.addEventListener('click', function () {
                const editedContent = post.querySelector('textarea').value;
                // Implement your fetch code here to update the content on the server
                fetch('/edit/' + post.id + '/' + editedContent)
                .then(() => {
                    // After updating the post on the server, update the UI with the new content.
                    post.innerHTML = `
                        <h4>${post.querySelector('h4').textContent}</h4>
                        <a class="edit">Edit</a>
                        <p>${editedContent}</p>
                        <span>${post.querySelector('span').textContent}</span>
                        <br>
                        <div class="likes">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
                            </svg>
                            <span>${post.querySelector('.likes span').textContent}</span>
                        </div>
                        <span>Comment</span>
                    `;
                });
            });
        };
    });

    let likebuttons = document.querySelectorAll('.likebutton');
    likebuttons.forEach(like => {
        like.addEventListener('click', function(){
            // fetch no url
            let post = like.parentElement.parentElement;
            fetch('/like/' + post.id.toString())
            .then(response => response.json())
            .then(status => {
                if (status == 'Added'){
                    let likecount = post.querySelector('.likes span');
                    likecount.textContent = (Number(likecount.textContent) + 1).toString();
                    
                    let icon = post.querySelector('svg');
                    icon.setAttribute('fill', 'red');
                    icon.classList.remove('bi-heart');
                    icon.classList.add('bi-heart-fill');
                    icon.innerHTML = `<path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>`;
                }
                if (status == 'Removed'){
                    let likecount = post.querySelector('.likes span');
                    likecount.textContent = (Number(likecount.textContent) - 1).toString();

                    let icon = post.querySelector('svg');
                    icon.setAttribute('fill', 'currentColor');
                    icon.classList.remove('bi-heart-fill');
                    icon.classList.add('bi-heart');
                    icon.innerHTML = `<path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>`;
                }
            })
        })
    });
});
