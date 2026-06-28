const KEY = "crtlEnabled";
const btn = document.getElementById("toggle");

function render(on) {
  btn.textContent = on ? "ON" : "OFF";
  btn.dataset.on = String(on);
}

// Show the ACTUAL state on open (default ON).
chrome.storage.local.get(KEY, (r) => render(r[KEY] !== false));

btn.addEventListener("click", () => {
  chrome.storage.local.get(KEY, (r) => {
    const next = !(r[KEY] !== false);
    chrome.storage.local.set({ [KEY]: next }, () => render(next));
  });
});
