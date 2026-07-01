/**
 * Midnight Champagne — shared motion layer
 * Spotlight, particles, scroll reveal, 3D tilt. Respects prefers-reduced-motion.
 */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initScrollReveal() {
    var targets = document.querySelectorAll('.reveal, .reveal-item');
    if (!targets.length) return;

    if (reduced) {
      targets.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          el.classList.add('is-visible');
          observer.unobserve(el);
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );

    targets.forEach(function (el, i) {
      var group = el.closest('.reveal-stagger');
      if (group && el.classList.contains('reveal-item')) {
        var siblings = group.querySelectorAll('.reveal-item');
        var idx = Array.prototype.indexOf.call(siblings, el);
        el.style.transitionDelay = (idx * 80) + 'ms';
      }
      observer.observe(el);
    });
  }

  function initHeroSpotlight() {
    var hero = document.querySelector('.hero, .pro-hero');
    var spotlight = hero && hero.querySelector('.hero-spotlight');
    if (!hero || !spotlight || reduced) return;

    hero.addEventListener('mousemove', function (e) {
      var rect = hero.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var y = e.clientY - rect.top;
      spotlight.style.setProperty('--spot-x', x + 'px');
      spotlight.style.setProperty('--spot-y', y + 'px');
      spotlight.style.opacity = '1';
    });

    hero.addEventListener('mouseleave', function () {
      spotlight.style.opacity = '0';
    });
  }

  function initParticles() {
    var canvas = document.querySelector('.hero-particles');
    if (!canvas || reduced) {
      if (canvas) canvas.style.display = 'none';
      return;
    }

    var ctx = canvas.getContext('2d');
    var particles = [];
    var count = window.innerWidth < 640 ? 18 : 32;
    var animId;

    function resize() {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    }

    function createParticle() {
      return {
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.2 + 0.4,
        vx: (Math.random() - 0.5) * 0.15,
        vy: (Math.random() - 0.5) * 0.15,
        a: Math.random() * 0.35 + 0.08
      };
    }

    function init() {
      resize();
      particles = [];
      for (var i = 0; i < count; i++) particles.push(createParticle());
    }

    function tick() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(function (p) {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(196, 163, 90, ' + p.a + ')';
        ctx.fill();
      });
      animId = requestAnimationFrame(tick);
    }

    init();
    tick();
    window.addEventListener('resize', init);

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        cancelAnimationFrame(animId);
      } else {
        tick();
      }
    });
  }

  function initTilt() {
    if (reduced) return;
    var tiltEls = document.querySelectorAll('[data-tilt], .card, .team-card, .pricing-card, .timeline-phase');

    tiltEls.forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var rect = el.getBoundingClientRect();
        var x = (e.clientX - rect.left) / rect.width - 0.5;
        var y = (e.clientY - rect.top) / rect.height - 0.5;
        el.style.transform = 'perspective(800px) rotateX(' + (-y * 4) + 'deg) rotateY(' + (x * 4) + 'deg) translateY(-4px)';
      });

      el.addEventListener('mouseleave', function () {
        el.style.transform = '';
      });
    });
  }

  function initFocusRings() {
    /* CSS handles focus-visible; ensure keyboard users see sections after nav */
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener('click', function () {
        var id = link.getAttribute('href');
        if (id && id.length > 1) {
          var target = document.querySelector(id);
          if (target && !target.hasAttribute('tabindex')) {
            target.setAttribute('tabindex', '-1');
          }
        }
      });
    });
  }

  initScrollReveal();
  initHeroSpotlight();
  initParticles();
  initTilt();
  initFocusRings();
})();
