document.addEventListener('DOMContentLoaded', () => {
    //manage bookmarks
    fetch('get_user_bookmarks').then(response => response.json()).then(data => {
        manage_bookmarks(data.article_urls)
    })

    document.querySelectorAll(".far").forEach(bookmark => {
        bookmark.onclick = function(event) {
            let bookmark = event.target

            let article = {
                "type": "bookmark",
                "title": bookmark.parentElement.querySelector('.card-title').innerHTML,
                "card_description": bookmark.parentElement.querySelector('.card-text').innerHTML,
                "image_url": bookmark.parentElement.parentElement.querySelector('img').src,
                "url": bookmark.parentElement.querySelector('.read').href
            }

            fetch('manage_bookmark', {
                method: "POST", 
                body: JSON.stringify(article),
                headers: {"Content-type": "application/json; charset=UTF-8"}
            }).then(response => response.json()).then(res => {
                console.log(res);
                bookmark.parentElement.querySelector(".far").style.display = 'none';
                bookmark.parentElement.querySelector(".fas").style.display = 'block';
            }).catch(error => {
                alert(error);
            })
        }
    })
})


function manage_bookmarks(article_urls) {
    document.querySelectorAll('.read').forEach((event) => {
        if (article_urls.includes(event.href) == true) {
            event.parentElement.querySelector('.far').style.display = 'none';
        } else {
            event.parentElement.querySelector('.fas').style.display = 'none';
        }
    })
}