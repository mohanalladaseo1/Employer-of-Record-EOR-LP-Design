/* Content protection: deters copying, printing and screen capture. Cannot stop OS-level screenshots or a camera. */
(function () {
  var d = document, w = window, root = d.documentElement;

  // 1. Styles: no selection, no drag, no print, blur state
  var css =
    'html,body{-webkit-user-select:none!important;-moz-user-select:none!important;user-select:none!important;-webkit-touch-callout:none!important}' +
    'input,textarea,select,[contenteditable]{-webkit-user-select:text!important;user-select:text!important}' +
    'img,svg{-webkit-user-drag:none;user-drag:none}' +
    'html.pz-blur body>*:not(.pz-shield){filter:blur(18px)!important;transition:filter .05s}' +
    '.pz-shield{position:fixed;inset:0;z-index:2147483646;display:none;align-items:center;justify-content:center;background:rgba(11,31,20,.55);color:#fff;font:600 18px Inter,system-ui,sans-serif;text-align:center;padding:24px}' +
    'html.pz-blur .pz-shield{display:flex}' +
    '@media print{html,body{display:none!important;visibility:hidden!important}}';
  var st = d.createElement('style'); st.textContent = css; d.head.appendChild(st);

  function addLayers() {
    if (!d.body || d.querySelector('.pz-shield')) return;
    var sh = d.createElement('div'); sh.className = 'pz-shield';
    sh.textContent = 'Content protected. Click here to continue reading.';
    d.body.appendChild(sh);
  }
  if (d.body) addLayers(); else d.addEventListener('DOMContentLoaded', addLayers);

  // 2. Block copy, cut, paste-out, selection, drag and right-click
  ['copy', 'cut', 'contextmenu', 'dragstart', 'selectstart'].forEach(function (ev) {
    d.addEventListener(ev, function (e) {
      var t = e.target;
      if (t && t.closest && t.closest('input,textarea,select,[contenteditable]')) return;
      e.preventDefault();
      if (ev === 'copy' || ev === 'cut') { try { e.clipboardData.setData('text/plain', ''); } catch (x) {} }
    }, true);
  });

  // 3. Block shortcuts: copy, cut, select all, save, print, view source, dev tools
  function wipeClipboard() { try { navigator.clipboard && navigator.clipboard.writeText(''); } catch (x) {} }
  function flash() { root.classList.add('pz-blur'); setTimeout(function () { if (d.hasFocus()) root.classList.remove('pz-blur'); }, 1500); }
  d.addEventListener('keydown', function (e) {
    var k = (e.key || '').toLowerCase(), mod = e.ctrlKey || e.metaKey;
    if (k === 'printscreen') { wipeClipboard(); flash(); e.preventDefault(); return; }
    if (k === 'f12') { e.preventDefault(); return; }
    if (mod && ['c', 'x', 'a', 's', 'p', 'u'].indexOf(k) > -1) { e.preventDefault(); return; }
    if (mod && e.shiftKey && ['i', 'j', 'c', 's', '3', '4', '5'].indexOf(k) > -1) { e.preventDefault(); flash(); return; }
  }, true);
  d.addEventListener('keyup', function (e) { if ((e.key || '').toLowerCase() === 'printscreen') { wipeClipboard(); flash(); } }, true);

  // 4. Blur when the window loses focus (screenshot tools, screen share, switching apps)
  w.addEventListener('blur', function () { root.classList.add('pz-blur'); });
  w.addEventListener('focus', function () { root.classList.remove('pz-blur'); });
  d.addEventListener('visibilitychange', function () { if (d.hidden) root.classList.add('pz-blur'); });
  d.addEventListener('click', function (e) { if (e.target && e.target.classList && e.target.classList.contains('pz-shield')) root.classList.remove('pz-blur'); }, true);

  // 5. Block printing from the browser menu
  w.addEventListener('beforeprint', function () { root.classList.add('pz-blur'); });
  w.addEventListener('afterprint', function () { root.classList.remove('pz-blur'); });
})();
