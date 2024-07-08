document.addEventListener("DOMContentLoaded", function() {
    const e = document.getElementById("current-date"),
        t = { day: "numeric", month: "long" },
        n = new Date().toLocaleDateString("en-US", t);
    e.textContent = n;
});

function closeSummaryModal(event) {
    event.stopPropagation();
    const modal = document.getElementById('summary-modal');
    modal.classList.remove('show');
}

function closeLinkModal(event) {
    event.stopPropagation();
    const modal = document.getElementById('link-modal');
    modal.classList.remove('show');
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeSummaryModal(event);
        closeLinkModal(event);
    }
});

function openSummaryModal(title, summary, imageUrl) {
    const modal = document.getElementById('summary-modal');
    document.getElementById('summary-modal-title').innerText = title;
    document.getElementById('summary-modal-summary').innerText = summary;
    document.getElementById('summary-modal-image').src = imageUrl;
    modal.classList.add('show');
}

function openLinkModal(title, url) {
    const modal = document.getElementById('link-modal');
    document.getElementById('link-modal-title').innerText = title;
    document.getElementById('link-modal-url').href = url;
    modal.classList.add('show');
}