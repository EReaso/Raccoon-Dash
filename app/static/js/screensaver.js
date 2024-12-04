// Get references to elements
const currentImage = document.getElementById('current-image');
const nextImage = document.getElementById('next-image');

// Total number of images
const totalImages = document.getElementById("total-images").value

// Current image index
let currentImageIndex = 0;

// Function to display the current image
function displayCurrentImage() {
    currentImage.style.display = 'block';
    nextImage.style.display = 'none';
}

// Function to preload the next image
function preloadNextImage() {
    const nextImageIndex = (currentImageIndex + 1) % totalImages;
    nextImage.src = `/screensaver/image/?num=${nextImageIndex}`;

}

// Initial setup
displayCurrentImage();
preloadNextImage();

// Automatic slideshow (adjust interval as needed)
/*setInterval(() => {
    currentImageIndex = (currentImageIndex + 1) % totalImages;
    preloadNextImage();
}, 3000);*/
