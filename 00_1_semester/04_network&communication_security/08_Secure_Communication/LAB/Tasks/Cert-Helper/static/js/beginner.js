/*
 * Project: Certificate Generation Lab
 * Institution: EK – Erhvervsakademi København
 * Author: moms@ek.dk
 */

const stateNode = document.querySelector("#initial-state");
let appState = stateNode ? JSON.parse(stateNode.textContent || "{}") : {};
let currentStep = 0;
const dirtyForms = new Set();

const panels = [...document.querySelectorAll("[data-panel]")];
const steps = [...document.querySelectorAll(".step")];

function projectName() {
  return appState.project || document.querySelector("#ca-form [name=project]")?.value || "student-lab";
}

function setStep(step) {
  currentStep = Number(step);
  panels.forEach((panel) => panel.classList.toggle("active", Number(panel.dataset.panel) === currentStep));
  refreshSteps();
}

function refreshSteps() {
  const done = [
    appState.ca_created,
    appState.trust_step_completed,
    appState.csr_created,
    appState.leaf_signed,
    appState.leaf_signed,
  ];
  steps.forEach((step) => {
    const idx = Number(step.dataset.step);
    step.classList.toggle("current", idx === currentStep);
    step.classList.toggle("done", Boolean(done[idx]));
    if (idx === currentStep) step.setAttribute("aria-current", "step");
    else step.removeAttribute("aria-current");
    step.querySelector("span").textContent = idx === currentStep ? "◐" : done[idx] ? "✓" : "○";
  });
  document.querySelector("#visual-ca").textContent = appState.ca_name || "Root CA";
  document.querySelector("#visual-leaf").textContent = appState.hostname || "server.lab";
  renderSummary();
}

steps.forEach((step) => step.addEventListener("click", () => setStep(step.dataset.step)));

document.querySelectorAll(".form-grid").forEach((form) => {
  form.addEventListener("input", () => dirtyForms.add(form));
  form.addEventListener("change", () => dirtyForms.add(form));
});
document.querySelectorAll("[data-mode-link]").forEach((link) => {
  link.addEventListener("click", (event) => {
    if (!dirtyForms.size) return;
    if (!window.confirm("Switching modes will discard form changes that have not been generated. Continue?")) {
      event.preventDefault();
    } else {
      dirtyForms.clear();
    }
  });
});
window.addEventListener("beforeunload", (event) => {
  if (!dirtyForms.size) return;
  event.preventDefault();
  event.returnValue = "";
});

document.querySelectorAll(".toggle-optional").forEach((button) => {
  button.addEventListener("click", () => {
    const fields = button.parentElement.querySelector(".optional-fields");
    fields.classList.toggle("open");
    button.textContent = fields.classList.contains("open") ? "- Optional identity fields" : "+ Optional identity fields";
  });
});

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((item) => {
      item.classList.remove("active");
      item.setAttribute("aria-selected", "false");
    });
    document.querySelectorAll(".tab-panel").forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");
    tab.setAttribute("aria-selected", "true");
    document.querySelector(`[data-tab-panel="${tab.dataset.tab}"]`).classList.add("active");
  });
});

function addSan(kind, value = "") {
  const list = document.querySelector(`#${kind}-list`);
  const row = document.createElement("div");
  row.className = "san-row";
  const input = document.createElement("input");
  input.setAttribute("aria-label", `${kind.toUpperCase()} SAN`);
  input.value = value;
  const remove = document.createElement("button");
  remove.type = "button";
  remove.className = "ghost";
  remove.textContent = "Remove";
  remove.addEventListener("click", () => {
    dirtyForms.add(row.closest("form"));
    row.remove();
  });
  row.append(input, remove);
  list.appendChild(row);
}

document.querySelectorAll(".add-san").forEach((button) => {
  button.addEventListener("click", () => {
    dirtyForms.add(button.closest("form"));
    addSan(button.dataset.kind);
  });
});
addSan("dns", "server.lab");
addSan("dns", "www.server.lab");
addSan("ip", "10.10.0.70");

function formData(form) {
  return Object.fromEntries(new FormData(form).entries());
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;",
  })[character]);
}

function identityFrom(form, target) {
  ["country", "state", "city", "organization", "unit", "email"].forEach((name) => {
    const value = form.querySelector(`[name="${name}"]`)?.value || "";
    target[name] = value;
  });
}

async function postJson(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!data.ok) throw new Error(data.error || "Request failed.");
  return data;
}

function renderResult(targetId, title, files, info, commands) {
  const target = document.querySelector(targetId);
  const project = projectName();
  target.innerHTML = `<div class="success">✓ ${escapeHtml(title)}</div>
    <p>Host folder: <code>./certificates/${escapeHtml(project)}/</code></p>
    <div class="file-list">${files.map(fileCard).join("")}</div>
    ${info ? infoTable(info) : ""}
    <details><summary>Behind the scenes</summary>${commandBlocks(commands)}</details>`;
}

function fileCard(file) {
  const cls = file.private ? "file-item private" : "file-item";
  const action = file.href ? `<a class="button" href="${escapeHtml(file.href)}">${escapeHtml(file.label || "Download")}</a>` : "<span>Stored locally</span>";
  return `<div class="${cls}"><strong>${escapeHtml(file.name)}</strong><span class="badge">${escapeHtml(file.kind)}</span><p>${escapeHtml(file.help)}</p>${action}</div>`;
}

function infoTable(info) {
  const rows = Object.entries(info).filter(([, value]) => value && (!Array.isArray(value) || value.length));
  return `<dl class="inspect-output">${rows.map(([key, value]) => `<dt>${escapeHtml(key.replaceAll("_", " "))}</dt><dd>${Array.isArray(value) ? value.map(escapeHtml).join("<br>") : escapeHtml(value)}</dd>`).join("")}</dl>`;
}

function commandBlocks(commands = []) {
  return (commands || []).map((cmd, index) => {
    const text = escapeHtml(cmd.join(" "));
    return `<div class="command-box"><pre><code>${text}</code></pre><button class="copy" type="button">Copy</button></div><p>${index + 1}. Generated file with OpenSSL.</p>`;
  }).join("");
}

document.querySelector("#ca-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = formData(form);
  try {
    document.querySelector("#ca-result").innerHTML = "<p>Generating certificate...</p>";
    const data = await postJson("/api/create-ca", payload);
    appState = data.state;
    dirtyForms.delete(form);
    renderResult("#ca-result", "Certificate Authority created", [
      {name: "ca.cert.pem", kind: "PUBLIC CERTIFICATE", help: "This CA certificate can be shared. Import it into a trust store only for the lab; this application does not verify trust.", href: `/download/${encodeURIComponent(appState.project)}/ca_cert`, label: "Download CA Certificate"},
      {name: "ca.key.pem", kind: "PRIVATE KEY - DO NOT DISTRIBUTE", help: "This private key signs certificates.", href: "", private: true},
    ], data.info, data.commands);
    refreshSteps();
  } catch (error) {
    document.querySelector("#ca-result").innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
  }
});

document.querySelector("#trust-complete").addEventListener("click", async () => {
  try {
    const data = await postJson("/api/trust-complete", {project: projectName()});
    appState = data.state;
    document.querySelector("#trust-result").innerHTML = "<div class=\"success\">✓ Trust guidance reviewed. The application cannot confirm whether the CA is trusted on your device.</div>";
    refreshSteps();
  } catch (error) {
    document.querySelector("#trust-result").innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
  }
});

document.querySelector("#leaf-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = formData(form);
  payload.project = projectName();
  payload.dns_names = [...document.querySelectorAll("#dns-list input")].map((item) => item.value);
  payload.ip_names = [...document.querySelectorAll("#ip-list input")].map((item) => item.value);
  identityFrom(form, payload);
  try {
    document.querySelector("#leaf-result").innerHTML = "<p>Generating CSR...</p>";
    const data = await postJson("/api/create-leaf", payload);
    appState = data.state;
    dirtyForms.delete(form);
    renderResult("#leaf-result", "Private key and CSR created", [
      {name: "server.key.pem", kind: "PRIVATE KEY - DO NOT DISTRIBUTE", help: "Anyone with this key can impersonate this server if trusted.", href: `/download/${encodeURIComponent(appState.project)}/server_key`, label: "Download Server Private Key", private: true},
      {name: "server.csr.pem", kind: "PUBLIC REQUEST", help: "Normally submitted to a CA for signing.", href: `/download/${encodeURIComponent(appState.project)}/csr`, label: "Download CSR"},
    ], data.info, data.commands);
    refreshSteps();
  } catch (error) {
    document.querySelector("#leaf-result").innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
  }
});

document.querySelector("#sign-leaf").addEventListener("click", async () => {
  try {
    document.querySelector("#sign-result").innerHTML = "<p>Signing certificate...</p>";
    const data = await postJson("/api/sign-leaf", {project: projectName()});
    appState = data.state;
    renderResult("#sign-result", "Certificate successfully signed", [
      {name: "server.cert.pem", kind: "PUBLIC CERTIFICATE", help: "Signed server certificate; signing does not make it trusted.", href: `/download/${encodeURIComponent(appState.project)}/leaf_cert`, label: "Download Leaf Certificate"},
    ], data.info, data.commands);
    refreshSteps();
  } catch (error) {
    document.querySelector("#sign-result").innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
  }
});

function renderSummary() {
  const target = document.querySelector("#summary-files");
  if (!target) return;
  const project = projectName();
  target.innerHTML = [
    {name: "ca.cert.pem", kind: "PUBLIC CERTIFICATE", help: `./certificates/${project}/ca/ca.cert.pem`, href: `/download/${encodeURIComponent(project)}/ca_cert`, label: "Download"},
    {name: "ca.key.pem", kind: "PRIVATE KEY", help: `Stored locally at ./certificates/${project}/ca/ca.key.pem`, private: true},
    {name: "server.csr.pem", kind: "PUBLIC REQUEST", help: `./certificates/${project}/leaf/server.csr.pem`, href: `/download/${encodeURIComponent(project)}/csr`, label: "Download"},
    {name: "server.cert.pem", kind: "PUBLIC CERTIFICATE", help: `./certificates/${project}/leaf/server.cert.pem`, href: `/download/${encodeURIComponent(project)}/leaf_cert`, label: "Download"},
    {name: "server.key.pem", kind: "PRIVATE KEY", help: `./certificates/${project}/leaf/server.key.pem`, href: `/download/${encodeURIComponent(project)}/server_key`, label: "Download Server Private Key", private: true},
  ].map(fileCard).join("");
  document.querySelector("#summary-inspector").href = `/inspector?project=${encodeURIComponent(project)}`;
}

refreshSteps();
