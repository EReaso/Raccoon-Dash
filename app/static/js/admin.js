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


let modalImageUrl = ""

document.querySelectorAll('.photo-thumbnail').forEach(img => {
  img.addEventListener('click', function() {
    modalImageUrl = this.dataset.photoUrl;
    document.getElementById('modalImage').src = modalImageUrl;
  });
});

document.getElementById('deletePhotoBtn').addEventListener('click', async function() {
  if (confirm('Are you sure you want to delete this image?')) {
    let response = await fetch(modalImageUrl, {
      method: 'DELETE'
    });
    if (response.ok) {
      location.reload();
    } else {
      alert('Error deleting image');
    }
  }
});
