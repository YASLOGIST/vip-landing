#!/usr/bin/env python3
"""
VIP Motors Atelier — Open Graph social-card synthesizer.

Produces `assets/og-image-animated.gif` (1200x630, seamless loop) from a
committed cinematic base plate (`tools/og/base.png`) plus the brand's real
typography (Playfair Display + Manrope, committed under `tools/og/fonts/`).

Pipeline
--------
1. Static stage  — grade the base plate, add an adaptive legibility scrim on
   the typographic column, bake fine film grain (prevents GIF banding), and
   composite the brand lockup with pixel-measured layout and safe-area asserts.
2. Analysis      — detect the horizon band and the brightest glow blob from
   the plate itself, so the light choreography tracks the artwork instead of
   guessing coordinates.
3. Motion stage  — a slow diagonal gold specular sweep across the lockup,
   drifting gold bokeh dust and a glint running along the hairline rule.
   The horizon band and showroom glow are screened in as fixed ambience:
   at ~2% amplitude their pulse is imperceptible, yet animating them would
   re-encode their entire region every frame. Every moving effect is
   parameterised on t in [0, 1) with integer harmonics, so the loop is
   mathematically seamless.
4. Encode        — every frame is screened onto the static plate, then
   quantised against ONE global 256-colour palette derived from the
   maximum-intensity composite (no palette flicker, no per-frame dither).

Usage
-----
    python3 tools/og/generate_og.py [--base PATH] [--out PATH]
                                    [--frames N] [--duration-ms MS]

Dependencies (build-time only; the site itself stays dependency-free):
    pip install pillow numpy arabic-reshaper python-bidi

The Arabic accent line degrades gracefully to Latin-only if the optional
arabic-reshaper / python-bidi packages are absent.

Determinism: all randomness is seeded; re-running reproduces the exact GIF.
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

W, H = 1200, 630
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent

# Brand palette (mirrors :root tokens in style.css).
GOLD = (201, 166, 107)
GOLD_BRIGHT = (224, 189, 125)
IVORY = (245, 241, 233)
MUTED = (155, 155, 150)
INK = (8, 10, 12)

SWEEP = {  # near-vertical specular sweep, confined to the typographic column
    "start_x": -300.0,
    "travel": 1000.0,
    "sigma": 100.0,
    "peak": 0.20,
    "tilt": math.tan(math.radians(6.0)),
    "zone": (0.0, 640.0),  # sheen glides across the lockup, never the car
}
# Effects snap to amplitude steps of this many 1/255ths. Between frames a
# region only changes when its amplitude crosses a step boundary, so slow
# gradients stop re-encoding every pixel and the loop stays feather-light.
AMPLITUDE_STEP = 14 / 255.0
PARTICLE_COUNT = 26
HORIZON_BREATHE = {"sigma": 30.0, "base": 0.045, "amp": 0.05}
GLOW_PULSE = {"sigma": 135.0, "base": 0.055, "amp": 0.05}
RULE_GLINT = {"sigma": 26.0, "peak": 0.60}

RANDOM_SEED = 7
# Grain is capped near 1 LSB: enough to defeat 256-colour banding, gentle on
# LZW (GIF frame compression collapses when every pixel carries white noise).
GRAIN_SIGMA = 1.05


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #

def load_font(weight: int, family: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(HERE / "fonts" / f"{family}-{weight}.ttf"), size)


def tracked(draw: ImageDraw.ImageDraw, xy, text: str, font, fill, tracking: float):
    """Draw text with manual letterspacing; returns the pen end position."""
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        x += font.getlength(char) + tracking
    return x - tracking


def tracked_width(text: str, font, tracking: float) -> float:
    return sum(font.getlength(c) for c in text) + tracking * max(len(text) - 1, 0)


def y_window(height: int) -> np.ndarray:
    """Smooth 0 -> 1 -> 0 window so effects never ignite the frame edges."""
    ys = np.arange(height, dtype=np.float32)
    rise = np.clip((ys - 36) / 66.0, 0.0, 1.0)
    fall = np.clip((596 - ys) / 66.0, 0.0, 1.0)
    smooth = lambda v: v * v * (3 - 2 * v)  # smoothstep
    return (smooth(rise) * smooth(fall))[:, None]


# --------------------------------------------------------------------------- #
# Static stage — grade, scrim, grain, typography
# --------------------------------------------------------------------------- #

def build_static(base_path: Path) -> tuple[np.ndarray, dict]:
    plate = Image.open(base_path).convert("RGB").resize((W, H), Image.LANCZOS)
    plate = ImageEnhance.Contrast(plate).enhance(1.06)
    plate = ImageEnhance.Color(plate).enhance(1.05)

    static = np.asarray(plate, dtype=np.float32)

    # Typographic legibility scrim: left column fade to near-ink.
    xs = np.arange(W, dtype=np.float32)
    scrim = np.clip(1.0 - xs / 560.0, 0.0, 1.0) ** 1.35
    scrim = (scrim[None, :, None] * 0.42).astype(np.float32)
    static = static * (1.0 - scrim) + np.array(INK, np.float32) * scrim

    # Fine monochrome film grain (static, kills 256-colour banding).
    rng = np.random.default_rng(42)
    static = static + rng.normal(0.0, GRAIN_SIGMA, (H, W, 1)).astype(np.float32)

    # ---- Typography ------------------------------------------------------- #
    meta: dict = {}
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    eyebrow_font = load_font(600, "manrope", 17)
    sub_font = load_font(700, "manrope", 27)
    tagline_font = load_font(400, "playfair-display", 31)
    micro_font = load_font(500, "manrope", 14)

    # Wordmark auto-fits the typographic safe column (right edge <= 500).
    probe = load_font(600, "playfair-display", 100)
    measured = tracked_width("VIP MOTORS", probe, 2.0)
    wm_size = max(56, min(112, round(100 * 412.0 / measured)))
    wordmark_font = load_font(600, "playfair-display", wm_size)
    meta["wordmark_size"] = wm_size

    X = 72.0
    lines = [  # (id, ink height, gap after)
        ("monogram", 44, 30),
        ("eyebrow", 13, 24),
        ("wordmark", wordmark_font.getbbox("VIP MOTORS")[3], 12),
        ("sub", sub_font.getbbox("ATELIER")[3] - sub_font.getbbox("ATELIER")[1], 24),
        ("rule", 2, 22),
        ("tagline", tagline_font.getbbox("A darker kind of luxury.")[3], 24),
        ("micro", micro_font.getbbox("DUBAI")[3], 0),
    ]
    total = sum(height + gap for _, height, gap in lines) - lines[-1][2]
    y = round((H - total) / 2) - 4
    meta["block_top"], meta["block_bottom"] = y, y + total
    assert 118 <= y and y + total <= 540, f"lockup exceeds safe area: {y}..{y + total}"

    # Monogram — the site's rotated-square seal, redrawn as vector strokes.
    ms = 44
    mx, my = X + ms / 2, y + ms / 2
    mono = Image.new("RGBA", (ms * 3, ms * 3), (0, 0, 0, 0))
    md = ImageDraw.Draw(mono)
    c = ms * 3 // 2
    half = ms / 2 - 3
    md.polygon(
        [(c - half, c), (c, c - half), (c + half, c), (c, c + half)],
        outline=(*GOLD_BRIGHT, 235), width=2,
    )
    md.ellipse([c - half + 9, c - half + 9, c + half - 9, c + half - 9], outline=(*GOLD, 190), width=1)
    md.ellipse([c - 3, c - 3, c + 3, c + 3], fill=(*GOLD_BRIGHT, 255))
    canvas.alpha_composite(mono, (int(mx - ms * 1.5), int(my - ms * 1.5)))
    y += lines[0][1] + lines[0][2]

    tracked(draw, (X, y), "PRIVATE AUTOMOTIVE CONCIERGE", eyebrow_font, (*GOLD_BRIGHT, 255), 5.4)
    y += lines[1][1] + lines[1][2]

    wm_right = tracked(draw, (X, y), "VIP MOTORS", wordmark_font, (*IVORY, 255), 2.0)
    assert wm_right <= 500, f"wordmark overflows column: {wm_right}"
    y += lines[2][1] + lines[2][2]

    tracked(draw, (X + 1, y), "ATELIER", sub_font, (*GOLD, 255), 19.0)
    y += lines[3][1] + lines[3][2]

    meta["rule"] = (X, y + 1, X + 300, y + 1)
    draw.rounded_rectangle([X, y, X + 300, y + 2], radius=1, fill=(*GOLD, 170))
    y += lines[4][1] + lines[4][2]

    draw.text((X, y), "A darker kind of luxury.", font=tagline_font, fill=(203, 198, 186, 255))
    y += lines[5][1] + lines[5][2]

    tracked(draw, (X, y), "DUBAI · LONDON · WORLDWIDE", micro_font, (*MUTED, 235), 4.6)

    # Bilingual signature, bottom-right.
    signature(canvas, micro_font)
    static = np.clip(static, 0, 255).astype(np.uint8)
    # Backdrop contrast is measured BEFORE typography lands on the plate.
    backdrop = np.asarray(Image.fromarray(static).convert("L"), dtype=np.float32)
    meta["backdrop_p95"] = float(np.percentile(backdrop[118:540, 60:500], 95))
    composed = Image.alpha_composite(
        Image.fromarray(static).convert("RGBA"), canvas).convert("RGB")
    static = np.asarray(composed, dtype=np.float32)

    return static, meta


def signature(canvas: Image.Image, micro_font) -> None:
    """Bottom-right bilingual line: Arabic accent + latin caption."""
    y = 566
    latin = "BY APPOINTMENT ONLY"
    draw = ImageDraw.Draw(canvas)
    latin_w = tracked_width(latin, micro_font, 3.4)
    x_end = W - 72
    tracked(draw, (x_end - latin_w, y + 2), latin, micro_font, (*MUTED, 225), 3.4)
    x_cursor = x_end - latin_w - 14
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display

        ar_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
        ar_text = get_display(arabic_reshaper.reshape("بالموعد فقط"))
        ar_w = ar_font.getlength(ar_text)
        draw.text((x_cursor - ar_w, y - 3), ar_text, font=ar_font, fill=(*GOLD, 235))
    except Exception as error:  # optional shaping libs — degrade to Latin only
        print(f"note: Arabic accent skipped ({error})")


# --------------------------------------------------------------------------- #
# Analysis — let the artwork dictate the light choreography
# --------------------------------------------------------------------------- #

def analyse(static: np.ndarray) -> dict:
    lum = static @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    right = lum[:, 680:1180].mean(axis=1)
    horizon_y = int(np.argmax(np.convolve(right, np.ones(9) / 9, mode="same")))

    region = lum[:, 640:]
    threshold = np.percentile(region, 97)
    ys, xs = np.nonzero(region >= threshold)
    weights = region[ys, xs] - threshold
    glow = {
        "x": float((xs * weights).sum() / weights.sum() + 640),
        "y": float((ys * weights).sum() / weights.sum()),
    }
    print(f"analysis: horizon y={horizon_y}, glow centroid=({glow['x']:.0f}, {glow['y']:.0f})")
    return {"horizon_y": horizon_y, "glow": glow}


# --------------------------------------------------------------------------- #
# Motion stage — additive light field, all harmonics integer => seamless loop
# --------------------------------------------------------------------------- #

def build_particles() -> list[dict]:
    rng = random.Random(RANDOM_SEED)
    parts = []
    for index in range(PARTICLE_COUNT):
        bokeh = index % 7 == 3
        parts.append({
            "x": rng.uniform(50, 1150),
            "y0": rng.uniform(210, 570),
            "rise": rng.uniform(130, 230),
            "phase": rng.random(),
            "radius": rng.uniform(6.4, 9.2) if bokeh else rng.uniform(1.6, 4.8),
            "amp": rng.uniform(0.07, 0.11) if bokeh else rng.uniform(0.13, 0.30),
            "sway": rng.uniform(10, 26),
            "sway_phase": rng.random() * math.tau,
            "sway_cycles": rng.choice((1, 2)),
            "tint": rng.choice(((1.00, 0.92, 0.70), (1.00, 0.86, 0.58), (0.95, 0.95, 0.88))),
        })
    return parts


def snap(values: np.ndarray | float) -> np.ndarray | float:
    """Snap an amplitude to the global step lattice (temporal anti-churn)."""
    return np.floor(values / AMPLITUDE_STEP) * AMPLITUDE_STEP


def span_window(length: int, a: float, b: float, fade: float = 120.0) -> np.ndarray:
    """Smooth 0 -> 1 -> 0 window that confines an effect to [a, b]."""
    positions = np.arange(length, dtype=np.float32)
    rise = np.clip((positions - a) / fade, 0.0, 1.0)
    fall = np.clip((b - positions) / fade, 0.0, 1.0)
    smooth = lambda v: v * v * (3 - 2 * v)
    return smooth(rise) * smooth(fall)


def x_window(width: int, x0: float, x1: float) -> np.ndarray:
    return span_window(width, x0, x1)[None, :]


def bake_ambience(static: np.ndarray, scene: dict) -> np.ndarray:
    """Screen the ambient showroom light into the static plate once.

    The horizon band and the corner glow breathe at only ~2% amplitude —
    below what an animated loop can justify against its encoding cost — so
    they are rendered as fixed ambience at their mid-cycle level instead of
    pulsing and re-encoding their entire region every frame.
    """
    ys = np.arange(H, dtype=np.float32)[:, None]
    xs = np.arange(W, dtype=np.float32)[None, :]
    field = np.zeros((H, W, 3), np.float32)

    hy = scene["horizon_y"]
    horizon = np.exp(-0.5 * ((ys - hy) / HORIZON_BREATHE["sigma"]) ** 2)
    level = HORIZON_BREATHE["base"] + 0.5 * HORIZON_BREATHE["amp"]
    field += (horizon * level)[..., None] * np.array([1.00, 0.86, 0.58], np.float32)

    gx, gy = scene["glow"]["x"], scene["glow"]["y"]
    glow_level = GLOW_PULSE["base"] + 0.5 * GLOW_PULSE["amp"]
    gd = ((xs - gx) ** 2 + (ys - gy) ** 2) / (2 * GLOW_PULSE["sigma"] ** 2)
    field += (np.exp(-gd) * glow_level)[..., None] * np.array([1.00, 0.88, 0.62], np.float32)

    return screen(static, field)


def fx_field(t: float, parts: list[dict], meta: dict, win: np.ndarray) -> np.ndarray:
    """Return the HxWx3 additive light field for normalised loop time t."""
    field = np.zeros((H, W, 3), np.float32)

    # Diagonal gold specular sweep across the lockup column. The column
    # profile is amplitude-snapped, so a pixel only re-encodes when the band's
    # intensity at that column crosses a lattice step.
    center = SWEEP["start_x"] + SWEEP["travel"] * t
    ys = np.arange(H, dtype=np.float32)[:, None]
    xs = np.arange(W, dtype=np.float32)[None, :]
    distance = xs - center + SWEEP["tilt"] * (ys - H / 2)
    profile = snap(np.exp(-0.5 * (distance / SWEEP["sigma"]) ** 2) * SWEEP["peak"])
    sweep_window = span_window(H, 60, 570, 130)[:, None]
    band = profile * sweep_window * x_window(W, *SWEEP["zone"])
    field += band[..., None] * np.array([1.00, 0.90, 0.70], np.float32)

    # Drifting gold dust with sinusoidal life fade (wrap-safe).
    for p in parts:
        u = (t + p["phase"]) % 1.0
        fade = math.sin(math.pi * u) ** 2
        if fade < 0.02:
            continue
        px = p["x"] + p["sway"] * math.sin(math.tau * (u * p["sway_cycles"] + p["sway_phase"]))
        py = p["y0"] - p["rise"] * u
        dx2 = (xs - px) ** 2          # (1, W)
        dy2 = (ys - py) ** 2          # (H, 1)
        sprite = np.exp(-0.5 * ((dx2 + dy2) / p["radius"] ** 2))
        field += (sprite * p["amp"] * fade * win)[..., None] * np.array(p["tint"], np.float32)

    # Glint running along the hairline rule.
    rx0, ry, rx1, _ = meta["rule"]
    glint_x = rx0 + (rx1 - rx0) * ((t + 0.3) % 1.0)
    gdist = ((xs - glint_x) ** 2 + (ys - ry) ** 2) / (2 * RULE_GLINT["sigma"] ** 2)
    field += (np.exp(-gdist) * RULE_GLINT["peak"])[..., None] * np.array([1.00, 0.95, 0.80], np.float32)

    return field


def screen(static: np.ndarray, fx: np.ndarray) -> np.ndarray:
    """True photographic screen blend: 1 - (1-a)(1-b). Text stays clipped-clean."""
    a = static / 255.0
    b = np.clip(fx, 0.0, 1.0)
    return ((1 - (1 - a) * (1 - b)) * 255).astype(np.uint8)


# --------------------------------------------------------------------------- #
# Encode — hand-stitched GIF89a with inter-frame transparency differencing
# --------------------------------------------------------------------------- #

TRANSPARENT_INDEX = 255
RGB_LATTICE = 3  # amplitude floor: changes below this many levels are dropped


def _lzw_stream(frame: Image.Image) -> bytes:
    """Encode one P-mode frame as a single-frame GIF and lift its LZW stream.

    Pillow cannot write per-frame transparency in a multi-frame GIF, so each
    frame is encoded alone (where its transparent index IS honoured) and the
    compressed stream is re-stitched into a single master file below.
    """
    buf = io.BytesIO()
    frame.save(buf, format="GIF", optimize=False, interlace=0)
    data = buf.getvalue()

    packed = data[10]
    i = 6 + 7
    if packed & 0x80:
        i += 3 * (2 ** ((packed & 0x07) + 1))  # global color table
    while i < len(data):
        marker = data[i]
        if marker == 0x21:  # extension block — skip
            i += 2
            while data[i] != 0x00:
                i += 1 + data[i]
            i += 1
        elif marker == 0x2C:  # image descriptor
            local_packed = data[i + 9]
            i += 10
            if local_packed & 0x80:
                i += 3 * (2 ** ((local_packed & 0x07) + 1))  # local color table
            start = i
            i += 1  # LZW min-code-size
            while data[i] != 0x00:  # data sub-blocks
                i += 1 + data[i]
            return data[start:i + 1]
        else:
            raise ValueError(f"unexpected GIF byte {marker:#04x} at {i}")
    raise ValueError("no image block found in encoded frame")


def encode_gif(frames: list[Image.Image], out_path: Path, duration_ms: int) -> None:
    """Assemble a looping GIF89a: one global palette, per-frame GCE.

    Frame 0 is fully opaque (it is the poster crawlers show when they do not
    animate); later frames carry only changed pixels, with every unchanged
    pixel mapped to the transparent index and disposal=1 so the accumulated
    canvas persists beneath them.
    """
    delay = max(2, round(duration_ms / 10))  # GIF stores centiseconds
    palette = bytes(frames[0].getpalette()[:768])

    parts = [
        b"GIF89a",
        struct.pack("<HHBBB", W, H, 0xF7, 0, 0),          # screen descriptor + GCT flag
        palette,
        b"\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00",    # loop forever
    ]
    for index, frame in enumerate(frames):
        transparent = index > 0
        packed = 0x04 | (0x01 if transparent else 0x00)    # disposal=1, transparency flag
        gce = b"\x21\xF9\x04" + bytes([packed]) + struct.pack("<H", delay)
        gce += bytes([TRANSPARENT_INDEX if transparent else 0x00]) + b"\x00"
        descriptor = b"\x2C" + struct.pack("<HHHH", 0, 0, W, H) + b"\x00"
        parts.append(gce + descriptor + _lzw_stream(frame))
    parts.append(b"\x3B")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(b"".join(parts))


def verify_gif(path: Path, index_frames: list[np.ndarray], duration_ms: int, palette: list) -> None:
    """Round-trip proof: decode the file through Pillow's own GIF compositor.

    Pillow applies Graphic Control Extension semantics (disposal, transparency)
    while decoding, so comparing its rendered frames against the intended
    palette-mapped colours proves the optimised file is pixel-faithful —
    exactly what a browser or social crawler will paint.
    """
    gif = Image.open(path)
    assert gif.n_frames == len(index_frames), f"frame count {gif.n_frames}"
    assert gif.info.get("loop", 1) == 0, "loop-forever extension missing"
    pal = np.array(palette[:768], dtype=np.uint8).reshape(256, 3)
    delay_cs = max(2, round(duration_ms / 10))
    for i in range(gif.n_frames):
        gif.seek(i)
        assert gif.info.get("duration") == delay_cs * 10, f"frame {i} delay {gif.info.get('duration')}"
        rendered = np.asarray(gif.convert("RGB"), dtype=np.uint8)
        intended = pal[index_frames[i]]
        assert (rendered == intended).all(), f"frame {i} does not compose faithfully"
    print(f"verify: {gif.n_frames} frames render pixel-faithfully, loop=forever, {delay_cs * 10} ms/frame")


# --------------------------------------------------------------------------- #
# Verification — the synthesiser ships without human eyes, so it measures
# --------------------------------------------------------------------------- #

def qa(frames_rgb: list[np.ndarray], count: int) -> None:
    """Numeric QA — the synthesiser ships without human eyes, so it measures."""
    diffs = [
        np.abs(frames_rgb[(i + 1) % count].astype(np.int16) - frames_rgb[i]).mean()
        for i in range(count)
    ]
    seam = diffs[-1]  # last -> first: the loop point
    body = float(np.mean(diffs[:-1]))
    print(f"qa: mean inter-frame delta = {body:.2f}/255, loop seam = {seam:.2f}/255")
    assert 0.25 <= body <= 6.0, "motion amplitude outside the subtle-luxury envelope"
    assert seam <= body * 2.2 + 0.4, "loop seam is visible — effects are not wrapping cleanly"

    lum = frames_rgb[0] @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    lockup = lum[150:500, 60:500]
    assert lockup.max() >= 200, "wordmark ink is missing or too dim"
    peak = int(np.abs(frames_rgb[count // 2].astype(np.int16) - frames_rgb[0]).max())
    assert peak >= 28, f"sweep/bokeh too faint (peak delta {peak})"
    print(f"qa: wordmark ink peak = {lockup.max():.0f}/255, sweep peak delta = {peak}/255 — OK")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--base", type=Path, default=HERE / "base.png")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "assets" / "og-image-animated.gif")
    parser.add_argument("--frames", type=int, default=36)
    parser.add_argument("--duration-ms", type=int, default=80)
    args = parser.parse_args()

    static, meta = build_static(args.base)
    scene = analyse(static)
    static = bake_ambience(static, scene)
    parts = build_particles()
    win = y_window(H)

    # Contrast guard: the lockup column must sit on near-black.
    print(f"contrast: backdrop p95 luminance = {meta['backdrop_p95']:.1f} (target <= 62)")
    assert meta["backdrop_p95"] <= 62, "typographic zone is too bright — increase scrim"

    frames_rgb, fx_max = [], np.zeros((H, W, 3), np.float32)
    for index in range(args.frames):
        t = index / args.frames
        fx = fx_field(t, parts, meta, win)
        fx_max = np.maximum(fx_max, fx)
        frames_rgb.append(screen(static, fx))

    # Snap frames to a 3-level RGB lattice: sub-1.2% intensity drift — the
    # faint tails of the sweep and the softest bokeh edges — collapses to
    # identical pixels, so palette indices stop churning and the inter-frame
    # diff carries only deliberate motion. The sweep core, bright dust and
    # rule glint operate far above the lattice and survive untouched.
    lattice = RGB_LATTICE
    bucketed = [(f // lattice) * lattice for f in frames_rgb]
    bucketed_max = (screen(static, fx_max) // lattice) * lattice

    # Global palette from the maximum-intensity composite (zero palette flicker).
    palette_img = Image.fromarray(bucketed_max).quantize(colors=256, method=Image.MEDIANCUT)
    palette = palette_img.getpalette()

    # Index frames against the shared palette; free index 255 for transparency.
    indices = [np.array(Image.fromarray(b).quantize(palette=palette_img, dither=Image.Dither.NONE))
               for b in bucketed]
    indices = [np.where(idx == TRANSPARENT_INDEX, TRANSPARENT_INDEX - 1, idx) for idx in indices]

    out_frames: list[Image.Image] = []
    for position, idx in enumerate(indices):
        if position == 0:
            data = idx
        else:
            unchanged = np.all(bucketed[position] == bucketed[position - 1], axis=-1)
            data = np.where(unchanged, TRANSPARENT_INDEX, idx)
        frame = Image.fromarray(data.astype(np.uint8), mode="P")
        frame.putpalette(palette)
        out_frames.append(frame)

    encode_gif(out_frames, args.out, args.duration_ms)
    verify_gif(args.out, indices, args.duration_ms, palette)

    size = args.out.stat().st_size
    ms = args.frames * args.duration_ms
    print(f"encoded: {args.out}")
    print(f"  frames={args.frames}  frame={args.duration_ms}ms  loop={ms / 1000:.2f}s  size={size / 1024:.0f} KB")
    qa(frames_rgb, args.frames)
    return 0


if __name__ == "__main__":
    sys.exit(main())
