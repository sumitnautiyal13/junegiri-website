# JuneGiri Farms — Website

The official website for **JuneGiri Farms Pvt. Ltd.** — a family-run resort, yoga retreat & yatra operator at the edge of Rajaji National Park, Rishikesh.

🌐 **Live:** [junegiriyatra.com](https://junegiriyatra.com)
📱 **Bookings:** WhatsApp [+91 98738 97652](https://wa.me/919873897652)

---

## Stack

- **Pure HTML / CSS / JavaScript** — no framework, no build step
- **Cloudflare Pages** — hosting + global edge CDN
- **Partials system** — shared header/footer loaded via `fetch()` from `/partials/`

## Structure

```
/
├── index.html              # Home (resort + yatra + retreats)
├── stay.html               # Rooms overview
├── room-jungle.html        # Jungle View Room detail
├── room-river.html         # River Cottage detail
├── room-farm.html          # Farm Stay Suite detail
├── retreat.html            # Reset Retreat (Meta-ads LP)
├── yatra.html              # Char Dham + Yatra packages
├── treks.html              # Himalayan treks
├── adventure.html          # Rishikesh adventures
├── corporate.html          # Corporate offsites
├── ttc.html                # 200-hr Yoga TTC
├── membership.html         # JuneGiri Circle
├── about.html              # Founders + story
├── sustainability.html     # Eco commitments
├── press.html              # Press & awards
├── faq.html                # FAQ
├── gallery.html            # Photo gallery
├── blog.html               # Journal listing
├── contact.html            # Contact form
├── privacy.html            # Privacy Policy
├── terms.html              # Terms & Conditions
├── cancellation.html       # Cancellation & Refund
├── partials/
│   ├── header.html         # Shared nav (mega-menu)
│   └── footer.html         # Shared footer
├── css/
│   └── styles.css          # Global styles
├── js/
│   └── main.js             # Partial loading + nav + animations
├── favicon.svg
├── _headers                # Cloudflare Pages cache + security headers
└── _redirects              # Cloudflare Pages redirect rules
```

## Local development

Static site — just open `index.html` in a browser, or serve with any static server:

```bash
python3 -m http.server 8000
# → http://localhost:8000
```

## Deployment

Pushed to `main` → Cloudflare Pages auto-deploys.

## Conventions

- **WhatsApp-first**: every CTA opens `wa.me/919873897652` with prefilled context
- **Cache busting**: bump `?v=YYYYMMDDNN` on `styles.css` and `main.js` references in all HTML when those files change
- **Partials**: don't duplicate nav/footer — edit `/partials/header.html` or `/partials/footer.html`, all pages update

## Brand palette

- Navy `#0F4C75` · Cyan `#00A8E8` · Gold `#F0A500` · WhatsApp `#25D366`
- Fonts: Poppins (headings) + Inter (body)
