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

document.addEventListener('DOMContentLoaded', function() {
    const searchBox = document.getElementById('searchBox');
    const addButton = document.getElementById('addButton');
    const popup = document.getElementById('popup');
    const addAvatar = document.querySelector('.add-avatar');

    searchBox.addEventListener('input', function() {
        if (searchBox.value.trim() !== '') {
            addButton.classList.add('active');
            addButton.disabled = false;
        } else {
            addButton.classList.remove('active');
            addButton.disabled = true;
        }
    });

    addButton.addEventListener('click', function() {
        const newValue = searchBox.value.trim();
        if (newValue !== '') {
            const avatarContainer = document.createElement('div');
            avatarContainer.className = 'avatar-container';

            const newAvatar = document.createElement('div');
            newAvatar.className = 'avatar mx-auto';
            newAvatar.dataset.value = newValue;
            newAvatar.onclick = function() {
                toggleTick(this);
            };

            const avatarLabel = document.createElement('div');
            avatarLabel.className = 'avatar-label';
            avatarLabel.textContent = newValue;

            avatarContainer.appendChild(newAvatar);
            avatarContainer.appendChild(avatarLabel);

            addAvatar.replaceWith(avatarContainer);
            popup.classList.add('hidden');
            searchBox.value = '';
            addButton.classList.remove('active');
            addButton.disabled = true;
        }
    });
});
