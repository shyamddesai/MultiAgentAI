document.addEventListener('DOMContentLoaded', function() {
    const dateElement = document.getElementById('current-date');
    const options = { day: 'numeric', month: 'long' };
    const today = new Date().toLocaleDateString('en-US', options);
    dateElement.textContent = today;
});

function openModal(title, summary, imageUrl) {
    const modal = document.getElementById('modal');
    const modalContent = document.querySelector('.modal-content');
    const mainContent = document.getElementById('main-content');

    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-summary').textContent = summary;
    document.getElementById('modal-image').src = imageUrl;

    modal.classList.add('show');
    modalContent.classList.add('show');
    mainContent.classList.add('blur'); // Add blur effect to main content
}

function closeModal(event) {
    if (event.target.id === 'modal') {
        const modal = document.getElementById('modal');
        const modalContent = document.querySelector('.modal-content');
        const mainContent = document.getElementById('main-content');

        modal.classList.remove('show');
        modalContent.classList.remove('show');
        mainContent.classList.remove('blur'); // Remove blur effect from main content
    }
}
