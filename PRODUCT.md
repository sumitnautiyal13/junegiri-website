# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: Indian leisure travellers — families, couples, and small friend-groups (largely metro/NCR, drive or train in) looking for a calm, nature-first base near Rishikesh rather than a transactional hotel. Many arrive around a purpose: a Char Dham Yatra start/rest point, a Himalayan trek, Rajaji wildlife, or simply unplugging at the forest edge. They evaluate on trust and feel (is this a real family place, is it safe, will we be looked after) and book conversationally over WhatsApp/phone, not through an OTA funnel.

## Product Purpose

JuneGiri Farms is a family-run farm house & homestay at the edge of Rajaji National Park near Rishikesh. It gives guests an unhurried stay in forest-edge rooms and cottages with home-cooked Pahadi meals, and acts as a trusted launch point for Char Dham Yatra, treks, Rajaji safaris, and Rishikesh adventure. Success = a guest trusts the family enough to message/call and book a stay, and feels hosted rather than processed.

## Positioning

A genuinely family-run homestay physically at the edge of Rajaji forest (not a branded hotel, not a party hostel): the hosts, the farm kitchen, and the forest setting are the product. The one thing a neighbouring property cannot truthfully copy is *this family and this exact forest-edge farm, running since 2020 with a 5.0★ reputation* — hospitality and place, not amenities.

## Operating Context

Static marketing site that leads to a WhatsApp/phone booking conversation (no live booking engine). Key surfaces: home, stay (overview) + three room pages, plan (rates/logistics), adventure, corporate retreats, blog/guides (Rishikesh travel content), about, gallery, FAQ, contact, plus a prepaid "Stay Pass" membership and policy pages. Built as hand-authored HTML through a Python build pipeline (`build.sh` → inline-partials, schema JSON-LD, analytics, sitemap, redirects, webp, asset-hash stamping); deployed on Cloudflare Pages. Edit source partials/body, never generated blocks.

## Capabilities and Constraints

- Static HTML/CSS/JS only — no server runtime, no booking backend; primary conversion is WhatsApp/call.
- Build pipeline is authoritative: partials in `partials/`, generated blocks (schema, analytics, sitemap, redirects, asset hashes) are produced by `tools/*.py` and must not be hand-edited.
- Cloudflare Pages: `_headers` (security/cache), `_redirects` (generated). HTML edge-cached ~300s.
- Yoga is intentionally out of scope — fully separated to junegiriyogretreats.com (`/retreat`, `/ttc` 301-redirect there). The redesign must not reintroduce yoga.
- Current fonts Poppins + Inter and the existing look are **anti-reference** for this redesign, not to be preserved.

## Brand Commitments

- Name: **JuneGiri Farms**. Emblem logo at `images/logo/junegiri-emblem.{png,webp}`.
- Voice: warm, grounded, first-person family host — plainspoken, specific, never luxury-hotel marketese or wellness-cliché.
- Real hosts (Geeta & Payal — `images/team/geeta-payal.*`); people-and-place are central, keep them visible.
- Operating since 2020; 5.0★ on Google (do not inflate or invent review counts/testimonials).

## Evidence on Hand

- Real photography: forest-edge hero (`images/surroundings/home-hero`, `mountain`, `waterfall`, `flower-walk`), rooms (`images/rooms/`), food (`images/food/`), guests, host portrait.
- Real video clips: `images/video/family.mp4`, `food.mp4`, `trek.mp4` (with posters).
- Real rates: rooms ₹2,500 / ₹3,500 / ₹4,000 per night (all-meals); packages ₹4,999 / ₹14,999 / ₹34,999; prepaid Stay Pass membership.
- Contact: +91 98738 97652 / WhatsApp. (Note: `contact.html` shows a placeholder +91 98765 43210 — a known dummy, not authoritative.)
- Absences to NOT fabricate: no named guest testimonials beyond what already exists in the repo, no awards, no star/amenity claims not already present.

## Product Principles

1. Trust before transaction — a real family, a real place; proof is photos, hosts, and plain facts, not adjectives.
2. Place is the hero — Rajaji forest edge and the Himalaya set the mood before any UI chrome.
3. Host, don't sell — copy and flow should feel like being welcomed, ending in a human WhatsApp conversation.
4. Earn the drive — give trip-planning substance (yatra, treks, safari, how-to-reach) so the stay is the obvious base.
5. Honest and light — fast static pages, no fake urgency, no invented social proof.

## Accessibility & Inclusion

General web accessibility (WCAG AA intent): legible contrast, keyboard-reachable nav and booking CTAs, real alt text on the photography, respects reduced-motion. No product-specific standard established beyond this.
