

function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2)
    return parts.pop().split(';').shift();
}

function submitFunction(id){
    const textAreaValue = document.getElementById(`textarea_${id}`).value
    const content = document.getElementById(`content_${id}`);
    const modal = document.getElementById(`modal_edit_post_${id}`); 
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            content: textAreaValue
        })

    })
    .then(response => response.json())
    .then(result => {
        content.innerHTML = result.data; 

        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');

        const modalsBackdrops = document.getElementsByClassName('modal-backdrop');

        for(let i=0; i < modalsBackdrops.length; i++){
            document.body.removeChild(modalsBackdrops[i]);

        }
    })

}
function likeFunction(id) {
    const i = document.getElementById(id);
    const likesCountSpan = document.getElementById(`likes-count_${id}`);

    fetch(`/post_data/${id}`)
        .then(response => response.json())
        .then(postData => {
            const hasLiked = postData.has_liked;

            const likeURL = hasLiked ? `/delete_like/${id}` : `/add_like/${id}`;

            fetch(likeURL)
                .then(response => response.json())
                .then(result => {
                    if (hasLiked) {                
                        i.classList.remove('fa-thumbs-up');
                        i.classList.add('fa-thumbs-down');
                    } else {
                        i.classList.remove('fa-thumbs-down');
                        i.classList.add('fa-thumbs-up');
                    }            
                    likesCountSpan.textContent = result.likes_count;
                });
        });
}

/*
function likeFunction(id) {
    const i = document.getElementById(id);
    //const isThumbsUp = i.classList.contains('fa-thumbs-up');
    const likesCountSpan = document.getElementById(`likes-count_${id}`);

    const likeURL = isThumbsUp ? `/delete_like/${id}` : `/add_like/${id}`;

    fetch(likeURL)
        .then(response => response.json())
        .then(result => {
            if (isThumbsUp) {                
                i.classList.remove('fa-thumbs-up');
                i.classList.add('fa-thumbs-down');
            } else {
                i.classList.remove('fa-thumbs-down');
                i.classList.add('fa-thumbs-up');
            }            
            likesCountSpan.textContent = result.likes_count;
        });
}*/


