# GGCF — A brighter tomorrow

Paper file: https://app.paper.design/file/01M4EF9BJ4BBEM40QX2PFG7QCC/p-1-0/71-1

Six editable artboards: brand foundations; component states; initial desktop and mobile explorations; inspiration and operating rules; refined desktop with original copy; refined mobile, story, and motion specifications. Boards 05 and 06 are the current direction and supersede the speculative wording in the initial exploration boards.

The working homepage prototype is at http://localhost:8088/prototype.html (run `python3 -m http.server 8088` from the repository). All original homepage copy and accessible labels are retained. The original production pages remain unchanged. Links lead to the existing pages; this is a visual and motion prototype, not a new payment integration.

Validation: homepage text comparison passed for 78 text segments and 11 accessible labels/attributes; JavaScript syntax check passed; mobile (390px), tablet (768px), and desktop (1440px) layouts were visually reviewed with no horizontal overflow. Both hero slides, menu opening/closing and Escape focus return, capped parallax, card perspective, and final impact values (600, 70, 50) were exercised. Reduced-motion rules are implemented; OS preference emulation was not available in this browser workflow.

Previews: prototype-desktop.jpg, prototype-mobile.jpg, and paper-refinement.jpg. The prototype also fixes a missed impact counter trigger when scrolling quickly past the original heading, without changing the figures.

## Identity

Preserve the existing red/gold heart-and-hand logo. Primary orange #FF6F0F; dark teal #001D23; green #00704A. Add warm paper #F8F5EF, peach #FFF0E6, and mint #E6F2EC. Dark teal text on orange actions.

Current direction: Switzer Medium (500) replaces Fraunces for headlines; Switzer 400–600 supports body and UI; all button labels use Switzer Medium (500). GGCF uses Clash Display Semibold (600) with tightened tracking; the supporting wordmark text uses Switzer 500. This typography choice supersedes the earlier Paper typography studies. Desktop hero scales from 44 to 76px with 1.06 line-height; mobile hero 46px. Body 18/30, UI 14px, section headings 36–56px. Active webfonts are self-hosted in fonts/, with shared declarations in css/fonts.css and typography in css/typography.css. design/fonts.css reuses those declarations.

Motion prototype: 700ms hero reveal with 20px travel; 650ms section reveal with 22px travel; desktop photograph parallax capped at 34px; pointer-driven card perspective capped at ±1.5 degrees. Parallax and tilt are disabled for touch/mobile. Reduced-motion preferences disable reveals, transforms, transitions, and animated number updates. Hero slides use manual navigation. Mobile menu supports focus containment and Escape dismissal.

## Layout and interaction

Spacing: 8, 16, 24, 32, 48, 64, 96px. Desktop: 12 columns, 1280px maximum content width, 24px gutters. Tablet: 8 columns with 32px margins. Mobile: 4 columns with 20px margins.

Controls: 52px tall, 8px radius; cards: 16px radius. Feature photography can use an arch crop. Minimum interaction target 44px. Visible focus, persistent field labels, explanatory errors, loading and disabled states. Validate contrast during implementation. Use 150–220ms transitions and respect reduced motion.

## Content and journey

Mission → programs → verified impact → stories → donation or involvement. Navigation: Our work, Our story, Impact, Get involved, Donate. Keep the faith-centered mission and Ghana context explicit.

Use real GGCF photography with accurate captions, dignified crops, and consent. Current figures (600+ schoolchildren, 70+ mothers/newborns, 50+ families) require verified periods and sources before launch. Do not assume figures are unique people or add them together.

Current payment journey continues to PayPal. Monthly giving is a proposed state requiring a real recurring payment integration. Do not collect donor details without processing them.

## Showcase research

- [HopeRise — Phenomenon, Dribbble](https://dribbble.com/shots/26290772-HopeRise-Charity-Landing-Page-Design): oversized typography, whitespace, warm surfaces and donation choices. A design concept; popularity is not conversion evidence.
- [Voices United — Phenomenon, Dribbble](https://dribbble.com/shots/26183245-Voices-United-Nonprofit-Organization-Website-Design): editorial storytelling and modular participation.
- [HopeRise mobile — Dribbble](https://dribbble.com/shots/26666035-Mobile-First-Charity-Web-Design-HopeRise): comfortable mobile donation controls.
- [SunCharity — Awwwards](https://www.awwwards.com/sites/suncharity-foundation): 2022 nominee, concise navigation and optimistic identity. Not a Site of the Day winner.
- [Luminar Foundation — Behance](https://www.behance.net/gallery/252149809/Luminar-Foundation-Branding-Website-Design): strategy-led branding, expressive typography and coherent visual language.

Reference imagery on the Paper research board is credited inspiration. Build an original GGCF interface from these principles. A premium design direction does not establish a guaranteed monetary valuation.
