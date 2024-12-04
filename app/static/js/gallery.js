document.addEventListener("DOMContentLoaded", () => {
    console.log("yay")
    document.querySelector("#gallery div:nth-child(1)").style.fontSize = JSON.stringify(document.querySelector("#gallery div:nth-child(1)").clientWidth - 40) + "px";
})

document.querySelector('input[type="file"]').oninput = (e) => {
    e.target.parentElement.parentElement.submit()
}
