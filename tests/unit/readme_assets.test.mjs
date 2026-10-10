import assert from "node:assert/strict";
import { readFileSync, statSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "../..");
const read = (file) => readFileSync(resolve(root, file));
const text = (file) => read(file).toString("utf8");

function gifInfo(buffer) {
  assert.equal(buffer.subarray(0, 6).toString("latin1"), "GIF89a", "GIF89a signature missing");
  return {
    width: buffer.readUInt16LE(6),
    height: buffer.readUInt16LE(8),
    loops: buffer.includes(Buffer.from("NETSCAPE2.0", "latin1")),
  };
}

function pngInfo(buffer) {
  assert.equal(buffer.subarray(1, 4).toString("latin1"), "PNG", "PNG signature missing");
  return { width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20) };
}

test("the README opens with the cinematic hero and references real assets", () => {
  const readme = text("README.md");
  const firstElement = readme.match(/<img[\s\S]*?\/>/)[0];
  assert.match(firstElement, /assets\/readme\/yaslogist-hero\.gif/);
  assert.match(firstElement, /width="100%"/);
  for (const asset of [
    "assets/readme/yaslogist-hero.gif",
    "assets/readme/yaslogist-hero.png",
    "assets/readme/yaslogist-divider.gif",
    "assets/readme/yaslogist-signature.gif",
  ]) {
    assert.ok(readme.includes(asset), `README must reference ${asset}`);
    statSync(resolve(root, asset)); // throws when the referenced file is missing
  }
  assert.match(readme, /YASLOGIST/);
});

test("the README hero ships as a valid 1920x720 looping GIF inside the delivery budget", () => {
  const gif = read("assets/readme/yaslogist-hero.gif");
  const info = gifInfo(gif);
  assert.equal(info.width, 1920, "hero must be 1920 wide");
  assert.equal(info.height, 720, "hero must be 720 tall");
  assert.equal(info.loops, true, "loop-forever extension missing");
  assert.ok(gif.length <= 10 * 1024 * 1024, `hero is ${gif.length} bytes (policy: 10 MB)`);
});

test("the hero poster and supporting animations exist with correct canvases", () => {
  const poster = pngInfo(read("assets/readme/yaslogist-hero.png"));
  assert.deepEqual({ w: poster.width, h: poster.height }, { w: 1920, h: 720 });

  const divider = gifInfo(read("assets/readme/yaslogist-divider.gif"));
  assert.equal(divider.width, 1200);
  assert.equal(divider.height, 28);
  assert.equal(divider.loops, true);

  const signature = gifInfo(read("assets/readme/yaslogist-signature.gif"));
  assert.equal(signature.width, 880);
  assert.equal(signature.height, 240);
  assert.equal(signature.loops, true);
  assert.ok(statSync(resolve(root, "assets/readme/yaslogist-signature.gif")).size <= 512 * 1024);
});
