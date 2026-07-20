from __future__ import annotations

from pathlib import Path
import html
import json
import os
import shutil
import urllib.parse

ROOT = Path(__file__).resolve().parent
OUT = ROOT / '_site'
CONTENT = ROOT / 'content' / 'de'
STATIC = ROOT / 'static'
CMS = ROOT / 'cms'


def load(name: str):
    return json.loads((CONTENT / name).read_text(encoding='utf-8'))


def esc(value):
    return html.escape(str(value or ''), quote=True)


def paragraphs(values, css=''):
    cls = f' class="{css}"' if css else ''
    return ''.join(f'<p{cls}>{esc(v).replace(chr(10), "<br>")}</p>' for v in (values or []))


def external(url, label, css='button button--ghost'):
    return f'<a class="{css}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>'


def page_head(site, title=None, description=None, canonical=None, noindex=False):
    page_title = title or site['site_title']
    desc = description or site['meta_description']
    canon = canonical or site['canonical_url']
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else ''
    return f'''<!doctype html>
<html lang="{esc(site.get('language','de'))}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(page_title)}</title>
  <meta name="description" content="{esc(desc)}">
  {robots}
  <meta name="theme-color" content="#07111c">
  <link rel="canonical" href="{esc(canon)}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="styles.css">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="de_DE">
  <meta property="og:title" content="{esc(page_title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{esc(canon)}">
  <meta property="og:image" content="https://iwe.hardt-wiehl.de/assets/ah-banner.webp">
</head>'''


def header(site, nav=None, home_link='#start'):
    nav_html = ''
    menu = ''
    if nav:
        menu = '<button class="menu-button" aria-label="Navigation öffnen" aria-expanded="false">☰</button>'
        nav_html = '<nav class="nav" aria-label="Hauptnavigation">' + ''.join(
            f'<a href="#{esc(item["anchor"])}">{esc(item["label"])}</a>' for item in nav
        ) + '</nav>'
    return f'''<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{home_link}" aria-label="Startseite">
      <span class="brand-mark" aria-hidden="true">AH</span>
      <span>{esc(site['short_name'])}<small>{esc(site['brand_subtitle'])}</small></span>
    </a>
    {menu}{nav_html}
  </div>
</header>'''


def footer(site):
    return f'''<footer class="site-footer">
  <div class="container footer-inner">
    <div>© <span id="year">2026</span> {esc(site['footer_text'])}</div>
    <div class="footer-links"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></div>
  </div>
</footer>
<script src="main.js"></script>'''


def render_index(site, home, career, expertise):
    h = home['hero']; p = home['profile']; c = home['competences']; l = home['leadership']
    pubsec = expertise['publication_section']; pub = expertise['publication']; speaker = expertise['speaker']; weld = expertise['welding']; contact = expertise['contact']
    mailto = 'mailto:' + site['email'] + '?subject=' + urllib.parse.quote(contact['email_subject'])

    facts = ''.join(f'<div class="fact"><strong>{esc(x["title"])}</strong><span>{esc(x["text"])}</span></div>' for x in p['facts'])
    cards = ''.join(f'<article class="card"><span class="card-num">{i:02d}</span><h3>{esc(x["title"])}</h3><p>{esc(x["text"])}</p></article>' for i, x in enumerate(c['items'], 1))
    leadership = ''.join(f'<div class="feature"><strong>{esc(x["title"])}</strong><span>{esc(x["text"])}</span></div>' for x in l['items'])
    timeline = ''.join(f'''<div class="timeline-item"><div class="timeline-date">{esc(x['date'])}</div><div class="timeline-content"><h3>{esc(x['title'])}</h3><p>{esc(x['text'])}</p></div></div>''' for x in career['items'])
    tags = ''.join(f'<span class="tag">{esc(x)}</span>' for x in pub['tags'])
    weld_items = ''.join(f'<div class="feature"><strong>{esc(x["title"])}</strong><span>{esc(x["text"])}</span></div>' for x in weld['items'])
    headline = '<br>'.join(esc(h['headline']).splitlines())

    return page_head(site) + f'''
<body>
<a class="skip-link" href="#inhalt">Zum Inhalt springen</a>
{header(site, home['navigation'])}
<main id="inhalt">
  <section class="hero" id="start">
    <div class="container hero-grid">
      <div>
        <p class="eyebrow">{esc(h['eyebrow'])}</p>
        <p class="hero-meta">{esc(h['meta'])}</p>
        <h1>{headline}</h1>
        <p class="hero-subtitle">{esc(h['qualification'])}</p>
        <p class="lead">{esc(h['lead'])}</p>
        <div class="actions">
          <a class="button button--gold" href="#profil">{esc(h['profile_button'])}</a>
          <a class="button button--ghost" href="#veroeffentlichungen">{esc(h['publication_button'])}</a>
          <a class="button button--ghost" href="{esc(mailto)}">{esc(h['email_button'])}</a>
        </div>
      </div>
      <div class="hero-card">
        <div class="portrait-wrap"><img class="portrait" src="assets/profil-andreas-hardt.webp" alt="Porträt von {esc(site['name'])}" width="999" height="943"></div>
        <div class="location">{esc(site['location'])}</div>
      </div>
    </div>
  </section>

  <section class="section" id="profil"><div class="container grid-2"><div>
    <p class="eyebrow">{esc(p['eyebrow'])}</p><h2>{esc(p['heading'])}</h2><p class="section-intro">{esc(p['intro'])}</p>{paragraphs(p['paragraphs'])}
  </div><aside class="fact-panel" aria-label="Profil auf einen Blick">{facts}</aside></div></section>

  <section class="section section--soft" id="kompetenzen"><div class="container">
    <p class="eyebrow">{esc(c['eyebrow'])}</p><h2>{esc(c['heading'])}</h2><p class="section-intro">{esc(c['intro'])}</p><div class="cards">{cards}</div>
  </div></section>

  <section class="section" id="fuehrung"><div class="container">
    <div class="grid-2"><div><p class="eyebrow">{esc(l['eyebrow'])}</p><h2>{esc(l['heading'])}</h2></div><div><p class="section-intro">{esc(l['intro'])}</p></div></div>
    <div class="feature-list">{leadership}</div><blockquote class="quote">„{esc(l['quote'])}“</blockquote>
  </div></section>

  <section class="section section--soft" id="werdegang"><div class="container">
    <p class="eyebrow">{esc(career['eyebrow'])}</p><h2>{esc(career['heading'])}</h2><div class="timeline">{timeline}</div>
  </div></section>

  <section class="section" id="veroeffentlichungen"><div class="container">
    <p class="eyebrow">{esc(pubsec['eyebrow'])}</p><h2>{esc(pubsec['heading'])}</h2>
    <div class="publication"><div class="publication-art" aria-hidden="true"></div><div class="publication-copy">
      <p class="meta">{esc(pub['meta'])}</p><h3>{esc(pub['title'])}</h3><p>{esc(pub['text'])}</p><div class="tags">{tags}</div>
      <div class="actions">{external(pub['url'], pub['button_label'], 'button button--gold')}{external(site['linkedin_url'], pub['linkedin_label'])}</div>
    </div></div>
  </div></section>

  <section class="section section--soft" id="referent"><div class="container grid-2"><div>
    <p class="eyebrow">{esc(speaker['eyebrow'])}</p><h2>{esc(speaker['heading'])}</h2><p class="section-intro">{esc(speaker['intro'])}</p><p>{esc(speaker['text'])}</p>
  </div><div class="card"><h3>{esc(speaker['topics_heading'])}</h3><p>{esc(speaker['topics'])}</p></div></div></section>

  <section class="section" id="schweissaufsicht"><div class="container grid-2"><div>
    <p class="eyebrow">{esc(weld['eyebrow'])}</p><h2>{esc(weld['heading'])}</h2><p class="section-intro">{esc(weld['intro'])}</p>
  </div><div><div class="feature-list">{weld_items}</div></div></div></section>

  <section class="section section--soft" id="kontakt"><div class="container"><div class="contact-card"><div>
    <p class="eyebrow">{esc(contact['eyebrow'])}</p><h2>{esc(contact['heading'])}</h2><p>{esc(contact['text'])}</p><p><strong>{esc(site['name'])}</strong><br>{esc(site['location'])}</p>
  </div><div class="contact-links">
    <a href="{esc(mailto)}"><span>{esc(site['email'])}</span><span>↗</span></a>
    <a href="{esc(site['linkedin_url'])}" target="_blank" rel="noopener noreferrer"><span>LinkedIn</span><span>↗</span></a>
    <a href="{esc(site['xing_url'])}" target="_blank" rel="noopener noreferrer"><span>XING</span><span>↗</span></a>
  </div></div></div></section>
</main>
{footer(site)}
</body></html>'''


def render_imprint(site, legal):
    x = legal['imprint']
    address = f'''<address>{esc(x['provider_name'])}<br>{esc(x['street'])}<br>{esc(x['postal_city'])}<br>{esc(x['country'])}</address>'''
    return page_head(site, f"{x['heading']} | {site['short_name']}", noindex=True) + f'''
<body>{header(site, home_link='index.html')}
<main class="legal"><div class="container"><article class="legal-card">
  <p class="eyebrow">{esc(x['eyebrow'])}</p><h1>{esc(x['heading'])}</h1><h2>{esc(x['provider_heading'])}</h2>
  <div class="legal-profile"><img class="legal-profile-image" src="assets/profil-andreas-hardt.webp" alt="Porträt von {esc(site['name'])}" width="999" height="943"><div>{address}<p>E-Mail: <a href="mailto:{esc(site['email'])}">{esc(site['email'])}</a></p></div></div>
  <h2>{esc(x['responsible_heading'])}</h2><p>{esc(x['provider_name'])}<br>{esc(x['street'])}<br>{esc(x['postal_city'])}</p>
  <h2>{esc(x['liability_heading'])}</h2><p>{esc(x['liability_text'])}</p>
  <h2>{esc(x['copyright_heading'])}</h2><p>{esc(x['copyright_text'])}</p>
  <p><a class="button button--gold" href="index.html">{esc(x['back_label'])}</a></p>
</article></div></main></body></html>'''


def render_privacy(site, legal):
    x = legal['privacy']
    sections = ''.join(f'<h2>{esc(s["heading"])}</h2>{paragraphs(s["paragraphs"])}' for s in x['sections'])
    return page_head(site, f"{x['heading']} | {site['short_name']}", noindex=True) + f'''
<body>{header(site, home_link='index.html')}
<main class="legal"><div class="container"><article class="legal-card">
  <p class="eyebrow">{esc(x['eyebrow'])}</p><h1>{esc(x['heading'])}</h1>{sections}
  <p><a class="button button--gold" href="index.html">{esc(x['back_label'])}</a></p>
</article></div></main></body></html>'''


def main():
    site = load('site.json'); home = load('home.json'); career = load('career.json'); expertise = load('expertise.json'); legal = load('legal.json')
    if OUT.exists(): shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)
    (OUT / 'admin').mkdir(parents=True, exist_ok=True)

    (OUT / 'index.html').write_text(render_index(site, home, career, expertise), encoding='utf-8')
    (OUT / 'impressum.html').write_text(render_imprint(site, legal), encoding='utf-8')
    (OUT / 'datenschutz.html').write_text(render_privacy(site, legal), encoding='utf-8')
    (OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: https://iwe.hardt-wiehl.de/sitemap.xml\n', encoding='utf-8')
    (OUT / 'sitemap.xml').write_text('''<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>https://iwe.hardt-wiehl.de/</loc></url>\n  <url><loc>https://iwe.hardt-wiehl.de/impressum.html</loc></url>\n  <url><loc>https://iwe.hardt-wiehl.de/datenschutz.html</loc></url>\n</urlset>\n''', encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')

    auth_url = os.environ.get('SVELTIA_AUTH_URL', '').strip().rstrip('/')
    if auth_url and auth_url.startswith('https://'):
        config = (CMS / 'config.template.yml').read_text(encoding='utf-8').replace('__SVELTIA_AUTH_URL__', auth_url)
        (OUT / 'admin/config.yml').write_text(config, encoding='utf-8')
        shutil.copy2(CMS / 'admin.live.html', OUT / 'admin/index.html')
        print(f'Admin OAuth aktiviert: {auth_url}')
    else:
        shutil.copy2(CMS / 'admin.setup.html', OUT / 'admin/index.html')
        print('Hinweis: SVELTIA_AUTH_URL fehlt; /admin zeigt die Einrichtungsseite.')

    print(f'Website erzeugt: {OUT}')

if __name__ == '__main__':
    main()
