"""Save the case-study photo galleries from the old WordPress site (crgplay.com)
into the new site, before the old site is switched off.

Run from the repo root on any computer with internet access:
    python3 tools/site-builder/fetch_case_photos.py
then rebuild:
    cd tools/site-builder && npm run build

For each case study it downloads the full-size gallery photos to
site/images/case-studies/<slug>/01.jpg, 02.jpg ... With ImageMagick installed
(`magick` or `convert`), it also shrinks each photo to 1600px wide, makes a
640px WebP thumbnail, and, for case studies without a hero photo yet, makes
the first gallery photo the hero. The build adds the photos to each page as
a gallery with a lightbox. Already-downloaded photos are skipped.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', '..', 'site')
OUT = os.path.join(SITE, 'images', 'case-studies')
OLD = 'https://crgplay.com/case-studies/{}/'
UA = {'User-Agent': 'Mozilla/5.0 (CRG site migration)'}
PHOTO = re.compile(r'href="((?:https?://crgplay\.com)?/wp-content/uploads/images/[^"?#]+?\.jpe?g)"', re.I)
MAGICK = shutil.which('magick') or shutil.which('convert')


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def magick(*args):
    subprocess.run([MAGICK, *args], check=True)


def main(only):
    cases = json.load(open(os.path.join(HERE, 'case_studies.json')))
    for c in cases:
        if only and c['slug'] not in only and c['old_slug'] not in only:
            continue
        try:
            page = get(OLD.format(c['old_slug'])).decode('utf-8', 'replace')
        except Exception as e:  # noqa: BLE001
            print(f"{c['slug']}: could not load the old page ({e})")
            continue
        urls = []
        for u in PHOTO.findall(page):
            u = u if u.startswith('http') else 'https://crgplay.com' + u
            # Skip WordPress's resized copies (name-300x200.jpg) and cached thumbnails.
            if '/cache/' in u or re.search(r'-\d+x\d+\.jpe?g$', u, re.I) or u in urls:
                continue
            urls.append(u)
        folder = os.path.join(OUT, c['slug'])
        os.makedirs(folder, exist_ok=True)
        got = 0
        for n, u in enumerate(urls, 1):
            dest = os.path.join(folder, f'{n:02d}.jpg')
            if not os.path.exists(dest):
                try:
                    data = get(u)
                except Exception as e:  # noqa: BLE001
                    print(f'  skipped {u} ({e})')
                    continue
                open(dest, 'wb').write(data)
                if MAGICK:
                    magick(dest, '-auto-orient', '-resize', '1600x>', '-strip', '-interlace', 'Plane', '-quality', '80', dest)
            thumb = dest[:-4] + '-640.webp'
            if MAGICK and not os.path.exists(thumb):
                magick(dest, '-resize', '640x', '-strip', '-quality', '72', thumb)
            got += 1
        hero = os.path.join(OUT, c['slug'] + '.jpg')
        first = os.path.join(folder, '01.jpg')
        if MAGICK and got and not os.path.exists(hero):
            magick(first, '-strip', '-interlace', 'Plane', '-quality', '80', hero)
            width = int(subprocess.run([MAGICK, 'identify', '-format', '%w', first] if MAGICK.endswith('magick')
                                       else ['identify', '-format', '%w', first], capture_output=True, text=True).stdout)
            for w in sorted({640, 960, 1280, 1600, width}):
                if w <= width:
                    magick(first, '-resize', f'{w}x', '-strip', '-quality', '72', os.path.join(OUT, f"{c['slug']}-{w}.webp"))
        print(f"{c['slug']}: {got} photos" + ('' if MAGICK else ' (install ImageMagick to resize them and make thumbnails)'))
        if c.get('old_mp4'):
            print(f"  also has a time-lapse video on the old site: {', '.join(c['old_mp4'])} (upload it to Vimeo or YouTube to keep it)")


if __name__ == '__main__':
    main(set(sys.argv[1:]))
