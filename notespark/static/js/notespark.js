// NoteSpark landing page JS (GPLv3)
document.addEventListener('DOMContentLoaded', function() {
  // GSAP entrance animations
  if (window.gsap) {
    gsap.from('nav.navbar', { duration: 1, y: -50, opacity: 0, ease: 'power2.out' });
    gsap.from('main section, .card', {
      duration: 1,
      y: 40,
      opacity: 0,
      stagger: 0.2,
      ease: 'power2.out'
    });
    gsap.from('.navbar-nav .nav-link', {
      duration: 0.7,
      scale: 0.8,
      opacity: 0,
      stagger: 0.1,
      ease: 'back.out(1.7)'
    });
    document.querySelectorAll('.btn').forEach(btn => {
      btn.addEventListener('mouseenter', () => {
        gsap.to(btn, { scale: 1.08, duration: 0.2 });
      });
      btn.addEventListener('mouseleave', () => {
        gsap.to(btn, { scale: 1, duration: 0.2 });
      });
    });
  }

  // Theme toggle icon update (if themeToggle exists)
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');
  if (themeToggle && themeIcon) {
    function updateThemeIcon() {
      const theme = document.documentElement.getAttribute('data-bs-theme');
      themeIcon.className = theme === 'dark' ? 'bi bi-moon-stars' : 'bi bi-brightness-high';
    }
    updateThemeIcon();
    themeToggle.addEventListener('click', () => {
      setTimeout(updateThemeIcon, 100);
    });
  }

  // Initialize Lenis for smooth scrolling
  const lenis = new Lenis({
    duration: 1.2,
    smooth: true,
    direction: 'vertical',
    gestureDirection: 'vertical',
    mouseMultiplier: 1,
    touchMultiplier: 2,
    smoothTouch: true,
    infinite: false
  });

  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);

  // Optional: update Three.js camera on scroll for 3D effect
  lenis.on('scroll', ({ scroll }) => {
    // Example: Parallax effect or camera movement
    // camera.position.z = 15 + scroll * 0.01;
  });
});
