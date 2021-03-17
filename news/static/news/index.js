document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('#dl_bookmark').forEach(bookmark => {
        console.log(bookmark);
        bookmark.style.display = 'none';
    })
})