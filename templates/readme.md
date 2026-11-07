# Templates

Self-contained website templates. Each is a single HTML file with its CSS and JavaScript inline.

## flooring-template.html

A dark navy and gold one-page site for a hardwood flooring business. Sections: header, hero, main services, complete services, stats, why refinish, credentials, gallery with lightbox, process steps, call to action and footer.

To customize it:

1. Replace `Your Flooring Co.`, `Your City`, `Your County`, the town names and `(555) 555-0123` / `+15555550123`.
2. Change the brand colors in the `:root` block at the top of the `<style>` tag.
3. Swap each image placeholder (`<div class="img" data-label="...">`) for `<img class="img" src="photo.jpg" alt="...">`.

## painting-template.html

A dark green and orange one-page site for a painting contractor. Sections: top bar, header with a services dropdown, hero with an estimate form, about, services, why choose us, process steps, FAQ accordion, contact info strip and footer.

To customize it:

1. Replace `Your Painting Co.`, `Your City`, `Your County`, the town names, `(555) 555-0123` / `+15555550123` and `hello@yourcompany.com`.
2. Change the brand colors and fonts in the `:root` block at the top of the `<style>` tag.
3. Swap each image placeholder (`<div class="img" data-label="...">`) for `<img class="img" src="photo.jpg" alt="...">`. For the hero and service cards, add `style="background-image: url('photo.jpg')"` to the `.hero-bg` / `.svc-bg` element.
4. The estimate form has no backend: set its `action` to your form handler and remove the demo submit handler in the script.

## roofing-template.html

A dark navy and red one-page site for a roofing contractor. Sections: top bar, header with a services dropdown, centered hero with a large photo, services, why choose us, who we are with counting stats, a tabbed "why choose us" panel, sample testimonials, call to action, contact info strip, footer with a newsletter signup, and a floating call bubble.

To customize it:

1. Replace `Your Roofing Co.`, `Your City`, `Your County`, `Your Region`, the town names, `(555) 555-0123` / `+15555550123` and `hello@yourcompany.com`.
2. Change the brand colors and fonts in the `:root` block at the top of the `<style>` tag.
3. Swap each image placeholder (`<div class="img" data-label="...">`) for `<img class="img" src="photo.jpg" alt="...">`.
4. Replace the sample testimonials with real reviews.
5. The newsletter form has no backend: set its `action` to your email service and remove the demo submit handler in the script.

## property-services-template.html

A forest green, cream and lime one-page site for a local property services company (tree removal, dumpster rentals, excavation, cleanup). Uses a serif heading font. Sections: transparent header over a full-height hero, numbered services list, full-width equipment photo, excavation checklist, dumpster rentals with stats, photo collage with a "Proudly local" badge, about the owner, seasonal golf course maintenance, sample reviews, closing call to action and footer.

To customize it:

1. Replace `Your Company Co.`, `Your City`, `Your County`, the town names, `Owner Name`, `(555) 555-0123` / `+15555550123` and `hello@yourcompany.com`.
2. Change the brand colors and fonts in the `:root` block at the top of the `<style>` tag.
3. Swap each image placeholder (`<div class="img" data-label="...">`) for `<img class="img" src="photo.jpg" alt="...">`. For the hero, add `style="background-image: url('photo.jpg')"` to `.hero-bg`.
4. Replace the sample reviews with real ones, and drop the golf course section if it doesn't apply.

## concrete-template.html

A black, construction-yellow and cream one-page site for a concrete contractor, with heavy condensed headings. Sections: header with a yellow "discuss your project" block, full-height hero, scrolling yellow services ticker, numbered service cards, meet the owner, a reviews carousel, a recent-projects photo grid with lightbox, contact list and footer.

To customize it:

1. Replace `Your Company Co.`, `Your City`, `Owner Name`, `Lic. #0000000`, `(555) 555-0123` / `+15555550123` and `hello@yourcompany.com`. The round badge logo uses the initials `YCC`.
2. Change the brand colors and fonts in the `:root` block at the top of the `<style>` tag.
3. Swap each image placeholder (`<div class="img" data-label="...">`) for `<img class="img" src="photo.jpg" alt="...">`. For the hero, add `style="background-image: url('photo.jpg')"` to `.hero-bg`.
4. Replace the sample reviews with real ones. Add more `.rev-slide` blocks and the counter updates automatically.
