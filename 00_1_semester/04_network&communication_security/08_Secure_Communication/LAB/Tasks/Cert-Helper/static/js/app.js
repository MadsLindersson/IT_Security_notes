/*
 * Project: Certificate Generation Lab
 * Institution: EK – Erhvervsakademi København
 * Author: moms@ek.dk
 */

const themeToggle = document.querySelector("[data-theme-toggle]");

function updateThemeControl(theme) {
  if (!themeToggle) return;
  themeToggle.setAttribute("aria-label", `Switch to ${theme === "dark" ? "light" : "dark"} mode`);
  themeToggle.title = `Switch to ${theme === "dark" ? "light" : "dark"} mode`;
}

updateThemeControl(document.documentElement.dataset.theme || "light");
themeToggle?.addEventListener("click", () => {
  const theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = theme;
  updateThemeControl(theme);
  try {
    localStorage.setItem("ek-lab-theme", theme);
    themeToggle.removeAttribute("data-storage-warning");
  } catch (error) {
    themeToggle.setAttribute("data-storage-warning", "true");
    themeToggle.title = "Theme changed for this session, but browser storage is unavailable.";
  }
});

function copyText(text, button) {
  navigator.clipboard.writeText(text).then(() => {
    const previous = button.textContent;
    button.textContent = "✓ Copied";
    setTimeout(() => { button.textContent = previous; }, 1200);
  }).catch(() => {
    button.textContent = "Copy failed";
    setTimeout(() => { button.textContent = "Copy"; }, 1600);
  });
}

document.addEventListener("click", (event) => {
  const copyButton = event.target instanceof Element ? event.target.closest(".copy") : null;
  if (!copyButton) return;
  const box = copyButton.closest(".command-box");
  const code = box ? box.querySelector("code") : null;
  if (code && navigator.clipboard) copyText(code.textContent, copyButton);
  else if (code) copyButton.textContent = "Copy unavailable";
});
