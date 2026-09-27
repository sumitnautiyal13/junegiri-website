#!/usr/bin/env python3
"""Stamp css/js links with a hash of the file they point at.

_headers serves /css/* and /js/* with `max-age=31536000, immutable`, which is
correct for versioned assets and dangerous for unversioned ones. The version
was a hand-typed date, `?v=2026052901`, last changed in May. Every CSS and JS
change since then reached new visitors only: anyone who had loaded the site
before kept the year-old copy their browser was told never to revalidate.

Hashing the file content removes the human step. The query string changes when
and only when the asset does, so returning visitors pick up a fix immediately
and still get a cold cache hit the rest of the time.

Run via ./build.sh. Idempotent.
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ("css/styles.css", "js/main.js")


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:10]


def main() -> int:
    stamps = {}
    for rel in ASSETS:
        p = ROOT / rel
        if not p.exists():
            print(f"  asset missing, skipped: {rel}")
            continue
        stamps[pathlib.PurePosixPath(rel).name] = digest(p)
    if not stamps:
        return 0

    # Matches href="…/styles.css?v=xxxx" and src="js/main.js" alike, with or
    # without an existing query string, at any relative or absolute depth.
    names = "|".join(re.escape(n) for n in stamps)
    pattern = re.compile(rf'((?:href|src)="[^"]*?({names}))(\?[^"]*)?(")')

    changed = 0
    for page in sorted(ROOT.glob("*.html")) + sorted((ROOT / "partials").glob("*.html")):
        src = page.read_text(encoding="utf-8")
        out = pattern.sub(lambda m: f"{m.group(1)}?v={stamps[m.group(2)]}{m.group(4)}", src)
        if out != src:
            page.write_text(out, encoding="utf-8")
            changed += 1

    listed = ", ".join(f"{n}={v}" for n, v in stamps.items())
    print(f"asset stamps: {listed}" + (f" — updated {changed} page(s)" if changed else " — all current"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
