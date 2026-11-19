#!/usr/bin/env python3
"""Builds the Critchfield Systems sample site (critchfield-systems/sample/):
a fictional roofing company, "Keystone Ridge Roofing", made from sections in
the DeveloperDadd/components library.

Usage: python3 _tools/build-sample-site.py /path/to/components

Every section is the component's own index.html with its copy, links and
images swapped (markup and layout untouched). Photos are the placeholder
photos that ship with the components (CodeStitch image CDN); swap any of them
in the IMG table below."""
import os, re, sys

COMP = os.path.join(sys.argv[1] if len(sys.argv) > 1 else '../components', 'sections')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'critchfield-systems', 'sample')

# ---------------------------------------------------------------- business (fictional)
BIZ = 'Keystone Ridge Roofing'
PHONE = '(859) 270-7050'          # Critchfield Systems' number, so calls reach Clayton
TEL = 'tel:+18592707050'
EMAIL = 'office@keystoneridge.example'
ADDRESS_1 = '1200 Summit Ridge Road'
ADDRESS_2 = 'Lexington, KY 40502'
HOURS = 'Mon - Sat: 7:00am to 6:00pm'

# Critchfield Systems (the demo banner)
CS_URL = 'https://critchfieldsystems.com'
CS_PHONE = '(859) 270-7050'
CS_TEL = 'tel:+18592707050'

# ---------------------------------------------------------------- placeholder photos
R = 'https://nyc3.digitaloceanspaces.com/csimages2/Roofer/'
IMG = {
    'hero': R + 'CTA.jpg',
    'aerial': 'https://nyc3.digitaloceanspaces.com/csimages2/Images/MISC/roofing-process.jpg',
    'roofer_seam': 'https://nyc3.digitaloceanspaces.com/csimages2/Images/Misc/roofing-man.jpg',
    'banner': 'https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/MISC/construction11.jpg',
    'crew1': R + 'steps1.jpg', 'crew2': R + 'steps2.jpg', 'crew3': R + 'steps3.jpg',
    'service2': R + 'services2.jpg', 'about': R + 'sbs-nonstandard.jpg',
    'house1': 'https://csimg.nyc3.digitaloceanspaces.com/Gallery/house1.jpg',
    'house2': 'https://csimg.nyc3.digitaloceanspaces.com/Gallery/house2.jpg',
    'house3': 'https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/house3.jpg',
    'house4': 'https://csimg.nyc3.digitaloceanspaces.com/Gallery/house4.jpg',
    'house5': 'https://csimg.nyc3.digitaloceanspaces.com/Gallery/house5.jpg',
    'house6': 'https://csimg.nyc3.digitaloceanspaces.com/Gallery/house6.jpg',
    'build1': 'https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/MISC/construction12.jpg',
    'build2': 'https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/MISC/construction13.jpg',
    'build3': 'https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/MISC/construction14.jpg',
    'build4': 'https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/MISC/construction15.jpg',
    'comm1': 'https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/MISC/building1.jpg',
    'comm2': 'https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/MISC/building2.jpg',
    'comm3': 'https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/MISC/building3.jpg',
}

# ---------------------------------------------------------------- helpers
def raw(path):
    return open(os.path.join(COMP, path, 'index.html')).read()

def css(path):
    return open(os.path.join(COMP, path, 'style.css')).read()

def js(path):
    return open(os.path.join(COMP, path, 'script.js')).read()

def call_now(h):
    """The one button on this site: every .cs-button-4 is a Call Now link to the business."""
    def fix(m):
        cls = re.search(r'class="(cs-button-4[^"]*)"', m.group(0)).group(1)
        return f'<a href="{TEL}" class="{cls}">Call Now</a>'
    return re.sub(r'<a\b[^>]*class="cs-button-4[^"]*"[^>]*>.*?</a>', fix, h, flags=re.S)

def section(path, repl, keep_empty_links=False):
    """Component markup with copy swapped. Each (old, new) replaces the FIRST
    remaining occurrence, so repeated placeholder text can be replaced in order."""
    h = raw(path)
    for old, new in repl:
        if old not in h:
            raise SystemExit(f'{path}: text not found: {old[:70]!r}')
        h = h.replace(old, new, 1)
    h = h.replace('class="cs-button-solid', 'class="cs-button-4')
    h = call_now(h)
    if not keep_empty_links:
        h = h.replace('href=""', 'href="contact.html"')
    leftovers = re.findall(r'[Ll]orem ipsum', h)
    if leftovers:
        raise SystemExit(f'{path}: lorem ipsum left in markup')
    return h

def icon(name, color='accent'):
    return f'assets/icons/{name}-{color}.svg'

# ---------------------------------------------------------------- shared CSS
ROOT_CSS = """/* Keystone Ridge Roofing (sample site by Critchfield Systems)
   60-30-10: 60% white / warm stone, 30% charcoal slate, 10% copper accent */
:root {
    --primary: #C2410C;          /* copper - 10% accent (buttons, toppers, icons) */
    --primaryLight: #F97316;     /* bright copper, decorative only */
    --secondary: #1C2530;        /* charcoal slate - 30% (headings, dark bands, footer) */
    --secondaryLight: #F97316;
    --stone: #F5F3F0;            /* warm light tint - part of the 60% */
    --headerColor: #1C2530;
    --bodyTextColor: #4A5361;
    --bodyTextColorWhite: #F7F6F4;
    --topperFontSize: clamp(0.8125rem, 1.6vw, 1rem);
    --headerFontSize: clamp(1.9375rem, 3.9vw, 3.0625rem);
    --bodyFontSize: 1rem;
    --sectionPadding: clamp(3.75rem, 7.82vw, 6.25rem) 1rem;
}
html { scroll-behavior: smooth; }
body {
    margin: 0; padding: 0;
    font-family: "Archivo", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    background-color: #fff; color: var(--bodyTextColor);
    -webkit-font-smoothing: antialiased;
}
*, *:before, *:after { box-sizing: border-box; }
img { max-width: 100%; }
button, input, textarea { font-family: inherit; }
.cs-topper { font-size: var(--topperFontSize); line-height: 1.2em; text-transform: uppercase; text-align: inherit; letter-spacing: .1em; font-weight: 700; color: var(--primary); margin-bottom: 0.25rem; display: block; }
.cs-title { font-size: var(--headerFontSize); font-weight: 800; line-height: 1.2em; text-align: inherit; max-width: 43.75rem; margin: 0 0 1rem 0; color: var(--headerColor); position: relative; }
.cs-text { font-size: var(--bodyFontSize); line-height: 1.5em; text-align: inherit; width: 100%; max-width: 40.625rem; margin: 0; color: var(--bodyTextColor); }

/*-- The one site button: components/sections/button/button3 (.cs-button-4) --*/
.cs-button-4 {
    text-align: center; font-size: 1rem;
    line-height: clamp(2.875rem, 8vw, 3.5rem);
    text-decoration: none; font-weight: 700; min-width: 10.875rem; margin: 0;
    overflow: hidden; color: #fff; padding: 0 3rem; box-sizing: border-box;
    background-color: var(--primary); border: none; cursor: pointer;
    display: inline-block; position: relative; z-index: 1;
    box-shadow: 0 1.125rem 2.25rem -0.5rem rgba(194, 65, 12, 0.55), 0 0.5rem 1rem rgba(28, 37, 48, 0.35);
    transition: box-shadow .3s, transform .3s;
}
.cs-button-4:before {
    content: ''; width: 150%; height: 110%; background: var(--secondary); opacity: 1;
    position: absolute; display: block; top: 50%; left: -130%; z-index: -2;
    transform: skew(45deg) translateY(-50%); transition: left .3s;
}
.cs-button-4:hover:before { left: -20%; }
.cs-button-4:hover { transform: translateY(-0.1875rem); box-shadow: 0 1.5rem 2.75rem -0.5rem rgba(194, 65, 12, 0.65), 0 0.75rem 1.5rem rgba(28, 37, 48, 0.4); }
.cs-button-4:focus-visible { outline: 3px solid var(--primaryLight); outline-offset: 3px; }

.cs-skip { position: absolute; left: 1rem; top: -4rem; z-index: 20000; background: var(--secondary); color: #fff; padding: .75rem 1rem; text-decoration: none; font-weight: 700; }
.cs-skip:focus { top: 1rem; }
.cs-demo-note { display: none; margin: 1rem 0 0; padding: .875rem 1rem; background: #FFF4EC; border-left: 4px solid var(--primary); color: var(--headerColor); font-size: .9375rem; line-height: 1.5em; }
.cs-demo-note.cs-show { display: block; }
.cs-demo-note a { color: var(--primary); font-weight: 700; }
@media (prefers-reduced-motion: reduce) {
    *, *:before, *:after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}
"""

NAV_OVR = """
/* nav: top bar carries the phone number and the demo notice */
#cs-navigation .cs-top-bar, #cs-navigation .cs-top-container { background-color: var(--secondary); }
#cs-navigation .cs-top-container:before { background: var(--secondary); }
#cs-navigation .cs-top-link { color: #E7E3DE; }
#cs-navigation .cs-top-link strong { color: #FDBA74; }
#cs-navigation .cs-top-link.cs-demo-link { color: #fff; font-weight: 600; }
#cs-navigation .cs-top-link.cs-demo-link:hover { color: #FDBA74; }
#cs-navigation .cs-logo img { height: 100%; width: auto; }
#cs-navigation .cs-nav-button { white-space: nowrap; }
@media only screen and (max-width: 1023.5px) {
  #cs-navigation .cs-nav-button { display: none; }
}
@media only screen and (max-width: 767px) {
  /* keep the demo notice visible on phones */
  #cs-navigation .cs-top-contact { flex-wrap: wrap; gap: .25rem 1.5rem; }
  #cs-navigation .cs-top-link:nth-of-type(2) { display: flex; }
  #cs-navigation .cs-top-container { padding: .625rem 1rem; }
}
"""

FOOTER_OVR = """
/* footer: charcoal slate (30%) */
#cs-footer-2544 { background-color: var(--secondary); }
#cs-footer-2544 .cs-top { background-color: #fff; }
#cs-footer-2544 .cs-copyright-link { color: var(--primary); font-weight: 700; }
#cs-footer-2544 .cs-wrapper { background-color: #FFF4EC; }
#cs-footer-2544 .cs-subscribe-group .cs-button-4 { align-self: flex-start; }
"""

def shared_css():
    return (ROOT_CSS + '\n' + css('nav/nav-1722-shaded-top-bar-with-dropdown') + NAV_OVR
            + '\n' + css('footer/footer-2544-signup-panel-icon-contact-row') + FOOTER_OVR)

def page_css(paths, overrides):
    return '\n'.join(css(p) for p in paths) + '\n/* ---- brand overrides ---- */\n' + overrides

# ---------------------------------------------------------------- nav + footer
NAV_LINKS = [('index.html', 'Home'), ('about.html', 'About'), ('services.html', 'Services'), ('gallery.html', 'Gallery'), ('contact.html', 'Contact')]

def nav(active):
    h = raw('nav/nav-1722-shaded-top-bar-with-dropdown')
    rep = [
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/phone-grey.svg"', f'src="{icon("phone", "light")}"'),
        ('href="" class="cs-top-link">', f'href="{TEL}" class="cs-top-link">'),
        ('Call us: +84 1985 33 999', f'Call us: <strong>{PHONE}</strong>'),
        ('href="" class="cs-top-link">', f'href="{CS_URL}" class="cs-top-link cs-demo-link">'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/clock-grey.svg"', f'src="{icon("star", "light")}"'),
        ('Opening hours: Mon - Sat: 8:00am To 9:00pm', 'Sample website built by Critchfield Systems. Get yours for $99/month &rarr;'),
        ('href="" class="cs-logo" aria-label="Return to [Company name] Home page"', f'href="index.html" class="cs-logo" aria-label="Return to {BIZ} home page"'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Logos/consulting-logo.svg" alt="" width="197" height="43" aria-hidden="true"',
         f'src="assets/logo.svg" alt="{BIZ}" width="230" height="48"'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/Icons/chev-down.svg"', f'src="{icon("chevron", "dark")}"'),
        ('<a href="" class="cs-li-link cs-drop-link">Housing</a>', '<a href="services.html#services" class="cs-li-link cs-drop-link">Roof Replacement</a>'),
        ('<a href="" class="cs-li-link cs-drop-link">Food Banks</a>', '<a href="services.html#services" class="cs-li-link cs-drop-link">Roof Repair</a>\n                            </li>\n                            <li class="cs-drop-li">\n                                <a href="services.html#services" class="cs-li-link cs-drop-link">Storm Damage</a>\n                            </li>\n                            <li class="cs-drop-li">\n                                <a href="services.html#pricing" class="cs-li-link cs-drop-link">Inspections &amp; Pricing</a>'),
        ('Blog', 'Gallery'),
        ('<a href="" class="cs-button-solid cs-nav-button">Contact Us</a>', f'<a href="{TEL}" class="cs-button-4 cs-nav-button">Call Now</a>'),
    ]
    for o, n in rep:
        assert o in h, o
        h = h.replace(o, n, 1)
    # socials: commented out until the client has profiles
    h = re.sub(r'(<div class="cs-top-social">)(.*?)(</div>)', lambda m: '<!-- social links go here once the client has profiles\n' + m.group(1) + m.group(2) + m.group(3) + ' -->', h, count=1, flags=re.S)
    # main links: Home, About, (Services dropdown), Gallery, Contact
    hrefs = {'Home': 'index.html', 'About': 'about.html', 'Gallery': 'gallery.html', 'Contact': 'contact.html'}
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
        ('Trusted roofing experts you can rely on', 'Roof leaking or storm damage? Talk to a real roofer today.'),
    ]
    services = ['Roof Installation', 'Roof Replacement', 'Roof Repairs', 'Storm Damage Restoration', 'Emergency Roofing', 'Roof Inspections']
    for s in services:
        rep.append(('<a class="cs-link" href="">', '<a class="cs-link" href="services.html#services">'))
    resources = [('FAQs', 'services.html#faq', 'FAQs'), ('Roofing Warranty', 'services.html#pricing', 'Pricing &amp; Warranty'),
                 ('Maintenance Tips', 'gallery.html', 'Project Gallery'), ('Insurance Claims', 'about.html', 'About Us'), ('Service Areas', 'about.html#service-area', 'Service Areas')]
    for old, href, new in resources:
        rep.append(('<a class="cs-link" href="">', f'<a class="cs-link" href="{href}">'))
        rep.append((old, new))
    rep += [
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/charity-pin-green.svg"', f'src="{icon("pin")}"'),
        ('<a class="cs-contact-link" href="" target="_blank" rel="noopener">38 Bridge Street, Andover,', f'<a class="cs-contact-link" href="contact.html#location">{ADDRESS_1},'),
        ('England, SP10 1BW</a>', f'{ADDRESS_2}</a>'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/charity-clock-green.svg"', f'src="{icon("clock")}"'),
        ('Monday - Saturday: 10:00 - 20:00', 'Monday - Saturday: 7:00am - 6:00pm'),
        ('Sunday: Closed', 'Emergency tarping: 24/7'),
        ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/charity-phone-green.svg"', f'src="{icon("phone")}"'),
        ('<a class="cs-contact-link" href="tel:+994070929">M: +99 40 70 929</a>', f'<a class="cs-contact-link" href="{TEL}">P: {PHONE}</a>'),
        ('<a class="cs-contact-link" href="mailto:info@rooferstitch.com">E: info@rooferstitch.com</a>', f'<a class="cs-contact-link" href="mailto:{EMAIL}">E: {EMAIL}</a>'),
        ('© Copyright 2026 - <a class="cs-copyright-link" href="">Roofer Stitch</a>', f'&copy; <span id="cs-year">2026</span> {BIZ}. Sample site by <a class="cs-copyright-link" href="{CS_URL}">Critchfield Systems</a>'),
        ('<a class="cs-bottom-link" href="">Terms &amp; Conditions</a>', '<a class="cs-bottom-link" href="services.html#faq">FAQ</a>'),
        ('<a class="cs-bottom-link" href="">Privacy Policy</a>', '<a class="cs-bottom-link" href="contact.html">Contact</a>'),
    ]
    h = section('footer/footer-2544-signup-panel-icon-contact-row', rep, keep_empty_links=True)
    # no forms on this site: the signup form's slot holds the Call Now button
    h, n = re.subn(r'<form class="cs-form".*?</form>', f'<a href="{TEL}" class="cs-button-4">Call Now</a>', h, flags=re.S)
    assert n == 1
    assert 'href=""' not in h, 'footer has empty link'
    return h

# ---------------------------------------------------------------- page shell
def head(title, desc, page_css_file):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <!-- Sample site: kept out of search results -->
    <meta name="robots" content="noindex, nofollow">
    <meta name="theme-color" content="#1C2530">
    <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap">
    <link rel="stylesheet" href="css/root.css">
    <link rel="stylesheet" href="css/{page_css_file}">
</head>
<body>
<a class="cs-skip" href="#main">Skip to content</a>
'''

DEMO_JS = """const year = document.getElementById('cs-year');
if (year) year.textContent = new Date().getFullYear();
"""

def page(name, title, desc, css_file, body, scripts=()):
    tags = ''.join(f'<script src="js/{s}" defer></script>\n' for s in ('nav.js', *scripts, 'year.js'))
    return head(title, desc, css_file) + nav(name) + '\n<main id="main">\n' + body + '\n</main>\n' + footer() + '\n' + tags + '</body>\n</html>\n'

# ---------------------------------------------------------------- shared sections
def banner(title, text, crumb):
    return section('page-banner/page-banner-2285-dark-photo-band-breadcrumb-bar', [
        ('<span class="cs-int-title">About Us</span>', f'<h1 class="cs-int-title">{title}</h1>'),
        ("Platinum Craft Exteriors enhances your home's exterior with quality roofing and stunning finishes.", text),
        ('<a href="" class="cs-link">Home</a>', '<a href="index.html" class="cs-link">Home</a>'),
        ('<a href="" class="cs-link cs-active">About</a>', f'<a href="#main" class="cs-link cs-active" aria-current="page">{crumb}</a>'),
        ('alt="construction" width="1280" height="568" aria-hidden="true"', 'alt="" width="1280" height="568" aria-hidden="true" fetchpriority="high"'),
    ])

def cta(topper, title, image='house4'):
    return section('cta/cta-2574-photo-band-contact-info-row', [
        ('Ready When you Are', topper),
        ('Reliable Roofing Solutions Built To Protect Your Property', title),
        ('<a href="" class="cs-button-solid">Schedule Free Inspection</a>', f'<a href="{TEL}" class="cs-button-solid">Call {PHONE}</a>'),
        ('mailto:info@roofingcompany.com', f'mailto:{EMAIL}'),
        ('info@roofingcompany.com</a>', f'{EMAIL}</a>'),
        ('tel:555-123-4688', TEL),
        ('(555) 123 5688', PHONE),
        ('<a href="" class="cs-link">4587 Summit Ridge, USA</a>', f'<a href="contact.html#location" class="cs-link">{ADDRESS_1}, {ADDRESS_2}</a>'),
        (R + 'CTA.jpg" alt="roof"', IMG[image] + '" alt=""'),
    ])

# ---------------------------------------------------------------- HOME
HOME_PATHS = ['hero/hero-1061-overlapping-four-icon-cards', 'services/services-2557-two-photo-cards-dark-center',
              'about/about-2555-wide-photo-overlap-icon-card', 'steps/steps-2549-cards-grid-photo-band-steps',
              'reviews/reviews-2565-cards-grid', 'cta/cta-2574-photo-band-contact-info-row']
HOME_OVR = """
#hero-1061 .cs-background:before { background: linear-gradient(90deg, rgba(28, 37, 48, .92) 0%, rgba(28, 37, 48, .55) 100%); opacity: 1; }
#hero-1061 .cs-icon-wrapper { background-color: #FFF4EC; }
#hero-1061 .cs-item { box-shadow: 0 1.25rem 2.5rem -1rem rgba(28, 37, 48, .35); }
#services-2557 .cs-item:nth-of-type(1) .cs-link, #services-2557 .cs-item:nth-of-type(2) .cs-link { color: var(--primary); }
#steps-2549 { background-color: var(--stone); }
#reviews-2565 { background-color: var(--stone); }
#cta-2574 .cs-background:before { background: var(--secondary); opacity: .82; }
#cta-2574 .cs-topper, #cta-2574 .cs-heading { color: #FDBA74; }
#cta-2574 .cs-link { white-space: nowrap; }
"""
HOME_BODY = section('hero/hero-1061-overlapping-four-icon-cards', [
    ('Stitch Mechanics Now Serving Designers & Developers', 'Lexington&rsquo;s Trusted Roofing Company Since 2012'),
    ('We are the premier Stitch Design Pack for mechanics and auto body websites of all varieties.', 'Roof replacements, repairs and storm damage restoration done right the first time, with a free inspection and a written estimate before any work starts.'),
    ('<a href="" class="cs-button-solid">Request Appointment</a>', f'<a href="{TEL}" class="cs-button-solid">Call for a Free Estimate</a>'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/car1.svg" alt="car"', f'src="{icon("home")}" alt=""'),
    ('Electrical System', 'Roof Replacement'),
    ('Our designs come with the perfect look and feel of an auto body shop or any car related industry. Use Stitch Mechanics for all car related sites!', 'Complete tear-off and new architectural shingle or metal roofs, installed in as little as one day.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/car2.svg" alt="car"', f'src="{icon("tool")}" alt=""'),
    ('System Service', 'Roof Repair'),
    ('Our designs come with the perfect look and feel of an auto body shop or any car related industry. Use Stitch Mechanics for all car related sites!', 'Leaks, missing shingles and flashing fixed fast before small problems turn into big ones.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/car3.svg" alt="car"', f'src="{icon("storm")}" alt=""'),
    ('Engine Diagnostics', 'Storm Damage'),
    ('Our designs come with the perfect look and feel of an auto body shop or any car related industry. Use Stitch Mechanics for all car related sites!', 'Hail and wind damage repairs, emergency tarping, and help working with your insurance company.'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/car3.svg" alt="car"', f'src="{icon("search")}" alt=""'),
    ('Engine Diagnostics', 'Free Inspections'),
    ('Our designs come with the perfect look and feel of an auto body shop or any car related industry. Use Stitch Mechanics for all car related sites!', 'A no-pressure roof inspection with photos of what we find and an honest recommendation.'),
    ('srcset="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/mechanic-m.jpg"', f'srcset="{IMG["hero"]}"'),
    ('srcset="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/mechanic.jpg"', f'srcset="{IMG["hero"]}"'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/mechanic.jpg" alt="mechanic" width="2250" height="1500" aria-hidden="true"',
     f'src="{IMG["hero"]}" alt="" width="1920" height="654" aria-hidden="true" fetchpriority="high"'),
]) + section('services/services-2557-two-photo-cards-dark-center', [
    ('Our featured services deliver reliable protection, expert craftsmanship, and long-lasting roofing solutions tailored to residential and commercial property needs.',
     'From a single leak to a full replacement, our crews handle residential and light commercial roofing across Central Kentucky.'),
    ('<a href="" class="cs-button-solid">Explore More Projects</a>', '<a href="services.html" class="cs-button-solid">See All Services</a>'),
    ('alt="roofer" width="427" height="320"', 'alt="Roofer repairing shingles on a pitched roof" width="427" height="320"'),
    ('<a href="" class="cs-link">\n', f'<a href="{TEL}" class="cs-link">\n'), ('Get Roof Repaired', 'Call Now'),
    ('alt="roofer" width="427" height="320"', 'alt="Roofing crew installing a new roof" width="427" height="320"'),
    ('<a href="" class="cs-link">\n', f'<a href="{TEL}" class="cs-link">\n'), ('Request Free Estimate', 'Call Now'),
]) + section('about/about-2555-wide-photo-overlap-icon-card', [
    ('Our Core Values', 'Why Homeowners Choose Us'),
    ('Driven By Quality Trust Craftsmanship', 'Quality You Can See, Service You Can Trust'),
    ('Our mission and philosophy guide every roofing project we complete, shaping how we serve clients, uphold craftsmanship, communicate transparently, and deliver long-lasting roofing solutions built on trust.',
     'Keystone Ridge is a family-owned roofing company. The same owner who inspects your roof is on site the day it&rsquo;s installed, and every job is backed by our 10-year workmanship warranty.'),
    ('alt="roofer" width="466" height="397"', 'alt="Two roofers inspecting a new metal roof" width="466" height="397"'),
]) + section('steps/steps-2549-cards-grid-photo-band-steps', [
    ('From inspection to completion, we follow a clear process that ensures quality workmanship, timely delivery, transparent communication, and durable roofing solutions for every project we handle.',
     'No surprises and no pressure. Here is exactly how a Keystone Ridge project works, from the first call to the final walkthrough.'),
    ('<a href="" class="cs-button-solid">Talk to An Expert</a>', f'<a href="{TEL}" class="cs-button-solid">Talk to an Expert</a>'),
]) + section('reviews/reviews-2565-cards-grid', [
    ('What Customers Say About Us', 'What Our Neighbors Are Saying'),
    ('From inspection to completion, we follow a clear process that ensures quality workmanship, timely delivery, transparent communication, and durable roofing solutions for every project we handle.',
     'Hundreds of Central Kentucky homeowners trust us with the most important part of their home. Here are a few of their stories.'),
    ('<a href="" class="cs-button-solid cs-desktop">More Reviews</a>', '<a href="gallery.html" class="cs-button-solid cs-desktop">See Our Work</a>'),
    ('alt="person"', 'alt="Customer photo"'),
    ('Excellent workmanship and clear communication throughout the project. They helped us understand every step and completed the roof ahead of schedule.',
     'Excellent workmanship and clear communication throughout the project. They explained every step and finished our new roof ahead of schedule.'),
    ('alt="person"', 'alt="Customer photo"'),
    ('Excellent workmanship and clear communication throughout the project. They helped us understand every step and completed the roof ahead of schedule.',
     'After the spring hail storm they tarped our roof the same night and walked us through the whole insurance claim. Couldn&rsquo;t recommend them more.'),
    ('James R.', 'NAME_A'), ('James R.', 'NAME_B'),
    ('alt="person"', 'alt="Customer photo"'),
    ('Excellent workmanship and clear communication throughout the project. They helped us understand every step and completed the roof ahead of schedule.',
     'Fair price, no pressure, and the crew left the yard cleaner than they found it. Our metal roof looks fantastic.'),
    ('James R.', 'NAME_C'),
    ('<a href="" class="cs-button-solid cs-mobile">More Reviews</a>', '<a href="gallery.html" class="cs-button-solid cs-mobile">See Our Work</a>'),
]).replace('NAME_A', 'James R.').replace('NAME_B', 'Megan T.').replace('NAME_C', 'Daniel K.') + cta('Free Inspections, Written Estimates', 'Protect Your Home With a Roof Built to Last')

# ---------------------------------------------------------------- ABOUT
ABOUT_PATHS = ['page-banner/page-banner-2285-dark-photo-band-breadcrumb-bar', 'stats/stats-2552-image-beside-vertical-timeline',
               'why-choose-us/why-choose-us-2556-split-cards-grid-accordion', 'locations/locations-2559-two-office-cards-with-maps',
               'cta/cta-2574-photo-band-contact-info-row']
BANNER_OVR = """
#banner-2285 .cs-background:before { background: var(--secondary); opacity: .78; }
#banner-2285 .cs-link.cs-active { color: #FDBA74; }
"""
ABOUT_OVR = BANNER_OVR + """
#steps-2552 { background-color: #fff; }
#why-2556 { background-color: var(--stone); }
#cta-2574 .cs-background:before { background: var(--secondary); opacity: .82; }
#cta-2574 .cs-topper, #cta-2574 .cs-heading { color: #FDBA74; }
#cta-2574 .cs-link { white-space: nowrap; }
"""
ABOUT_BODY = banner('About Keystone Ridge Roofing', 'A family-owned roofing company protecting Central Kentucky homes since 2012.', 'About') + section('stats/stats-2552-image-beside-vertical-timeline', [
    ('Our Work Process', 'Our Story'),
    ('Simple Reliable Roofing Process', 'Built One Roof at a Time'),
    ('From inspection to completion, we follow a clear process that ensures quality workmanship, timely delivery, transparent communication, and durable roofing solutions for every project we handle.',
     'What started as one truck and a two-person crew has grown into one of Lexington&rsquo;s most trusted roofing teams, without losing the small-company care.'),
    ('<span class="cs-number">2020</span>', '<span class="cs-number">2012</span>'),
    ('Inspection &amp; Assessment', 'One Truck, Two Roofers'),
    ('We thoroughly inspect your roof to identify any issues. After discussing your options, we provide honest recommendations tailored specifically to your needs.',
     'Owner Mark Ellison opens Keystone Ridge after 15 years in the trade, promising honest estimates and work he would put on his own home.'),
    ('<span class="cs-number">2021</span>', '<span class="cs-number">2016</span>'),
    ('Planning &amp; Installation', 'Storm Response Team'),
    ('Our team efficiently schedules work, prepares necessary materials, adheres to safety standards, and completes repairs with minimal disruption to your daily routine.',
     'After a record hail season we add a dedicated storm crew offering same-day emergency tarping and insurance claim support.'),
    ('alt="roofer fitting a standing seam metal panel to a pitched roof"', 'alt="Roofer fitting a standing seam metal panel to a pitched roof"'),
    ('<span class="cs-number">2022</span>', '<span class="cs-number">2020</span>'),
    ('Setup and Configuration', 'Metal Roofing Division'),
    ('Our crew expertly organizes tasks, gathers essential supplies, follows safety protocols, and performs repairs while ensuring your daily activities are minimally affected.',
     'We become certified metal roofing installers, giving homeowners a 50-year roof option with standing seam and metal shingle systems.'),
    ('<span class="cs-number">2023</span>', '<span class="cs-number">2024</span>'),
    ('Final Check &amp; Support', '2,000 Roofs and Counting'),
    ('We conduct final inspections to ensure quality results, clean the site thoroughly, and remain available for ongoing maintenance support whenever you need it.',
     'Our crews pass 2,000 completed roofs across Fayette and the surrounding counties, with an A+ rating and hundreds of five-star reviews.'),
]) + section('why-choose-us/why-choose-us-2556-split-cards-grid-accordion', [
    ('Trusted Roofing Experts You Can Rely', 'Trusted Roofing Experts You Can Rely On'),
    ('We stand behind every roofing project with quality, accountability, and long-term performance assurance.',
     'Every roof is backed by our 10-year workmanship warranty on top of the manufacturer&rsquo;s material warranty.'),
    ('Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptates, et ut expedita iure odit nesciunt.',
     'Our crews average over 12 years of experience, and the owner personally checks every finished roof.'),
    ('Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptates, et ut expedita iure odit nesciunt.',
     'We install only name-brand shingles, underlayment and metal systems rated for Kentucky weather.'),
    ('Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptates, et ut expedita iure odit nesciunt.',
     'Clear written estimates, a dedicated project manager, and a full magnetic nail sweep when we leave.'),
    ('alt="roofer" width="466" height="397"', 'alt="Roofer inspecting a finished roof" width="466" height="397"'),
    ('Certified and trained roofing specialists', 'Licensed and fully insured crews'),
    ('Transparent pricing with no surprises', 'Written estimates with no surprises'),
]).replace('<section id="why-2556">', '<section id="why-2556">', 1) + section('locations/locations-2559-two-office-cards-with-maps', [
    ('Our Office Locations', 'Service Area'),
    ('Visit Our Offices', 'Proudly Serving Central Kentucky'),
    ('Our offices are conveniently located to serve residential and commercial clients, offering easy access, responsive support, and professional roofing consultations from experienced team members.',
     'Two locations mean our crews are never far away. We serve Lexington, Nicholasville, Georgetown, Versailles, Winchester, Richmond and everywhere in between.'),
    ('<a href="" class="cs-button-solid">Get Directions</a>', '<a href="contact.html#location" class="cs-button-solid">Get Directions</a>'),
    ('Austin, Texas', 'Lexington, Kentucky'), ('Maple Ridge Residence', 'Main Office &amp; Showroom'),
    ('href="mailto:info@roofingcompany.com">info@roofingcompany.com</a>', f'href="mailto:{EMAIL}">{EMAIL}</a>'),
    ('href="tel:(512) 555-0198">(512) 555-0198</a>', f'href="{TEL}">{PHONE}</a>'),
    ('<a class="cs-contact-link" href="">245 Market Street, Suite 300, Austin, TX 78701</a>', f'<a class="cs-contact-link" href="contact.html#location">{ADDRESS_1}, {ADDRESS_2}</a>'),
    ('<a class="cs-button-solid" href="" class="cs-button-solid">Get Directions</a>', '<a class="cs-button-solid" href="contact.html#location">Get Directions</a>'),
    ('San Diego, California', 'Richmond, Kentucky'), ('Westside Service Office', 'Southside Service Office'),
    ('href="mailto:info@roofingcompany.com">info@roofingcompany.com</a>', f'href="mailto:{EMAIL}">{EMAIL}</a>'),
    ('href="tel:(619) 555-0246">(619) 555-0246</a>', 'href="tel:+18595550187">(859) 555-0187</a>'),
    ('<a class="cs-contact-link" href="">880 Harbor Avenue, San Diego, CA 92101</a>', '<a class="cs-contact-link" href="contact.html#location">480 Eastern Bypass, Richmond, KY 40475</a>'),
]).replace('<section id="locations-2559">', '<section id="locations-2559">\n    <span id="service-area"></span>', 1) + cta("Let's Talk About Your Roof", 'Meet the Team That Treats Your Home Like Their Own', 'house2')

# ---------------------------------------------------------------- SERVICES
SERVICES_PATHS = ['page-banner/page-banner-2285-dark-photo-band-breadcrumb-bar', 'services/services-282-six-text-cards-one-highlighted',
                  'steps/steps-2551-numbered-steps-card-intro-right', 'pricing/pricing-2562-three-icon-cards-one-outlined',
                  'faq/faq-1109-accordion-cards-image-right', 'cta/cta-2574-photo-band-contact-info-row']
SERVICES_OVR = BANNER_OVR + """
#services-282 .cs-item:hover .cs-h3, #services-282 .cs-item:hover .cs-item-text, #services-282 .cs-item:hover .cs-fake-link { color: #fff; }
#steps-2551 { background-color: var(--stone); }
#pricing-2562 .cs-item { filter: none; }
#pricing-2562 .cs-item.cs-available:before { content: "Most Popular"; }
#pricing-2562 .cs-icon-wrapper { background-color: #FFF4EC; }
#pricing-2562 .cs-price { display: block; font-size: 2.5rem; font-weight: 800; line-height: 1.1em; color: var(--headerColor); margin: 0 0 1rem; }
#pricing-2562 .cs-price small { font-size: 1rem; font-weight: 500; color: var(--bodyTextColor); }
#pricing-2562 .cs-item .cs-button-4 { width: 100%; }
#faq-1109 { background-color: #fff; }
#cta-2574 .cs-background:before { background: var(--secondary); opacity: .82; }
#cta-2574 .cs-topper, #cta-2574 .cs-heading { color: #FDBA74; }
#cta-2574 .cs-link { white-space: nowrap; }
"""
SERVICES_282 = [
    ('Roof Replacement', 'Full tear-off and replacement with architectural shingles, synthetic underlayment and new flashing.'),
    ('Roof Repair', 'Leaks, lifted or missing shingles, cracked boots and damaged flashing repaired quickly and cleanly.'),
    ('Storm Damage Restoration', 'Hail and wind damage inspections, emergency tarping and full insurance claim support.'),
    ('Metal Roofing', 'Standing seam and metal shingle systems built to last 50 years with little maintenance.'),
    ('Gutters &amp; Ventilation', 'Seamless gutters, guards, ridge vents and attic ventilation that protect your roof from the inside out.'),
    ('Inspections &amp; Maintenance', 'Free inspections with photos, plus yearly tune-ups that catch small problems before they leak.'),
]
rep282 = [
    ('Grow Musically and Experience Personal Development', 'Complete Roofing Services for Your Home'),
    ('Lorem ipsum dolor sit amet consectetur, adipisicing elit. Harum necessitatibus, reiciendis accusamus quaerat hic ipsum laborum ullam doloremque velit ratione porro nostrum, minima deserunt reprehenderit adipisci, accusantium repellendus omnis voluptas.',
     'Whatever your roof needs, one call covers it. Every service starts with a free inspection and a written, itemized estimate.'),
]
for old, (name, text) in zip(['Concerts & Recitals', 'Competitions', 'Orchestras', 'Piano Duets', 'Master Classes', 'Chamber'], SERVICES_282):
    rep282 += [('<a class="cs-link" href="">', f'<a class="cs-link" href="{TEL}">'), (old, name),
               ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi magna ut et, ut.', text), ('Read More', 'Call Now')]

def price_card(price, unit):
    return f'<span class="cs-price">{price}<small>{unit}</small></span>'

SERVICES_BODY = banner('Roofing Services', 'Replacement, repair, storm damage and more, all backed by our 10-year workmanship warranty.', 'Services') + section(
    'services/services-282-six-text-cards-one-highlighted', rep282).replace('<section id="services-282">', '<section id="services-282">\n    <span id="services"></span>', 1) + section(
    'steps/steps-2551-numbered-steps-card-intro-right', [
    ('Our Work Process', 'What to Expect'),
    ('Simple Reliable Roofing Process', 'Your Roof, Start to Finish'),
    ('From inspection to completion, we follow a clear process that ensures quality workmanship, timely delivery, transparent communication, and durable roofing solutions for every project we handle.',
     'Most replacements take one to two days. You&rsquo;ll know the price, the schedule and the materials before we ever set up a ladder.'),
    ('<a href="" class="cs-button-solid">Talk to An Expert</a>', f'<a href="{TEL}" class="cs-button-solid">Book a Free Inspection</a>'),
    ('Inspection &amp; Assessment', 'Free Inspection &amp; Estimate'),
    ('We thoroughly inspect your roof to identify any issues. After discussing your options, we provide honest recommendations tailored specifically to your needs.',
     'We inspect your roof, show you photos of what we find, and give you a written, itemized estimate. No pressure, no obligation.'),
    ('Planning &amp; Installation', 'Scheduling &amp; Installation'),
    ('Our team efficiently schedules work, prepares necessary materials, adheres to safety standards, and completes repairs with minimal disruption to your daily routine.',
     'We order materials, protect your landscaping, and our crew completes the work quickly with a project manager on site.'),
    ('Final Check &amp; Support', 'Cleanup &amp; Final Walkthrough'),
    ('We conduct final inspections to ensure quality results, clean the site thoroughly, and remain available for ongoing maintenance support whenever you need it.',
     'We run a magnetic nail sweep, walk the finished roof with you, and register your warranty before we leave.'),
]) + section('pricing/pricing-2562-three-icon-cards-one-outlined', [
    ('Our Pricing Plans', 'Pricing'),
    ('Fair, Predictable Pricing', 'Honest, Upfront Pricing'),
    ('Our model is designed to grow with you. We offer a fixed price for each operational level, ensuring there are no barriers to adoption as your agency scales.',
     'Every roof is different, so every job gets a written quote. These starting prices give you a realistic idea before we visit.'),
    ('src="https://nyc3.digitaloceanspaces.com/csimages2/Roofer/pricing5.svg"', f'src="{icon("home")}"'),
    ('<h3 class="cs-h3">Administrative</h3>', '<h3 class="cs-h3">Roof Replacement</h3>\n                    ' + price_card('$8,900', ' starting')),
    ('Essential tools for effective agency communication and management.', 'Full replacement for a typical 1,800 sq ft home with architectural shingles.'),
    ('Warranty Coverage', 'Complete tear-off and disposal'), ('Inbox organization', 'Synthetic underlayment and ice guard'),
    ('Standard form templates', 'New flashing, vents and drip edge'), ('Client notifications', '10-year workmanship warranty'),
    ('<a href="" class="cs-button-solid">Start Free Trial</a>', f'<a href="{TEL}" class="cs-button-solid">Get My Quote</a>'),
    ('Fixed monthly Rate', 'Financing available'),
    ('src="https://nyc3.digitaloceanspaces.com/csimages2/Roofer/pricing6.svg"', f'src="{icon("tool")}"'),
    ('<h3 class="cs-h3">Analytical</h3>', '<h3 class="cs-h3">Roof Repair</h3>\n                    ' + price_card('$350', ' starting')),
    ('Advanced data processing and powerful spreadsheet automation.', 'Leaks, missing shingles, flashing and pipe boot repairs.'),
    ('Excel data exports', 'Same-week scheduling'), ('Performance reporting', 'Matching shingles when available'), ('Financial forecasting', '2-year repair warranty'),
    ('<a href="" class="cs-button-solid">Coming Soon</a>', f'<a href="{TEL}" class="cs-button-solid">Schedule a Repair</a>'),
    ('Join the waitlist for early access', 'Most repairs done in one visit'),
    ('src="https://nyc3.digitaloceanspaces.com/csimages2/Roofer/pricing7.svg"', f'src="{icon("search")}"'),
    ('<h3 class="cs-h3">Integrations</h3>', '<h3 class="cs-h3">Roof Inspection</h3>\n                    ' + price_card('Free', '')),
    ('Seamless connections with your favorite third-party integration tools.', 'A complete roof check with photos and an honest recommendation.'),
    ('Excel data exports', 'Shingles, flashing and gutters'), ('Performance reporting', 'Attic and ventilation check'), ('Financial forecasting', 'Storm damage documentation'),
    ('<a href="" class="cs-button-solid">Coming Soon</a>', f'<a href="{TEL}" class="cs-button-solid">Book Inspection</a>'),
    ('Join the waitlist for early access', 'No cost, no obligation'),
]).replace('<section id="pricing-2562">', '<section id="pricing-2562">\n    <span id="pricing"></span>', 1) + section('faq/faq-1109-accordion-cards-image-right', [
    ('FAQ’s', 'FAQ'),
    ('srcset="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/MISC/mechanic23.jpg"', f'srcset="{IMG["crew2"]}"'),
    ('srcset="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/MISC/mechanic23.jpg"', f'srcset="{IMG["crew2"]}"'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/MISC/mechanic23.jpg" alt="appliance"', f'src="{IMG["crew2"]}" alt="Roofers working on a residential roof"'),
    ('Do you have experience with car like mine?', 'How long does a roof replacement take?'),
    ('In the U.S., the terms lawyer and attorney are often used interchangeably. A lawyer provides legal services such as giving legal advice, writing legal documents and providing policy counsel to governments. An attorney, on top of these things also holds a state or regional license to represent clients in a law court.',
     'Most homes are finished in one to two days. Larger or steeper roofs can take a little longer, and we&rsquo;ll give you the schedule up front.'),
    ('What is your plan cancellation policy?', 'Do you help with insurance claims?'),
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sit convallis nunc neque, bibendum pulvinar vitae commodo velit. Proin diam tortor sed malesuada nunc, habitant. Dignissim ipsum porta enim, magna urna, quam. ',
     'Yes. We document storm damage with photos, meet your adjuster on site, and handle the paperwork so you can focus on your family.'),
    ('What professional certifications you have?', 'Are you licensed and insured?'),
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sit convallis nunc neque, bibendum pulvinar vitae commodo velit. Proin diam tortor sed malesuada nunc, habitant. Dignissim ipsum porta enim, magna urna, quam. ',
     'Yes. Keystone Ridge is fully licensed, carries general liability and workers&rsquo; compensation insurance, and is certified by major shingle manufacturers.'),
    ('What professional certifications you have?', 'Do you offer financing?'),
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sit convallis nunc neque, bibendum pulvinar vitae commodo velit. Proin diam tortor sed malesuada nunc, habitant. Dignissim ipsum porta enim, magna urna, quam. ',
     'We offer low monthly payment options for replacements so you don&rsquo;t have to put off a roof you need.'),
    ('How much air pressure should I put my tires?', 'What warranty do you offer?'),
    ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sit convallis nunc neque, bibendum pulvinar vitae commodo velit. Proin diam tortor sed malesuada nunc, habitant. Dignissim ipsum porta enim, magna urna, quam. ',
     'Every replacement includes our 10-year workmanship warranty plus the manufacturer&rsquo;s material warranty, registered in your name.'),
]).replace('<section id="faq-1109">', '<section id="faq-1109">\n    <span id="faq"></span>', 1) + cta('Same-Week Inspections', 'Get a Free, Written Roofing Estimate', 'house5')

# ---------------------------------------------------------------- GALLERY
GALLERY_PATHS = ['page-banner/page-banner-2285-dark-photo-band-breadcrumb-bar', 'gallery/gallery-44-three-column-grid-with-button',
                 'gallery/gallery-379-rounded-three-column-grid', 'reviews/reviews-1307-centered-quote-over-photo-band',
                 'cta/cta-2574-photo-band-contact-info-row']
GALLERY_OVR = BANNER_OVR + """
#gallery-379 { background-color: var(--stone); }
#quote-1307 .cs-background:before { background: var(--secondary); opacity: .8; }
#quote-1307 .cs-job { color: #FDBA74; }
#cta-2574 .cs-background:before { background: var(--secondary); opacity: .82; }
#cta-2574 .cs-topper, #cta-2574 .cs-heading { color: #FDBA74; }
#cta-2574 .cs-link { white-space: nowrap; }
"""
HOMES = [('house1', 'Finished home with a new roof'), ('house2', 'New roof on a two-story home'), ('house3', 'Home exterior after roof replacement'),
         ('house4', 'Completed residential roofing project'), ('house5', 'Home with new architectural shingles'), ('house6', 'Finished home with new shingles')]
CREW = [('crew1', 'Roofer repairing shingles'), ('crew2', 'Roofers working on a residential roof'), ('crew3', 'Roofer installing flashing'),
        ('service2', 'Crew installing a new roof'), ('about', 'Roofers inspecting a metal roof'), ('roofer_seam', 'Roofer fitting a standing seam metal panel')]

def swap_pictures(h, tag, items, w, hgt, cls):
    start = 0
    for key, alt in items:
        i = h.index(tag, start)
        j = h.index('</picture>', i) + len('</picture>')
        new = f'{tag}\n                    <img loading="lazy" decoding="async" src="{IMG[key]}" alt="{alt}" width="{w}" height="{hgt}">\n                </picture>'
        h = h[:i] + new + h[j:]
        start = i + len(new)
    return h

GALLERY_BODY = banner('Project Gallery', 'A look at recent roof replacements and repairs across Central Kentucky.', 'Gallery') + swap_pictures(section(
    'gallery/gallery-44-three-column-grid-with-button', [
    ('Service', 'Finished Homes'),
    ('Landscaping Services in Sometown, USA', 'Roof Replacements Across Central Kentucky'),
    ('Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit. Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit.',
     'Architectural shingles, metal roofs and full replacements on homes in Lexington, Nicholasville, Georgetown and Richmond.'),
]), '<picture class="cs-picture">', HOMES, 346, 346, 'cs-picture') + swap_pictures(section(
    'gallery/gallery-379-rounded-three-column-grid', [
    ('Our Portfolio', 'Crew at Work'),
    ('Some Work from Our Memorable Gallery', 'Craftsmanship You Can See'),
    ('At Stitch Cleaning Service, let us help you solve problems so that you can focus on your mission. We support businesses through periods of expansion, succession.',
     'Our licensed, insured crews protect your property, work safely, and leave the job site cleaner than they found it.'),
]), '<picture class="cs-image">', CREW, 305, 400, 'cs-image') + section(
    'reviews/reviews-1307-centered-quote-over-photo-band', [
    ('Creating long-term value with entrepreneurial intelligence! Our main goal is Growth.', '&ldquo;They replaced our entire roof in a single day and you&rsquo;d never know a crew had been here. Best contractor we&rsquo;ve ever hired.&rdquo;'),
    ('Piter Bowman', 'Sarah &amp; Tom W.'), ('Creative Director', 'Homeowners, Nicholasville'),
    ('srcset="https://csimages2.nyc3.digitaloceanspaces.com/Images/MISC/banking-district.jpg"', f'srcset="{IMG["house3"]}"'),
    ('srcset="https://csimages2.nyc3.digitaloceanspaces.com/Images/MISC/banking-district.jpg"', f'srcset="{IMG["house3"]}"'),
    ('src="https://csimages2.nyc3.digitaloceanspaces.com/Images/MISC/banking-district.jpg"', f'src="{IMG["house3"]}"'),
    ('alt="banking cityscape"', 'alt=""'),
]) + cta('Like What You See?', 'Your Home Could Be Our Next Project', 'aerial')

# ---------------------------------------------------------------- CONTACT
CONTACT_PATHS = ['page-banner/page-banner-2285-dark-photo-band-breadcrumb-bar', 'contact/contact-1111-three-icon-info-row-over-photo',
                 'locations/locations-2560-map-with-pinned-photo-card', 'cta/cta-2574-photo-band-contact-info-row']
CONTACT_OVR = BANNER_OVR + """
#contact-strip-1111 .cs-background:before { background: var(--secondary); opacity: .82; }
#contact-strip-1111 .cs-icon { width: 2rem; height: auto; }
#contact-strip-1111 .cs-header { color: #FDBA74; }
#locations-2560 { background-color: var(--stone); }
#cta-2574 .cs-background:before { background: var(--secondary); opacity: .82; }
#cta-2574 .cs-topper, #cta-2574 .cs-heading { color: #FDBA74; }
#cta-2574 .cs-link { white-space: nowrap; }
"""
CONTACT_BODY = banner('Contact Us', 'Call us to schedule your free roof inspection. Emergency tarping is available 24/7.', 'Contact') + section(
    'contact/contact-1111-three-icon-info-row-over-photo', [
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/mech-phone.svg" alt="icon"', f'src="{icon("phone", "light")}" alt=""'),
    ('<a href="tel:555-456-7899" class="cs-link">+1 (555) 456 7899</a>', f'<a href="{TEL}" class="cs-link">{PHONE}</a>'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/mech-email.svg" alt="icon"', f'src="{icon("mail", "light")}" alt=""'),
    ('<a href="mailto:Info@email.com" class="cs-link">Info@email.com</a>', f'<a href="mailto:{EMAIL}" class="cs-link">{EMAIL}</a>'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/mech-pin.svg" alt="icon"', f'src="{icon("pin", "light")}" alt=""'),
    ('121 King St, Melbourne VIC 300, ', f'{ADDRESS_1}, '), ('Australia</span>', f'{ADDRESS_2}</span>'),
    ('srcset="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/mechanic24.jpg"', f'srcset="{IMG["crew3"]}"'),
    ('srcset="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/mechanic24.jpg"', f'srcset="{IMG["crew3"]}"'),
    ('src="https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/mechanic24.jpg" alt="mechanic"', f'src="{IMG["crew3"]}" alt=""'),
]) + section('locations/locations-2560-map-with-pinned-photo-card', [
    ('Our Office Locations', 'Visit Our Showroom'),
    ('Visit Our Offices', 'Find Us in Lexington'),
    ('Our offices are conveniently located to serve residential and commercial clients, offering easy access, responsive support, and professional roofing consultations from experienced team members.',
     f'Stop by to see shingle and metal samples in person, or call ahead and we&rsquo;ll have an estimator ready. {HOURS}.'),
    ('Regional Roofing Headquarters', 'Keystone Ridge Main Office'),
    ('<a class="cs-link" href="">7425 Industrial Parkway, Suite 400, Dallas, TX 75247</a>', f'<a class="cs-link" href="{TEL}">{ADDRESS_1}, {ADDRESS_2}</a>'),
]).replace('<section id="locations-2560">', '<section id="locations-2560">\n    <span id="location"></span>', 1) + cta('Free Inspections, Written Estimates', 'Call Today to Schedule Your Free Roof Inspection', 'house6')

# ---------------------------------------------------------------- assets
ICONS = {
    'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    'mail': '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
    'pin': '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    'home': '<path d="M3 11 12 3l9 8"/><path d="M5 9.5V21h14V9.5"/><path d="M10 21v-6h4v6"/>',
    'tool': '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    'storm': '<path d="M19 16.9A5 5 0 0 0 18 7h-1.26a8 8 0 1 0-11.62 9"/><polyline points="13 11 9 17 15 17 11 23"/>',
    'search': '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    'star': '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    'chevron': '<polyline points="6 9 12 15 18 9"/>',
}
COLORS = {'accent': '#C2410C', 'light': '#FDBA74', 'dark': '#1C2530', 'white': '#FFFFFF'}
LOGO = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 48" width="230" height="48">
<path d="M4 30 L22 12 L40 30" fill="none" stroke="#C2410C" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M12 30 L22 20 L32 30" fill="none" stroke="#1C2530" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="4" y="35" width="36" height="4" rx="2" fill="#1C2530"/>
<text x="50" y="26" font-family="Arial, Helvetica, sans-serif" font-size="19" font-weight="700" letter-spacing=".5" fill="#1C2530">KEYSTONE RIDGE</text>
<text x="51" y="42" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="700" letter-spacing="4.2" fill="#C2410C">ROOFING CO.</text>
</svg>'''
FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48"><rect width="48" height="48" rx="10" fill="#1C2530"/>
<path d="M8 30 L24 14 L40 30" fill="none" stroke="#F97316" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><rect x="10" y="34" width="28" height="4" rx="2" fill="#fff"/></svg>'''

# ---------------------------------------------------------------- write
def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(text)

for name, body in ICONS.items():
    for cname, col in COLORS.items():
        write(f'assets/icons/{name}-{cname}.svg', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')
write('assets/logo.svg', LOGO)
write('assets/favicon.svg', FAVICON)

write('css/root.css', shared_css())
write('css/home.css', page_css(HOME_PATHS, HOME_OVR))
write('css/about.css', page_css(ABOUT_PATHS, ABOUT_OVR))
write('css/services.css', page_css(SERVICES_PATHS, SERVICES_OVR))
write('css/gallery.css', page_css(GALLERY_PATHS, GALLERY_OVR))
write('css/contact.css', page_css(CONTACT_PATHS, CONTACT_OVR))

write('js/nav.js', js('nav/nav-1722-shaded-top-bar-with-dropdown'))
write('js/faq.js', js('faq/faq-1109-accordion-cards-image-right'))
write('js/why.js', js('why-choose-us/why-choose-us-2556-split-cards-grid-accordion').replace('".cs-button"', '"#why-2556 .cs-button"'))
write('js/year.js', DEMO_JS)

D = f'{BIZ} is a sample roofing website built by Critchfield Systems.'
write('index.html', page('index.html', f'Roof Replacement &amp; Repair in Lexington, KY | {BIZ}', D, 'home.css', HOME_BODY))
write('about.html', page('about.html', f'About Us | {BIZ}', D, 'about.css', ABOUT_BODY, ('why.js',)))
write('services.html', page('services.html', f'Roofing Services &amp; Pricing | {BIZ}', D, 'services.css', SERVICES_BODY, ('faq.js',)))
write('gallery.html', page('gallery.html', f'Project Gallery | {BIZ}', D, 'gallery.css', GALLERY_BODY))
write('contact.html', page('contact.html', f'Contact Us | {BIZ}', D, 'contact.css', CONTACT_BODY))
print('built', os.path.normpath(OUT))
