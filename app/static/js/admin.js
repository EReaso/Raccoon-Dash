document.querySelector("#photo_upload_form").onsubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const response = await fetch("/photos/", {
    method: "POST",
    body: formData
  });
  if (response.ok) {
    location.reload();
  } else {
    alert("Failed to upload photo");
  }
}

let currentPhotoUrl = '';

document.querySelectorAll('.photo-thumbnail').forEach(img => {
  img.addEventListener('click', function() {
    currentPhotoUrl = this.dataset.photoUrl;
    document.getElementById('modalImage').src = currentPhotoUrl;
  });
});

document.getElementById('deletePhotoBtn').addEventListener('click', async function() {
  if (confirm('Are you sure you want to delete this image?')) {
    let response = await fetch(currentPhotoUrl, {
      method: 'DELETE'
    });
    if (response.ok) {
      location.reload();
    } else {
      alert('Error deleting image');
    }
  }
});

// Delete all photos confirmation
const deleteConfirmInput = document.getElementById('deleteConfirmInput');
const confirmDeleteAllBtn = document.getElementById('confirmDeleteAllBtn');

deleteConfirmInput.addEventListener('input', function() {
    confirmDeleteAllBtn.disabled = this.value.toLowerCase() !== 'delete';
});

confirmDeleteAllBtn.addEventListener('click', async function() {
    if (deleteConfirmInput.value.toLowerCase() === 'delete') {
        try {
            const response = await fetch('/photos/', {
                method: 'DELETE'
            });
            
            if (response.ok) {
                location.reload();
            } else {
                alert('Error deleting photos');
            }
        } catch (error) {
            alert('Error deleting photos');
        }
    }
});

// Clear confirmation input when modal is hidden
document.getElementById('deleteAllModal').addEventListener('hidden.bs.modal', function() {
    deleteConfirmInput.value = '';
    confirmDeleteAllBtn.disabled = true;
});
