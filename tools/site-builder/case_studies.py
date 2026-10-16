"""Case-study pages (site/case-studies/<slug>.html) and the card grid on projects.html.

Content lives in case_studies.json: CRG's case studies from the old WordPress site,
with the editorial fixes listed in README.md. Photos:
  site/images/case-studies/<slug>.jpg (+ -640/-960/-<width>.webp)  hero photo, optional
  site/images/case-studies/<slug>/NN.jpg (+ NN-640.webp)           gallery, optional
fetch_case_photos.py downloads the galleries from the old site.
"""
import glob
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = json.load(open(os.path.join(HERE, 'case_studies.json')))
URL = 'case-studies/{}.html'


def md(text):
    """The little markdown the scraped copy uses: [links](url) and _italics_."""
    text = html.escape(text, quote=False)
    def link(m):
        label, href = m.group(1), m.group(2)
        ext = href.startswith('http')
        return f'<a href="{href}"' + (' target="_blank" rel="noopener"' if ext else '') + f'>{label}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, text)
    return re.sub(r'(?<![\w/])_([^_]+)_(?!\w)', r'<i>\1</i>', text)


def esc(s):
    return html.escape(s, quote=True)


def hero_widths(site, slug):
    ws = []
    for f in glob.glob(os.path.join(site, 'images', 'case-studies', slug + '-*.webp')):
        m = re.search(r'-(\d+)\.webp$', f)
        if m:
            ws.append(int(m.group(1)))
    return sorted(ws)


def picture(site, c, cls, sizes, eager=False):
    ws = hero_widths(site, c['slug'])
    srcset = ', '.join(f'images/case-studies/{c["slug"]}-{w}.webp {w}w' for w in ws)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    alt = esc(c['photo_alt'])
    return (f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img class="{cls}" src="images/case-studies/{c["slug"]}.jpg" alt="{alt}" width="{ws[-1]}" '
            f'height="{round(ws[-1] * 9 / 16)}" {load} decoding="async"></picture>')


def gallery(site, slug):
    files = sorted(f for f in glob.glob(os.path.join(site, 'images', 'case-studies', slug, '*.jpg')))
    return [os.path.basename(f)[:-4] for f in files]


def video(v, name):
    if v['provider'] == 'vimeo':
        m = re.search(r'/video/(\d+)(?:\?h=(\w+))?', v['url'])
        vid, h = m.group(1), m.group(2)
        page = f'https://vimeo.com/{vid}' + (f'/{h}' if h else '')
        embed = f'https://player.vimeo.com/video/{vid}?' + (f'h={h}&amp;' if h else '') + 'dnt=1&amp;autoplay=1'
        where = 'Vimeo'
    else:
        vid = re.search(r'/embed/([\w-]+)', v['url']).group(1)
        page = f'https://www.youtube.com/watch?v={vid}'
        embed = f'https://www.youtube-nocookie.com/embed/{vid}?autoplay=1'
        where = 'YouTube'
    caption = esc(v['caption'] or f'{name} video')
    return f'''<a class="crg-video" href="{page}" target="_blank" rel="noopener" data-embed="{embed}" data-title="{caption}">
                        <span class="crg-video__play" aria-hidden="true"><svg class="crg-icon crg-icon--lg"><use href="#i-play"/></svg></span>
                        <span class="crg-video__text"><b>{caption}</b><span>Play video · {where}</span></span>
                    </a>'''


def card(site, c):
    if c['photo']:
        media = picture(site, c, 'crg-case-card__img', '(min-width: 1200px) 360px, (min-width: 768px) 45vw, 100vw')
    else:
        media = (f'<span class="crg-case-card__sheet" aria-hidden="true"><span>CS-{c["number"]:02d}</span>'
                 f'<svg class="crg-icon crg-icon--xl"><use href="#i-pencil-ruler"/></svg></span>')
    return f'''            <li>
                <a class="crg-case-card" href="{URL.format(c['slug'])}">
                    <span class="crg-case-card__media">{media}</span>
                    <span class="crg-case-card__body">
                        <span class="crg-case-card__meta">{esc(c['city'])}, {c['state']} · {c['type']}</span>
                        <span class="crg-case-card__title">{esc(c['name'])}</span>
                        <span class="crg-case-card__sum">{esc(c['summary'])}</span>
                    </span>
                </a>
            </li>'''


def refresh(site):
    """A case study has a hero photo when its file exists (see fetch_case_photos.py)."""
    for c in CASES:
        c['photo'] = os.path.exists(os.path.join(site, 'images', 'case-studies', c['slug'] + '.jpg'))
        c['photo_alt'] = c['photo_alt'] or f"{c['name']}, {c['city']}, {c['state']}"


def grid(site):
    refresh(site)
    return ('        <ul class="crg-case-grid">\n' + '\n'.join(card(site, c) for c in CASES) + '\n        </ul>')


def page(site, c, h):
    icon, cta = h['icon'], h['cta']
    i = CASES.index(c)
    prev_c, next_c = CASES[i - 1], CASES[(i + 1) % len(CASES)]
    sheet = f'CS-{c["number"]:02d}'
    if c['photo']:
        media = picture(site, c, 'crg-banner__photo', '100vw', eager=True)
        banner_cls = 'crg-banner crg-banner--case'
    else:
        media = f'<span class="crg-banner__sheet" aria-hidden="true">{sheet}</span>'
        banner_cls = 'crg-banner crg-banner--case crg-banner--sheet'

    facts = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in c['facts'])
    facts += f'<div><dt>Sheet</dt><dd>{sheet} / {len(CASES)}</dd></div>'
    body = '\n'.join(f'                    <p>{md(p)}</p>' for p in c['paragraphs'])
    if c['products']:
        items = '\n'.join(f'                        <li>{icon("check", "crg-icon--sm")}<span>{md(p)}</span></li>' for p in c['products'])
        body += f'''
                    <h2 class="crg-h3">What we installed</h2>
                    <ul class="crg-checks">
{items}
                    </ul>'''
    if c['videos']:
        vids = '\n'.join('                    ' + video(v, c['name']) for v in c['videos'])
        body += f'''
                    <h2 class="crg-h3">Project video{"s" if len(c["videos"]) > 1 else ""}</h2>
                    <div class="crg-videos{' crg-videos--multi' if len(c['videos']) > 1 else ''}">
{vids}
                    </div>'''

    quotes = '\n'.join(f'''                    <figure class="crg-quote">
                        {icon('quote', 'crg-icon--lg')}
                        <blockquote><p>{md(q['text'])}</p></blockquote>
                        <figcaption><b>{esc(q['name'])}</b>{f"<span>{esc(q['role'])}</span>" if q['role'] else ''}</figcaption>
                    </figure>''' for q in c['quotes'])

    photos = gallery(site, c['slug'])
    gallery_html = ''
    if photos:
        items = '\n'.join(
            f'''            <li><a class="mfp-link" href="images/case-studies/{c['slug']}/{p}.jpg" title="{esc(c['name'])}, photo {n} of {len(photos)}">'''
            + (f'<picture><source type="image/webp" srcset="images/case-studies/{c["slug"]}/{p}-640.webp">' if os.path.exists(os.path.join(site, 'images', 'case-studies', c['slug'], p + '-640.webp')) else '<picture>')
            + f'''<img src="images/case-studies/{c['slug']}/{p}.jpg" alt="{esc(c['name'])}, photo {n}" loading="lazy" decoding="async" width="640" height="427"></picture></a></li>'''
            for n, p in enumerate(photos, 1))
        gallery_html = f'''
<section class="section-full crg-section crg-section--tight" aria-labelledby="gallery-title">
    <div class="container">
        <h2 id="gallery-title" class="crg-h2">Project photos</h2>
        <ul class="crg-gallery mfp-gallery">
{items}
        </ul>
    </div>
</section>'''

    html_body = f'''<div class="{banner_cls}" data-parallax>
    {media}
    <div class="container crg-banner__entry">
        <p class="crg-eyebrow">Case study · {c['type']}</p>
        <h1 class="crg-h1">{esc(c['name'])}</h1>
        <p class="crg-banner__lede">{esc(c['summary'])}</p>
        <nav class="crg-breadcrumb" aria-label="Breadcrumb">
            <ol>
                <li><a href="index.html">Home</a></li>
                <li><a href="projects.html#cases-title">Projects</a></li>
                <li aria-current="page">{esc(c['name'])}</li>
            </ol>
        </nav>
    </div>
</div>
<section class="section-full content-inner crg-section crg-case" aria-label="Project details">
    <div class="container">
        <dl class="crg-titleblock">{facts}</dl>
        <div class="crg-case__grid">
            <div class="crg-case__body">
{body}
            </div>
            <aside class="crg-case__aside" aria-label="Client feedback and next steps">
{quotes}
                <div class="crg-case__cta">
                    <h2 class="crg-h3">Planning a project like this?</h2>
                    <p>Tell us about your site, who will use it, and your budget. We’ll design it, supply it and install it.</p>
                    <a href="contact.html" class="crg-btn crg-btn--primary">Request a quote {icon('arrow-right', 'crg-icon--md')}</a>
                    <a href="tel:+13177767830" class="crg-case__phone">{icon('phone', 'crg-icon--sm')} (317) 776-7830</a>
                </div>
            </aside>
        </div>
    </div>
</section>{gallery_html}
<nav class="crg-case-nav" aria-label="More case studies">
    <div class="container">
        <a class="crg-case-nav__link" href="{URL.format(prev_c['slug'])}" rel="prev">{icon('arrow-left', 'crg-icon--md')}<span><small>Previous</small>{esc(prev_c['name'])}</span></a>
        <a class="crg-case-nav__all" href="projects.html#cases-title">All case studies</a>
        <a class="crg-case-nav__link crg-case-nav__link--next" href="{URL.format(next_c['slug'])}" rel="next"><span><small>Next</small>{esc(next_c['name'])}</span>{icon('arrow-right', 'crg-icon--md')}</a>
    </div>
</nav>
{cta('Have a site in mind?')}'''

    place = f"{c['city']}, {c['state']}"
    return dict(
        filename=URL.format(c['slug']),
        title=esc(f"{c['name']} Case Study | CRG Commercial Recreation Group"),
        desc=esc(f"{c['summary']} A Commercial Recreation Group project in {place}."),
        body=html_body, active='projects.html',
        crumbs=[('Projects', 'projects.html'), (c['name'], URL.format(c['slug']))],
        image=f"images/case-studies/{c['slug']}.jpg" if c['photo'] else None,
        image_alt=esc(c['photo_alt']) if c['photo'] else None,
    )


def pages(site, h):
    refresh(site)
    return [page(site, c, h) for c in CASES]
