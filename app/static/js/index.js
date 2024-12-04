let drawer = document.querySelector("#drawer");
let drawer_close_btn = document.querySelector("#drawer_close_btn");
let drawer_open_btn = document.querySelector("#drawer_open_btn");

drawer_close_btn.onclick = () => {
  drawer.style.display = "none";
  drawer_open_btn.style.display = "initial";
  console.log("closing drawer");
}

drawer_open_btn.onclick = (e) => {
  drawer.style.display = "flex";
  e.target.style.display = "none";
  console.log("opening drawer");
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
