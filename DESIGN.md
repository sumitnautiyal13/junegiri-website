# Design — JuneGiri Farms

<!-- impeccable:design-schema 1 -->

The visual world is **Kaath** — the Garhwali carved-wood pahari house. It replaces the
previous navy/cyan "premium resort" skin (Poppins/Inter), which is now anti-reference.
Trust comes from craft and place: the hand-carved window frame (khyoli), the indigo-painted
shutter, the slate roof, and mud-ochre plaster. Mode: **Persuade**. Seed: `c17ab705`
(user-pinned direction; the carved-wood world was IMPECCABLE'S PICK, chosen over the
dice-assigned hill-travel-ephemera direction).

## Palette

Grounds are warm mud-plaster (never cream). Color commits at region scale.

| Token | Value | Role |
|---|---|---|
| `--plaster` | `#EBDFC6` | page ground (with faint warm grain) |
| `--plaster-2` | `#E2D2B0` | deeper alt-section ground |
| `--parchment` | `#F4ECD8` | lightest card ground |
| `--walnut` | `#2A2016` | headings / darkest ink |
| `--text` / `--text-light` | `#3C2F20` / `#5E4E38` | body / secondary (warm, never gray) |
| `--wood` / `--wood-soft` | `#6E4A2B` / `#8A6440` | carved-frame keylines |
| `--indigo` | `#283B6B` | Garhwali door indigo — primary brand; dark sections |
| `--indigo-deep` / `--indigo-bright` / `--indigo-soft` | `#1A2747` / `#3C538F` / `#DCE0EC` | |
| `--terracotta` | `#A23E1D` | clay/tile — **primary action** (AA on plaster + white) |
| `--terracotta-deep` / `--terracotta-soft` | `#7C2D13` / `#F1DFD3` | |
| `--marigold` / `--marigold-deep` | `#D4902A` / `#B0741A` | brass/haldi — stars, highlights, accents on dark |
| `--moss` | `#5D6A3A` | ringaal green — quiet secondary (checkmarks) |
| `--line` | `#D2BE98` | carved keyline on plaster |
| `--whatsapp` / `--whatsapp-dark` | `#13743C` / `#0E5A2E` | deep green (AA white-on-green) |

Legacy aliases are kept so all 28 pages re-skin from one file: `--green`/`--navy`→indigo,
`--orange`→terracotta, `--gold`→marigold, `--cream`→parchment, `--warm`→plaster,
`--ink`→walnut, `--border`→line.

## Type

- **Display** (`--font-display`): **Marcellus** (architectural carved-Roman caps) — `h1`, `h2`,
  prices, section titles, pull quotes, card headings. Single weight; scale carries hierarchy.
- **Body / UI** (`--font-body`): **Hind** (humanist, Devanagari-rooted, 300–700) — `h3`–`h6`,
  body, labels, controls.
- Loaded via `@import` at the top of `styles.css` (applies site-wide regardless of per-page links).

## Signature materials

- **Carved khyoli frame** (`.carved` + `2px solid var(--wood)` + inset double keyline + notched
  terracotta corners) on the booking panel, room/experience cards, OTA cards, mega-menu.
- **Indigo shutter-post**: a marigold vertical bar beside the hero lockup (`.cm-hero-lockup::before`).
- **Carved woven ledge**: `repeating-linear-gradient` terracotta↔marigold band under the page-hero
  and newsletter panel.
- **Carved section rule**: centered section titles carry a short terracotta rule with marigold
  caps (`.section-header .section-title::after`) in place of the (banned) kicker eyebrow — the
  `.kicker` class is globally suppressed.
- Plaster grain on `body` (layered low-opacity radial gradients).

## Components & depth

- Buttons are **wooden latch-press**: `0 3px 0` solid under-shadow, press-down `translateY(3px)`
  on `:active`. Radius 6px (squared, carved — not pills).
- Shadows are warm, wood-tinted, with real offset + contained blur (`--shadow*`); borders carry
  structure (2px wood), not soft halos.
- Browser surfaces themed: `::selection` marigold, focus-ring `--indigo-bright`, custom
  plaster/wood scrollbar.

## Motion

- One authored reveal: `.fade-up` rises + settles on a soft exponential ease (IntersectionObserver
  in `js/main.js`), plus the latch-press on buttons. Hero runs a 4-slide crossfade.
- Respects `prefers-reduced-motion`.

## Scope & provenance

Built and verified: the global system (`css/styles.css`) — which re-skins shared chrome across
all 28 pages — and the **homepage** (`index.html`, all ~20 sections) fully committed to the world.
Inner pages inherit the world through shared classes/tokens; pages with their own inline `<style>`
blocks still carry old-palette accents in page-specific sections and need a per-page polish pass.
All content (copy, hosts, rates, the WhatsApp booking flow, and the press/awards/OTA claims the
owner chose to keep) is preserved — this was a visual-world replacement, not a content rewrite.
No new rasters were generated; all imagery is the site's existing real photography/video.
