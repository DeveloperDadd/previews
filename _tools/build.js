#!/usr/bin/env node
/*
 * Build a one-page preview site from _content/<slug>.json.
 *
 * Usage:
 *   node _tools/build.js <slug>
 *
 * Reads   _content/<slug>.json   (the business details)
 *         _tools/config.json     (your agency name, preview base URL)
 *         _template/index.html, styles.css, script.js
 * Writes  <slug>/index.html, <slug>/styles.css, <slug>/script.js
 *
 * Prints any problems, the preview URL, and every "guesses" entry so you can
 * check it before sending. Exits with status 1 if a required field is missing.
 * Uses only Node's built-in modules: no npm install needed.
 */
'use strict';
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

// paint = brand color (header, hero, footer), deep = darker shade,
// sign = highlight for stars, stripes and the call button.
const PALETTES = {
  navy:  { paint: '#1D3557', deep: '#13243B', sign: '#F4C542' },
  red:   { paint: '#9E2A22', deep: '#6B1C17', sign: '#F6DFA0' },
  green: { paint: '#2D5A3D', deep: '#1D3D29', sign: '#E9D57A' },
  teal:  { paint: '#135E63', deep: '#0B4246', sign: '#F2D06B' },
  slate: { paint: '#36454F', deep: '#222D34', sign: '#F29A3A' },
  plum:  { paint: '#5B2A4A', deep: '#3D1B32', sign: '#F1C6A8' },
};
const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
// Page layouts. "classic" is the original one-page template; "components" is built
// from the pieces in components/ (see _template/components/). Pick one per business
// with the JSON "layout" field; leaving it out means classic.
const LAYOUTS = {
  classic: '_template',
  components: path.join('_template', 'components'),
};
const REQUIRED = ['slug', 'name', 'category', 'city', 'headline', 'intro', 'phone',
  'listing_url', 'services'];
const MIST = '#F1F3F2';

// The only call to action on these sites is a phone call. Fields from the
// old quote-form template are ignored, and booking language stops the build.
const RETIRED_FIELDS = ['quote_label', 'contact_heading', 'contact_intro', 'form_prompt', 'submit_label'];
const BOOKING_BLOCK = /\b(book(ing)? online|online (booking|scheduling|appointments?)|schedul(e|ing) online|book now|booking (link|page|widget|system)|request (an )?appointment online)\b/i;
const BOOKING_CHECK = /\b(book|request|schedule) (an |your )?appointment\b/i;

const esc = (value) => String(value)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;').replace(/'/g, '&#x27;');

const isBlank = (v) => v === undefined || v === null || v === '' || v === false ||
  (Array.isArray(v) && v.length === 0);

function telLink(phone) {
  let digits = phone.replace(/\D/g, '');
  if (digits.length === 10) digits = '1' + digits;
  return '+' + digits;
}

function stars(rating) {
  const full = Math.max(0, Math.min(5, Math.round(Number(rating))));
  return '★'.repeat(full) + '☆'.repeat(5 - full);
}

function luminance(hex) {
  const lin = [1, 3, 5].map((i) => {
    const c = parseInt(hex.slice(i, i + 2), 16) / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2];
}

function contrast(a, b) {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

// Custom colors must stay readable everywhere the template uses them.
function checkColors(colors, errors, warnings) {
  const bad = ['paint', 'deep', 'sign'].filter((key) => !/^#[0-9A-Fa-f]{6}$/.test(String(colors[key] || '')));
  for (const key of bad) errors.push(`colors.${key} must be a hex color like #1D3557`);
  if (bad.length) return;
  const { paint: p, deep: dp, sign: s } = colors;
  for (const [label, a, b, need] of [
    ['white text on paint (hero, buttons)', '#FFFFFF', p, 4.5],
    ['white text on deep (footer)', '#FFFFFF', dp, 4.5],
    ['deep text on sign (call button)', dp, s, 4.5],
  ]) {
    const ratio = contrast(a, b);
    if (ratio < need) errors.push(`${label} contrast is ${ratio.toFixed(1)}:1; needs ${need}:1`);
  }
  // Optional accent: a brighter brand color, used only for large numbers, stripes and bullets.
  if (colors.accent !== undefined) {
    if (!/^#[0-9A-Fa-f]{6}$/.test(String(colors.accent))) {
      errors.push('colors.accent must be a hex color like #007DFA');
    } else if (contrast(colors.accent, '#FFFFFF') < 3.0) {
      errors.push(`accent on white contrast is ${contrast(colors.accent, '#FFFFFF').toFixed(1)}:1; needs 3:1 for large numbers`);
    }
  }
  for (const [label, a, b, need] of [
    ['sign on paint (stars, stripes)', s, p, 3.0],
    ['paint links on grey sections', p, MIST, 4.5],
  ]) {
    const ratio = contrast(a, b);
    if (ratio < need) warnings.push(`${label} contrast is ${ratio.toFixed(1)}:1; aim for ${need}:1`);
  }
}

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));

function fill(template, values, file) {
  const out = template.replace(/\{\{(\w+)\}\}/g, (match, key) => {
    if (!(key in values)) throw new Error(`${file} has a slot with no value: ${match}`);
    return values[key];
  });
  return out;
}

// Extra slots for the "components" layout: nav links, the hero photo with credential
// boxes (hero-408), about (sbs-2525), new-patient steps (steps-889), reviews
// (reviews-1088) and the footer (cs-footer-1292), which carries the hours and location.
// Sections without content are left out.
function componentValues(d, ctx) {
  const { photos, reviews, listing, sample, address, hours, warnings } = ctx;
  const about = d.about && !isBlank(d.about.paragraphs) ? d.about : null;
  const steps = d.steps && !isBlank(d.steps.items) ? d.steps : null;
  const stats = (d.stats || []).slice(0, 2);
  if ((d.stats || []).length > 2) warnings.push('more than 2 stats given; showing the first 2');

  // Page order after Services: about, new patients, reviews. Backgrounds alternate.
  // Hours and location live in the footer.
  const order = [...(about ? ['about'] : []), ...(steps ? ['steps'] : []), ...(reviews.length ? ['reviews'] : [])];
  const alt = Object.fromEntries(order.map((key, i) => [key, i % 2 === 0 ? ' alt' : '']));

  const links = [
    ['services', 'Services'],
    ...(about ? [['about', 'About']] : []),
    ...(steps ? [['new-patients', 'New Patients']] : []),
  ];
  const navHtml = links.map(([id, label]) =>
    `          <li class="cs-li"><a class="cs-li-link" href="#${id}">${label}</a></li>`).join('\n');
  const footerLinks = [...links, ...(reviews.length ? [['reviews', 'Reviews']] : [])];
  const footerLinksHtml = footerLinks.map(([id, label]) =>
    `      <li class="cs-nav-li"><a class="cs-nav-link" href="#${id}">${label}</a></li>`).join('\n');

  // Footer columns: hours (today's row is marked by script.js) and location with directions.
  const hourDays = DAYS.filter((day) => day in hours);
  const footerHoursHtml = hourDays.length
    ? '    <div class="cs-hours">\n      <span class="cs-header">Hours</span>\n      <dl class="cs-hours-list">\n' +
      hourDays.map((day) =>
        `        <div class="cs-hours-row" data-day="${day}"><dt>${day}</dt><dd>${esc(hours[day])}</dd></div>`).join('\n') +
      '\n      </dl>\n    </div>'
    : '';
  const footerLocationHtml = address
    ? '    <ul class="cs-nav cs-location">\n      <li class="cs-nav-li"><span class="cs-header">Location</span></li>\n' +
      `      <li class="cs-nav-li"><address>${esc(address)}</address></li>\n` +
      `      <li class="cs-nav-li"><a class="cs-nav-link" href="${listing}">Get directions</a></li>\n    </ul>`
    : '';

  // Hero media: first photo behind up to two credential boxes.
  let heroMediaHtml = '';
  if (photos.length || stats.length) {
    const p = photos[0];
    const picture = p
      ? `      <picture class="cs-background"><img src="${esc(p.url)}" alt="${esc(p.alt || '')}" ` +
        'referrerpolicy="no-referrer" width="600" height="900"></picture>\n'
      : '';
    const boxes = stats.map((s) =>
      `        <div class="cs-stat-box"><span class="cs-stat">${esc(s.value)}</span>` +
      `<span class="cs-desc">${esc(s.label)}</span></div>`).join('\n');
    heroMediaHtml =
      `    <div class="cs-stat-group${p ? '' : ' no-photo'}">\n${picture}` +
      (boxes ? `      <div class="cs-stats">\n${boxes}\n      </div>\n` : '') + '    </div>';
  }

  let aboutHtml = '';
  if (about) {
    const photo = about.photo && String(about.photo.url || '').startsWith('https://') ? about.photo : null;
    if (about.photo && !photo) warnings.push('about.photo needs an https:// URL; left out');
    const picture = photo
      ? `      <picture class="cs-picture"><img src="${esc(photo.url)}" alt="${esc(photo.alt || '')}" ` +
        'loading="lazy" referrerpolicy="no-referrer" width="800" height="600"></picture>\n'
      : '';
    const paras = about.paragraphs.map((t) => `        <p class="cs-text">${esc(t)}</p>`).join('\n');
    const list = isBlank(about.list) ? '' :
      (about.list_heading ? `        <h3 class="cs-h3">${esc(about.list_heading)}</h3>\n` : '') +
      '        <ul class="cs-card-group">\n' +
      about.list.map((t) => `          <li class="cs-item">${esc(t)}</li>`).join('\n') + '\n        </ul>\n';
    aboutHtml =
      `  <section class="section${alt.about}" id="about">\n    <div id="sbs-2525">\n` +
      `    <div class="cs-container wrap">\n${picture}      <div class="cs-content">\n` +
      `        <h2 class="cs-title">${esc(about.heading || 'About us')}</h2>\n${paras}\n${list}` +
      '      </div>\n    </div>\n    </div>\n  </section>';
  }

  let stepsHtml = '';
  if (steps) {
    const items = steps.items.map((s, i) =>
      '        <li class="cs-item">' +
      `<span class="cs-number" aria-hidden="true">${i + 1}</span>` +
      `<h3 class="cs-h3">${esc(s.name)}</h3>` +
      (s.detail ? `<p class="cs-item-p">${esc(s.detail)}</p>` : '') + '</li>').join('\n');
    stepsHtml =
      `  <section class="section${alt.steps}" id="new-patients">\n    <div id="steps-889">\n    <div class="wrap">\n` +
      `      <h2 class="cs-title">${esc(steps.heading || 'Your first visit')}</h2>\n` +
      (steps.intro ? `      <p class="section-intro">${esc(steps.intro)}</p>\n` : '') +
      `      <ol class="cs-card-group">\n${items}\n      </ol>\n    </div>\n    </div>\n  </section>`;
  }

  let reviewsHtml = '';
  if (reviews.length) {
    const items = reviews.map((r) => {
      const rating = parseInt(r.rating ?? 5, 10);
      const who = sample ? 'Sample review' : esc(r.author || 'Customer');
      return '        <li class="cs-item">' +
        `<span class="stars" aria-label="${rating} out of 5 stars">${stars(rating)}</span>` +
        `<p class="cs-item-text">${esc(r.text)}</p>` +
        `<div class="cs-flex"><span class="cs-name">${who}</span><span class="cs-desc">Google review</span></div></li>`;
    }).join('\n');
    const more = d.review_count
      ? `      <a class="more-link" href="${listing}">Read all ${parseInt(d.review_count, 10).toLocaleString('en-US')} reviews on Google</a>\n`
      : '';
    reviewsHtml =
      `  <section class="section${alt.reviews}" id="reviews">\n    <div id="reviews-1088">\n    <div class="wrap">\n` +
      `      <h2 class="cs-title">${esc(d.reviews_heading || 'What customers say')}</h2>\n` +
      `      <ul class="cs-card-group">\n${items}\n      </ul>\n${more}    </div>\n    </div>\n  </section>`;
  }

  return {
    nav_html: navHtml,
    hero_class: heroMediaHtml ? '' : ' no-media',
    hero_media_html: heroMediaHtml,
    about_html: aboutHtml,
    steps_html: stepsHtml,
    c_reviews_html: reviewsHtml,
    footer_links_html: footerLinksHtml,
    c_footer_hours_html: footerHoursHtml,
    c_footer_location_html: footerLocationHtml,
    footer_blurb: esc(d.footer_blurb || `${d.category} in ${d.city}.`),
  };
}

function fail(lines) {
  console.log('Build stopped:');
  for (const line of lines) console.log('  -', line);
  process.exit(1);
}

function main() {
  if (process.argv.length !== 3) fail(['Usage: node _tools/build.js <slug>']);
  const slug = process.argv[2].trim().replace(/^\/+|\/+$/g, '');
  const src = path.join(ROOT, '_content', `${slug}.json`);
  if (!fs.existsSync(src)) fail([`Not found: ${src}`]);

  const d = readJson(src);
  const cfg = readJson(path.join(ROOT, '_tools', 'config.json'));
  const errors = [];
  const warnings = [];

  for (const key of REQUIRED) {
    if (isBlank(d[key])) errors.push(`missing required field: ${key}`);
  }
  if (d.slug && d.slug !== slug) errors.push(`slug in file (${d.slug}) doesn't match file name (${slug})`);
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(slug)) errors.push('slug must be lowercase letters, numbers and single hyphens');
  if (d.colors) {
    checkColors(d.colors, errors, warnings);
  } else if (!d.palette) {
    errors.push('missing required field: palette (or a custom colors block)');
  } else if (!(d.palette in PALETTES)) {
    errors.push(`palette must be one of: ${Object.keys(PALETTES).join(', ')}`);
  }
  if (d.phone && ![10, 11].includes(d.phone.replace(/\D/g, '').length)) {
    errors.push(`phone doesn't look like a US number: ${d.phone}`);
  }
  const layout = d.layout || 'classic';
  if (!(layout in LAYOUTS)) errors.push(`layout must be one of: ${Object.keys(LAYOUTS).join(', ')}`);
  if (errors.length) fail(errors);
  const retired = RETIRED_FIELDS.filter((key) => key in d);
  if (retired.length) warnings.push(`ignored ${retired.join(', ')}: sites are call-only now (use call_heading and call_intro)`);

  const name = d.name.trim();
  const phone = d.phone.trim();
  const pal = d.colors ? d.colors : PALETTES[d.palette];
  const sample = Boolean(d.sample);
  const listing = esc(d.listing_url);

  if (d.headline.length > 90) warnings.push(`headline is ${d.headline.length} characters; aim for under 90`);
  const services = d.services;
  if (services.length < 3 || services.length > 8) warnings.push(`${services.length} services; 3 to 8 reads best`);

  // Photos: the first is the hero image, the next up to 3 form a gallery.
  const allPhotos = d.photos || [];
  const photos = allPhotos.filter((p) => String(p.url || '').startsWith('https://'));
  if (photos.length !== allPhotos.length) warnings.push('dropped photos without an https:// URL');

  // Name size: long names step down so they stay on two or three lines.
  // Without a photo the name has the full width, so it gets one size up.
  const sizes = ['', 'medium', 'long'];
  let step = name.length <= 16 ? 0 : name.length <= 28 ? 1 : 2;
  if (!photos.length) step = Math.max(0, step - 1);
  const nameSize = sizes[step];

  // Sections after "What we do" alternate grey, white, grey... so neighbours never match.
  let reviews = d.reviews || [];
  const order = [...(photos.length >= 3 ? ['gallery'] : []), ...(reviews.length ? ['reviews'] : []), 'area'];
  const alt = Object.fromEntries(order.map((key, i) => [key, i % 2 === 0 ? ' alt' : '']));

  // Rating line
  let ratingHtml = '';
  if (d.rating && d.review_count) {
    const count = parseInt(d.review_count, 10);
    ratingHtml =
      `<p class="rating"><span class="stars" aria-hidden="true">${stars(d.rating)}</span>` +
      `<span><strong>${Number(d.rating).toFixed(1)}</strong> from ` +
      `<a href="${listing}">${count.toLocaleString('en-US')} Google review${count !== 1 ? 's' : ''}</a></span></p>`;
  }

  let heroPhotoHtml = '';
  let heroGridClass = '';
  let galleryHtml = '';
  if (photos.length) {
    const p = photos[0];
    heroGridClass = ' has-photo';
    heroPhotoHtml =
      `<div class="hero-photo"><img src="${esc(p.url)}" alt="${esc(p.alt || '')}" ` +
      'referrerpolicy="no-referrer" width="1200" height="900"></div>';
  }
  if (photos.length >= 3) {
    const imgs = photos.slice(1, 4).map((p) =>
      `        <img src="${esc(p.url)}" alt="${esc(p.alt || '')}" loading="lazy" ` +
      'referrerpolicy="no-referrer" width="800" height="600">').join('\n');
    galleryHtml =
      `  <section class="section${alt.gallery}" id="work">\n    <div class="wrap">\n` +
      '      <h2>Recent work</h2>\n      <p class="section-intro">' +
      `${esc(d.gallery_intro || 'A few recent jobs.')}</p>\n` +
      `      <div class="gallery">\n${imgs}\n      </div>\n    </div>\n  </section>`;
  }

  const servicesHtml = services.map((s) =>
    `        <li><h3>${esc(s.name)}</h3>` + (s.detail ? `<p>${esc(s.detail)}</p>` : '') + '</li>').join('\n');

  // Reviews: real reviews only, up to 3.
  if (reviews.length > 3) {
    warnings.push(`${reviews.length} reviews given; showing the first 3`);
    reviews = reviews.slice(0, 3);
  }
  let reviewsHtml = '';
  if (reviews.length) {
    const items = reviews.map((r) => {
      const who = sample ? 'Sample review' : `${esc(r.author || 'Customer')} on Google`;
      if ((r.text || '').length > 320) warnings.push(`review by ${r.author} is long; trim it to its best 1-3 sentences`);
      const rating = parseInt(r.rating ?? 5, 10);
      return '        <figure class="review">' +
        `<span class="stars" aria-label="${rating} out of 5 stars">${stars(rating)}</span>` +
        `<blockquote><p>${esc(r.text)}</p></blockquote>` +
        `<figcaption>${who}</figcaption></figure>`;
    });
    const more = d.review_count
      ? `      <a class="more-link" href="${listing}">Read all ${parseInt(d.review_count, 10).toLocaleString('en-US')} reviews on Google</a>\n`
      : '';
    reviewsHtml =
      `  <section class="section${alt.reviews}" id="reviews">\n    <div class="wrap">\n` +
      '      <h2>What customers say</h2>\n' +
      '      <div class="reviews">\n' + items.join('\n') + '\n      </div>\n' +
      more + '    </div>\n  </section>';
  } else {
    warnings.push('no reviews; the reviews section is left out');
  }

  // Area / location column
  const area = d.service_area || [];
  const address = (d.address || '').trim();
  const parts = [];
  if (area.length) {
    const towns = area.map((t) => `          <li>${esc(t)}</li>`).join('\n');
    const areaIntro = d.area_intro || `We serve ${d.city} and nearby towns, including:`;
    parts.push(`        <h2>Where we work</h2>\n        <p class="section-intro">${esc(areaIntro)}</p>\n` +
      `        <ul class="towns">\n${towns}\n        </ul>`);
  }
  if (address) {
    const open = area.length ? 'h3 class="sub"' : 'h2';
    const close = area.length ? 'h3' : 'h2';
    const heading = area.length ? 'Visit us' : 'Where to find us';
    parts.push(`        <${open}>${heading}</${close}>\n` +
      `        <address class="address">${esc(address)}</address>\n` +
      `        <a class="more-link" style="margin-top:0" href="${listing}">Get directions</a>`);
  }
  if (!parts.length) warnings.push('no service_area or address; the location column is empty');
  const areaHtml = '      <div>\n' + parts.join('\n') + '\n      </div>';

  // Hours
  const hours = d.hours || {};
  let hoursHtml = '';
  if (Object.keys(hours).length) {
    const missing = DAYS.filter((day) => !(day in hours));
    if (missing.length) warnings.push(`hours missing for: ${missing.join(', ')}`);
    const rows = DAYS.filter((day) => day in hours).map((day) =>
      `          <tr data-day="${day}"><th scope="row">${day}</th><td>${esc(hours[day])}</td></tr>`).join('\n');
    hoursHtml = `      <div>\n        <h2>Hours</h2>\n        <table class="hours">\n${rows}\n        </table>\n      </div>`;
  } else {
    warnings.push('no hours; the hours table is left out');
  }

  // Preview notice and credit
  const agency = (cfg.agency_name || '').trim();
  const agencyUrl = (cfg.agency_url || '').trim();
  let note = sample
    ? 'Sample preview. The business, reviews and details on this page are made up.'
    : `This is a preview of a new website for ${esc(name)}. It isn't live yet.`;
  let creditHtml = '';
  if (agency) {
    const who = agencyUrl ? `<a href="${esc(agencyUrl)}">${esc(agency)}</a>` : esc(agency);
    note += ` Made by ${who}.`;
    creditHtml = `<p>Website by ${who}</p>`;
  }

  const values = {
    title: esc(`${name} | ${d.category} in ${d.city}`),
    headline: esc(d.headline),
    paint: pal.paint, deep: pal.deep, sign: pal.sign, accent: pal.accent || pal.paint,
    preview_note: note,
    name: esc(name),
    name_size: nameSize,
    tel: telLink(phone),
    phone: esc(phone),
    hero_grid_class: heroGridClass,
    rating_html: ratingHtml,
    hero_photo_html: heroPhotoHtml,
    intro: esc(d.intro),
    services_html: servicesHtml,
    gallery_html: galleryHtml,
    reviews_html: reviewsHtml,
    area_alt: alt.area,
    area_html: areaHtml,
    hours_html: hoursHtml,
    call_heading: esc(d.call_heading || 'Give us a call'),
    call_intro: esc(d.call_intro || 'Tell us what you need and when you need it.'),
    footer_address_html: address ? `<p>${esc(address)}</p>` : '',
    year: String(new Date().getFullYear()),
    credit_html: creditHtml,
  };

  if (layout === 'components') {
    Object.assign(values, componentValues(d, { photos, reviews, listing, sample, address, hours, warnings }));
  }

  const tpl = (file) => fs.readFileSync(path.join(ROOT, LAYOUTS[layout], file), 'utf8');
  const css = fill(tpl('styles.css'), values, 'styles.css');
  const js = tpl('script.js');
  // Stamps styles.css and script.js links so a rebuilt page never pairs with a cached old stylesheet.
  values.asset_version = crypto.createHash('sha1').update(css).update(js).digest('hex').slice(0, 8);
  const files = {
    'index.html': fill(tpl('index.html'), values, 'index.html'),
    'styles.css': css,
    'script.js': js,
  };
  if (!files['index.html'].includes('name="robots" content="noindex')) fail(['Safety check failed: noindex tag missing']);
  if (!files['index.html'].includes('class="preview-bar"')) fail(['Safety check failed: preview notice missing']);

  // Call-only checks: no forms or embedded widgets, no invitations to book online.
  const page = files['index.html'];
  if (/<(form|input|textarea|select|iframe)\b/i.test(page)) {
    fail(['Call-only check failed: the page contains a form or embedded widget']);
  }
  const visible = page.replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
  const blocked = visible.match(BOOKING_BLOCK);
  if (blocked) fail([`Call-only check failed: "${blocked[0]}" invites online booking. Reword it to point to calling.`]);
  const flagged = visible.match(BOOKING_CHECK);
  if (flagged) warnings.push(`"${flagged[0]}" appears on the page; make sure it tells people to call, not book online`);

  const outDir = path.join(ROOT, slug);
  fs.mkdirSync(outDir, { recursive: true });
  for (const [file, content] of Object.entries(files)) fs.writeFileSync(path.join(outDir, file), content);

  console.log(`Built ${slug}/ (index.html, styles.css, script.js)`);
  const base = (cfg.preview_base_url || '').replace(/\/+$/, '');
  if (base) console.log(`Preview URL after push: ${base}/${slug}/`);
  for (const w of warnings) console.log('Warning:', w);
  const guesses = d.guesses || [];
  if (guesses.length) {
    console.log('Check these before sending (not taken from the listing):');
    for (const g of guesses) console.log('  -', g);
  }
}

main();
