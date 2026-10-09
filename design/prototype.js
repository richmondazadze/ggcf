(() => {
  'use strict';
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const desktop = matchMedia('(min-width: 992px) and (hover: hover) and (pointer: fine)');
  const sections = [...document.querySelectorAll('main > section:not(:first-child)')];
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.remove('is-waiting');
      observer.unobserve(entry.target);
    }
  }), { threshold: 0.06 });
  sections.forEach(section => {
    section.classList.add('reveal');
    if (!motion.matches && section.getBoundingClientRect().top > innerHeight) {
      section.classList.add('is-waiting');
      observer.observe(section);
    }
  });
  let frame = 0;
  const hero = document.querySelector('#header-carousel');
  const update = () => {
    frame = 0;
    const offset = !motion.matches && desktop.matches ? Math.min(scrollY * .07, 34) : 0;
    hero.style.setProperty('--photo-shift', `${offset}px`);
    document.querySelector('.back-to-top')?.classList.toggle('is-visible', scrollY > 300);
  };
  const schedule = () => { if (!frame) frame = requestAnimationFrame(update); };
  addEventListener('scroll', schedule, { passive: true });
  desktop.addEventListener('change', schedule);
  const counters = [...document.querySelectorAll('.countup')];
  let counterFrames = [];
  const finishCounters = () => {
    counterFrames.forEach(cancelAnimationFrame);
    counterFrames = [];
    counters.forEach(el => { el.textContent = el.dataset.target; });
  };
  const impact = document.querySelector('section[aria-labelledby="impact-highlights-title"]');
  const counterObserver = new IntersectionObserver(entries => {
    if (!entries.some(entry => entry.isIntersecting)) return;
    counterObserver.disconnect();
    if (motion.matches) { finishCounters(); return; }
    const start = performance.now();
    const tick = time => {
      if (motion.matches) { finishCounters(); return; }
      const progress = Math.min((time - start) / 1000, 1);
      counters.forEach(el => { el.textContent = Math.round(Number(el.dataset.target) * (1 - (1 - progress) ** 3)); });
      if (progress < 1) counterFrames = [requestAnimationFrame(tick)];
    };
    counterFrames = [requestAnimationFrame(tick)];
  }, { threshold: 0.05 });
  if (impact) counterObserver.observe(impact);
  document.querySelectorAll('.causes-item,.service-item').forEach(card => {
    card.addEventListener('pointermove', event => {
      if (motion.matches || !desktop.matches) return;
      const bounds = card.getBoundingClientRect();
      card.style.setProperty('--tilt-x', `${(0.5 - (event.clientY - bounds.top) / bounds.height) * 3}deg`);
      card.style.setProperty('--tilt-y', `${((event.clientX - bounds.left) / bounds.width - 0.5) * 3}deg`);
    });
    card.addEventListener('pointerleave', () => {
      card.style.setProperty('--tilt-x', '0deg');
      card.style.setProperty('--tilt-y', '0deg');
    });
  });
  const reduce = () => {
    if (motion.matches) {
      sections.forEach(section => section.classList.remove('is-waiting'));
      finishCounters();
      document.querySelectorAll('.causes-item,.service-item').forEach(card => {
        card.style.setProperty('--tilt-x', '0deg');
        card.style.setProperty('--tilt-y', '0deg');
      });
    }
    schedule();
  };
  motion.addEventListener('change', reduce);
  reduce();
  const navMenu = document.querySelector('.navbar-collapse');
  navMenu?.addEventListener('shown.bs.collapse', event => {
    document.body.style.overflow = 'hidden';
    document.querySelector('main').inert = true;
    document.querySelector('.footer').inert = true;
    event.target.querySelector('a')?.focus();
  });
  navMenu?.addEventListener('hidden.bs.collapse', () => {
    document.body.style.overflow = '';
    document.querySelector('main').inert = false;
    document.querySelector('.footer').inert = false;
    document.querySelector('.navbar-toggler').focus();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Tab' && navMenu?.classList.contains('show')) {
      const items = [...navMenu.querySelectorAll('a,button')].filter(el => el.getClientRects().length);
      const first = items[0], last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
    if (event.key === 'Escape') {
      const menu = document.querySelector('.navbar-collapse.show');
      if (menu && window.bootstrap) {
        (bootstrap.Collapse.getInstance(menu) || new bootstrap.Collapse(menu, { toggle: false })).hide();
        document.querySelector('.navbar-toggler').focus();
      }
    }
  });
})();
