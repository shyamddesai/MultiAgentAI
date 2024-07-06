function toggleTick(element) {
    element.classList.toggle('selected');
    checkSelectedAvatars();
}

function checkSelectedAvatars() {
    const avatars = document.querySelectorAll('.avatar.selected');
    const continueButton = document.getElementById('continueButton');
    if (avatars.length > 0) {
        continueButton.disabled = false;
    } else {
        continueButton.disabled = true;
    }
}

function showPopup() {
    const popup = document.getElementById('popup');
    popup.classList.toggle('hidden');
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const popup = document.getElementById('popup');
        if (!popup.classList.contains('hidden')) {
            popup.classList.add('hidden');
        }
    }
});

document.getElementById('selectionForm').addEventListener('submit', function(event) {
    const selectedAvatars = document.querySelectorAll('.avatar.selected');
    const selectedValues = Array.from(selectedAvatars).map(avatar => avatar.getAttribute('data-value'));
    document.getElementById('selectedAvatars').value = selectedValues.join(',');
});