"""Assemble the CRG static pages from shared partials.

Writes plain HTML into site/. Run from the repo root:  python3 tools/site-builder/build.py
Then regenerate the trimmed template CSS:  node tools/site-builder/purge.mjs site
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', 'site')
LUCIDE = os.path.join(HERE, 'icons')  # Lucide v0.460.0 (ISC), only the icons used

ICONS = [
    'award', 'dog', 'quote', 'rotate-cw', 'trophy',
    'accessibility', 'armchair', 'arrow-right', 'arrow-up-right', 'baby', 'building-2',
    'check', 'chevron-up', 'church', 'clipboard-list', 'clock', 'facebook', 'hammer',
    'handshake', 'hard-hat', 'house', 'instagram', 'layers', 'linkedin', 'mail', 'map-pin',
    'moon', 'pause', 'pencil-ruler', 'phone', 'play', 'school', 'shield-check', 'sun', 'trees', 'truck',
    'umbrella', 'users', 'wrench', 'arrow-left',
]


def sprite():
    out = []
    for name in ICONS:
        src = open(os.path.join(LUCIDE, name + '.svg')).read().split('-->', 1)[1]
        body = re.search(r'>\s*(.*)</svg>', src, re.S).group(1)
        body = ' '.join(line.strip() for line in body.strip().splitlines())
        out.append(f'  <symbol id="i-{name}" viewBox="0 0 24 24">{body}</symbol>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n'
            '  <!-- Lucide v0.460.0, ISC license -->\n' + '\n'.join(out) + '\n</svg>')


def icon(name, cls=''):
    c = 'crg-icon' + (' ' + cls if cls else '')
    return f'<svg class="{c}" aria-hidden="true"><use href="#i-{name}"/></svg>'


NAV = [
    ('index.html', 'Home'),
    ('products.html', 'Products'),
    ('projects.html', 'Projects'),
    ('about.html', 'About'),
    ('contact.html', 'Contact'),
]

LOGO_SVG = open(os.path.join(HERE, 'logo-inline.svg')).read()

LOGO = ('<img class="crg-light-only" src="images/logo/crg-horizontal-color.png" alt="CRG Commercial Recreation Group" width="220" height="31" loading="lazy" decoding="async">'
        '<img class="crg-dark-only" src="images/logo/crg-horizontal-reverse.png" alt="CRG Commercial Recreation Group" width="220" height="31" loading="lazy" decoding="async">')



# ------------------------------------------------------------------- SEO
# Production address. Canonical links, the sitemap and share images all use
# it. The GitHub Pages preview is marked noindex by the deploy workflow.
SITE_URL = 'https://crgplay.com/'
LASTMOD = '2026-10-16'
CRUMBS = {'products.html': 'Products', 'projects.html': 'Projects', 'about.html': 'About', 'contact.html': 'Contact'}

BUSINESS = {
    '@type': 'LocalBusiness',
    '@id': SITE_URL + '#business',
    'name': 'Commercial Recreation Group',
    'alternateName': 'CRG',
    'description': 'One of the largest commercial dealers for playground equipment in Indiana: '
                   'Playcraft Systems play systems, shade structures, safety surfacing, sports '
                   'equipment, site amenities and dog parks, with planning, design and installation.',
    'url': SITE_URL,
    'logo': SITE_URL + 'images/logo/crg-stacked-color.png',
    'image': SITE_URL + 'images/og-image.jpg',
    'telephone': '+1-317-776-7830',
    'email': 'info@CRGplay.com',
    'address': {
        '@type': 'PostalAddress',
        'streetAddress': '15150 Herriman Blvd',
        'addressLocality': 'Noblesville',
        'addressRegion': 'IN',
        'postalCode': '46060',
        'addressCountry': 'US',
    },
    'openingHoursSpecification': [{
        '@type': 'OpeningHoursSpecification',
        'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'opens': '08:00',
        'closes': '17:00',
    }],
    'areaServed': {'@type': 'State', 'name': 'Indiana'},
    'sameAs': [
        'https://www.facebook.com/Crgplay',
        'https://www.instagram.com/commercialrecreationgroup/',
        'https://www.linkedin.com/company/commercial-recreation-group-llc/',
    ],
}


def canonical(filename):
    return SITE_URL if filename == 'index.html' else SITE_URL + filename


def structured_data(filename, crumbs=None):
    graph = [BUSINESS]
    if crumbs is None and filename in CRUMBS:
        crumbs = [(CRUMBS[filename], filename)]
    if crumbs:
        trail = [('Home', 'index.html')] + crumbs
        graph.append({
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': n, 'name': name.replace('&amp;', '&'), 'item': canonical(f)}
                for n, (name, f) in enumerate(trail, 1)
            ],
        })
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    return '<script type="application/ld+json">\n' + data.replace('</', '<\\/') + '\n</script>'


def seo_head(filename, title, desc, crumbs=None, image=None, image_alt=None):
    if filename == '404.html':
        return '<meta name="robots" content="noindex">'
    return '\n'.join([
        f'<link rel="canonical" href="{canonical(filename)}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Commercial Recreation Group">',
        '<meta property="og:locale" content="en_US">',
        f'<meta property="og:url" content="{canonical(filename)}">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:image" content="{SITE_URL}{image or "images/og-image.jpg"}">',
        *([] if image else ['<meta property="og:image:width" content="1200">',
                            '<meta property="og:image:height" content="630">']),
        f'<meta property="og:image:alt" content="{image_alt or "CRG Commercial Recreation Group logo over a playground with a green spiral slide"}">',
        '<meta name="twitter:card" content="summary_large_image">',
        structured_data(filename, crumbs),
    ])


ATTR_RE = re.compile(r'\b(href|src|srcset|imagesrcset|data-src|data-srcset)="([^"]*)"')


def root_relative(html, root='/'):
    """For the 404 page, which can be served at any depth: make every local
    asset/link path start at the site root."""
    def fix(url):
        url = url.strip()
        if not url or url.startswith(('http:', 'https:', '#', 'mailto:', 'tel:', '/', 'data:')):
            return url
        return root + url
    def sub(m):
        name, value = m.group(1), m.group(2)
        if 'srcset' in name:
            value = ', '.join(' '.join([fix(p.split(' ', 1)[0])] + p.split(' ', 1)[1:]) for p in value.split(', '))
        else:
            value = fix(value)
        return f'{name}="{value}"'
    return ATTR_RE.sub(sub, html)


def head(title, desc, filename, seo=''):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{seo}
<meta name="format-detection" content="telephone=no">
<meta name="color-scheme" content="light dark">
<script>try{{var d=document.documentElement,t=localStorage.getItem('crg-theme');if(t)d.dataset.theme=t;if(!sessionStorage.getItem('crg-logo')&&!matchMedia('(prefers-reduced-motion: reduce)').matches){{d.classList.add('crg-logo-intro');sessionStorage.setItem('crg-logo','1')}}}}catch(e){{}}</script>
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="images/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<meta name="theme-color" content="#1F1B1C">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&amp;family=Barlow:wght@400;500;600;700&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="css/crg-tokens.css">
<link rel="stylesheet" href="css/intera.css">
<link rel="stylesheet" href="css/skin/skin-crg.css">
<link rel="stylesheet" href="css/crg-base.css">
<link rel="stylesheet" href="css/crg-site.css">
<link rel="stylesheet" href="css/crg-motion.css">
<link rel="stylesheet" href="css/crg-blueprint.css">
</head>'''


def header(active):
    items = '\n'.join(
        f'                        <li{" class=\"active\"" if href == active else ""}><a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a></li>'
        for href, label in NAV)
    return f'''<header class="site-header mo-left">
    <div class="sticky-header main-bar-wraper navbar-expand-lg">
        <div class="main-bar clearfix">
            <div class="container clearfix">
                <div class="logo-header mostion">
                    <a href="index.html">{LOGO_SVG}</a>
                </div>
                <button class="navbar-toggler collapsed navicon justify-content-end" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span></span><span></span><span></span>
                </button>
                <div class="extra-nav">
                    <div class="extra-cell">
                        <button type="button" class="crg-theme-toggle crg-pause-toggle" data-motion-pause aria-pressed="false" aria-label="Pause animations">{icon('pause', 'crg-icon--md i-pause')}{icon('play', 'crg-icon--md i-play')}</button>
                        <button type="button" class="crg-theme-toggle" data-theme-toggle aria-label="Switch theme">{icon('moon', 'crg-icon--md i-moon')}{icon('sun', 'crg-icon--md i-sun')}</button>
                        <a href="contact.html" class="crg-btn crg-btn--primary crg-header-cta">Request a quote</a>
                    </div>
                </div>
                <div class="header-nav navbar-collapse collapse justify-content-end" id="navbarNavDropdown">
                    <div class="logo-header">
                        <a href="index.html">{LOGO}</a>
                    </div>
                    <ul class="nav navbar-nav">
{items}
                        <li class="crg-nav-cta"><a href="contact.html" class="crg-btn crg-btn--primary">Request a quote</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</header>'''


def banner(eyebrow, title, photo, crumb):
    return f'''<div class="crg-banner" data-parallax>
    <img class="crg-banner__photo" src="images/photos/{photo}" alt="" width="1600" height="900">
    <div class="container crg-banner__entry">
        <p class="crg-eyebrow">{eyebrow}</p>
        <h1 class="crg-h1">{title}</h1>
        <nav class="crg-breadcrumb" aria-label="Breadcrumb">
            <ol>
                <li><a href="index.html">Home</a></li>
                <li aria-current="page">{crumb}</li>
            </ol>
        </nav>
    </div>
</div>'''


AUDIENCES = [('school', 'Schools'), ('church', 'Churches'), ('building-2', 'Apartments'),
             ('baby', 'Daycares'), ('trees', 'Parks'), ('house', 'HOAs')]


def cta(title='Ready to start a project?', text='Our representatives are standing by to help you design the perfect play area. Call for a custom project quote.'):
    return f'''<section class="section-full crg-cta" aria-labelledby="cta-title" data-parallax>
    <img class="crg-cta__photo" src="images/photos/crisp-wet-morning.jpg" alt="" loading="lazy">
    <div class="crg-scrim"></div>
    <div class="container">
        <div class="crg-cta__inner">
            <h2 id="cta-title" class="crg-h1">{title}</h2>
            <p class="crg-body-lg">{text}</p>
            <div class="crg-actions">
                <a href="contact.html" class="crg-btn crg-btn--primary">Request a quote {icon('arrow-right', 'crg-icon--md')}</a>
                <a href="tel:+13177767830" class="crg-btn crg-btn--outline-light">{icon('phone', 'crg-icon--md')} (317) 776-7830</a>
            </div>
        </div>
    </div>
</section>'''


def footer():
    links = '\n'.join(f'                        <li><a href="{h}">{l}</a></li>' for h, l in NAV)
    return f'''<footer class="site-footer crg-footer">
    <div class="footer-top">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 col-md-12">
                    <div class="widget">
                        <div class="footer-logo"><img src="images/logo/crg-stacked-reverse.png" alt="CRG Commercial Recreation Group" width="140" height="96" loading="lazy" decoding="async"></div>
                        <p>One of the largest commercial dealers for playground equipment in the state of Indiana. Planning, design and installation for playgrounds, sports facilities and parks.</p>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-sm-6">
                    <div class="widget">
                        <h2 class="crg-footer__title">Explore</h2>
                        <ul class="crg-footer__list">
{links}
                        </ul>
                    </div>
                </div>
                <div class="col-lg-3 col-md-4 col-sm-6">
                    <div class="widget">
                        <h2 class="crg-footer__title">Who we serve</h2>
                        <ul class="crg-footer__list">
                            <li>Schools &amp; daycares</li>
                            <li>Churches</li>
                            <li>Apartments &amp; HOAs</li>
                            <li>Parks &amp; recreation</li>
                        </ul>
                    </div>
                </div>
                <div class="col-lg-3 col-md-4">
                    <div class="widget">
                        <h2 class="crg-footer__title">Contact</h2>
                        <ul class="crg-footer__list crg-footer__contact">
                            <li>{icon('phone', 'crg-icon--sm')}<a href="tel:+13177767830">(317) 776-7830</a></li>
                            <li>{icon('mail', 'crg-icon--sm')}<a href="mailto:info@CRGplay.com">info@CRGplay.com</a></li>
                            <li>{icon('map-pin', 'crg-icon--sm')}<span>15150 Herriman Blvd<br>Noblesville, IN 46060</span></li>
                            <li>{icon('clock', 'crg-icon--sm')}<span>Mon–Fri, 8am–5pm</span></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="footer-bottom">
        <div class="container">
            <div class="crg-footer__bottom">
                <p>&copy; <span class="current-year">2026</span> Commercial Recreation Group. All rights reserved.</p>
                <ul class="crg-social">
                    <li><a href="https://www.facebook.com/Crgplay" target="_blank" rel="noopener" aria-label="CRG on Facebook">{icon('facebook', 'crg-icon--md')}</a></li>
                    <li><a href="https://www.instagram.com/commercialrecreationgroup/" target="_blank" rel="noopener" aria-label="CRG on Instagram">{icon('instagram', 'crg-icon--md')}</a></li>
                    <li><a href="https://www.linkedin.com/company/commercial-recreation-group-llc/" target="_blank" rel="noopener" aria-label="CRG on LinkedIn">{icon('linkedin', 'crg-icon--md')}</a></li>
                </ul>
            </div>
        </div>
    </div>
</footer>
<button class="scroltop crg-scroltop" type="button" aria-label="Back to top">{icon('chevron-up')}</button>'''



# ---------------------------------------------------------------- images
WIDTHS = (640, 960, 1280, 1600)
SIZES = [  # (context marker, sizes) - first match wins
    ('crg-slide', '(min-width: 992px) 54vw, 100vw'),
    ('crg-banner__photo', '100vw'),
    ('crg-cta__photo', '100vw'),
    ('crg-about__photo', '(min-width: 992px) 50vw, 100vw'),
    ('crg-feature__media', '(min-width: 992px) 55vw, 100vw'),
    ('crg-project__media', '(min-width: 992px) 33vw, (min-width: 768px) 50vw, 100vw'),
]
IMG_RE = re.compile(r'<img ([^>]*?)src="images/photos/([a-z0-9-]+)\.jpg"([^>]*)>')


def responsive(html):
    """Wrap every content photo in <picture> with WebP srcset + sizes.
    The original JPEG stays as the fallback src (and as the lightbox target)."""
    def sub(m):
        before, name, after = m.group(1), m.group(2), m.group(3)
        context = html[max(0, m.start() - 160):m.start()] + before + after
        sizes = next((s for k, s in SIZES if k in context), '100vw')
        webp = ', '.join(f'images/photos/{name}-{w}.webp {w}w' for w in WIDTHS)
        attrs = (before + after).strip()
        if 'decoding=' not in attrs:
            attrs += ' decoding="async"'
        if 'data-defer' in attrs:
            # Loaded later by crg-motion.js (hidden hero slides).
            return (f'<picture><source type="image/webp" data-srcset="{webp}" sizes="{sizes}">'
                    f'<img {attrs} data-src="images/photos/{name}.jpg"></picture>')
        return (f'<picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
                f'<img {attrs} src="images/photos/{name}.jpg"></picture>')
    return IMG_RE.sub(sub, html)


SCRIPTS = '''<script src="js/combining.js"></script>
<script src="js/theme.js"></script>
<script src="js/crg-site.js"></script>
<script src="js/crg-motion.js"></script>
<script src="js/crg-blueprint.js"></script>'''


def page(filename, title, desc, body, extra_scripts='', active=None, crumbs=None, image=None, image_alt=None):
    html = '\n'.join([
        head(title, desc, filename, seo_head(filename, title, desc, crumbs, image, image_alt)),
        '<body id="bg">',
        sprite(),
        '<a class="crg-skip" href="#main">Skip to content</a>',
        '<div class="crg-blueprint" aria-hidden="true"><canvas></canvas></div>',
        '<div class="crg-progress" aria-hidden="true"></div>',
        '<div class="page-wraper">',
        header(active or filename),
        '<main id="main" class="page-content">',
        body,
        '</main>',
        footer(),
        '</div>',
        SCRIPTS + extra_scripts,
        '</body>',
        '</html>',
        '',
    ])
    html = responsive(html)
    if filename == '404.html':
        html = root_relative(html)
    elif '/' in filename:  # pages one folder down, e.g. case-studies/
        html = root_relative(html, '../')
    if filename == 'index.html':
        # The first hero slide is the largest paint on the home page.
        hero = ', '.join(f'images/photos/asla-sunset-{w}.webp {w}w' for w in WIDTHS)
        html = html.replace('<link rel="stylesheet" href="css/crg-tokens.css">',
            f'<link rel="preload" as="image" type="image/webp" imagesrcset="{hero}" imagesizes="(min-width: 992px) 54vw, 100vw" fetchpriority="high">\n<link rel="stylesheet" href="css/crg-tokens.css">', 1)
    os.makedirs(os.path.dirname(os.path.join(SITE, filename)), exist_ok=True)
    open(os.path.join(SITE, filename), 'w').write(html)


sys.path.insert(0, HERE)
import pages  # noqa: E402
import case_studies  # noqa: E402

helpers = dict(icon=icon, banner=banner, cta=cta, AUDIENCES=AUDIENCES, case_grid=case_studies.grid(SITE))
specs = pages.build(helpers) + case_studies.pages(SITE, helpers)
for spec in specs:
    page(**spec)
print('built', len(specs), 'pages')

# ------------------------------------------------- sitemap, robots, htaccess
SITEMAP_PAGES = [('index.html', '1.0'), ('products.html', '0.9'), ('projects.html', '0.8'),
                 ('about.html', '0.7'), ('contact.html', '0.9')]
SITEMAP_PAGES += [(case_studies.URL.format(c['slug']), '0.6') for c in case_studies.CASES]
urls = '\n'.join(f'  <url><loc>{canonical(f)}</loc><lastmod>{LASTMOD}</lastmod><priority>{p}</priority></url>'
                 for f, p in SITEMAP_PAGES)
open(os.path.join(SITE, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '\n</urlset>\n')
open(os.path.join(SITE, 'robots.txt'), 'w').write(
    'User-agent: *\nDisallow: /script/\n\nSitemap: ' + SITE_URL + 'sitemap.xml\n')
redirects = '\n'.join(
    f"RewriteRule ^case-studies/{c['old_slug']}(/.*)?$ /{case_studies.URL.format(c['slug'])} [R=301,L]"
    for c in case_studies.CASES)
open(os.path.join(SITE, '.htaccess'), 'w').write(
    open(os.path.join(HERE, 'htaccess.txt')).read().replace('#CASE-STUDY-REDIRECTS#', redirects))
print('wrote sitemap.xml, robots.txt, .htaccess')
