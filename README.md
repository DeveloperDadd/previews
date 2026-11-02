# Previews

One-page preview websites for prospects who asked to see one. Each preview is
published by GitHub Pages at:

    https://developerdadd.github.io/previews/<slug>/

## How it's organized

| Folder | What's in it | Published? |
| --- | --- | --- |
| `_content/<slug>.json` | The business details for one preview | No |
| `_template/index.html` | The page design every preview is built from | No |
| `_tools/build.py` | Turns a JSON file into a page | No |
| `_tools/config.json` | Your agency name and the preview base URL | No |
| `<slug>/index.html` | The built page | Yes |

Folders that start with `_` are never published, so only built pages go live.
Every page carries a "this is a preview" bar and a `noindex` tag, so search
engines leave it alone.

## Build one by hand

    python3 _tools/build.py <slug>

It reads `_content/<slug>.json`, writes `<slug>/index.html`, and lists anything
that was guessed rather than taken from the listing. Then commit and push.

## Remove a preview

Delete `_content/<slug>.json` and the `<slug>/` folder, then commit and push.
Clear out previews that haven't turned into clients after 30 days.

## When a prospect signs

Copy their page into its own repository, remove the preview bar and the
`noindex` tag, swap the form for a real one, and point their domain at it.

## Colors

Pick one per business in the JSON `palette` field:
`navy`, `red`, `green`, `teal`, `slate`, `plum`.

Or match the business's own branding with a `colors` block instead:

    "colors": {"paint": "#7A3B12", "deep": "#4E250B", "sign": "#F3D9A4"}

`paint` is the main brand color (header, hero, buttons), `deep` a darker shade
(footer, call-button text), `sign` the highlight (stars, stripes, call button).
The build refuses colors that would make text hard to read.
