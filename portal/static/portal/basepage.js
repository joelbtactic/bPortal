if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/serviceworker.js')
}
window.addEventListener('offline', function () {
    const popup = document.getElementById('offline-notification');
    popup.classList.toggle("show");

    setTimeout(() => {
        popup.classList.remove('show');
    }, 3000);
});

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function (event) {
            if (!navigator.onLine) {
                event.preventDefault();
                const popup = document.getElementById('offline-notification');
                popup.classList.toggle("show");

                setTimeout(() => {
                    popup.classList.remove('show');
                }, 3000);
            }
        });
    });
});
