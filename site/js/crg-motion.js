/*
 * CRG motion layer.
 *
 * Everything here is progressive: without JavaScript, or with
 * prefers-reduced-motion, the page shows its final, static state.
 * Anything that moves on its own (hero slideshow, audience marquee)
 * stops with the hero's pause button, on hover/focus, or when the tab
 * is hidden.
 */
(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

  if (reduce.matches) return;
  root.classList.add('crg-motion');

  var raf = window.requestAnimationFrame.bind(window);
  var vh = function () { return window.innerHeight || document.documentElement.clientHeight; };

  /* ---------------------------------------------------------------
   * 1. Scroll reveals (auto-tagged so the HTML stays clean)
   * --------------------------------------------------------------- */
  var SINGLE = [
    '.crg-section-head', '.crg-feature__body', '.crg-cta__inner', '.crg-contact',
    '.crg-quote-form', '.crg-about .col-lg-6:first-child', '.crg-serve .crg-eyebrow',
    '.crg-filters', '.crg-section > .container > .crg-btn'
  ];
  var WIPE = ['.crg-feature__media', '.crg-about__photo'];
  var STAGGER = [
    ['.crg-section .row:not(.crg-project-list)', ':scope > [class*="col-"]'],
    ['.crg-project-list', ':scope > li > .crg-project'],
    ['.crg-steps', ':scope > li'],
    ['.crg-serve__list', ':scope > li'],
    ['.crg-checks', ':scope > li'],
    ['.crg-cases', ':scope > li'],
    ['.crg-team', ':scope > li'],
    ['.crg-footer .footer-top .row', ':scope > [class*="col-"]']
  ];

  function tag(el, kind, delay) {
    if (el.hasAttribute('data-reveal')) return;
    el.setAttribute('data-reveal', kind || '');
    if (delay) el.style.setProperty('--reveal-delay', delay + 'ms');
  }
  SINGLE.forEach(function (sel) { document.querySelectorAll(sel).forEach(function (el) { tag(el); }); });
  WIPE.forEach(function (sel) { document.querySelectorAll(sel).forEach(function (el) { tag(el, 'wipe'); }); });
  STAGGER.forEach(function (pair) {
    document.querySelectorAll(pair[0]).forEach(function (parent) {
      var kids;
      try { kids = parent.querySelectorAll(pair[1]); } catch (e) { return; }
      kids.forEach(function (kid, i) { tag(kid, '', Math.min(i, 6) * 90); });
    });
  });

  // Checked on every scroll frame rather than with an IntersectionObserver,
  // so elements skipped by a fast jump (End key, anchor link) still reveal,
  // and fully clipped wipes (zero visible area) are handled too.
  var pending = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
  function revealPassed() {
    if (!pending.length) return;
    var line = vh() * 0.9;
    pending = pending.filter(function (el) {
      if (el.getBoundingClientRect().top < line) {
        el.classList.add('is-revealed');
        return false;
      }
      return true;
    });
  }
  raf(revealPassed);

  /* ---------------------------------------------------------------
   * 2. Split headlines into words for the entrance animation
   * --------------------------------------------------------------- */
  function splitWords(el, cls) {
    var words = el.textContent.trim().split(/\s+/);
    el.setAttribute('aria-label', el.textContent.trim());
    el.textContent = '';
    words.forEach(function (w, i) {
      var outer = document.createElement('span');
      outer.className = cls;
      outer.setAttribute('aria-hidden', 'true');
      outer.style.setProperty('--i', i);
      var inner = document.createElement('span');
      inner.textContent = w;
      outer.appendChild(inner);
      el.appendChild(outer);
      if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
    });
    return el.querySelectorAll('.' + cls);
  }
  document.querySelectorAll('[data-split]').forEach(function (el) {
    splitWords(el, 'crg-word');
    raf(function () { raf(function () { el.classList.add('is-split-in'); }); });
  });

  /* ---------------------------------------------------------------
   * 3. "Who we serve" statement lights up word by word on scroll
   * --------------------------------------------------------------- */
  var scrubs = [];
  document.querySelectorAll('[data-scrub-words]').forEach(function (el) {
    scrubs.push({ el: el, words: splitWords(el, 'crg-scrub') });
    el.classList.add('is-scrubbing');
  });

  /* ---------------------------------------------------------------
   * 4. Scroll-linked: progress bar, header, parallax, step line, scrub
   * --------------------------------------------------------------- */
  var bar = document.querySelector('.crg-progress');
  var header = document.querySelector('.site-header .sticky-header');
  var parallax = Array.prototype.slice.call(document.querySelectorAll('[data-parallax]'));
  var stepLines = Array.prototype.slice.call(document.querySelectorAll('.crg-steps'));
  var lastY = window.scrollY;
  var ticking = false;

  function progressOf(el, start, end) {
    // 0 when el's top is at `start` (fraction of viewport height), 1 when it reaches `end`.
    var h = vh();
    var p = (h * start - el.getBoundingClientRect().top) / (h * (start - end));
    return Math.max(0, Math.min(1, p));
  }

  function onScroll() {
    ticking = false;
    revealPassed();
    var y = window.scrollY;
    var max = document.documentElement.scrollHeight - vh();
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';

    if (header) {
      var menuOpen = document.querySelector('#navbarNavDropdown.show');
      var hide = y > 320 && y > lastY + 4 && !menuOpen;
      if (hide) header.classList.add('crg-header-hidden');
      else if (y < lastY - 4 || y < 320) header.classList.remove('crg-header-hidden');
      root.classList.toggle('crg-header-up',
        header.classList.contains('is-fixed') && !header.classList.contains('crg-header-hidden'));
    }
    lastY = y;

    var h = vh();
    parallax.forEach(function (wrap) {
      var r = wrap.getBoundingClientRect();
      if (r.bottom < 0 || r.top > h) return;
      var center = (r.top + r.height / 2 - h / 2) / h; // -1..1 around viewport centre
      wrap.style.setProperty('--parallax', (center * -60).toFixed(1) + 'px');
    });

    stepLines.forEach(function (list) {
      list.style.setProperty('--line', progressOf(list, 0.85, 0.45).toFixed(3));
    });

    scrubs.forEach(function (s) {
      var p = progressOf(s.el, 0.85, 0.2);
      var lit = Math.round(p * s.words.length);
      s.words.forEach(function (w, i) { w.classList.toggle('is-lit', i < lit); });
    });
  }
  function requestTick() {
    if (!ticking) { ticking = true; raf(onScroll); }
  }
  window.addEventListener('scroll', requestTick, { passive: true });
  window.addEventListener('resize', requestTick);
  onScroll();

  /* ---------------------------------------------------------------
   * 5. Hero slideshow + global pause
   * --------------------------------------------------------------- */
  var hero = document.querySelector('[data-slideshow]');
  var paused = false;
  var pauseBtns = document.querySelectorAll('[data-motion-pause]');

  function setPaused(value) {
    paused = value;
    root.classList.toggle('crg-paused', paused);
    try { localStorage.setItem('crg-motion-paused', paused ? '1' : '0'); } catch (e) {}
    pauseBtns.forEach(function (btn) {
      btn.setAttribute('aria-pressed', String(paused));
      btn.setAttribute('aria-label', paused ? 'Play animations' : 'Pause animations');
    });
  }
  pauseBtns.forEach(function (btn) {
    btn.addEventListener('click', function () { setPaused(!paused); });
  });
  try { if (localStorage.getItem('crg-motion-paused') === '1') setPaused(true); } catch (e) {}

  if (hero) {
    var slides = hero.querySelectorAll('.crg-slide');
    var dots = document.querySelectorAll('[data-slide-to]');
    var index = 0;
    var hovering = false;

    var show = function (n) {
      index = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) {
        var on = i === index;
        s.classList.toggle('is-active', on);
        s.setAttribute('aria-hidden', String(!on));
      });
      dots.forEach(function (d, i) { d.setAttribute('aria-current', i === index ? 'true' : 'false'); });
    };
    dots.forEach(function (d) {
      d.addEventListener('click', function () { show(parseInt(d.getAttribute('data-slide-to'), 10)); });
    });
    hero.addEventListener('mouseenter', function () { hovering = true; });
    hero.addEventListener('mouseleave', function () { hovering = false; });
    setInterval(function () {
      if (!paused && !hovering && !document.hidden) show(index + 1);
    }, 6000);
    root.classList.add('crg-slideshow-ready');
  }

  /* ---------------------------------------------------------------
   * 6. Project card tilt (mouse only)
   * --------------------------------------------------------------- */
  if (finePointer.matches) {
    document.querySelectorAll('.crg-project').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        card.style.setProperty('--tilt-x', (y * -6).toFixed(2) + 'deg');
        card.style.setProperty('--tilt-y', (x * 8).toFixed(2) + 'deg');
        card.style.setProperty('--glare-x', ((x + 0.5) * 100).toFixed(1) + '%');
        card.style.setProperty('--glare-y', ((y + 0.5) * 100).toFixed(1) + '%');
      });
      card.addEventListener('pointerleave', function () {
        card.style.removeProperty('--tilt-x');
        card.style.removeProperty('--tilt-y');
      });
    });
  }

  /* ---------------------------------------------------------------
   * 7. Products jump nav: highlight the section in view
   * --------------------------------------------------------------- */
  var jumpLinks = document.querySelectorAll('.crg-jump a[href^="#"]');
  if (jumpLinks.length) {
    var byId = {};
    jumpLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        jumpLinks.forEach(function (a) { a.removeAttribute('aria-current'); });
        var link = byId[entry.target.id];
        if (link) link.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(byId).forEach(function (id) {
      var target = document.getElementById(id);
      if (target) spy.observe(target);
    });
  }
})();
