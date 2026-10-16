/*
 * CRG theme toggle.
 *
 * The site follows the visitor's OS light/dark setting until they press
 * a toggle; their choice is then remembered on this device.
 *
 * Markup: <button type="button" data-theme-toggle aria-label="Switch to dark mode">…</button>
 *
 * To avoid a flash of the wrong theme, also inline this in <head>,
 * before any stylesheet:
 *   <script>try{var t=localStorage.getItem('crg-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}</script>
 */
(function () {
  var KEY = 'crg-theme';
  var root = document.documentElement;
  var media = window.matchMedia('(prefers-color-scheme: dark)');

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function current() {
    return root.dataset.theme || (media.matches ? 'dark' : 'light');
  }

  function sync() {
    var next = current() === 'dark' ? 'light' : 'dark';
    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
      btn.setAttribute('aria-label', 'Switch to ' + next + ' mode');
      btn.setAttribute('aria-pressed', String(current() === 'dark'));
    });
  }

  var saved = stored();
  if (saved === 'light' || saved === 'dark') root.dataset.theme = saved;

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-theme-toggle]');
    if (!btn) return;
    var next = current() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem(KEY, next); } catch (err) {}
    sync();
  });

  media.addEventListener('change', sync);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', sync);
  } else {
    sync();
  }
})();
