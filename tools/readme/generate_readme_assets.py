#!/usr/bin/env python3
"""
VIP Motors Atelier — README cinematic asset synthesizer (YASLOGIST edition).

Produces the README visual system under `assets/readme/`:

  * yaslogist-hero.gif        1920x720 seamless cinematic loop (~9.6 s)
  * yaslogist-hero.png        full-quality static poster (frame-0 composite)
  * yaslogist-divider.gif     1200x28 luminous section divider loop
  * yaslogist-signature.gif   880x240 closing YASLOGIST brand loop

Pipeline (mirrors tools/og/generate_og.py engineering)
------------------------------------------------------
1. Static stage  — grade the committed base plate, adaptive legibility scrim
   on the typographic column, fine film grain (kills 256-colour banding),
   brand lockup with pixel-measured layout + safe-area asserts, permanent
   YASLOGIST signature, then bake the ambient showroom light (horizon band +
   emerald glow, both detected from the plate itself) as fixed ambience.
2. Motion stage  — every moving effect is parameterised on t in [0, 1) with
   integer harmonics so the loop is mathematically seamless: a diagonal gold
   specular sweep, drifting gold dust, a rule glint, travelling pulses along
   the floor light line, a breathing reflection shimmer, a rotating dashed
   orbit around the brand seal and a coordinate scanner over the vehicle.
3. Encode        — amplitudes snap to a temporal lattice, frames snap to a
   3-level RGB lattice, ONE global 256-colour palette (no flicker), inter-frame
   transparency differencing (unchanged pixels cost ~nothing), hand-stitched
   GIF89a with disposal=1, then a Pillow round-trip proof of every frame.

Usage
-----
    python3 tools/readme/generate_readme_assets.py [--frames N] [--duration-ms MS]

Dependencies (build-time only; the site itself stays dependency-free):
    pip install pillow numpy arabic-reshaper python-bidi

Determinism: all randomness is seeded; re-running reproduces the exact files.
"""

from __future__ import annotations

import argparse
import io
import math
import random
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

W, H = 1920, 720
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
FONTS = REPO_ROOT / "tools" / "og" / "fonts"
OUT = REPO_ROOT / "assets" / "readme"

# Brand palette (mirrors :root tokens in style.css).
GOLD = (201, 166, 107)
GOLD_BRIGHT = (224, 189, 125)
IVORY = (245, 241, 233)
MUTED = (155, 155, 150)
INK = (8, 10, 12)
EMERALD = (47, 111, 79)

SWEEP = {  # diagonal specular sweep across the whole stage
    "start_x": -520.0,
    "travel": 2960.0,
    "sigma": 150.0,
    "peak": 0.15,
    "tilt": math.tan(math.radians(5.0)),
}
AMPLITUDE_STEP = 12 / 255.0
RGB_LATTICE = 3
PARTICLE_COUNT = 34
RANDOM_SEED = 11
GRAIN_SIGMA = 1.0
TRANSPARENT_INDEX = 255

# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #


def load_font(weight: int, family: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / f"{family}-{weight}.ttf"), size)


def tracked(draw, xy, text: str, font, fill, tracking: float):
    """Draw text with manual letterspacing; returns the pen end position."""
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        x += font.getlength(char) + tracking
    return x - tracking


def tracked_width(text: str, font, tracking: float) -> float:
    return sum(font.getlength(c) for c in text) + tracking * max(len(text) - 1, 0)


def smooth(v: np.ndarray) -> np.ndarray:
    return v * v * (3 - 2 * v)


def span_window(length: int, a: float, b: float, fade: float = 120.0) -> np.ndarray:
    positions = np.arange(length, dtype=np.float32)
    rise = np.clip((positions - a) / fade, 0.0, 1.0)
    fall = np.clip((b - positions) / fade, 0.0, 1.0)
    return smooth(rise) * smooth(fall)


def snap(values):
    """Snap amplitudes to the global step lattice (temporal anti-churn)."""
    return np.floor(values / AMPLITUDE_STEP) * AMPLITUDE_STEP


def screen(static: np.ndarray, fx: np.ndarray) -> np.ndarray:
    """True photographic screen blend: 1 - (1-a)(1-b)."""
    a = static / 255.0
    b = np.clip(fx, 0.0, 1.0)
    return ((1 - (1 - a) * (1 - b)) * 255).astype(np.uint8)


def draw_seal(canvas: Image.Image, cx: float, cy: float, size: float, alpha: int = 235):
    """The rotated-square brand seal as vector strokes."""
    sprite = Image.new("RGBA", (size * 3, size * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(sprite)
    c = size * 3 // 2
    half = size / 2 - 3
    d.polygon(
        [(c - half, c), (c, c - half), (c + half, c), (c, c + half)],
        outline=(*GOLD_BRIGHT, alpha),
        width=2,
    )
    d.ellipse([c - half + 9, c - half + 9, c + half - 9, c + half - 9],
              outline=(*GOLD, 190), width=1)
    d.ellipse([c - 3, c - 3, c + 3, c + 3], fill=(*GOLD_BRIGHT, 255))
    canvas.alpha_composite(sprite, (int(cx - size * 1.5), int(cy - size * 1.5)))


# --------------------------------------------------------------------------- #
# Static stage — grade, scrim, grain, typography, YASLOGIST signature
# --------------------------------------------------------------------------- #


def build_static(base_path: Path) -> tuple[np.ndarray, dict]:
    plate = Image.open(base_path).convert("RGB").resize((W, H), Image.LANCZOS)
    plate = ImageEnhance.Contrast(plate).enhance(1.05)
    plate = ImageEnhance.Color(plate).enhance(1.06)
    static = np.asarray(plate, dtype=np.float32)

    # Typographic legibility scrim: left column fade to near-ink.
    xs = np.arange(W, dtype=np.float32)
    scrim = np.clip(1.0 - xs / 700.0, 0.0, 1.0) ** 1.3
    static = static * (1.0 - (scrim[None, :, None] * 0.46)) + \
        np.array(INK, np.float32) * (scrim[None, :, None] * 0.46)

    # Soft vignette to focus the composition.
    ys = np.arange(H, dtype=np.float32)[:, None]
    vig = 1.0 - 0.22 * np.exp(-0.5 * ((ys - H / 2) / (H * 0.62)) ** 2) * \
        np.exp(-0.5 * ((xs[None, :] - W / 2) / (W * 0.62)) ** 2)
    static *= vig[..., None]

    # Fine monochrome film grain (static, kills 256-colour banding).
    rng = np.random.default_rng(42)
    static = static + rng.normal(0.0, GRAIN_SIGMA, (H, W, 1)).astype(np.float32)
    static = np.clip(static, 0, 255)

    meta: dict = {}
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    eyebrow_font = load_font(600, "manrope", 21)
    sub_font = load_font(700, "manrope", 33)
    tagline_font = load_font(400, "playfair-display", 40)
    micro_font = load_font(500, "manrope", 17)
    sig_font = load_font(700, "manrope", 21)
    sig_cap_font = load_font(500, "manrope", 13)

    # Wordmark auto-fits the typographic safe column (right edge <= 660).
    probe = load_font(600, "playfair-display", 100)
    measured = tracked_width("VIP MOTORS", probe, 2.5)
    wm_size = max(64, min(132, round(100 * 500.0 / measured)))
    wordmark_font = load_font(600, "playfair-display", wm_size)
    meta["wordmark_size"] = wm_size

    X = 96.0
    lines = [  # (id, ink height, gap after)
        ("seal", 56, 34),
        ("eyebrow", 16, 28),
        ("wordmark", wordmark_font.getbbox("VIP MOTORS")[3], 14),
        ("sub", sub_font.getbbox("ATELIER")[3] - sub_font.getbbox("ATELIER")[1], 28),
        ("rule", 2, 26),
        ("tagline", tagline_font.getbbox("A darker kind of luxury.")[3], 26),
        ("micro", micro_font.getbbox("DUBAI")[3], 0),
    ]
    total = sum(h + g for _, h, g in lines) - lines[-1][2]
    y = 116
    meta["block_top"], meta["block_bottom"] = y, y + total
    assert y + total <= 596, f"lockup exceeds safe area: {y}..{y + total}"

    draw_seal(canvas, X + 28, y + 28, 56)
    meta["seal"] = (X + 28.0, y + 28.0)
    y += lines[0][1] + lines[0][2]

    tracked(draw, (X, y), "PRIVATE AUTOMOTIVE CONCIERGE", eyebrow_font,
            (*GOLD_BRIGHT, 255), 6.5)
    y += lines[1][1] + lines[1][2]

    wm_right = tracked(draw, (X, y), "VIP MOTORS", wordmark_font, (*IVORY, 255), 2.5)
    assert wm_right <= 660, f"wordmark overflows column: {wm_right}"
    y += lines[2][1] + lines[2][2]

    tracked(draw, (X + 2, y), "ATELIER", sub_font, (*GOLD, 255), 22.0)
    y += lines[3][1] + lines[3][2]

    meta["rule"] = (X, y + 1, X + 380, y + 1)
    draw.rounded_rectangle([X, y, X + 380, y + 2], radius=1, fill=(*GOLD, 170))
    y += lines[4][1] + lines[4][2]

    draw.text((X, y), "A darker kind of luxury.", font=tagline_font,
              fill=(203, 198, 186, 255))
    y += lines[5][1] + lines[5][2]

    tracked(draw, (X, y), "DUBAI · LONDON · WORLDWIDE", micro_font,
            (*MUTED, 235), 5.2)

    # ---- permanent YASLOGIST signature, bottom-left (always visible) ----- #
    sy = 648
    draw_seal(canvas, X + 13, sy + 13, 26, alpha=220)
    sig_x = X + 40
    sig_end = tracked(draw, (sig_x, sy + 2), "YASLOGIST", sig_font,
                      (*GOLD_BRIGHT, 255), 7.0)
    tracked(draw, (sig_x, sy + 28), "CREATIVE ENGINEERING SIGNATURE",
            sig_cap_font, (*MUTED, 215), 3.6)
    meta["yas_sig"] = (sig_x, sy, sig_end)

    # ---- bilingual brand accent, bottom-right ----------------------------- #
    latin = "A YASLOGIST CINEMATIC EXPERIENCE"
    latin_w = tracked_width(latin, sig_cap_font, 3.4)
    x_end = W - 96
    tracked(draw, (x_end - latin_w, sy + 12), latin, sig_cap_font,
            (*MUTED, 225), 3.4)
    x_cursor = x_end - latin_w - 16
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display

        ar_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        ar_text = get_display(arabic_reshaper.reshape("ياسلوجست"))
        ar_w = ar_font.getlength(ar_text)
        draw.text((x_cursor - ar_w, sy + 6), ar_text, font=ar_font,
                  fill=(*GOLD, 235))
    except Exception as error:  # optional shaping libs — degrade to Latin only
        print(f"note: Arabic accent skipped ({error})")

    static = np.clip(static, 0, 255).astype(np.uint8)
    backdrop = np.asarray(Image.fromarray(static).convert("L"), dtype=np.float32)
    meta["backdrop_p95"] = float(np.percentile(backdrop[116:596, 80:660], 95))
    composed = Image.alpha_composite(
        Image.fromarray(static).convert("RGBA"), canvas).convert("RGB")
    static = np.asarray(composed, dtype=np.float32)
    return static, meta


# --------------------------------------------------------------------------- #
# Analysis — let the artwork dictate the light choreography
# --------------------------------------------------------------------------- #


def analyse(static: np.ndarray) -> dict:
    lum = static @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    right = lum[:, int(W * 0.42):int(W * 0.97)].mean(axis=1)
    horizon_y = int(np.argmax(np.convolve(right, np.ones(9) / 9, mode="same")))

    region = lum[:, int(W * 0.55):]
    threshold = np.percentile(region, 97)
    ys, xs = np.nonzero(region >= threshold)
    weights = region[ys, xs] - threshold + 1e-6
    glow = {
        "x": float((xs * weights).sum() / weights.sum() + W * 0.55),
        "y": float((ys * weights).sum() / weights.sum()),
    }

    # Vehicle bounding box from luminous structure (right of the column).
    zone = lum[:, int(W * 0.44):int(W * 0.97)]
    thr = max(34.0, float(np.percentile(zone, 82)))
    rows = (zone > thr).mean(axis=1)
    cols = (zone > thr).mean(axis=0)
    row_idx = np.nonzero(rows > 0.16)[0]
    col_idx = np.nonzero(cols > 0.12)[0]
    car = {
        "top": int(row_idx.min()) if len(row_idx) else horizon_y - 220,
        "x0": int(col_idx.min()) + int(W * 0.44) if len(col_idx) else int(W * 0.5),
        "x1": int(col_idx.max()) + int(W * 0.44) if len(col_idx) else int(W * 0.95),
    }
    car["top"] = min(car["top"], horizon_y - 120)
    print(f"analysis: horizon y={horizon_y}, glow=({glow['x']:.0f},{glow['y']:.0f}), "
          f"car top={car['top']} x=[{car['x0']},{car['x1']}]")
    return {"horizon_y": horizon_y, "glow": glow, "car": car}


# --------------------------------------------------------------------------- #
# Motion stage — additive light field, integer harmonics => seamless loop
# --------------------------------------------------------------------------- #


def build_particles() -> list:
    rng = random.Random(RANDOM_SEED)
    parts = []
    for index in range(PARTICLE_COUNT):
        bokeh = index % 7 == 3
        parts.append({
            "x": rng.uniform(90, W - 90),
            "y0": rng.uniform(260, 640),
            "rise": rng.uniform(150, 260),
            "phase": rng.random(),
            "radius": rng.uniform(7.0, 10.0) if bokeh else rng.uniform(1.8, 5.2),
            "amp": rng.uniform(0.06, 0.10) if bokeh else rng.uniform(0.12, 0.28),
            "sway": rng.uniform(10, 28),
            "sway_phase": rng.random() * math.tau,
            "sway_cycles": rng.choice((1, 2)),
            "tint": rng.choice(((1.00, 0.92, 0.70), (1.00, 0.86, 0.58), (0.95, 0.95, 0.88))),
        })
    return parts


def bake_ambience(static: np.ndarray, scene: dict) -> np.ndarray:
    """Screen fixed ambient showroom light into the plate once."""
    ys = np.arange(H, dtype=np.float32)[:, None]
    xs = np.arange(W, dtype=np.float32)[None, :]
    field = np.zeros((H, W, 3), np.float32)

    hy = scene["horizon_y"]
    horizon = np.exp(-0.5 * ((ys - hy) / 34.0) ** 2)
    field += (horizon * 0.07)[..., None] * np.array([1.00, 0.86, 0.58], np.float32)

    gx, gy = scene["glow"]["x"], scene["glow"]["y"]
    gd = ((xs - gx) ** 2 + (ys - gy) ** 2) / (2 * 150.0 ** 2)
    field += (np.exp(-gd) * 0.08)[..., None] * np.array([0.55, 0.90, 0.75], np.float32)
    return screen(static, field)


def fx_field(t: float, parts: list, meta: dict, scene: dict) -> np.ndarray:
    """Additive light field for normalised loop time t in [0, 1)."""
    field = np.zeros((H, W, 3), np.float32)
    ys = np.arange(H, dtype=np.float32)[:, None]
    xs = np.arange(W, dtype=np.float32)[None, :]
    hy = scene["horizon_y"]
    car = scene["car"]

    # 1 — diagonal gold specular sweep across the stage.
    center = SWEEP["start_x"] + SWEEP["travel"] * t
    distance = xs - center + SWEEP["tilt"] * (ys - H / 2)
    profile = snap(np.exp(-0.5 * (distance / SWEEP["sigma"]) ** 2) * SWEEP["peak"])
    band = profile * span_window(H, 50, H - 40, 140)[:, None]
    field += band[..., None] * np.array([1.00, 0.90, 0.70], np.float32)

    # 2 — drifting gold dust with sinusoidal life fade (wrap-safe).
    for p in parts:
        u = (t + p["phase"]) % 1.0
        fade = math.sin(math.pi * u) ** 2
        if fade < 0.02:
            continue
        px = p["x"] + p["sway"] * math.sin(math.tau * (u * p["sway_cycles"] + p["sway_phase"]))
        py = p["y0"] - p["rise"] * u
        sprite = np.exp(-0.5 * (((xs - px) ** 2) + ((ys - py) ** 2)) / p["radius"] ** 2)
        field += (sprite * p["amp"] * fade)[..., None] * np.array(p["tint"], np.float32)

    # 3 — glint running along the hairline rule.
    rx0, ry, rx1, _ = meta["rule"]
    glint_x = rx0 + (rx1 - rx0) * ((t + 0.3) % 1.0)
    gdist = ((xs - glint_x) ** 2 + (ys - ry) ** 2) / (2 * 26.0 ** 2)
    field += (np.exp(-gdist) * 0.55)[..., None] * np.array([1.00, 0.95, 0.80], np.float32)

    # 4 — travelling pulses along the floor light line (1 + 2 cycles).
    for cycles, amp, sigma, direction in ((1, 0.42, 95.0, 1.0), (2, 0.18, 55.0, -1.0)):
        u = (t * cycles) % 1.0
        if direction > 0:
            px = (car["x0"] - 260) + (W + 260 - (car["x0"] - 260)) * u
        else:
            px = (W + 160) - (W + 320) * u
        pulse = np.exp(-0.5 * ((xs - px) / sigma) ** 2) * \
            np.exp(-0.5 * ((ys - hy) / 7.0) ** 2)
        field += (snap(pulse * amp))[..., None] * np.array([1.00, 0.88, 0.62], np.float32)

    # 5 — breathing reflection shimmer under the vehicle (integer cycles).
    cx = (car["x0"] + car["x1"]) / 2
    half_w = (car["x1"] - car["x0"]) / 2 + 60
    env = span_window(W, cx - half_w, cx + half_w, 160)[None, :]
    for offset, k, phase in ((26.0, 1, 0.0), (52.0, 2, 0.33), (84.0, 1, 0.62)):
        level = snap(0.05 + 0.05 * math.sin(math.tau * (k * t + phase)))
        streak = np.exp(-0.5 * ((ys - (hy + offset)) / 3.2) ** 2)
        field += (streak * level * env)[..., None] * np.array([1.00, 0.86, 0.58], np.float32)

    # 6 — coordinate scanner gliding over the vehicle (cosine ease, wraps).
    sy = max(40, car["top"] - 42)
    sx0, sx1 = car["x0"] + 40, car["x1"] - 40
    dot_x = sx0 + (sx1 - sx0) * (0.5 - 0.5 * math.cos(math.tau * t))
    dot = np.exp(-0.5 * (((xs - dot_x) ** 2) / 16.0 + ((ys - sy) ** 2) / 9.0))
    field += (dot * 0.5)[..., None] * np.array([1.00, 0.95, 0.80], np.float32)
    trail = np.exp(-0.5 * ((ys - sy) / 1.6) ** 2) * \
        np.clip((xs - (dot_x - 130)) / 130.0, 0.0, 1.0) * \
        np.clip((dot_x - xs) / 8.0, 0.0, 1.0)
    field += (trail * 0.16)[..., None] * np.array([1.00, 0.90, 0.70], np.float32)

    return field


def seal_ring(t: float, meta: dict) -> Image.Image:
    """Rotating dashed orbit around the brand seal (one revolution per loop)."""
    cx, cy = meta["seal"]
    size = 168
    sprite = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(sprite)
    rot = t * 360.0
    r = 46
    for i in range(10):
        a0 = rot + i * 36
        d.arc([size / 2 - r, size / 2 - r, size / 2 + r, size / 2 + r],
              start=a0, end=a0 + 17, fill=(*GOLD_BRIGHT, 150), width=1)
    return sprite, (int(cx - size / 2), int(cy - size / 2))


# --------------------------------------------------------------------------- #
# Encode — hand-stitched GIF89a with inter-frame transparency differencing
# --------------------------------------------------------------------------- #


def _lzw_stream(frame: Image.Image) -> bytes:
    """Encode one P-mode frame as a single-frame GIF and lift its LZW stream."""
    buf = io.BytesIO()
    frame.save(buf, format="GIF", optimize=False, interlace=0)
    data = buf.getvalue()
    packed = data[10]
    i = 6 + 7
    if packed & 0x80:
        i += 3 * (2 ** ((packed & 0x07) + 1))
    while i < len(data):
        marker = data[i]
        if marker == 0x21:
            i += 2
            while data[i] != 0x00:
                i += 1 + data[i]
            i += 1
        elif marker == 0x2C:
            local_packed = data[i + 9]
            i += 10
            if local_packed & 0x80:
                i += 3 * (2 ** ((local_packed & 0x07) + 1))
            start = i
            i += 1
            while data[i] != 0x00:
                i += 1 + data[i]
            return data[start:i + 1]
        else:
            raise ValueError(f"unexpected GIF byte {marker:#04x} at {i}")
    raise ValueError("no image block found in encoded frame")


def encode_gif(frames: list, out_path: Path, duration_ms: int, w: int, h: int) -> None:
    delay = max(2, round(duration_ms / 10))
    palette = bytes(frames[0].getpalette()[:768])
    parts = [
        b"GIF89a",
        struct.pack("<HHBBB", w, h, 0xF7, 0, 0),
        palette,
        b"\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00",
    ]
    for index, frame in enumerate(frames):
        transparent = index > 0
        packed = 0x04 | (0x01 if transparent else 0x00)
        gce = b"\x21\xF9\x04" + bytes([packed]) + struct.pack("<H", delay)
        gce += bytes([TRANSPARENT_INDEX if transparent else 0x00]) + b"\x00"
        descriptor = b"\x2C" + struct.pack("<HHHH", 0, 0, w, h) + b"\x00"
        parts.append(gce + descriptor + _lzw_stream(frame))
    parts.append(b"\x3B")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(b"".join(parts))


def verify_gif(path: Path, index_frames: list, duration_ms: int, palette: list) -> None:
    """Round-trip proof through Pillow's own GIF compositor."""
    gif = Image.open(path)
    assert gif.n_frames == len(index_frames), f"frame count {gif.n_frames}"
    assert gif.info.get("loop", 1) == 0, "loop-forever extension missing"
    pal = np.array(palette[:768], dtype=np.uint8).reshape(256, 3)
    delay_cs = max(2, round(duration_ms / 10))
    for i in range(gif.n_frames):
        gif.seek(i)
        assert gif.info.get("duration") == delay_cs * 10, \
            f"frame {i} delay {gif.info.get('duration')}"
        rendered = np.asarray(gif.convert("RGB"), dtype=np.uint8)
        intended = pal[index_frames[i]]
        assert (rendered == intended).all(), f"frame {i} does not compose faithfully"
    print(f"verify: {gif.n_frames} frames render pixel-faithfully, loop=forever, "
          f"{delay_cs * 10} ms/frame")


def qa(frames_rgb: list, count: int, body_lo=0.2, body_hi=7.0,
       check_lockup=True) -> None:
    diffs = [
        np.abs(frames_rgb[(i + 1) % count].astype(np.int16) - frames_rgb[i]).mean()
        for i in range(count)
    ]
    seam = diffs[-1]
    body = float(np.mean(diffs[:-1]))
    print(f"qa: mean inter-frame delta = {body:.2f}/255, loop seam = {seam:.2f}/255")
    assert body_lo <= body <= body_hi, "motion amplitude outside the luxury envelope"
    assert seam <= body * 2.2 + 0.4, "loop seam is visible"
    if check_lockup:
        lum = frames_rgb[0] @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        lockup = lum[116:596, 80:660]
        assert lockup.max() >= 200, "wordmark ink is missing or too dim"
        print(f"qa: wordmark ink peak = {lockup.max():.0f}/255")
    peak = int(np.abs(frames_rgb[count // 2].astype(np.int16) - frames_rgb[0]).max())
    assert peak >= 20, f"effects too faint (peak delta {peak})"
    print(f"qa: sweep peak delta = {peak}/255 — OK")


def render_sequence(static, meta, scene, parts, frames: int):
    frames_rgb, fx_max = [], np.zeros((H, W, 3), np.float32)
    for index in range(frames):
        t = index / frames
        fx = fx_field(t, parts, meta, scene)
        fx_max = np.maximum(fx_max, fx)
        frames_rgb.append(screen(static, fx))
    return frames_rgb, fx_max


def package(frames_rgb, fx_max, static):
    """Lattice-snap, global palette, index frames, transparency-diff frames."""
    lattice = RGB_LATTICE
    bucketed = [(f // lattice) * lattice for f in frames_rgb]
    bucketed_max = (screen(static, fx_max) // lattice) * lattice
    palette_img = Image.fromarray(bucketed_max).quantize(
        colors=256, method=Image.MEDIANCUT)
    palette = palette_img.getpalette()
    # Pillow 12 trims palettes to the colours actually present; the GIF89a
    # header promises a 256-entry global table, so pad back to 768 bytes
    # (index 255 stays reserved for inter-frame transparency).
    if len(palette) < 768:
        palette = (palette + list(INK) * ((768 - len(palette)) // 3 + 1))[:768]
    indices = [
        np.array(Image.fromarray(b).quantize(palette=palette_img,
                                             dither=Image.Dither.NONE))
        for b in bucketed
    ]
    indices = [np.where(idx == TRANSPARENT_INDEX, TRANSPARENT_INDEX - 1, idx)
               for idx in indices]
    out_frames = []
    for position, idx in enumerate(indices):
        if position == 0:
            data = idx
        else:
            unchanged = np.all(bucketed[position] == bucketed[position - 1], axis=-1)
            data = np.where(unchanged, TRANSPARENT_INDEX, idx)
        frame = Image.fromarray(data.astype(np.uint8), mode="P")
        frame.putpalette(palette)
        out_frames.append(frame)
    return out_frames, indices, palette


# --------------------------------------------------------------------------- #
# Supporting animations — divider + closing signature
# --------------------------------------------------------------------------- #


def build_divider(duration_ms: int, frames: int = 48) -> None:
    dw, dh = 1200, 28
    base = np.zeros((dh, dw, 3), np.float32)
    xs = np.arange(dw, dtype=np.float32)[None, :]
    ys = np.arange(dh, dtype=np.float32)[:, None]
    line = np.exp(-0.5 * ((ys - dh / 2) / 1.1) ** 2)
    edge = np.clip(xs / 220.0, 0, 1) * np.clip((dw - xs) / 220.0, 0, 1)
    base += (line * 0.16 * edge)[..., None] * np.array([1.00, 0.86, 0.58], np.float32)

    canvas = Image.new("RGBA", (dw, dh), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    c = dw / 2
    half = 7
    d.polygon([(c - half, dh / 2), (c, dh / 2 - half), (c + half, dh / 2),
               (c, dh / 2 + half)], outline=(*GOLD_BRIGHT, 230), width=1)
    d.ellipse([c - 2, dh / 2 - 2, c + 2, dh / 2 + 2], fill=(*GOLD_BRIGHT, 255))
    static = np.asarray(
        Image.alpha_composite(
            Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA"),
            canvas).convert("RGB"), dtype=np.float32)

    frames_rgb = []
    fx_max = np.zeros((dh, dw, 3), np.float32)
    for index in range(frames):
        t = index / frames
        fx = np.zeros((dh, dw, 3), np.float32)
        for cycles, amp, sigma in ((1, 0.5, 70.0), (2, 0.2, 40.0)):
            u = (t * cycles) % 1.0
            px = -80 + (dw + 160) * u
            pulse = np.exp(-0.5 * ((xs - px) / sigma) ** 2) * \
                np.exp(-0.5 * ((ys - dh / 2) / 2.2) ** 2)
            fx += (snap(pulse * amp))[..., None] * np.array([1.00, 0.90, 0.66], np.float32)
        glint = np.exp(-0.5 * (((xs - c) ** 2) / 26.0 ** 2)) * \
            (0.05 + 0.05 * math.sin(math.tau * 2 * t))
        fx += (snap(glint))[..., None] * np.array([1.00, 0.95, 0.80], np.float32)
        frames_rgb.append(screen(static, fx))
        fx_max = np.maximum(fx_max, fx)

    out_frames, indices, palette = package(frames_rgb, fx_max, static)
    path = OUT / "yaslogist-divider.gif"
    encode_gif(out_frames, path, duration_ms, dw, dh)
    verify_gif(path, indices, duration_ms, palette)
    qa(frames_rgb, frames, body_lo=0.05, body_hi=8.0, check_lockup=False)
    print(f"encoded: {path} ({path.stat().st_size / 1024:.0f} KB)")


def build_signature(duration_ms: int, frames: int = 40) -> None:
    sw, sh = 880, 240
    base = np.zeros((sh, sw, 3), np.float32)
    ys = np.arange(sh, dtype=np.float32)[:, None]
    xs = np.arange(sw, dtype=np.float32)[None, :]
    glow = np.exp(-0.5 * (((xs - sw / 2) ** 2) / (2 * 260.0 ** 2) +
                          ((ys - sh / 2) ** 2) / (2 * 90.0 ** 2)))
    base += (glow * 0.05)[..., None] * np.array([1.00, 0.86, 0.58], np.float32)

    canvas = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    word_font = load_font(700, "manrope", 46)
    cap_font = load_font(500, "manrope", 15)
    draw_seal(canvas, sw / 2, 74, 44)
    text = "YASLOGIST"
    tw = tracked_width(text, word_font, 14.0)
    tracked(d, (sw / 2 - tw / 2, 122), text, word_font, (*IVORY, 255), 14.0)
    cap = "CREATIVE ENGINEERING SIGNATURE  ·  WWW.YASLOGIST.COM"
    cw = tracked_width(cap, cap_font, 3.6)
    tracked(d, (sw / 2 - cw / 2, 186), cap, cap_font, (*MUTED, 225), 3.6)
    d.rounded_rectangle([sw / 2 - 150, 172, sw / 2 + 150, 173], radius=1,
                        fill=(*GOLD, 140))
    static = np.asarray(
        Image.alpha_composite(
            Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA"),
            canvas).convert("RGB"), dtype=np.float32)

    rng = random.Random(5)
    parts = [{
        "x": rng.uniform(120, sw - 120), "y0": rng.uniform(90, 210),
        "rise": rng.uniform(40, 80), "phase": rng.random(),
        "radius": rng.uniform(1.6, 3.6), "amp": rng.uniform(0.10, 0.22),
        "sway": rng.uniform(6, 14), "sway_phase": rng.random() * math.tau,
        "sway_cycles": rng.choice((1, 2)),
        "tint": (1.00, 0.90, 0.66),
    } for _ in range(12)]

    frames_rgb = []
    fx_max = np.zeros((sh, sw, 3), np.float32)
    for index in range(frames):
        t = index / frames
        fx = np.zeros((sh, sw, 3), np.float32)
        center = -260 + (sw + 520) * t
        distance = xs - center + math.tan(math.radians(8)) * (ys - sh / 2)
        profile = snap(np.exp(-0.5 * (distance / 90.0) ** 2) * 0.14)
        fx += profile[..., None] * np.array([1.00, 0.90, 0.70], np.float32)
        for p in parts:
            u = (t + p["phase"]) % 1.0
            fade = math.sin(math.pi * u) ** 2
            if fade < 0.02:
                continue
            px = p["x"] + p["sway"] * math.sin(math.tau * (u * p["sway_cycles"] + p["sway_phase"]))
            py = p["y0"] - p["rise"] * u
            sprite = np.exp(-0.5 * (((xs - px) ** 2) + ((ys - py) ** 2)) / p["radius"] ** 2)
            fx += (sprite * p["amp"] * fade)[..., None] * np.array(p["tint"], np.float32)
        frames_rgb.append(screen(static, fx))
        fx_max = np.maximum(fx_max, fx)

    out_frames, indices, palette = package(frames_rgb, fx_max, static)
    path = OUT / "yaslogist-signature.gif"
    encode_gif(out_frames, path, duration_ms, sw, sh)
    verify_gif(path, indices, duration_ms, palette)
    qa(frames_rgb, frames, body_lo=0.05, body_hi=8.0, check_lockup=False)
    print(f"encoded: {path} ({path.stat().st_size / 1024:.0f} KB)")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main() -> int:
    parser = argparse.ArgumentParser(description="README cinematic assets")
    parser.add_argument("--base", type=Path, default=HERE / "base.png")
    parser.add_argument("--frames", type=int, default=96)
    parser.add_argument("--duration-ms", type=int, default=100)
    parser.add_argument("--skip-support", action="store_true")
    args = parser.parse_args()

    static, meta = build_static(args.base)
    print(f"contrast: backdrop p95 luminance = {meta['backdrop_p95']:.1f} (target <= 66)")
    assert meta["backdrop_p95"] <= 66, "typographic zone too bright — increase scrim"

    scene = analyse(static)
    static = bake_ambience(static, scene).astype(np.float32)
    parts = build_particles()

    frames_rgb, fx_max = render_sequence(static, meta, scene, parts, args.frames)

    # Poster — full-quality frame 0 composite, lossless PNG.
    poster = OUT / "yaslogist-hero.png"
    poster.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(frames_rgb[0]).save(poster, optimize=True)
    print(f"encoded: {poster} ({poster.stat().st_size / 1024:.0f} KB)")

    out_frames, indices, palette = package(frames_rgb, fx_max, static)
    hero = OUT / "yaslogist-hero.gif"
    encode_gif(out_frames, hero, args.duration_ms, W, H)
    verify_gif(hero, indices, args.duration_ms, palette)
    size = hero.stat().st_size
    print(f"encoded: {hero}\n  frames={args.frames} frame={args.duration_ms}ms "
          f"loop={args.frames * args.duration_ms / 1000:.1f}s size={size / 1024 / 1024:.2f} MB")
    qa(frames_rgb, args.frames)

    if not args.skip_support:
        build_divider(80)
        build_signature(90)
    return 0


if __name__ == "__main__":
    sys.exit(main())
