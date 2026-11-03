# Previews

One-page preview websites for prospects who asked to see one. Every site is
plain HTML, CSS and JavaScript: no frameworks, nothing to install, nothing to
compile. Each preview is published by GitHub Pages at:

    https://developerdadd.github.io/previews/<slug>/

## How it's organized

| Folder | What's in it | Published? |
| --- | --- | --- |
| `_content/<slug>.json` | The business details for one preview | No |
| `_template/` | The page every preview is built from: `index.html`, `styles.css`, `script.js` | No |
| `_tools/build.js` | Turns a JSON file into a site (Node, no packages needed) | No |
| `_tools/config.json` | Your agency name and the preview base URL | No |
| `<slug>/` | The built site: `index.html`, `styles.css`, `script.js` | Yes |

Folders that start with `_` are never published, so only built pages go live.
Every page carries a "this is a preview" bar and a `noindex` tag, so search
engines leave it alone.

Every site has one call to action: calling the business. There are no forms,
no online booking and no embedded widgets. The build stops if a page has a
form or invites people to book online.

## Build one by hand

    node _tools/build.js <slug>

It reads `_content/<slug>.json`, writes the three files into `<slug>/`, and lists anything
that was guessed rather than taken from the listing. Then commit and push.

## Remove a preview

Delete `_content/<slug>.json` and the `<slug>/` folder, then commit and push.
Clear out previews that haven't turned into clients after 30 days.

## When a prospect signs

Copy their `<slug>/` folder into its own repository, remove the preview bar and the
`noindex` tag, and point their domain at it.

## Layouts

Pick one per business in the JSON `layout` field. Leaving it out means `classic`.

- `classic`: the original one-page template in `_template/`.
- `components`: built from the pieces in `components/` (navigation, call-now button,
  grid pattern, hero-408, sbs-2525, steps-889, reviews-1088, cs-footer-272), restyled
  to the preview rules. Lives in `_template/components/`. Extra optional fields:
  - `stats`: up to 2 `{"value", "label"}` boxes over the hero photo (facts only)
  - `about`: `{"heading", "paragraphs", "list_heading", "list", "photo": {"url", "alt"}}`
  - `steps`: `{"heading", "intro", "items": [{"name", "detail"}]}`, shown as "New Patients"
  - `reviews_heading`, `footer_blurb`
  - `colors.accent`: an optional brighter brand color for step numbers, stripes and
    bullets (large or decorative only, so it needs just 3:1 on white)

  The nav links to Services, plus About and New Patients when those sections have content.

## Colors

Pick one per business in the JSON `palette` field:
`navy`, `red`, `green`, `teal`, `slate`, `plum`.

Or match the business's own branding with a `colors` block instead:

    "colors": {"paint": "#7A3B12", "deep": "#4E250B", "sign": "#F3D9A4"}

`paint` is the main brand color (header, hero, buttons), `deep` a darker shade
(footer, call-button text), `sign` the highlight (stars, stripes, call button).
The build refuses colors that would make text hard to read.
