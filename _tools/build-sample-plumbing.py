#!/usr/bin/env python3
"""Builds the Critchfield Systems plumbing sample (critchfield-systems/sample-plumbing/):
a fictional plumbing company, "Limestone Plumbing & Drain", made from sections in the
DeveloperDadd/components library (none of them reused from the roofing or landscaping
samples, or from the Critchfield Systems site itself).

Usage: python3 _tools/build-sample-plumbing.py /path/to/components

Rules the build enforces: one button style (components/sections/button/button1) and every
button is a "Call Now" link; no forms; one H1 per page; no placeholder text left over.
Photos are the placeholder photos that ship with the components (CodeStitch image CDN),
listed in the IMG table below. The phone number is Critchfield Systems' own, so a prospect
who taps Call reaches Clayton."""
import os, re, sys

COMP = os.path.join(sys.argv[1] if len(sys.argv) > 1 else '../components', 'sections')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'critchfield-systems', 'sample-plumbing')

# ---------------------------------------------------------------- business (fictional)
BIZ = 'Limestone Plumbing &amp; Drain'
PHONE = '(859) 270-7050'          # Critchfield Systems' number, so calls reach Clayton
TEL = 'tel:+18592707050'
EMAIL = 'office@limestoneplumbing.example'
AREA = 'Lexington &amp; Central Kentucky'
MAP_EMBED = 'https://maps.google.com/maps?q=Lexington%2C%20KY&amp;z=10&amp;output=embed'

CS_URL = 'https://critchfieldsystems.com'

# ---------------------------------------------------------------- placeholder photos
D = 'https://csimg.nyc3.digitaloceanspaces.com/'
C = 'https://csimg.nyc3.cdn.digitaloceanspaces.com/'
IMG = {
    'kitchen': D + 'Hero/kitchen.jpg', 'kitchen_m': D + 'Hero/kitchen-m.jpg',
    'cabinets': D + 'CTA/cabinets.jpg', 'cabinets_m': D + 'CTA/cabinets-m.jpg',
    'room4': C + 'Hero/room4.jpg', 'room': C + 'SideBySide/room.jpg',
    'room3': C + 'SideBySide/room3.jpg', 'room3_m': C + 'SideBySide/room3-m.jpg',
    'room2': C + 'Contact-Page/room2.jpg', 'room2_m': C + 'Contact-Page/room2-m.jpg',
    'kitchen1': C + 'FAQ/kitchen1.jpg', 'kitchen1_m': C + 'FAQ/kitchen1-m.jpg',
    'living': D + 'Services/living-room2.jpg',
    'worker': C + 'Images/People/mechaninc29.jpg', 'tools': C + 'Images/People/tools.jpg',
    'p1': D + 'Reviews/profile2.jpg', 'p2': 'https://csimages2.nyc3.digitaloceanspaces.com/Reviews/profile3.jpg',
    'p3': 'https://csimages2.nyc3.digitaloceanspaces.com/Reviews/profile5.jpg', 'p4': C + 'Images/People/profile1.jpg',
    'p5': C + 'Images/People/profile8.jpg', 'p6': C + 'Images/People/review-profile.jpg',
}

# ---------------------------------------------------------------- helpers
def raw(path):
    return open(os.path.join(COMP, path, 'index.html')).read()

def css(path):
    return open(os.path.join(COMP, path, 'style.css')).read()

def js(path):
    return open(os.path.join(COMP, path, 'script.js')).read()

def call_now(h):
    """The one button on this site: every .cs-button-1 is a Call Now link to the business."""
    def fix(m):
        cls = re.search(r'class="(cs-button-1[^"]*)"', m.group(0)).group(1)
        return f'<a href="{TEL}" class="{cls}">Call Now</a>'
    return re.sub(r'<a\b[^>]*class="cs-button-1[^"]*"[^>]*>.*?</a>', fix, h, flags=re.S)

def seq(h, pattern, values, where=''):
    """Replace group 1 of each successive match of pattern with the next value."""
    matches = list(re.finditer(pattern, h, flags=re.S))
    assert len(matches) == len(values), f'{where}: {pattern!r} matched {len(matches)}, expected {len(values)}'
    for m, v in reversed(list(zip(matches, values))):
        h = h[:m.start(1)] + v + h[m.end(1):]
    return h

PLACEHOLDER = r'[Ll]orem ipsum|Amet minim|Curabitur|Facilisis|Extensible|Stitch|Yokoloko|Fake Rd|Manhattan|New York|Ut enim ad|Sed ultricies|Haircut|Vitae ultricies|\(555\)|Info@email'

def section(path, repl, empty_links_to='contact.html', fills=(), allrep=()):
    """Component markup with copy swapped. Each (old, new) in repl replaces the FIRST remaining
    occurrence; each (old, new) in allrep replaces every occurrence; fills are seq() calls."""
    h = raw(path)
    for old, new in allrep:
        assert old in h, f'{path}: text not found: {old[:70]!r}'
        h = h.replace(old, new)
    for old, new in repl:
        if old not in h:
            raise SystemExit(f'{path}: text not found: {old[:70]!r}')
        h = h.replace(old, new, 1)
    for pattern, values in fills:
        h = seq(h, pattern, values, path)
    h = h.replace('class="cs-button-solid', 'class="cs-button-1')
    h = call_now(h)
    if empty_links_to:
        h = h.replace('href=""', f'href="{empty_links_to}"')
    h = h.replace('alt="icon"', 'alt=""')
    left = re.search(PLACEHOLDER, re.sub(r'<!--.*?-->', '', h, flags=re.S))
    if left:
        raise SystemExit(f'{path}: placeholder text left in markup: {left.group(0)!r}')
    return h

def icon(name, color='copper'):
    return f'assets/icons/{name}-{color}.svg'

def anchor(h, sec_id, anchor_id):
    tag = f'<section id="{sec_id}">'
    assert tag in h, tag
    return h.replace(tag, f'{tag}\n    <span id="{anchor_id}"></span>', 1)

def picture(src, alt, w, h, cls='cs-picture', mobile=None, lazy=True):
    load = 'loading="lazy" ' if lazy else ''
    return (f'<picture class="{cls}">\n'
            f'                        <source media="(max-width: 600px)" srcset="{mobile or src}">\n'
            f'                        <source media="(min-width: 601px)" srcset="{src}">\n'
            f'                        <img {load}decoding="async" src="{src}" alt="{alt}" width="{w}" height="{h}">\n'
            f'                    </picture>')

# ---------------------------------------------------------------- shared CSS
ROOT_CSS = """/* Limestone Plumbing & Drain (sample site by Critchfield Systems)
   60-30-10: 60% limestone #F5F1E8 (and white), 30% deep water #0E3A56, 10% copper #A9501A */
:root {
    --stone: #F5F1E8;            /* 60% - page and section backgrounds */
    --stoneMid: #E6DECD;         /* borders, card edges */
    --water: #0E3A56;            /* 30% - headings, dark bands, logo panel, footer */
    --waterDeep: #0A2B40;
    --copper: #A9501A;           /* 10% - the Call Now buttons, toppers, icons */
    --copperLight: #E8A36B;      /* copper on dark backgrounds */
    --primary: #0E3A56;
    --primaryLight: #2F7FA8;
    --secondary: #A9501A;
    --secondaryLight: #E8A36B;
    --headerColor: #0E3A56;
    --bodyTextColor: #44505A;
    --bodyTextColorWhite: #F7F4EE;
    --topperFontSize: clamp(0.8125rem, 1.6vw, 1rem);
    --headerFontSize: clamp(1.9375rem, 3.9vw, 3.0625rem);
    --bodyFontSize: 1rem;
    --sectionPadding: clamp(3.75rem, 7.82vw, 6.25rem) 1rem;
}
html { scroll-behavior: smooth; }
body {
    margin: 0; padding: 0;
    font-family: "Barlow", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    background-color: var(--stone); color: var(--bodyTextColor);
    -webkit-font-smoothing: antialiased;
}
*, *:before, *:after { box-sizing: border-box; }
img { max-width: 100%; }
button { font-family: inherit; }
.cs-topper { font-size: var(--topperFontSize); line-height: 1.2em; text-transform: uppercase; text-align: inherit; letter-spacing: .12em; font-weight: 700; color: var(--copper); margin-bottom: 0.25rem; display: block; }
.cs-title { font-size: var(--headerFontSize); font-weight: 800; line-height: 1.15em; text-align: inherit; max-width: 43.75rem; margin: 0 0 1rem 0; color: var(--headerColor); position: relative; }
.cs-text { font-size: var(--bodyFontSize); line-height: 1.6em; text-align: inherit; width: 100%; max-width: 40.625rem; margin: 0; color: var(--bodyTextColor); }

/*-- The one site button: components/sections/button/button1, as a link (.cs-button-1) --*/
.cs-button-1 {
    --color: #A9501A;
    font-family: inherit;
    display: inline-block;
    min-width: 8em;
    height: 2.75em;
    line-height: 2.6em;
    padding: 0 1.6em;
    margin: 0;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    z-index: 1;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: .02em;
    color: var(--color);
    background-color: #FFFDF9;
    border: 2px solid var(--color);
    border-radius: 6px;
    text-align: center;
    text-decoration: none;
    box-sizing: border-box;
    /* foreground shadow so the button pops off every background */
    box-shadow: 0 1rem 2rem -0.5rem rgba(10, 43, 64, 0.5), 0 0.375rem 0.875rem rgba(169, 80, 26, 0.22);
    transition: color .3s, transform .3s, box-shadow .3s;
}
.cs-button-1::before {
    position: absolute;
    content: "";
    background: var(--color);
    width: 240px;
    height: 240px;
    z-index: -1;
    border-radius: 50%;
    top: 100%;
    left: 100%;
    transition: 0.3s all;
}
.cs-button-1:hover { color: #fff; transform: translateY(-0.1875rem); box-shadow: 0 1.375rem 2.5rem -0.5rem rgba(10, 43, 64, 0.6), 0 0.5rem 1.125rem rgba(169, 80, 26, 0.3); }
.cs-button-1:hover::before { top: -40px; left: -40px; }
.cs-button-1:focus-visible { outline: 3px solid var(--copperLight); outline-offset: 3px; }

.cs-skip { position: absolute; left: 1rem; top: -4rem; z-index: 20000; background: var(--water); color: #fff; padding: .75rem 1rem; text-decoration: none; font-weight: 700; }
.cs-skip:focus { top: 1rem; }
@media (prefers-reduced-motion: reduce) {
    *, *:before, *:after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}
"""

NAV_OVR = """
/* nav: logo on a deep-water panel, demo notice in the top bar */
#cs-navigation { background-color: #fff; }
#cs-navigation .cs-logo { background-color: var(--water); }
#cs-navigation .cs-header { color: var(--copper); font-weight: 700; }
#cs-navigation .cs-link { color: var(--water); font-weight: 700; }
#cs-navigation .cs-picture { background-color: var(--stone); }
#cs-navigation .cs-li-link { color: var(--water); font-weight: 600; }
#cs-navigation .cs-li-link.cs-active, #cs-navigation .cs-li-link:hover { color: var(--copper); }
#cs-navigation .cs-li-link:before { background: var(--copper); }
@media only screen and (max-width: 1023.5px) {
  #cs-navigation .cs-logo { padding: .5rem .75rem; }
  #cs-navigation .cs-ul-wrapper { background-color: #fff; }
  #cs-navigation .cs-toggle { background-color: var(--water); }
  /* the header is fixed on phones: start the page below it */
  main { padding-top: 9rem; }
  /* the component hides its button on phones; it is .cs-button-1 here */
  #cs-navigation .cs-button-1 { display: none; }
  /* keep the sample-site notice visible on phones, wrapped beside the logo */
  #cs-navigation .cs-item.cs-demo .cs-link { display: block; max-width: 12.5rem; text-align: right; font-size: .75rem; line-height: 1.3em; }
}
@media only screen and (min-width: 650px) and (max-width: 1023.5px) {
  main { padding-top: 8rem; }
}
@media only screen and (min-width: 1024px) {
  #cs-navigation .cs-drop-ul { background-color: #fff; }
  #cs-navigation .cs-drop-link { color: var(--water); }
  #cs-navigation .cs-item.cs-demo .cs-link { max-width: 17rem; font-size: .875rem; line-height: 1.3em; }
}
"""

FOOTER_OVR = """
/* footer: deep water (30%) with copper accents */
#cs-footer-1782 { background-color: var(--waterDeep); }
#cs-footer-1782 .cs-topper { color: var(--copperLight); }
#cs-footer-1782 .cs-header { color: #fff; }
#cs-footer-1782 .cs-text, #cs-footer-1782 .cs-link, #cs-footer-1782 .cs-contact-link,
#cs-footer-1782 .cs-table th, #cs-footer-1782 .cs-table td, #cs-footer-1782 .cs-credit,
#cs-footer-1782 .cs-credit-link, #cs-footer-1782 .cs-bottom-link { color: var(--bodyTextColorWhite); }
#cs-footer-1782 .cs-table { background-color: rgba(255, 255, 255, .05); border-top-color: var(--copper); }
#cs-footer-1782 .cs-table tr { border-bottom-color: rgba(255, 255, 255, .12); }
#cs-footer-1782 .cs-credit-link.cs-cs { color: var(--copperLight); font-weight: 700; }
#cs-footer-1782 .cs-link:hover, #cs-footer-1782 .cs-contact-link:hover, #cs-footer-1782 .cs-bottom-link:hover { color: var(--copperLight); }
"""

def shared_css():
    return (ROOT_CSS + '\n' + css('nav/nav-759-two-row-logo-panel-dropdown') + NAV_OVR
            + '\n' + css('footer/footer-1782-dark-columns-with-hours-table') + FOOTER_OVR)

def page_css(paths, overrides, repl=()):
    out = '\n'.join(css(p) for p in paths)
    for a, b in repl:
        assert a in out, a
        out = out.replace(a, b)
    return out + '\n/* ---- brand overrides ---- */\n' + overrides

# ---------------------------------------------------------------- nav + footer
SERVICE_LINKS = [('Drain Cleaning', 'services.html#services'), ('Water Heaters', 'services.html#services'),
                 ('Leak Detection', 'services.html#services'), ('Pricing', 'services.html#pricing'),
                 ('Service FAQ', 'services.html#faq')]

def nav(active):
    h = raw('nav/nav-759-two-row-logo-panel-dropdown')
    rep = [
        ('<a href="" class="cs-logo" aria-label="Return to [Company Name] Home page">', f'<a href="index.html" class="cs-logo" aria-label="Return to {BIZ} home page">'),
        ('src="https://csimg.nyc3.digitaloceanspaces.com/Footer/logo-light.svg" alt="" width="210" height="29"', 'src="assets/logo-light.svg" alt="" width="220" height="64"'),
        # top bar: phone, the sample-site notice, then email (hidden on phones by the component's .cs-remove)
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons%2Fphone-stroke-green.svg"', f'src="{icon("phone")}"'),
        ('<span class="cs-header">Call Us Now</span>', '<span class="cs-header">Call 24/7</span>'),
        ('<a href="tel:555-555-0234" class="cs-link">(555) 555-0234</a>', f'<a href="{TEL}" class="cs-link">{PHONE}</a>'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons%2Fmail-stroke-green.svg"', f'src="{icon("star")}"'),
        ('<span class="cs-header">Send A Message</span>', '<span class="cs-header">Sample Website</span>'),
        ('<a href="mailto:Info@email.com" class="cs-link">Info@email.com</a>', f'<a href="{CS_URL}" class="cs-link">Built by Critchfield Systems. Get yours for $99/mo</a>'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons%2Fpin-stroke-green.svg"', f'src="{icon("mail")}"'),
        ('<span class="cs-header">Visit Us At</span>', '<span class="cs-header">Email Us</span>'),
        ('<a href="" class="cs-link">2492 Fake Rd.</a>', f'<a href="mailto:{EMAIL}" class="cs-link">{EMAIL}</a>'),
    ]
    for o, n in rep:
        assert o in h, o
        h = h.replace(o, n, 1)
    # mark the second top-bar item (the sample-site notice) so it can be styled
    i = h.index('<li class="cs-item">', h.index('<li class="cs-item">') + 1)
    h = h[:i] + '<li class="cs-item cs-demo">' + h[i + len('<li class="cs-item">'):]
    # the link list, rebuilt with the component's own li / dropdown markup
    def li(label, href):
        cur = ' cs-active" aria-current="page' if href == active else ''
        return (f'                        <li class="cs-li">\n'
                f'                            <a href="{href}" class="cs-li-link{cur}">\n'
                f'                                {label}\n'
                f'                            </a>\n'
                f'                        </li>\n')
    drops = ''.join(f'                                <li class="cs-drop-li">\n'
                    f'                                    <a href="{href}" class="cs-li-link cs-drop-link">{label}</a>\n'
                    f'                                </li>\n' for label, href in SERVICE_LINKS)
    svc_active = ' cs-active' if active == 'services.html' else ''
    dropdown = (f'                        <li class="cs-li cs-dropdown">\n'
                f'                            <button class="cs-li-link cs-dropdown-toggle{svc_active}" aria-haspopup="menu" aria-expanded="false" id="services-dropdown-toggle">\n'
                f'                                Services\n'
                f'                                <img class="cs-drop-icon" src="{icon("chevron", "water")}" alt="" width="15" height="15" decoding="async" aria-hidden="true">\n'
                f'                            </button>\n'
                f'                            <ul class="cs-drop-ul" aria-labelledby="services-dropdown-toggle">\n'
                f'{drops}'
                f'                            </ul>\n'
                f'                        </li>\n')
    items = li('Home', 'index.html') + li('About', 'about.html') + dropdown + li('Gallery', 'gallery.html') + li('Contact', 'contact.html')
    h, n = re.subn(r'(<ul class="cs-ul">\n).*?(\s*</ul>\s*</div>\s*</nav>)', lambda m: m.group(1) + items.rstrip('\n') + m.group(2), h, count=1, flags=re.S)
    assert n == 1
    h = h.replace('class="cs-button-solid', 'class="cs-button-1')
    h = call_now(h)
    clean = re.sub(r'<!--.*?-->', '', h, flags=re.S)
    assert 'href=""' not in clean, 'nav has empty link'
    assert not re.search(PLACEHOLDER, clean), 'nav placeholder left'
    return h

def footer():
    rep = [
        ('<a aria-label="go back to home" class="cs-logo" href="">', '<a aria-label="go back to home" class="cs-logo" href="index.html">'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Logos/gym-logo-white.svg" alt="logo" width="240" height="32"', 'src="assets/logo-light.svg" alt="" width="220" height="64"'),
        ('Welcome to Stitch Fitness! We believe that true wellness encompasses the mind, body & soul. We are here to support and guide you every step of the way.',
         'Family-owned plumbing, drain and water heater service for Lexington and Central Kentucky since 2010. Licensed, insured and on call 24/7.'),
        ('<a href="" class="cs-contact-link">+123 458 789412</a>', f'<a href="{TEL}" class="cs-contact-link">{PHONE}</a>'),
        ('<span class="cs-topper">Visit our location</span>', '<span class="cs-topper">Service area</span>'),
        ('<a href="" class="cs-contact-link">17110 116th Ave SE Unit Renton, WA 38058-5055</a>', f'<a href="contact.html#map-1834" class="cs-contact-link">{AREA}</a>'),
    ]
    for old, href, new in [('Personal Training', 'services.html#services', 'Drain Cleaning'), ('Group Workout', 'services.html#services', 'Water Heaters'),
                           ('Muscle Building', 'services.html#services', 'Leak Detection'), ('Virtual Gym Training', 'services.html#services', 'Sewer Lines'),
                           ('Weightloss Training', 'services.html#services', 'Fixtures &amp; Faucets'), ('Body Stretching', 'services.html#pricing', 'Pricing'),
                           ('About Stitch Gym', 'about.html', 'About Us'), ('Membership Details', 'about.html#reviews', 'Reviews'),
                           ('Class Timetable', 'gallery.html', 'Project Gallery'), ('Our Expert Trainers', 'services.html#faq', 'FAQ'),
                           ('Upcoming Events', 'contact.html#map-1834', 'Service Area'), ('Contact Us', 'contact.html', 'Contact Us')]:
        rep.append((f'<a class="cs-link" href="">{old}</a>', f'<a class="cs-link" href="{href}">{new}</a>'))
    rep += [
        ('<span class="cs-header">Useful Links</span>', '<span class="cs-header">Company</span>'),
        ('© Copyright 2023 - <a href="" class="cs-credit-link" target="_blank">Stitch Gym</a>',
         f'&copy; <span id="cs-year">2026</span> <a href="index.html" class="cs-credit-link">{BIZ}</a>. Sample site by <a href="{CS_URL}" class="cs-credit-link cs-cs">Critchfield Systems</a>.'),
        ('<a href="" class="cs-bottom-link">Terms & Conditions</a>', '<a href="services.html#faq" class="cs-bottom-link">FAQ</a>'),
        ('<a href="" class="cs-bottom-link">Privacy Policy</a>', '<a href="contact.html" class="cs-bottom-link">Contact</a>'),
    ]
    hours = ['7:00am - 7:00pm'] * 5 + ['8:00am - 4:00pm', 'Emergency calls']
    h = section('footer/footer-1782-dark-columns-with-hours-table', rep, empty_links_to=None,
                fills=[(r'<td>(9\.00am - 11\.00am)</td>', hours)])
    assert 'href=""' not in h, 'footer has empty link'
    return h

# ---------------------------------------------------------------- page shell
def head(title, css_file, description):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <!-- Sample site: kept out of search results -->
    <meta name="robots" content="noindex, nofollow">
    <meta name="theme-color" content="#0E3A56">
    <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700;800&display=swap">
    <link rel="stylesheet" href="css/root.css">
    <link rel="stylesheet" href="css/{css_file}">
</head>
<body>
<a class="cs-skip" href="#main">Skip to content</a>
'''

YEAR_JS = "const year = document.getElementById('cs-year');\nif (year) year.textContent = new Date().getFullYear();\n"
DESC = f'{BIZ} is a sample plumbing website built by Critchfield Systems.'

def page(name, title, css_file, body, scripts=()):
    html = head(title, css_file, DESC) + nav(name) + '\n<main id="main">\n' + body + '\n</main>\n' + footer() + '\n'
    html += ''.join(f'<script src="js/{s}" defer></script>\n' for s in ('nav.js', *scripts, 'year.js')) + '</body>\n</html>\n'
    # site rules
    assert not re.search(r'<(form|input|textarea|select)\b', html), f'{name}: form element found'
    assert html.count('<h1') == 1, f'{name}: needs exactly one h1'
    assert 'cs-button-solid' not in html and 'cs-button-2' not in html and 'cs-button-4' not in html, f'{name}: second button style'
    labels = set(re.findall(r'class="cs-button-1[^"]*">([^<]*)</a>', html))
    assert labels == {'Call Now'}, f'{name}: button labels {labels}'
    assert '555' not in re.sub(r'<!--.*?-->', '', html, flags=re.S), f'{name}: placeholder phone number'
    return html

# ---------------------------------------------------------------- shared sections
def banner(title, crumb, image):
    return section('page-banner/page-banner-310-centered-photo-band-breadcrumb', [
        ('<span class="cs-int-title">About Us</span>', f'<h1 class="cs-int-title">{title}</h1>'),
        ('<a href="" class="cs-link">Home</a>', '<a href="index.html" class="cs-link">Home</a>'),
        ('<a href="" class="cs-link cs-active">About Us</a>', f'<a href="#main" class="cs-link cs-active" aria-current="page">{crumb}</a>'),
        ('alt="library"', 'alt=""'),
    ], allrep=[('https://csimg.nyc3.digitaloceanspaces.com/Banners/library-m.jpg', IMG.get(image + '_m', IMG[image])),
               ('https://csimg.nyc3.digitaloceanspaces.com/Banners/library.jpg', IMG[image])])
BANNER_OVR = """
#banner-310 .cs-background:before { background: var(--waterDeep); opacity: .78; }
#banner-310 .cs-int-title { color: #fff; }
#banner-310 .cs-link { color: var(--bodyTextColorWhite); }
#banner-310 .cs-link.cs-active { color: var(--copperLight); }
"""

def cta():
    return section('cta/cta-51-dark-centered-photo-band', [
        ('<span class="cs-topper">Contact Us</span>', '<span class="cs-topper">Plumbing Emergency?</span>'),
        ('Get It Done With Us Today', 'A Real Plumber Answers 24/7'),
        ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quis at sit pellentesque molestie.  Diam, adipiscing ultrices eu turpis gravida.',
         'Burst pipe, no hot water or a backed-up drain? Call now and a licensed plumber will be on the way, usually within the hour.'),
        ('alt="cabinets"', 'alt=""'),
    ])
CTA_OVR = """
#cta-51 .cs-picture:before, #cta-51:before { background: var(--waterDeep); opacity: .82; }
#cta-51 .cs-topper { color: var(--copperLight); }
#cta-51 .cs-title { color: #fff; }
#cta-51 .cs-text { color: var(--bodyTextColorWhite); margin-bottom: 2rem; }
"""

# ---------------------------------------------------------------- HOME
HOME_PATHS = ['hero/hero-143-photo-band-four-icon-card', 'services/services-222-eight-icon-boxes-split-header',
              'why-choose-us/why-choose-us-223-text-beside-four-icon-cards', 'stats/stats-5-four-stats-card-over-photo',
              'reviews/reviews-567-three-filled-star-rating-cards', 'cta/cta-51-dark-centered-photo-band']
HOME_CSS = [('url("https://csimg.nyc3.digitaloceanspaces.com/Stats/bg.jpg")', f'url("{IMG["kitchen1"]}")')]
HOME_OVR = """
#hero-143 .cs-background:before, #hero-143:before { background: var(--waterDeep); opacity: .72; }
#hero-143 .cs-title { color: #fff; }
#hero-143 .cs-text { color: var(--bodyTextColorWhite); margin-bottom: 2rem; }
#hero-143 .cs-title:after, #hero-143 .cs-title:before { background: var(--copper); }
@media only screen and (max-width: 1023.5px) {
  /* main already starts below the fixed header on phones */
  #hero-143 { padding-top: 4.5rem; }
}
#h-services-143 .cs-item { border-bottom-color: var(--copper); }
#h-services-143 .cs-title { color: var(--water); }
#services-222 { background-color: #fff; }
#services-222 .cs-item { background-color: var(--stone); }
#services-222 .cs-picture { background-color: #fff; }
#why-choose-223 { background-color: var(--stone); }
#why-choose-223 .cs-item { background-color: #fff; border-color: var(--stoneMid); }
#why-choose-223 .cs-item:first-of-type { background-color: var(--water); }
#why-choose-223 .cs-item:first-of-type .cs-h3, #why-choose-223 .cs-item:first-of-type .cs-item-text { color: #fff; }
#stats-5 .cs-background:before, #stats-5:before { background: var(--waterDeep); opacity: .8; }
#stats-5 .cs-topper { color: var(--copperLight); }
#stats-5 .cs-title { color: #fff; }
#stats-5 .cs-text { color: var(--bodyTextColorWhite); }
#stats-5 .cs-card-group { border-color: var(--copper); }
#stats-5 .cs-number { color: var(--copper); }
#stats-5 .cs-header { color: var(--water); }
#reviews-567 { background-color: #fff; }
#reviews-567 .cs-item { background-color: var(--stone); }
#reviews-567 .cs-job { color: var(--copper); }
""" + CTA_OVR

HERO_CARDS = [('alert', '24/7 Emergency Repairs', 'Burst pipe or backed-up sewer? A real plumber answers day and night.'),
              ('pipe', 'Drain Cleaning', 'Kitchen, bath and main lines cleared, then camera-checked.'),
              ('thermometer', 'Water Heaters', 'Tank and tankless repair, replacement and same-day installs.'),
              ('droplet', 'Leak Detection', 'Hidden leaks found fast, with less digging and less mess.')]

def hero():
    h = section('hero/hero-143-photo-band-four-icon-card', [
        ('Construction & Maintenance Experts in New York City', 'Plumbing &amp; Drain Experts in Lexington, KY'),
        ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. At quis donec eget tellus turpis imperdiet aenean libero. ',
         'Leaks, clogs and cold showers fixed fast by licensed local plumbers. Upfront pricing, clean work and a real person on the phone, day or night.'),
        # the hero photo is the first thing on the page: load it right away
        ('<img loading="lazy" decoding="async" src="https://csimg.nyc3.digitaloceanspaces.com/Hero/kitchen.jpg" alt="kitchen"',
         '<img decoding="async" fetchpriority="high" src="https://csimg.nyc3.digitaloceanspaces.com/Hero/kitchen.jpg" alt=""'),
    ], fills=[
        (r'src="(https://csimg\.nyc3\.digitaloceanspaces\.com/Hero/(?:toolbox|buildings|gear|user)\.svg)"', [icon(c[0]) for c in HERO_CARDS]),
        (r'<h2 class="cs-title">([^<]*)</h2>', [c[1] for c in HERO_CARDS]),
        (r'<p class="cs-text">\s*(Lorem ipsum dolor sit amet, consectetur adipiscing elit\.)\s*</p>', [c[2] for c in HERO_CARDS]),
    ])
    return h

SERVICES8 = [('droplet', 'Leak Repair', 'Dripping faucets, leaking pipes and slab leaks found and fixed for good.'),
             ('pipe', 'Drain Cleaning', 'Slow sinks, tubs and floor drains cleared by snaking or hydro-jetting.'),
             ('thermometer', 'Water Heaters', 'Repair and replacement for tank and tankless units, often same day.'),
             ('tool', 'Toilet Repair', 'Running, clogged or rocking toilets repaired or replaced the same visit.'),
             ('search', 'Sewer Lines', 'Camera inspections, root removal and trenchless sewer line repair.'),
             ('shower', 'Fixtures &amp; Faucets', 'New sinks, faucets, showers and disposals installed the right way.'),
             ('rain', 'Sump Pumps', 'Keep a wet Kentucky spring out of your basement with a new pump.'),
             ('filter', 'Water Filtration', 'Softeners and whole-home filters for Lexington&rsquo;s hard water.')]

HOME_BODY = hero() + section('services/services-222-eight-icon-boxes-split-header', [
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc massa ut sed odio cursus. Malesuada scelerisque eget eu, sollicitudin tellus nibh aenean enim sed. Ut vitae eget commodo consectetur felis augue.',
     'From a dripping faucet to a full repipe, our licensed plumbers handle every job in your home. You get an upfront price before any work starts, and we clean up before we leave.'),
], fills=[
    (r'src="(https://csimg\.nyc3\.digitaloceanspaces\.com/Services/pipes\.svg)"', [icon(s[0]) for s in SERVICES8]),
    (r'<h3 class="cs-h3">(Lorem Ipsum)</h3>', [s[1] for s in SERVICES8]),
    (r'<p class="cs-item-text">\s*(Sed ultricies.*?)\s*</p>', [s[2] for s in SERVICES8]),
]) + section('why-choose-us/why-choose-us-223-text-beside-four-icon-cards', [
    ('A Plumber You Can Trust in Manhattan', 'A Plumber You Can Trust in Lexington'),
    ('Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit. Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit.',
     'We&rsquo;re a local, family-owned shop, not a call center. The plumber who quotes your job is the one who does it, and every repair is backed by our two-year workmanship warranty.'),
    ('20+ Years Experience', '15+ Years Experience'),
    ('<h3 class="cs-h3">Licensed & Insured</h3>', '<h3 class="cs-h3">Licensed &amp; Insured</h3>'),
], fills=[
    (r'src="(https://csimg\.nyc3\.cdn\.digitaloceanspaces\.com/Icons/pipes\.svg)"', [icon('users', 'white'), icon('award'), icon('shield'), icon('star')]),
    (r'<p class="cs-item-text">\s*(Amet minim.*?)\s*</p>', [
        'Background-checked, uniformed plumbers who treat your home with respect.',
        'Thousands of Central Kentucky homes served since 2010.',
        'Kentucky-licensed plumbers with full liability and workers&rsquo; comp coverage.',
        'If it isn&rsquo;t right, we come back and make it right at no charge.']),
]) + section('stats/stats-5-four-stats-card-over-photo', [
    ('<span class="cs-topper">Why Work with Us</span>', '<span class="cs-topper">By the Numbers</span>'),
    ('Facilisis condimentum viverra scelerisque ac morbi sit sed. Turpis sagittis in blandit eleifend tortor ullamcorper eu placerat. Et orci felis volutpat, etiam vitae egestas volutpat pulvinar. ',
     'Fifteen years of fixing Lexington&rsquo;s plumbing has earned us a lot of repeat customers, and a few numbers we&rsquo;re proud of.'),
    ('<span class="cs-number">40+</span>', '<span class="cs-number">15+</span>'), ('Years Experience', 'Years in Business'),
    ('<span class="cs-number">4</span>', '<span class="cs-number">8,500+</span>'), ('Experienced Staff', 'Jobs Completed'),
    ('<span class="cs-number">100+</span>', '<span class="cs-number">4.9</span>'), ('Happy Clients', 'Google Rating'),
    ('<span class="cs-number">1</span>', '<span class="cs-number">24/7</span>'), ('Year Warranty', 'Emergency Service'),
    ('alt="brick wall"', 'alt=""'),
], allrep=[('https://csimg.nyc3.digitaloceanspaces.com/Stats/bg-m.jpg', IMG['kitchen1_m']),
           ('https://csimg.nyc3.digitaloceanspaces.com/Stats/bg.jpg', IMG['kitchen1'])]) + section(
    'reviews/reviews-567-three-filled-star-rating-cards', [
    ('What Our Clients Say', 'What Lexington Homeowners Say'),
    ('Vitae ultricies leo integer malesuada nunc vel. Molestie ac feugiat sed lectus vestibulum mattis ullamcorper velit. Viverra aliquet eget sit amet tellus cras adipiscing. Molestie ac feugiat sed lectus vestibulum mattis ullamcorper velit',
     'More than 600 five-star reviews on Google. Here are a few from the last month.'),
    ('Vera Robinson', 'Megan R.'), ('Psychologist', 'Chevy Chase'),
    ('Benjamin Norris', 'David L.'), ('Business analyst', 'Hamburg'),
    ('Benjamin Norris', 'Tasha W.'), ('Business analyst', 'Masterson Station'),
], fills=[
    (r'<p class="cs-item-text">\s*(Curabitur.*?)\s*</p>', [
        'Our water heater died on a Sunday night. They had a new one in by noon Monday, and the price was exactly what they quoted on the phone.',
        'Fast, friendly and clean. The plumber put on shoe covers, found the leak behind our shower in twenty minutes and fixed it without tearing out the tile.',
        'Our basement drain backed up twice in a month. They ran a camera, found tree roots in the line and fixed it for good. Highly recommend.']),
    (r'class="cs-profile" src="([^"]+)"', [IMG['p1'], IMG['p2'], IMG['p4']]),
], allrep=[('alt="quote icon"', 'alt=""'), ('alt="profile"', 'alt=""')]) + cta()

# ---------------------------------------------------------------- ABOUT
ABOUT_PATHS = ['page-banner/page-banner-310-centered-photo-band-breadcrumb', 'about/about-298-stat-card-over-image-right',
               'about/about-1161-two-photos-left-stat-tile', 'reviews/reviews-864-three-avatar-header-rated-cards',
               'cta/cta-51-dark-centered-photo-band']
ABOUT_OVR = BANNER_OVR + """
#sbsr-298 { background-color: #fff; }
#sbsr-298 .cs-text + .cs-text { margin-top: 1rem; }
#sbsr-298 .cs-link { color: var(--copper); font-weight: 700; white-space: nowrap; }
#sbsr-298 .cs-desc { text-transform: none; }
#sbsr-298 .cs-button-1 { margin-top: 2rem; }
#sbs-1161 { background-color: var(--stone); }
#sbs-1161 .cs-box { background-color: var(--copper); }
#sbs-1161 .cs-li:before { background-color: var(--copper); }
#reviews-864 { background-color: #fff; }
#reviews-864 .cs-item { background-color: var(--stone); }
#reviews-864 .cs-job, #reviews-864 .cs-desc { color: var(--copper); }
""" + CTA_OVR

ABOUT_BODY = banner('About Limestone Plumbing', 'About', 'room3') + section('about/about-298-stat-card-over-image-right', [
    ('<span class="cs-number">14</span>', '<span class="cs-number">15</span>'),
    ('years of practicing', 'years serving Lexington'),
    ('Good People, Great Lawyers', 'Good People, Great Plumbers'),
    ('If you are facing criminal charges, it is crucial to have effective representation immediately. Not only during trial, but also during the pretrial phase as well. At Bernstein Attorneys, our London criminal defense lawyer give your case our full time and attention, to ensure you are treated fairly under the justice system.',
     'Owner Dale Whitaker started Limestone Plumbing &amp; Drain in 2010 with one van and a simple promise: show up on time, explain the problem in plain English and charge a fair price. Fifteen years later we run eight trucks across Central Kentucky, and that promise hasn&rsquo;t changed.'),
    ('Call to ask any question: <a class="cs-link" href="tel:">(555) 455-4555</a>', f'Questions? Call us anytime: <a class="cs-link" href="{TEL}">{PHONE}</a>'),
    ('alt="greek pillars"', 'alt=""'), ('alt="greek pillars"', 'alt=""'),
], allrep=[('https://csimg.nyc3.digitaloceanspaces.com/SideBySide/justice-m.jpg', IMG['tools']),
           ('https://csimg.nyc3.digitaloceanspaces.com/SideBySide/justice.jpg', IMG['tools']),
           ('https://csimg.nyc3.digitaloceanspaces.com/SideBySide/pillars-m.jpg', IMG['worker']),
           ('https://csimg.nyc3.digitaloceanspaces.com/SideBySide/pillars.jpg', IMG['worker'])]) + section(
    'about/about-1161-two-photos-left-stat-tile', [
    ('alt="appliance"', 'alt="Kitchen with a new sink and faucet"'), ('alt="appliance"', 'alt="Kitchen island with a prep sink"'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Graphics/tire-mark.svg" alt="tire mark"', 'src="assets/waves-water.svg" alt=""'),
    ('alt="splash"', 'alt=""'),
    ('<span class="cs-number">2500+</span>', '<span class="cs-number">8,500+</span>'),
    ('Cars repaired this year', 'Jobs completed in Central Kentucky'),
    ('<span class="cs-topper">About Us</span>', '<span class="cs-topper">Our Promise</span>'),
    ('Quality With The Best Standards', 'Work Done Right the First Time'),
    ('Our professionals will perform diagnostic tests, fluid flush and fills, engine replacement, oil changes, and total vehicle overhauls. Busto auctor lectus vitae conubia euismod nec rhoncus parturient convallis parturient accumsan volutpat ligula and intege aenean facilisis.',
     'Every Limestone plumber is licensed, background-checked and trained on the latest equipment. We find the real problem, quote the job before we start and stand behind the work for two years.'),
    ('We handle all makes and models', 'Upfront, flat-rate pricing before any work begins'),
    ('We are endorsed by the local trading standards office', 'Kentucky-licensed, insured plumbers on every job'),
    ('All our technicians are equipped with the latest portable', 'Camera inspections and modern leak detection'),
    ('Proven results for setting exceptional standards', 'Two-year workmanship warranty on every repair'),
    ('Same day service for most repairs', 'Same-day service for most repairs'),
], allrep=[('https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/mechanic25.jpg', IMG['room']),
           ('https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/mechanic26.jpg', IMG['kitchen1'])]) + anchor(section(
    'reviews/reviews-864-three-avatar-header-rated-cards', [
    ('<span class="cs-topper">Testimonials</span>', '<span class="cs-topper">Reviews</span>'),
    ('Trusted by Thousand of People & Companies', 'Trusted by Thousands of Kentucky Families'),
    ('Vitae ultricies leo integer malesuada nunc vel. Molestie ac feugiat sed lectus vestibulum mattis ullamcorper velit. Viverra aliquet eget sit amet tellus cras adipiscing. Molestie ac feugiat sed lectus vestibulum mattis ullamcorper velit.',
     'Homeowners, landlords and local businesses call us back again and again. Here&rsquo;s why.'),
    ('George Thomas', 'Karen B.'), ('Knee Patient', 'Homeowner'),
    ('Barbara Titus', 'Marcus J.'), ('Knee Patient', 'Property Manager'),
    ('Barbara Titus', 'Linda P.'), ('Knee Patient', 'Restaurant Owner'),
], fills=[
    (r'<p class="cs-review">\s*(Curabitur.*?)\s*</p>', [
        'They replaced every galvanized pipe in our 1950s house in three days and patched the drywall so well you can&rsquo;t tell they were there.',
        'I manage forty rental units. Limestone is the only plumber I call because they show up when they say and the invoices always match the quote.',
        'Our grease trap and kitchen drains back up during the dinner rush, and they come out after hours so we never have to close. Lifesavers.']),
    (r'class="cs-profile" src="([^"]+)"', [IMG['p5'], IMG['p3'], IMG['p6']]),
], allrep=[('alt="quote icon"', 'alt=""'), ('alt="profile"', 'alt=""')]), 'reviews-864', 'reviews') + cta()

# ---------------------------------------------------------------- SERVICES
SERVICES_PATHS = ['page-banner/page-banner-310-centered-photo-band-breadcrumb', 'services/services-1188-six-bordered-icon-cards-button',
                  'pricing/pricing-975-two-column-price-list', 'steps/steps-1171-dark-four-icon-steps-arrows',
                  'faq/faq-351-two-column-divided-accordion', 'cta/cta-51-dark-centered-photo-band']
SERVICES_OVR = BANNER_OVR + """
#services-1188 { background-color: var(--stone); }
#services-1188 .cs-item { border-color: var(--stoneMid); background-color: #fff; }
#services-1188 .cs-picture { background-color: var(--stone); }
#pricing-975 { background-color: #fff; }
#pricing-975 .cs-content .cs-text { margin: 0 auto; text-align: center; }
#pricing-975 .cs-header { color: var(--water); }
#pricing-975 .cs-price { color: var(--copper); }
#steps-1171 { background-color: var(--water); }
#steps-1171 .cs-topper { color: var(--copperLight); }
#steps-1171 .cs-picture { background-color: var(--copper); border-color: var(--copperLight); }
#steps-1171 .cs-graphic { opacity: .5; }
#steps-1171 .cs-item:after { filter: brightness(0) invert(1); opacity: .45; }
#faq-351 { background-color: #fff; }
#faq-351 .cs-faq-item.active .cs-button-text, #faq-351 .cs-button:hover .cs-button-text { color: var(--copper); }
#faq-351 .cs-faq-item.active .cs-button:before, #faq-351 .cs-faq-item.active .cs-button:after { background-color: var(--copper); }
""" + CTA_OVR

SERVICES6 = [('pipe', 'Drain Cleaning &amp; Hydro-Jetting', 'Kitchen, bath and main line clogs cleared, then camera-checked so they stay clear.'),
             ('thermometer', 'Water Heater Repair &amp; Install', 'Tank and tankless units repaired or replaced, most the same day you call.'),
             ('droplet', 'Leak Detection &amp; Repair', 'Hidden leaks in walls, ceilings and slabs found fast with less tearing out.'),
             ('search', 'Sewer Line Repair', 'Camera inspections, root removal and trenchless repairs that save your yard.'),
             ('shower', 'Toilets, Faucets &amp; Fixtures', 'Repairs and installs for toilets, sinks, showers, tubs and garbage disposals.'),
             ('rain', 'Sump Pumps &amp; Water Filtration', 'Sump pumps, backups, water softeners and whole-home filters for hard water.')]

PRICES = [('Drain Cleaning (sink or tub)', 'from $129', 'Clear one fixture drain and test the flow.'),
          ('Main Sewer Line Clearing', 'from $249', 'Cleanout access and full-length line clearing.'),
          ('Sewer Camera Inspection', '$199', 'Video inspection with recording you can keep.'),
          ('Toilet Repair', 'from $119', 'Running, leaking or weak flushes fixed.'),
          ('Faucet Installation', 'from $149', 'Your faucet or ours, connected and leak-tested.'),
          ('Garbage Disposal Install', 'from $229', 'Old unit removed and a new 1/2 HP installed.'),
          ('Water Heater Flush', '$129', 'Sediment flush and safety check to extend its life.'),
          ('Tank Water Heater Install', 'from $1,450', 'Haul-away, permit and new 40 or 50 gallon tank.'),
          ('Tankless Water Heater Install', 'from $3,200', 'Endless hot water, sized to your home.'),
          ('Sump Pump Replacement', 'from $495', 'New pump, check valve and a test run.')]

FAQS = [('How much does a service call cost?', 'Our diagnostic visit is $79, and it&rsquo;s waived when you go ahead with the repair. You always get the full price before we start.'),
        ('Do you offer 24/7 emergency service?', 'Yes. A real person answers around the clock, and we keep plumbers on call nights, weekends and holidays.'),
        ('How fast can you get here?', 'Most Lexington calls get a same-day visit, and we can usually reach emergencies within an hour.'),
        ('Are your plumbers licensed and insured?', 'Every plumber holds a Kentucky plumbing license, and we carry full liability and workers&rsquo; compensation coverage.'),
        ('Do you guarantee your work?', 'Yes. Every repair comes with a two-year workmanship warranty, and new water heaters keep their full manufacturer warranty.'),
        ('Should I repair or replace my water heater?', 'If it&rsquo;s under ten years old and the tank isn&rsquo;t leaking, a repair usually makes sense. We&rsquo;ll give you both prices so you can decide.'),
        ('Do you install tankless water heaters?', 'Yes. We size, install and service tankless units from all the major brands, including any gas line work they need.'),
        ('What causes slow drains?', 'Grease, hair and soap build up over time, and tree roots can get into older sewer lines. A camera inspection shows exactly what&rsquo;s going on.'),
        ('Do you work on older homes?', 'All the time. Lexington has plenty of older homes with cast iron and galvanized pipes, and we know how to work with them.'),
        ('What areas do you serve?', 'Lexington and the surrounding area, including Nicholasville, Georgetown, Winchester, Versailles and Richmond.')]

def pricing():
    h = section('pricing/pricing-975-two-column-price-list', [
        ('<span class="cs-topper">Pricing</span>', '<span class="cs-topper">Upfront Pricing</span>'),
        ('<h2 class="cs-title">All Hair Services</h2>',
         '<h2 class="cs-title">Common Jobs &amp; Starting Prices</h2>\n'
         '                <p class="cs-text">Every job gets a flat, written price before we start. No overtime charges, even at night.</p>'),
    ], fills=[
        (r'<span class="cs-header">(Haircut With Blow Dry)</span>', [p[0] for p in PRICES]),
        (r'<span class="cs-price">(\$39)</span>', [p[1] for p in PRICES]),
        (r'<p class="cs-menu-text">\s*(Creative way.*?)\s*</p>', [p[2] for p in PRICES]),
    ])
    return anchor(h, 'pricing-975', 'pricing')

SERVICES_BODY = banner('Plumbing Services', 'Services', 'kitchen') + anchor(section('services/services-1188-six-bordered-icon-cards-button', [
    ('<span class="cs-topper">Other services</span>', '<span class="cs-topper">What We Fix</span>'),
    ('We Provide Quality Auto Repair Services', 'Full-Service Residential Plumbing'),
    ('Facilisis condimentum viverra scelerisque ac morbi sit sed. Turpis sagittis in blandit eleifend tortor ullamcorper eu placerat. Et orci felis volutpat, etiam vitae egestas volutpat pulvinar.',
     'Every service comes with an upfront price, a clean work area and our two-year workmanship warranty.'),
], fills=[
    (r'<img class="cs-icon"\s+src="([^"]+)"', [icon(s[0]) for s in SERVICES6]),
    (r'<h3 class="cs-h3">([^<]*)</h3>', [s[1] for s in SERVICES6]),
    (r'<p class="cs-item-text">(Ut enim ad.*?)</p>', [s[2] for s in SERVICES6]),
]), 'services-1188', 'services') + pricing() + section('steps/steps-1171-dark-four-icon-steps-arrows', [
    ('<span class="cs-topper">Our Work Process</span>', '<span class="cs-topper">How It Works</span>'),
    ('How To Get Started', 'Fixed in Four Simple Steps'),
    ('Lorem ipsum dolor, sit amet consectetur adipisicing elit. Culpa libero sint hic accusantium exercitationem, voluptatem officia quaerat velit quis ullam?',
     'No forms and no runaround. One phone call gets a licensed plumber headed your way.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Graphics/tire-mark.svg"', 'src="assets/waves-light.svg"'),
], fills=[
    (r'src="(https://csimg\.nyc3\.cdn\.digitaloceanspaces\.com/Icons/(?:lightbulb|puzzle|gear|box)\.svg)"', [icon('phone', 'white'), icon('truck', 'white'), icon('dollar', 'white'), icon('check', 'white')]),
    (r'<h3 class="cs-h3">([^<]*)</h3>', ['1. You Call', '2. We Arrive', '3. Upfront Price', '4. Fixed Right']),
    (r'<p class="cs-item-p">\s*(Extensible.*?)\s*</p>', [
        'A real person answers 24/7 and books a time that works for you.',
        'A licensed plumber shows up on time in a fully stocked truck.',
        'We find the real problem and quote the job before any work starts.',
        'We fix it, clean up and back the repair for two full years.']),
]) + anchor(section('faq/faq-351-two-column-divided-accordion', [
    ('<span class="cs-topper">Asked questions</span>', '<span class="cs-topper">FAQ</span>'),
], fills=[
    (r'<span class="cs-button-text">\s*(.*?)\s*</span>', [q for q, a in FAQS]),
    (r'<p class="cs-item-p">\s*(.*?)\s*</p>', [a for q, a in FAQS]),
]), 'faq-351', 'faq') + cta()

# ---------------------------------------------------------------- GALLERY
GALLERY_PATHS = ['page-banner/page-banner-310-centered-photo-band-breadcrumb', 'gallery/gallery-1086-four-column-staggered-masonry',
                 'reviews/reviews-1673-three-rated-cards-over-photo', 'cta/cta-51-dark-centered-photo-band']
GALLERY_OVR = BANNER_OVR + """
#gallery-1086 { background-color: #fff; }
#reviews-1673 { background-color: var(--stone); }
#reviews-1673 .cs-job { color: var(--copper); }
""" + CTA_OVR
WORK = [('kitchen', 'Kitchen sink and faucet replacement'), ('room', 'Kitchen island prep sink plumbing'),
        ('room3', 'New kitchen sink, dishwasher and disposal hookup'), ('room2', 'Open kitchen with new fixtures'),
        ('kitchen1', 'Kitchen remodel rough-in and fixtures'), ('living', 'Wet bar plumbing in a finished basement'),
        ('room4', 'Kitchen with a new pot filler'), ('cabinets', 'Kitchen sink base and supply lines')]

def gallery1086():
    h = section('gallery/gallery-1086-four-column-staggered-masonry', [
        ('<span class="cs-topper">Service</span>', '<span class="cs-topper">Recent Projects</span>'),
        ('<h2 class="cs-title">Our Gallery</h2>', '<h2 class="cs-title">Kitchens, Baths and Everything in Between</h2>'),
    ])
    for n, (key, alt) in enumerate(WORK, 1):
        h, k = re.subn(rf'<picture class="cs-picture cs-picture{n}">.*?</picture>',
                       picture(IMG[key], alt, 345, 345, f'cs-picture cs-picture{n}', IMG.get(key + '_m')), h, count=1, flags=re.S)
        assert k == 1
    assert 'mechanic1' not in h
    return h

GALLERY_BODY = banner('Our Work', 'Gallery', 'room') + gallery1086() + section('reviews/reviews-1673-three-rated-cards-over-photo', [
    ('<span class="cs-topper">Testimonials</span>', '<span class="cs-topper">Reviews</span>'),
    ('Our Customer Reviews', 'Neighbors We&rsquo;ve Helped'),
    ('Britney Allison', 'Jessica H.'), ('Founder of Yokoloko', 'Homeowner, Andover'),
    ('Brooklyn Simmons', 'Tom &amp; Ann K.'), ('Founder of Yokoloko', 'Homeowners, Beaumont'),
    ('Cameron Williamson', 'Chris D.'), ('Founder of Yokoloko', 'Homeowner, Hartland'),
    ('alt="accountant"', 'alt=""'),
], fills=[
    (r'<p class="cs-review">\s*(Stitch Consulting.*?)\s*</p>', [
        'They plumbed our whole kitchen remodel and worked around the cabinet crew without a single delay.',
        'New tankless water heater, new shower valves and a gas line, all done in one day. Spotless work.',
        'Called at 6am with water pouring through the ceiling. They were here by 7 and had it fixed by 8.']),
], allrep=[('alt="profile"', 'alt=""'), ('alt="stars"', 'alt=""'), ('alt="quote icon"', 'alt=""'),
           ('https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/business-meeting.jpeg', IMG['living'])]) + cta()

# ---------------------------------------------------------------- CONTACT
CONTACT_PATHS = ['page-banner/page-banner-310-centered-photo-band-breadcrumb', 'contact/contact-719-single-row',
                 'locations/locations-1834-map-with-four-pill-cards', 'faq/faq-254-accordion-beside-contact-card']
CONTACT_OVR = BANNER_OVR + """
#contact-strip-719 { background-color: var(--water); }
#contact-strip-719 .cs-header { color: var(--copperLight); }
#contact-strip-719 .cs-link, #contact-strip-719 .cs-address { color: #fff; }
#contact-strip-719 .cs-picture { border-color: var(--copperLight); }
#map-1834 .cs-item { background-color: #fff; }
#map-1834 .cs-item:nth-of-type(2) { background-color: var(--water); }
#map-1834 .cs-item:nth-of-type(2) .cs-h2, #map-1834 .cs-item:nth-of-type(2) .cs-item-text { color: #fff; }
#faq-254 { background-color: var(--stone); }
#faq-254 .cs-faq-item { background-color: #fff; }
#faq-254 .cs-faq-item.active .cs-button { color: var(--copper); }
#faq-254 .cs-cta { background-color: var(--water); }
#faq-254 .cs-cta .cs-h3 { color: #fff; }
#faq-254 .cs-cta-p { color: var(--bodyTextColorWhite); }
"""

CONTACT_BODY = banner('Contact Us', 'Contact', 'room2') + section('contact/contact-719-single-row', [
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons%2Fphone-stroke-light.svg"', f'src="{icon("phone", "white")}"'),
    ('<a href="tel:555-456-7899" class="cs-link">+1 (555) 456 7899</a>', f'<a href="{TEL}" class="cs-link">{PHONE}</a>'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons%2Fmail-stroke-light.svg"', f'src="{icon("mail", "white")}"'),
    ('<a href="mailto:Info@email.com" class="cs-link">Info@email.com</a>', f'<a href="mailto:{EMAIL}" class="cs-link">{EMAIL}</a>'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons%2Fpin-stroke-light.svg"', f'src="{icon("pin", "white")}"'),
    ('<span class="cs-header">Address</span>', '<span class="cs-header">Service Area</span>'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images%2FGraphics%2Fwaves-3.svg" alt="wave graphic"', 'src="assets/band-waves.svg" alt=""'),
], fills=[(r'<span class="cs-address">(.*?)</span>', [AREA])]) + section('locations/locations-1834-map-with-four-pill-cards', [
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/brown-pin.svg"', 'src="assets/pin.svg"'),
], fills=[
    (r'<iframe loading="lazy" src="([^"]+)"', [MAP_EMBED]),
    (r'<h2 class="cs-h2">\s*(.*?)\s*</h2>', ['Lexington', 'Nicholasville', 'Georgetown', 'Winchester &amp; Richmond']),
    (r'<span class="cs-item-text">\s*(.*?)\s*</span>', ['Home base, with same-day service across Fayette County.',
                                                         'Daily routes through Jessamine County, including Wilmore.',
                                                         'Daily routes through Scott County and Versailles.',
                                                         'Clark and Madison counties, most days of the week.']),
]).replace('<iframe loading="lazy"', '<iframe title="Map of the Lexington, KY service area" loading="lazy"', 1) + section(
    'faq/faq-254-accordion-beside-contact-card', [
    ('<span class="cs-topper">FAQ’s</span>', '<span class="cs-topper">Before You Call</span>'),
    ('<h2 class="cs-title">Frequently Asked Questions</h2>', '<h2 class="cs-title">Quick Answers</h2>'),
    ('Lorem ipsum, dolor sit amet consectetur adipisicing elit. Consequatur veritatis quae explicabo a quia veniam temporibus aliquid? Quos maiores architecto a officia aliquid atque reiciendis quae? Voluptas maxime sit quae!',
     'The questions we hear most on the phone. Anything else, just ask when you call.'),
    ('That’s ok. Just drop a message and we will get back to you ASAP.', 'That&rsquo;s OK. Give us a call and a real person will answer, day or night.'),
], fills=[
    (r'<button class="cs-button">(.*?)</button>', ['Do you charge to come out?', 'Can you come today?', 'Will I know the price first?',
                                                   'Do you take credit cards?', 'Do you clean up after?']),
    (r'<p class="cs-item-p">\s*(.*?)\s*</p>', [
        'Our $79 diagnostic visit is waived when you go ahead with the repair.',
        'Usually, yes. Most calls get a same-day visit, and emergencies are answered 24/7.',
        'Always. You approve a written, flat-rate price before any work starts.',
        'Yes, plus checks, cash and financing on bigger jobs like water heaters.',
        'Every time. We wear shoe covers, lay drop cloths and haul away old parts.']),
])

# ---------------------------------------------------------------- assets
ICONS = {
    'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    'mail': '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
    'pin': '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    'star': '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
    'award': '<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>',
    'users': '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    'droplet': '<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>',
    'tool': '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    'thermometer': '<path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>',
    'pipe': '<path d="M2 7h9a6 6 0 0 1 6 6v9"/><path d="M2 12h8a2 2 0 0 1 2 2v8"/><line x1="2" y1="5" x2="2" y2="14"/><line x1="10" y1="22" x2="19" y2="22"/>',
    'shower': '<path d="M4 22V9a6 6 0 0 1 12 0"/><path d="M11 9h10"/><line x1="13" y1="13" x2="13" y2="14"/><line x1="17" y1="13" x2="17" y2="14"/><line x1="21" y1="13" x2="21" y2="14"/><line x1="15" y1="17" x2="15" y2="18"/><line x1="19" y1="17" x2="19" y2="18"/><line x1="13" y1="21" x2="13" y2="22"/><line x1="17" y1="21" x2="17" y2="22"/>',
    'search': '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    'filter': '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
    'rain': '<line x1="16" y1="13" x2="16" y2="21"/><line x1="8" y1="13" x2="8" y2="21"/><line x1="12" y1="15" x2="12" y2="23"/><path d="M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/>',
    'alert': '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    'truck': '<rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>',
    'dollar': '<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    'check': '<polyline points="20 6 9 17 4 12"/>',
    'chevron': '<polyline points="6 9 12 15 18 9"/>',
}
COLORS = {'water': '#0E3A56', 'copper': '#A9501A', 'white': '#FFFFFF'}
LOGO_TMPL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 64" width="220" height="64">
<path d="M26 6C26 6 10 24 10 36a16 16 0 0 0 32 0C42 24 26 6 26 6Z" fill="{drop}"/>
<path d="M13 33c4 0 6-2 13-2s9 2 13 2" fill="none" stroke="{layer}" stroke-width="2.4" stroke-linecap="round"/>
<path d="M12 40c5 0 7-2 14-2s9 2 15 2" fill="none" stroke="{layer}" stroke-width="2.4" stroke-linecap="round"/>
<path d="M15 47c4 0 6-2 11-2s7 2 11 2" fill="none" stroke="{layer}" stroke-width="2.4" stroke-linecap="round"/>
<text x="52" y="33" font-family="Arial, Helvetica, sans-serif" font-size="23" font-weight="700" letter-spacing=".8" fill="{text}">LIMESTONE</text>
<text x="53" y="50" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="700" letter-spacing="2.2" fill="{sub}">PLUMBING &amp; DRAIN</text>
</svg>'''
FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48"><rect width="48" height="48" rx="10" fill="#0E3A56"/>
<path d="M24 5C24 5 10 21 10 31a14 14 0 0 0 28 0C38 21 24 5 24 5Z" fill="#FFFFFF"/>
<path d="M13 30c4 0 6-2 11-2s7 2 11 2M13 36c4 0 6-2 11-2s7 2 11 2" fill="none" stroke="#A9501A" stroke-width="2.6" stroke-linecap="round"/></svg>'''
PIN = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80"><path fill="#A9501A" d="M40 4C25 4 13 16 13 31c0 20 27 45 27 45s27-25 27-45C67 16 55 4 40 4z"/><circle cx="40" cy="31" r="10" fill="#FFFFFF"/></svg>'

def ripples(w, h, color, opacity, n=9):
    paths = ''.join(f'<path d="M0 {h*0.55 + i*14:.0f} C {w*0.25:.0f} {h*0.2 + i*14:.0f}, {w*0.5:.0f} {h*0.9 + i*14:.0f}, {w} {h*0.35 + i*14:.0f}"/>' for i in range(n))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="none" '
            f'fill="none" stroke="{color}" stroke-width="2" stroke-opacity="{opacity}">{paths}</svg>')

# ---------------------------------------------------------------- write
def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(text)

for name, body in ICONS.items():
    for cname, col in COLORS.items():
        write(f'assets/icons/{name}-{cname}.svg', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')
write('assets/logo.svg', LOGO_TMPL.format(drop='#0E3A56', layer='#F5F1E8', text='#0E3A56', sub='#A9501A'))
write('assets/logo-light.svg', LOGO_TMPL.format(drop='#FFFFFF', layer='#A9501A', text='#FFFFFF', sub='#E8A36B'))
write('assets/favicon.svg', FAVICON)
write('assets/pin.svg', PIN)
write('assets/waves-light.svg', ripples(840, 357, '#FFFFFF', '.18'))
write('assets/waves-water.svg', ripples(1085, 322, '#0E3A56', '.12'))
write('assets/band-waves.svg', ripples(1920, 318, '#FFFFFF', '.1', 12))

write('css/root.css', shared_css())
write('css/home.css', page_css(HOME_PATHS, HOME_OVR, HOME_CSS))
write('css/about.css', page_css(ABOUT_PATHS, ABOUT_OVR))
write('css/services.css', page_css(SERVICES_PATHS, SERVICES_OVR))
write('css/gallery.css', page_css(GALLERY_PATHS, GALLERY_OVR))
write('css/contact.css', page_css(CONTACT_PATHS, CONTACT_OVR))

write('js/nav.js', js('nav/nav-759-two-row-logo-panel-dropdown'))
write('js/faq.js', js('faq/faq-351-two-column-divided-accordion'))   # same script ships with faq-254
write('js/year.js', YEAR_JS)

write('index.html', page('index.html', f'Plumber in Lexington, KY | {BIZ}', 'home.css', HOME_BODY))
write('about.html', page('about.html', f'About Us | {BIZ}', 'about.css', ABOUT_BODY))
write('services.html', page('services.html', f'Plumbing Services &amp; Pricing | {BIZ}', 'services.css', SERVICES_BODY, ('faq.js',)))
write('gallery.html', page('gallery.html', f'Project Gallery | {BIZ}', 'gallery.css', GALLERY_BODY))
write('contact.html', page('contact.html', f'Contact Us | {BIZ}', 'contact.css', CONTACT_BODY, ('faq.js',)))
print('built', os.path.normpath(OUT))
