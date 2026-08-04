#!/usr/bin/env python3
"""Regenerate sitemap.xml from the pages that actually exist.

The hand-maintained sitemap had drifted: /plan and /stay-pass were live and
linked from the nav but missing entirely, and every lastmod was frozen at
2026-05-23 while the pages had moved on. This reads the directory and takes
lastmod from each file's last git commit, so it can't drift again.

Run via ./build.sh.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://junegirifarms.com"

# Excluded from the deploy via .assetsignore, so it must stay out of the sitemap.
SKIP = {"brochure-print.html", "payment.html"}  # payment: noindex transactional page, not for search

# changefreq + priority per page. Anything not listed falls back to DEFAULT.
RULES = {
    "index": ("weekly", "1.0"),
    "plan": ("weekly", "0.9"),
    "stay": ("weekly", "0.9"),
    "retreat": ("weekly", "0.9"),
    "yatra": ("weekly", "0.9"),
    "stay-pass": ("monthly", "0.8"),
    "treks": ("monthly", "0.8"),
    "adventure": ("monthly", "0.8"),
    "membership": ("monthly", "0.8"),
    "room-jungle": ("monthly", "0.8"),
    "room-river": ("monthly", "0.8"),
    "room-farm": ("monthly", "0.8"),
    "blog": ("weekly", "0.7"),
    "corporate": ("monthly", "0.7"),
    "gallery": ("monthly", "0.7"),
    "about": ("monthly", "0.7"),
    "faq": ("monthly", "0.7"),
    "ttc": ("monthly", "0.6"),
    "sustainability": ("monthly", "0.6"),
    "press": ("monthly", "0.6"),
    "contact": ("yearly", "0.6"),
    "cancellation": ("yearly", "0.4"),
    "privacy": ("yearly", "0.3"),
    "terms": ("yearly", "0.3"),
}
DEFAULT = ("monthly", "0.5")


def last_modified(path: pathlib.Path) -> str:
    """Date of the file's last commit; falls back to mtime if untracked."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", path.name],
        cwd=ROOT, capture_output=True, text=True,
    )
    stamp = result.stdout.strip()
    if stamp:
        return stamp
    import datetime
    return datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()


def main():
    pages = sorted(p for p in ROOT.glob("*.html") if p.name not in SKIP)
    # Sitemap order follows priority, highest first, so it reads sensibly.
    pages.sort(key=lambda p: (-float(RULES.get(p.stem, DEFAULT)[1]), p.stem))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page in pages:
        loc = f"{BASE}/" if page.stem == "index" else f"{BASE}/{page.stem}"
        freq, priority = RULES.get(page.stem, DEFAULT)
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{last_modified(page)}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ]
    lines += ["</urlset>", ""]

    (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
    print(f"sitemap.xml: {len(pages)} URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
