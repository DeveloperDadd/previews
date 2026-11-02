#!/usr/bin/env python3
"""Build a one-page preview site from _content/<slug>.json.

Usage:
    python3 _tools/build.py <slug>

Reads   _content/<slug>.json   (the business details)
        _tools/config.json     (your agency name, preview base URL)
        _template/index.html   (the page template)
Writes  <slug>/index.html

Prints any problems, the preview URL, and every "guesses" entry so you can
check it before sending. Exits with status 1 if a required field is missing.
Standard library only, so it runs anywhere Python 3.8+ is installed.
"""
import datetime
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# paint = brand colour (header, hero, footer), deep = darker shade,
# sign = highlight for stars, stripes and the call button.
PALETTES = {
    "navy":  {"paint": "#1D3557", "deep": "#13243B", "sign": "#F4C542"},
    "red":   {"paint": "#9E2A22", "deep": "#6B1C17", "sign": "#F6DFA0"},
    "green": {"paint": "#2D5A3D", "deep": "#1D3D29", "sign": "#E9D57A"},
    "teal":  {"paint": "#135E63", "deep": "#0B4246", "sign": "#F2D06B"},
    "slate": {"paint": "#36454F", "deep": "#222D34", "sign": "#F29A3A"},
    "plum":  {"paint": "#5B2A4A", "deep": "#3D1B32", "sign": "#F1C6A8"},
}
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
REQUIRED = ["slug", "name", "category", "city", "headline", "intro", "phone",
            "palette", "listing_url", "services"]


def esc(value):
    return html.escape(str(value), quote=True)


def tel_link(phone):
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        digits = "1" + digits
    return "+" + digits


def stars(rating):
    full = max(0, min(5, int(round(float(rating)))))
    return "★" * full + "☆" * (5 - full)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 _tools/build.py <slug>")
    slug = sys.argv[1].strip().strip("/")
    src = ROOT / "_content" / f"{slug}.json"
    if not src.exists():
        sys.exit(f"Not found: {src}")

    d = load(src)
    cfg = load(ROOT / "_tools" / "config.json")
    errors, warnings = [], []

    for key in REQUIRED:
        if not d.get(key):
            errors.append(f"missing required field: {key}")
    if d.get("slug") and d["slug"] != slug:
        errors.append(f"slug in file ({d['slug']}) doesn't match file name ({slug})")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        errors.append("slug must be lowercase letters, numbers and single hyphens")
    if d.get("palette") and d["palette"] not in PALETTES:
        errors.append(f"palette must be one of: {', '.join(PALETTES)}")
    if d.get("phone") and len(re.sub(r"\D", "", d["phone"])) not in (10, 11):
        errors.append(f"phone doesn't look like a US number: {d['phone']}")
    if errors:
        print("Build stopped:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    name = d["name"].strip()
    phone = d["phone"].strip()
    pal = PALETTES[d["palette"]]
    sample = bool(d.get("sample"))

    if len(d["headline"]) > 90:
        warnings.append(f"headline is {len(d['headline'])} characters; aim for under 90")
    services = d["services"]
    if not 3 <= len(services) <= 8:
        warnings.append(f"{len(services)} services; 3 to 8 reads best")

    # Name size: long names step down so they stay on two or three lines.
    # Without a photo the name has the full width, so it gets one size up.
    sizes = ["", "medium", "long"]
    step = 0 if len(name) <= 16 else (1 if len(name) <= 28 else 2)
    if not [p for p in d.get("photos", []) if str(p.get("url", "")).startswith("https://")]:
        step = max(0, step - 1)
    name_size = sizes[step]

    # Rating line
    rating_html = ""
    if d.get("rating") and d.get("review_count"):
        count = int(d["review_count"])
        rating_html = (
            f'<p class="rating"><span class="stars" aria-hidden="true">{stars(d["rating"])}</span>'
            f'<span><strong>{float(d["rating"]):.1f}</strong> from '
            f'<a href="{esc(d["listing_url"])}">{count:,} Google review{"s" if count != 1 else ""}</a></span></p>'
        )

    # Photos: the first is the hero image, the next up to 3 form a gallery.
    photos = [p for p in d.get("photos", []) if str(p.get("url", "")).startswith("https://")]
    if len(photos) != len(d.get("photos", [])):
        warnings.append("dropped photos without an https:// URL")

    # Sections after "What we do" alternate grey, white, grey... so neighbours never match.
    reviews = d.get("reviews", [])
    order = (["gallery"] if len(photos) >= 3 else []) + (["reviews"] if reviews else []) + ["area", "contact"]
    alt = {key: (" alt" if i % 2 == 0 else "") for i, key in enumerate(order)}
    hero_photo_html, hero_grid_class, gallery_html = "", "", ""
    if photos:
        p = photos[0]
        hero_grid_class = " has-photo"
        hero_photo_html = (
            f'<div class="hero-photo"><img src="{esc(p["url"])}" alt="{esc(p.get("alt", ""))}" '
            f'referrerpolicy="no-referrer" width="1200" height="900"></div>'
        )
    if len(photos) >= 3:
        imgs = "\n".join(
            f'        <img src="{esc(p["url"])}" alt="{esc(p.get("alt", ""))}" loading="lazy" '
            f'referrerpolicy="no-referrer" width="800" height="600">'
            for p in photos[1:4]
        )
        gallery_html = (
            f'  <section class="section{alt["gallery"]}" id="work">\n    <div class="wrap">\n'
            '      <h2>Recent work</h2>\n      <p class="section-intro">'
            f'{esc(d.get("gallery_intro", "A few recent jobs."))}</p>\n'
            f'      <div class="gallery">\n{imgs}\n      </div>\n    </div>\n  </section>'
        )

    services_html = "\n".join(
        f'        <li><h3>{esc(s["name"])}</h3>'
        + (f'<p>{esc(s["detail"])}</p>' if s.get("detail") else "")
        + "</li>"
        for s in services
    )

    # Reviews: real reviews only, up to 3.
    if len(reviews) > 3:
        warnings.append(f"{len(reviews)} reviews given; showing the first 3")
        reviews = reviews[:3]
    reviews_html = ""
    if reviews:
        alt_reviews = alt["reviews"]
        items = []
        for r in reviews:
            who = "Sample review" if sample else f'{esc(r.get("author", "Customer"))} on Google'
            if len(r.get("text", "")) > 320:
                warnings.append(f"review by {r.get('author')} is long; trim it to its best 1-3 sentences")
            items.append(
                '        <figure class="review">'
                f'<span class="stars" aria-label="{int(r.get("rating", 5))} out of 5 stars">{stars(r.get("rating", 5))}</span>'
                f'<blockquote><p>{esc(r["text"])}</p></blockquote>'
                f'<figcaption>{who}</figcaption></figure>'
            )
        more = ""
        if d.get("review_count"):
            more = (f'      <a class="more-link" href="{esc(d["listing_url"])}">'
                    f'Read all {int(d["review_count"]):,} reviews on Google</a>\n')
        reviews_html = (
            f'  <section class="section{alt_reviews}" id="reviews">\n    <div class="wrap">\n'
            '      <h2>What customers say</h2>\n'
            '      <div class="reviews">\n' + "\n".join(items) + "\n      </div>\n"
            + more + "    </div>\n  </section>"
        )
    else:
        warnings.append("no reviews; the reviews section is left out")

    # Area / location column
    area = d.get("service_area", [])
    address = (d.get("address") or "").strip()
    parts = []
    if area:
        towns = "\n".join(f"          <li>{esc(t)}</li>" for t in area)
        parts.append(f'        <h2>Where we work</h2>\n        <p class="section-intro">'
                     f'{esc(d.get("area_intro", "We serve " + d["city"] + " and nearby towns, including:"))}</p>\n'
                     f'        <ul class="towns">\n{towns}\n        </ul>')
    if address:
        heading = "Visit us" if area else "Where to find us"
        tag = "h3 class=\"sub\"" if area else "h2"
        close = "h3" if area else "h2"
        parts.append(f'        <{tag}>{heading}</{close}>\n'
                     f'        <address class="address">{esc(address)}</address>\n'
                     f'        <a class="more-link" style="margin-top:0" href="{esc(d["listing_url"])}">Get directions</a>')
    if not parts:
        warnings.append("no service_area or address; the location column is empty")
    area_html = "      <div>\n" + "\n".join(parts) + "\n      </div>"

    # Hours
    hours = d.get("hours", {})
    hours_html = ""
    if hours:
        missing = [day for day in DAYS if day not in hours]
        if missing:
            warnings.append(f"hours missing for: {', '.join(missing)}")
        rows = "\n".join(
            f'          <tr data-day="{day}"><th scope="row">{day}</th><td>{esc(hours[day])}</td></tr>'
            for day in DAYS if day in hours
        )
        hours_html = ('      <div>\n        <h2>Hours</h2>\n        <table class="hours">\n'
                      f'{rows}\n        </table>\n      </div>')
    else:
        warnings.append("no hours; the hours table is left out")

    # Preview notice and credit
    agency = (cfg.get("agency_name") or "").strip()
    agency_url = (cfg.get("agency_url") or "").strip()
    if sample:
        note = "Sample preview. The business, reviews and details on this page are made up."
    else:
        note = f"This is a preview of a new website for {esc(name)}. It isn't live yet."
    if agency:
        who = f'<a href="{esc(agency_url)}">{esc(agency)}</a>' if agency_url else esc(agency)
        note += f" Made by {who}."
        credit_html = f"<p>Website by {who}</p>"
    else:
        credit_html = ""

    values = {
        "title": esc(f"{name} | {d['category']} in {d['city']}"),
        "headline": esc(d["headline"]),
        "paint": pal["paint"], "deep": pal["deep"], "sign": pal["sign"],
        "preview_note": note,
        "name": esc(name),
        "name_size": name_size,
        "tel": tel_link(phone),
        "phone": esc(phone),
        "hero_grid_class": hero_grid_class,
        "rating_html": rating_html,
        "hero_photo_html": hero_photo_html,
        "quote_label": esc(d.get("quote_label", "Request a quote")),
        "intro": esc(d["intro"]),
        "services_html": services_html,
        "gallery_html": gallery_html,
        "reviews_html": reviews_html,
        "area_alt": alt["area"],
        "area_html": area_html,
        "hours_html": hours_html,
        "contact_alt": alt["contact"],
        "contact_heading": esc(d.get("contact_heading", "Get a quote")),
        "contact_intro": esc(d.get("contact_intro",
                             f"Call us, or tell us what you need and we'll get back to you.")),
        "form_prompt": esc(d.get("form_prompt", "What do you need?")),
        "submit_label": esc(d.get("submit_label", "Send request")),
        "footer_address_html": f"<p>{esc(address)}</p>" if address else "",
        "year": str(datetime.date.today().year),
        "credit_html": credit_html,
    }

    template = (ROOT / "_template" / "index.html").read_text(encoding="utf-8")
    page = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], template)
    leftover = re.findall(r"\{\{\w+\}\}", page)
    if leftover:
        sys.exit(f"Template has unfilled slots: {leftover}")
    if 'name="robots" content="noindex' not in page:
        sys.exit("Safety check failed: noindex tag missing")

    out = ROOT / slug / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")

    base = (cfg.get("preview_base_url") or "").rstrip("/")
    print(f"Built {out.relative_to(ROOT)}")
    if base:
        print(f"Preview URL after push: {base}/{slug}/")
    for w in warnings:
        print("Warning:", w)
    guesses = d.get("guesses", [])
    if guesses:
        print("Check these before sending (not taken from the listing):")
        for g in guesses:
            print("  -", g)


if __name__ == "__main__":
    main()
