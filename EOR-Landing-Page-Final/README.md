# Paybooks Employer of Record landing page (final)

Sample landing page built for the TransPerfect Paybooks SEO proposal. Locked on 24 September 2026.

- **Live preview:** https://claude.ai/artifact/FF9f1hPNrvvjUmK8tbAMxp (Version 79)
- **Open locally:** `index.html` (needs the `assets/` folder next to it)

## What is in this folder

| Path | What it is |
|---|---|
| `index.html` | The finished page |
| `assets/pb.css` | Stylesheet |
| `assets/mark.png` | Paybooks leaf mark |
| `assets/logos-t/` | 23 client logos with transparent backgrounds (City Union Bank is left out of the strip) |
| `_source/` | Generator: `eor_page.py` (copy), `render_eor.py` (layout), `build.py`, and the stylesheet |
| `design-options/logo-strip-options/` | The logo strip comparison page (options C, F to K) |

## Page structure

Hero with video holder, trust strip, then nine chapters: fit table, offer letter, who does what, compliance clause, cost calculator (USD, ₹95.7 per $1 as of 23 Sep 2026), provider comparison, exits, working with us, timeline, then FAQ and the closing banner.

## Still to confirm with Paybooks before going live

- Family health cover on the offer letter
- Guarantee clause wording
- The 2-minute EOR walkthrough video (holder only)
- Competitor fees in the comparison table (checked 23 Sep 2026)

## Rebuilding

The generator lives in the session build tree. To edit, change `eor_page.py` (copy) or `render_eor.py` (layout), then run `python3 build.py standalone`.
