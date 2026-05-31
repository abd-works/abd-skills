(function () {

  const deck = document.getElementById('kanban-slides-deck');

  if (!deck) return;



  const slides = Array.from(deck.querySelectorAll(':scope > .kb-slide'));

  const STEP_MS = 320;



  function playSlide(slide) {

    if (!slide) return;

    slide.querySelectorAll('.kb-ticket').forEach((ticket, index) => {

      if (ticket.classList.contains('shown')) return;

      window.setTimeout(() => ticket.classList.add('shown'), 80 + index * 90);

    });

    slide.querySelectorAll('[data-d]').forEach((el) => {

      if (el.classList.contains('shown')) return;

      const delay = parseInt(el.getAttribute('data-d'), 10) || 0;

      window.setTimeout(() => el.classList.add('shown'), 200 + delay * STEP_MS);

    });

    slide.querySelectorAll('.kb-col-def:not(.shown)').forEach((def, index) => {

      window.setTimeout(() => def.classList.add('shown'), 100 + index * 100);

    });

  }



  function resetSlide(slide) {

    if (!slide) return;

    slide.querySelectorAll('.kb-ticket.shown').forEach((el) => el.classList.remove('shown'));

    slide.querySelectorAll('[data-d].shown').forEach((el) => el.classList.remove('shown'));

    slide.querySelectorAll('.kb-col-def.shown').forEach((el) => el.classList.remove('shown'));

  }



  let activeIndex = -1;



  function onSlideVisible(index) {

    if (index === activeIndex) return;

    if (activeIndex >= 0 && slides[activeIndex]) {

      resetSlide(slides[activeIndex]);

    }

    activeIndex = index;

    playSlide(slides[index]);

  }



  function currentIndex() {

    let best = 0;

    let bestVis = -1;

    slides.forEach((slide, index) => {

      const rect = slide.getBoundingClientRect();

      const visible = Math.min(rect.bottom, window.innerHeight) - Math.max(rect.top, 0);

      if (visible > bestVis) {

        bestVis = visible;

        best = index;

      }

    });

    return best;

  }



  function scrollToIndex(index) {

    const i = Math.max(0, Math.min(slides.length - 1, index));

    slides[i].scrollIntoView({ behavior: 'smooth', block: 'start' });

  }



  function scrollToHash() {

    const id = window.location.hash.replace(/^#/, '');

    if (!id) return;

    const target = document.getElementById(id);

    if (target && slides.includes(target)) {

      target.scrollIntoView({ block: 'start' });

    }

  }



  document.querySelectorAll('.kb-col-head--link[href^="#"]').forEach((link) => {

    link.addEventListener('click', (event) => {

      const href = link.getAttribute('href');

      if (!href || href.length < 2) return;

      const target = document.getElementById(href.slice(1));

      if (!target || !slides.includes(target)) return;

      event.preventDefault();

      target.scrollIntoView({ behavior: 'smooth', block: 'start' });

      history.replaceState(null, '', href);

    });

  });



  document.addEventListener('keydown', (event) => {

    if (event.target.closest('input, textarea, select, [contenteditable="true"]')) return;

    const idx = currentIndex();

    if (event.key === 'ArrowDown' || event.key === 'PageDown') {

      event.preventDefault();

      scrollToIndex(idx + 1);

    } else if (event.key === 'ArrowUp' || event.key === 'PageUp') {

      event.preventDefault();

      scrollToIndex(idx - 1);

    }

  });



  const observer = new IntersectionObserver(

    (entries) => {

      entries.forEach((entry) => {

        if (!entry.isIntersecting || entry.intersectionRatio < 0.45) return;

        const index = slides.indexOf(entry.target);

        if (index >= 0) onSlideVisible(index);

      });

    },

    { threshold: [0.45, 0.6, 0.75] },

  );



  slides.forEach((slide) => observer.observe(slide));



  scrollToHash();

  window.addEventListener('hashchange', scrollToHash);



  window.requestAnimationFrame(() => onSlideVisible(currentIndex()));

})();


