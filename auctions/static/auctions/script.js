document.addEventListener('DOMContentLoaded', () => {
    // Dropdown menu hovering
    dropdown = document.querySelector('.dropdown');
    menu = document.querySelector('.dropdown-menu');

    dropdown.addEventListener('mouseover', () => {
        menu.style.display = 'block';
    })
    dropdown.addEventListener('mouseout', () => {
        menu.style.display = 'none';
    })

    // Notifications
    const message = document.querySelector('.alert');
    if(message) {
        setTimeout(fadeOut, 3000);
    }
});

function fadeOut() {
    element = document.querySelector('.alert');
    var oppacityArray = ["0.9", "0.8", "0.7", "0.6", "0.5", "0.4", "0.3", "0.2", "0.1", "0"];
    var i = 0;
    (function next() {
        element.style.opacity = oppacityArray[i];
        if(++i < oppacityArray.length) {
            setTimeout(next, 180);
        }
    })();
}