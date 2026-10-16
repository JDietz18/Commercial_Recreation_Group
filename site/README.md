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
| 25 case studies | `case-studies/<project>.html` |

## Run it locally

```sh
cd site
php -S localhost:8000      # then open http://localhost:8000
```

Opening the HTML files straight from disk also works, but the quote form needs PHP.

## Deploy

Upload the contents of `site/` to any host with PHP 7.4+ and a working `mail()`
(most shared hosting, e.g. cPanel). The quote form then emails info@CRGplay.com directly.

On static hosting without PHP (such as the GitHub Pages preview), or if sending fails,
the form keeps everything the visitor typed. It offers an **Email this request** button
(a pre-filled email to info@CRGplay.com) and a **Call (317) 776-7830** button instead, so
no lead is lost.

## Content

All copy uses CRG's real information, taken from crgplay.com in October 2026 and confirmed
by CRG where noted:

- phone, email, address, hours and social links
- company history, leadership team and the 25 years of experience (confirmed by CRG; the
  company changed ownership in 2020)
- the Playcraft Systems partnership, product lines, certifications and Navitas financing
- client testimonials
- the 25 case studies (see "Case studies" below)

## Before launch

1. **Quote form.** `script/quote.php` delivers to `info@CRGplay.com`. Set `CRG_QUOTE_FROM`
   to a real address on CRG's mail domain (it's currently `website@crgplay.com`), or mail
   may land in spam. For stronger spam protection, add a Google reCAPTCHA v2 secret to
   `CRG_RECAPTCHA_SECRET`, then add the widget to `contact.html`:
   `<div class="g-recaptcha" data-sitekey="…"></div>` plus
   `<script src="https://www.google.com/recaptcha/api.js" async defer></script>`.
2. **Project names.** Five gallery photos are renders whose real project names aren't known
   yet. They have descriptive titles marked `data-draft`; add `?draft` to a URL to outline
   them. The Possibility Playground at Hayswood Nature Reserve is confirmed.
3. **Copy check.** The "Who we serve" statement is CRG's own wording, word for word,
   including "that is need of", which probably should be "that is in need of".
4. **Photos.** Add real installation photos to `images/photos/` and the gallery as projects
   are documented (see "Adding photos" below).
5. **Case-study photos. Do this before crgplay.com's WordPress site is switched off.** The old
   site holds about 320 project photos. Run `python3 tools/site-builder/fetch_case_photos.py` to
   save them (see "Case studies" below).
6. **Case-study copy.** Review the edits to CRG's case-study text listed under "Case studies".

## Search engines and launch

The site is set up for **https://crgplay.com/** (replacing CRG's current WordPress site):

- **Every page:** a canonical URL, share-preview tags (`images/og-image.jpg`, 1200×630) and
  structured data describing CRG as a LocalBusiness (address, phone, email, hours, Indiana
  service area, social profiles). Inner pages also carry breadcrumbs.
- **`sitemap.xml` and `robots.txt`** point search engines at the five pages and the 25 case studies.
- **`.htaccess`** (Apache, CRG's PHP host):
  - permanent (301) redirects for all 64 addresses of the old WordPress site, each to its
    closest new page; product pages go to their section, e.g. `/dog-parks/` →
    `/products.html#dog-parks`, and each old case study (including its photo pages) goes to
    its new page, e.g. `/case-studies/burris-backyard/` → `/case-studies/burris-laboratory-school.html`
  - a custom 404 page
  - compression and caching
  - blocks web access to the reCAPTCHA library's files
- **`404.html`:** branded, `noindex`, with links back to Products, Projects and Contact.
- **The GitHub Pages preview is `noindex`.** The deploy workflow adds the tag to the preview
  copy only, so it never competes with crgplay.com in search results.

At launch:
1. Upload `site/` (including the hidden `.htaccess`) to the crgplay.com web root.
2. Spot-check a few old addresses, e.g. `/about/`, `/play-systems/`, `/case-studies/cool-creek-park/`.
3. In Google Search Console and Bing Webmaster Tools, submit `https://crgplay.com/sitemap.xml`.
4. Check that the Google Business Profile shows the same address, phone and hours.

If the domain ever changes, update `SITE_URL` in `tools/site-builder/build.py` and rebuild.

## Case studies

`case-studies/` has a page for each of the 25 case studies on the old site (the 18 on its
Case Studies page plus the 7 under "More case studies"). The Projects page lists them as cards.
Each page has:
- the project facts as a drawing title block: location, ages, completion, budget
- CRG's write-up and the client's quote
- the project videos, which load from Vimeo or YouTube only when a visitor presses play
- a quote request, and links to the previous and next case study

Content is in `tools/site-builder/case_studies.json`. It was copied from crgplay.com in October 2026.

**Photos.** Nine case studies have a hero photo, cropped from the old site's pages. They are in
`images/case-studies/`. The other 16 show a drafting-sheet placeholder until they get one. The old
site also has a gallery for most projects, about 320 photos in all. They couldn't be downloaded
from this build environment. Save them before the WordPress site goes away:

```sh
python3 tools/site-builder/fetch_case_photos.py     # needs internet; ImageMagick recommended
cd tools/site-builder && npm run build
```

The script saves each gallery to `images/case-studies/<project>/`. With ImageMagick, it also
resizes the photos, makes thumbnails, and uses the first photo as the hero where there isn't
one. The build then adds a photo gallery with a lightbox to each page.

**Not carried over:** The Play School at Legacy's time-lapse is a video file on the old site
(`wp-content/uploads/images/Playground-Timelapse.mp4`). Upload it to Vimeo or YouTube, then
add it to the page's `videos` in `case_studies.json`.

**Edits to CRG's copy.** These are for CRG to review.
- **Client quotes:** kept word for word, except that the old company name (Recreation
  Unlimited) is shown as "[Commercial Recreation Group]".
- **CRG's own text:**
  - The old name is changed to CRG.
  - Clear typos are fixed: "Student Counsel", "it’s toll", "tic-tac-tow", "temperatures rises",
    "We’d like thank", "include line of", "standard belts seat".
  - "Elletsville" is spelled Ellettsville.
  - "poured-in-place" is used consistently.
  - Foot and inch marks (′ ″) are written ' and ", because the site's font doesn't have the
    prime characters.
  - "The Possibilities Playground" is changed to "Possibility Playground".
  - Links to the old site now point to the new pages.
  - The mention of recunlimited.com is removed.
  - Two sentences that refer to the missing time-lapse video are removed.
- **Yorktown Elementary:**
  - The old page's location said Westfield, IN; it now says Yorktown, IN.
  - "The structure provides the perfect backdrop to the stadium" is removed. It was copied from
    the Kokomo page, and Yorktown has no stadium.
- **Meridian Health Services:** the quote had no name, so it's attributed to the organization.
- **Home Gym:** the first item of the equipment list was split across two bullets on the old
  page; it's one item now.

## Adding photos

Pages serve each photo as responsive WebP (640/960/1280/1600px wide) with the JPEG as a
fallback and as the lightbox image. For a new `images/photos/<name>.jpg` (about 1600px wide),
create the variants with ImageMagick:

```sh
cd site/images/photos
for w in 640 960 1280 1600; do
  convert <name>.jpg -resize ${w}x -strip -quality 72 -define webp:method=6 <name>-$w.webp
done
```

Then reference it like the existing photos: a `<picture>` with a WebP `srcset` and a `sizes`
value that matches its layout slot.

## How it's put together

Load order in every page's `<head>`:

| File | Role |
|---|---|
| `css/crg-tokens.css` | CRG colors, type scale and light/dark theme values (from `brand/`) |
| `css/intera.css` | Intera's CSS (Bootstrap 4, Magnific Popup, its stylesheets and recolored skin), trimmed to the rules the site uses. Generated; see "Trimmed template CSS" |
| `css/skin/skin-crg.css` | Maps Intera's CSS variables and headings to CRG (from `brand/`) |
| `css/crg-base.css` | CRG type, buttons, icons and theme-aware logos (from `brand/`) |
| `css/crg-site.css` | Site layout and CRG components, including dark mode for Intera's parts |
| `css/crg-motion.css` | Animations and transitions (paired with `js/crg-motion.js`) |
| `css/crg-blueprint.css` | Blueprint background, animated header logo, site-wide pause button |

Scripts: `js/combining.js` (Intera's jQuery bundle: Bootstrap, sticky header, mobile
menu, masonry filter, lightbox, back-to-top), `js/theme.js` (light/dark toggle),
`js/crg-site.js` (filter state, `?draft`, click-to-play videos), `js/crg-motion.js` (motion layer, below),
`js/crg-blueprint.js` (blueprint drawings), and
`js/quote-form.js` on the contact page.

### Motion

`js/crg-motion.js` and `css/crg-motion.css` add:

- **Hero:** headline rises in word by word, the photo wipes in on its diagonal cut, and a
  crossfading slideshow of four photos with a slow zoom. Dots and a pause button sit on the photo.
- **Audience strip:** becomes a marquee that pauses on hover or focus.
- **"Who we serve":** the statement lights up word by word as you scroll.
- **Scrolling:** sections, cards and photos reveal in staggered order, and feature photos wipe in.
  An orange progress bar runs along the top, and the header hides on scroll down and returns on scroll up.
- **Photos:** parallax on banners and the CTA band, and 3D tilt with glare on project cards (mouse only).
- **How we work:** a line draws across the steps.
- **Products:** the category bar sticks under the header and underlines the section in view.
- **Theme toggle:** a circular reveal from the button. Page-to-page navigation cross-fades
  (View Transitions; Chrome and Edge).

Accessibility rules:
- Nothing animates for visitors who set "reduce motion" in their system settings, or when JavaScript is off.
- Content is never hidden without JS, so print, screen readers and search engines see everything.
- Anything that moves on its own stops with the hero's pause button, and also pauses on hover
  or when the tab is in the background.
- To tag a new element for a scroll reveal, add `data-reveal` to it, or add its selector to
  the lists at the top of `crg-motion.js`.

### Blueprint background, logo and favicon

- **Blueprint background:** a fixed layer behind the page. A faint drafting grid is pure CSS
  (shows without JS), and a canvas sketches construction drawings that draw themselves, hold
  and fade:
  - dimension lines with feet-and-inch labels
  - circles with radii, and compass arcs with angles
  - footprints with hatching
  - construction lines
  - a drafting crosshair with coordinates that follows the mouse

  New drawings favor the page margins, the ink is theme-aware and low-contrast, and cards and
  colored bands stay solid, so text keeps full contrast. With reduced motion it's a single
  still drawing.
- **Header logo:** an inline SVG traced from the full-resolution logo PNG, so the wordmark
  follows the light/dark theme. On the first page of a visit, the CRG letters draw their
  outlines and fill, the divider grows and the wordmark slides in. On hover, the letters hop.
- **Pause:** the header's pause button (and the hero's) stops the slideshow, the marquee and
  the blueprint drawings on every page, and is remembered on this device.
- **Favicon:** the orange mark on a Night square. Files: `favicon.ico` (16/32/48),
  `images/favicon.svg`, and `images/apple-touch-icon.png` / `images/icon-192.png`.

### Changes made to Intera

- Intera's full-screen `#loading-area` overlay is removed. It hid the whole page until every
  image had downloaded (about 12 seconds on a slow phone connection) and never went away
  without JavaScript.
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

### Trimmed template CSS

Intera shipped 584 KB of CSS (99 KB compressed), loaded as five files, two of them through
`@import`, so the browser could only find them one after another. Almost all of it styled parts
of the template this site doesn't use. Now:

- `tools/site-builder/template-css/` holds Intera's original stylesheets (recolored).
- `tools/site-builder/purge.mjs` keeps only the rules that match something in the site's pages or
  scripts, and writes them to `css/intera.css` (one file, about 53 KB, or 11 KB compressed).
  Classes that Intera's scripts add while the page runs (menu, sticky header, lightbox) are
  kept on purpose.
- Nothing is rounded or rewritten, so the result is visually identical. This was checked by
  comparing the computed style of every element, old CSS against new:
  - every page
  - light and dark themes, at desktop and mobile widths
  - with the mobile menu open, the header stuck, the lightbox open and the project filter in use
- `npm run build` regenerates it.
- If you use a template class that's new to the site, rebuild. Its rules come back
  automatically, because the trim reads the pages.
- Prefer overriding Intera in `crg-site.css` to editing the template CSS.

### Editing pages

The pages are generated. Don't edit the HTML in `site/` directly; your changes would be
overwritten on the next build. The generator is in `tools/site-builder/`:

| File | What it holds |
|---|---|
| `build.py` | Shared `<head>`, header, footer, icons, search metadata, sitemap and redirects |
| `pages.py` | The five main pages and the 404 page |
| `case_studies.json`, `case_studies.py` | Case-study content and its page template |
| `htaccess.txt` | Apache settings and the old-site redirects |
| `purge.mjs`, `template-css/` | The trimmed template CSS |

The CSS and JS in `site/css` and `site/js` (other than `intera.css`) are edited directly.

To rebuild, you need Python 3 and Node 18 or later:

```sh
cd tools/site-builder
npm install        # first time only
npm run build      # writes the pages, sitemap.xml, robots.txt, .htaccess and css/intera.css
```
