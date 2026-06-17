# CLAUDE.md — Makeup & Hair by Andreina

## Project Overview
Static portfolio/marketing website for Makeup & Hair by Andreina LLC — an on-location bridal hair & makeup artist serving the DFW area.

**Stack:** Vanilla HTML/CSS/JS — no build system, no framework.
**Deployment:** Vercel with custom domain `makeupandhairbyandreina.com`
**GitHub remote:** `https://github.com/pnerbun/makeupandhairbyandreinallc.git`

## Pages
| File | Purpose |
|---|---|
| `index.html` | Home |
| `services.html` | Services & Pricing |
| `gallery.html` | Photo Portfolio |
| `about.html` | About Andreina |
| `contact.html` | Book / Contact |

## Shared Assets
- `styles.css` — all styles (one file, linked from every page)
- `main.js` — fade-up observer + mobile nav toggle (linked from every page)
- `photos/` — client photos and Pexels placeholders (lowercase filenames only)

## Design System
| Token | Hex | Use |
|---|---|---|
| `--brand` | `#3B1A3A` | Deep plum — nav, footer, dark sections |
| `--blush` | `#F2DDD8` | Warm blush — alternating section backgrounds |
| `--gold` | `#C8A06A` | Warm gold — accent, dividers, hover |
| `--ink` | `#1E1218` | Near-black — body text |

**Fonts (Google Fonts CDN):**
- `Cormorant Garamond` — display headings (italic is key to the romantic feel)
- `Jost` — body, nav, labels

## Client Info
- **Name:** Andreina (last name [NEEDED])
- **Business:** Makeup & Hair by Andreina LLC
- **Phone:** 956-640-6220
- **Email:** wilsonandreina@yahoo.com
- **Instagram:** @makeupandhairbyandreinallc
- **TikTok:** @makeupandhairbyandreina
- **Location:** Rockwall, TX (DFW area) — home studio + travels to venues

## Services (from intake seed context)
1. Bridal hair & makeup — elegant, romantic, professional
2. Quinceañera hair & makeup — similar to bridal, softer pink
3. Photoshoot makeup — black-and-white, modern
4. Special events (any occasion)

## Photos Status
All `photos/` entries are currently Pexels placeholders (hosted via placehold.co URLs).
Replace placeholder `src` attributes with real client photos when received.
See `gallery.html` comments for which photos to swap where.

## Serving Locally
```bash
cd MakeupAndHairbyAndreina && python3 ../serve.py
# Opens at http://localhost:8765
```

## SEO
All pages comply with `on-page-seo.md`. Blog posts will need FAQ schema, Article schema, and author byline (see SEO standard).
Primary keyword: `bridal hair and makeup artist Dallas TX`
Secondary: `quinceañera makeup DFW`, `on-location makeup artist Dallas`
