# -*- coding: utf-8 -*-
"""
Rebuild tools/pubs_final.json from the curriculum_vitae repo's ref.bib/pub.tex.

Run from the website repo root:
    python3 tools/build_pub_data.py --cv-repo /path/to/curriculum_vitae

Three things ref.bib alone doesn't give us, so they're kept here and carried
forward across regenerations by reading the *previous* tools/pubs_final.json:

  - `code=`/`video=` links (ref.bib has no such fields; these were originally
    recovered from the old bibtex_js-based publications.html, back when the
    site used that format).
  - A short "badge" label (e.g. "IROS", "IEEE Trans. Robotics") for entries
    whose full venue name is too long for the small badge on each pub-card.
    See BADGE below; add an entry there for any new paper whose auto-derived
    badge (an acronym pulled from parentheses in the venue string) looks bad.
  - A fallback `url` for the handful of older entries that have neither a
    `url=` nor a `doi=` field in ref.bib. See URL_OVERRIDE below; these come
    from the equivalent \\href{} in curriculum_vitae/cv_7.tex.

If you add a new paper to ref.bib, just rerun this script: existing entries
keep their curated badge/url/code/video (matched by BibTeX key), and the new
one gets a best-effort auto badge — check it and add it to BADGE if it's ugly.
"""
import re, json, argparse, os

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--cv-repo', default='/home/kchatzil/Workspaces/git/curriculum_vitae',
                 help="Path to the curriculum_vitae checkout (default: this machine's usual location).")
args = ap.parse_args()

BIB = os.path.join(args.cv_repo, 'publication-list', 'ref.bib')
PUBTEX = os.path.join(args.cv_repo, 'publication-list', 'pub.tex')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'pubs_final.json')

# Hand-picked short badge labels (journal/conference/workshop name), used
# only when nothing better can be auto-derived from the venue string.
BADGE = {
    'tsakonas2025vqelites': 'IEEE Trans. Evol. Comput.',
    'trinh2025hybrid': 'Ind. Eng. Chem. Res.',
    'totsila2025sensorimotor': 'RA-L',
    'syriopoulos2025dsm': 'Annals of Math. &amp; AI',
    'chatzilygeroudis2024robotdart': 'JOSS',
    'allard2023damage': 'ACM TELO',
    'khadivar2023selfcorrecting': 'IEEE Trans. SMC: Systems',
    'tsinganos2022behavior': 'Frontiers in Robotics and AI',
    'paul2020robustrl': 'JMLR',
    'chatzilygeroudis2019benchmark': 'RA-L',
    'sanchez2019benchmark': 'RA-L',
    'chatzilygeroudis2018survey': 'IEEE Trans. Robotics',
    'chatzilygeroudis2018resetfree': 'Robotics &amp; Auton. Systems',
    'cully2018limbo': 'JOSS',
    'vassiliades2017scaling': 'IEEE Trans. Evol. Comput.',
    'chatzilygeroudis2025summer': 'IEEE Robotics &amp; Automation Mag.',
    'chatzilygeroudis2020qd': 'Springer, SOIA series',
    'chatzilygeroudis2020ml': 'ACM Book Chapter',
    'ntagkas2026pgtt': 'IROS',
    'printzios2026constrained': 'GECCO',
    'ntagkas2025orientations': 'RiTA',
    'tsikelis2025ahmp': 'Humanoids',
    'tsiatsianas2025comparative': 'Humanoids',
    'trakas2025adaptive': 'ECC',
    'asimakopoulos2025icara': 'ICARA',
    'tsikelis2024gait': 'Humanoids',
    'asimakopoulos2024lion': 'LION',
    'evolving2023locomotion': 'IISA',
    'tsakonas2023agrl': 'IISA',
    'chatzilygeroudis2023lion': 'LION',
    'mayr2022skill': 'ROBIO',
    'mayr2022learning': 'CASE',
    'allard2022gecco': 'GECCO',
    'dimitropoulos2022raad': 'RAAD',
    'mayr2021learning': 'IROS',
    'chatzilygeroudis2021feature': 'LION',
    'duarte2020human': 'ICDL-EpiRob',
    'starke2019GraspForces': 'Humanoids',
    'kaushik2018multi': 'CoRL',
    'chatzilygeroudis2018using': 'ICRA',
    'pautrat2018bayesian': 'ICRA',
    'paul2018aloq': 'AAAI',
    'chatzilygeroudis2017black': 'IROS',
    'koustoumpardis2015human': 'RAAD',
    'printzios2025hybrid': 'RoboARCH @ ICRA',
    'totsila2023andp': 'L3H2 @ ICRA',
    'mayr2022combining': 'Workshop @ IROS',
    'mayr2022set': 'European Robotics Forum',
    'mouret201720': 'Workshop @ GECCO',
    'vassiliades2017comparing': 'GECCO (Poster)',
    'vassiliades2017comparison': 'Workshop @ GECCO',
    'papaspyros2016safety': 'BayesOpt @ NeurIPS',
    'chatzilygeroudis2016semi': 'AILTA @ ICRA',
}

# Entries with neither `url=` nor `doi=` in ref.bib (mostly pre-2022 papers
# hosted only via a personal-page or arXiv link) — taken from the matching
# \href{} in curriculum_vitae/cv_7.tex.
URL_OVERRIDE = {
    'tsinganos2022behavior': 'https://www.frontiersin.org/articles/10.3389/frobt.2022.974537/full',
    'paul2020robustrl': 'https://jmlr.org/papers/volume21/18-216/18-216.pdf',
    'chatzilygeroudis2020qd': 'https://arxiv.org/abs/2012.04322',
    'mayr2022skill': 'https://arxiv.org/abs/2203.10033',
    'mayr2022learning': 'https://arxiv.org/abs/2208.01605',
    'allard2022gecco': 'https://arxiv.org/abs/2204.05726',
    'dimitropoulos2022raad': 'https://link.springer.com/chapter/10.1007/978-3-031-04870-8_16',
    'mayr2021learning': 'https://arxiv.org/abs/2109.13050',
    'chatzilygeroudis2021feature': 'https://link.springer.com/chapter/10.1007/978-3-030-92121-7_6',
    'duarte2020human': 'http://costashatz.github.io/files/ICDL2020.pdf',
    'koustoumpardis2015human': 'https://scholar.google.gr/citations?view_op=view_citation&hl=en&user=tnf6B-EAAAAJ&citation_for_view=tnf6B-EAAAAJ:u5HHmVD_uO8C',
    'mayr2022combining': 'https://arxiv.org/abs/2212.03570',
    'mayr2022set': 'https://portal.research.lu.se/en/publications/how-to-set-up-amp-learn-new-robot-tasks-with-explainable-behavior',
    'chatzilygeroudis2016semi': 'https://arxiv.org/abs/1610.01407',
    # chatzilygeroudis2020ml ("Machine Learning Basics") has no known online
    # copy — left unlinked on purpose.
}


def norm(s):
    s = re.sub(r'\\textbf\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\{|\}', '', s)
    s = re.sub(r'[^a-z0-9]+', '', s.lower())
    return s


def auto_badge(venue):
    """Best-effort short label: the last, shortish parenthesised acronym in
    the venue string, with a trailing year stripped (e.g. "(IROS 2026)" ->
    "IROS"). Falls back to the full venue string."""
    m = None
    for m in re.finditer(r'\(([^()]{2,20})\)', venue or ''):
        pass  # keep the last match
    if m:
        acr = re.sub(r'\s*\d{4}$', '', m.group(1)).strip()
        if acr and len(acr) <= 20:
            return acr
    return venue


# ---- ref.bib ----
raw = open(BIB, encoding='utf-8').read()
entries = re.split(r'\n\s*(?=@\w+\{)', raw)
bib = {}
for e in entries:
    m = re.match(r'\s*@(\w+)\{([^,]+),', e)
    if not m:
        continue
    etype, key = m.group(1), m.group(2)

    def f(k, e=e):
        r = re.search(r'\b' + k + r'\s*=\s*\{(.*?)\},?\s*\n', e, re.S)
        return re.sub(r'\s+', ' ', r.group(1)).strip() if r else ''

    bib[key] = dict(type=etype, key=key, title=f('title').strip('{}'), author=f('author'),
                     journal=f('journal'), booktitle=f('booktitle'), year=f('year'),
                     volume=f('volume'), number=f('number'), pages=f('pages'),
                     doi=f('doi'), url=f('url'), note=f('note'))

# ---- pub.tex section order (use the commented English headings, which precede the Greek ones) ----
pt = open(PUBTEX, encoding='utf-8').read()
pt = pt[:pt.index('\\iffalse')]
heads = [(m.start(), m.group(1).strip()) for m in re.finditer(r'\\subsection\*\{(.*?)\}\n', pt)]
EN_OVERRIDE = {
    'Peer-Reviewed Journal Publications': 'Peer-Reviewed Journal Papers',
    'Invited and Peer-Reviewed Book Chapters': 'Peer-Reviewed Book Chapters',
    'Peer-Reviewed Conference Publications': 'Peer-Reviewed Conference Papers',
    'International Workshops and Minimally-Reviewed Publications': 'Peer-Reviewed Workshop Papers',
    # pub.tex has no commented English heading before the magazine-articles
    # section, so the Greek one is what gets captured as `h` below.
    'Άρθρα σε επαγγελματικά περιοδικά και περιοδικά εκλαΐκευσης': 'Magazine Articles',
}
blocks = []
for m in re.finditer(r'\\begin\{etaremune\}(.*?)\n  \\end\{etaremune\}', pt, re.S):
    h = None
    for pos, txt in heads:
        if pos < m.start():
            h = txt
        else:
            break
    keys = re.findall(r'\\bibentry\{([^}]+)\}', m.group(1))
    label = EN_OVERRIDE.get(h, h)
    blocks.append((label, keys))

# ---- carry forward code/video/url/badge from the previous run, by bib key ----
prev = {}
if os.path.exists(OUT):
    for sec in json.load(open(OUT, encoding='utf-8')):
        for it in sec['items']:
            prev[it['key']] = it


def split_authors(a):
    a = a.replace('\\&', '&')
    parts = re.split(r'\s+and\s+', a)
    out = []
    for p in parts:
        p = p.strip()
        bold = bool(re.search(r'\\textbf\{', p))
        name = re.sub(r'\\textbf\{([^}]*)\}', r'\1', p).strip()
        star = '*' in name
        name = name.replace('*', '').strip()
        if ',' in name:
            last, first = [x.strip() for x in name.split(',', 1)]
            name = f"{first} {last}"
        out.append(dict(name=name, self=bold, equal=star))
    return out


result = []
for label, keys in blocks:
    items = []
    for k in keys:
        b = bib.get(k)
        if not b:
            print('MISSING BIB:', k)
            continue
        venue = b['journal'] or b['booktitle']
        p = prev.get(k, {})
        url = b['url'] or URL_OVERRIDE.get(k, '') or p.get('url', '')
        badge = BADGE.get(k) or p.get('badge') or auto_badge(venue)
        items.append(dict(
            key=k, title=b['title'], authors=split_authors(b['author']),
            venue=venue, year=b['year'], volume=b['volume'], number=b['number'],
            pages=b['pages'], doi=b['doi'], url=url, note=b['note'], badge=badge,
            code=p.get('code', ''), video=p.get('video', ''),
        ))
    result.append(dict(label=label, items=items))

for sec in result:
    print(sec['label'], len(sec['items']))

json.dump(result, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved', OUT)
