import '@fontsource/schibsted-grotesk/400';
import '@fontsource/schibsted-grotesk/500';
import '@fontsource/schibsted-grotesk/600';
import './style.css';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';
import { metrics, compare, layers, timeline, costs, pipeline, palette, states } from './data.js';

gsap.registerPlugin(ScrollTrigger);

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const fmt = (n, dec = 0) => n.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
const temp = (t) => t.toFixed(1).replace('-', '−');

/* ---------------------------------------------------------------- estados */
const ICONS = {
  normal: '<circle cx="12" cy="12" r="9.5"/><path d="M7.5 12.5l3 3 6-6.5"/>',
  advertencia: '<path d="M12 3.2L22 20.5H2z"/><path d="M12 10v5"/><path d="M12 17.8v.2"/>',
  excursion: '<path d="M12 1.8L22.2 12 12 22.2 1.8 12z"/><path d="M12 16.5V8M8.2 11.6L12 7.8l3.8 3.8"/>',
  sinsenal: '<circle cx="12" cy="12" r="9.5" stroke-dasharray="3 3"/><path d="M5.8 18.2L18.2 5.8"/>'
};
const icon = (svg, k) => {
  for (const [a, v] of [['fill', 'none'], ['stroke', 'currentColor'], ['stroke-width', '2'], ['stroke-linecap', 'round'], ['stroke-linejoin', 'round']]) svg.setAttribute(a, v);
  svg.innerHTML = ICONS[k];
};
const NAME = { normal: 'Normal', advertencia: 'Warning', excursion: 'Excursion', sinsenal: 'No signal' };
const stateOf = (t) => {
  if (t === null) return 'sinsenal';
  if (t > -16 || t < -20) return 'excursion';
  if (t > -16.8 || t < -19.4) return 'advertencia';
  return 'normal';
};

/* ---------------------------------------------------------------- render */
function render() {
  $('#metrics').innerHTML = metrics.map((m) => `
    <div class="metric fade">
      <b>${m.pre || ''}<span data-count="${m.n}" data-dec="${m.dec || 0}">${fmt(m.n, m.dec || 0)}</span>${m.u ? `<small>${m.u}</small>` : ''}</b>
      <span>${m.l}</span><i>${m.s}</i>
    </div>`).join('');

  $('#compare').insertAdjacentHTML('beforeend', compare.map(([a, b]) => `<div class="cmp"><span>${a}</span><span>${b}</span></div>`).join(''));

  $('#layersNav').innerHTML = layers.map((l, i) => `<li><a href="#layer-${i}">${l.name}</a></li>`).join('');
  $('#layersList').innerHTML = layers.map((l, i) => `
    <article class="layer" id="layer-${i}">
      <h3 class="fade">${l.title}</h3>
      <p class="fade">${l.text}</p>
      <div class="layer-facts fade">${l.facts.map(([b, s]) => `<div><b>${b}</b><span>${s}</span></div>`).join('')}</div>
      <figure class="diagram" data-zoom>
        <div class="inner"><img src="img/diagrams/${l.img}.svg" alt="Diagram: ${l.cap}" loading="lazy"></div>
        <figcaption>${l.cap}</figcaption>
      </figure>
    </article>`).join('');

  $('#tlItems').innerHTML = timeline.map((t) => `
    <div class="tl-item ${t.key ? 'key' : ''}">
      <small>Day</small><b>${t.d}</b>
      <h3>${t.t}</h3><p>${t.p}</p>
    </div>`).join('');

  $('#pipeSteps').innerHTML = pipeline.map((p, i) => `
    <li><span class="node">${i + 1}</span><div><h3>${p.t}</h3><p>${p.p}</p></div></li>`).join('');

  const top = costs[0].bars[2][0];
  $('#costs').innerHTML = costs.map((c) => `
    <article class="cost fade ${c.cls || ''}">
      <span class="cost-l">${c.l}</span>
      <div>
        <div class="cost-v">${c.approx ? '~' : ''}$<span data-count="${c.n}">${fmt(c.n)}</span></div>
        <p class="cost-n">${c.note}</p>
        ${c.bars ? `<div class="bars">${c.bars.map(([v, l]) => `<div class="bar"><span>${l}</span><div class="bar-t"><i data-w="${v / top}"></i></div><span>$${fmt(v)}</span></div>`).join('')}</div>` : ''}
      </div>
    </article>`).join('');

  $('#palette').innerHTML = palette.map(([n, h, c]) => `<div class="sw" style="background:${h};color:${c}"><span>${n}</span><b>${h}</b></div>`).join('');
  $('#states').innerHTML = states.map((s) => `
    <div class="st" style="background:${s.soft};border-color:${s.soft};color:${s.ink}">
      <svg viewBox="0 0 24 24" data-k="${s.k}" class="state-ico"></svg>
      <div><b>${s.name}</b><span>${s.p}</span></div>
    </div>`).join('');

  $$('.state-ico').forEach((s) => icon(s, s.dataset.k));
}

/* ---------------------------------------------------------------- scroll y navegación */
let lenis;
function setupScroll() {
  if (!reduce) {
    lenis = new Lenis({ lerp: 0.09 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const t = a.getAttribute('href') === '#top' ? 0 : $(a.getAttribute('href'));
    if (t === null) return;
    e.preventDefault();
    lenis ? lenis.scrollTo(t, { offset: t ? -96 : 0, duration: 1.4 }) : (t ? t.scrollIntoView() : scrollTo(0, 0));
  });

  const nav = $('.nav');
  let last = 0;
  const onScroll = (y) => {
    nav.classList.toggle('scrolled', y > 24);
    nav.classList.toggle('hide', y > 400 && y > last);
    last = y;
  };
  lenis ? lenis.on('scroll', ({ scroll }) => onScroll(scroll)) : addEventListener('scroll', () => onScroll(scrollY));

  const links = $$('.nav-links a');
  links.forEach((a) => {
    const sec = $(a.getAttribute('href'));
    ScrollTrigger.create({ trigger: sec, start: 'top 50%', end: 'bottom 50%', onToggle: (s) => a.classList.toggle('on', s.isActive) });
  });
}

/* ---------------------------------------------------------------- texto */
function splitWords(el) {
  const out = [];
  const word = (w) => {
    const ow = document.createElement('span'); ow.className = 'ow';
    const iw = document.createElement('span'); iw.className = 'iw'; iw.textContent = w;
    ow.appendChild(iw); out.push(iw); return ow;
  };
  const fill = (target, text) => text.split(/(\s+)/).forEach((p) => {
    if (!p) return;
    target.appendChild(/^\s+$/.test(p) ? document.createTextNode(' ') : word(p));
  });
  const nodes = [...el.childNodes];
  el.textContent = '';
  nodes.forEach((n) => {
    if (n.nodeType === 1 && n.tagName === 'EM') {
      const mark = document.createElement('span'); mark.className = 'mark';
      fill(mark, n.textContent); el.appendChild(mark);
    } else fill(el, n.textContent);
  });
  return out;
}

function count(el, dur = 1.6) {
  const n = +el.dataset.count, dec = +el.dataset.dec || 0, o = { v: 0 };
  gsap.to(o, { v: n, duration: dur, ease: 'power3.out', onUpdate: () => { el.textContent = fmt(o.v, dec); } });
}

/* ---------------------------------------------------------------- animaciones */
function setupReveals() {
  if (reduce) { $$('.reveal em').forEach((e) => e.classList.add('mark', 'on')); return; }

  $$('.reveal').forEach((h) => {
    const w = splitWords(h);
    gsap.set(w, { yPercent: 110 });
    if (h.closest('.hero')) { h._words = w; return; }
    ScrollTrigger.create({ trigger: h, start: 'top 88%', once: true, onEnter: () => { gsap.to(w, { yPercent: 0, duration: 1.1, ease: 'expo.out', stagger: 0.045 }); $$('.mark', h).forEach((m) => m.classList.add('on')); } });
  });

  $$('.fade').forEach((el) => {
    if (el.closest('.hero')) return;
    gsap.set(el, { opacity: 0, y: 28 });
    ScrollTrigger.create({ trigger: el, start: 'top 90%', once: true, onEnter: () => gsap.to(el, { opacity: 1, y: 0, duration: 1.1, ease: 'power3.out', delay: (el.dataset.i || 0) * 0.08 }) });
  });

  // filas de comparación
  $$('.cmp').forEach((r) => {
    gsap.set(r, { opacity: 0, y: 20 });
    ScrollTrigger.create({ trigger: r, start: 'top 92%', once: true, onEnter: () => gsap.to(r, { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }) });
  });

  // diagramas
  $$('.diagram, .fig-img').forEach((d) => {
    gsap.fromTo(d, { clipPath: 'inset(12% 6% 12% 6% round 12px)', opacity: 0 }, { clipPath: 'inset(0% 0% 0% 0% round 12px)', opacity: 1, duration: 1.4, ease: 'expo.out', scrollTrigger: { trigger: d, start: 'top 88%', once: true } });
    const img = $('img', d);
    gsap.fromTo(img, { scale: 1.12 }, { scale: 1, duration: 1.8, ease: 'expo.out', scrollTrigger: { trigger: d, start: 'top 88%', once: true } });
  });

  // la cresta del fondo se mueve con el scroll
  gsap.to('.hero-ridge', { yPercent: 30, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });

  // contadores
  ScrollTrigger.create({ trigger: '.mig-figs', start: 'top 88%', once: true, onEnter: () => $$('.mig-figs [data-count]').forEach((el) => count(el, 1.2)) });
  ScrollTrigger.create({ trigger: '#costs', start: 'top 85%', once: true, onEnter: () => {
    $$('#costs [data-count]').forEach((el) => count(el, 2));
    $$('.bar-t i').forEach((b, i) => gsap.to(b, { scaleX: +b.dataset.w, duration: 1.6, ease: 'expo.out', delay: 0.3 + i * 0.12 }));
  } });
}

function setupLayers() {
  const links = $$('#layersNav a');
  $$('.layer').forEach((l, i) => {
    ScrollTrigger.create({ trigger: l, start: 'top 55%', end: 'bottom 55%', onToggle: (s) => { if (s.isActive) links.forEach((a, j) => a.classList.toggle('on', j === i)); } });
  });
  links[0].classList.add('on');
  gsap.to('#layersBar', { scaleY: 1, ease: 'none', scrollTrigger: { trigger: '#layersList', start: 'top 55%', end: 'bottom 55%', scrub: true } });
}

function setupTimeline() {
  const items = $$('.tl-item');
  if (reduce) { items.forEach((i) => i.classList.add('on')); gsap.set('#tlFill', { scaleX: 1 }); return; }
  ScrollTrigger.create({
    trigger: '#tl', start: 'top 80%', end: 'top 30%', scrub: true,
    onUpdate: (s) => {
      gsap.set('#tlFill', { scaleX: s.progress });
      items.forEach((it, i) => it.classList.toggle('on', i / (items.length - 1) <= s.progress + 0.01));
    }
  });
  gsap.from(items, { opacity: 0, y: 24, duration: 1, stagger: 0.07, ease: 'power3.out', scrollTrigger: { trigger: '#tl', start: 'top 85%', once: true } });
}

function setupPipeline() {
  const steps = $$('#pipeSteps li');
  if (reduce) { steps.forEach((s) => s.classList.add('on')); return; }
  ScrollTrigger.create({
    trigger: '#pipe', start: 'top 80%', end: 'top 35%', scrub: true,
    onUpdate: (s) => {
      gsap.set('#pipeFill', { scaleX: s.progress });
      $('#pipeDot').style.left = s.progress * 100 + '%';
      steps.forEach((st, i) => st.classList.toggle('on', i / (steps.length - 1) <= s.progress + 0.01));
    }
  });
}

/* ---------------------------------------------------------------- tarjeta del héroe */
function setupHeroSensor() {
  const line = $('#heroLine'), dot = $('#heroDot'), tEl = $('#heroTemp');
  const N = 48, pts = [];
  const Y = (t) => 40 + ((-16 - t) / 4) * 60;
  let v = -18.2, phase = 0;
  for (let i = 0; i < N; i++) { phase += 0.35; pts.push(-18.2 + 0.45 * Math.sin(phase) + 0.18 * Math.sin(phase * 2.7)); }
  const draw = () => {
    const d = pts.map((t, i) => `${i ? 'L' : 'M'}${(i / (N - 1)) * 400} ${Y(t).toFixed(2)}`).join(' ');
    line.setAttribute('d', d);
    dot.setAttribute('cy', Y(pts[N - 1]).toFixed(2));
  };
  draw();
  let tick = 0;
  setInterval(() => {
    if (reduce) return;
    phase += 0.35;
    v = -18.2 + 0.45 * Math.sin(phase) + 0.18 * Math.sin(phase * 2.7) + (Math.random() - 0.5) * 0.12;
    pts.shift(); pts.push(v); draw();
    if (++tick % 4 === 0) tEl.textContent = temp(v);
  }, 260);
}

/* ---------------------------------------------------------------- demo */
function setupDemo() {
  const range = $('#dRange'), tEl = $('#dTemp'), badge = $('#dBadge'), stEl = $('#dState'), ico = $('#dIcon'), note = $('#dNote');
  const cv = $('#dChart'), ctx = cv.getContext('2d');
  const box = $('#dAlert'), aTitle = $('#dAlertTitle'), aBar = $('#dAlertBar'), aText = $('#dAlertText');
  const NOTES = {
    normal: 'Within range. Nobody needs to act.',
    advertencia: 'Close to the limit. The tower sees it highlighted and can act before it becomes an excursion.',
    excursion: 'Out of range. An alert opens with an acknowledgement and the reading is kept as evidence.',
    sinsenal: 'The sensor stopped reporting. The alert fires even with no temperature to show.'
  };
  const COL = { normal: '#0D7894', advertencia: '#C98A12', excursion: '#D93A2B', sinsenal: '#7B5FD8' };
  let cut = false, shift = 'day', state = '', buf = [], W = 0, H = 200, alertFor = '', tw;
  const MAXB = 120;
  const resize = () => { const d = Math.min(2, devicePixelRatio || 1); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * d; cv.height = H * d; ctx.setTransform(d, 0, 0, d, 0, 0); };
  addEventListener('resize', resize); resize();
  const Y = (t) => H - 16 - ((t + 28) / 22) * (H - 32);

  function setAlert(st) {
    if (st === 'excursion' || st === 'sinsenal') {
      if (alertFor === st) return;
      alertFor = st; box.dataset.on = 'true';
      aTitle.textContent = st === 'excursion' ? 'Temperature excursion' : 'Sensor without signal';
      aText.textContent = 'Detecting and routing…';
      const secs = Math.round(24 + Math.random() * 20), o = { v: 0 };
      tw && tw.kill();
      tw = gsap.to(o, { v: secs / 60, duration: 1.4, ease: 'power2.out', onUpdate: () => { aBar.style.width = o.v * 100 + '%'; }, onComplete: () => {
        aText.textContent = `On screen after ${secs} s at the ${shift === 'day' ? 'control tower' : 'night quality on-call'}. Simulated with sample values.`;
      } });
    } else if (alertFor) {
      alertFor = ''; box.dataset.on = 'false'; tw && tw.kill();
      gsap.to(aBar, { width: 0, duration: 0.6 });
      aTitle.textContent = 'No active alerts';
      aText.textContent = 'The reading is back in range. The alert closes and stays in the history.';
    }
  }
  icon(ico, 'normal');

  let last = 0, ph = 0;
  gsap.ticker.add((time) => {
    if (time - last < 0.07) return; last = time; ph += 0.3;
    const r = cut ? null : +range.value + 0.12 * Math.sin(ph) + (Math.random() - 0.5) * 0.12;
    buf.push(r); if (buf.length > MAXB) buf.shift();
    const rect = cv.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > innerHeight) return;

    const st = stateOf(r);
    if (st !== state) { state = st; badge.dataset.state = st; stEl.textContent = NAME[st]; icon(ico, st); note.textContent = NOTES[st]; setAlert(st); }
    tEl.textContent = r === null ? '– –.–' : temp(r);

    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = 'rgba(221,243,248,.6)'; ctx.fillRect(0, Y(-16), W, Y(-20) - Y(-16));
    ctx.strokeStyle = '#DDE3E6'; ctx.setLineDash([3, 4]); ctx.lineWidth = 1;
    [-16, -20].forEach((t) => { ctx.beginPath(); ctx.moveTo(0, Y(t) + .5); ctx.lineTo(W, Y(t) + .5); ctx.stroke(); });
    ctx.setLineDash([]);
    ctx.font = '12px "Schibsted Grotesk"'; ctx.fillStyle = '#8696A0';
    ctx.fillText('−16 °C', 4, Y(-16) - 6); ctx.fillText('−20 °C', 4, Y(-20) + 16);
    ctx.lineWidth = 2; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    const dx = W / (MAXB - 1), off = (MAXB - buf.length) * dx;
    let prev = null;
    buf.forEach((t, i) => {
      const x = off + i * dx;
      if (t === null) { if (prev) { ctx.strokeStyle = COL.sinsenal; ctx.setLineDash([3, 5]); ctx.beginPath(); ctx.moveTo(prev.x, prev.y); ctx.lineTo(x, prev.y); ctx.stroke(); ctx.setLineDash([]); prev.x = x; } return; }
      const y = Y(t);
      if (prev) { ctx.strokeStyle = COL[stateOf(t)]; ctx.beginPath(); ctx.moveTo(prev.x, prev.y); ctx.lineTo(x, y); ctx.stroke(); }
      prev = { x, y };
    });
    if (prev) { ctx.fillStyle = COL[st]; ctx.beginPath(); ctx.arc(prev.x, prev.y, 4.5, 0, 7); ctx.fill(); }
  });

  $('#dCut').addEventListener('click', (e) => { cut = !cut; e.currentTarget.classList.toggle('on', cut); e.currentTarget.textContent = cut ? 'Restore signal' : 'Cut signal'; });
  $$('.seg button').forEach((b) => b.addEventListener('click', () => {
    shift = b.dataset.shift; $$('.seg button').forEach((x) => x.classList.toggle('on', x === b));
    if (alertFor) { const f = alertFor; alertFor = ''; setAlert(f); }
  }));
}

/* ---------------------------------------------------------------- lightbox */
function setupLightbox() {
  const lb = $('#lightbox'), sc = $('.lb-scroll'), im = $('.lb-scroll img');
  const close = () => { lb.hidden = true; lenis && lenis.start(); };
  document.addEventListener('click', (e) => {
    const f = e.target.closest('[data-zoom]');
    if (!f) return;
    const i = $('img', f); im.src = i.src; im.alt = i.alt; sc.classList.remove('zoom'); lb.hidden = false; lenis && lenis.stop();
  });
  sc.addEventListener('click', () => sc.classList.toggle('zoom'));
  $('.lb-close').addEventListener('click', close);
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && !lb.hidden) close(); });
}

/* ---------------------------------------------------------------- entrada */
function intro() {
  const pre = $('#pre'), path = $('.pre-mark path'), dot = $('.pre-mark circle');
  const len = path.getTotalLength();
  const h1 = $('.hero h1');
  const heroFades = $$('.hero .fade');
  const ridge = $('.hero-ridge path'), rlen = ridge.getTotalLength();
  if (reduce) { pre.remove(); document.body.classList.remove('is-loading'); return; }
  gsap.set(path, { strokeDasharray: len, strokeDashoffset: len });
  gsap.set(dot, { scale: 0, transformOrigin: 'center' });
  gsap.set(heroFades, { opacity: 0, y: 28 });
  gsap.set(ridge, { strokeDasharray: rlen, strokeDashoffset: rlen });
  gsap.set('.nav', { yPercent: -100 });

  gsap.timeline()
    .to(path, { strokeDashoffset: 0, duration: 1.1, ease: 'power2.inOut' })
    .to(dot, { scale: 1, duration: 0.5, ease: 'back.out(3)' }, '-=0.2')
    .to(pre, { yPercent: -100, duration: 1, ease: 'expo.inOut', delay: 0.2, onStart: () => document.body.classList.remove('is-loading') })
    .to(h1._words || [], { yPercent: 0, duration: 1.2, ease: 'expo.out', stagger: 0.05, onComplete: () => $$('.mark', h1).forEach((m) => m.classList.add('on')) }, '-=0.45')
    .to(heroFades, { opacity: 1, y: 0, duration: 1.1, ease: 'power3.out', stagger: 0.1 }, '-=0.9')
    .to('.nav', { yPercent: 0, duration: 1, ease: 'expo.out' }, '-=1')
    .to(ridge, { strokeDashoffset: 0, duration: 2.4, ease: 'power2.inOut' }, '-=1.4')
    .add(() => { pre.remove(); $$('#metrics [data-count]').forEach((el) => count(el)); });
}

/* ---------------------------------------------------------------- arranque */
render();
setupScroll();
setupLightbox();
setupHeroSensor();
setupDemo();

document.fonts.ready.then(() => {
  setupReveals();
  intro();
  setupLayers();
  setupTimeline();
  setupPipeline();
  ScrollTrigger.refresh();
  addEventListener('load', () => ScrollTrigger.refresh());
});
