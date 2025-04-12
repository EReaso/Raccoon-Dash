document.addEventListener("DOMContentLoaded", function () {
  var toastElList = [].slice.call(document.querySelectorAll('.toast'));
  toastElList.forEach(function (toastEl) {
    var toast = new bootstrap.Toast(toastEl, {delay: 5000});
    toast.show();
  });
});

function connectWebSocket(retries = 0) {
  const socket = new WebSocket('ws://' + location.host + '/reload/');

  socket.addEventListener('message', function (event) {
    if (event.data === 'reload') {
      window.location.reload();
    }
  });

  socket.addEventListener('error', function (event) {
    console.error('WebSocket error:', event);
  });

  socket.addEventListener('close', function () {
    const delay = Math.min(10000, Math.pow(2, retries) * 1000);
    console.log(`WebSocket closed. Reconnecting in ${delay / 1000}s...`);
    setTimeout(() => connectWebSocket(), delay);
  });
}

connectWebSocket();
