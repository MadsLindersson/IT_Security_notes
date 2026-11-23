/*
 * Project: Certificate Generation Lab
 * Institution: EK – Erhvervsakademi København
 * Author: moms@ek.dk
 */

const projectSelect = document.querySelector("#inspect-project");
const kindSelect = document.querySelector("#inspect-kind");
const output = document.querySelector("#inspect-output");
const raw = document.querySelector("#raw-output");
const rawToggle = document.querySelector("#raw-toggle");

const params = new URLSearchParams(window.location.search);
if (params.get("project") && projectSelect) projectSelect.value = params.get("project");

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;",
  })[character]);
}

async function loadInspect(includeRaw = false) {
  if (!projectSelect || !projectSelect.value) {
    output.innerHTML = "<p>No generated projects found.</p>";
    return;
  }
  const url = `/api/inspect/${encodeURIComponent(projectSelect.value)}/${encodeURIComponent(kindSelect.value)}${includeRaw ? "?raw=1" : ""}`;
  const response = await fetch(url);
  const data = await response.json();
  if (!data.ok) {
    output.innerHTML = `<div class="error">${escapeHtml(data.error)}</div>`;
    raw.textContent = "";
    return;
  }
  output.innerHTML = `<dl>${Object.entries(data.info).map(([key, value]) => `<dt>${escapeHtml(key.replaceAll("_", " "))}</dt><dd>${Array.isArray(value) ? value.map(escapeHtml).join("<br>") : escapeHtml(value)}</dd>`).join("")}</dl>`;
  if (includeRaw) raw.textContent = data.raw;
}

projectSelect?.addEventListener("change", () => loadInspect(raw.classList.contains("open")));
kindSelect?.addEventListener("change", () => loadInspect(raw.classList.contains("open")));
rawToggle.addEventListener("click", () => {
  raw.classList.toggle("open");
  rawToggle.textContent = raw.classList.contains("open") ? "Hide raw OpenSSL output" : "Show raw OpenSSL output";
  loadInspect(raw.classList.contains("open"));
});

loadInspect(false);
