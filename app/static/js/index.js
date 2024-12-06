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


// var maxInactivity = 10000;
// let inactivityTimer = setTimeout(() => {
//     window.location.href = "/screensaver/";
// }, maxInactivity)
//
// const resetTimer = () => {
//     clearTimeout(inactivityTimer);
//     inactivityTimer = setTimeout(null, maxInactivity);
// };
//
// window.onload = function () {
//     document.body.onmousemove = resetTimer;
//     document.body.onkeydown = resetTimer;
//     document.body.ontouchstart = resetTimer;
// };
