import assert from "node:assert/strict";
import { readFileSync, statSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "../..");
const read = (file) => readFileSync(resolve(root, file), "utf8");

test("security policy and host headers protect the static entry point", () => {
  const html = read("index.html");
  const headers = read("_headers");

  assert.match(html, /Content-Security-Policy/);
  assert.match(html, /script-src 'self'/);
  assert.match(headers, /frame-ancestors 'none'/);
  assert.match(headers, /X-Content-Type-Options: nosniff/);
  assert.match(headers, /Permissions-Policy:/);
  const executableInlineScripts = [...html.matchAll(/<script([^>]*)>/gi)].filter(([, attributes]) => !/\bsrc=/.test(attributes) && !/type=["']application\/ld\+json["']/.test(attributes));
  assert.equal(executableInlineScripts.length, 0);
  assert.doesNotMatch(html, /\son[a-z]+\s*=/i);
});

test("the static shell has a real no-JavaScript consultation path", () => {
  const html = read("index.html");
  assert.match(html, /<noscript>/);
  assert.match(html, /name="vip-consultation"/);
  assert.match(html, /name="channel"/);
  assert.match(html, /<main class="noscript-experience"/);
});

test("interactive source contains guarded content rendering and resilient delivery", () => {
  const source = read("script.js");
  assert.match(source, /function escapeHTML/);
  assert.match(source, /function escapeContent/);
  assert.match(source, /new AbortController\(\)/);
  assert.match(source, /FORM_TIMEOUT_MS = 10000/);
  assert.match(source, /credentials: "same-origin"/);
  assert.match(source, /data-brief-dialog/);
  assert.match(source, /data-form-progress/);
  assert.match(source, /prefers-reduced-motion/);
});

test("first-party critical assets stay inside the 150 KB transfer budget", () => {
  const assets = ["index.html", "style.css", "script.js", "assets/mark.svg"];
  const total = assets.reduce((sum, file) => sum + statSync(resolve(root, file)).size, 0);
  assert.ok(total < 150 * 1024, `critical first-party assets are ${total} bytes`);
});

test("the social card ships as a valid looping GIF and is wired into the shell", () => {
  const html = read("index.html");
  assert.match(html, /property="og:image" content="assets\/og-image-animated\.gif"/);
  assert.match(html, /name="twitter:card" content="summary_large_image"/);
  assert.match(html, /property="og:image:width" content="1200"/);

  const gif = readFileSync(resolve(root, "assets/og-image-animated.gif"));
  assert.equal(gif.subarray(0, 6).toString("latin1").startsWith("GIF"), true, "GIF signature missing");
  assert.equal(gif.readUInt16LE(6), 1200, "social card must be 1200 wide");
  assert.equal(gif.readUInt16LE(8), 630, "social card must be 630 tall");
  assert.ok(gif.length <= 2.5 * 1024 * 1024, `social card is ${gif.length} bytes (policy: 2.5 MB)`);
  assert.ok(gif.includes(Buffer.from("NETSCAPE2.0", "latin1")), "loop-forever extension missing");
});

async function createRuntime() {
  const { Window } = await import("happy-dom");
  const window = new Window({ url: "http://localhost:4173/" });
  window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
  window.IntersectionObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
  window.requestAnimationFrame = (callback) => { callback(); return 1; };
  window.cancelAnimationFrame = () => {};
  window.HTMLElement.prototype.scrollIntoView = () => {};
  window.fetch = async () => ({ ok: true, status: 200 });
  window.document.body.innerHTML = '<div id="app"></div>';
  window.eval(read("script.js"));
  return window;
}

test("runtime renders the bilingual brief, private-brief dialog, and form progress flow", async () => {
  const window = await createRuntime();
  const { document } = window;

  assert.equal(document.documentElement.lang, "en");
  assert.ok(document.querySelector("main"));
  document.querySelector('[data-language="ar"]').click();
  assert.equal(document.documentElement.lang, "ar");
  assert.equal(document.documentElement.dir, "rtl");

  document.querySelector('[data-language="en"]').click();
  document.querySelector('[data-visual-mode="emerald"]').click();
  assert.match(document.querySelector(".hero-visual").className, /visual-mode-emerald/);

  document.querySelector('[data-brief="hybrid-gt"]').click();
  assert.ok(document.querySelector("[data-brief-dialog]"));
  assert.match(document.querySelector("[data-brief-dialog]").textContent, /Emerald Voltage/);
  document.querySelector("[data-brief-request]").click();
  assert.equal(document.querySelector('select[name="interest"]').value, "hybrid-gt");
  await new Promise((resolve) => setTimeout(resolve, 600));
  assert.equal(document.activeElement, document.querySelector('.contact-form input[name="name"]'));

  const form = document.querySelector(".contact-form");
  form.querySelector('input[name="name"]').value = "Ari Client";
  form.querySelector('input[name="email"]').value = "ari@example.test";
  form.querySelector('select[name="timeline"]').value = "30-days";
  form.querySelector('select[name="channel"]').value = "private-viewing";
  form.dispatchEvent(new window.Event("input", { bubbles: true }));
  assert.equal(form.querySelector("[data-form-progress]").getAttribute("aria-valuenow"), "5");

  form.dispatchEvent(new window.Event("submit", { bubbles: true, cancelable: true }));
  await new Promise((resolve) => setTimeout(resolve, 0));
  assert.match(form.querySelector(".form-status").className, /is-success/);
  window.close();
});
