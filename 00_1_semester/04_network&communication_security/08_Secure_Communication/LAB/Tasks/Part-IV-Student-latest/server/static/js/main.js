// Progressive enhancement only: the browser submits the ordinary HTML form.
'use strict';
const toggle = document.querySelector('[data-password-toggle]');
if (toggle) {
  const password = document.getElementById(toggle.getAttribute('aria-controls'));
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    const show = password.type === 'password';
    password.type = show ? 'text' : 'password';
    toggle.textContent = show ? 'Hide' : 'Show';
    toggle.setAttribute('aria-pressed', String(show));
  });
}
