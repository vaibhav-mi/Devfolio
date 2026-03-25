// DevFolio — Main JS

// Live clock
function tick() {
  const el = document.getElementById('clk');
  if (!el) return;
  const n = new Date();
  el.textContent = [n.getHours(), n.getMinutes(), n.getSeconds()]
    .map(v => String(v).padStart(2, '0')).join(':');
}
tick();
setInterval(tick, 1000);

// Sidebar mobile
function tSide() {
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('sov').classList.toggle('active');
}
function cSide() {
  const s = document.getElementById('sidebar');
  const o = document.getElementById('sov');
  if (s) s.classList.remove('open');
  if (o) o.classList.remove('active');
}

// Modals
function openM(id) {
  const el = document.getElementById(id);
  if (el) { el.classList.add('open'); document.body.style.overflow = 'hidden'; }
}
function closeM(id) {
  const el = document.getElementById(id);
  if (el) { el.classList.remove('open'); document.body.style.overflow = ''; }
}

// Close modal on backdrop click
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.modal-bd').forEach(bd => {
    bd.addEventListener('click', e => { if (e.target === bd) closeM(bd.id); });
  });

  // Escape key closes modals
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-bd.open').forEach(bd => closeM(bd.id));
    }
  });

  // Auto-dismiss flash messages
  const flashContainer = document.getElementById('flash-container');
  if (flashContainer) {
    setTimeout(() => {
      flashContainer.style.transition = 'opacity 0.5s';
      flashContainer.style.opacity = '0';
      setTimeout(() => flashContainer.remove(), 500);
    }, 3500);
  }

  // Animate skill progress bars if on skills page
  const bars = document.querySelectorAll('.p-fill[data-t]');
  if (bars.length) {
    setTimeout(() => {
      bars.forEach(b => { b.style.width = b.dataset.t + '%'; });
    }, 150);
  }
});
