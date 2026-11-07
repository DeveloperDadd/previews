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
