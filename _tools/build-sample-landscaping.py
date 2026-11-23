#!/usr/bin/env python3
"""Builds the Critchfield Systems landscaping sample (critchfield-systems/sample-landscaping/):
a fictional landscaping company, "Hollow Creek Lawn & Landscape", made from sections in the
DeveloperDadd/components library (none of them reused from the roofing sample).

Usage: python3 _tools/build-sample-landscaping.py /path/to/components

Rules the build enforces: one button style (components/sections/button/button2) and every
button is a "Call Now" link; no forms; one H1 per page; no placeholder text left over.
Photos are the placeholder photos that ship with the components (CodeStitch image CDN),
listed in the IMG table below."""
import os, re, sys

COMP = os.path.join(sys.argv[1] if len(sys.argv) > 1 else '../components', 'sections')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'critchfield-systems', 'sample-landscaping')

# ---------------------------------------------------------------- business (fictional)
BIZ = 'Hollow Creek Lawn &amp; Landscape'
BIZ_TEXT = 'Hollow Creek Lawn & Landscape'
PHONE = '(859) 270-7050'          # Critchfield Systems' number, so calls reach Clayton
TEL = 'tel:+18592707050'
EMAIL = 'office@hollowcreek.example'
ADDRESS_1 = '400 Old Frankfort Pike'
ADDRESS_2 = 'Lexington, KY 40510'

CS_URL = 'https://critchfieldsystems.com'

# ---------------------------------------------------------------- placeholder photos
C = 'https://csimg.nyc3.cdn.digitaloceanspaces.com/'
IMG = {
    'leaf_bg': C + 'Hero/leaf-bg.jpg', 'leaf_bg_m': C + 'Hero/leaf-bg-m.jpg',
    'leaf': C + 'Services/leaf.jpg', 'grass': C + 'Services/grass.jpg', 'leaves': C + 'Services/leaves.jpg', 'path': C + 'Services/path.jpg',
    'grass2': C + 'SideBySide/grass2.jpg', 'tall_grass': C + 'SideBySide/tall-grass.jpg', 'garden': C + 'SideBySide/landscaping1.jpg',
    'rocks': C + 'Images%2FLandscapes%2Frocks.jpg',
    'house1': 'https://csimg.nyc3.digitaloceanspaces.com/Gallery/house1.jpg', 'house2': 'https://csimg.nyc3.digitaloceanspaces.com/Gallery/house2.jpg',
    'house4': 'https://csimg.nyc3.digitaloceanspaces.com/Gallery/house4.jpg', 'house5': 'https://csimg.nyc3.digitaloceanspaces.com/Gallery/house5.jpg',
    'house6': 'https://csimg.nyc3.digitaloceanspaces.com/Gallery/house6.jpg', 'house3': C + 'Images/house3.jpg',
    'house3b': C + 'Images/house4.jpg', 'house5b': C + 'Images/house5.jpg',
    'profile1': 'https://csimg.nyc3.digitaloceanspaces.com/Reviews/profile2.jpg', 'profile2': 'https://csimages2.nyc3.digitaloceanspaces.com/Reviews/profile3.jpg',
}

# ---------------------------------------------------------------- helpers
def raw(path):
    return open(os.path.join(COMP, path, 'index.html')).read()

def css(path):
    return open(os.path.join(COMP, path, 'style.css')).read()

def js(path):
    return open(os.path.join(COMP, path, 'script.js')).read()

BUTTON_CLASSES = ('cs-button-solid',)

def call_now(h):
    """The one button on this site: every .cs-button-2 is a Call Now link to the business."""
    def fix(m):
        cls = re.search(r'class="(cs-button-2[^"]*)"', m.group(0)).group(1)
        return f'<a href="{TEL}" class="{cls}">Call Now</a>'
    return re.sub(r'<a\b[^>]*class="cs-button-2[^"]*"[^>]*>.*?</a>', fix, h, flags=re.S)

def section(path, repl, empty_links_to='contact.html'):
    """Component markup with copy swapped. Each (old, new) replaces the FIRST remaining
    occurrence, so repeated placeholder text is replaced in order."""
    h = raw(path)
    for old, new in repl:
        if old not in h:
            raise SystemExit(f'{path}: text not found: {old[:70]!r}')
        h = h.replace(old, new, 1)
    h = h.replace('class="cs-button-solid', 'class="cs-button-2')
    h = call_now(h)
    if empty_links_to:
        h = h.replace('href=""', f'href="{empty_links_to}"')
    if re.search(r'[Ll]orem ipsum|Amet minim|Aqestic|Stitch', re.sub(r'<!--.*?-->', '', h, flags=re.S)):
        raise SystemExit(f'{path}: placeholder text left in markup')
    return h

def icon(name, color='olive'):
    return f'assets/icons/{name}-{color}.svg'

# ---------------------------------------------------------------- shared CSS
ROOT_CSS = """/* Hollow Creek Lawn & Landscape (sample site by Critchfield Systems)
   60-30-10: 60% sage #9DA65D (and its light tints), 30% olive #3B4013, 10% brown #402C1A */
:root {
    --sage: #9DA65D;             /* 60% - backgrounds (full sage bands + light tints) */
    --sageLight: #EEF0DF;        /* light sage tint, most section backgrounds */
    --sageMid: #DDE2BD;          /* mid sage tint */
    --olive: #3B4013;            /* 30% - headings, dark bands, nav bar, footer */
    --brown: #402C1A;            /* 10% - the Call Now buttons and accents */
    --primary: #3B4013;
    --primaryLight: #9DA65D;
    --secondary: #402C1A;
    --secondaryLight: #9DA65D;
    --headerColor: #3B4013;
    --bodyTextColor: #4B4F33;
    --bodyTextColorWhite: #F6F7EE;
    --topperFontSize: clamp(0.8125rem, 1.6vw, 1rem);
    --headerFontSize: clamp(1.9375rem, 3.9vw, 3.0625rem);
    --bodyFontSize: 1rem;
    --sectionPadding: clamp(3.75rem, 7.82vw, 6.25rem) 1rem;
}
html { scroll-behavior: smooth; }
body {
    margin: 0; padding: 0;
    font-family: "Nunito Sans", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    background-color: var(--sageLight); color: var(--bodyTextColor);
    -webkit-font-smoothing: antialiased;
}
*, *:before, *:after { box-sizing: border-box; }
img { max-width: 100%; }
button { font-family: inherit; }
.cs-topper { font-size: var(--topperFontSize); line-height: 1.2em; text-transform: uppercase; text-align: inherit; letter-spacing: .1em; font-weight: 800; color: var(--brown); margin-bottom: 0.25rem; display: block; }
.cs-title { font-size: var(--headerFontSize); font-weight: 900; line-height: 1.2em; text-align: inherit; max-width: 43.75rem; margin: 0 0 1rem 0; color: var(--headerColor); position: relative; }
.cs-text { font-size: var(--bodyFontSize); line-height: 1.5em; text-align: inherit; width: 100%; max-width: 40.625rem; margin: 0; color: var(--bodyTextColor); }

/*-- The one site button: components/sections/button/button2, as a link (.cs-button-2) --*/
.cs-button-2 {
    --color: #402C1A;
    font-family: inherit;
    display: inline-block;
    min-width: 8em;
    height: 2.6em;
    line-height: 2.5em;
    padding: 0 1.5em;
    margin: 0;
    position: relative;
    cursor: pointer;
    overflow: hidden;
    border: 2px solid var(--color);
    transition: color 0.5s, transform .3s, box-shadow .3s;
    z-index: 1;
    font-size: 17px;
    border-radius: 6px;
    font-weight: 800;
    color: var(--color);
    background-color: #FBFBF4;
    text-align: center;
    text-decoration: none;
    box-sizing: border-box;
    /* foreground shadow so the button pops off every background */
    box-shadow: 0 1rem 2rem -0.5rem rgba(64, 44, 26, 0.55), 0 0.375rem 0.875rem rgba(59, 64, 19, 0.3);
}
.cs-button-2:before {
    content: "";
    position: absolute;
    z-index: -1;
    background: var(--color);
    height: 150px;
    width: 200px;
    border-radius: 50%;
    top: 100%;
    left: 100%;
    transition: all 0.7s;
}
.cs-button-2:hover { color: #fff; transform: translateY(-0.1875rem); box-shadow: 0 1.375rem 2.5rem -0.5rem rgba(64, 44, 26, 0.65), 0 0.5rem 1.125rem rgba(59, 64, 19, 0.35); }
.cs-button-2:hover:before { top: -30px; left: -30px; }
.cs-button-2:active:before { background: #2A1C10; transition: background 0s; }
.cs-button-2:focus-visible { outline: 3px solid var(--sage); outline-offset: 3px; }

.cs-skip { position: absolute; left: 1rem; top: -4rem; z-index: 20000; background: var(--olive); color: #fff; padding: .75rem 1rem; text-decoration: none; font-weight: 700; }
.cs-skip:focus { top: 1rem; }
@media (prefers-reduced-motion: reduce) {
    *, *:before, *:after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}
"""

NAV_OVR = """
/* nav: top row on light sage, link row in olive */
#cs-navigation { background-color: #fff; }
#cs-navigation .cs-top-bar { background-color: #fff; }
#cs-navigation .cs-bottom-bar, #cs-navigation .cs-bottom-bar:before { background-color: var(--olive); }
#cs-navigation .cs-wrapper { background-color: var(--sageLight); }
#cs-navigation .cs-contact-link .cs-header { color: var(--brown); font-weight: 800; }
#cs-navigation .cs-contact-link .cs-link-content { color: var(--olive); font-weight: 700; }
#cs-navigation .cs-call .cs-header { color: var(--sageMid); }
#cs-navigation .cs-call .cs-link-content { color: #fff; font-weight: 800; }
#cs-navigation .cs-call .cs-wrapper { background-color: var(--sage); }
#cs-navigation .cs-logo img { height: 100%; width: auto; }
#cs-navigation .cs-li-link.cs-active, #cs-navigation .cs-li-link:hover { color: var(--sageMid); }
@media only screen and (max-width: 1023.5px) {
  /* keep the sample-site notice visible on phones */
  #cs-navigation .cs-top-container { flex-wrap: wrap; }
  #cs-navigation .cs-contact-group { flex: 1; justify-content: flex-end; }
  #cs-navigation .cs-contact-link.cs-demo { display: flex; order: 2; flex-basis: 100%; justify-content: flex-end; gap: .5rem; margin-top: .5rem; }
  #cs-navigation .cs-contact-link.cs-demo .cs-wrapper { display: none; }
  #cs-navigation .cs-contact-link.cs-demo .cs-header, #cs-navigation .cs-contact-link.cs-demo .cs-link-content { font-size: .75rem; text-align: right; }
}
@media only screen and (min-width: 64rem) {
  #cs-navigation .cs-ul > .cs-li > .cs-li-link { color: #fff; opacity: 1; }
  #cs-navigation .cs-li-link:before { background: var(--sage); }
  #cs-navigation .cs-drop-ul { background-color: #fff; }
  #cs-navigation .cs-drop-link { color: var(--olive); }
}
"""

FOOTER_OVR = """
/* footer: olive (30%) with the call-to-action banner in full sage */
#cs-footer-1294 { background-color: var(--olive); }
/* the footer's CTA banner rises 150px into the page: leave room so it never covers content */
main { padding-bottom: 9.375rem; }
#cta-1294 .cs-background { background-color: var(--sage); }
#cta-1294 .cs-title { color: var(--olive); }
#cs-footer-1294 .cs-header { color: #fff; }
#cs-footer-1294 .cs-text, #cs-footer-1294 .cs-link, #cs-footer-1294 .cs-nav-link, #cs-footer-1294 .cs-copyright, #cs-footer-1294 .cs-copyright-link { color: var(--bodyTextColorWhite); }
#cs-footer-1294 .cs-copyright-link.cs-cs { color: var(--sageMid); font-weight: 800; }
"""

def shared_css():
    return (ROOT_CSS + '\n' + css('nav/nav-1343-light-over-dark-rows-dropdown') + NAV_OVR
            + '\n' + css('footer/footer-1294-dark-cta-banner-over-columns') + FOOTER_OVR)

def page_css(paths, overrides, repl=()):
    out = '\n'.join(css(p) for p in paths)
    for a, b in repl:
        assert a in out, a
        out = out.replace(a, b)
    return out + '\n/* ---- brand overrides ---- */\n' + overrides

# ---------------------------------------------------------------- nav + footer
def nav(active):
    h = raw('nav/nav-1343-light-over-dark-rows-dropdown')
    rep = [
        ('<a href="" class="cs-logo" aria-label="Return to [Company Name] Home page">', f'<a href="index.html" class="cs-logo" aria-label="Return to {BIZ} home page">'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Logos/invest-logo-black.svg" alt="" width="197" height="43" aria-hidden="true"', f'src="assets/logo.svg" alt="{BIZ}" width="250" height="52"'),
        ('<a class="cs-contact-link" href="mailto:Info@invetexfinance.com">', f'<a class="cs-contact-link" href="{TEL}">'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/yellow-mail.svg"', f'src="{icon("phone", "brown")}"'),
        ('<span class="cs-header">Send A Message</span>', '<span class="cs-header">Call Us Today</span>'),
        ('<span class="cs-link-content">Info@invetexfinance.com</span>', f'<span class="cs-link-content">{PHONE}</span>'),
        ('<a class="cs-contact-link" href="">', f'<a class="cs-contact-link cs-demo" href="{CS_URL}">'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/yellow-pin.svg"', f'src="{icon("star", "brown")}"'),
        ('<span class="cs-header">Visit Us At</span>', '<span class="cs-header">Sample Website</span>'),
        ('<span class="cs-link-content">Oak Harbor, WA</span>', '<span class="cs-link-content">Built by Critchfield Systems. Get yours for $99/mo</span>'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Logos/down-yellow.svg"', f'src="{icon("chevron", "sage")}"'),
        ('<a href="" class="cs-li-link cs-drop-link">About</a>', '<a href="services.html#services" class="cs-li-link cs-drop-link">Lawn Care &amp; Mowing</a>'),
        ('<a href="" class="cs-li-link cs-drop-link">Tax Prep</a>', '<a href="services.html#services" class="cs-li-link cs-drop-link">Landscape Design</a>\n                                </li>\n                                <li class="cs-drop-li">\n                                    <a href="services.html#services" class="cs-li-link cs-drop-link">Hardscapes &amp; Patios</a>\n                                </li>\n                                <li class="cs-drop-li">\n                                    <a href="services.html#faq" class="cs-li-link cs-drop-link">Service FAQ</a>'),
        ('Team', 'Gallery'), ('Our Work', 'Contact'),
        ('<a class="cs-call" href="tel:555-555-0234">', f'<a class="cs-call" href="{TEL}">'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/phone-1a.svg"', f'src="{icon("phone", "olive")}"'),
        ('<span class="cs-header">Free Contact 24/7</span>', '<span class="cs-header">Free Estimates</span>'),
        ('<span class="cs-link-content">(604) 555-0234</span>', f'<span class="cs-link-content">{PHONE}</span>'),
    ]
    for o, n in rep:
        assert o in h, o
        h = h.replace(o, n, 1)
    h = h.replace('class="cs-button-solid', 'class="cs-button-2')
    h = call_now(h)
    hrefs = {'Home': 'index.html', 'About': 'about.html', 'Gallery': 'gallery.html', 'Contact': 'contact.html', 'FAQ': 'services.html#faq'}
    def fix(m):
        label = m.group(2).strip()
        href = hrefs[label]
        cur = ' cs-active" aria-current="page' if href == active else ''
        return f'<a href="{href}" class="cs-li-link{cur}">{m.group(2)}</a>'
    h = re.sub(r'<a href="" class="cs-li-link( cs-active" aria-current="page)?">(\s*\w+\s*)</a>', fix, h)
    if active == 'services.html':
        h = h.replace('class="cs-li-link cs-dropdown-toggle"', 'class="cs-li-link cs-dropdown-toggle cs-active"')
    assert 'href=""' not in re.sub(r'<!--.*?-->', '', h, flags=re.S), 'nav has empty link'
    return h

def footer():
    rep = [
        ('Call us today to get your free estimate. Let us build your dream home.', 'Call today for a free estimate. Let&rsquo;s build the yard you&rsquo;ve been dreaming about.'),
        ('srcset="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Graphics/cta-waves.svg"', 'srcset="assets/cta-waves.svg"'),
        ('srcset="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Graphics/cta-waves-t.svg"', 'srcset="assets/cta-waves.svg"'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Graphics/cta-waves-t.svg" alt="waves"', 'src="assets/cta-waves.svg" alt=""'),
        ('<a aria-label="go back to home" class="cs-logo" href="">', '<a aria-label="go back to home" class="cs-logo" href="index.html">'),
        ('src="https://csimg.nyc3.digitaloceanspaces.com/Footer/logo-light.svg" alt="logo" width="240" height="32"', f'src="assets/logo-light.svg" alt="{BIZ}" width="250" height="52"'),
        ('We planning, designing, financing, and executing projects.', 'Family-owned lawn care, landscape design and hardscaping for Central Kentucky homes since 2009.'),
        ('<a href="mailto:info@mail.com" class="cs-link">', f'<a href="mailto:{EMAIL}" class="cs-link">'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/thick-mail.svg" alt="icon"', f'src="{icon("mail", "sage")}" alt=""'),
        ('hi@stitchconstruction.com', EMAIL),
    ]
    for old, href, new in [('Email Marketing', 'services.html#services', 'Lawn Care'), ('Brandings', 'services.html#services', 'Landscape Design'),
                           ('Campaign', 'services.html#services', 'Hardscapes'), ('Offline', 'services.html#services', 'Seasonal Cleanups'),
                           ('Our Story', 'about.html', 'Our Story'), ('Benefits', 'about.html#why', 'Why Hollow Creek'),
                           ('Team', 'about.html#reviews', 'Reviews'), ('Career', 'gallery.html', 'Project Gallery'),
                           ('Facebook', TEL, f'Call {PHONE}'), ('Instagram', f'mailto:{EMAIL}', 'Email Us'), ('LinkedIn', 'contact.html', 'Service Area'),
                           ('FAQ', 'services.html#faq', 'FAQ'), ('Contact us', 'contact.html', 'Contact Us')]:
        rep.append((f'<a class="cs-nav-link" href="">{old}</a>', f'<a class="cs-nav-link" href="{href}">{new}</a>'))
    rep += [
        ('<span class="cs-header">Contact</span>', '<span class="cs-header">Get in Touch</span>'),
        ('Copyright© 2023. ', '&copy; <span id="cs-year">2026</span> '),
        ('<a class="cs-copyright-link" href="">Stitch Construction.</a>', f'<a class="cs-copyright-link" href="index.html">{BIZ}.</a>'),
        ('All Right Reserved.', f'Sample site by <a class="cs-copyright-link cs-cs" href="{CS_URL}">Critchfield Systems</a>.'),
        ('<a href="" class="cs-copyright-link">Terms of Service</a>', '<a href="services.html#faq" class="cs-copyright-link">FAQ</a>'),
        ('<a href="" class="cs-copyright-link">Privacy Policy</a>', '<a href="contact.html" class="cs-copyright-link">Contact</a>'),
    ]
    h = section('footer/footer-1294-dark-cta-banner-over-columns', rep, empty_links_to=None)
    assert 'href=""' not in h, 'footer has empty link'
    return h

# ---------------------------------------------------------------- page shell
def head(title, css_file):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="{BIZ} is a sample landscaping website built by Critchfield Systems.">
    <!-- Sample site: kept out of search results -->
    <meta name="robots" content="noindex, nofollow">
    <meta name="theme-color" content="#3B4013">
    <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700;800;900&display=swap">
    <link rel="stylesheet" href="css/root.css">
    <link rel="stylesheet" href="css/{css_file}">
</head>
<body>
<a class="cs-skip" href="#main">Skip to content</a>
'''

YEAR_JS = "const year = document.getElementById('cs-year');\nif (year) year.textContent = new Date().getFullYear();\n"

def page(name, title, css_file, body, scripts=()):
    html = head(title, css_file) + nav(name) + '\n<main id="main">\n' + body + '\n</main>\n' + footer() + '\n'
    html += ''.join(f'<script src="js/{s}" defer></script>\n' for s in ('nav.js', *scripts, 'year.js')) + '</body>\n</html>\n'
    # site rules
    assert not re.search(r'<(form|input|textarea|select)\b', html), f'{name}: form element found'
    assert html.count('<h1') == 1, f'{name}: needs exactly one h1'
    assert 'cs-button-solid' not in html and 'cs-button-4' not in html, f'{name}: second button style'
    labels = set(re.findall(r'class="cs-button-2[^"]*">([^<]*)</a>', html))
    assert labels == {'Call Now'}, f'{name}: button labels {labels}'
    return html

# ---------------------------------------------------------------- shared sections
def banner(topper, title, crumb, image='leaf_bg'):
    return section('page-banner/page-banner-559-tinted-photo-band-left-title', [
        ('<span class="cs-int-topper">Building Communities</span>', f'<span class="cs-int-topper">{topper}</span>'),
        ('<span class="cs-int-title">About</span>', f'<h1 class="cs-int-title">{title}</h1>'),
        ('<a href="" class="cs-link">Home</a>', '<a href="index.html" class="cs-link">Home</a>'),
        ('<a href="" class="cs-link cs-active">About</a>', f'<a href="#main" class="cs-link cs-active" aria-current="page">{crumb}</a>'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Hero/dna.jpg" alt="dna"', f'src="{IMG[image]}" alt=""'),
    ])
BANNER_OVR = """
#banner-559 .cs-background:before { background: var(--olive); opacity: .8; }
#banner-559 .cs-int-topper { color: var(--sageMid); }
#banner-559 .cs-link.cs-active { color: var(--sageMid); }
"""

def stats_band(numbers):
    rep = []
    for (old_n, old_d), (n, d) in zip([('10+', 'Years Experience'), ('2,000+', 'Products Sold'), ('4.9', 'Star Rating'), ('100+', 'Happy Customers')], numbers):
        rep += [(f'<span class="cs-number">{old_n}</span>', f'<span class="cs-number">{n}</span>'), (old_d, d)]
    rep.append(('src="https://csimg.nyc3.digitaloceanspaces.com/Stats/bg-m.jpg" alt="brick Wall"', f'src="{IMG["leaf_bg_m"]}" alt=""'))
    return section('stats/stats-16-photo-band-stats-with-button', rep)
STATS16_CSS = [('url("https://csimg.nyc3.digitaloceanspaces.com/Stats/bg.jpg")', f'url("{IMG["leaf_bg"]}")')]
STATS16_OVR = """
#cs-stats-16 .cs-background:before, #cs-stats-16:before { background: var(--olive); opacity: .82; }
#cs-stats-16 .cs-number { color: #fff; }
#cs-stats-16 .cs-desc { color: var(--sageMid); }
"""

# ---------------------------------------------------------------- HOME
HOME_PATHS = ['hero/hero-445-left-text-overlapping-stats', 'services/services-447-four-photos-overlapping-cards',
              'about/about-457-image-right-overlapping-card', 'stats/stats-479-stats-bar-split-image-right',
              'reviews/reviews-510-two-cards-bottom-accent-bar', 'stats/stats-16-photo-band-stats-with-button']
HOME_OVR = """
#hero-445 .cs-background:before { background: var(--olive); opacity: .55; }
#hero-445 .cs-tag { background-color: var(--sage); color: var(--olive); font-weight: 800; }
#hero-445 .cs-content .cs-button-2 { margin-top: 2rem; }
#hero-445 .cs-number { color: var(--olive); }
#services-447 { background-color: #fff; }
#services-447 .cs-wrapper { background-color: var(--sageLight); border-color: var(--sage); }
#services-447 .cs-link { color: var(--brown); font-weight: 800; }
#sbsr-457 { background-color: var(--sageLight); }
#stats-479 { background-color: var(--olive); }
#stats-479 .cs-number { color: #fff; }
#stats-479 .cs-desc { color: var(--sageMid); }
#services-479 { background-color: #fff; }
#services-479 .cs-cta { background-color: var(--brown); }
#services-479 .cs-icon-wrap { background-color: var(--sageLight); border-color: var(--sage); }
#services-479 .cs-item { border-color: var(--sage); }
#services-479 .cs-link { color: var(--brown); font-weight: 800; }
#reviews-510 { background-color: var(--sage); }
#reviews-510 .cs-topper { color: var(--olive); }
#reviews-510 .cs-content .cs-text { color: var(--olive); font-weight: 600; }
#reviews-510 .cs-item { border-bottom-color: var(--brown); }
#reviews-510 .cs-job { color: var(--bodyTextColor); }
""" + STATS16_OVR

def hero():
    h = section('hero/hero-445-left-text-overlapping-stats', [
        ('<span class="cs-tag">Tag Example</span>', '<span class="cs-tag">Lexington, KY &bull; Since 2009</span>'),
        ('Solutions we crafted to make human lives easier.', 'Beautiful Yards, Done Right Every Season'),
        ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut.',
         'Weekly lawn care, landscape design and stone patios from a local crew that shows up on time and treats your property like their own.'),
        ('Satisfied Customers in Bartown, MA', 'Yards cared for across Central Kentucky'),
        ('<span class="cs-number">18k+</span>', '<span class="cs-number">1,200+</span>'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Hero/leaf-bg.jpg" alt="leaf"', f'src="{IMG["leaf_bg"]}" alt="" fetchpriority="high"'),
    ])
    # one button style: the component's round "Get Free Quote" link becomes the site's Call Now button
    h, n = re.subn(r'\s*<a href="[^"]*" class="cs-cta">.*?</a>', '', h, count=1, flags=re.S)
    assert n == 1
    h = h.replace('</p>\n        </div>', f'</p>\n            <a href="{TEL}" class="cs-button-2">Call Now</a>\n        </div>', 1)
    assert 'cs-button-2' in h
    return h

HOME_BODY = hero() + section('services/services-447-four-photos-overlapping-cards', [
    ('<span class="cs-topper">Services</span>', '<span class="cs-topper">What We Do</span>'),
    ('Landscaping Services in Sometown, USA', 'Landscaping Services in Lexington, KY'),
    ('Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit. Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit.',
     'From weekly mowing to a complete backyard makeover, one local crew handles it all. Every project starts with a free on-site estimate.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Services/tree.svg" alt="icon"', f'src="{icon("leaf")}" alt=""'),
    ('Service 1', 'Lawn Care'), ('Lorem ipsum dolor sit amet, consectetur.', 'Mowing, edging, fertilizing and weed control.'), ('Read More', 'Call Now'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Services/truck.svg" alt="icon"', f'src="{icon("tree")}" alt=""'),
    ('Service 1', 'Landscape Design'), ('Lorem ipsum dolor sit amet, consectetur.', 'Planting plans, beds and shrubs built for Kentucky.'), ('Read More', 'Call Now'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Services/user.svg" alt="icon"', f'src="{icon("scissors")}" alt=""'),
    ('Service 1', 'Trimming &amp; Pruning'), ('Lorem ipsum dolor sit amet, consectetur.', 'Shrubs, hedges and small trees shaped and healthy.'), ('Read More', 'Call Now'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Services/sticker.svg" alt="icon"', f'src="{icon("grid")}" alt=""'),
    ('Service 1', 'Patios &amp; Walkways'), ('Lorem ipsum dolor sit amet, consectetur.', 'Stone patios, paths and retaining walls.'), ('Read More', 'Call Now'),
    ('alt="leaf" width="345" height="428"', 'alt="" width="345" height="428"'), ('alt="grass" width="345" height="428"', 'alt="" width="345" height="428"'),
    ('alt="leaves" width="345" height="428"', 'alt="" width="345" height="428"'), ('alt="path" width="345" height="428"', 'alt="" width="345" height="428"'),
], empty_links_to=TEL) + section('about/about-457-image-right-overlapping-card', [
    ('<span class="cs-topper">Features</span>', '<span class="cs-topper">Full-Service Landscaping</span>'),
    ('Landscape Renovation And Maintenance ', 'Landscape Renovation and Maintenance'),
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Nunc lobortis mattis aliquam faucibus purus in. Diam ut venenatis tellus in metus vulputate eu. Massa vitae tortor condimentum lacinia quis vel eros donec ac.',
     'Whether your yard needs a fresh start or steady upkeep, we bring the plan, the plants and the crew. We redesign tired beds, fix drainage, lay new sod, and then keep everything looking sharp with weekly or bi-weekly visits.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/SideBySide/grass2.jpg" alt="grass"', f'src="{IMG["grass2"]}" alt="Close-up of healthy green lawn grass"'),
]) + section('stats/stats-479-stats-bar-split-image-right', [
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Stats/codestitch.svg"', f'src="{icon("tree", "sage")}"'),
    ('<span class="cs-number">100+</span>', '<span class="cs-number">350+</span>'),
    ('Landscape Renovations Completed', 'Landscape Renovations Completed'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Stats/codestitch.svg"', f'src="{icon("award", "sage")}"'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Stats/codestitch.svg"', f'src="{icon("star", "sage")}"'),
    ('From 34 Google Ratings', 'From 280+ Google Reviews'),
    ('<a class="cs-cta" href="">', '<a class="cs-cta" href="#reviews-510">'),
    ('src="https://csimg.nyc3.digitaloceanspaces.com/SideBySide/arrow.svg"', f'src="{icon("arrow", "white")}"'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/SideBySide/tall-grass.jpg" alt="grass"', f'src="{IMG["tall_grass"]}" alt=""'),
    ('<span class="cs-topper">Features</span>', '<span class="cs-topper">Seasonal Care</span>'),
    ('Side by Side Section Example Right ', 'A Yard That Looks Great All Year'),
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ',
     'Kentucky yards need different care every season. Our maintenance plans adjust as the weather changes, so you never have to think about it.'),
    ('src="https://csimg.nyc3.digitaloceanspaces.com/SideBySide/geen1.svg"', f'src="{icon("sun")}"'), ('alt="moon"', 'alt=""'),
    ('Service 1', 'Spring &amp; Summer'),
    ('Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis, sapiente.', 'Aeration, overseeding, mulch and weekly mowing.'),
    ('Read More', 'Call Now'),
    ('src="https://csimg.nyc3.digitaloceanspaces.com/SideBySide/geen1.svg"', f'src="{icon("leaf")}"'), ('alt="moon"', 'alt=""'),
    ('Service 1', 'Fall &amp; Winter'),
    ('Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis, sapiente.', 'Leaf cleanup, winterizing and snow-ready beds.'),
    ('Read More', 'Call Now'),
], empty_links_to=TEL) + section('reviews/reviews-510-two-cards-bottom-accent-bar', [
    ('<span class="cs-topper">Reviews</span>', '<span class="cs-topper">Reviews</span>'),
    ('What People Say', 'What Our Neighbors Say'),
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
     'Over 280 five-star Google reviews from homeowners across Lexington and the surrounding counties.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Reviews/quote-left-green.svg"', 'src="assets/quote.svg"'),
    ('This platform is one of the best companies I have dealt with in Indonesia. They’re always happy to help, and i wouldn’t hesitate to recommend them.',
     'Hollow Creek turned our muddy backyard into a patio and garden we use every single night. The crew was friendly, on time and spotless.'),
    ('alt="profile" width="50" height="50" aria-hidden="true"', 'alt="" width="50" height="50" aria-hidden="true"'),
    ('Anne Brown', 'Rachel M.'), ('Landscape Web Customer', 'Homeowner, Hamburg'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Reviews/quote-left-green.svg"', 'src="assets/quote.svg"'),
    ('This platform is one of the best companies I have dealt with in Indonesia. They’re always happy to help, and i wouldn’t hesitate to recommend them.',
     'We&rsquo;ve had them on weekly mowing for three years. The lawn has never looked better and I haven&rsquo;t touched a mower since.'),
    ('alt="profile" width="50" height="50" aria-hidden="true"', 'alt="" width="50" height="50" aria-hidden="true"'),
    ('Anne Brown', 'Greg T.'), ('Landscape Web Customer', 'Homeowner, Chevy Chase'),
]) + stats_band([('15+', 'Years in Business'), ('1,200+', 'Yards Maintained'), ('4.9', 'Google Rating'), ('350+', 'Landscape Projects')])

# ---------------------------------------------------------------- ABOUT
ABOUT_PATHS = ['page-banner/page-banner-559-tinted-photo-band-left-title', 'about/about-466-circle-left-five-icon-cards',
               'why-choose-us/why-choose-us-1631-image-left-three-icon-columns', 'reviews/reviews-2418-photo-band-rated-card-right']
ABOUT_OVR = BANNER_OVR + """
#sbs-466 { background-color: #fff; }
#sbs-466 .cs-picture:before { background-color: var(--sage); }
#services-466 { background-color: #fff; }
#services-466 .cs-item { border-color: var(--sageMid); }
#services-466 .cs-item:hover { border-color: var(--olive); }
#why-choose-1631 { background-color: var(--sageLight); }
#why-choose-1631 .cs-wrapper { background-color: var(--sage); }
#reviews-2418 .cs-background:before { background: var(--olive); opacity: .35; }
#reviews-2418 .cs-card { background-color: var(--sageLight); }
#reviews-2418 .cs-topper { color: var(--brown); }
"""
ABOUT_BODY = banner('About Us', 'Rooted in Lexington Since 2009', 'About', 'garden') + section('about/about-466-circle-left-five-icon-cards', [
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/SideBySide/landscaping1.jpg" alt="leaf"', f'src="{IMG["garden"]}" alt="Freshly planted garden bed"'),
    ('Small Group Training', 'Our Story'),
    ('Make your circle healthier Together', 'From One Mower to a Full Landscaping Team'),
    ('Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit. Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit. Lorem ipsum dolor sit, amet consectetur adipisicing elit. Commodi, nam!',
     'Owner Luis Ortega started Hollow Creek in 2009 with one mower, a borrowed trailer and a handful of neighbors&rsquo; yards. Today our crews care for more than 1,200 properties across Central Kentucky, but every yard still gets the same attention as those first ones.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/SideBySide/geen1.svg"', f'src="{icon("clock")}"'), ('Service 1', 'On-Time Crews'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/SideBySide/green2.svg"', f'src="{icon("shield")}"'), ('Service 2', 'Licensed &amp; Insured'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/SideBySide/green3.svg"', f'src="{icon("leaf")}"'), ('Service 3', 'Eco-Friendly Care'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/SideBySide/green4.svg"', f'src="{icon("users")}"'), ('Service 4', 'Family Owned'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/SideBySide/green5.svg"', f'src="{icon("award")}"'), ('Service 5', 'Satisfaction Guaranteed'),
]) + section('why-choose-us/why-choose-us-1631-image-left-three-icon-columns', [
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/meeting-8.jpg" alt="therapy"', f'src="{IMG["path"]}" alt="Stone garden path through planted beds"'),
    ('Experience the Immersive Impact of Stitch Consulting Services on Your Business', 'Why Homeowners Choose Hollow Creek'),
    ('Aqestic recusandae laudantium optio amet a quisquam saepe aliquid, voluptate praesentium dicta fuga dolor error perspiciatis voluptatem eum cupiditate totam reiciendis quam minus inventore sint rem impedit esse quasi.',
     'There are plenty of lawn companies. Here&rsquo;s why our customers stay with us year after year.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/chat-gold.svg"', f'src="{icon("message", "white")}"'), ('Answer a Few Questions', 'One Point of Contact'),
    ('We welcome and celebrate different perspectives to help our firm, our clients and our people achieve adip iscing elit enduring results.',
     'You get a dedicated crew lead who knows your yard and answers the phone when you call.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/call-gold.svg"', f'src="{icon("calendar", "white")}"'), ('Complimentary Call', 'Same Day, Every Week'),
    ('We welcome and celebrate different perspectives to help our firm, our clients and our people achieve adip iscing elit enduring results.',
     'Maintenance visits happen on a set schedule, so you always know when we&rsquo;ll be there.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/money-gold.svg"', f'src="{icon("check", "white")}"'), ('Grow Your Wealth', 'Honest, Upfront Pricing'),
    ('We welcome and celebrate different perspectives to help our firm, our clients and our people achieve adip iscing elit enduring results.',
     'Free written estimates with no surprise fees. If something isn&rsquo;t right, we come back and fix it.'),
]).replace('<section id="why-choose-1631">', '<section id="why-choose-1631">\n    <span id="why"></span>', 1) + section(
    'reviews/reviews-2418-photo-band-rated-card-right', [
    ('<h2 class="cs-topper">Happy Clients Speak</h2>', '<h2 class="cs-topper">Happy Clients Speak</h2>'),
    ('Poop Patrol Stitches has been a game-changer for us! The team is always punctual, professional, and leaves our yard spotless. Highly recommend their services to every pet owner.',
     'Hollow Creek has been a game-changer for us! The team is always punctual, professional, and leaves our yard spotless. We recommend them to every neighbor who asks.'),
    ('src="https://nyc3.digitaloceanspaces.com/csimages2/Images/People/reviewbg-pet-services-840x840.jpg"', f'src="{IMG["profile1"]}"'),
    ('Jenny Y.', 'Jenny Y.'),
    ('src="https://nyc3.digitaloceanspaces.com/csimages2/Images/People/reviewbg-pet-services-1800x1350.jpg"', f'src="{IMG["house1"]}"'),
]).replace('<section id="reviews-2418">', '<section id="reviews-2418">\n    <span id="reviews"></span>', 1)

# ---------------------------------------------------------------- SERVICES
SERVICES_PATHS = ['page-banner/page-banner-559-tinted-photo-band-left-title', 'services/services-1131-two-by-two-side-icon-cards',
                  'steps/steps-2128-divided-icon-steps-corner-art', 'faq/faq-709-divided-accordion-beside-photo',
                  'stats/stats-16-photo-band-stats-with-button']
SERVICES_OVR = BANNER_OVR + """
#services-1131 { background-color: #fff; }
#services-1131 .cs-item { background-color: var(--sageLight); }
#services-1131 .cs-icon { z-index: 2; }
#steps-2128 { background-color: var(--sage); }
#steps-2128 .cs-topper { color: var(--olive); }
#steps-2128 .cs-item-text { color: var(--olive); font-weight: 600; }
#steps-2128 .cs-graphic { opacity: .35; }
#faq-709 { background-color: var(--sageLight); }
#faq-709 .cs-faq-item.active .cs-button, #faq-709 .cs-button:hover { color: var(--brown); }
""" + STATS16_OVR
SERVICES_BODY = banner('Our Services', 'Landscaping &amp; Lawn Care Services', 'Services', 'grass') + section('services/services-1131-two-by-two-side-icon-cards', [
    ('We Are Here to Help Them', 'Everything Your Yard Needs, One Call'),
    ('Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatem quia odit omnis eligendi libero porro quisquam delectus, dolore maiores qui minus suscipit optio.',
     'Pick one service or bundle them into a year-round plan. Every job starts with a free on-site estimate.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/charity4.svg" alt="icon"', f'src="{icon("leaf", "white")}" alt=""'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/charity-shape.svg" alt="graphic"', 'src="assets/blob.svg" alt=""'),
    ('Healthy Food', 'Lawn Care &amp; Mowing'),
    ('We help companies develop powerful corporate social responsibility, grantmaking, and employee engagement strategies.',
     'Weekly or bi-weekly mowing, edging, blowing, fertilization and weed control programs for a thick, green lawn.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/charity5.svg" alt="icon"', f'src="{icon("tree", "white")}" alt=""'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/charity-shape.svg" alt="graphic"', 'src="assets/blob.svg" alt=""'),
    ('Kids Education', 'Landscape Design &amp; Planting'),
    ('We help companies develop powerful corporate social responsibility, grantmaking, and employee engagement strategies.',
     'Custom planting plans, new beds, shrubs, trees and sod, designed for Kentucky soil and your budget.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/charity6.svg" alt="icon"', f'src="{icon("grid", "white")}" alt=""'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/charity-shape.svg" alt="graphic"', 'src="assets/blob.svg" alt=""'),
    ('Medical Care', 'Hardscapes &amp; Patios'),
    ('We help companies develop powerful corporate social responsibility, grantmaking, and employee engagement strategies.',
     'Stone patios, walkways, fire pits and retaining walls built to last, with drainage done right.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/charity7.svg" alt="icon"', f'src="{icon("droplet", "white")}" alt=""'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/charity-shape.svg" alt="graphic"', 'src="assets/blob.svg" alt=""'),
    ('Medical Care', 'Cleanups &amp; Irrigation'),
    ('We help companies develop powerful corporate social responsibility, grantmaking, and employee engagement strategies.',
     'Spring and fall cleanups, mulching, leaf removal and sprinkler startup, repair and winterizing.'),
]).replace('<section id="services-1131">', '<section id="services-1131">\n    <span id="services"></span>', 1) + section('steps/steps-2128-divided-icon-steps-corner-art', [
    ('Perfect Photography at Your Doorstep', 'How It Works'),
    ('Your Wedding Memory will be More Memorable with Our Photography', 'From First Call to a Yard You Love'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/layer.svg"', f'src="{icon("phone", "white")}"'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/orange-shape.svg"', 'src="assets/blob-olive.svg"'),
    ('Perfect Arrangement', '1. Call Us'), ('Choose from our range of Photo booth options.', 'Tell us what you have in mind and we&rsquo;ll set a time to visit.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/snowflake.svg"', f'src="{icon("pin", "white")}"'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/orange-shape.svg"', 'src="assets/blob-olive.svg"'),
    ('The Wedding Bliss', '2. Free Estimate'), ('Choose from our range of Photo booth options.', 'We walk your property and send a written quote within 48 hours.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/two-users.svg"', f'src="{icon("users", "white")}"'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/orange-shape.svg"', 'src="assets/blob-olive.svg"'),
    ('Just The Two of Us', '3. We Get to Work'), ('Choose from our range of Photo booth options.', 'Our crew completes the job on schedule and cleans up after.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/heart-outline.svg"', f'src="{icon("sun", "white")}"'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/orange-shape.svg"', 'src="assets/blob-olive.svg"'),
    ('Make With Love', '4. Enjoy Your Yard'), ('Choose from our range of Photo booth options.', 'Relax while we keep it looking great every season.'),
]) + section('faq/faq-709-divided-accordion-beside-photo', [
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images%2FLandscapes%2Frocks.jpg" alt="rocks"', f'src="{IMG["leaves"]}" alt=""'),
    ('Asked questions', 'FAQ'),
    ('How much are house painting services?', 'How much does weekly lawn care cost?'),
    ('Some cleaning plans require a minimum commitment term. Cancelling your plan before the minimum term is complete will result in a $99 fee. If you want to learn more information about how to cancel, please inbox us.',
     'Most Lexington lawns run $35 to $55 per weekly visit, depending on size. We&rsquo;ll give you an exact price after a free walk-through.'),
    ('What is your plan cancellation policy?', 'Do I have to sign a contract?'),
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sit convallis nunc neque, bibendum pulvinar vitae commodo velit. Proin diam tortor sed malesuada nunc, habitant. Dignissim ipsum porta enim, magna urna, quam. ',
     'No. Maintenance plans are month to month. Most customers stay because they like the results, not because they have to.'),
    ('How long should a house painting take?', 'How long does a patio project take?'),
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sit convallis nunc neque, bibendum pulvinar vitae commodo velit. Proin diam tortor sed malesuada nunc, habitant. Dignissim ipsum porta enim, magna urna, quam. ',
     'Most patios and walkways are finished in three to five days, weather permitting. We&rsquo;ll give you a schedule with your estimate.'),
    ('How much are house painting services?', 'Are you licensed and insured?'),
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sit convallis nunc neque, bibendum pulvinar vitae commodo velit. Proin diam tortor sed malesuada nunc, habitant. Dignissim ipsum porta enim, magna urna, quam. ',
     'Yes. Hollow Creek is fully insured, and our team includes certified horticulturists and a licensed pesticide applicator.'),
    ('How much are house painting services?', 'What areas do you serve?'),
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sit convallis nunc neque, bibendum pulvinar vitae commodo velit. Proin diam tortor sed malesuada nunc, habitant. Dignissim ipsum porta enim, magna urna, quam. ',
     'Lexington and the surrounding area, including Nicholasville, Georgetown, Versailles, Winchester and Paris.'),
]).replace('<section id="faq-709">', '<section id="faq-709">\n    <span id="faq"></span>', 1) + stats_band(
    [('Free', 'On-Site Estimates'), ('48h', 'Quote Turnaround'), ('0', 'Contracts Required'), ('100%', 'Satisfaction Guarantee')])

# ---------------------------------------------------------------- GALLERY
GALLERY_PATHS = ['page-banner/page-banner-559-tinted-photo-band-left-title', 'gallery/gallery-45-four-column-grid-with-button',
                 'gallery/gallery-377-rounded-four-column-hover-grid']
GALLERY_OVR = BANNER_OVR + """
#gallery-45 { background-color: #fff; }
#gallery-377 { background-color: var(--sage); }
#gallery-377 .cs-topper { color: var(--olive); }
#gallery-377 .cs-content .cs-text { color: var(--olive); font-weight: 600; }
#gallery-377 .cs-hover-box { background-color: rgba(59, 64, 19, .82); }
"""
FINISHED = [('house1', 'Front yard with fresh landscaping'), ('house2', 'Modern home with new lawn'), ('house3', 'Landscaped front entry'),
            ('house4', 'Backyard with new plantings'), ('house5', 'Evening view of a landscaped home'), ('house6', 'Finished front lawn and beds'),
            ('house3b', 'Home with trimmed hedges'), ('house5b', 'Front yard renovation')]
DETAILS = [('leaf', 'Planting', 'Healthy shrub foliage'), ('grass', 'Lawn Care', 'Thick green lawn'), ('leaves', 'Garden Beds', 'Layered garden plants'),
           ('path', 'Walkways', 'Stone garden path'), ('grass2', 'Sod Install', 'New sod'), ('tall_grass', 'Ornamental Grasses', 'Ornamental grass planting'),
           ('garden', 'Garden Design', 'Raised garden bed'), ('rocks', 'Hardscapes', 'Natural stone accents')]

def gallery45():
    h = section('gallery/gallery-45-four-column-grid-with-button', [
        ('<span class="cs-topper">Service</span>', '<span class="cs-topper">Finished Properties</span>'),
        ('Landscaping Services in Sometown, USA', 'Recent Projects Around Lexington'),
        ('Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit. Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit.',
         'Full yard renovations and ongoing maintenance from the past few seasons. Your property could be next.'),
    ])
    start = 0
    for key, alt in FINISHED:
        i = h.index('<picture class="cs-picture">', start)
        j = h.index('</picture>', i) + len('</picture>')
        new = f'<picture class="cs-picture">\n                        <img loading="lazy" decoding="async" src="{IMG[key]}" alt="{alt}" width="346" height="346">\n                    </picture>'
        h = h[:i] + new + h[j:]
        start = i + len(new)
    return h

def gallery377():
    h = section('gallery/gallery-377-rounded-four-column-hover-grid', [
        ('Our Portfolio', 'Up Close'), ('Some Work from Our Memorable Gallery', 'The Details Make the Difference'),
        ('At Stitch Cleaning Service, let us help you solve problems so that you can focus on your mission. We support businesses through periods of expansion, succession.',
         'Clean edges, healthy plants and stonework that lasts. Hover over a photo to see the service behind it.'),
    ], empty_links_to='services.html#services')
    start = 0
    for key, title, alt in DETAILS:
        i = h.index('<h3 class="cs-h3">House Cleaning</h3>', start)
        h = h[:i] + f'<h3 class="cs-h3">{title}</h3>' + h[i + len('<h3 class="cs-h3">House Cleaning</h3>'):]
        i = h.index('<picture class="cs-image">', i)
        j = h.index('</picture>', i) + len('</picture>')
        new = f'<picture class="cs-image">\n                    <img loading="lazy" decoding="async" src="{IMG[key]}" alt="{alt}" width="305" height="400">\n                </picture>'
        h = h[:i] + new + h[j:]
        start = i + len(new)
    h = h.replace('src="https://csimg.nyc3.digitaloceanspaces.com/Gallery/arrows.svg"', f'src="{icon("arrow", "white")}"')
    assert 'House Cleaning' not in h and 'Gallery/gallery' not in h
    return h

GALLERY_BODY = banner('Our Work', 'Project Gallery', 'Gallery', 'house2') + gallery45() + gallery377()

# ---------------------------------------------------------------- CONTACT
CONTACT_PATHS = ['page-banner/page-banner-559-tinted-photo-band-left-title', 'contact/contact-325-dark-three-icon-info-row',
                 'steps/steps-1172-light-four-icon-steps-arrows', 'locations/locations-720-full-width-map-band']
CONTACT_OVR = BANNER_OVR + """
#contact-strip-325 { background-color: var(--olive); }
#contact-strip-325 .cs-header { color: var(--sageMid); }
#contact-strip-325 .cs-link, #contact-strip-325 .cs-hours { color: var(--bodyTextColorWhite); }
#contact-strip-325 .cs-picture { border-color: var(--sage); }
#contact-strip-325 .cs-icon { width: 2rem; height: auto; }
#steps-1172 { background-color: var(--sageLight); }
#steps-1172 .cs-picture { border-color: var(--olive); background-color: #fff; }
#steps-1172 .cs-graphic { opacity: .4; }
#steps-1172 .cs-call { text-align: center; margin-top: clamp(2rem, 4vw, 3rem); }
"""
def steps1172():
    h = section('steps/steps-1172-light-four-icon-steps-arrows', [
        ('Our Work Process', 'What Happens When You Call'),
        ('How To Get Started', 'Getting Started Is Easy'),
        ('Lorem ipsum dolor, sit amet consectetur adipisicing elit. Culpa libero sint hic accusantium exercitationem, voluptatem officia quaerat velit quis ullam?',
         'No forms and no runaround. One phone call gets your free estimate on the calendar.'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/lightbulb-red.svg"', f'src="{icon("phone")}"'), ('Identify Issues', 'You Call'),
        ('Extensible for web iterate process before meta services impact with employee engagement strategies.', 'A real person answers, Monday through Saturday, 7am to 6pm.'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/puzzle-red.svg"', f'src="{icon("calendar")}"'), ('Prepare Solution', 'We Visit'),
        ('Extensible for web iterate process before meta services impact with employee engagement strategies.', 'We walk your property with you, usually within the week.'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/gears-red.svg"', f'src="{icon("message")}"'), ('Working On This', 'You Get a Quote'),
        ('Extensible for web iterate process before meta services impact with employee engagement strategies.', 'A clear written estimate lands in your inbox within 48 hours.'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/box-red.svg"', f'src="{icon("sun")}"'), ('Deliver On Hand', 'We Get to Work'),
        ('Extensible for web iterate process before meta services impact with employee engagement strategies.', 'Pick a start date and our crew takes it from there.'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Graphics/tire-mark.svg" alt="icon"', 'src="assets/swoosh.svg" alt=""'),
    ])
    return h

CONTACT_BODY = banner('Contact', 'Get Your Free Estimate', 'Contact', 'tall_grass') + section('contact/contact-325-dark-three-icon-info-row', [
    ('src="https://csimg.nyc3.digitaloceanspaces.com/Contact-Page/phone-gold.svg" alt="icon"', f'src="{icon("phone", "sage")}" alt=""'),
    ('<a href="tel:555-456-7899" class="cs-link">+1 (555) 456 7899</a>', f'<a href="{TEL}" class="cs-link">{PHONE}</a>'),
    ('<a href="tel:555-456-7899" class="cs-link">+1 (555) 456 7899</a>', f'<a href="mailto:{EMAIL}" class="cs-link">{EMAIL}</a>'),
    ('src="https://csimg.nyc3.digitaloceanspaces.com/Contact-Page/pin-gold.svg" alt="icon"', f'src="{icon("pin", "sage")}" alt=""'),
    ('<a href="" class="cs-link">123 Fake St, STE 100 <br> Somewhere, FL 98755</a>', f'<a href="#map-720" class="cs-link">{ADDRESS_1} <br> {ADDRESS_2}</a>'),
    ('src="https://csimg.nyc3.digitaloceanspaces.com/Contact-Page/clock-gold.svg" alt="icon"', f'src="{icon("clock", "sage")}" alt=""'),
    ('Monday To Saturday', 'Monday to Saturday'), ('9:00 AM - 10:30 PM', '7:00 AM - 6:00 PM'),
]).replace('<span class="cs-header">Phone</span>', '<span class="cs-header">Phone &amp; Email</span>', 1) + steps1172() + section(
    'locations/locations-720-full-width-map-band', [
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons%2Fred-pin.svg"', 'src="assets/pin.svg"'),
    ('alt="map" width="1280" height="600"', f'alt="Map showing {BIZ} at {ADDRESS_1}, {ADDRESS_2}" width="1280" height="600"'),
])

# ---------------------------------------------------------------- assets
ICONS = {
    'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    'mail': '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
    'pin': '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    'leaf': '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    'tree': '<path d="M12 2 5 12h4l-3 5h12l-3-5h4z"/><line x1="12" y1="17" x2="12" y2="22"/>',
    'scissors': '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/>',
    'grid': '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>',
    'droplet': '<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>',
    'sun': '<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>',
    'users': '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    'award': '<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>',
    'star': '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
    'message': '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    'calendar': '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    'check': '<polyline points="20 6 9 17 4 12"/>',
    'chevron': '<polyline points="6 9 12 15 18 9"/>',
    'arrow': '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
}
COLORS = {'olive': '#3B4013', 'brown': '#402C1A', 'sage': '#9DA65D', 'white': '#FFFFFF'}
LOGO_TMPL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 250 52" width="250" height="52">
<path d="M26 47C12 47 5 36 7 22 18 22 27 29 26 47Z" fill="{leaf1}"/>
<path d="M26 47C26 30 33 16 46 9 50 27 42 44 26 47Z" fill="{leaf2}"/>
<path d="M26 47C27 37 32 27 41 19" fill="none" stroke="{vein}" stroke-width="2" stroke-linecap="round"/>
<text x="56" y="28" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="700" letter-spacing=".4" fill="{text}">HOLLOW CREEK</text>
<text x="57" y="45" font-family="Arial, Helvetica, sans-serif" font-size="10.5" font-weight="700" letter-spacing="2.6" fill="{sub}">LAWN &amp; LANDSCAPE</text>
</svg>'''
FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48"><rect width="48" height="48" rx="10" fill="#3B4013"/>
<path d="M24 42C11 42 6 32 8 20 18 20 25 27 24 42Z" fill="#9DA65D"/><path d="M24 42C24 27 30 14 41 8 45 24 38 39 24 42Z" fill="#DDE2BD"/></svg>'''
QUOTE = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 46" width="40" height="46"><path fill="#402C1A" d="M0 26C0 13 6 5 17 2l2 5c-6 2-9 6-9 11h8v18H0zM22 26C22 13 28 5 39 2l1 5c-6 2-9 6-9 11h8v18H22z"/></svg>'
BLOB = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 103" width="100" height="103"><path fill="{c}" d="M52 3c20 1 40 13 45 33s-4 44-22 56S30 107 14 92 -3 52 6 32 32 2 52 3z"/></svg>'
PIN = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80"><path fill="#402C1A" d="M40 4C25 4 13 16 13 31c0 20 27 45 27 45s27-25 27-45C67 16 55 4 40 4z"/><circle cx="40" cy="31" r="10" fill="#DDE2BD"/></svg>'
SWOOSH = ''.join(f'<path d="M0 {200+i*14} C 200 {40+i*14}, 420 {360+i*14}, 840 {120+i*14}"/>' for i in range(10))
SWOOSH = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 357" width="840" height="357" fill="none" stroke="#9DA65D" stroke-width="2" stroke-opacity=".7">{SWOOSH}</svg>'
WAVES = ''.join(f'<path d="M0 {150+i*18} C 320 {60+i*18}, 640 {240+i*18}, 1280 {110+i*18}"/>' for i in range(8))
WAVES = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 278" width="1280" height="278" preserveAspectRatio="none" fill="none" stroke="#3B4013" stroke-width="2" stroke-opacity=".18">{WAVES}</svg>'

# ---------------------------------------------------------------- write
def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(text)

for name, body in ICONS.items():
    for cname, col in COLORS.items():
        write(f'assets/icons/{name}-{cname}.svg', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')
write('assets/logo.svg', LOGO_TMPL.format(leaf1='#9DA65D', leaf2='#3B4013', vein='#EEF0DF', text='#3B4013', sub='#402C1A'))
write('assets/logo-light.svg', LOGO_TMPL.format(leaf1='#9DA65D', leaf2='#DDE2BD', vein='#3B4013', text='#FFFFFF', sub='#DDE2BD'))
write('assets/favicon.svg', FAVICON)
write('assets/quote.svg', QUOTE)
write('assets/blob.svg', BLOB.format(c='#3B4013'))
write('assets/blob-olive.svg', BLOB.format(c='#3B4013'))
write('assets/pin.svg', PIN)
write('assets/swoosh.svg', SWOOSH)
write('assets/cta-waves.svg', WAVES)

write('css/root.css', shared_css())
write('css/home.css', page_css(HOME_PATHS, HOME_OVR, STATS16_CSS))
write('css/about.css', page_css(ABOUT_PATHS, ABOUT_OVR))
write('css/services.css', page_css(SERVICES_PATHS, SERVICES_OVR, STATS16_CSS))
write('css/gallery.css', page_css(GALLERY_PATHS, GALLERY_OVR))
write('css/contact.css', page_css(CONTACT_PATHS, CONTACT_OVR))

write('js/nav.js', js('nav/nav-1343-light-over-dark-rows-dropdown'))
write('js/faq.js', js('faq/faq-709-divided-accordion-beside-photo'))
write('js/year.js', YEAR_JS)

write('index.html', page('index.html', f'Landscaping &amp; Lawn Care in Lexington, KY | {BIZ}', 'home.css', HOME_BODY))
write('about.html', page('about.html', f'About Us | {BIZ}', 'about.css', ABOUT_BODY))
write('services.html', page('services.html', f'Landscaping Services | {BIZ}', 'services.css', SERVICES_BODY, ('faq.js',)))
write('gallery.html', page('gallery.html', f'Project Gallery | {BIZ}', 'gallery.css', GALLERY_BODY))
write('contact.html', page('contact.html', f'Contact Us | {BIZ}', 'contact.css', CONTACT_BODY))
print('built', os.path.normpath(OUT))
