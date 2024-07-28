document.addEventListener('DOMContentLoaded', function() {
    const articlesList = document.getElementById('articles-list');
    const newsData = window.newsData; // Assuming newsData is set globally in HTML
    const reportContent = document.getElementById('report-content');
    const reportData = window.reportData; // Assuming reportData is set globally in HTML
    const loadingBar = document.getElementById('loading-bar');
    const progressBar = loadingBar.querySelector('.progress-bar');
    const toastElement = document.getElementById('regenerate-toast');
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 15000 // 15 seconds
    });
    
    document.getElementById('total-articles-counter').addEventListener('click', function() {
        // Clear existing articles except the counter
        articlesList.innerHTML = '<li class="list-group-item d-flex justify-content-between align-items-center" id="total-articles-counter" style="cursor: pointer;">Total Articles: ' + newsData.length + '<div class="thumbs-buttons"><i class="fas fa-thumbs-up"></i><i class="fas fa-thumbs-down"></i></div></li>';
        
        // Append articles
        newsData.forEach(article => {
            const listItem = document.createElement('li');
            listItem.className = 'list-group-item';
            
            const link = document.createElement('a');
            link.href = article.Link;
            link.target = '_blank';
            link.textContent = article.Title;
            
            const summary = document.createElement('p');
            summary.textContent = article.Summary;

            listItem.appendChild(link);
            listItem.appendChild(summary);
            articlesList.appendChild(listItem);
        });
    });

    document.getElementById('summary-report-tab').addEventListener('click', function() {
        // Clear existing report content
        reportContent.innerHTML = '';
        
        // Append report content
        reportData.forEach(report => {
            const reportItem = document.createElement('div');
            reportItem.className = 'report-item';
            
            const title = document.createElement('h4');
            title.textContent = report.Title;
            
            const summary = document.createElement('p');
            summary.textContent = report.Summary;
            
            reportItem.appendChild(title);
            reportItem.appendChild(summary);
            reportContent.appendChild(reportItem);
        });
    });

    document.getElementById('export-pdf').addEventListener('click', function() {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        let y = 10;
        reportData.forEach(report => {
            doc.setFontSize(16);
            doc.text(report.Title, 10, y);
            y += 10;
            doc.setFontSize(12);
            doc.text(report.Summary, 10, y);
            y += 20;
        });

        doc.save('report.pdf');
    });

    document.getElementById('generate-refresh').addEventListener('click', function() {
        loadingBar.style.display = 'block';
        progressBar.style.width = '0%';
        progressBar.setAttribute('aria-valuenow', 0);

        let progress = 0;
        const interval = setInterval(() => {
            progress += 2; // Slower increment
            progressBar.style.width = progress + '%';
            progressBar.setAttribute('aria-valuenow', progress);

            if (progress >= 100) {
                clearInterval(interval);
                loadingBar.style.display = 'none';
            }
        }, 500); // Slower interval

        // Show toast notification
        toast.show();
    });

    document.getElementById('timeline-tab').addEventListener('click', function() {
        const ctx = document.getElementById('timeline-chart').getContext('2d');
        const timelineChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], // Days of the week
                datasets: [{
                    label: 'Popularity',
                    data: [12, 19, 3, 5, 2, 3, 7], // Mock data
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    tooltip: {
                        enabled: true
                    }
                }
            }
        });
    });

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
});
