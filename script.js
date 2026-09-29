/* VIP Motors Atelier — dependency-free presentation layer.
 * The page is server-renderable as plain HTML, then enhanced with language switching,
 * motion, form delivery, and small interaction affordances. No runtime framework or
 * build step is required for the static edge deployment.
 */

const copy = {
  en: {
    langName: "English",
    alternateLang: "العربية",
    brandNote: "By appointment only",
    nav: { home: "Home", collection: "Collection", concierge: "Concierge", contact: "Contact" },
    menu: "Menu",
    close: "Close menu",
    hero: {
      eyebrow: "Private showroom · Dubai / London",
      badgeAlt: "Arabic + English concierge",
      title: "A darker kind of luxury.",
      description: "VIP Motors curates grand tourers, executive SUVs, and discreet off-market acquisitions with white-glove sourcing, protected logistics, and after-delivery concierge.",
      primary: "Reserve a private viewing",
      secondary: "Explore the collection",
      trust: "Trusted by collectors, founders, and family offices",
      visualKicker: "Featured allocation",
      visualTitle: "Midnight Sovereign",
      visualMeta: "V12 Grand Coupe · 715 hp",
      visualNote: "A study in quiet authority",
      visualCta: "Request specification",
      stats: [
        ["87", "annual arrivals"],
        ["24/7", "acquisition desk"],
        ["11", "private suites"],
      ],
      tags: ["Invite-only sourcing", "Worldwide enclosed delivery", "Collectors & family offices"],
    },
    collection: {
      eyebrow: "Private collection",
      title: "Inventory selected for presence, not volume.",
      description: "Every arrival is chosen for silhouette, provenance, and cabin finish. The result feels edited like a gallery rather than stacked like a lot.",
      viewLabel: "View private brief",
      cards: [
        {
          key: "grand-coupe",
          index: "01",
          series: "V12 Grand Coupe",
          name: "Midnight Sovereign",
          description: "Low-mileage flagship with obsidian paint, hand-finished walnut, and rear lounge specification.",
          specs: ["715 hp", "48-hour preview"],
          chips: ["Obsidian black", "Bespoke trim", "Rear suite"],
          note: "Featured allocation",
        },
        {
          key: "hybrid-gt",
          index: "02",
          series: "Hybrid GT",
          name: "Emerald Voltage",
          description: "Long-distance performance commission pairing silent city mode with a dramatic grand touring profile.",
          specs: ["812 hp", "Factory commission"],
          chips: ["Satin green", "Carbon package", "Private spec"],
          note: "Build slot open",
        },
        {
          key: "executive-suv",
          index: "03",
          series: "Executive SUV",
          name: "Obsidian Atlas",
          description: "Family-office transport tuned for chauffeur comfort, secure travel, and custom cabin privacy.",
          specs: ["850 Nm", "Immediate handover"],
          chips: ["Quiet cabin", "Privacy glass", "Long-wheelbase"],
          note: "Ready now",
        },
      ],
    },
    concierge: {
      eyebrow: "Ownership concierge",
      title: "The dealership disappears. The service remains.",
      description: "A single bilingual team handles acquisition, valuation, logistics, and post-delivery details so ownership feels calm from first inquiry to final handover.",
      cards: [
        ["01", "Private acquisition desk", "We source from collectors, embassies, and closed dealer networks before vehicles reach public inventory feeds."],
        ["02", "Signature trade-ins", "Inspection, valuation, and exchange are structured discreetly for executives, founders, and family offices."],
        ["03", "Travel and delivery", "Airport pickup, enclosed shipping, secure transfer, and document handling are coordinated end to end."],
      ],
      loungeTitle: "Members lounge",
      quote: "We do not compete on volume. We curate time, certainty, and access.",
      points: ["Arabic and English advisors in one thread", "Digital signing for remote approvals", "Presentation-grade detailing before handover"],
    },
    contact: {
      eyebrow: "Reserve a viewing",
      title: "Start with a confidential brief.",
      description: "Tell us what you drive now, what you want next, and how soon you want the first keys on the table.",
      name: "Full name",
      email: "Email address",
      interest: "Vehicle interest",
      timeline: "Purchase timing",
      notes: "What should we source for you?",
      namePlaceholder: "Your name",
      emailPlaceholder: "name@example.com",
      notesPlaceholder: "Preferred body style, budget range, or delivery city.",
      interestOptions: [["grand-coupe", "Grand coupe"], ["executive-suv", "Executive SUV"], ["hybrid-gt", "Hybrid GT"], ["bespoke", "Bespoke sourcing"]],
      timelineOptions: [["30-days", "Within 30 days"], ["quarter", "This quarter"], ["exploring", "Exploring options"]],
      submit: "Request concierge call",
      submitting: "Sending brief…",
      success: "Your brief is with the concierge desk. We will be in touch shortly.",
      error: "The brief could not be sent. Please try again or contact the desk directly.",
      sidebarTitle: "Client protocol",
      sidebarTitleAlt: "Private by design",
      sidebarBody: "Every inquiry is handled as a private brief, then routed to one advisor who stays with the purchase through delivery.",
      bullets: ["Appointment-only showroom access", "Worldwide enclosed delivery", "Arabic and English buyer support"],
    },
    footer: { line: "Reserved for the few.", subline: "VIP Motors Atelier · Private automotive concierge" },
    floating: "Book appointment",
    sectionLabels: { discover: "Discover the edit", process: "How we move", protocol: "Your private protocol" },
  },
  ar: {
    langName: "العربية",
    alternateLang: "English",
    brandNote: "بالموعد فقط",
    nav: { home: "الرئيسية", collection: "المجموعة", concierge: "الخدمات", contact: "التواصل" },
    menu: "القائمة",
    close: "إغلاق القائمة",
    hero: {
      eyebrow: "صالة خاصة · دبي / لندن",
      badgeAlt: "خدمة بالعربية والإنجليزية",
      title: "فخامة داكنة بطابع مختلف.",
      description: "تنسق VIP Motors سيارات الجراند تورر وSUV التنفيذية والفرص الحصرية خارج السوق مع توريد راق ولوجستيات مؤمنة ومرافقة بعد التسليم.",
      primary: "احجز معاينة خاصة",
      secondary: "استعرض المجموعة",
      trust: "يثق بنا الجامعون والمؤسسون والمكاتب العائلية",
      visualKicker: "حصة مميزة",
      visualTitle: "Midnight Sovereign",
      visualMeta: "كوبيه جراند V12 · 715 حصان",
      visualNote: "دراسة في الحضور الهادئ",
      visualCta: "اطلب المواصفات",
      stats: [["87", "وصول سنوي"], ["24/7", "مكتب التوريد"], ["11", "أجنحة خاصة"]],
      tags: ["توريد حصري", "تسليم مغلق حول العالم", "للجامعين والمكاتب العائلية"],
    },
    collection: {
      eyebrow: "المجموعة الخاصة",
      title: "مخزون مختار للحضور لا للكثرة.",
      description: "كل سيارة يتم اختيارها بسبب الخط الخارجي والسجل والمقصورة، ليبدو المعرض كأنه مساحة منسقة لا ساحة ممتلئة.",
      viewLabel: "اطلب الملف الخاص",
      cards: [
        { key: "grand-coupe", index: "01", series: "كوبيه جراند V12", name: "Midnight Sovereign", description: "فئة رئيسية قليلة الاستخدام بطلاء أوبسيديان وخشب جوز يدوي وتجهيز صالة خلفية.", specs: ["715 حصان", "معاينة خلال 48 ساعة"], chips: ["أسود أوبسيديان", "تفصيل خاص", "جناح خلفي"], note: "حصة مميزة" },
        { key: "hybrid-gt", index: "02", series: "Hybrid GT", name: "Emerald Voltage", description: "نسخة أداء للمسافات الطويلة تجمع هدوء المدينة مع حضور حاد لسيارة جراند تورر.", specs: ["812 حصان", "طلب مصنع خاص"], chips: ["أخضر ساتان", "حزمة كربون", "مواصفات خاصة"], note: "فتحة تصنيع متاحة" },
        { key: "executive-suv", index: "03", series: "SUV تنفيذية", name: "Obsidian Atlas", description: "سيارة تنقل تنفيذية معدلة لراحة السائق والركاب والخصوصية الكاملة أثناء السفر.", specs: ["850 نيوتن متر", "تسليم فوري"], chips: ["مقصورة هادئة", "زجاج خصوصية", "قاعدة عجلات طويلة"], note: "جاهزة الآن" },
      ],
    },
    concierge: {
      eyebrow: "خدمات التملك",
      title: "المعرض يختفي، والخدمة تبقى.",
      description: "فريق ثنائي اللغة يدير الشراء والتقييم واللوجستيات وما بعد التسليم لكي تبدو التجربة هادئة من أول رسالة حتى الاستلام النهائي.",
      cards: [["01", "مكتب اقتناء خاص", "نحصل على السيارات من جامعين وسفارات وشبكات وكلاء مغلقة قبل ظهورها في القوائم العامة."], ["02", "استبدال بتوقيع خاص", "الفحص والتقييم والاستبدال يتم تنظيمها بسرية للمؤسسين والتنفيذيين والمكاتب العائلية."], ["03", "السفر والتسليم", "استقبال المطار والشحن المغلق والنقل المؤمن وإنهاء المستندات يتم تنسيقه كاملا من طرف واحد."]],
      loungeTitle: "صالة الأعضاء",
      quote: "نحن لا ننافس بالكثرة، بل ننظم الوقت واليقين والوصول.",
      points: ["مستشارون بالعربية والإنجليزية ضمن مسار واحد", "توقيع رقمي للاعتمادات عن بعد", "تجهيز تفصيلي نهائي قبل التسليم"],
    },
    contact: {
      eyebrow: "احجز معاينة",
      title: "ابدأ بطلب سري ومختصر.",
      description: "أخبرنا بما تقوده الآن وما تبحث عنه لاحقا ومتى تريد أن تصل المفاتيح الأولى إلى الطاولة.",
      name: "الاسم الكامل", email: "البريد الإلكتروني", interest: "نوع السيارة", timeline: "توقيت الشراء", notes: "ماذا تريد منا أن نوفر لك؟",
      namePlaceholder: "اسمك", emailPlaceholder: "name@example.com", notesPlaceholder: "نوع الهيكل أو الميزانية أو مدينة التسليم.",
      interestOptions: [["grand-coupe", "كوبيه فاخرة"], ["executive-suv", "SUV تنفيذية"], ["hybrid-gt", "Hybrid GT"], ["bespoke", "توريد حسب الطلب"]],
      timelineOptions: [["30-days", "خلال 30 يوما"], ["quarter", "خلال هذا الربع"], ["exploring", "أستكشف الخيارات"]],
      submit: "اطلب اتصالا من المستشار", submitting: "جار إرسال الطلب…", success: "وصل طلبك إلى مكتب المستشارين. سنتواصل معك قريبا.", error: "تعذر إرسال الطلب. حاول مجددا أو تواصل مع المكتب مباشرة.",
      sidebarTitle: "بروتوكول العميل", sidebarTitleAlt: "خصوصية مصممة", sidebarBody: "كل استفسار يعامل كطلب خاص ثم يوجه إلى مستشار واحد يرافق عملية الشراء حتى التسليم.", bullets: ["الوصول إلى المعرض بالمواعيد فقط", "تسليم مغلق حول العالم", "دعم شراء بالعربية والإنجليزية"],
    },
    footer: { line: "للقلة فقط.", subline: "VIP Motors Atelier · خدمة السيارات الخاصة" },
    floating: "احجز موعدا",
    sectionLabels: { discover: "اكتشف المجموعة", process: "كيف نتحرك", protocol: "بروتوكولك الخاص" },
  },
};

const state = {
  language: (() => {
    try {
      return localStorage.getItem("vip-motors-language") === "ar" ? "ar" : "en";
    } catch (error) {
      return "en";
    }
  })(),
  menuOpen: false,
};

const root = document.getElementById("app");
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
let revealObserver;
let activeNavObserver;
let scrollListener;

function iconArrow() {
  return `<svg class="arrow-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg>`;
}

function iconCheck() {
  return `<svg class="check-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 4.3 4.3L19 7" /></svg>`;
}

function sectionHeader(section, alternateSection, content) {
  return `<div class="section-heading reveal">
    <div class="eyebrow"><span>${section.eyebrow}</span><i></i><span class="eyebrow-alt">${alternateSection.eyebrow}</span></div>
    <h2>${content.title}</h2>
    <p>${content.description}</p>
  </div>`;
}

function render() {
  const currentForm = root.querySelector(".contact-form");
  const previousFormValues = currentForm ? Object.fromEntries(new FormData(currentForm)) : null;
  const content = copy[state.language];
  const alternate = copy[state.language === "en" ? "ar" : "en"];
  document.documentElement.lang = state.language;
  document.documentElement.dir = state.language === "ar" ? "rtl" : "ltr";
  document.title = state.language === "ar" ? "VIP Motors Atelier | صالة خاصة" : "VIP Motors Atelier | Private showroom";
  const metaDescription = document.querySelector('meta[name="description"]');
  const ogDescription = document.querySelector('meta[property="og:description"]');
  metaDescription?.setAttribute("content", content.hero.description);
  ogDescription?.setAttribute("content", content.hero.description);

  root.innerHTML = `<div class="site-shell">
    <div class="ambient ambient-one"></div><div class="ambient ambient-two"></div>
    <div class="scroll-progress" aria-hidden="true"><span></span></div>

    <header class="site-header" data-header>
      <div class="container nav-bar">
        <a class="brand" href="#home" aria-label="VIP Motors Atelier — ${content.nav.home}">
          <span class="brand-mark" aria-hidden="true"><span></span></span>
          <span class="brand-copy"><strong>VIP Motors <em>Atelier</em></strong><small>${content.brandNote}</small></span>
        </a>
        <nav class="desktop-nav" aria-label="Primary navigation">
          ${Object.entries(content.nav).map(([id, label]) => `<a href="#${id}" data-nav-link="${id}"><span>${label}</span><small>${alternate.nav[id]}</small></a>`).join("")}
        </nav>
        <div class="nav-actions">
          <div class="language-switcher" aria-label="Language">
            <button type="button" class="language-button ${state.language === "en" ? "is-active" : ""}" data-language="en" aria-pressed="${state.language === "en"}">EN</button>
            <button type="button" class="language-button ${state.language === "ar" ? "is-active" : ""}" data-language="ar" aria-pressed="${state.language === "ar"}">ع</button>
          </div>
          <a class="button button-small button-gold nav-cta" href="#contact">${content.floating}${iconArrow()}</a>
          <button class="menu-toggle" type="button" data-menu-toggle aria-expanded="${state.menuOpen}" aria-controls="mobile-menu" aria-label="${state.menuOpen ? content.close : content.menu}"><span></span><span></span><span></span></button>
        </div>
      </div>
      <div class="container mobile-menu ${state.menuOpen ? "is-open" : ""}" id="mobile-menu" data-mobile-menu aria-hidden="${!state.menuOpen}" ${state.menuOpen ? "" : "inert"}>
        <div class="mobile-menu-inner">
          <div class="mobile-menu-top"><span>${content.hero.eyebrow}</span><div class="language-switcher"><button type="button" class="language-button ${state.language === "en" ? "is-active" : ""}" data-language="en" aria-pressed="${state.language === "en"}">EN</button><button type="button" class="language-button ${state.language === "ar" ? "is-active" : ""}" data-language="ar" aria-pressed="${state.language === "ar"}">ع</button></div></div>
          <nav aria-label="Mobile navigation">${Object.entries(content.nav).map(([id, label]) => `<a href="#${id}" data-close-menu><span>${label}</span><small>${alternate.nav[id]}</small></a>`).join("")}</nav>
        </div>
      </div>
    </header>

    <main id="main-content">
      <section class="hero container" id="home" data-section="home">
        <div class="hero-copy reveal">
          <div class="eyebrow hero-eyebrow"><span class="eyebrow-dot"></span>${content.hero.eyebrow}</div>
          <h1>${content.hero.title}</h1>
          <p class="hero-description">${content.hero.description}</p>
          <div class="hero-actions"><a class="button button-gold" href="#contact">${content.hero.primary}${iconArrow()}</a><a class="button button-quiet" href="#collection">${content.hero.secondary}<span class="button-line"></span></a></div>
          <div class="trust-line"><span class="trust-avatars" aria-hidden="true"><i>V</i><i>M</i><i>+</i></span><span>${content.hero.trust}</span></div>
          <div class="stats-row">${content.hero.stats.map(([value, label], index) => `<div class="stat reveal reveal-delay-${index + 1}"><strong data-count="${value}">${value}</strong><span>${label}</span></div>`).join("")}</div>
        </div>
        <div class="hero-visual-wrap reveal reveal-delay-2">
          <div class="hero-visual spotlight" data-tilt>
            <div class="visual-grid" aria-hidden="true"></div><div class="visual-orbit orbit-one" aria-hidden="true"></div><div class="visual-orbit orbit-two" aria-hidden="true"></div>
            <div class="visual-header"><span><i class="status-dot"></i>${content.hero.visualKicker}</span><span>№ 001 / 003</span></div>
            <div class="car-stage" role="img" aria-label="${content.hero.visualTitle}, ${content.hero.visualMeta}">
              <div class="car-glow"></div><div class="car-shadow"></div>
              <div class="car-art"><div class="car-roof"></div><div class="car-window window-one"></div><div class="car-window window-two"></div><div class="car-body"></div><div class="car-highlight"></div><div class="car-wheel wheel-one"></div><div class="car-wheel wheel-two"></div><div class="car-light light-one"></div><div class="car-light light-two"></div></div>
            </div>
            <div class="visual-footer"><div><span class="visual-label">${content.hero.visualTitle}</span><strong>${content.hero.visualMeta}</strong><small>${content.hero.visualNote}</small></div><button type="button" class="icon-button" data-interest="grand-coupe" aria-label="${content.hero.visualCta}" title="${content.hero.visualCta}">${iconArrow()}</button></div>
          </div>
          <div class="hero-tags">${content.hero.tags.map((tag) => `<span>${tag}</span>`).join("")}</div>
        </div>
      </section>

      <section class="section container" id="collection" data-section="collection">
        ${sectionHeader(content.collection, alternate.collection, content.collection)}
        <div class="collection-grid">${content.collection.cards.map((car, index) => `<article class="collection-card card-tone-${index + 1} reveal reveal-delay-${(index % 3) + 1}" data-card="${car.key}">
          <div class="card-art"><span class="card-number">${car.index}</span><span class="art-line art-line-one"></span><span class="art-line art-line-two"></span><div class="mini-car"><i></i><b></b><em></em></div><span class="card-sheen"></span></div>
          <div class="card-content"><div class="card-series">${car.series}</div><h3>${car.name}</h3><p>${car.description}</p><div class="chip-row">${car.chips.map((chip) => `<span>${chip}</span>`).join("")}</div><div class="card-meta"><span>${car.specs[0]}</span><span>${car.specs[1]}</span></div><div class="card-divider"></div><div class="card-bottom"><span class="card-note">${car.note}</span><button type="button" class="text-button" data-interest="${car.key}">${content.collection.viewLabel}${iconArrow()}</button></div></div>
        </article>`).join("")}</div>
        <div class="section-caption reveal"><span>${content.sectionLabels.discover}</span><i></i><span>03 / 03</span></div>
      </section>

      <section class="section concierge-section" id="concierge" data-section="concierge">
        <div class="container">${sectionHeader(content.concierge, alternate.concierge, content.concierge)}
          <div class="concierge-layout"><div class="service-grid">${content.concierge.cards.map(([number, title, body], index) => `<article class="service-card reveal reveal-delay-${index + 1}"><span class="service-number">${number}</span><div class="service-icon" aria-hidden="true">${index === 0 ? "◌" : index === 1 ? "↗" : "⌁"}</div><h3>${title}</h3><p>${body}</p><span class="service-arrow">${iconArrow()}</span></article>`).join("")}</div>
            <aside class="lounge-card reveal spotlight"><div class="lounge-top"><span>${content.concierge.loungeTitle}</span><span class="lounge-mark">VM</span></div><blockquote>“${content.concierge.quote}”</blockquote><div class="card-divider"></div><ul>${content.concierge.points.map((point) => `<li>${iconCheck()}<span>${point}</span></li>`).join("")}</ul><div class="lounge-seal" aria-hidden="true">VIP<br><small>ATELIER</small></div></aside>
          </div>
        </div>
      </section>

      <section class="section contact-section container" id="contact" data-section="contact">
        ${sectionHeader(content.contact, alternate.contact, content.contact)}
        <div class="contact-layout"><form class="contact-form reveal" name="vip-consultation" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/" novalidate>
          <input type="hidden" name="form-name" value="vip-consultation" /><input type="text" name="bot-field" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true" />
          <div class="form-top"><span>${content.sectionLabels.protocol}</span><span>01 — 05</span></div>
          <div class="form-grid"><label><span>${content.contact.name}</span><input type="text" name="name" placeholder="${content.contact.namePlaceholder}" autocomplete="name" required /></label><label><span>${content.contact.email}</span><input type="email" name="email" placeholder="${content.contact.emailPlaceholder}" autocomplete="email" required /></label><label><span>${content.contact.interest}</span><select name="interest" required><option value="" disabled selected>${content.contact.interest}</option>${content.contact.interestOptions.map(([value, label]) => `<option value="${value}">${label}</option>`).join("")}</select></label><label><span>${content.contact.timeline}</span><select name="timeline" required><option value="" disabled selected>${content.contact.timeline}</option>${content.contact.timelineOptions.map(([value, label]) => `<option value="${value}">${label}</option>`).join("")}</select></label></div>
          <label class="notes-field"><span>${content.contact.notes}</span><textarea name="notes" placeholder="${content.contact.notesPlaceholder}" rows="4"></textarea></label>
          <div class="form-submit-row"><button class="button button-gold" type="submit">${content.contact.submit}${iconArrow()}</button><div class="form-status" role="status" aria-live="polite"></div></div>
        </form>
        <aside class="protocol-card reveal"><div class="protocol-glow"></div><div class="eyebrow"><span>${content.contact.sidebarTitle}</span><i></i><span class="eyebrow-alt">${content.contact.sidebarTitleAlt}</span></div><h3>${content.hero.badgeAlt || content.hero.eyebrow}</h3><p>${content.contact.sidebarBody}</p><div class="card-divider"></div><ul>${content.contact.bullets.map((bullet) => `<li>${iconCheck()}<span>${bullet}</span></li>`).join("")}</ul><div class="protocol-footer"><span>PRIVATE / 2026</span><span>⌁</span></div></aside></div>
      </section>
    </main>

    <footer class="site-footer container"><div class="footer-rule"></div><div class="footer-content"><div><div class="footer-title">${content.footer.line}</div><div class="footer-subtitle">${content.footer.subline}</div></div><div class="footer-right"><span>Dubai</span><i></i><span>London</span><i></i><span>Worldwide</span></div></div></footer>
    <a class="floating-cta" href="#contact">${content.floating}${iconArrow()}</a>
  </div>`;

  bindInteractions();
  if (previousFormValues) {
    Object.entries(previousFormValues).forEach(([name, value]) => {
      if (name === "form-name" || name === "bot-field") return;
      const field = root.querySelector(`.contact-form [name="${name}"]`);
      if (field) field.value = value;
    });
  }
}

function bindInteractions() {
  document.querySelectorAll("[data-language]").forEach((button) => button.addEventListener("click", () => {
    const next = button.dataset.language;
    if (next === state.language) return;
    state.language = next;
    state.menuOpen = false;
    try { localStorage.setItem("vip-motors-language", next); } catch (error) { /* storage is optional */ }
    render();
  }));

  const menuToggle = document.querySelector("[data-menu-toggle]");
  menuToggle?.addEventListener("click", () => { state.menuOpen = !state.menuOpen; render(); });
  document.querySelectorAll("[data-close-menu]").forEach((link) => link.addEventListener("click", () => { state.menuOpen = false; }));

  document.querySelectorAll("[data-interest]").forEach((button) => button.addEventListener("click", () => {
    const select = document.querySelector('select[name="interest"]');
    if (select) select.value = button.dataset.interest;
    document.getElementById("contact")?.scrollIntoView({ behavior: prefersReducedMotion.matches ? "auto" : "smooth", block: "start" });
    window.setTimeout(() => document.querySelector('input[name="name"]')?.focus(), prefersReducedMotion.matches ? 0 : 550);
  }));

  const form = document.querySelector(".contact-form");
  form?.addEventListener("submit", handleFormSubmit);
  setupRevealObserver();
  setupActiveNavigation();
  setupScrollProgress();
  setupTilt();
}

async function handleFormSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const status = form.querySelector(".form-status");
  const submit = form.querySelector('button[type="submit"]');
  const content = copy[state.language];
  if (form.elements["bot-field"]?.value) return;
  if (!form.checkValidity()) {
    form.classList.add("has-error");
    form.reportValidity();
    return;
  }
  form.classList.remove("has-error");
  submit.disabled = true;
  submit.setAttribute("aria-busy", "true");
  submit.childNodes[0].textContent = content.contact.submitting;
  status.textContent = "";
  try {
    const data = new URLSearchParams(new FormData(form));
    const response = await fetch(form.action || "/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: data.toString() });
    if (!response.ok) throw new Error("Form request failed");
    form.reset();
    status.className = "form-status is-success";
    status.textContent = content.contact.success;
  } catch (error) {
    status.className = "form-status is-error";
    status.textContent = content.contact.error;
  } finally {
    submit.disabled = false;
    submit.removeAttribute("aria-busy");
    submit.childNodes[0].textContent = content.contact.submit;
  }
}

function setupRevealObserver() {
  revealObserver?.disconnect();
  const elements = document.querySelectorAll(".reveal");
  if (prefersReducedMotion.matches || !("IntersectionObserver" in window)) {
    elements.forEach((element) => element.classList.add("is-visible"));
    return;
  }
  revealObserver = new IntersectionObserver((entries, instance) => {
    entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add("is-visible"); instance.unobserve(entry.target); } });
  }, { threshold: 0.12, rootMargin: "0px 0px -36px" });
  elements.forEach((element) => revealObserver.observe(element));
}

function setupActiveNavigation() {
  activeNavObserver?.disconnect();
  const links = document.querySelectorAll("[data-nav-link]");
  const sections = document.querySelectorAll("[data-section]");
  if (!("IntersectionObserver" in window)) return;
  activeNavObserver = new IntersectionObserver((entries) => entries.forEach((entry) => {
    if (entry.isIntersecting) links.forEach((link) => link.classList.toggle("is-current", link.dataset.navLink === entry.target.dataset.section));
  }), { threshold: 0, rootMargin: "-42% 0px -52%" });
  sections.forEach((section) => activeNavObserver.observe(section));
}

function setupScrollProgress() {
  const bar = document.querySelector(".scroll-progress span");
  if (!bar) return;
  if (scrollListener) window.removeEventListener("scroll", scrollListener);
  let ticking = false;
  const update = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = `scaleX(${max > 0 ? window.scrollY / max : 0})`;
    ticking = false;
  };
  scrollListener = () => { if (!ticking) { window.requestAnimationFrame(update); ticking = true; } };
  window.addEventListener("scroll", scrollListener, { passive: true });
  update();
}

function setupTilt() {
  const visual = document.querySelector("[data-tilt]");
  if (!visual || prefersReducedMotion.matches || !window.matchMedia("(pointer: fine)").matches) return;
  let frame;
  visual.addEventListener("pointermove", (event) => {
    const bounds = visual.getBoundingClientRect();
    const x = (event.clientX - bounds.left) / bounds.width - 0.5;
    const y = (event.clientY - bounds.top) / bounds.height - 0.5;
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => { visual.style.setProperty("--tilt-x", `${x * 3}deg`); visual.style.setProperty("--tilt-y", `${y * -3}deg`); visual.style.setProperty("--pointer-x", `${(x + 0.5) * 100}%`); visual.style.setProperty("--pointer-y", `${(y + 0.5) * 100}%`); });
  });
  visual.addEventListener("pointerleave", () => { visual.style.setProperty("--tilt-x", "0deg"); visual.style.setProperty("--tilt-y", "0deg"); });
}

prefersReducedMotion.addEventListener?.("change", () => render());
render();
