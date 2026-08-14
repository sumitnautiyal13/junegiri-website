#!/usr/bin/env python3
"""Point the pages at the WebP renditions, keeping the JPEG/PNG as fallback.

tools/optimise-images.py writes a .webp beside every raster source. Nothing
uses them until the markup asks for them, which is what this does:

  inline CSS backgrounds -> a plain url() declaration followed by an
      image-set() declaration. Browsers that do not understand image-set keep
      the first declaration and still get an image; everything else takes the
      WebP. Emitting only image-set() would leave old browsers with no
      background at all, which is why the fallback line stays.

  <img> -> wrapped in <picture> with a WebP <source>. The <img> keeps its src,
      alt and dimensions, so nothing changes for a client without WebP.

  <link rel=preload as=image> -> repointed at the WebP, since that is what a
      modern browser will actually fetch.

  og:image / twitter:image -> left on JPEG on purpose. Social and chat
      scrapers are the one place where WebP support is still patchy.

Only rewrites a reference when the .webp file exists. Idempotent.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Trailing ?query / #fragment is kept: some URLs carry a ?v= cache-buster, and
# dropping it would re-serve a stale cached copy.
RASTER = re.compile(r"^(?P<path>[^'\"?#]+)\.(?P<ext>jpg|jpeg|png)(?P<qs>[?#][^'\"]*)?$", re.I)


def webp_exists(url: str) -> str | None:
    """Return the .webp URL if the file is on disk, else None."""
    m = RASTER.match(url.strip())
    if not m:
        return None
    rel = m.group("path").lstrip("/")
    if not (ROOT / rel).with_suffix(".webp").exists():
        return None
    return m.group("path") + ".webp" + (m.group("qs") or "")


def rewrite_backgrounds(html: str, stats: dict) -> str:
    # A plain url() declaration that is NOT already followed by its image-set
    # partner. The negative lookahead is what makes this idempotent - without
    # it, a second run appends another image-set to every background.
    pattern = re.compile(
        r"background-image:\s*url\((?P<q>['\"]?)(?P<url>[^'\")]+)(?P=q)\)"
        r"(?!\s*;\s*background-image:\s*image-set)")

    def repl(m):
        url = m.group("url")
        webp = webp_exists(url)
        if not webp:
            return m.group(0)
        stats["bg"] += 1
        return (f"background-image:url('{url}');"
                f"background-image:image-set(url('{webp}') type('image/webp'),"
                f"url('{url}') type('image/jpeg'))")

    html = pattern.sub(repl, html)

    # The `background:` shorthand needs different handling: leave the shorthand
    # intact (it also carries position/size/repeat) and append a background-image
    # longhand after it, which overrides just the image layer.
    #
    # The "already migrated?" test is done on the text *after* the match rather
    # than with a trailing negative lookahead. A lookahead here sits behind a
    # greedy group, so the engine backtracks until the lookahead passes and the
    # insertion lands mid-token ("no-repe" + inserted css + "at").
    short = re.compile(
        r"background:\s*url\((?P<q>['\"]?)(?P<url>[^'\")]+)(?P=q)\)(?P<rest>[^;\"]*)")

    def repl_short(m):
        url = m.group("url")
        webp = webp_exists(url)
        if not webp:
            return m.group(0)
        tail = html[m.end():m.end() + 40]
        if re.match(r"\s*;\s*background-image:\s*image-set", tail):
            return m.group(0)          # already migrated
        stats["bg"] += 1
        return (m.group(0) + f";background-image:image-set(url('{webp}') type('image/webp'),"
                             f"url('{url}') type('image/jpeg'))")

    return short.sub(repl_short, html)


def rewrite_imgs(html: str, stats: dict) -> str:
    def repl(m):
        tag = m.group(0)
        src = m.group("src")
        webp = webp_exists(src)
        if not webp:
            return tag
        stats["img"] += 1
        return (f'<picture><source srcset="{webp}" type="image/webp">{tag}</picture>')

    # Don't re-wrap an <img> that already sits inside a <picture>.
    parts = re.split(r"(<picture>.*?</picture>)", html, flags=re.S)
    for i, part in enumerate(parts):
        if part.startswith("<picture>"):
            continue
        parts[i] = re.sub(r'<img\b[^>]*\bsrc="(?P<src>[^"]+)"[^>]*>', repl, part)
    return "".join(parts)


def rewrite_posters(html: str, stats: dict) -> str:
    """<video poster>. No fallback needed: any browser that plays the video
    also decodes WebP, and a poster that fails to load is a blank frame, not a
    broken layout."""
    def repl(m):
        webp = webp_exists(m.group("src"))
        if not webp:
            return m.group(0)
        stats["poster"] += 1
        return m.group(0).replace(m.group("src"), webp)
    return re.sub(r'poster="(?P<src>[^"]+)"', repl, html)


def rewrite_preloads(html: str, stats: dict) -> str:
    def repl(m):
        tag, href = m.group(0), m.group("href")
        webp = webp_exists(href)
        if not webp:
            return tag
        stats["preload"] += 1
        return tag.replace(href, webp).replace("as=\"image\"", "as=\"image\" type=\"image/webp\"", 1) \
            if 'type="image/webp"' not in tag else tag.replace(href, webp)

    return re.sub(r'<link\b[^>]*rel="preload"[^>]*\bhref="(?P<href>[^"]+)"[^>]*>', repl, html)


def main():
    stats = {"bg": 0, "img": 0, "preload": 0, "poster": 0}
    touched = 0
    # partials/ must be migrated too: build.sh inlines them into every page, so
    # a partial left on JPEG silently undoes this on the next build.
    targets = sorted(ROOT.glob("*.html")) + sorted((ROOT / "partials").glob("*.html"))
    for path in targets:
        src = path.read_text(encoding="utf-8")
        out = rewrite_posters(rewrite_preloads(rewrite_imgs(rewrite_backgrounds(src, stats), stats), stats), stats)
        if out != src:
            path.write_text(out, encoding="utf-8")
            touched += 1

    css = ROOT / "css" / "styles.css"
    text = css.read_text(encoding="utf-8")
    new = rewrite_backgrounds(text, stats)
    if new != text:
        css.write_text(new, encoding="utf-8")

    print(f"webp refs: {stats['bg']} backgrounds, {stats['img']} <img>, "
          f"{stats['preload']} preloads, {stats['poster']} posters across {touched} file(s)")
    print("og:image / twitter:image intentionally left on JPEG for scrapers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
