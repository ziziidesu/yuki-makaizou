window.onload = function () {
  setTimeout(() => {
    document.getElementById("loader").style.display = "none";
    document.getElementById("content").style.display = "block";
  }, 2000);

  if (getCookie("darkMode") === "true") {
    document.body.classList.add("dark-mode");
  }
};

const bgmButton = document.getElementById("bgm-button");
const bgmAudio = document.getElementById("bgm-audio");

bgmButton.addEventListener("click", () => {
  if (bgmAudio.paused) {
    bgmAudio.play();
    bgmButton.textContent = "⏸️ bgmを停止する ⏸️";
  } else {
    bgmAudio.pause();
    bgmButton.textContent = "🎵 bgmを再生する 🎵";
  }
});

const darkModeToggle = document.getElementById("dark-mode-toggle");

darkModeToggle.addEventListener("click", () => {
  const isDarkMode = document.body.classList.toggle("dark-mode");
  setCookie("darkMode", isDarkMode, 7);
});

function setCookie(name, value, days) {
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie =
    name + "=" + value + ";expires=" + expires.toUTCString() + ";path=/";
}

function getCookie(name) {
  const nameEQ = name + "=";
  const ca = document.cookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i].trim();
    if (c.indexOf(nameEQ) === 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
}
