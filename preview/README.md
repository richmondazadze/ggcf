# GGCF redesign preview

Open http://localhost:8088/preview/index.html while the repository's local HTTP server is running. All navigation remains inside `preview/`. Home, About, Donate, Contact and the 404 page are included. The original website pages have not been replaced; no commit was made.

The pages translate the approved Paper compositions in `design/pages/` into responsive HTML. Switzer and Clash Display are served from the existing local licensed fonts. Photography is served as local responsive WebP variants; existing brand and transfer logos are preserved.

## Motion and accessibility

Automatic two-photo background hero with overlay, fixed 3.5-second slide interval, smooth 1.4-second transitions, manual controls and touch swipe; 1-second staggered headline entrances; staggered element-level scroll reveals; desktop photos move inside clipped parallax frames, capped at 42px; card tilt capped at 1.5 degrees; 200ms button feedback; animated impact figures; on-demand story video; back-to-top control. The slideshow clock is independent of image loading and hover. It respects reduced-motion preferences, hidden tabs and keyboard focus within a slide. Mobile disables photo parallax and card tilt. Reduced-motion preferences stop animation and expose all content. The mobile menu traps focus, supports Escape, and makes the underlying content inert. Forms use persistent labels and native required-field validation.

## Existing service connections

The donation form opens the existing PayPal.me recipient with the entered USD amount. The monthly donation option is omitted. Donation type/name/email are not saved or transmitted by the preview; PayPal handles the actual transaction. The contact form retains its existing Formspree endpoint. No payment or contact submission was performed during validation. The original Google Drive story video loads only after Play is pressed.

## Build and verification

`python3 preview/build.py` regenerates the five HTML pages and WebP derivatives from the saved Paper HTML. Requires BeautifulSoup and Pillow. Shared CSS and JavaScript are maintained separately in `preview/assets/`.

Checked desktop and mobile layouts, carousel controls, mobile menu and Escape, native empty-form validation, local asset/link/anchor resolution, unique IDs, one H1 per page, labeled form fields, original paragraph preservation, JavaScript syntax, and unchanged original-page hashes. The original pages' hashes are recorded in `original-page-hashes.json`.

## Review refinements

Corrected the shared WhatsApp icon across all preview pages; bottom-aligned service-card buttons and balanced heading heights; rebuilt the founder profile using the supplied `theo_mensah.png` portrait, Clash Display name, role badge and personal LinkedIn/Instagram links; removed missing-photo placeholder dots; preserved transfer logos with `object-fit: contain`; moved scroll reveals from large sections to individual headings, cards, image frames and profile elements. Original copy and production pages remain intact.

## Final browser comments

Removed the hero play/pause control and loading-style progress bar. Slides advance on a fixed 3.5-second interval. Impact and volunteer cards share the same bottom-aligned button rule as service cards. Founder role/email use Clash Display, the role is plain text, the profile has square corners, and its square social controls are centered. Donation selects use a custom chevron centered vertically and inset 18px from the right edge.

Impact stories: About now presents six uniform landscape cards, ordered newest first, linking to `story-*.html`. Full original copy is retained on each detail page. Rebuild with `python3 preview/build.py`. Shared content source: https://drive.google.com/drive/folders/1-JJmocMdYsnGJewq_d9S8AUYJDHvzmAA (2022–2023, 2024, 2025, completed 2026). New event narratives and photos must be matched before publishing additional stories.

2026-10-09: Added 2024 New Amakom, 2025 Missionaries of Charity Sisters, and completed 2026 Asonsuaso school water project stories. New content is maintained in `content/impact-stories.json`; provenance and outstanding factual details are in `content/story-sources.md`. 2026 includes four chapters, real construction photography, initial/handover film stills, and click-to-load Drive films without external Drive links. All six story cards appear newest first.
