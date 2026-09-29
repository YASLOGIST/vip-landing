<div align="center">

# VIP Motors Atelier
### Private showroom interface — dependency-free at the edge.

**A cinematic, bilingual landing surface for a premium automotive concierge.**

</div>

---

## What this is

VIP Motors Atelier is a static, conversion-focused landing experience for private vehicle sourcing, curated inventory, and white-glove ownership services. It is designed to deploy directly to any static host or CDN without a build pipeline.

The implementation deliberately avoids a client framework, runtime UI dependency, and heavy 3D asset. The page still feels dimensional through a CSS-rendered hero vehicle, layered lighting, motion-safe reveal choreography, and pointer-aware visual depth.

## Architecture

```text
index.html       semantic shell, SEO metadata, JSON-LD, progressive form discovery
script.js        content model, bilingual renderer, interactions, form delivery
style.css        responsive design system, CSS vehicle art, motion and accessibility
```

### Runtime flow

1. The browser receives a small HTML shell and loads the stylesheet and one deferred script.
2. `script.js` renders the selected locale from the `copy` content model.
3. Intersection observers progressively reveal content and track the active section.
4. The contact form submits as a Netlify-compatible URL-encoded request with a honeypot field.
5. `prefers-reduced-motion`, keyboard focus, semantic labels, and inline form feedback are treated as first-class behavior.

## Product capabilities

- English / Arabic locale switching with `lang`, `dir`, and persisted preference.
- Responsive navigation with keyboard-accessible mobile drawer.
- Curated collection cards that deep-link a selected vehicle into the inquiry form.
- CSS-only hero vehicle and showroom art: no remote GLB, WebGL, or model runtime required.
- Scroll progress, active navigation state, reveal transitions, pointer tilt, and reduced-motion fallback.
- Netlify form discovery in the static HTML shell plus enhanced async submission in the visible form.
- SEO description, Open Graph metadata, semantic sections, skip link, live form status, and JSON-LD.

## Run locally

No install step is required:

```bash
python3 -m http.server 4173 --bind 0.0.0.0
```

Open `http://localhost:4173` in a browser. For a production deployment, publish the repository root to a static host with Netlify form handling enabled.

## Performance posture

- Zero framework hydration or runtime transpilation.
- One deferred application script; no Tailwind CDN, React CDN, Babel runtime, or model-viewer dependency.
- CSS art avoids large hero media and reserves layout dimensions to prevent cumulative shift.
- Motion is observer-driven, uses `requestAnimationFrame` for pointer and scroll work, and is disabled for reduced-motion users.
- External fonts are the only presentation dependency and have `preconnect` hints plus system fallbacks.

## Design principles

1. Cinema over decoration. Motion supports the story.
2. Performance is part of the visual system.
3. Private intent should feel answered before it is submitted.
4. Bilingual content is a product behavior, not a translation afterthought.
5. Every interactive control should remain understandable without motion.
