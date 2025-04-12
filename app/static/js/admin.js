document.addEventListener("DOMContentLoaded", function () {
  const colors = JSON.parse(document.getElementById("theme_colors_object").value)

  function toSixDigitHex(color) {
    if (color.length === 4) {
      return '#' + color[1] + color[1] + color[2] + color[2] + color[3] + color[3];
    }
    return color;
  }

  Object.keys(colors).forEach(name => {
    const input = document.getElementById(name + "_color_input");
    if (input) {
      input.value = toSixDigitHex(getComputedStyle(document.documentElement).getPropertyValue(`--bs-${name}`).trim());
    }
  });
});


document.querySelector("#photo_upload_form").onsubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const response = await fetch("/photos/", {
    method: "POST", body: formData
  });
  if (response.ok) {
    location.reload();
  } else {
    alert("Failed to upload photo");
  }
}


let modalImageUrl = ""

document.querySelectorAll('.photo-thumbnail').forEach(img => {
  img.addEventListener('click', function () {
    modalImageUrl = this.dataset.photoUrl;
    document.getElementById('modalImage').src = modalImageUrl;
  });
});

document.getElementById('deletePhotoBtn').addEventListener('click', async function () {
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

fetch("/font_url/")
.then(res => {
  if (!res.ok) {
    throw new Error(`HTTP error! Status: ${res.status}`);
  }
  return res.text();
})
.then(data => document.querySelector("#font_url_input").value = data);
