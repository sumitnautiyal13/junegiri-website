#!/usr/bin/env python3
"""Convert the JPEG/PNG library to WebP and cap absurd source dimensions.

The audit measured the homepage at 3.5 MB of transfer and 29 s to finish
loading, with individual background JPEGs at 492/450/429 KB. The whole
/images tree was 35 MB across 58 JPEGs with zero WebP.

This writes a .webp next to every raster source. It does not delete the
originals: they stay as the fallback for the small share of clients that
still cannot read WebP, and as the editable master.

Sources are also downscaled to MAX_EDGE first. Several were far larger than
any slot that displays them - a 44x44 logo shipping as an 82 KB PNG, heroes at
several times their rendered width - so resizing does most of the work and
the codec change does the rest.

Idempotent: skips a target that is newer than its source. Run directly, or
via ./build.sh --images.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"

QUALITY = 80
RETINA = 2               # serve 2x the CSS width so it stays crisp on retina
HARD_CAP = 1600          # beyond this the bytes cost more than the sharpness
FALLBACK_EDGE = 1200     # for anything not in the measured manifest
SUFFIXES = {".jpg", ".jpeg", ".png"}

# Max CSS width each image is actually displayed at, measured in a real browser.
# Recoding alone only bought 40%: the sources are 1400-1600px while most gallery
# tiles render at 281px. Sizing to the slot is where the bytes actually go.
MANIFEST = json.loads((ROOT / "tools" / "image-render-widths.json").read_text(encoding="utf-8"))


def target_edge(path: pathlib.Path) -> int:
    key = path.relative_to(IMAGES).with_suffix("").as_posix()
    css_w = MANIFEST.get(key)
    if css_w is None:
        return FALLBACK_EDGE
    return min(HARD_CAP, int(math.ceil(css_w * RETINA / 50.0) * 50))


def convert(path: pathlib.Path) -> tuple[int, int] | None:
    out = path.with_suffix(".webp")
    if out.exists() and out.stat().st_mtime >= path.stat().st_mtime:
        return None
    before = path.stat().st_size
    im = Image.open(path)
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") and path.suffix == ".png" else "RGB")
    edge = target_edge(path)
    if max(im.size) > edge:
        im.thumbnail((edge, edge), Image.LANCZOS)
    im.save(out, "WEBP", quality=QUALITY, method=6)
    return before, out.stat().st_size


# The nav mega-menu renders these at 44x44 but shares the files with full-width
# heroes, so every page was pulling ~1.2 MB of imagery to paint seven thumbnails.
# They get their own tiny renditions instead.
NAV_THUMBS = [
    "rooms/1", "rooms/5", "rooms/10",
    "surroundings/7", "surroundings/9", "surroundings/15", "surroundings/home-hero",
]
THUMB_EDGE = 128         # 44px slot at up to 3x


def build_thumbs():
    out_dir = IMAGES / "thumbs"
    out_dir.mkdir(exist_ok=True)
    total = 0
    for key in NAV_THUMBS:
        src = next((IMAGES / f"{key}{e}" for e in (".jpg", ".jpeg", ".png")
                    if (IMAGES / f"{key}{e}").exists()), None)
        if src is None:
            print(f"  thumb source missing: {key}")
            continue
        out = out_dir / (key.replace("/", "-") + ".webp")
        if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
            total += out.stat().st_size
            continue
        im = Image.open(src).convert("RGB")
        im.thumbnail((THUMB_EDGE, THUMB_EDGE), Image.LANCZOS)
        im.save(out, "WEBP", quality=82, method=6)
        total += out.stat().st_size
    print(f"nav thumbs: {len(NAV_THUMBS)} at {THUMB_EDGE}px, {total/1024:.0f} KB total")


def main():
    if not IMAGES.exists():
        print("no images/ directory")
        return 1
    srcs = sorted(p for p in IMAGES.rglob("*") if p.suffix.lower() in SUFFIXES)
    tb = ta = n = 0
    for p in srcs:
        r = convert(p)
        if r is None:
            continue
        b, a = r
        tb += b
        ta += a
        n += 1
    skipped = len(srcs) - n
    if n:
        print(f"images: {n} converted to WebP "
              f"({tb/1_048_576:.1f} MB -> {ta/1_048_576:.1f} MB, "
              f"-{100 - ta * 100 // tb}%)"
              + (f", {skipped} already current" if skipped else ""))
    else:
        print(f"images: all {len(srcs)} WebP files already current")
    build_thumbs()
    return 0


if __name__ == "__main__":
    sys.exit(main())
