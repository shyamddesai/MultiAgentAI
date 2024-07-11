document.querySelectorAll('.sidebar-link').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);
        showSection(targetSection);
    });
});

function showSection(targetSection) {
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    targetSection.classList.add('active');
}