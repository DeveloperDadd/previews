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

# Microsoft Clarity (approved third-party script exception; see CLAUDE.md). Goes in <head> of every page.
CLARITY = '''    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "zix1q7ur26");
    </script>
'''

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
#cs-footer-145 .cs-bottom { flex-wrap: wrap; gap: .75rem 1.5rem; }
#cs-footer-145 .cs-legal { display: flex; flex-wrap: wrap; gap: .5rem 1.25rem; }
#cs-footer-145 .cs-legal a { color: #9fb0cc; font-size: .9375rem; text-decoration: none; }
#cs-footer-145 .cs-legal a:hover { color: #fff; text-decoration: underline; }
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
{CLARITY}</head>
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
                    <span>Serving all of the U.S.,</span> fully remote
                </a>
            </li>
        </ul>
        <!-- Bottom Credits -->
        <div class="cs-bottom">
            <span class="cs-copyright">&copy; <span id="cs-year">2026</span> Critchfield Systems. All rights reserved.</span>
            <span class="cs-legal"><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms of Service</a></span>
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
Q_SPEED = ('What is the PageSpeed guarantee?', 'Your site scores 90+ on Google PageSpeed Insights. Google measures how fast your site loads and uses it when ranking search results, so a fast site helps you get found.')
Q_START = ('How do I get started?', f'Call or text me at <a href="{TEL}">{PHONE_DISPLAY}</a>. We talk for a few minutes about your business, I tell you exactly what I need from you, and your site can be live within 48 hours.')
Q_CONTENT = ('What do I need to send you?', 'Your business name, phone number, the services you offer, the area you serve, and any photos or logo you have. No photos yet? No problem. I design clean graphics around your brand so the site looks finished from day one.')
Q_PAGES = ('Which five pages do I get?', 'Most businesses go with Home, About, Services, Contact and one more of their choice, like a Gallery, Reviews or FAQ page. We decide together based on what your customers need to see.')
Q_HOSTING = ('Are hosting and SSL really included?', 'Yes. Fast hosting and an SSL certificate are part of the $99 a month. There are no separate hosting bills and no surprise renewal fees from me.')
Q_TECH = ('Do I need any tech skills?', 'None. You will never log into a page builder or touch code. When you want something changed, you call or text me and it gets done.')
Q_WOM = ('I get all my work from word of mouth. Why do I need a website?', 'Because your referrals look you up before they call. When someone hears your name from a friend or neighbor, the first thing they do is search for you. A professional website shows them they found the right business and makes it easy to pick up the phone.')
Q_FB = ('I already have a Facebook page.', 'Keep it. Why not have another lead source, and one that you own? Your website shows up on Google, it is yours instead of a social media platform&rsquo;s, and customers trust a business with a real website more.')
Q_DOMAIN = ('What happens if I cancel? Who owns my domain?', 'Critchfield Systems owns the domain. If you cancel, no hard feelings. There is no contract, so you can walk away at any time.')
Q_ECOM = ('Can you build an online store?', f'Not on this plan. The $99 plan is built for service businesses that want calls and texts. See <a href="pricing.html#what-i-dont-offer">what I don&rsquo;t offer</a> for the full list.')

# ---------------------------------------------------------------- HOME
HOME_SECTIONS = [
    ('hero/hero-1349-dark-photo-band-circle-accents', '1349', [('https://csimg.nyc3.cdn.digitaloceanspaces.com/Images/People/on-computer.jpg', '../assets/bg-waves.svg')]),
    ('services/services-877-three-rounded-photo-cards', '877', []),
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
/* sample of my work: homepage screenshots of the three sample sites */
#services-877 { background-color: #fff; padding-bottom: clamp(2.5rem, 5vw, 3.5rem); }
#services-877 .cs-item { background-color: var(--ice); border-radius: .5rem; overflow: hidden; box-shadow: 0 1rem 2rem -1rem rgba(11, 35, 80, .35); transition: transform .3s, box-shadow .3s; }
#services-877 .cs-item:hover { transform: translateY(-0.25rem); box-shadow: 0 1.5rem 2.5rem -1rem rgba(11, 35, 80, .45); }
#services-877 .cs-picture { height: auto; aspect-ratio: 800 / 525; background-color: var(--ice); border-bottom: 1px solid #D3DEEC; }
#services-877 .cs-picture img { object-position: top; }
#services-877 .cs-link:focus-visible { outline: 3px solid var(--primary); outline-offset: 3px; }
#services-877 .cs-h3, #services-877 .cs-item-text, #services-877 .cs-view { padding: 0 1.25rem; }
#services-877 .cs-trade { display: block; font-size: .8125rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--primary); margin-bottom: .25rem; }
#services-877 .cs-view { display: block; margin-top: .75rem; font-size: .9375rem; font-weight: 700; color: var(--primary); }
#services-877 .cs-button-4 { margin-top: clamp(2rem, 4vw, 3rem); }
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
            <span class="cs-topper">Hand-Coded, Professional Design</span>
            <h1 class="cs-title">Lexington, Kentucky Web Design</h1>
            <p class="cs-text">
                Lexington web design that gets your business found on Google and makes you more money. We build 100% hand-coded websites, for just $99/month. Reach out for a free demo!
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
<!--              Sample of My Work               -->
<!--   components: services-877-three-rounded-photo-cards   -->
<!-- ============================================ -->
<section id="services-877" aria-labelledby="work-title">
    <div class="cs-container">
        <div class="cs-content">
            <span class="cs-topper">Sample of My Work</span>
            <h2 id="work-title" class="cs-title">See What Your Website Could Look Like</h2>
            <p class="cs-text">
                Each one is a full 5-page sample site for a made-up home service business, built exactly the way I would build yours. Click around, then call or text me for a free demo of your own.
            </p>
        </div>
        <ul class="cs-card-group">
            <li class="cs-item">
                <a href="sample/" class="cs-link">
                    <picture class="cs-picture" aria-hidden="true">
                        <img loading="lazy" decoding="async" src="assets/work/sample-roofing.webp" alt="" width="800" height="525">
                    </picture>
                    <h3 class="cs-h3"><span class="cs-trade">Roofing</span>Keystone Ridge Roofing</h3>
                    <p class="cs-item-text">
                        A bold, trustworthy roofer site with services, pricing, a project gallery and FAQs.
                    </p>
                    <span class="cs-view">View the sample site &rarr;</span>
                </a>
            </li>
            <li class="cs-item">
                <a href="sample-landscaping/" class="cs-link">
                    <picture class="cs-picture" aria-hidden="true">
                        <img loading="lazy" decoding="async" src="assets/work/sample-landscaping-v2.webp" alt="" width="800" height="525">
                    </picture>
                    <h3 class="cs-h3"><span class="cs-trade">Landscaping</span>Hollow Creek Lawn &amp; Landscape</h3>
                    <p class="cs-item-text">
                        Earthy greens, seasonal services and a step-by-step estimate process.
                    </p>
                    <span class="cs-view">View the sample site &rarr;</span>
                </a>
            </li>
            <li class="cs-item">
                <a href="sample-plumbing/" class="cs-link">
                    <picture class="cs-picture" aria-hidden="true">
                        <img loading="lazy" decoding="async" src="assets/work/sample-plumbing.webp" alt="" width="800" height="525">
                    </picture>
                    <h3 class="cs-h3"><span class="cs-trade">Plumbing</span>Limestone Plumbing &amp; Drain</h3>
                    <p class="cs-item-text">
                        24/7 emergency focus, an upfront price list and a service-area map.
                    </p>
                    <span class="cs-view">View the sample site &rarr;</span>
                </a>
            </li>
        </ul>
        <a href="{TEL}" class="cs-button-4">Call or Text for a Free Demo</a>
    </div>
</section>

<!-- ============================================ -->
<!--                 Fact Strip                   -->
<!-- ============================================ -->
<section id="stats-2596" aria-label="Quick facts">
	<div class="cs-container">
		<ul class="cs-card-group">
			<li class="cs-item">
				<span class="cs-desc">Flat Monthly Price</span>
				<span class="cs-number">$99</span>
				<p class="cs-item-text">Less than one service call.</p>
			</li>
			<li class="cs-item">
				<span class="cs-desc">Hours to Go Live</span>
				<span class="cs-number">48h</span>
				<p class="cs-item-text">Your new site is online within two days of getting your info.</p>
			</li>
			<li class="cs-item">
				<span class="cs-desc">Guaranteed Page Score</span>
				<span class="cs-number">
					90+
				</span>
				<p class="cs-item-text">Get found on Google. Increase your bottom line.</p>
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
        <h2 id="what-you-get-title" class="cs-title">A Tool to Build Trust, Capture Leads Before They Call</h2>
    </div>
    <div class="cs-container">
        <ul class="cs-card-group">
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('layout')}" loading="lazy" decoding="async" alt="" width="24" height="24" aria-hidden="true">
                </picture>
                <div class="cs-text-group">
                    <h3 class="cs-h3">A 5-Page Website</h3>
                    <p class="cs-item-text">Build trust, inform your customers, make more. Less than the cost of one service call.</p>
                </div>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('clock')}" loading="lazy" decoding="async" alt="" width="24" height="24" aria-hidden="true">
                </picture>
                <div class="cs-text-group">
                    <h3 class="cs-h3">Live Within 48 Hours</h3>
                    <p class="cs-item-text">No back and forth with an agency. Send me your info and your site is online within two days.</p>
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
                    <p class="cs-item-text">No 'Not Secure' warning scaring your customers off.</p>
                </div>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('edit')}" loading="lazy" decoding="async" alt="" width="24" height="24" aria-hidden="true">
                </picture>
                <div class="cs-text-group">
                    <h3 class="cs-h3">Unlimited Small Edits</h3>
                    <p class="cs-item-text">New text, photos or videos? Just text me the change, I'll have it up the same day.</p>
                </div>
            </li>
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" src="{icon('gauge')}" loading="lazy" decoding="async" alt="" width="24" height="24" aria-hidden="true">
                </picture>
                <div class="cs-text-group">
                    <h3 class="cs-h3">PageSpeed Guarantee</h3>
                    <p class="cs-item-text">Your customers don't have time to wait, don't lead them to your competitor. A fast website will keep them dialed in</p>
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
                No forms, no meetings, no page builders. One conversation and your business is online and making more.
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
                <img loading="lazy" decoding="async" src="assets/clayton-square.webp" alt="Clayton Critchfield, owner of Critchfield Systems" width="630" height="630">
            </picture>
            <div class="cs-box">
                <span class="cs-number">48h</span>
                <span class="cs-desc">To Go<br> Live</span>
            </div>
        </div>
        <div class="cs-content">
            <span class="cs-topper">Meet Clayton Critchfield</span>
            <h2 class="cs-title">One Person, No Runaround</h2>
            <p class="cs-text">
                I'm Clayton Critchfield, I help small businesses that need a great website without the agency price tag or the do-it-yourself headache. When you call or text, you talk to me, 
				the person who actually builds and looks after your site.
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
            <ul class="cs-faq-group">{faq_items([Q_INCLUDED, Q_48, Q_CONTRACT, Q_EDITS, Q_WOM, Q_FB, Q_DOMAIN, Q_START])}
            </ul>
        </div>
    </div>
</section>
''' + cta('Ready When You Are', 'Your Customers Are Looking For Your Business Right Now')

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
                    Scores 90+ on Google PageSpeed Insights.
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
            <li class="cs-item">
                <picture class="cs-picture">
                    <img class="cs-icon" loading="lazy" decoding="async" src="{icon('camera-white')}" alt="" width="32" height="32">
                </picture>
                <div class="cs-flex">
                    <h3 class="cs-h3">Professional Photography</h3>
                    <p class="cs-item-text">
                        No photo shoots. Send me the photos you have, and if you have none I design clean graphics around your brand.
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
                <p class="cs-item-text">Scores 90+ on Google PageSpeed Insights.</p>
                <ul class="cs-ul">
                    <li class="cs-li">Scores 90+ on Google PageSpeed Insights</li>
                    <li class="cs-li">Fast on phones and computers</li>
                    <li class="cs-li">Included with every site</li>
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
            <ul class="cs-faq-group">{faq_items([Q_INCLUDED, Q_48, Q_CONTRACT, Q_EDITS, Q_SPEED, Q_WOM, Q_FB], numbered=True, start=1)}
            </ul>
            <ul class="cs-faq-group">{faq_items([Q_CONTENT, Q_PAGES, Q_HOSTING, Q_TECH, Q_ECOM, Q_DOMAIN], numbered=True, start=8)}
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
    'I&rsquo;m Clayton Critchfield. Critchfield Systems is my one-person web studio for small businesses. You get one point of contact, honest pricing and a website that actually works for you.') + f'''
<!-- ============================================ -->
<!--                    Story                     -->
<!-- ============================================ -->
<section id="sbsr-99">
    <div class="cs-container">
        <picture class="cs-picture">
            <img loading="lazy" decoding="async" src="assets/clayton-portrait.webp" alt="Clayton Critchfield, owner of Critchfield Systems" width="500" height="552">
        </picture>
        <div class="cs-content">
            <span class="cs-topper">My Story</span>
            <h2 class="cs-title">Why I Started Critchfield Systems</h2>
            <p class="cs-text">
                Hi, I'm Clayton Critchfield. Too many good small businesses are stuck with no website, an outdated one, or a do-it-yourself builder they never have time to update. Agencies quote thousands of dollars up front and disappear after launch. I started Critchfield Systems to fix that: a professional website, kept fast and up to date, for one flat monthly price.
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
        <h2 class="cs-title" id="service-area-title">All of the U.S., Fully Remote</h2>
        <p class="cs-text">I work with small businesses in every state. Everything happens by phone, text and email, so where you are doesn&rsquo;t matter.</p>
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
                    Call, Text or Email
                </h3>
                <p class="cs-item-text">
                    {PHONE_DISPLAY}<br>{EMAIL}
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
    f'The fastest way to get your website started is a quick call or text to <a href="{TEL}">{PHONE_DISPLAY}</a>, or email <a href="mailto:{EMAIL}">{EMAIL}</a>. No forms, no waiting on a sales team.') + f'''
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
                <span class="cs-hours">All of the U.S.</span>
                <span class="cs-hours">Fully remote</span>
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
        <ul class="cs-faq-group">{faq_items([Q_START, Q_CONTENT, Q_48, Q_CONTRACT, Q_WOM, Q_FB, Q_DOMAIN, ('Is it okay to just ask questions first?', 'Of course. Call or text with any questions. There is no obligation and no pushy sales pitch.')])}
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


# ---------------------------------------------------------------- legal pages
LEGAL_UPDATED = 'November 24, 2026'
LEGAL_SECTIONS = [
    ('hero/hero-493-centered-band-line-eyebrow', '493', []),
]
LEGAL_OVR = HERO_493_OVR + """
#legal { padding: var(--sectionPadding); background-color: #fff; }
#legal .cs-container { max-width: 50rem; margin: 0 auto; }
#legal h2 { font-size: clamp(1.25rem, 2.4vw, 1.5rem); font-weight: 800; line-height: 1.25em; color: var(--headerColor); margin: 2.5rem 0 .75rem; }
#legal h2:first-child { margin-top: 0; }
#legal p, #legal li { font-size: var(--bodyFontSize); line-height: 1.75em; color: var(--bodyTextColor); }
#legal p { margin: 0 0 1rem; }
#legal ul { margin: 0 0 1rem; padding-left: 1.25rem; }
#legal li { margin-bottom: .5rem; }
#legal a { color: var(--primary); font-weight: 600; }
#legal .cs-updated { font-weight: 600; color: var(--headerColor); }
"""

PRIVACY_BODY = hero_493('Legal', 'Privacy Policy', f'How Critchfield Systems collects, uses and protects your information. Last updated {LEGAL_UPDATED}.') + f'''
<section id="legal">
    <div class="cs-container">
        <h2>Who we are</h2>
        <p>Critchfield Systems (&ldquo;we,&rdquo; &ldquo;us&rdquo; or &ldquo;our&rdquo;) is a web design business based in Lexington, Kentucky. We build and host websites for small businesses and serve customers across the United States remotely. This policy explains what information we collect when you visit <a href="{SITE}">critchfieldsystems.com</a> or contact us, and how we use it. Questions? Call or text <a href="{TEL}">{PHONE_DISPLAY}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

        <h2>Information we collect</h2>
        <p><strong>Information you give us.</strong> This website does not have a sign-up or contact form. We receive information when you call, text or email us, and when you become a customer. That can include:</p>
        <ul>
            <li>Your name, phone number and email address</li>
            <li>Your business name, services, service area and hours</li>
            <li>Photos, logos, videos and text you send us to put on your website</li>
            <li>The content of your messages, and billing details needed to charge you for your plan</li>
        </ul>
        <p><strong>Information collected automatically.</strong> When you visit this website, we and our service providers receive technical information such as your IP address, browser and device type, operating system, the pages you view, how long you stay, the website that referred you, and your approximate location (for example, city or region) based on your IP address. With our session-recording tool (described below), we also see how you interact with pages, such as clicks, taps, scrolling and mouse movement.</p>

        <h2>How we use your information</h2>
        <ul>
            <li>To respond to your calls, texts and emails</li>
            <li>To build, host, secure and maintain your website</li>
            <li>To bill you and keep records</li>
            <li>To understand how people use this website so we can fix problems and make it faster and clearer</li>
            <li>To protect against fraud, abuse and security threats, and to meet legal obligations</li>
        </ul>

        <h2>Analytics, cookies and similar tools</h2>
        <p>This website uses the following third-party services:</p>
        <ul>
            <li><strong>Cloudflare</strong> hosts this website and provides Cloudflare Web Analytics for basic traffic statistics. Cloudflare describes Web Analytics as privacy-focused, and it does not use cookies to track visitors. Cloudflare also processes visitor IP addresses as part of delivering and securing the site. See the <a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener">Cloudflare Privacy Policy</a>.</li>
            <li><strong>Microsoft Clarity</strong> is a free analytics tool that records how visitors use this website, including session replays and heatmaps. Clarity uses cookies and similar technologies to recognize a visit across pages, and it masks sensitive content by default. Microsoft receives and processes this data under the <a href="https://privacy.microsoft.com/en-us/privacystatement" target="_blank" rel="noopener">Microsoft Privacy Statement</a> and the <a href="https://clarity.microsoft.com/terms" target="_blank" rel="noopener">Clarity terms</a>.</li>
            <li><strong>Google Fonts</strong> serves the typeface used on this website. When a page loads, your browser requests the font from Google, which means Google receives your IP address. See the <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google Privacy Policy</a>.</li>
        </ul>
        <p>You can limit cookies and tracking through your browser settings, a content blocker or a privacy-focused browser. Blocking these tools will not stop you from using the website.</p>

        <h2>Text messages</h2>
        <p>If you text us, we use your phone number and message only to reply and to provide our services. We do not sell or share mobile phone numbers or text messaging opt-in information with third parties for their marketing or promotional purposes. If we ever send you recurring or automated text messages, we will first get your consent, tell you how often to expect messages, and you can reply STOP at any time to opt out or HELP for help. Message and data rates may apply.</p>

        <h2>How we share information</h2>
        <p>We do not sell your personal information. We share it only with:</p>
        <ul>
            <li><strong>Service providers</strong> that help us run the business, such as hosting, analytics, payment processing, email and phone services. They may use the information only to provide services to us.</li>
            <li><strong>Legal and safety recipients</strong> when we believe disclosure is required by law, or necessary to protect our rights, our customers or others.</li>
            <li><strong>A successor</strong> if our business is sold or transferred, in which case this policy continues to apply to your information.</li>
        </ul>
        <p>If you are a customer, the business information and content you ask us to publish on your website becomes public when the site goes live.</p>

        <h2>How long we keep information</h2>
        <p>We keep information only as long as we need it for the purposes above, to keep business and tax records, and to resolve disputes. When it is no longer needed, we delete it or de-identify it. Analytics providers keep data under their own retention periods.</p>

        <h2>Your choices</h2>
        <p>You can ask us to access, correct or delete the personal information we hold about you by calling, texting or emailing us. Depending on where you live, you may have additional privacy rights under state law. We will respond to reasonable requests as required by law. We may need to verify your identity first.</p>

        <h2>Security</h2>
        <p>This website is served over HTTPS, and we use reputable providers to host and protect it. No method of transmission or storage is completely secure, so we cannot guarantee absolute security.</p>

        <h2>Children</h2>
        <p>This website is intended for business owners and is not directed to children under 13. We do not knowingly collect personal information from children. If you believe a child has given us information, contact us and we will delete it.</p>

        <h2>Changes to this policy</h2>
        <p>We may update this policy from time to time. The &ldquo;last updated&rdquo; date at the top shows when it last changed. Continuing to use the website after an update means you accept the updated policy.</p>

        <h2>Contact us</h2>
        <p>Critchfield Systems<br>Lexington, Kentucky<br><a href="{TEL}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
</section>
'''

TERMS_BODY = hero_493('Legal', 'Terms of Service', f'The terms that apply when you use this website or sign up for a Critchfield Systems website plan. Last updated {LEGAL_UPDATED}.') + f'''
<section id="legal">
    <div class="cs-container">
        <h2>Agreement to these terms</h2>
        <p>These Terms of Service (&ldquo;Terms&rdquo;) are an agreement between you and Critchfield Systems (&ldquo;we,&rdquo; &ldquo;us&rdquo; or &ldquo;our&rdquo;), a web design business based in Lexington, Kentucky. They apply when you visit <a href="{SITE}">critchfieldsystems.com</a> and when you sign up for our website plan (the &ldquo;Service&rdquo;). By using this website or the Service, you agree to these Terms and to our <a href="privacy.html">Privacy Policy</a>. If you do not agree, please do not use them.</p>

        <h2>The Service</h2>
        <p>For a flat monthly fee, the Service includes:</p>
        <ul>
            <li>A custom 5-page website designed around your business</li>
            <li>Website hosting and an SSL certificate, set up and renewed for you</li>
            <li>Unlimited small edits, meaning updates to the text, photos and videos on your existing pages, such as new hours, a new service or fresh project photos</li>
            <li>Our PageSpeed commitment, described below</li>
        </ul>
        <p>We aim to put your website online within 48 hours of receiving the information we need from you. Timing depends on how quickly you send us your business details, photos and approvals.</p>

        <h2>What is not included</h2>
        <p>The plan is built for service businesses and does not include online stores or shopping carts, custom web applications (such as customer logins, member portals or booking systems), social media management, paid advertising management, or professional photography. Redesigns, new pages beyond the five included and other custom work are not &ldquo;small edits.&rdquo; If you need something that is not included, we will tell you before we do any work and agree on a price in advance.</p>

        <h2>Fees and billing</h2>
        <p>The plan is $99 per month, billed monthly, plus any applicable taxes. By signing up, you authorize us to charge the payment method you provide each month until you cancel. We will tell you at least 30 days before any change in price, and you may cancel before the new price applies.</p>

        <h2>Month to month and cancellation</h2>
        <p>There is no contract and no cancellation fee. You can cancel at any time by calling, texting or emailing us. Cancellation takes effect at the end of the month you have already paid for, and we do not refund partial months. When your plan ends, your website will be taken offline. On request, we will send you the text, photos and logos you provided to us.</p>

        <h2>Your content and responsibilities</h2>
        <p>You are responsible for the accuracy of the information you give us and for having the right to use everything you send us, including logos, photos, text, videos and any third-party material. You promise that your content does not infringe anyone&rsquo;s rights and is not unlawful, misleading or harmful. You keep ownership of your content and give us permission to use, copy, display and modify it as needed to build, host and maintain your website. You are also responsible for the claims your business makes about itself, including prices, licenses, certifications and reviews.</p>

        <h2>Ownership</h2>
        <ul>
            <li><strong>Domain name.</strong> Critchfield Systems owns and registers the domain name used for your website.</li>
            <li><strong>Website design and code.</strong> We own the design, code and underlying materials we create. While your plan is active, you have the right to use them for your business&rsquo;s website.</li>
            <li><strong>Your content.</strong> You keep ownership of the content you provide, as described above.</li>
        </ul>

        <h2>PageSpeed commitment</h2>
        <p>We design your site to score 90 or higher on Google PageSpeed Insights. If your site scores below 90 for reasons within our control, we will fix it at no extra charge. This commitment does not apply to score drops caused by things outside our control, such as third-party scripts or embeds you ask us to add, very large images or videos you provide, changes Google makes to how it measures speed, or variations between tests and testing conditions.</p>

        <h2>Third-party services and availability</h2>
        <p>Your website depends on third-party providers, including hosting, domain and internet infrastructure. We work to keep your site online and secure, but we do not guarantee uninterrupted or error-free service, and we are not responsible for outages or failures of those providers.</p>

        <h2>Acceptable use</h2>
        <p>You may not use the Service or this website to break the law, to infringe others&rsquo; rights, to send spam or malware, to publish deceptive or harmful content, or to interfere with the website&rsquo;s security or operation. We may remove content or suspend a site that violates these Terms or the law, and we will try to notify you when we do.</p>

        <h2>Disclaimers</h2>
        <p>The website and the Service are provided &ldquo;as is&rdquo; and &ldquo;as available.&rdquo; To the fullest extent permitted by law, we disclaim all warranties, express or implied, including warranties of merchantability, fitness for a particular purpose and non-infringement. We do not guarantee any particular number of visitors, calls, search rankings or sales.</p>

        <h2>Limitation of liability</h2>
        <p>To the fullest extent permitted by law, Critchfield Systems will not be liable for any indirect, incidental, special, consequential or punitive damages, or for lost profits, revenue, data or business opportunities, arising from your use of the website or the Service. Our total liability for any claim relating to the Service will not exceed the amount you paid us in the three months before the event that gave rise to the claim. Some jurisdictions do not allow certain limitations, so some of these may not apply to you.</p>

        <h2>Indemnification</h2>
        <p>You agree to defend and hold us harmless from claims, losses and expenses (including reasonable attorney fees) arising from the content you provide, your use of the Service in violation of these Terms, or your violation of any law or third-party right.</p>

        <h2>Using this website</h2>
        <p>The information on this website is for general information about our services. The text, design, graphics and code on this website belong to Critchfield Systems, and you may not copy or reuse them without our written permission. Sample sites shown on this website are examples and are not real businesses.</p>

        <h2>Governing law</h2>
        <p>These Terms are governed by the laws of the Commonwealth of Kentucky, without regard to conflict-of-law rules. Any dispute that cannot be resolved informally will be brought in the state or federal courts located in Fayette County, Kentucky, and you agree to their jurisdiction.</p>

        <h2>Changes to these Terms</h2>
        <p>We may update these Terms from time to time. The &ldquo;last updated&rdquo; date at the top shows the latest version. For active customers, we will give at least 30 days&rsquo; notice of material changes, and you may cancel before they take effect. Continuing to use the website or the Service after changes take effect means you accept them.</p>

        <h2>Contact us</h2>
        <p>Critchfield Systems<br>Lexington, Kentucky<br><a href="{TEL}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
</section>
'''

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
write('about.html', page('about.html', 'About | Critchfield Systems', 'Critchfield Systems is a one-person web studio building fast, affordable websites for small businesses across the U.S., fully remote.', 'about.css', ABOUT_BODY))
write('contact.html', page('contact.html', 'Contact | Critchfield Systems', f'Call or text {PHONE_DISPLAY} to get your $99/month small business website started. Live within 48 hours.', 'contact.css', CONTACT_BODY, faq=True))

write('css/legal.css', page_css(LEGAL_SECTIONS, LEGAL_OVR))
write('privacy.html', page('privacy.html', 'Privacy Policy | Critchfield Systems', 'How Critchfield Systems collects, uses and protects your information.', 'legal.css', PRIVACY_BODY))
write('terms.html', page('terms.html', 'Terms of Service | Critchfield Systems', 'The terms that apply to this website and the Critchfield Systems website plan.', 'legal.css', TERMS_BODY))

write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
urls = ''.join(f'  <url><loc>{SITE}{u}</loc></url>\n' for u in ['/', '/pricing', '/about', '/contact', '/privacy', '/terms'])
write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
write('_headers', '/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/css/*\n  Cache-Control: public, max-age=86400\n/js/*\n  Cache-Control: public, max-age=86400\n')
print('built', OUT)
