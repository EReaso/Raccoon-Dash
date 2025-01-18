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
      if (this.interval != undefined) {
        clearInterval(this.interval)
      }
      this.interval = setInterval(this.showNextPhoto, delay);
    }

    clearAutoRotate() {
      if (this.interval !== undefined) {
        clearInterval(this.interval)
      }
    }
  }


  // Initializes the screensaver by shuffling images
  const initializeScreensaver = () => {
    // shuffle the image array defined in HTML
    shuffleArray(images);
    const screensaver = new Screensaver(window.images, window.screensaver_delay, document.getElementById('screensaver'));
    screensaver.setAutoRotate();
  };

  initializeScreensaver();
});
