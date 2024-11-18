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
