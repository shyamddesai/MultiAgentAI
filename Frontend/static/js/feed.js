// Handle sidebar link navigation
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

// Handle news card click to display PDF in slideover
document.querySelectorAll('.news-card').forEach(card => {
    card.addEventListener('click', function() {
        const pdf = this.getAttribute('data-pdf');
        const title = this.getAttribute('data-title');
        if (pdf) {
            const slideover = document.getElementById('slideover');
            const contentSection = this.closest('.content-section');
            const cardTop = this.getBoundingClientRect().top - contentSection.getBoundingClientRect().top;

            slideover.style.top = `${cardTop}px`;
            slideover.style.height = `${contentSection.clientHeight - cardTop}px`;
            slideover.style.display = 'flex';

            document.getElementById('pdf-frame').src = `/pdf/${pdf}`;
            document.getElementById('slideover-title').textContent = title;
        }
    });
});

// Handle Escape key to close slideover
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeSlideover();
    }
});

// Handle 'x' button click to close slideover
document.getElementById('slideover-close').addEventListener('click', function() {
    closeSlideover();
});

function closeSlideover() {
    document.getElementById('slideover').style.display = 'none';
    document.getElementById('pdf-frame').src = '';
    document.getElementById('slideover-title').textContent = '';
}