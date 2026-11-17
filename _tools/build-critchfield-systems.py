#!/usr/bin/env python3
"""Builds the Critchfield Systems site (critchfield-systems/) from the
DeveloperDadd/components section library.

Usage: python3 _tools/build-critchfield-systems.py /path/to/components
Edit the CONTACT block below to change the phone/email everywhere."""
import os, re, sys

COMP = os.path.join(sys.argv[1] if len(sys.argv) > 1 else '../components', 'sections')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'critchfield-systems')

# ---------------------------------------------------------------- contact
PHONE_DISPLAY = '(859) 270-7050'
PHONE_E164 = '+18592707050'
EMAIL = 'critchfieldsystems@gmail.com'
TEL = f'tel:{PHONE_E164}'
SMS = f'sms:{PHONE_E164}'
SITE = 'https://critchfieldsystems.com'

def comp_css(path):
    return open(os.path.join(COMP, path, 'style.css')).read()

def rename_keyframes(css, sid):
    return re.sub(r'floatAnimation(2?)', lambda m: f'float-{sid}{m.group(1)}', css)

# ---------------------------------------------------------------- shared CSS
ROOT_CSS = """/* Critchfield Systems - shared styles (palette, core, button, nav, footer)
   60-30-10: 60% white / ice tint, 30% navy, 10% royal blue + cyan accent */
:root {
    --primary: #0070D3;          /* royal blue - 10% accent (buttons, toppers, icons) */
    --primaryLight: #22C3FF;     /* cyan highlight from the logo (decorative only) */
    --secondary: #0B2350;        /* navy - 30% (wordmark color, dark bands, headings) */
    --secondaryLight: #22C3FF;
    --deep: #061633;             /* darkest navy (footer, hero base) */
    --ice: #F2F6FB;              /* light tint - part of the 60% */
    --headerColor: #0B2350;
    --bodyTextColor: #3E4C66;
    --bodyTextColorWhite: #F4F8FC;
    /* 13px - 16px */
    --topperFontSize: clamp(0.8125rem, 1.6vw, 1rem);
    /* 31px - 49px */
    --headerFontSize: clamp(1.9375rem, 3.9vw, 3.0625rem);
    --bodyFontSize: 1rem;
    /* 60px - 100px top and bottom */
    --sectionPadding: clamp(3.75rem, 7.82vw, 6.25rem) 1rem;
}

html { scroll-behavior: smooth; }
body {
    margin: 0;
    padding: 0;
    font-family: "Montserrat", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    background-color: #fff;
    color: var(--bodyTextColor);
    -webkit-font-smoothing: antialiased;
}
*, *:before, *:after { box-sizing: border-box; }
img { max-width: 100%; }
button { font-family: inherit; }
a { color: var(--primary); }

.cs-topper {
    font-size: var(--topperFontSize);
    line-height: 1.2em;
    text-transform: uppercase;
    text-align: inherit;
    letter-spacing: .1em;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 0.25rem;
    display: block;
}
.cs-title {
    font-size: var(--headerFontSize);
    font-weight: 900;
    line-height: 1.2em;
    text-align: inherit;
    max-width: 43.75rem;
    margin: 0 0 1rem 0;
    color: var(--headerColor);
    position: relative;
}
.cs-text {
    font-size: var(--bodyFontSize);
    line-height: 1.5em;
    text-align: inherit;
    width: 100%;
    max-width: 40.625rem;
    margin: 0;
    color: var(--bodyTextColor);
}

/*-- The one site button: components/sections/button/button3 (.cs-button-4) --*/
.cs-button-4 {
    text-align: center;
    font-size: 1rem;
    /* 46px - 56px */
    line-height: clamp(2.875rem, 8vw, 3.5rem);
    text-decoration: none;
    font-weight: 700;
    min-width: 10.875rem;
    margin: 0;
    overflow: hidden;
    color: #fff;
    padding: 0 3rem;
    box-sizing: border-box;
    background-color: var(--primary);
    display: inline-block;
    position: relative;
    z-index: 1;
    /* foreground shadow so the button stands out */
    box-shadow: 0 1.125rem 2.25rem -0.5rem rgba(0, 112, 211, 0.6), 0 0.5rem 1rem rgba(6, 22, 51, 0.35);
    transition: box-shadow .3s, transform .3s;
}
.cs-button-4:before {
    content: '';
    width: 150%;
    height: 110%;
    background: var(--secondary);
    opacity: 1;
    position: absolute;
    display: block;
    top: 50%;
    left: -130%;
    z-index: -2;
    transform: skew(45deg) translateY(-50%);
    transition: left .3s;
}
.cs-button-4:hover:before { left: -20%; }
.cs-button-4:hover {
    transform: translateY(-0.1875rem);
    box-shadow: 0 1.5rem 2.75rem -0.5rem rgba(0, 112, 211, 0.7), 0 0.75rem 1.5rem rgba(6, 22, 51, 0.4);
}
.cs-button-4:focus-visible { outline: 3px solid var(--primaryLight); outline-offset: 3px; }

.cs-skip {
    position: absolute; left: 1rem; top: -4rem; z-index: 20000;
    background: var(--secondary); color: #fff; padding: .75rem 1rem; text-decoration: none; font-weight: 700;
}
.cs-skip:focus { top: 1rem; }
@media (prefers-reduced-motion: reduce) {
    *, *:before, *:after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}
"""

NAV_OVERRIDES = """
/* nav: brand logo + the shared .cs-button-4 in the button slot */
#cs-navigation .cs-nav-button { white-space: nowrap; }
@media only screen and (max-width: 1023.5px) {
  #cs-navigation .cs-logo { width: 55%; max-width: 13rem; }
  #cs-navigation .cs-nav-button { display: none; }
  #cs-navigation .cs-line { background-color: var(--secondary); }
}
@media only screen and (min-width: 1024px) {
  #cs-navigation .cs-logo { width: 22%; max-width: 17rem; height: 4.5rem; }
  #cs-navigation .cs-li-link { font-weight: 600; color: var(--headerColor); }
}
"""

FOOTER_OVERRIDES = """
/* footer: navy (30%) with brand accents */
#cs-footer-145 { background-color: var(--deep); }
#cs-footer-145 .cs-logo { width: clamp(14rem, 20vw, 17rem); }
#cs-footer-145 .cs-header { color: #fff; }
#cs-footer-145 .cs-nav-link:before { background: var(--primaryLight); }
#cs-footer-145 .cs-contact { border-color: rgba(34, 195, 255, .25); }
#cs-footer-145 .cs-contact-link .cs-label { display: block; font-size: .8125rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--primaryLight); }
#cs-footer-145 .cs-copyright { color: #9fb0cc; }
@media only screen and (max-width: 47.9375rem) {
  #cs-footer-145 .cs-container { align-items: flex-start; }
  #cs-footer-145 .cs-nav { width: 50%; margin-bottom: 2.5rem; }
}
@media only screen and (min-width: 64rem) {
  #cs-footer-145 .cs-bottom { border-top-color: rgba(34, 195, 255, .25); }
}
"""

def shared_css():
    css = ROOT_CSS
    css += '\n' + comp_css('nav/nav-757-light-single-row-bar') + NAV_OVERRIDES
    css += '\n' + comp_css('footer/footer-145-dark-logo-three-link-columns') + FOOTER_OVERRIDES
    return css

# ---------------------------------------------------------------- page CSS
def page_css(sections, overrides):
    parts = []
    for path, sid, repl in sections:
        css = rename_keyframes(comp_css(path), sid)
        for a, b in repl:
            assert a in css, (path, a)
            css = css.replace(a, b)
        parts.append(css)
    return '\n'.join(parts) + '\n/* ---- Critchfield Systems brand overrides ---- */\n' + overrides

HERO_493_OVR = """
#hero-493 .cs-background:before { background: var(--deep); opacity: 0.35; }
#hero-493 .cs-topper:before, #hero-493 .cs-topper:after { background: var(--primaryLight); }
#hero-493 .cs-text a { color: #fff; font-weight: 700; }
"""
CTA_OVR = """
#cta-2574 .cs-background:before { background: var(--deep); opacity: 0.55; }
#cta-2574 .cs-topper { color: var(--primaryLight); }
#cta-2574 .cs-heading { color: var(--primaryLight); }
"""
FAQ_JS_NOTE = ''

# ---------------------------------------------------------------- HTML pieces
def icon(name, alt=''):
    return f'assets/icons/{name}.svg'

def head(title, desc, css, path):
    url = SITE + ('/' if path == 'index.html' else '/' + path.replace('.html', ''))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{url}">
    <meta name="theme-color" content="#0B2350">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{SITE}/assets/logo.webp">
    <link rel="icon" type="image/png" href="assets/favicon.png">
    <link rel="apple-touch-icon" href="assets/favicon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&display=swap">
    <link rel="stylesheet" href="css/root.css">
    <link rel="stylesheet" href="css/{css}">
</head>
<body>
<a class="cs-skip" href="#main">Skip to content</a>
'''

NAV_LINKS = [('index.html', 'Home'), ('pricing.html', 'Pricing'), ('about.html', 'About'), ('contact.html', 'Contact')]

def nav(active):
    lis = ''
    for href, label in NAV_LINKS:
        cur = ' cs-active" aria-current="page' if href == active else ''
        lis += f'''
                    <li class="cs-li">
                        <a href="{href}" class="cs-li-link{cur}">
                            {label}
                        </a>
                    </li>'''
    return f'''
<!-- ============================================ -->
<!--                 Navigation                   -->
<!-- ============================================ -->
<header id="cs-navigation">
    <div class="cs-container">
        <!--Nav Logo-->
        <a href="index.html" class="cs-logo" aria-label="Return to Critchfield Systems home page">
            <img src="assets/logo-horizontal.webp" alt="Critchfield Systems" width="900" height="143" decoding="async">
        </a>
        <!--Navigation List-->
        <nav class="cs-nav" aria-label="main navigation">
            <!--Mobile Nav Toggle-->
            <button class="cs-toggle" id="mobile-menu-toggle" aria-expanded="false" aria-controls="cs-ul-wrapper" aria-label="mobile menu toggle" aria-haspopup="menu">
                <span class="cs-box" aria-hidden="true">
                    <span class="cs-line cs-line1"></span>
                    <span class="cs-line cs-line2"></span>
                    <span class="cs-line cs-line3"></span>
                </span>
            </button>
            <div class="cs-ul-wrapper" id="cs-ul-wrapper">
                <ul class="cs-ul">{lis}
                </ul>
            </div>
        </nav>
        <a href="{TEL}" class="cs-button-4 cs-nav-button">Call or Text</a>
    </div>
</header>
'''

FOOTER = f'''
<!-- ============================================ -->
<!--                   Footer                     -->
<!-- ============================================ -->
<footer id="cs-footer-145">
    <div class="cs-container">
        <!-- Logo Group -->
        <div class="cs-logo-group">
            <a aria-label="go back to home" class="cs-logo" href="index.html">
                <img class="cs-logo-img" loading="lazy" decoding="async" src="assets/logo-horizontal-light.webp" alt="Critchfield Systems" width="900" height="143">
            </a>
            <p class="cs-text">
                Professional websites for small businesses for $99/month. Five pages, hosting, SSL and unlimited small edits, live within 48 hours. No contract.
            </p>
        </div>
        <!-- Links -->
        <ul class="cs-nav">
            <li class="cs-nav-li">
                <span class="cs-header">Sitemap</span>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="index.html">Home</a>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="pricing.html">Pricing</a>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="about.html">About</a>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="contact.html">Contact</a>
            </li>
        </ul>
        <ul class="cs-nav">
            <li class="cs-nav-li">
                <span class="cs-header">What You Get</span>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="pricing.html#what-i-offer">5-Page Website</a>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="pricing.html#what-i-offer">Hosting &amp; SSL</a>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="pricing.html#what-i-offer">Unlimited Small Edits</a>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="pricing.html#guarantee">PageSpeed Guarantee</a>
            </li>
        </ul>
        <ul class="cs-nav">
            <li class="cs-nav-li">
                <span class="cs-header">Get Started</span>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="{TEL}">Call Me</a>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="{SMS}">Text Me</a>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="pricing.html#faq">FAQ</a>
            </li>
            <li class="cs-nav-li">
                <a class="cs-nav-link" href="about.html#service-area">Service Area</a>
            </li>
        </ul>
        <!-- Contact Info -->
        <ul class="cs-contact">
            <li class="cs-contact-li">
                <a class="cs-contact-link" href="{TEL}"><span class="cs-label">Call or Text</span>{PHONE_DISPLAY}</a>
            </li>
            <li class="cs-contact-li">
                <a class="cs-contact-link" href="mailto:{EMAIL}"><span class="cs-label">Email</span>{EMAIL}</a>
            </li>
            <li class="cs-contact-li">
                <a class="cs-contact-link cs-address" href="about.html#service-area">
                    <span>Serving small businesses</span> anywhere in the U.S.
                </a>
            </li>
        </ul>
        <!-- Bottom Credits -->
        <div class="cs-bottom">
            <span class="cs-copyright">&copy; <span id="cs-year">2026</span> Critchfield Systems. All rights reserved.</span>
            <!-- Social links from the component go here once profiles exist:
            <a class="cs-social-link" aria-label="visit facebook profile" href="" target="_blank" rel="noopener">...</a> -->
        </div>
    </div>
</footer>
'''

def tail(faq=False):
    s = '\n<script src="js/nav.js" defer></script>\n'
    if faq:
        s += '<script src="js/faq.js" defer></script>\n'
    s += '<script>document.getElementById("cs-year").textContent = new Date().getFullYear();</script>\n'
    return s + '</body>\n</html>\n'

def page(path, title, desc, css, body, faq=False):
    return head(title, desc, css, path) + nav(path) + '\n<main id="main">\n' + body + '\n</main>\n' + FOOTER + tail(faq)

# Shared CTA (components/sections/cta/cta-2574) - used on Home, Pricing, About
def cta(topper, title):
    return f'''
<!-- ============================================ -->
<!--                    CTA                       -->
<!-- ============================================ -->
<section id="cta-2574">
	<div class="cs-container">
		<div class="cs-content">
			<span class="cs-topper">{topper}</span>
			<h2 class="cs-title">{title}</h2>
			<a href="{TEL}" class="cs-button-4">Call or Text {PHONE_DISPLAY}</a>
		</div>
		<ul class="cs-contact-list">
			<li class="cs-item">
				<span class="cs-heading">Call</span>
				<a href="{TEL}" class="cs-link">{PHONE_DISPLAY}</a>
			</li>
			<li class="cs-item">
				<span class="cs-heading">Text</span>
				<a href="{SMS}" class="cs-link">{PHONE_DISPLAY}</a>
			</li>
			<li class="cs-item">
				<span class="cs-heading">Email</span>
				<a href="mailto:{EMAIL}" class="cs-link">{EMAIL}</a>
			</li>
		</ul>
	</div>
	<picture class="cs-background">
		<img src="assets/bg-poly.svg" alt="" width="1266" height="712" decoding="async" loading="lazy" aria-hidden="true">
	</picture>
</section>
'''

def hero_493(topper, h1, text):
    return f'''
<!-- ============================================ -->
<!--                    Hero                      -->
<!-- ============================================ -->
<section id="hero-493">
    <div class="cs-container">
        <div class="cs-content">
            <span class="cs-topper">{topper}</span>
            <h1 class="cs-title">{h1}</h1>
            <p class="cs-text">
                {text}
            </p>
            <a href="{TEL}" class="cs-button-4">Call or Text {PHONE_DISPLAY}</a>
        </div>
    </div>
    <!-- Background: SVG (no photo) -->
    <picture class="cs-background">
        <img decoding="async" src="assets/bg-poly.svg" alt="" width="1266" height="712" aria-hidden="true" fetchpriority="high">
    </picture>
</section>
'''

def faq_items(items, numbered=False, start=1, open_first=True):
    out = ''
    for i, (q, a) in enumerate(items):
        active = ' active' if (i == 0 and open_first) else ''
        num = f'\n                        <span class="cs-number">{start + i}</span>' if numbered else ''
        out += f'''
                <li class="cs-faq-item{active}">
                    <button class="cs-button" aria-expanded="{'true' if active else 'false'}">{num}
                        <span class="cs-button-text">
                            {q}
                        </span>
                    </button>
                    <p class="cs-item-p">
                        {a}
                    </p>
                </li>'''
    return out

# ---------------------------------------------------------------- FAQ copy
Q_INCLUDED = ('What do I get for $99 a month?', 'A custom 5-page website, hosting, an SSL certificate (the padlock in the address bar), unlimited small edits to your text, photos and videos, and my PageSpeed guarantee. One flat monthly price.')
Q_48 = ('How fast can my website be live?', 'Within 48 hours of getting your info. Send me your business details, services and any photos or logo you have, and I build it, show it to you, and put it online.')
Q_CONTRACT = ('Is there a contract?', 'No. It is month to month and you can cancel anytime. I would rather keep your business by doing good work than by locking you in.')
Q_EDITS = ('What counts as a small edit?', 'Swapping or updating text, photos and videos on your pages: new hours, a new service, fresh project photos, a promo video. Text or call me with the change and I take care of it. There is no limit on how many you send.')
Q_SPEED = ('What is the PageSpeed guarantee?', 'Google measures how fast your site loads and uses it when ranking search results. Your site is built to score 90 or higher on Google PageSpeed Insights. If it ever drops below that, I fix it at no extra cost.')
Q_START = ('How do I get started?', f'Call or text me at <a href="{TEL}">{PHONE_DISPLAY}</a>. We talk for a few minutes about your business, I tell you exactly what I need from you, and your site can be live within 48 hours.')
Q_CONTENT = ('What do I need to send you?', 'Your business name, phone number, the services you offer, the area you serve, and any photos or logo you have. No photos yet? No problem. I design clean graphics around your brand so the site looks finished from day one.')
Q_PAGES = ('Which five pages do I get?', 'Most businesses go with Home, About, Services, Contact and one more of their choice, like a Gallery, Reviews or FAQ page. We decide together based on what your customers need to see.')
Q_HOSTING = ('Are hosting and SSL really included?', 'Yes. Fast hosting and an SSL certificate are part of the $99 a month. There are no separate hosting bills and no surprise renewal fees from me.')
Q_TECH = ('Do I need any tech skills?', 'None. You will never log into a page builder or touch code. When you want something changed, you call or text me and it gets done.')
Q_ECOM = ('Can you build an online store?', f'Not on this plan. The $99 plan is built for service businesses that want calls and texts. See <a href="pricing.html#what-i-dont-offer">what I don&rsquo;t offer</a> for the full list.')

# ---------------------------------------------------------------- HOME
HOME_SECTIONS = [
    ('hero/hero-1349-dark-photo-band-circle-accents', '1349', [('https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/on-computer.jpg', '../assets/bg-waves.svg')]),
    ('stats/stats-2596-four-stats-with-descriptions', '2596', []),
    ('services/services-18-circled-icon-grid-line-button', 's18', []),
    ('steps/steps-1173-light-three-icon-steps-arrows', '1173', [('https://csimg.nyc3.cdn.digitaloceanspaces.com/Icons/curved-arrow-light.svg', '../assets/curved-arrow.svg')]),
    ('about/about-333-circle-photo-right-stat-badge', '333', []),
    ('faq/faq-326-centered-rounded-accordion-cards', '326', []),
    ('cta/cta-2574-photo-band-contact-info-row', '2574', []),
]
HOME_OVR = """
/* hero: SVG waves instead of a photo, brand bubbles */
#hero-1349:before { background: linear-gradient(to bottom, rgba(6, 22, 51, .85) 0%, rgba(6, 22, 51, 0) 100%); }
#hero-1349 .cs-background:before { background: var(--deep); opacity: .15; }
#hero-1349 .cs-topper { color: var(--primaryLight); }
#hero-1349 .cs-bubbles1:after, #hero-1349 .cs-bubbles2:after { background: linear-gradient(135deg, var(--primaryLight), var(--primary)); opacity: .55; }
#hero-1349 .cs-bubbles1:before, #hero-1349 .cs-bubbles2:before { border-color: rgba(34, 195, 255, .6); }
#hero-1349 .cs-price { color: var(--primaryLight); white-space: nowrap; }
/* fact strip */
#stats-2596 .cs-container { background-color: var(--ice); border-top: 4px solid var(--primary); }
#stats-2596 .cs-number { color: var(--secondary); border-bottom-color: #D3DEEC; }
#stats-2596 .cs-desc { color: #5B6B86; }
/* what you get - the component's button slot holds the shared .cs-button-4 */
#services-18 .cs-icon { width: 1.75rem; }
#services-18 .cs-section-head { text-align: center; max-width: 80rem; margin: 0 auto clamp(2rem, 4vw, 3rem); }
#services-18 .cs-section-head .cs-title { margin: 0 auto; }
#services-18 .cs-button-4 { margin-top: -4.5rem; outline: 1.25rem solid #ffffff; }
@media only screen and (min-width: 37.5rem) {
  #services-18 .cs-button-4 { margin-top: calc(clamp(4.5rem, 9vw, 5.625rem) * -1); }
}
/* how it works */
#steps-1173 { background-color: var(--ice); }
#steps-1173 .cs-picture { border-color: var(--primary); background: #fff; box-shadow: 0 .75rem 1.5rem -0.5rem rgba(11, 35, 80, .25); }
#steps-1173 .cs-graphic { opacity: .25; }
/* about */
#sbsr-333 .cs-picture { border-color: var(--ice); }
#sbsr-333 .cs-box { background-color: var(--secondary); border-color: var(--ice); }
#sbsr-333 .cs-image-group:after { background: var(--primaryLight); }
#sbsr-333 .cs-image-group:before { background: var(--primary); }
#sbsr-333 .cs-li:before { background: var(--primary); width: 6px; height: 6px; top: .5625rem; }
/* faq */
#faq-326 { background-color: var(--ice); }
#faq-326 .cs-faq-item, #faq-326 .cs-button { background-color: #fff; }
#faq-326 .cs-faq-item { box-shadow: 0 .5rem 1.25rem -0.75rem rgba(11, 35, 80, .25); }
#faq-326 .cs-faq-item.active .cs-button { background-color: var(--primary); color: #fff; }
#faq-326 .cs-faq-item.active .cs-button:before, #faq-326 .cs-faq-item.active .cs-button:after { background-color: #fff; }
""" + CTA_OVR

HOME_BODY = f'''
<!-- ============================================ -->
<!--                    Hero                      -->
<!-- ============================================ -->
<section id="hero-1349">
    <div class="cs-container">
        <div class="cs-content">
            <span class="cs-topper">Websites for Small Businesses</span>
            <h1 class="cs-title">A Professional Website for <span class="cs-price">$99/Month</span></h1>
            <p class="cs-text">
                Five pages, hosting, SSL and unlimited edits. Live within 48 hours, with no contract. Call or text and I take it from there.
            </p>
            <a href="{TEL}" class="cs-button-4">Call or Text {PHONE_DISPLAY}</a>
        </div>
    </div>
    <!--Bubble Groups-->
    <div class="cs-bubbles cs-bubbles1" aria-hidden="true"></div>
    <div class="cs-bubbles cs-bubbles2" aria-hidden="true"></div>
    <!-- Background: SVG waves (no photo) -->
    <picture class="cs-background">
        <img decoding="async" src="assets/bg-waves.svg" alt="" width="1266" height="712" aria-hidden="true" fetchpriority="high">
    </picture>
</section>

<!-- ============================================ -->
<!--                 Fact Strip                   -->
<!-- ============================================ -->
<section id="stats-2596" aria-label="Quick facts">
	<div class="cs-container">
		<ul class="cs-card-group">
			<li class="cs-item">
				<span class="cs-desc">Flat Monthly Price</span>
				<span class="cs-number">
					<span class="cs-color">$</span>99
				</span>
				<p class="cs-item-text">Everything included for one predictable monthly price.</p>
			</li>
			<li class="cs-item">
				<span class="cs-desc">Hours to Go Live</span>
				<span class="cs-number">
					48<span class="cs-color">h</span>
				</span>
				<p class="cs-item-text">Your new site is online within two days of getting your info.</p>
			</li>
			<li class="cs-item">
				<span class="cs-desc">Pages Included</span>
				<span class="cs-number">
					5
				</span>
				<p class="cs-item-text">Room for your home page, services, about, contact and more.</p>
			</li>
			<li class="cs-item">
				<span class="cs-desc">Contracts</span>
				<span class="cs-number">
					0
				</span>
				<p class="cs-item-text">Month to month. Cancel anytime, no strings attached.</p>
			</li>
		</ul>
	</div>
</section>

<!-- ============================================ -->
<!--                What You Get                  -->
<!-- ============================================ -->
<section id="services-18" aria-labelledby="what-you-get-title">
    <div class="cs-section-head">
        <span class="cs-topper">What You Get</span>
        <h2 id="what-you-get-title" class="cs-title">Everything Included for $99/Month</h2>
    </div>
    <div class="cs-container">
        <ul class="cs-card-group">
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('layout')}" loading="lazy" decoding="async" alt="" width="24" height="24" aria-hidden="true">
                </picture>
                <div class="cs-text-group">
                    <h3 class="cs-h3">A 5-Page Website</h3>
                    <p class="cs-item-text">Custom-built pages that tell customers who you are, what you do and how to reach you, on every screen size.</p>
                </div>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('clock')}" loading="lazy" decoding="async" alt="" width="24" height="24" aria-hidden="true">
                </picture>
                <div class="cs-text-group">
                    <h3 class="cs-h3">Live Within 48 Hours</h3>
                    <p class="cs-item-text">No months-long projects. Send me your info and your site is online within two days.</p>
                </div>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('server')}" loading="lazy" decoding="async" alt="" width="24" height="24" aria-hidden="true">
                </picture>
                <div class="cs-text-group">
                    <h3 class="cs-h3">Hosting Included</h3>
                    <p class="cs-item-text">Fast, reliable hosting is part of the price. No separate hosting bill and nothing for you to manage.</p>
                </div>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('lock')}" loading="lazy" decoding="async" alt="" width="24" height="24" aria-hidden="true">
                </picture>
                <div class="cs-text-group">
                    <h3 class="cs-h3">SSL Security</h3>
                    <p class="cs-item-text">The padlock in the address bar that tells visitors and Google your site is safe. Set up and renewed for you.</p>
                </div>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('edit')}" loading="lazy" decoding="async" alt="" width="24" height="24" aria-hidden="true">
                </picture>
                <div class="cs-text-group">
                    <h3 class="cs-h3">Unlimited Small Edits</h3>
                    <p class="cs-item-text">New text, photos or videos? Just text me the change. As many as you need, every month.</p>
                </div>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('gauge')}" loading="lazy" decoding="async" alt="" width="24" height="24" aria-hidden="true">
                </picture>
                <div class="cs-text-group">
                    <h3 class="cs-h3">PageSpeed Guarantee</h3>
                    <p class="cs-item-text">Built to score 90+ on Google PageSpeed Insights. If it ever slips, I fix it at no extra cost.</p>
                </div>
            </li>
        </ul>
        <a href="{TEL}" class="cs-button-4">Call or Text Now</a>
    </div>
</section>

<!-- ============================================ -->
<!--                How It Works                  -->
<!-- ============================================ -->
<section id="steps-1173">
    <div class="cs-container">
        <div class="cs-content">
            <span class="cs-topper">How It Works</span>
            <h2 class="cs-title">Three Steps to Your New Website</h2>
            <p class="cs-text">
                No forms, no meetings, no page builders. One conversation and your business is online.
            </p>
        </div>
        <ul class="cs-card-group">
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('phone')}" alt="" width="40" height="40" loading="lazy" decoding="async" aria-hidden="true">
                </picture>
                <h3 class="cs-h3">1. Call or Text</h3>
                <p class="cs-item-text">
                    Tell me about your business in a quick call or text. I let you know exactly what to send over.
                </p>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('code')}" alt="" width="40" height="40" loading="lazy" decoding="async" aria-hidden="true">
                </picture>
                <h3 class="cs-h3">2. I Build It</h3>
                <p class="cs-item-text">
                    I design and code your 5-page site, then send you a link to look it over and request changes.
                </p>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('rocket')}" alt="" width="40" height="40" loading="lazy" decoding="async" aria-hidden="true">
                </picture>
                <h3 class="cs-h3">3. You Go Live</h3>
                <p class="cs-item-text">
                    Your site is online within 48 hours. Hosting, security and edits are handled from then on.
                </p>
            </li>
        </ul>
    </div>
    <img class="cs-graphic" src="assets/swoosh.svg" alt="" width="840" height="357" loading="lazy" decoding="async" aria-hidden="true">
</section>

<!-- ============================================ -->
<!--                   About                      -->
<!-- ============================================ -->
<section id="sbsr-333">
    <div class="cs-container">
        <div class="cs-image-group">
            <picture class="cs-picture">
                <!-- Swap for the owner photo: assets/owner.jpg -->
                <img loading="lazy" decoding="async" src="assets/portrait-placeholder.svg" alt="" width="630" height="630" aria-hidden="true">
            </picture>
            <div class="cs-box">
                <span class="cs-number">48h</span>
                <span class="cs-desc">To Go<br> Live</span>
            </div>
        </div>
        <div class="cs-content">
            <span class="cs-topper">About Critchfield Systems</span>
            <h2 class="cs-title">One Person, One Phone Number, No Runaround</h2>
            <p class="cs-text">
                Critchfield Systems is a one-person web studio built for small businesses that need a great website without the agency price tag or the do-it-yourself headache. When you call or text, you talk to me, the person who actually builds and looks after your site.
            </p>
            <ul class="cs-ul">
                <li class="cs-li">Hand-built sites that load fast on any phone</li>
                <li class="cs-li">Plain-English answers, never tech jargon</li>
                <li class="cs-li">Changes handled by text, usually same day</li>
                <li class="cs-li">One flat price with no contract</li>
            </ul>
            <a class="cs-button-4" href="about.html">More About Me</a>
        </div>
    </div>
</section>

<!-- ============================================ -->
<!--                    FAQ                       -->
<!-- ============================================ -->
<section id="faq-326">
    <div class="cs-container">
        <div class="cs-content">
            <span class="cs-topper">FAQ</span>
            <h2 class="cs-title">Frequently Asked Questions</h2>
        </div>
        <div class="cs-flex-group">
            <ul class="cs-faq-group">{faq_items([Q_INCLUDED, Q_48, Q_CONTRACT, Q_EDITS, Q_START])}
            </ul>
        </div>
    </div>
</section>
''' + cta('Ready When You Are', 'Get Your Business Online This Week')

# ---------------------------------------------------------------- PRICING
PRICING_SECTIONS = [
    ('hero/hero-493-centered-band-line-eyebrow', '493', []),
    ('why-choose-us/why-choose-us-1371-center-photo-six-icon-cards', '1371', []),
    ('why-choose-us/why-choose-us-1772-dark-heading-beside-icon-grid', '1772', []),
    ('pricing/pricing-2562-three-icon-cards-one-outlined', '2562', [('https://nyc3.digitaloceanspaces.com/csimages2/Roofer/check.svg', '../assets/check.svg')]),
    ('faq/faq-1237-two-numbered-accordion-columns', '1237', []),
    ('cta/cta-2574-photo-band-contact-info-row', '2574', []),
]
PRICING_OVR = HERO_493_OVR + """
/* what I offer */
#why-choose-1371 .cs-picture { background: linear-gradient(135deg, var(--primary), var(--secondary)); }
#why-choose-1371 .cs-picture img { object-fit: contain; }
#why-choose-1371 .cs-price-note { font-weight: 700; color: var(--headerColor); }
/* what I don't offer: dark band in navy (30%) */
#why-choose-1772 { background-color: var(--secondary); }
#why-choose-1772 .cs-topper { color: var(--primaryLight); }
#why-choose-1772 .cs-picture { background-color: var(--primary); box-shadow: 0 .75rem 1.5rem -0.5rem rgba(0, 0, 0, .45); }
#why-choose-1772 .cs-icon { opacity: 1; filter: none; }
#why-choose-1772 .cs-text { color: var(--bodyTextColorWhite); margin-top: 1rem; }
/* guarantee cards */
#pricing-2562 { background-color: var(--ice); }
#pricing-2562 .cs-item.cs-available:before { content: "Guaranteed"; }
#pricing-2562 .cs-item { filter: none; }
#pricing-2562 .cs-icon-wrapper { background-color: #E6F0FB; }
#pricing-2562 .cs-item .cs-button-4 { width: 100%; }
/* faq */
#faq-1237 .cs-faq-item.active, #faq-1237 .cs-faq-item.active .cs-number { background-color: var(--secondary); }
#faq-1237 .cs-faq-item.active .cs-button, #faq-1237 .cs-faq-item.active .cs-number { color: var(--primaryLight); }
#faq-1237 .cs-faq-item.active .cs-button:before, #faq-1237 .cs-faq-item.active .cs-button:after { background-color: var(--primaryLight); }
#faq-1237 .cs-item-p a { font-weight: 700; color: var(--primaryLight); }
""" + CTA_OVR

PRICING_BODY = hero_493('Pricing', 'One Simple Plan: $99/Month',
    'Everything your small business needs to look professional online. No setup headaches, no contract and no surprise bills from me.') + f'''
<!-- ============================================ -->
<!--                What I Offer                  -->
<!-- ============================================ -->
<section id="why-choose-1371">
    <div class="cs-container" id="what-i-offer">
        <div class="cs-content">
            <span class="cs-topper">What I Offer</span>
            <h2 class="cs-title">$99 Per Month, Everything Included, No Contract</h2>
            <p class="cs-text">
                A standard 5-page small business website, built for you and kept running for you. Hosting, security, speed and your edits are all part of the same monthly price.
            </p>
            <p class="cs-text">
                <strong>Month to month. Cancel anytime with no fees or hassle.</strong>
            </p>
        </div>
        <ul class="cs-card-group">
            <li class="cs-item">
                <h3 class="cs-h3">
                    <img class="cs-h3-icon" aria-hidden="true" loading="lazy" decoding="async" src="{icon('layout')}" alt="" width="24" height="24">
                    5-Page Custom Website
                </h3>
                <p class="cs-item-text">
                    Home, About, Services, Contact and one more page of your choice, designed around your business.
                </p>
            </li>
            <li class="cs-item">
                <h3 class="cs-h3">
                    <img class="cs-h3-icon" aria-hidden="true" loading="lazy" decoding="async" src="{icon('clock')}" alt="" width="24" height="24">
                    Live Within 48 Hours
                </h3>
                <p class="cs-item-text">
                    Once I have your info, your website is online within two days.
                </p>
            </li>
            <li class="cs-item">
                <h3 class="cs-h3">
                    <img class="cs-h3-icon" aria-hidden="true" loading="lazy" decoding="async" src="{icon('server')}" alt="" width="24" height="24">
                    Hosting Included
                </h3>
                <p class="cs-item-text">
                    Fast, reliable hosting with no separate bill and nothing for you to manage.
                </p>
            </li>
            <li class="cs-item-picture">
                <picture class="cs-picture">
                    <img loading="lazy" decoding="async" src="assets/site-mockup.svg" alt="Illustration of a small business website on a laptop browser and a phone" width="590" height="418">
                </picture>
            </li>
            <li class="cs-item">
                <h3 class="cs-h3">
                    <img class="cs-h3-icon" aria-hidden="true" loading="lazy" decoding="async" src="{icon('lock')}" alt="" width="24" height="24">
                    SSL Certificate
                </h3>
                <p class="cs-item-text">
                    The secure padlock that visitors and Google look for, set up and renewed for you.
                </p>
            </li>
            <li class="cs-item">
                <h3 class="cs-h3">
                    <img class="cs-h3-icon" aria-hidden="true" loading="lazy" decoding="async" src="{icon('edit')}" alt="" width="24" height="24">
                    Unlimited Small Edits
                </h3>
                <p class="cs-item-text">
                    Text, photo and video changes whenever you need them. Just send a text.
                </p>
            </li>
            <li class="cs-item">
                <h3 class="cs-h3">
                    <img class="cs-h3-icon" aria-hidden="true" loading="lazy" decoding="async" src="{icon('gauge')}" alt="" width="24" height="24">
                    PageSpeed Guarantee
                </h3>
                <p class="cs-item-text">
                    Built to score 90+ on Google PageSpeed Insights, and kept there.
                </p>
            </li>
        </ul>
        <a href="{TEL}" class="cs-button-4">Call or Text to Get Started</a>
    </div>
    <div class="cs-bubbles cs-bubbles1" aria-hidden="true"></div>
    <div class="cs-bubbles cs-bubbles2" aria-hidden="true"></div>
</section>

<!-- ============================================ -->
<!--              What I Don't Offer              -->
<!-- ============================================ -->
<section id="why-choose-1772">
    <div class="cs-container" id="what-i-dont-offer">
        <div class="cs-content">
            <span class="cs-topper">What I Don't Offer</span>
            <h2 class="cs-title">Honest About What This Plan Isn't</h2>
            <p class="cs-text">The $99 plan is built for service businesses that want a fast, professional site that gets the phone ringing. To keep it simple and affordable, it doesn't include:</p>
        </div>
        <ul class="cs-card-group">
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" loading="lazy" decoding="async" src="{icon('cart-white')}" alt="" width="32" height="32">
                </picture>
                <div class="cs-flex">
                    <h3 class="cs-h3">Online Stores</h3>
                    <p class="cs-item-text">
                        No shopping carts, product catalogs or online checkout. This plan is for service businesses, not e-commerce.
                    </p>
                </div>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" loading="lazy" decoding="async" src="{icon('code-white')}" alt="" width="32" height="32">
                </picture>
                <div class="cs-flex">
                    <h3 class="cs-h3">Custom Web Apps</h3>
                    <p class="cs-item-text">
                        No customer logins, member portals, booking systems or custom software.
                    </p>
                </div>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" loading="lazy" decoding="async" src="{icon('share-white')}" alt="" width="32" height="32">
                </picture>
                <div class="cs-flex">
                    <h3 class="cs-h3">Social Media Management</h3>
                    <p class="cs-item-text">
                        I build and maintain your website. Posting to and managing your social accounts isn't part of the plan.
                    </p>
                </div>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" loading="lazy" decoding="async" src="{icon('megaphone-white')}" alt="" width="32" height="32">
                </picture>
                <div class="cs-flex">
                    <h3 class="cs-h3">Paid Ad Campaigns</h3>
                    <p class="cs-item-text">
                        No Google Ads or Facebook Ads management. Your site will be fast and ready if you run ads yourself.
                    </p>
                </div>
            </li>
        </ul>
    </div>
</section>

<!-- ============================================ -->
<!--                  Guarantee                   -->
<!-- ============================================ -->
<section id="pricing-2562">
    <div class="cs-container" id="guarantee">
        <div class="cs-content">
            <div class="cs-content-flex">
                <span class="cs-topper">My Guarantee</span>
                <h2 class="cs-title">Fast, Flexible and Risk Free</h2>
            </div>
            <p class="cs-text">You shouldn't have to gamble on a website. These three promises come with every plan, from day one.</p>
        </div>
        <ul class="cs-card-group">
            <li class="cs-item cs-available">
                <picture class="cs-icon-wrapper">
                    <img class="cs-icon" loading="lazy" decoding="async" src="{icon('zap')}" alt="" width="24" height="24" />
                </picture>
                <h3 class="cs-h3">Speed Guarantee</h3>
                <p class="cs-item-text">Your site is built to score 90+ on Google PageSpeed Insights.</p>
                <ul class="cs-ul">
                    <li class="cs-li">90+ PageSpeed score</li>
                    <li class="cs-li">Fast on phones and computers</li>
                    <li class="cs-li">Fixed at no cost if it slips</li>
                    <li class="cs-li">Re-checked when edits are made</li>
                </ul>
                <a href="{TEL}" class="cs-button-4">Call or Text</a>
                <span class="cs-subtext">Included in $99/month</span>
            </li>
            <li class="cs-item">
                <picture class="cs-picture cs-icon-wrapper">
                    <img class="cs-icon" loading="lazy" decoding="async" src="{icon('unlock')}" alt="" width="24" height="24" />
                </picture>
                <h3 class="cs-h3">No Contract</h3>
                <p class="cs-item-text">Month to month from the very first day. No long-term commitment.</p>
                <ul class="cs-ul">
                    <li class="cs-li">No 12-month lock-in</li>
                    <li class="cs-li">No commitment term</li>
                    <li class="cs-li">One flat monthly price</li>
                </ul>
                <a href="{SMS}" class="cs-button-4">Text Me</a>
                <span class="cs-subtext">Stay because it works</span>
            </li>
            <li class="cs-item">
                <picture class="cs-icon-wrapper">
                    <img class="cs-icon" loading="lazy" decoding="async" src="{icon('x')}" alt="" width="24" height="24" />
                </picture>
                <h3 class="cs-h3">Cancel Anytime</h3>
                <p class="cs-item-text">Need to stop? Tell me and you're done. No cancellation fees.</p>
                <ul class="cs-ul">
                    <li class="cs-li">No cancellation fees</li>
                    <li class="cs-li">Cancel with a call or text</li>
                    <li class="cs-li">No hoops to jump through</li>
                </ul>
                <a href="{TEL}" class="cs-button-4">Call Me</a>
                <span class="cs-subtext">Zero risk to try it</span>
            </li>
        </ul>
    </div>
</section>

<!-- ============================================ -->
<!--                     FAQ                      -->
<!-- ============================================ -->
<section id="faq-1237">
    <div class="cs-container" id="faq">
        <div class="cs-content">
            <span class="cs-topper">Questions</span>
            <h2 class="cs-title">Frequently Asked Questions</h2>
        </div>
        <div class="cs-wrapper">
            <ul class="cs-faq-group">{faq_items([Q_INCLUDED, Q_48, Q_CONTRACT, Q_EDITS, Q_SPEED], numbered=True, start=1)}
            </ul>
            <ul class="cs-faq-group">{faq_items([Q_CONTENT, Q_PAGES, Q_HOSTING, Q_TECH, Q_ECOM], numbered=True, start=6)}
            </ul>
        </div>
    </div>
</section>
''' + cta('No Contract. Cancel Anytime.', 'Your New Website Is One Call or Text Away')
# pricing-2562 middle card: keep the component's markup exactly (picture.cs-icon-wrapper)
PRICING_BODY = PRICING_BODY.replace('<picture class="cs-picture cs-icon-wrapper">', '<picture class="cs-icon-wrapper">')

# ---------------------------------------------------------------- ABOUT
ABOUT_SECTIONS = [
    ('hero/hero-493-centered-band-line-eyebrow', '493', []),
    ('about/about-99-portrait-right-numbered-list', '99', []),
    ('steps/steps-276-four-numbered-timeline-steps', '276', []),
    ('locations/locations-1844-photo-band-four-pill-cards', '1844', []),
    ('cta/cta-2574-photo-band-contact-info-row', '2574', []),
]
ABOUT_OVR = HERO_493_OVR + """
/* story */
#sbsr-99 .cs-picture img { object-fit: cover; }
#sbsr-99 .cs-text + .cs-text { margin-top: 1rem; }
/* how I work */
#steps-276 { background-color: var(--ice); }
/* service area */
#locations-1844 .cs-background:before { background: var(--deep); opacity: .35; }
#locations-1844 .cs-item { background-color: #fff; box-shadow: 0 1rem 2rem -0.75rem rgba(6, 22, 51, .45); }
#locations-1844 .cs-item:hover { background-color: var(--primary); }
#locations-1844 .cs-area-intro { text-align: center; max-width: 44rem; margin: 0 auto clamp(2rem, 4vw, 3rem); position: relative; z-index: 1; }
#locations-1844 .cs-area-intro .cs-topper { color: var(--primaryLight); }
#locations-1844 .cs-area-intro .cs-title { color: #fff; margin-left: auto; margin-right: auto; }
#locations-1844 .cs-area-intro .cs-text { color: var(--bodyTextColorWhite); margin: 0 auto; }
""" + CTA_OVR

ABOUT_BODY = hero_493('About', 'The Person Behind Your Website',
    'Critchfield Systems is a one-person web studio for small businesses. You get one point of contact, honest pricing and a website that actually works for you.') + f'''
<!-- ============================================ -->
<!--                    Story                     -->
<!-- ============================================ -->
<section id="sbsr-99">
    <div class="cs-container">
        <picture class="cs-picture">
            <!-- Swap for the owner photo: assets/owner.jpg -->
            <img loading="lazy" decoding="async" src="assets/portrait-placeholder.svg" alt="" width="500" height="552" aria-hidden="true">
        </picture>
        <div class="cs-content">
            <span class="cs-topper">My Story</span>
            <h2 class="cs-title">Why I Started Critchfield Systems</h2>
            <p class="cs-text">
                Too many good small businesses are stuck with no website, an outdated one, or a do-it-yourself builder they never have time to update. Agencies quote thousands of dollars up front and disappear after launch. I started Critchfield Systems to fix that: a professional website, kept fast and up to date, for one flat monthly price.
            </p>
            <p class="cs-text">
                I keep it simple on purpose. You call or text, I do the work, and you get back to running your business.
            </p>
            <ul class="cs-ul">
                <li class="cs-li">
                    <span class="cs-number">1</span>
                    Fair, flat pricing anyone can afford
                </li>
                <li class="cs-li">
                    <span class="cs-number">2</span>
                    Fast sites that help you show up on Google
                </li>
                <li class="cs-li">
                    <span class="cs-number">3</span>
                    Real answers from a real person
                </li>
                <li class="cs-li">
                    <span class="cs-number">4</span>
                    No contracts, ever
                </li>
            </ul>
            <a class="cs-button-4" href="pricing.html">See What's Included</a>
        </div>
    </div>
</section>

<!-- ============================================ -->
<!--                 How I Work                   -->
<!-- ============================================ -->
<section id="steps-276">
    <div class="cs-container">
        <div class="cs-content">
            <span class="cs-topper">How I Work</span>
            <h2 class="cs-title">A Simple Process from First Call to Launch</h2>
            <p class="cs-text">
                No long questionnaires or weeks of back and forth. Here is exactly what working with me looks like.
            </p>
        </div>
        <ul class="cs-card-group">
            <li class="cs-item">
                <span class="cs-number">01</span>
                <p class="cs-item-text">
                    <strong>You call or text.</strong> We talk about your business, your customers and what you want the site to do.
                </p>
            </li>
            <li class="cs-item">
                <span class="cs-number">02</span>
                <p class="cs-item-text">
                    <strong>You send your info.</strong> Services, service area, photos and logo, whatever you have.
                </p>
            </li>
            <li class="cs-item">
                <span class="cs-number">03</span>
                <p class="cs-item-text">
                    <strong>I build and launch.</strong> You review a preview link, and your site is live within 48 hours.
                </p>
            </li>
            <li class="cs-item">
                <span class="cs-number">04</span>
                <p class="cs-item-text">
                    <strong>I keep it running.</strong> Hosting, SSL, speed and every small edit you text me.
                </p>
            </li>
        </ul>
        <a href="{TEL}" class="cs-button-4">Start With a Call or Text</a>
    </div>
</section>

<!-- ============================================ -->
<!--                Service Area                  -->
<!-- ============================================ -->
<section id="locations-1844" aria-labelledby="service-area-title">
    <div class="cs-area-intro" id="service-area">
        <span class="cs-topper">Service Area</span>
        <h2 class="cs-title" id="service-area-title">Serving Small Businesses Anywhere in the U.S.</h2>
        <p class="cs-text">Everything happens by phone, text and email, so where you are doesn't matter. If you can send a text, I can build your website.</p>
    </div>
    <div class="cs-container">
        <ul class="cs-card-group">
            <li class="cs-item">
                <h3 class="cs-h3">
                    Local Businesses
                </h3>
                <p class="cs-item-text">
                    Contractors, salons, shops and service pros
                </p>
            </li>
            <li class="cs-item">
                <h3 class="cs-h3">
                    All 50 States
                </h3>
                <p class="cs-item-text">
                    100% remote, no office visit needed
                </p>
            </li>
            <li class="cs-item">
                <h3 class="cs-h3">
                    Any Time Zone
                </h3>
                <p class="cs-item-text">
                    Text me whenever it works for you
                </p>
            </li>
            <li class="cs-item">
                <h3 class="cs-h3">
                    Phone &amp; Text First
                </h3>
                <p class="cs-item-text">
                    {PHONE_DISPLAY}
                </p>
            </li>
        </ul>
    </div>
    <picture class="cs-background">
        <img loading="lazy" decoding="async" src="assets/bg-waves.svg" alt="" width="1266" height="712" aria-hidden="true">
    </picture>
</section>
''' + cta("Let's Work Together", 'Ready for a Website That Works as Hard as You Do?')

# ---------------------------------------------------------------- CONTACT
CONTACT_SECTIONS = [
    ('hero/hero-493-centered-band-line-eyebrow', '493', []),
    ('contact/contact-324-light-three-icon-info-row', '324', []),
    ('steps/steps-687-dark-three-icon-steps', '687', []),
    ('faq/faq-1263-dark-centered-accordion', '1263', []),
]
CONTACT_OVR = HERO_493_OVR + """
/* contact cards */
#contact-strip-324 { background-color: var(--ice); }
#contact-strip-324 .cs-item { box-shadow: 0 1rem 2rem -1rem rgba(11, 35, 80, .3); }
#contact-strip-324 .cs-header { color: var(--primary); font-weight: 700; }
#contact-strip-324 .cs-link { color: var(--headerColor); font-weight: 600; overflow-wrap: anywhere; }
#contact-strip-324 .cs-flex-group { min-width: 0; }
#contact-strip-324 .cs-hours { color: var(--bodyTextColor); }
#contact-strip-324 .cs-icon { width: 2.25rem; height: auto; }
/* what happens next - blue band (10% accent used as a single band) */
#process-687 { background-color: var(--primary); }
#process-687 .cs-topper { color: #fff; opacity: .9; }
#process-687 .cs-title, #process-687 .cs-text { color: #fff; }
#process-687 .cs-picture { background-color: #fff; box-shadow: 0 1rem 2rem -0.75rem rgba(6, 22, 51, .5); }
#process-687 .cs-background { opacity: 1; }
/* short faq - navy (30%) */
#faq-1263 { background-color: var(--secondary); }
#faq-1263 .cs-topper { color: var(--primaryLight); }
#faq-1263 .cs-faq-item { background-color: rgba(255, 255, 255, .06); }
#faq-1263 .cs-faq-item.active .cs-button { color: var(--primaryLight); }
#faq-1263 .cs-item-p a { color: var(--primaryLight); font-weight: 700; }
"""

CONTACT_BODY = hero_493('Contact', "Call or Text. I'll Take It from There.",
    f'The fastest way to get your website started is a quick call or text to <a href="{TEL}">{PHONE_DISPLAY}</a>. No forms, no waiting on a sales team.') + f'''
<!-- ============================================ -->
<!--               Contact Cards                  -->
<!-- ============================================ -->
<div id="contact-strip-324">
    <ul class="cs-stat-group">
        <li class="cs-item">
            <picture class="cs-picture">
                <img class="cs-icon" src="{icon('phone')}" alt="" width="24" height="24" loading="lazy" decoding="async" aria-hidden="true">
            </picture>
            <div class="cs-flex-group">
                <span class="cs-header">Call or Text</span>
                <a href="{TEL}" class="cs-link">Call {PHONE_DISPLAY}</a>
                <a href="{SMS}" class="cs-link">Text {PHONE_DISPLAY}</a>
            </div>
        </li>
        <li class="cs-item">
            <picture class="cs-picture">
                <img class="cs-icon" src="{icon('mail')}" alt="" width="24" height="24" loading="lazy" decoding="async" aria-hidden="true">
            </picture>
            <div class="cs-flex-group">
                <span class="cs-header">Email</span>
                <a href="mailto:{EMAIL}" class="cs-link">{EMAIL}</a>
            </div>
        </li>
        <li class="cs-item">
            <picture class="cs-picture">
                <img class="cs-icon" src="{icon('pin')}" alt="" width="24" height="24" loading="lazy" decoding="async" aria-hidden="true">
            </picture>
            <div class="cs-flex-group">
                <span class="cs-header">Service Area</span>
                <span class="cs-hours">Small businesses</span>
                <span class="cs-hours">anywhere in the U.S.</span>
            </div>
        </li>
    </ul>
</div>

<!-- ============================================ -->
<!--             What Happens Next                -->
<!-- ============================================ -->
<section id="process-687">
    <div class="cs-container">
        <div class="cs-content">
            <span class="cs-topper">What Happens Next</span>
            <h2 class="cs-title">From First Message to Live Website</h2>
            <p class="cs-text">
                Here is what to expect after you reach out. No pressure and no obligation.
            </p>
        </div>
        <ul class="cs-card-group">
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" loading="lazy" decoding="async" src="{icon('message')}" alt="" width="42" height="42">
                </picture>
                <h3 class="cs-h3">1. We Talk</h3>
                <p class="cs-item-text">I get back to you, answer your questions and learn what your business needs.</p>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" loading="lazy" decoding="async" src="{icon('send')}" alt="" width="42" height="42">
                </picture>
                <h3 class="cs-h3">2. You Send Your Info</h3>
                <p class="cs-item-text">I send a short list of what I need: services, photos, logo and contact details.</p>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" loading="lazy" decoding="async" src="{icon('rocket')}" alt="" width="42" height="42">
                </picture>
                <h3 class="cs-h3">3. You're Live in 48 Hours</h3>
                <p class="cs-item-text">I build your site, you approve it, and it goes live. Then it's $99/month, cancel anytime.</p>
            </li>
        </ul>
    </div>
    <img class="cs-background" loading="lazy" decoding="async" src="assets/ripples.svg" aria-hidden="true" alt="" width="1280" height="568">
</section>

<!-- ============================================ -->
<!--                     FAQ                      -->
<!-- ============================================ -->
<section id="faq-1263">
    <div class="cs-container">
        <div class="cs-content">
            <span class="cs-topper">Quick Answers</span>
            <h2 class="cs-title">Before You Reach Out</h2>
        </div>
        <ul class="cs-faq-group">{faq_items([Q_START, Q_CONTENT, Q_48, Q_CONTRACT, ('Is it okay to just ask questions first?', 'Of course. Call or text with any questions. There is no obligation and no pushy sales pitch.')])}
        </ul>
    </div>
    <picture class="cs-background">
        <img aria-hidden="true" src="assets/ripples.svg" loading="lazy" decoding="async" alt="" width="1280" height="568">
    </picture>
</section>
'''

# ---------------------------------------------------------------- JS
NAV_JS = open(os.path.join(COMP, 'nav/nav-757-light-single-row-bar/script.js')).read()
FAQ_JS = """// components/sections/faq/*/script.js, plus aria-expanded for screen readers
const faqItems = Array.from(document.querySelectorAll('.cs-faq-item'));
for (const item of faqItems) {
    const button = item.querySelector('.cs-button');
    item.addEventListener('click', () => {
        item.classList.toggle('active');
        if (button) button.setAttribute('aria-expanded', item.classList.contains('active') ? 'true' : 'false');
    });
}
"""

# ---------------------------------------------------------------- write
def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(text)

write('css/root.css', shared_css())
write('css/home.css', page_css(HOME_SECTIONS, HOME_OVR))
write('css/pricing.css', page_css(PRICING_SECTIONS, PRICING_OVR))
write('css/about.css', page_css(ABOUT_SECTIONS, ABOUT_OVR))
write('css/contact.css', page_css(CONTACT_SECTIONS, CONTACT_OVR))
write('js/nav.js', NAV_JS)
write('js/faq.js', FAQ_JS)

D = 'Critchfield Systems builds professional 5-page websites for small businesses for $99/month: hosting, SSL, unlimited small edits and a PageSpeed guarantee. Live in 48 hours, no contract.'
write('index.html', page('index.html', 'Small Business Websites for $99/Month | Critchfield Systems', D, 'home.css', HOME_BODY, faq=True))
write('pricing.html', page('pricing.html', 'Pricing: $99/Month, No Contract | Critchfield Systems', 'One simple plan: a 5-page website, hosting, SSL, unlimited small edits and a PageSpeed guarantee for $99/month. No contract, cancel anytime.', 'pricing.css', PRICING_BODY, faq=True))
write('about.html', page('about.html', 'About | Critchfield Systems', 'Critchfield Systems is a one-person web studio building fast, affordable websites for small businesses anywhere in the U.S.', 'about.css', ABOUT_BODY))
write('contact.html', page('contact.html', 'Contact | Critchfield Systems', f'Call or text {PHONE_DISPLAY} to get your $99/month small business website started. Live within 48 hours.', 'contact.css', CONTACT_BODY, faq=True))

write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
urls = ''.join(f'  <url><loc>{SITE}{u}</loc></url>\n' for u in ['/', '/pricing', '/about', '/contact'])
write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
write('_headers', '/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/css/*\n  Cache-Control: public, max-age=86400\n/js/*\n  Cache-Control: public, max-age=86400\n')
print('built', OUT)
