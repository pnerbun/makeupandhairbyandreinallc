// Scroll-triggered fade-up
const fadeObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.fade-up').forEach(el => fadeObserver.observe(el));
});

// Mobile nav
function toggleMenu() {
  const m = document.getElementById('mobile-menu');
  m.style.display = m.style.display === 'block' ? 'none' : 'block';
}

function closeMenu() {
  const m = document.getElementById('mobile-menu');
  if (m) m.style.display = 'none';
}
