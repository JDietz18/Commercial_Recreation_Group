/*
 * CRG blueprint background.
 *
 * A fixed layer behind the page: a drafting grid (pure CSS, in
 * crg-motion.css) plus a canvas where construction drawings sketch
 * themselves, hold, and fade: dimension lines, circles, footprints,
 * compass arcs and construction lines, with a drafting crosshair that
 * follows the mouse.
 *
 * Subtle by design: thin lines in a low-alpha ink taken from the theme
 * (--crg-bp-ink). Visitors who prefer reduced motion get a single still
 * drawing. Everything stops when animations are paused, and the canvas
 * sleeps while the tab is hidden.
 */
(function () {
  var layer = document.querySelector('.crg-blueprint');
  var canvas = layer && layer.querySelector('canvas');
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext('2d');
  if (!ctx) return;

  var root = document.documentElement;
  var still = window.matchMedia('(prefers-reduced-motion: reduce)');
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  var W = 0, H = 0, dpr = 1;
  var ink = 'rgba(30, 89, 205, 0.16)';
  var inkStrong = 'rgba(30, 89, 205, 0.28)';
  var accent = 'rgba(242, 84, 34, 0.45)';
  var shapes = [];
  var mouse = null;
  var lastSpawn = 0;
  var running = false;

  /* Seeded random so the still drawing is stable between loads. */
  var seed = 7;
  function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
  function rand(a, b) { return a + (b - a) * rnd(); }
  function pick(arr) { return arr[Math.floor(rnd() * arr.length)]; }

  function readInk() {
    var cs = getComputedStyle(layer);
    ink = cs.getPropertyValue('--crg-bp-ink').trim() || ink;
    inkStrong = cs.getPropertyValue('--crg-bp-ink-strong').trim() || inkStrong;
    accent = cs.getPropertyValue('--crg-bp-accent').trim() || accent;
  }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  /* Feet-and-inches labels, like a site plan. */
  function feet(px) {
    var inches = Math.round(px / 4) * 3;
    return Math.floor(inches / 12) + "'-" + (inches % 12) + '"';
  }

  /* Bias new drawings toward the page margins, away from body text. */
  function spot(margin) {
    var side = rnd();
    var x = side < 0.38 ? rand(margin, W * 0.24) : side < 0.76 ? rand(W * 0.76, W - margin) : rand(margin, W - margin);
    return { x: x, y: rand(margin, H - margin) };
  }

  /* ---- Shape factories: each returns {draw(progress), life...} ---- */
  function dimension() {
    var p = spot(60);
    var len = rand(120, Math.min(360, W * 0.3));
    var vertical = rnd() < 0.35;
    var label = feet(len);
    return {
      draw: function (t) {
        var x1 = p.x, y1 = p.y;
        var x2 = vertical ? x1 : x1 + len * t, y2 = vertical ? y1 + len * t : y1;
        ctx.strokeStyle = ink;
        ctx.beginPath();
        ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
        // extension lines
        var e = 14;
        if (vertical) { ctx.moveTo(x1 - e, y1); ctx.lineTo(x1 + e, y1); ctx.moveTo(x2 - e, y2); ctx.lineTo(x2 + e, y2); }
        else { ctx.moveTo(x1, y1 - e); ctx.lineTo(x1, y1 + e); ctx.moveTo(x2, y2 - e); ctx.lineTo(x2, y2 + e); }
        ctx.stroke();
        // architectural slash ticks
        ctx.strokeStyle = inkStrong;
        ctx.beginPath();
        [[x1, y1], [x2, y2]].forEach(function (q) { ctx.moveTo(q[0] - 5, q[1] + 5); ctx.lineTo(q[0] + 5, q[1] - 5); });
        ctx.stroke();
        if (t > 0.6) {
          ctx.globalAlpha *= (t - 0.6) / 0.4;
          ctx.fillStyle = inkStrong;
          if (vertical) {
            ctx.save(); ctx.translate(x1 - 8, y1 + len / 2); ctx.rotate(-Math.PI / 2);
            ctx.textAlign = 'center'; ctx.fillText(label, 0, 0); ctx.restore();
          } else {
            ctx.textAlign = 'center'; ctx.fillText(label, x1 + len / 2, y1 - 8);
          }
        }
      }
    };
  }

  function circle() {
    var p = spot(80);
    var r = rand(28, 90);
    return {
      draw: function (t) {
        ctx.strokeStyle = ink;
        ctx.beginPath();
        ctx.arc(p.x, p.y, r, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * t);
        ctx.stroke();
        // centre lines
        ctx.setLineDash([10, 4, 2, 4]);
        ctx.beginPath();
        ctx.moveTo(p.x - r - 14, p.y); ctx.lineTo(p.x + r + 14, p.y);
        ctx.moveTo(p.x, p.y - r - 14); ctx.lineTo(p.x, p.y + r + 14);
        ctx.stroke();
        ctx.setLineDash([]);
        if (t > 0.5) {
          var a = -Math.PI / 4, k = (t - 0.5) / 0.5;
          ctx.strokeStyle = inkStrong;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y); ctx.lineTo(p.x + Math.cos(a) * r * k, p.y + Math.sin(a) * r * k);
          ctx.stroke();
          ctx.fillStyle = inkStrong; ctx.textAlign = 'left';
          ctx.globalAlpha *= k;
          ctx.fillText('R ' + feet(r), p.x + Math.cos(a) * r + 6, p.y + Math.sin(a) * r - 4);
        }
      }
    };
  }

  function footprint() {
    var p = spot(90);
    var w = rand(90, 220), h = rand(60, 150);
    var label = pick(['DECK', 'PLAY AREA', 'SHADE', 'PAD', 'TOWER', 'SLIDE ZONE', 'USE ZONE']);
    return {
      draw: function (t) {
        var per = 2 * (w + h), d = per * t;
        ctx.strokeStyle = ink;
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        var pts = [[p.x + w, p.y], [p.x + w, p.y + h], [p.x, p.y + h], [p.x, p.y]];
        var cx = p.x, cy = p.y;
        for (var i = 0; i < 4 && d > 0; i++) {
          var nx = pts[i][0], ny = pts[i][1];
          var seg = Math.abs(nx - cx) + Math.abs(ny - cy);
          var f = Math.min(1, d / seg);
          ctx.lineTo(cx + (nx - cx) * f, cy + (ny - cy) * f);
          d -= seg; cx = nx; cy = ny;
        }
        ctx.stroke();
        if (t > 0.7) {
          var k = (t - 0.7) / 0.3;
          ctx.save();
          ctx.beginPath(); ctx.rect(p.x, p.y, w * k, h); ctx.clip();
          ctx.strokeStyle = ink; ctx.globalAlpha *= 0.5;
          ctx.beginPath();
          for (var s = -h; s < w; s += 12) { ctx.moveTo(p.x + s, p.y + h); ctx.lineTo(p.x + s + h, p.y); }
          ctx.stroke();
          ctx.restore();
          ctx.globalAlpha *= k;
          ctx.fillStyle = inkStrong; ctx.textAlign = 'left';
          ctx.fillText(label + '  ' + feet(w) + ' × ' + feet(h), p.x, p.y - 8);
        }
      }
    };
  }

  function arc() {
    var p = spot(80);
    var r = rand(70, 160), start = rand(0, Math.PI * 2), sweep = rand(0.5, 1.6);
    return {
      draw: function (t) {
        ctx.strokeStyle = ink;
        ctx.beginPath();
        ctx.moveTo(p.x, p.y); ctx.lineTo(p.x + Math.cos(start) * r, p.y + Math.sin(start) * r);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(p.x, p.y, r, start, start + sweep * t);
        ctx.stroke();
        if (t > 0.4) {
          var e = start + sweep * t;
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x + Math.cos(e) * r, p.y + Math.sin(e) * r); ctx.stroke();
          ctx.fillStyle = accent;
          ctx.beginPath(); ctx.arc(p.x, p.y, 2.5, 0, Math.PI * 2); ctx.fill();
        }
        if (t > 0.8) {
          ctx.globalAlpha *= (t - 0.8) / 0.2;
          var mid = start + sweep / 2;
          ctx.fillStyle = inkStrong; ctx.textAlign = 'center';
          ctx.fillText(Math.round(sweep * 180 / Math.PI) + '°', p.x + Math.cos(mid) * (r * 0.62), p.y + Math.sin(mid) * (r * 0.62));
        }
      }
    };
  }

  function construction() {
    var horizontal = rnd() < 0.6;
    var at = horizontal ? rand(40, H - 40) : rand(40, W - 40);
    return {
      draw: function (t) {
        ctx.strokeStyle = ink;
        ctx.setLineDash([2, 6]);
        ctx.beginPath();
        if (horizontal) { ctx.moveTo(0, at); ctx.lineTo(W * t, at); }
        else { ctx.moveTo(at, 0); ctx.lineTo(at, H * t); }
        ctx.stroke();
        ctx.setLineDash([]);
      }
    };
  }

  var FACTORIES = [dimension, dimension, circle, footprint, footprint, arc, construction];

  function spawn(now, instant) {
    var make = pick(FACTORIES);
    var s = make();
    s.born = now;
    s.drawFor = instant ? 0 : rand(1400, 2600);
    s.hold = instant ? Infinity : rand(4000, 8000);
    s.fade = 1600;
    shapes.push(s);
  }

  function ease(t) { return 1 - Math.pow(1 - t, 3); }

  function render(now) {
    ctx.clearRect(0, 0, W, H);
    ctx.lineWidth = 1;
    ctx.font = '10px "IBM Plex Mono", ui-monospace, monospace';
    ctx.textBaseline = 'alphabetic';

    shapes = shapes.filter(function (s) {
      var age = now - s.born;
      var t = s.drawFor ? Math.min(1, age / s.drawFor) : 1;
      var alpha = 1;
      var fadeStart = s.drawFor + s.hold;
      if (age > fadeStart) alpha = 1 - (age - fadeStart) / s.fade;
      if (alpha <= 0) return false;
      ctx.save();
      ctx.globalAlpha = alpha;
      s.draw(ease(t));
      ctx.restore();
      return true;
    });

    if (mouse) {
      // Drafting crosshair with a coordinate readout.
      ctx.save();
      ctx.strokeStyle = ink;
      ctx.setLineDash([1, 5]);
      ctx.beginPath();
      ctx.moveTo(0, mouse.y); ctx.lineTo(W, mouse.y);
      ctx.moveTo(mouse.x, 0); ctx.lineTo(mouse.x, H);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.strokeStyle = accent;
      ctx.beginPath();
      ctx.arc(mouse.x, mouse.y, 9, 0, Math.PI * 2);
      ctx.moveTo(mouse.x - 14, mouse.y); ctx.lineTo(mouse.x - 4, mouse.y);
      ctx.moveTo(mouse.x + 4, mouse.y); ctx.lineTo(mouse.x + 14, mouse.y);
      ctx.stroke();
      ctx.fillStyle = inkStrong; ctx.textAlign = 'left';
      ctx.fillText('X ' + Math.round(mouse.x + window.scrollX) + '  Y ' + Math.round(mouse.y + window.scrollY), mouse.x + 16, mouse.y - 12);
      ctx.restore();
    }
  }

  function tick(now) {
    if (!running) return;
    var paused = root.classList.contains('crg-paused');
    if (!paused) {
      var target = W < 700 ? 4 : 8;
      if (shapes.length < target && now - lastSpawn > 1100) { spawn(now); lastSpawn = now; }
    } else {
      // Freeze: keep every shape fully drawn and held while paused.
      shapes.forEach(function (s) { s.born = now - s.drawFor - 1; });
    }
    render(now);
    requestAnimationFrame(tick);
  }

  function drawStill() {
    seed = 7;
    shapes = [];
    var n = W < 700 ? 5 : 10;
    for (var i = 0; i < n; i++) spawn(0, true);
    render(1);
  }

  function start() {
    readInk();
    resize();
    if (still.matches) { running = false; drawStill(); return; }
    if (running) return;
    running = true;
    seed = Date.now() % 2147483647 || 7;
    // Begin with a few drawings already on the board.
    var now = performance.now();
    for (var i = 0; i < 4; i++) { spawn(now - rand(0, 4000)); }
    requestAnimationFrame(tick);
  }

  window.addEventListener('resize', function () { resize(); if (still.matches) drawStill(); });
  still.addEventListener('change', function () { running = false; start(); });
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { running = false; } else if (!still.matches) { running = true; requestAnimationFrame(tick); }
  });
  // Re-read the ink when the theme changes.
  new MutationObserver(readInk).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', readInk);

  if (finePointer.matches && !still.matches) {
    window.addEventListener('pointermove', function (e) { mouse = { x: e.clientX, y: e.clientY }; }, { passive: true });
    document.addEventListener('pointerleave', function () { mouse = null; });
    window.addEventListener('blur', function () { mouse = null; });
  }

  // Grid drifts slightly against the scroll for depth.
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      layer.style.setProperty('--bp-shift', (-window.scrollY * 0.15).toFixed(1) + 'px');
    });
  }, { passive: true });

  if (document.fonts && document.fonts.ready) document.fonts.ready.then(start); else start();
})();
