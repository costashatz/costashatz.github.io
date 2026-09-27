# costashatz.github.io

Personal site of Konstantinos Chatzilygeroudis: <https://costashatz.github.io>

## What's here

Plain, static HTML/CSS — no build step needed to view it, just open a file or
serve the folder. GitHub Pages serves it directly from `master`.

Pages:

| Page | Status |
|---|---|
| `index.html` | Home / profile |
| `research.html` | Research overview |
| `publications.html` | Full publication list (generated, see below) |
| `contact.html` | Contact details |
| `deadlines.html` | Personal conference-deadline tracker, not linked from the nav |
| `videos.html` | Talks/demos archive, not linked from the nav (legacy) |

`index.html`, `research.html`, `publications.html` and `contact.html` share
one theme ("Ink & Slate": dark, Inter typeface, indigo accent) defined in
[`assets/css/main.css`](assets/css/main.css). The only external dependency is
the Inter font from Google Fonts; there's no JS framework, no Bootstrap, no
build tool.

`deadlines.html` and `videos.html` still run on the old Bootstrap 3 /
["Initio"](https://github.com/pozh/Initio/) template
(`assets/css/styles.css`, `assets/css/academicons.css`, `assets/less/`,
`assets/js/`) and haven't been migrated to the new theme yet — see
[Attributions](#attributions).

## Regenerating `publications.html` (and the homepage's publication list)

`publications.html`, plus the "Recent preprint" and "Selected publications"
cards on `index.html`, are generated from **[`tools/pubs_final.json`](tools/pubs_final.json)**,
not hand-edited. That file is itself built from the canonical publication
list kept in the [`curriculum_vitae`](https://github.com/costashatz/curriculum_vitae)
repo (`publication-list/ref.bib` and `publication-list/pub.tex`, which give
the per-section ordering).

To refresh after adding/editing a paper there:

```bash
cd costashatz.github.io
python3 tools/build_pub_data.py --cv-repo /path/to/curriculum_vitae   # rewrites tools/pubs_final.json
python3 tools/page_index.py                                          # rewrites index.html
python3 tools/page_publications.py                                   # rewrites publications.html
```

`--cv-repo` defaults to this machine's usual checkout path; pass it
explicitly on a different machine. `build_pub_data.py` also tries to carry
over any `code=`/`video=` links it finds for a matching title in the
*current* `publications.html`, so those aren't lost across regenerations —
recheck them after big rewrites.

Active preprints (not yet in `ref.bib`, since they're unpublished) are kept
directly in `tools/build_site.py`'s `PREPRINTS` list, newest first — the
homepage always features `PREPRINTS[0]`, and `publications.html` lists all of
them. Move an entry out once it has a real venue and add it to `ref.bib`
instead.

`tools/page_research.py` and `tools/page_contact.py` regenerate
`research.html` and `contact.html` respectively, but those pages are mostly
hand-written prose, not data-driven — edit the Python (the HTML is an
f-string) directly and rerun.

`tools/build_site.py` holds the shared page shell: the `<head>`, nav, and
footer used by every generated page. Edit it (e.g. to add a nav item or
footer link) and rerun all four `page_*.py` scripts to propagate the change.

`deadlines.html` and `videos.html` are not part of this generator and are
edited by hand.

## Attributions

#### Initio Template *(deadlines.html and videos.html only)*
- Created by Sergey Pozhilov
- License: Creative Commons Attribution 3.0
- <https://github.com/pozh/Initio/>

#### Academicons *(deadlines.html and videos.html only)*
- Version 1.5, 2015
- Created by James Walsh
- License: SIL OFL 1.1/MIT
- <https://github.com/jpswalsh/academicons>
- <http://jpswalsh.github.io/academicons>
