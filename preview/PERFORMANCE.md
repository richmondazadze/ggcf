# Preview performance review — 2026-10-08

Implemented without changing the approved layout, copy, image compression quality, or motion timing:

- Corrected team portrait `sizes` to match the actual responsive grid. At the verified 1440px, DPR1 viewport, all six photos select 480px variants instead of oversized 768px variants. Combined files: 311,250 bytes versus 568,700 bytes, a 45% reduction for these portraits.
- Added a responsive 480px founder portrait (36,898 bytes), retaining the 800px version (102,332 bytes) for higher-density displays. Both use quality 91 WebP.
- Prioritized the first hero photograph; the second remains eager but low priority so it does not compete equally with the initial hero.
- Parallax processes only photos within 160px of the viewport. Layout measurements are batched before style writes, using one requestAnimationFrame per scroll frame.
- Card tilt caches geometry and coalesces pointer events into one animation-frame update.
- Photo compositing hints are enabled only near the viewport when desktop motion is enabled. Mobile and reduced-motion behavior remain lightweight.
- Image generation skips unchanged derivatives on rebuild.

Existing efficient behavior retained: responsive WebP photography, lazy lower-page images, deferred vanilla JavaScript, local WOFF2 fonts with swap, and video loaded only after Play.

## Verification

- Five-page build and JavaScript syntax check passed.
- Referenced local assets exist on all five pages.
- Browser verification at 1440px and 390px: no horizontal overflow; correct desktop portrait sources; offscreen parallax layers inactive; mobile parallax reset to zero; no browser console errors.
- Production page hashes unchanged. No commits.
- CSS 19,930 bytes; JavaScript 7,550 bytes (uncompressed).

## Hosting work before launch

Configure compression and appropriate caching on the actual host, using versioned asset URLs when enabling long-lived immutable caching. Measure Core Web Vitals and throttled loading on the deployed preview. Local testing confirms implementation and asset savings, but does not establish a production Lighthouse score or network loading time.

## About impact layout recommendation

Replace repeated portrait-photo/long-essay rows with a compact impact journal: one featured event, followed by equal landscape image cards with dates, titles, and aligned story links. About should show a small selection; a dedicated impact archive can hold every event. Full event pages retain every existing paragraph and hold each event's photo gallery. Use pagination as the archive grows, and year/program filters once there are enough events to benefit. New entries require their actual approved text, dates, locations, and matching photos. The three existing stories now use uniform cards and individual pages. Their complete original paragraphs are preserved; 2024–2026 Drive events have been added as three new stories; 2026 uses four films loaded only after user interaction.
