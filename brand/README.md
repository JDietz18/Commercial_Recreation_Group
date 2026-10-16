# CRG Identity System — implementation

Code version of the Claude Design deck in `../project/CRG Identity System.dc.html`.
Open `index.html` for the style guide. It works straight from disk, no build step.

**Decisions locked in**
- Typography: pairing **A · Signage**, with Barlow Condensed for headings, Barlow for text and IBM Plex Mono for eyebrows and data.
- Dark mode is a full site theme. It follows the visitor's device setting, a toggle overrides it, and the choice is remembered on that device.

## Files

| Path | What it is |
|---|---|
| `css/crg-tokens.css` | All tokens as CSS variables: color ramps, light/dark theme values, fonts, fluid type scale, icon sizes. Load it first. |
| `css/crg-base.css` | Reusable pieces: `.crg-display/.crg-h1–h3/.crg-eyebrow/.crg-body-lg`, `.crg-btn--primary/--outline`, `.crg-icon`, `.crg-light-only/.crg-dark-only`, `.crg-photo-cut`, `.crg-scrim`. |
| `css/skin-crg.css` | Replaces Intera's `css/skin/skin-1.css`. Points Intera's variables and fonts at the CRG tokens. |
| `js/theme.js` | The light/dark toggle. Any element with `data-theme-toggle` becomes a toggle. |
| `icons/` | The Lucide icons used here (v0.460.0, ISC), plus `sprite.svg`. |
| `assets/logo/` | Logo lockups resized for web (color, reverse, white, black). |
| `assets/photos/` | Project photos resized to 1600px wide. |
| `css/styleguide.css`, `index.html` | The style guide page only. Not needed on the site. |

## Using it on a page

```html
<script>try{var t=localStorage.getItem('crg-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="css/crg-tokens.css">
<link rel="stylesheet" href="css/crg-base.css">
<script src="js/theme.js" defer></script>
```

Use the semantic tokens (`--crg-bg`, `--crg-surface`, `--crg-text`, `--crg-text-muted`,
`--crg-primary`, `--crg-primary-text`, `--crg-icon`, …) in components, not the raw ramp
values. That way components switch with the theme automatically.

Icons: `<svg class="crg-icon"><use href="icons/sprite.svg#i-school"/></svg>`. An external
sprite only works over http(s), so inline the sprite when testing from `file://`. To add
icons, copy them from `lucide-static@0.460.0`.

## Applying to Intera

1. Copy `css/crg-tokens.css` and `css/crg-base.css` into Intera's `css/`, and
   `css/skin-crg.css` into `css/skin/`. Load them in that order, in place of `skin-1.css`.
2. `skin-1.css` declares its color variables, but most rules hard-code the hex values,
   so swap those too:

   ```sh
   sed -i -e 's/#ffa200/#F25422/gI' -e 's/#ff6c00/#D2410C/gI' -e 's/#91ae1d/#68BE32/gI' \
          -e 's/#b056ff/#1E59CD/gI' -e 's/#a8ca1e/#F25422/gI' css/skin/skin-1.css
   ```

   `#ffa200` is used for both backgrounds and text. After the swap, review the `color:`
   rules and change orange text on light backgrounds to `#A82F00` (Orange 700).
3. Replace the Montserrat/Poppins and Open Sans/Roboto font links with the Barlow link above.
4. Replace Intera's four icon fonts with Lucide icons.

## Accessibility notes

- White on CRG Orange is 3.46:1, which passes WCAG AA for large text only. `.crg-btn`
  labels are 19px bold for that reason, so don't make them smaller. For small orange text
  on light backgrounds, use `--crg-primary-text` (#A82F00, 6.46:1 on Paper).
- Logos: full color only on white or Paper. Use reverse on Night or Charcoal, and all white
  on orange or on photos behind a 55% Night scrim (`.crg-scrim`).

## Open items

- Logos are raster PNGs made from the supplied files. Get vector (SVG) originals before launch.
- The "Who we serve" copy is reproduced word for word, including "that is need of", which
  probably should read "that is in need of".
- In the deck, the mark's minimum size reads "24px · 0.25in". This build treats that as
  24px **tall**.
