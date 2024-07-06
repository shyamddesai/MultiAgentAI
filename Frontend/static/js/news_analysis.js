document.addEventListener('DOMContentLoaded', function() {
    const articlesList = document.getElementById('articles-list');
    const newsData = JSON.parse(document.getElementById('news-data').textContent);
    const reportContent = document.getElementById('report-content');
    const reportData = JSON.parse(document.getElementById('report-data').textContent);
    const loadingBar = document.getElementById('loading-bar');
    const progressBar = loadingBar.querySelector('.progress-bar');
    const toast = new bootstrap.Toast(document.getElementById('toast-notification'));
    const timelineChart = document.getElementById('timeline-chart');

    document.getElementById('total-articles-counter').addEventListener('click', function() {
        // Handle click event for total articles counter
    });

    document.getElementById('export-pdf').addEventListener('click', function() {
        // Handle export as PDF functionality
    });

    // Initialize particles.js
    particlesJS('particles-js-news', {
        "particles": {
            "number": {
                "value": 80,
                "density": {
                    "enable": true,
                    "value_area": 800
                }
            },
            "color": {
                "value": "#ffffff"
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                },
                "polygon": {
                    "nb_sides": 5
                },
                "image": {
                    "src": "img/github.svg",
                    "width": 100,
                    "height": 100
                }
            },
            "opacity": {
                "value": 0.5,
                "random": false,
                "anim": {
                    "enable": false,
                    "speed": 1,
                    "opacity_min": 0.1,
                    "sync": false
                }
            },
            "size": {
                "value": 3,
                "random": true,
                "anim": {
                    "enable": false,
                    "speed": 40,
                    "size_min": 0.1,
                    "sync": false
                }
            },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#ffffff",
                "opacity": 0.4,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 6,
                "direction": "none",
                "random": false,
                "straight": false,
                "out_mode": "out",
                "bounce": false,
                "attract": {
                    "enable": false,
                    "rotateX": 600,
                    "rotateY": 1200
                }
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "repulse"
                },
                "onclick": {
                    "enable": true,
                    "mode": "push"
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 400,
                    "line_linked": {
                        "opacity": 1
                    }
                },
                "bubble": {
                    "distance": 400,
                    "size": 40,
                    "duration": 2,
                    "opacity": 8,
                    "speed": 3
                },
                "repulse": {
                    "distance": 200,
                    "duration": 0.4
                },
                "push": {
                    "particles_nb": 4
                },
                "remove": {
                    "particles_nb": 2
                }
            }
        },
        "retina_detect": true
    });

    // Example function to update the progress bar
    function updateProgressBar(percentage) {
        progressBar.style.width = percentage + '%';
    }

    // Example function to show a toast notification
    function showToast(message) {
        document.querySelector('.toast-body').textContent = message;
        toast.show();
    }

    // Example function to render the timeline chart using Chart.js
    function renderTimelineChart(data) {
        new Chart(timelineChart, {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day'
                        }
                    }
                }
            }
        });
    }

    // Call the renderTimelineChart function with the report data
    renderTimelineChart(reportData);
});
