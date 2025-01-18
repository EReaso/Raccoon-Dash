/* Randomize array in-place using Durstenfeld shuffle algorithm */
function shuffleArray(array) {
  for (let i = array.length - 1; i >= 0; i--) {
    let j = Math.floor(Math.random() * (i + 1));
    let temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  class Screensaver {
    constructor(images = [], delay = 0, elem) {
      this.images = images;
      this.n = -1;
      this.delay = delay;
      this.elem = elem;
      this.showNextPhoto();
    }

    showNextPhoto = () => {
      if (this.n < this.images.length - 1) {
        this.n++;
      } else {
        this.n = 0;
      }
      this.elem.setAttribute("src", `/photo/${images[this.n]}/`);
    };

    setAutoRotate(delay = this.delay) {
      if (this.interval !== undefined) {
        clearInterval(this.interval)
      }
      this.interval = setInterval(this.showNextPhoto, delay);
    }

    showPreviousPhoto = () => {
      if (this.n > 0) {
        this.n--;
      } else {
        this.n = this.images.length - 1;
      }
      this.elem.setAttribute("src", `/photo/${images[this.n]}/`);
    }
  }


  // Initializes the screensaver by shuffling images
  const initializeScreensaver = () => {
    // shuffle the image array defined in HTML
    shuffleArray(images);
    const screensaver = new Screensaver(window.images, window.screensaver_delay, document.getElementById('screensaver'));
    document.getElementById("forward_btn").onclick = screensaver.showNextPhoto;
    document.getElementById("back_btn").onclick = screensaver.showPreviousPhoto;
    screensaver.setAutoRotate();
  };

  // Exit screensaver on any user interaction, excluding button presses
  const exitScreensaver = (event) => {
    // Check if the event came from the buttons
    const targetElement = event.target;
    if (
        targetElement.id === "forward_btn" || // Ignore forward button
        targetElement.id === "back_btn" || // Ignore backward button
        targetElement.closest("#forward_btn") || // Ignore forward button icon
        targetElement.closest("#back_btn") // Ignore backward button icon
    ) {
       // Don't trigger screensaver exit
    } else {
      location.href = "/display/"
    }

  };

  // Attach event listeners for user interaction
  document.addEventListener("mousemove", exitScreensaver);
  document.addEventListener("keypress", exitScreensaver);
  document.addEventListener("click", exitScreensaver);
  document.addEventListener("touchstart", exitScreensaver);

  initializeScreensaver();
});
