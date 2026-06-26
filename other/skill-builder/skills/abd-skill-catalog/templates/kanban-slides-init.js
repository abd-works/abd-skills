import Reveal from 'https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.esm.js';

const deck = new Reveal({
  hash: true,
  history: true,
  controls: true,
  controlsTutorial: false,
  progress: true,
  slideNumber: 'c/t',
  showSlideNumber: 'all',
  width: 1280,
  height: 720,
  margin: 0,
  minScale: 0.2,
  maxScale: 2.0,
  navigationMode: 'default',
  transition: 'slide',
  transitionSpeed: 'fast',
  backgroundTransition: 'fade',
  autoAnimateDuration: 0.4,
  center: false,
});

deck.initialize();

// Spotlight stagger only — tickets are static (no stagger on slide enter).
const STEP_MS = 320;
function play(slide) {
  if (!slide) return;
  slide.querySelectorAll('.kb-ticket').forEach((t) => t.classList.add('shown'));
  const stagger = slide.querySelectorAll('[data-d]');
  stagger.forEach((el) => {
    const d = parseInt(el.getAttribute('data-d'), 10) || 0;
    setTimeout(() => el.classList.add('shown'), 200 + d * STEP_MS);
  });
  slide.querySelectorAll('.kb-col-def').forEach((d) => d.classList.add('shown'));
}
function resetSlide(slide) {
  if (!slide) return;
  slide.querySelectorAll('[data-d]').forEach((el) => el.classList.remove('shown'));
}

function slideToId(id) {
  if (!id || id.startsWith('/')) return;
  const target = document.getElementById(id);
  if (!target) return;
  const indices = deck.getIndices(target);
  if (indices) deck.slide(indices.h, indices.v, indices.f);
}

deck.on('ready', (e) => {
  slideToId(window.location.hash.replace(/^#/, ''));
  play(e.currentSlide);
});
deck.on('slidechanged', (e) => {
  if (e.previousSlide) resetSlide(e.previousSlide);
  play(e.currentSlide);
  const id = e.currentSlide && e.currentSlide.id;
  if (id) history.replaceState(null, '', `#${id}`);
});

document.querySelectorAll('.kb-col-head--link[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const href = link.getAttribute('href');
    if (!href || href.length < 2) return;
    if (!document.getElementById(href.slice(1))) return;
    event.preventDefault();
    slideToId(href.slice(1));
    history.replaceState(null, '', href);
  });
});

window.addEventListener('hashchange', () => {
  slideToId(window.location.hash.replace(/^#/, ''));
});
