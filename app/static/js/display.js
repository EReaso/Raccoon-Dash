let drawer = document.querySelector("#drawer");
let drawer_btn = document.querySelector("#drawer_btn");

drawer_btn.onclick = () => {
  if (drawer.classList.contains("d-none")) {
    drawer.classList.remove("d-none");
    drawer_btn.innerHTML = ">";
  } else {
    drawer.classList.add("d-none");
    drawer_btn.innerHTML = "<";
  }
}

// Screensaver functionality
let inactivityTimer;
let debounceTimer;

function resetInactivityTimer() {
  clearTimeout(inactivityTimer);
  clearTimeout(debounceTimer);
  // Only set timer if screensaver delay is greater than 0
  if (screensaver_delay > 0) {
    inactivityTimer = setTimeout(() => {
      window.location.href = "/screensaver/";
    }, screensaver_delay * 1000);  // Convert seconds to milliseconds
  }
}

function debounceResetInactivityTimer() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(resetInactivityTimer, 200);  // 200ms debounce
}

// Only set up event listeners if screensaver is enabled
if (screensaver_delay > 0) {
  // Reset timer on any interaction
  document.addEventListener('mousemove', resetInactivityTimer);
  document.addEventListener('keypress', resetInactivityTimer);
  document.addEventListener('click', resetInactivityTimer);
  document.addEventListener('touchstart', debounceResetInactivityTimer);

  // Initial setup of timer
  resetInactivityTimer();
}

// Generate QR code when modal is shown
document.getElementById('qrModal').addEventListener('show.bs.modal', function () {
  const canvas = document.getElementById('qrcode');

  // Use the server's IP address instead of localhost
  const port = window.location.port;
  const adminUrl = `http://${window.location.hostname}${port ? ':' + port : ''}/`;

  // Generate QR code
  QrCreator.render({
    text: adminUrl,
    radius: 0.5,
    ecLevel: 'H',
    fill: '#000000',
    background: '#ffffff',
    size: 256
  }, canvas);
});
