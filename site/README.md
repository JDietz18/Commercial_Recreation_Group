# CRG website

The CRG Commercial Recreation Group website, built on the Intera HTML template with
the CRG identity system (`../brand/`). Plain static HTML, CSS and JS, plus one PHP file
for the quote form.

| Page | File |
|---|---|
| Home | `index.html` |
| Products | `products.html` |
| Projects | `projects.html` |
| About | `about.html` |
| Request a quote | `contact.html` |

## Run it locally

```sh
cd site
php -S localhost:8000      # then open http://localhost:8000
```

Opening the HTML files straight from disk also works, but the quote form needs PHP.

## Deploy

Upload the contents of `site/` to any host with PHP 7.4+ and a working `mail()`
(most shared hosting, e.g. cPanel). Without PHP the pages still work; only the form fails.

## Before launch

1. **Quote form.** In `script/quote.php`, set `CRG_QUOTE_TO` (CRG's inbox) and `CRG_QUOTE_FROM`
   (an address on CRG's own domain, so mail isn't marked as spam). The form has a hidden
   honeypot field against spam bots. For stronger protection, add a Google reCAPTCHA v2
   secret to `CRG_RECAPTCHA_SECRET`, then add the widget to `contact.html`:
   `<div class="g-recaptcha" data-sitekey="…"></div>` plus
   `<script src="https://www.google.com/recaptcha/api.js" async defer></script>`.
2. **Draft copy.** Add `?draft` to any page URL (e.g. `index.html?draft`) to outline every
   piece of placeholder text in blue. That covers:
   - phone, email, address and hours (header CTA band, footer, contact page)
   - social links in the footer
   - project titles (they describe the photos, not real project names or locations)
   - product, process and values descriptions
   - the About story, including the bracketed note to add CRG's history and manufacturers
3. **Copy check.** The "Who we serve" statement is CRG's own wording, word for word,
   including "that is need of", which probably should be "that is in need of".
4. **Logos.** These are raster PNGs. Swap in SVG versions when CRG supplies vector files.
5. **Photos.** The six photos are product renders. Add real project photos to
   `images/photos/` and to the grid in `projects.html` as installs are documented.

## How it's put together

Load order in every page's `<head>`:

| File | Role |
|---|---|
| `css/crg-tokens.css` | CRG colors, type scale and light/dark theme values (from `brand/`) |
| `css/vendor.css` | Bootstrap 4, animate, Magnific Popup, scrollbar (Intera's plugins, trimmed) |
| `css/style.css`, `css/templete.css` | Intera's stylesheets, with its colors and fonts swapped for CRG tokens |
| `css/skin/skin-crg-base.css` | Intera's `skin-1.css`, recolored |
| `css/skin/skin-crg.css` | Maps Intera's CSS variables and headings to CRG (from `brand/`) |
| `css/crg-base.css` | CRG type, buttons, icons and theme-aware logos (from `brand/`) |
| `css/crg-site.css` | Site layout and CRG components, including dark mode for Intera's parts |

Scripts: `js/combining.js` (Intera's jQuery bundle: Bootstrap, sticky header, mobile
menu, masonry filter, lightbox, back-to-top), `js/theme.js` (light/dark toggle),
`js/crg-site.js` (filter state, `?draft`), and `js/quote-form.js` on the contact page.

### Changes made to Intera

- The bundle injected the template vendor's "Buy Now" and "Support" buttons and the
  AddThis tracking script into every page. Both are removed from `js/combining.js`.
- `bootstrap-select` now only enhances selects that have the `selectpicker` class, so
  the quote form keeps native, accessible dropdowns.
- The old Google Fonts import (Montserrat, Poppins, Open Sans, Oswald, Roboto) and the
  four icon fonts are no longer loaded. Icons are inline Lucide SVGs (ISC license).
  Revolution Slider, the Maps API and unused plugins were left out.
- `script/contact.php` and `mailchamp.php` are replaced by `script/quote.php`. It
  validates input, escapes it in the email, uses a fixed From address with Reply-To set
  to the visitor, and makes reCAPTCHA optional.

### Editing pages

The header, footer and icon sprite are repeated in each of the five HTML files.
A navigation or footer change has to be made in all five.
