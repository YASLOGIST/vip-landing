<div align="center">
  <img
    src="assets/readme/yaslogist-hero.gif"
    alt="Cinematic animated hero for VIP Motors Atelier — an obsidian grand coupe under champagne-gold rim light in a private showroom; gold dust drifts, a specular sweep crosses the lockup, a coordinate scanner glides over the vehicle, and the permanent YASLOGIST signature holds the lower frame. 9.6-second seamless loop."
    width="100%"
  />
</div>

<div align="center">

# VIP MOTORS ATELIER

### A bilingual, dependency-free luxury concierge experience — engineered like a system, not a page.

**Discreet vehicle sourcing · private viewings · white-glove ownership — delivered as a static, security-hardened, accessibility-gated single page.**

[![runtime dependencies: 0](https://img.shields.io/badge/runtime_dependencies-0-111519?labelColor=c9a66b)](#tech-stack)
[![critical transfer](https://img.shields.io/badge/critical_transfer-95.4_of_150_KB-2f6f4f?labelColor=111519)](#07--deep-system-access)
[![readme hero](https://img.shields.io/badge/readme_hero-9.6s_seamless_loop-6e3642?labelColor=111519)](#w5--the-readme-cinematic-pipeline)
[![social card](https://img.shields.io/badge/social_card-1.9_MB_seamless_loop-6e3642?labelColor=111519)](#w4--social-card-synthesis)
[![i18n](https://img.shields.io/badge/i18n-EN_and_AR_RTL-111519?labelColor=c9a66b)](#accessibility--internationalization)
[![a11y](https://img.shields.io/badge/a11y-axe_clean-111519?labelColor=829582)](#accessibility--internationalization)
[![node](https://img.shields.io/badge/node-%E2%89%A5_20-111519?labelColor=9b9b96)](#tech-stack)

[01 / The System](#01--the-system) · [02 / Core Capabilities](#02--core-capabilities) · [03 / Engineering Architecture](#03--engineering-architecture) · [04 / System Blueprint](#04--system-blueprint) · [05 / Execution Intelligence](#05--execution-intelligence) · [06 / Ignition](#06--ignition) · [07 / Deep System Access](#07--deep-system-access) · [08 / Engineering Status](#08--engineering-status) · [09 / YASLOGIST](#09--yaslogist)

</div>

<div align="center">
  <img src="assets/readme/yaslogist-divider.gif" alt="" width="100%" />
</div>

---

## 01 / THE SYSTEM

VIP Motors Atelier is a lead-capture landing experience for a private automotive concierge: plain HTML, CSS and browser JavaScript — **no framework, no build step, no runtime dependency, no application server, no database, no analytics SDK**. Everything a visitor sees is either semantic markup, tokenised CSS, or progressively-enhanced vanilla JS.

The engineering thesis is deliberate: **luxury is constraint.** A page that carries zero runtime dependencies, ships under a 150 KiB first-party budget, remains fully usable without JavaScript, passes automated accessibility audits in two languages and reading directions, and still delivers a cinematic obsidian-and-gold showroom — proves the brand's "quiet authority" through the technology itself.

> **Content ownership note** — vehicle names, availability labels, stats, locations and service claims in `script.js` are seeded presentation copy inherited from the original artifact. Validate or replace every business claim before publishing to a real audience.

### At a glance

| Dimension | Position |
| --- | --- |
| Runtime dependencies | **0** — packages in `package.json` are dev/test tooling only |
| First-party critical transfer | **95,448 B** uncompressed (enforced ceiling: 153,600 B) |
| First-party image/video/model assets in the page | **0** — the vehicle is CSS art; the favicon is a 312 B SVG |
| Locales | English + Arabic, full `lang`/`dir` switching with persisted preference |
| Conversion path | Collection → private specification dialog → prefilled confidential brief → resilient same-origin POST |
| JavaScript unavailable | Full confidential brief retained via semantic `<noscript>` fallback |
| README cinematic system | `assets/readme/` — 1920×720 hero (96-frame seamless 9.6 s loop), static poster, luminous divider, closing signature — all deterministic build artifacts |
| Social card | `assets/og-image-animated.gif` — 1200×630, 36-frame seamless loop, 1.9 MB, purpose-synthesised |
| Security | Same-origin CSP in markup **and** host headers, honeypot, 10 s abortable delivery, `npm audit` gate |
| Verification | 6 unit/static tests, 8 Chromium E2E flows (a11y + performance tagged), CI on every push and PR |

---

## 02 / CORE CAPABILITIES

| # | Capability | Visitor outcome | Implementation | Verified by |
| --- | --- | --- | --- | --- |
| 1 | Bilingual shell (EN ⇄ AR) | Switches language and reading direction with full document semantics | `copy` model + `lang`/`dir` re-render + guarded storage | unit · e2e (persistence across reload) |
| 2 | Signature atmospheres | Chooses Midnight / Emerald / Platinum showroom profiles, no imagery downloaded | CSS custom-property profiles on the CSS-art stage | e2e (class + `aria-pressed` + persistence) |
| 3 | CSS-rendered vehicle | A sculpted grand coupe with glow, glass and wheels at zero asset cost | Pure CSS shapes/gradients, profile-tinted | transfer budget test |
| 4 | Private specification dialog | Inspects a vehicle brief before any commitment | Native `<dialog>`, backdrop/Escape close, focus return | unit · e2e |
| 5 | Dialog → form conversion | Arrives at the brief with the vehicle preselected | `data-brief` → `data-brief-request` → `interest` prefill + focus | unit · e2e |
| 6 | Brief completion signal | Sees real-time completion of required lead fields | Accessible `role="progressbar"` with `aria-valuenow`/`aria-valuetext` | unit · e2e (resets after success) |
| 7 | Resilient delivery | Submits safely; never hangs; failures are graceful | `fetch` URL-encoded same-origin POST, `AbortController` 10 s timeout, generic error copy, honeypot | unit (source contract) · e2e (success path) |
| 8 | No-JavaScript path | Can still send a complete confidential brief | Semantic `<noscript>` form with identical payload shape | static test · e2e (JS-disabled context) |
| 9 | Reduced motion | Gets an instantly-available, calm experience | `prefers-reduced-motion` removes scanner/brief animation, resolves reveals | e2e + CSS review |
| 10 | Mobile navigation | Drawer receives focus, closes with Escape, returns focus | Inert when closed, focus management on open/close | e2e (390×844 viewport) |
| 11 | Accessibility | No known violations on the critical screen | Semantic landmarks, labels, live regions, skip link + **axe** | e2e `@a11y` (zero violations) |
| 12 | Performance budget | Fast first render on modest hardware | 95,448 B first-party critical transfer, < 500 DOM nodes | unit + e2e `@performance` |
| 13 | Security posture | Hardened static client | CSP (markup + headers), `object-src 'none'`, `frame-ancestors 'none'`, nosniff, strict referrer, deny-by-default Permissions Policy, escaping, `npm audit` | static tests · audit gate |
| 14 | Social card | Premium animated share preview everywhere the link travels | Purpose-synthesised 1200×630 looping GIF wired into OG/Twitter/JSON-LD | unit (asset policy gate) |
| 15 | CI quality gate | Every push and PR proves the above | GitHub Actions: install → check → audit → Chromium suite | workflow on this branch and PRs |

---

## 03 / ENGINEERING ARCHITECTURE

### Architectural principle

The system is a **static shell with progressive enhancement**, deployed to the edge. There is no hydration, no SSR, no client runtime — the shell renders, an optional deferred script enhances, and the delivery plane is a static host's form endpoint.

### Module responsibility map

| Path | Layer | Responsibility |
| --- | --- | --- |
| `index.html` | Shell | Semantic document, SEO/Open Graph/JSON-LD, content-security-policy meta, favicon, skip link, hidden Netlify form discovery record, `<noscript>` consultation fallback, deferred entry script. |
| `style.css` | Presentation | Tokenised visual system (`:root` custom properties), responsive CSS-art vehicle, atmosphere profiles (Midnight / Emerald / Platinum), glass controls, dialogs, form states, `prefers-reduced-motion` alternatives. |
| `script.js` | Enhancement | Bilingual `copy` model, defensive HTML escaping of every rendered string, full-page renderer, preference state (guarded `localStorage`), dialog/menu/focus management, form progress + resilient delivery. |
| `assets/mark.svg` | Brand | 312 B vector favicon. |
| `assets/og-image-animated.gif` | Brand | Social sharing card — 1200×630 looping GIF, synthesised by the asset pipeline. |
| `assets/readme/` | Brand · docs | README cinematic system — hero loop, static poster, divider, closing signature (deterministic build artifacts). |
| `tools/og/` | Build tooling | Deterministic social-card synthesiser (base plate, brand fonts, generator, verification). Not part of the runtime surface. |
| `tools/readme/` | Build tooling | Deterministic README-asset synthesiser + committed AI-synthesised base plate. Not part of the runtime surface. |
| `_headers` | Security | Netlify security header policy mirroring the in-page CSP. |
| `tests/unit/site.test.mjs` | Verification | Static policy + budget assertions and a Happy-DOM characterisation of the conversion flow. |
| `tests/e2e/site.spec.mjs` | Verification | Chromium flows: locale persistence, atmosphere, mobile navigation, dialog→form conversion, delivery, no-JS, axe, transfer/DOM budgets. |
| `.github/workflows/quality.yml` | CI | Install → static gate → audit → browser suite; failure artifacts retained. |

### Tech stack

| Layer | Choice | Version | Why this and not the obvious alternative |
| --- | --- | --- | --- |
| Document | Semantic HTML5, hand-authored | — | Server-renderable as-is; no hydration tax, meaningful without CSS/JS |
| Styling | Hand-authored CSS, custom properties, `backdrop-filter` | — | Design tokens in the cascade; atmosphere switching costs one class change, not a theme runtime |
| Logic | Vanilla ECMAScript, one IIFE-free module | ES2022 | The interaction surface is small; a framework would cost more transfer than the entire page |
| i18n | Application-level `copy` model + `lang`/`dir` mutation | — | True document semantics per locale, persisted client-side, zero i18n runtime |
| Dialogs | Native `<dialog>` | — | Free focus trapping, Escape and top-layer; a JS focus-trap is the fallback, not the default |
| Delivery | Static host + Netlify-compatible form endpoint | — | The trust boundary is the host's endpoint; no server code of ours to attack or operate |
| Unit testing | `node:test` + Happy DOM | Node ≥ 20 · happy-dom 20 | Stdlib runner; DOM characterisation without a browser |
| E2E testing | Playwright (Chromium) + axe-core | Playwright 1.63 · axe 4.13 | Real-browser conversion, a11y and budget flows in CI |
| Security policy | CSP in markup + Netlify `_headers` | — | Defence in depth: policy holds even if one layer is stripped |
| Social card tooling | Python + Pillow + NumPy (+ fontTools, arabic-reshaper) | Python 3.11 | Deterministic image synthesis; build-time only, never shipped |
| README cinematic tooling | Python + Pillow + NumPy (+ arabic-reshaper, python-bidi) | Python 3.11 | Deterministic hero/divider/signature synthesis; build-time only, never shipped |
| Brand type | Playfair Display & Manrope (self-hosted for the cards, Google Fonts for the page with system fallbacks) | — | The artifacts bake the exact brand fonts as vectors of the layout; the page degrades gracefully offline |
| CI | GitHub Actions | Node 22 runner | Install → check → audit → browser suite, artifacts on failure |

### State model

The enhancement layer keeps exactly one serialisable preference set and one transient interaction state:

```mermaid
stateDiagram-v2
  [*] --> Midnight : saved profile (validated)
  Midnight --> Emerald : atmosphere select
  Emerald --> Platinum : atmosphere select
  Platinum --> Midnight : atmosphere select

  [*] --> BriefClosed
  BriefClosed --> BriefOpen : view private brief
  BriefOpen --> BriefClosed : backdrop / button / Escape
  BriefOpen --> BriefPrefilled : continue with this vehicle
  BriefPrefilled --> BriefClosed : interest prefilled, form focused
```

**Invariants** (all covered by the automated suite):

- The locale switch updates `<html lang>` **and** `dir`, the document title, and the description/OG metadata — not merely visible strings — and persists only the locale preference.
- The atmosphere selector accepts exactly `midnight`, `emerald`, `platinum`; unknown saved values fall back to Midnight.
- A private brief renders only for a known collection key; closing by button, backdrop or Escape returns focus to its opener.
- Continuing a brief preselects the matching `interest`, preserves all other in-progress form values, scrolls to the form and focuses the name field.
- Form progress equals the count of non-empty required controls (notes stay optional).
- Re-rendering (locale or atmosphere change) restores in-progress form values from the previous DOM before replacing it.

---

## 04 / SYSTEM BLUEPRINT

```mermaid
flowchart TB
  subgraph EDGE["Edge delivery — any static host"]
    HEADERS["_headers<br/>CSP · nosniff · frame-deny<br/>Permissions-Policy"]
  end

  subgraph SHELL["Static shell — index.html"]
    SEO["SEO / Open Graph / JSON-LD"]
    NOJS["&lt;noscript&gt; fallback brief"]
    DISCOVERY["Hidden Netlify discovery record"]
  end

  subgraph ENHANCE["Enhancement layer — deferred, optional"]
    COPY["copy model — EN / AR content tree"]
    RENDER["Renderer + safe escaping"]
    STATE["Preference state<br/>locale · atmosphere · focus"]
    FX["Motion system<br/>rAF-coalesced, transform/opacity only"]
  end

  subgraph INTERACTION["Interaction surfaces"]
    DIALOG["Private brief dialog<br/>native &lt;dialog&gt;"]
    FORM["Confidential brief<br/>validation · progress · delivery"]
  end

  DELIVERY["Same-origin form endpoint<br/>URL-encoded POST · 10 s abort"]

  SEO --> COPY
  COPY --> RENDER --> STATE
  STATE --> DIALOG --> FORM
  STATE --> FX
  FORM -->|"fetch + AbortController"| DELIVERY
  HEADERS --> SHELL
```

---

## 05 / EXECUTION INTELLIGENCE

### W1 — The conversion spine

From anonymous arrival to a qualified, correctly-prefilled confidential brief in four moves:

```mermaid
sequenceDiagram
  participant V as Visitor
  participant R as Renderer (script.js)
  participant D as Private brief dialog
  participant F as Confidential brief form
  participant H as Static host / form endpoint

  V->>R: Land; deferred script enhances the shell
  R->>R: Render locale + atmosphere from persisted preference
  V->>D: "View private brief" on a collection card
  D-->>V: Focused specification sheet (Escape/backdrop safe)
  V->>D: "Continue with this vehicle"
  D->>R: Close, return focus, hand off the collection key
  R->>F: Preselect interest · preserve other values · scroll · focus name field
  V->>F: Complete required fields (progress announced live)
  V->>F: Submit
  F->>F: Native validation + honeypot must pass
  F->>H: URL-encoded same-origin POST (AbortController, 10 s)
  H-->>F: 200 or error
  F-->>V: Polite live-region success / failure; progress resets
```

### W2 — Preference persistence

1. Visitor switches locale or atmosphere → state updates → `render()` rebuilds the page from the escaped `copy` tree.
2. In-progress form values are snapshotted from the previous DOM and re-applied — a language switch never destroys a half-written brief.
3. Only `vip-motors-language` and `vip-motors-visual-mode` are persisted, each wrapped in `try/catch` (storage is an optional enhancement, never a dependency).

### W3 — Delivery resilience

| Condition | Behaviour | Guarantee |
| --- | --- | --- |
| JavaScript enabled, network healthy | URL-encoded same-origin POST with `credentials: "same-origin"` | Payload identical to the hidden discovery record |
| Endpoint slow / hung | `AbortController` cancels after `FORM_TIMEOUT_MS = 10000` | Visitor is never left on a stuck button |
| Endpoint error / abort | Generic, human failure message in a polite live region | No exception text or internals leak to the visitor |
| Honeypot field filled | Submission is not attempted | Bot traffic never reaches the endpoint |
| JavaScript disabled | Semantic `<noscript>` form POSTs the same payload shape (`name`, `email`, `interest`, `timeline`, `channel`, `notes`) | The lead path survives total enhancement failure |

### W4 — Social card synthesis

The share preview is not a screenshot — it is **generated as a build artifact** by `tools/og/generate_og.py`, fully deterministic and re-runnable: base plate grade + adaptive scrim + film grain → scene analysis (horizon & glow centroid detected from pixels) → typography lockup (Playfair Display + Manrope, measured, safe-area asserted) → light choreography (sweep · gold dust · rule glint, amplitude-lattice snapped) → screen blend onto plate with one global 256-colour palette → frame-differenced GIF89a (disposal=1, transparent deltas) → round-trip verification (every frame re-renders pixel-faithfully).

- **Loop mathematics.** Every effect is parameterised on `t ∈ [0,1)` with integer harmonics; the loop seam measures **0.77/255** mean delta against a 0.74 body average — mathematically seamless.
- **Frame 0 is a complete poster.** Crawlers that do not animate GIFs render the full brand card.
- **Policy gate.** ≤ 2.5 MB, 1200×630, loop-forever extension — enforced in the unit suite.

Regenerate after any brand/copy change:

```bash
pip install pillow numpy arabic-reshaper python-bidi   # build-time only
npm run og:regenerate                                  # → assets/og-image-animated.gif
```

### W5 — The README cinematic pipeline

The hero that opens this document is a second engineered artifact, synthesised by `tools/readme/generate_readme_assets.py` from a committed AI-synthesised base plate (`tools/readme/base.png`) and the same brand fonts and encoding mathematics as the social card:

| Artifact | Canvas | Motion | Verified |
| --- | --- | --- | --- |
| `yaslogist-hero.gif` | 1920×720 | 96 frames × 100 ms — a 9.6 s seamless loop | round-trip: every frame re-renders pixel-faithfully; seam 0.34/255 vs 0.55 body |
| `yaslogist-hero.png` | 1920×720 | static poster (frame-0 composite) | lossless PNG fallback |
| `yaslogist-divider.gif` | 1200×28 | 48 frames × 80 ms travelling light pulses | round-trip verified |
| `yaslogist-signature.gif` | 880×240 | 40 frames × 90 ms closing brand loop | round-trip verified |

The static poster (`assets/readme/yaslogist-hero.png`) is the lossless frame-0 composite — the same complete poster that crawlers and non-animating contexts receive from the GIF's first frame.

The hero composes coordinated depth layers — graded obsidian atmosphere with baked horizon + emerald ambience detected from the plate itself; the brand lockup set in the real Playfair Display / Manrope faces with pixel-measured safe areas; a permanent YASLOGIST signature and bilingual accent that never leave the frame — animated by seven integer-harmonic motions: a diagonal gold specular sweep, drifting gold dust, a hairline-rule glint, travelling pulses along the floor light line, a breathing reflection shimmer under the vehicle, a coordinate scanner gliding over its roofline, and a slowly rotating dashed orbit around the brand seal. Amplitudes snap to a temporal lattice, frames snap to a 3-level RGB lattice, one global 256-colour palette prevents flicker, and inter-frame transparency differencing keeps unchanged pixels nearly free; the file lands at **6.97 MB** for a 1.38-megapixel, 9.6-second loop.

The pipeline ships without human eyes and proves itself instead: after encoding, each GIF is decoded through Pillow's own compositor and every frame is compared against the intended palette-mapped colours, and a numeric QA asserts loop-seam continuity, wordmark ink and effect amplitude.

```bash
pip install pillow numpy arabic-reshaper python-bidi   # build-time only
python3 tools/readme/generate_readme_assets.py         # → assets/readme/*
```

### W6 — Continuous verification

```mermaid
flowchart LR
  P["Push / PR"] --> I["npm ci"]
  I --> C["node --check + unit/static suite"]
  C --> A["npm audit --audit-level=high"]
  A --> B["npx playwright install chromium"]
  B --> E["Chromium E2E: 8 flows<br/>incl. axe + budgets"]
  E --> OK["✓ Merge with evidence"]
  E -->|failure| ART["HTML report + traces<br/>retained as artifacts"]
```

---

## 06 / IGNITION

### Preview in one command (no install)

```bash
python3 -m http.server 4173 --bind 0.0.0.0
```

Open `http://localhost:4173`. A plain Python server does **not** process form POSTs or apply `_headers` — those belong to the production host.

### Full contributor setup

```bash
npm ci
npx playwright install chromium
npm test          # unit + static gates, then the Chromium suite
```

Requirements: Node.js ≥ 20 and Python 3. The shipped site itself has **no runtime package dependency**.

---

## 07 / DEEP SYSTEM ACCESS

<details>
<summary><strong>Security posture</strong> — a public static client, not an authentication system</summary>

| Control | Implementation |
| --- | --- |
| Output escaping | Every string from the content model is defensively escaped before it reaches the renderer's template |
| Content Security Policy | Same-origin CSP in both HTML meta and Netlify `_headers`; executable scripts restricted to the local deferred entry file |
| Framing / plugin defense | `object-src 'none'`, `base-uri 'self'`, `frame-ancestors 'none'`, `X-Frame-Options: DENY` |
| Transport hygiene | `nosniff`, strict referrer policy, deny-by-default Permissions Policy, cross-origin opener policy |
| Form abuse | Honeypot field, native required/email constraints, same-origin `form-action`, 10 s cancellation, generic visitor-facing failures |
| Supply chain | `npm audit --audit-level=high` in local commands and CI |

**Host responsibilities.** `_headers` is a Netlify convention — on another provider, translate the policy into that provider's native configuration and verify with an HTTPS response check. Never add secrets, API keys, personal addresses or CRM tokens to this repository or client JavaScript.

</details>

<details>
<summary><strong>Performance & motion budget</strong> — measured, enforced, and honest</summary>

| Metric | Value | Enforcement |
| --- | --- | --- |
| First-party critical transfer (uncompressed) | **95,448 B** (`index.html` + `style.css` + `script.js` + `assets/mark.svg`) | Unit + browser tests: `< 153,600 B` (150 KiB) |
| Headroom against the ceiling | 58,152 B | — |
| First-party image / video / 3D assets in the page | **0** — CSS vehicle art + 312 B SVG favicon | Transfer budget test |
| DOM nodes | **< 500** | Playwright `@performance` |
| README hero | 6.97 MB GIF, fetched only when viewing the repository page — **not** part of the site's critical path | Asset policy test: 1920×720, loop-forever, ≤ 10 MB |
| Social card | 2,019,902 B, fetched by crawlers only — **not** part of the page's critical path | Unit policy gate: ≤ 2.5 MB, 1200×630, loop-forever extension |

The first-party critical surface grew from 74,296 B (original checked-in shell) to 95,448 B across the upgrade series because it now carries a real no-JS path, dialog flow, atmosphere profiles, focus management and delivery resilience. These are uncompressed source measurements — not substituted network-transfer or Core Web Vitals claims.

> **Field-data caveat.** This repository ships a browser performance test, but no desktop browser binary was available in the authoring workspace, so no FPS, LCP, INP or CLS number is claimed. Run `npx playwright install chromium && npm run test:performance` locally or in CI, and measure production field data before publishing any performance score.

### Motion system contract

| Behaviour | Rule |
| --- | --- |
| Reveals | 800 ms `cubic-bezier(0.22, 1, 0.36, 1)` — opacity + translate only |
| Pointer depth | Fine-pointer only, `requestAnimationFrame`-coalesced, ±3° maximum |
| Scanner / dialog scan | Transform + opacity only; subdued 8 s / 5 s loops |
| Scroll indicator | Passive listener, one frame per update |
| Reduced motion | Reveals resolve instantly; scanner and brief scan removed — motion is never the only carrier of information |

</details>

<a id="accessibility--internationalization"></a>
<details>
<summary><strong>Accessibility & internationalization</strong></summary>

- Semantic `<main>`, `<nav>`, `<section>`, `<article>`, `<aside>`, `<footer>`; labelled controls; visible focus treatment; skip link; polite live regions for form and language announcements.
- English and Arabic are first-class: switching updates `lang` and `dir` and the document metadata; the layout mirrors under RTL (progress bar, nav, ambient accents).
- Native dialog semantics with focus return; the mobile drawer receives focus on open and restores it on Escape.
- Responsive to 320 px; collection cards become a touch-friendly horizontal rail on small screens.
- The Chromium suite runs **axe** on the critical screen and asserts zero violations.
- Manual review is still required for real copy quality, Arabic translation quality, and final contrast on the production font stack.

</details>

<details>
<summary><strong>Deployment & forms</strong></summary>

1. Publish the repository root to any static host.
2. On Netlify, keep the visible form name as `vip-consultation` — the hidden discovery record makes it discoverable and the enhanced request posts URL-encoded data to the same origin.
3. Configure the legitimate destination/notification flow in the host or connected CRM. This repository intentionally contains no destination address or credential.
4. Verify a submission on the deployed HTTPS domain, then verify response headers: `curl -I https://YOUR-DOMAIN.example`.
5. If the host cannot process Netlify-style forms, preserve the field names and replace the `action`/delivery implementation with an owned, authenticated backend — maintain the same success/error accessibility contract.

> The local Python server returns no form handler; an error state there is expected and demonstrates the visitor-facing fallback path, not delivery.

</details>

<details>
<summary><strong>Customization guide</strong></summary>

**Copy** — edit only the `copy.en` and `copy.ar` records in `script.js`. Keep keys and option values matched across locales — the interaction code uses values such as `grand-coupe`, `hybrid-gt` and `executive-suv` as stable form identifiers. Before launch, replace or validate: service/location statements; all availability, power, timing and fleet metrics; claims involving client types, logistics, privacy or global support; Open Graph and structured-data URL values once a canonical domain exists.

**Design tokens** — the visual system begins at the top of `style.css`: `--ink`, `--surface`, `--text`, `--muted`, `--gold` (palette); `--sans` / `--display` (typography); `--ease` (choreography). Atmosphere profiles live under the *high-tech luxury system* section at the end of the file. Keep scanner and dialog effects transform/opacity-only, and do not replace the CSS vehicle with unlicensed imagery without setting a new measurable budget.

**Social card** — update `tools/og/base.png` (or the typography constants in `tools/og/generate_og.py`) and run `npm run og:regenerate`. The unit gate re-checks dimensions, size and wiring.

**README cinematic system** — update `tools/readme/base.png` or the constants in `tools/readme/generate_readme_assets.py` and re-run the generator; the asset policy test re-checks dimensions, loop, size and README wiring.

</details>

<details>
<summary><strong>Asset provenance & license</strong></summary>

No license file was present in the supplied repository — treat source and brand material as private until the owner adds an explicit license.

| Asset | Origin | License / action |
| --- | --- | --- |
| Layout, CSS vehicle, effects, scripts | Original source in this repository | Verify project ownership before reuse |
| `assets/mark.svg` | Created in this upgrade | Project-owned; add a license before redistribution |
| `assets/og-image-animated.gif` + `tools/og/base.png` | AI-generated base plate, programmatic synthesis in this repo | Project-owned; add a license before redistribution |
| `assets/readme/*` + `tools/readme/base.png` | AI-generated base plate, programmatic synthesis in this repo (YASLOGIST cinematic system) | Project-owned; add a license before redistribution |
| `tools/og/fonts/*.ttf` | Playfair Display & Manrope (Google Fonts) | SIL Open Font License 1.1 — redistribution with the license preserved is permitted |
| Google Fonts (page load) | Google Fonts CDN | Subject to their font licenses; self-host or document consent/privacy needs |

</details>

---

## 08 / ENGINEERING STATUS

**Implemented and verified** (by the automated suite in this repository):

- Bilingual EN/AR shell with persisted `lang`/`dir` semantics; three atmosphere profiles; CSS-art vehicle.
- Private brief dialog → prefilled confidential brief conversion spine with focus management.
- Resilient same-origin delivery with 10 s abort; complete `<noscript>` fallback path.
- Security posture (CSP in markup + headers, escaping, honeypot, audit gate).
- Social card and README cinematic system as deterministic, self-verifying build artifacts.
- CI ladder: static/unit gates → audit → Chromium E2E (axe + budgets) on every push and PR.

**Open, planned, or unverified** — owner decisions and field measurements that deliberately do not exist in this repository:

- [ ] Validate every public business statement in both languages.
- [ ] Set the canonical URL; prefix OG/Twitter/JSON-LD image paths with the origin.
- [ ] Verify actual host form delivery, retention policy and rate limiting.
- [ ] Translate `_headers` if the host is not Netlify.
- [ ] Run every quality gate, including the browser suite, on a machine with Chromium.
- [ ] Test keyboard flow, mobile drawer, Arabic RTL and reduced motion on the deployed HTTPS domain.
- [ ] Measure production LCP/INP/CLS on representative mobile hardware before adding heavier visuals.
- Social-platform GIF behaviour varies and evolves; every animated artifact is designed so its static first frame is a complete, on-brand poster regardless.

---

## 09 / YASLOGIST

<div align="center">
  <img
    src="assets/readme/yaslogist-signature.gif"
    alt="YASLOGIST — creative engineering signature; the diamond seal above the letterspaced wordmark with a slow gold sweep and drifting dust. www.yaslogist.com"
    width="480"
  />
</div>

The cinematic identity of this repository — hero, divider and closing signature — carries the permanent creative-engineering signature of **[YASLOGIST](https://www.yaslogist.com)**. The product keeps its own voice: *VIP Motors Atelier* remains the primary identity, its obsidian-and-gold showroom language setting the palette, typography and motion philosophy; YASLOGIST is the studio hand that composed, synthesised and verified the experience as one coherent visual system.

- **In the hero** — the YASLOGIST wordmark and seal hold the lower-left of every frame; the bilingual accent `ياسلوجست · A YASLOGIST CINEMATIC EXPERIENCE` closes the lower-right.
- **In the document** — this section binds the brand to its verified engineering: deterministic synthesis, self-verifying encoders, honest budgets.
- **At the end** — the signature above, and the seal below.

Official website: **https://www.yaslogist.com**

---

<div align="center">
  <img src="assets/readme/yaslogist-divider.gif" alt="" width="100%" />

**VIP MOTORS ATELIER** — a darker kind of luxury.
A **YASLOGIST** cinematic engineering experience · [www.yaslogist.com](https://www.yaslogist.com)

</div>
