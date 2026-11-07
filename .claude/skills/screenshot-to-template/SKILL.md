---
name: screenshot-to-template
description: Rebuild a website from a full-page screenshot as one self-contained HTML file (inline CSS and JS) in templates/, verify it, and open a pull request. Use when the user uploads a full-page screenshot of a website and asks for a template, site or page built from it.
---

# Screenshot to template

Turn a full-page website screenshot into a single self-contained HTML template in
`templates/`, verify it in a browser, then commit, push and open a pull request.

Use `templates/flooring-template.html` as the reference for structure, comments
and quality.

## 1. Study the screenshot

Go through it from top to bottom and note:
- every section, in order
- the color palette
- the fonts (serif or sans)
- spacing, buttons, cards, icons and badges
- the general mood

Most screenshots are phone-width captures. Build mobile-first, then lay the page
out well on desktop, using multi-column grids where they make sense.

## 2. Build ONE self-contained HTML file

- All CSS goes in a single `<style>` block in `<head>`. Don't create separate `.css` files.
- All JavaScript goes in a single `<script>` block at the end of `<body>`. Don't create separate `.js` files.
- Use plain HTML, CSS and vanilla JS only: no frameworks, no build step, no npm packages.
- Google Fonts is the only external resource allowed.
- Define brand colors and fonts as CSS custom properties in `:root` so the template is easy to re-brand.
- Keep the sections in the same order as the screenshot and match its look as closely as you can.

## 3. Placeholder content only

The screenshot is usually of a real company. **Never** copy its name, logo, phone
number, address, license numbers, reviews or wording. Use generic placeholders:

- "Your Company Co." (or "Your Roofing Co." and the like)
- "Your City, ST", "Your County"
- "Town One, Town Two, ..."
- (555) 555-0123, linked as `tel:+15555550123`
- `hello@yourcompany.com`
- "Lic. #0000000"

Rewrite all body text in your own words so it fits the industry.

## 4. Images

Don't hotlink stock photos. Use CSS-gradient placeholder blocks styled to suit
the industry, for example:

```html
<div class="img" data-label="Photo: kitchen remodel"></div>
```

Show the label on the block with `div.img::after { content: attr(data-label); }`.
At the top of the file, add an HTML comment explaining how to swap each block for
`<img class="img" src="..." alt="...">`.

## 5. JavaScript features

Include these where they fit the design:
- a mobile hamburger menu that updates `aria-expanded` and closes when a link is clicked
- a shadow on the sticky header once the page scrolls
- sections that fade in on scroll, using IntersectionObserver (`.reveal` → `.visible`)
- stat numbers that count up when they come into view
- a gallery lightbox that closes with the X, a click on the backdrop, or Esc
- the current year filled in automatically in the footer

Respect `prefers-reduced-motion`. The page must stay readable if JS fails: put
`class="no-js"` on `<body>`, remove it in JS, and add the rule
`.no-js .reveal { opacity: 1; transform: none; }`.

## 6. Accessibility basics

- Semantic landmarks: `header`, `nav`, `main`, `section`, `footer`
- Exactly one `h1`
- Alt text or `aria-label` where needed, and `aria-hidden="true"` on decorative SVGs
- Visible `:focus-visible` styles
- Readable color contrast
- Tap targets of at least 44px

## 7. File name and readme

- Save the page as `templates/<industry>-template.html`, for example
  `templates/roofing-template.html` or `templates/dental-template.html`.
- If that name already exists, append `-2`, `-3` and so on.
- Add a short entry to `templates/readme.md` saying what the template is and how
  to customize it: names and phone, `:root` colors, swapping images.

## 8. Verify before committing

Chromium and Playwright are pre-installed. Don't run `playwright install`.

Save this script in the scratchpad and run it with
`node check.js templates/<file>.html`:

```js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file://' + path.resolve(process.argv[2]);
  const browser = await chromium.launch();
  for (const width of [390, 1280]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => m.type() === 'error' && errors.push(m.text()));
    await page.goto(file);
    // Full-page screenshots don't scroll, so reveal everything first.
    await page.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('visible')));
    await page.waitForTimeout(800);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    console.log(width + 'px', 'overflow:', overflow, 'errors:', errors);
    await page.screenshot({ path: `shot-${width}.png`, fullPage: true });
  }
  await browser.close();
})();
```

Then check the results:
- Look at both screenshots next to the original.
- There should be no console errors. Font load failures caused by the network sandbox are fine.
- Overflow must be `0` at 390px.
- Fix any problems and run the script again.

Fonts may not load in the sandbox, so judge layout and color rather than exact typography.

## 9. Git and pull request

1. Check the working branch first. If its earlier pull request is already merged,
   restart it from the latest `main` before committing:
   `git fetch origin main && git checkout -B <branch> origin/main`
2. Commit with a clear message, e.g. "Add roofing website template".
3. Push to the working branch with `git push -u origin <branch>`.
4. Open a pull request into `main`. The body should summarize the sections and
   say that the content is placeholder.
5. **Do NOT merge unless the user asks.**

## 10. Reply to the user

Include:
- a short list of what's on the page
- the pull request link
- the GitHub Pages URL the page will have once merged:
  `https://developerdadd.github.io/previews/templates/<file-name>.html`
- a private preview link they can open on their phone right away, if publishing
  an Artifact is available (publish the HTML file itself)
