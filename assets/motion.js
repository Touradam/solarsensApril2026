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

  /* Neural mesh: drifting nodes, proximity edges, traveling signal pulses. */
  function initNeuralMesh() {
    var canvas = document.querySelector('.hero-particles');
    if (!canvas) return;
    if (reduced) {
      canvas.style.display = 'none';
      return;
    }

    var ctx = canvas.getContext('2d');
    var nodes = [];
    var pulses = [];
    var animId = null;
    var running = false;
    var inView = true;
    var mouse = { x: -9999, y: -9999 };
    var LINK_DIST = 150;
    var MOUSE_DIST = 170;

    function nodeCount() {
      var w = canvas.offsetWidth;
      if (w < 640) return 16;
      if (w < 1100) return 24;
      return 32;
    }

    function resize() {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    }

    function createNode() {
      return {
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.3 + 0.7,
        vx: (Math.random() - 0.5) * 0.22,
        vy: (Math.random() - 0.5) * 0.22,
        tw: Math.random() * Math.PI * 2
      };
    }

    function init() {
      resize();
      var count = nodeCount();
      nodes = [];
      for (var i = 0; i < count; i++) nodes.push(createNode());
      pulses = [];
    }

    function spawnPulse(edge) {
      pulses.push({ a: edge[0], b: edge[1], t: 0, speed: 0.006 + Math.random() * 0.008 });
    }

    function tick() {
      if (!running) return;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      var i, j, n, m, dx, dy, d;

      for (i = 0; i < nodes.length; i++) {
        n = nodes[i];
        n.x += n.vx;
        n.y += n.vy;
        n.tw += 0.02;
        if (n.x < -20) n.x = canvas.width + 20;
        if (n.x > canvas.width + 20) n.x = -20;
        if (n.y < -20) n.y = canvas.height + 20;
        if (n.y > canvas.height + 20) n.y = -20;
      }

      /* Edges: faint web, brighter near the cursor */
      for (i = 0; i < nodes.length; i++) {
        for (j = i + 1; j < nodes.length; j++) {
          n = nodes[i];
          m = nodes[j];
          dx = n.x - m.x;
          dy = n.y - m.y;
          d = Math.sqrt(dx * dx + dy * dy);
          if (d > LINK_DIST) continue;
          var alpha = (1 - d / LINK_DIST) * 0.16;
          var mdx = (n.x + m.x) / 2 - mouse.x;
          var mdy = (n.y + m.y) / 2 - mouse.y;
          var md = Math.sqrt(mdx * mdx + mdy * mdy);
          if (md < MOUSE_DIST) alpha += (1 - md / MOUSE_DIST) * 0.3;
          ctx.strokeStyle = 'rgba(196, 163, 90, ' + alpha.toFixed(3) + ')';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(n.x, n.y);
          ctx.lineTo(m.x, m.y);
          ctx.stroke();

          if (pulses.length < 6 && Math.random() < 0.0018 && d < LINK_DIST * 0.85) {
            spawnPulse([n, m]);
          }
        }
      }

      /* Signal pulses traveling along edges */
      for (i = pulses.length - 1; i >= 0; i--) {
        var p = pulses[i];
        p.t += p.speed;
        if (p.t >= 1) {
          pulses.splice(i, 1);
          continue;
        }
        var px = p.a.x + (p.b.x - p.a.x) * p.t;
        var py = p.a.y + (p.b.y - p.a.y) * p.t;
        var fade = Math.sin(p.t * Math.PI);
        var grad = ctx.createRadialGradient(px, py, 0, px, py, 5);
        grad.addColorStop(0, 'rgba(226, 200, 135, ' + (0.75 * fade).toFixed(3) + ')');
        grad.addColorStop(1, 'rgba(226, 200, 135, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(px, py, 5, 0, Math.PI * 2);
        ctx.fill();
      }

      /* Nodes with gentle twinkle */
      for (i = 0; i < nodes.length; i++) {
        n = nodes[i];
        var glow = 0.28 + Math.sin(n.tw) * 0.14;
        var ndx = n.x - mouse.x;
        var ndy = n.y - mouse.y;
        var nd = Math.sqrt(ndx * ndx + ndy * ndy);
        if (nd < MOUSE_DIST) glow += (1 - nd / MOUSE_DIST) * 0.45;
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(226, 200, 135, ' + Math.min(glow, 0.9).toFixed(3) + ')';
        ctx.fill();
      }

      animId = requestAnimationFrame(tick);
    }

    function start() {
      if (running || reduced) return;
      running = true;
      tick();
    }

    function stop() {
      running = false;
      if (animId) cancelAnimationFrame(animId);
    }

    var hero = canvas.closest('.hero') || canvas.parentElement;
    if (hero) {
      hero.addEventListener('mousemove', function (e) {
        var rect = canvas.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;
      });
      hero.addEventListener('mouseleave', function () {
        mouse.x = -9999;
        mouse.y = -9999;
      });
    }

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        inView = entries[0].isIntersecting;
        if (inView && !document.hidden) start(); else stop();
      }, { threshold: 0.02 }).observe(canvas);
    }

    init();
    start();
    window.addEventListener('resize', init);
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stop();
      else if (inView) start();
    });
  }

  /* Hero entrance: word-by-word title reveal + 3D parallax on the media frame. */
  function initHeroDepth() {
    var hero = document.querySelector('.hero');
    if (!hero) return;
    var title = hero.querySelector('.hero-title');
    var frame = hero.querySelector('.hero-frame');

    function splitTitle() {
      if (!title) return;
      if (reduced) return;
      var text = title.textContent.replace(/\s+/g, ' ').trim();
      if (!text) return;
      title.setAttribute('aria-label', text);
      title.textContent = '';
      text.split(' ').forEach(function (word, i) {
        var span = document.createElement('span');
        span.className = 'hero-word';
        span.textContent = word;
        span.style.animationDelay = (0.15 + i * 0.055) + 's';
        span.setAttribute('aria-hidden', 'true');
        title.appendChild(span);
        title.appendChild(document.createTextNode(' '));
      });
    }

    splitTitle();
    document.addEventListener('solarsense:langchange', splitTitle);

    if (!frame || reduced) return;
    var rafId = null;
    var target = { rx: 0, ry: 0, tx: 0, ty: 0 };
    var current = { rx: 0, ry: 0, tx: 0, ty: 0 };

    function lerp(a, b, f) { return a + (b - a) * f; }

    function applyFrame() {
      current.rx = lerp(current.rx, target.rx, 0.08);
      current.ry = lerp(current.ry, target.ry, 0.08);
      current.tx = lerp(current.tx, target.tx, 0.08);
      current.ty = lerp(current.ty, target.ty, 0.08);
      frame.style.transform =
        'perspective(1100px) rotateX(' + current.rx.toFixed(3) + 'deg) rotateY(' +
        current.ry.toFixed(3) + 'deg) translate3d(' + current.tx.toFixed(2) + 'px, ' +
        current.ty.toFixed(2) + 'px, 0)';
      var settled = Math.abs(current.rx - target.rx) < 0.01 &&
        Math.abs(current.ry - target.ry) < 0.01 &&
        Math.abs(current.tx - target.tx) < 0.05 &&
        Math.abs(current.ty - target.ty) < 0.05;
      if (settled) {
        rafId = null;
        return;
      }
      rafId = requestAnimationFrame(applyFrame);
    }

    function queue() {
      if (!rafId) rafId = requestAnimationFrame(applyFrame);
    }

    hero.addEventListener('mousemove', function (e) {
      var rect = hero.getBoundingClientRect();
      var nx = (e.clientX - rect.left) / rect.width - 0.5;
      var ny = (e.clientY - rect.top) / rect.height - 0.5;
      target.ry = nx * 8;
      target.rx = -ny * 6;
      target.tx = nx * 12;
      target.ty = ny * 10;
      queue();
    });

    hero.addEventListener('mouseleave', function () {
      target.rx = 0;
      target.ry = 0;
      target.tx = 0;
      target.ty = 0;
      queue();
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
  initNeuralMesh();
  initHeroDepth();
  initTilt();
  initFocusRings();
})();
