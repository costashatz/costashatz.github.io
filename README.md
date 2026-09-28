# costashatz.github.io

Personal site of Konstantinos Chatzilygeroudis: <https://costashatz.github.io>

## What's here

Plain, static HTML/CSS — no build step needed to view it, just open a file or
serve the folder. GitHub Pages serves it directly from `master`.

Pages:

| Page | Purpose |
|---|---|
| `index.html` | Home / profile |
| `research.html` | Research overview |
| `publications.html` | Full publication list (generated, see below) |
| `contact.html` | Contact details |

All four share one theme defined in [`assets/css/main.css`](assets/css/main.css):
Inter typeface, an indigo accent, and a light/dark toggle (light by default,
persisted in `localStorage`; see `assets/js/theme.js`). The only external
dependency is the Inter font from Google Fonts — no JS framework, no
Bootstrap, no build tool.

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
explicitly on a different machine. `ref.bib` alone doesn't carry a `code=`/
`video=` link, a short badge label, or (for a handful of pre-2022 papers) a
url — those are curated directly in `build_pub_data.py` (`BADGE`,
`URL_OVERRIDE`) or, for `code`/`video`, read back from the *previous*
`tools/pubs_final.json` by BibTeX key, so a rerun never loses them. Add a new
paper's badge to `BADGE` if the auto-derived one (a parenthesised acronym
pulled from the venue string) looks bad.

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
