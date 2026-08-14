#!/usr/bin/env python3
"""Normalise the heading outline on every page.

The audit found H2->H4 and H2->H5 jumps on 12 pages: card sub-headings were
picked by visual weight rather than depth, so the document outline skipped a
level. Search engines - and AI answer engines especially - read the heading
tree to decide which passage answers which question, so the gaps cost us.

This walks each page's headings in order and clamps any heading that sits more
than one level below its predecessor. It also reports the ancestor classes of
every element it changed, so the matching CSS descendant selectors can be
retargeted in the same pass (a demoted <h4> stops matching `.why-item h4`).

Run directly; it is idempotent. Not wired into build.sh because it rewrites
authored page bodies rather than generated regions.
"""
import pathlib
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
SKIP_FILE = {"brochure-print.html"}


class HeadingScanner(HTMLParser):
    """Collect every heading with its byte span and ancestor class list."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []          # [(tag, classes)]
        self.headings = []       # [{level, start, end, ancestors}]
        self._open = None
        self._mute = 0           # inside <script>/<style>

    def _pos(self):
        line, off = self.getpos()
        return self.line_starts[line - 1] + off

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._mute += 1
            return
        if tag in VOID:
            return
        classes = ""
        for k, v in attrs:
            if k == "class":
                classes = v or ""
        self.stack.append((tag, classes))
        if self._mute == 0 and re.fullmatch(r"h[1-6]", tag):
            self._open = {
                "level": int(tag[1]),
                "start": self._pos(),
                # ancestors excluding the heading itself
                "ancestors": [c for _, c in self.stack[:-1] if c],
            }

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._mute = max(0, self._mute - 1)
            return
        if tag in VOID:
            return
        if self._open and re.fullmatch(r"h[1-6]", tag) and self._open["level"] == int(tag[1]):
            self._open["end"] = self._pos() + len(f"</{tag}>")
            self.headings.append(self._open)
            self._open = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def scan(html):
    p = HeadingScanner()
    p.line_starts = [0]
    for line in html.splitlines(keepends=True):
        p.line_starts.append(p.line_starts[-1] + len(line))
    p.feed(html)
    return p.headings


def target_levels(headings):
    """Re-level the outline so depth is contiguous and siblings agree.

    Keeps a stack of the *original* levels representing the current ancestry.
    A heading's new level is its depth in that stack, so a run of sibling cards
    that all started as <h5> all land on the same new level - which a simple
    "clamp to previous + 1" pass gets wrong, splitting the first card off from
    the rest.
    """
    out = []
    stack = []
    for h in headings:
        lvl = h["level"]
        while stack and stack[-1] >= lvl:
            stack.pop()
        out.append(len(stack) + 1)
        stack.append(lvl)
    return out


def main():
    changed_pages = 0
    total = 0
    css_moves = defaultdict(set)   # (ancestor_class, old_tag) -> {new_tag}

    for path in sorted(ROOT.glob("*.html")):
        if path.name in SKIP_FILE:
            continue
        html = path.read_text(encoding="utf-8")
        heads = scan(html)
        if not heads:
            continue
        targets = target_levels(heads)
        edits = [(h, t) for h, t in zip(heads, targets) if h["level"] != t]
        if not edits:
            continue

        # Rewrite back-to-front so earlier spans keep their offsets.
        for h, new in sorted(edits, key=lambda x: -x[0]["start"]):
            old = h["level"]
            frag = html[h["start"]:h["end"]]
            frag = re.sub(rf"^<h{old}\b", f"<h{new}", frag)
            frag = re.sub(rf"</h{old}>$", f"</h{new}>", frag)
            html = html[:h["start"]] + frag + html[h["end"]:]
            for cls in h["ancestors"]:
                for token in cls.split():
                    css_moves[(token, f"h{old}")].add(f"h{new}")
            total += 1

        path.write_text(html, encoding="utf-8")
        changed_pages += 1
        print(f"  {path.name}: {len(edits)} heading(s) re-levelled")

    print(f"\nheadings: {total} changed across {changed_pages} page(s)")
    if css_moves:
        print("\nCSS descendant selectors that may need retargeting:")
        for (cls, old), news in sorted(css_moves.items()):
            print(f"  .{cls} {old}  ->  .{cls} {'/'.join(sorted(news))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
