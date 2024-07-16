// Handle sidebar link navigation with smooth scrolling
document.querySelectorAll('.sidebar-link').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);
        showSection(targetSection);
        targetSection.scrollIntoView({ behavior: 'smooth' });  // Smooth scrolling
    });
});

function showSection(targetSection) {
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    targetSection.classList.add('active');
}

// Handle news card click to display PDF in slideover with smooth animation
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
            slideover.classList.add('open');  // Add class for smooth animation
            slideover.style.visibility = 'visible';
            slideover.style.opacity = '1';

            document.getElementById('pdf-frame').src = `/pdf/${pdf}`;
            document.getElementById('slideover-title').textContent = title;
        }
    });
});

// Handle Escape key to close slideover with smooth animation
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeSlideover();
    }
});

function closeSlideover() {
    const slideover = document.getElementById('slideover');
    slideover.classList.remove('open');  // Remove class for smooth animation
    slideover.style.opacity = '0';
    setTimeout(() => {
        slideover.style.visibility = 'hidden';
        document.getElementById('pdf-frame').src = '';
        document.getElementById('slideover-title').textContent = '';
    }, 300);  // Match the duration of the CSS transition
}

// Make the page automatically scroll to the the news card that is animating
document.addEventListener('DOMContentLoaded', function() {
    const newsCards = document.querySelectorAll('.news-card-container .news-card');
    const counters = document.querySelectorAll('.animated-number');
    const trendText = document.querySelector('.trend-text');
    const trendTarget = trendText.getAttribute('data-target');
    const trendAlternates = ["Bearish", "Bullish"];
    let trendIndex = 0;

    function animateCounter(counter, callback) {
        const target = +counter.getAttribute('data-target');
        const increment = target / 100;
        let currentNumber = 0;

        const updateCounter = setInterval(() => {
            currentNumber += increment;
            counter.innerText = Math.ceil(currentNumber);
            if (currentNumber >= target) {
                clearInterval(updateCounter);
                counter.innerText = target;
                if (callback) callback();
            }
        }, 30);
    }

    function animateTrend(callback) {
        const trendInterval = setInterval(() => {
            trendText.innerText = trendAlternates[trendIndex];
            trendIndex = (trendIndex + 1) % trendAlternates.length;
        }, 500);

        setTimeout(() => {
            clearInterval(trendInterval);
            trendText.innerText = trendTarget;
            if (callback) callback();
        }, 5000); // Switch for 5 seconds
    }

    function showCard(index) {
        if (index >= newsCards.length) return;
        const card = newsCards[index];
        card.classList.add('active', 'glowing-border');

        // Scroll to the card
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });

        if (index < counters.length) {
            animateCounter(counters[index], () => {
                card.classList.remove('glowing-border');
                showCard(index + 1);
            });
        } else {
            animateTrend(() => {
                card.classList.remove('glowing-border');
                showCard(index + 1);
            });
        }
    }

    showCard(0);
});