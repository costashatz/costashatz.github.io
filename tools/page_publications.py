# -*- coding: utf-8 -*-
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site import shell, write, PUBS, esc_amp, PREPRINTS, preprint_card, authors_line

def clean(s):
    if not s: return s
    s = s.strip()
    if s.startswith('{') and s.endswith('}'):
        s = s[1:-1]
    s = s.replace('\\&', '&amp;').replace('--', '–')
    return s

def venue_line(item):
    v = clean(item['venue'])
    bits = [v] if v else []
    extra = []
    if item.get('volume'): extra.append(f"vol. {item['volume']}")
    if item.get('number'): extra.append(f"no. {item['number']}")
    if item.get('pages'): extra.append(f"pp. {clean(item['pages'])}")
    if extra: bits.append(", ".join(extra))
    bits.append(item['year'])
    return " &middot; ".join(b for b in bits if b)

def links_row(item, primary_url):
    pills = []
    if item.get('doi') and (not primary_url or item['doi'] not in primary_url):
        pills.append(('DOI', f"https://doi.org/{item['doi']}"))
    if item.get('code'):
        pills.append(('Code', item['code']))
    if item.get('video'):
        pills.append(('Video', item['video']))
    pills = [(l, esc_amp(h)) for l, h in pills]
    if not pills:
        return ''
    parts = "".join(f'<a class="link-pill" href="{h}" target="_blank" rel="noopener">{l}</a>' for l, h in pills)
    return f'<div class="pub-links">{parts}</div>'

def pub_card(item):
    title = clean(item['title'])
    primary = esc_amp(item['url'] or (f"https://doi.org/{item['doi']}" if item['doi'] else ''))
    title_html = f'<a href="{primary}" target="_blank" rel="noopener">{title}</a>' if primary else title
    note = clean(item.get('note') or '')
    note_html = f'<div class="pub-venue" style="margin-top:2px;">{note}</div>' if note else ''
    badge = f'<span class="badge">{clean(item["badge"])} &middot; {item["year"]}</span>'
    return f'''<div class="pub-card">
  {badge}
  <div class="pub-title">{title_html}</div>
  <div class="pub-authors">{authors_line(item["authors"])}</div>
  <div class="pub-venue">{venue_line(item)}</div>
  {note_html}
  {links_row(item, primary)}
</div>'''

sections_html = []
for sec in PUBS:
    cards = [pub_card(it) for it in sec['items']]
    sections_html.append(f'''
  <h2 class="page-title">{sec['label']}</h2>
  <div class="pub-list">
{"".join(cards)}
  </div>''')

preprint = f'''
  <h2 class="page-title" style="margin-top:52px;">Preprints</h2>
  <div class="pub-list">
{"".join(preprint_card(p) for p in PREPRINTS)}
  </div>
'''

body = f'''
<div class="container">

  <div class="hero" style="padding-top:48px;">
    <div>
      <h1>Publications</h1>
      <p class="tagline" style="max-width:700px;">According to <a href="https://scholar.google.com/citations?user=tnf6B-EAAAAJ&amp;hl=en" target="_blank" rel="noopener">Google Scholar</a> (updated September 2026), this work has been cited 1,850 times, with an h-index of 22 and an i10-index of 28. Names in <span class="self">bold</span> are mine; * marks equal contribution.</p>
    </div>
  </div>

  {preprint}
{"".join(sections_html)}

</div>
'''

write('publications.html', shell(
    "Publications — Konstantinos Chatzilygeroudis",
    "Full list of journal papers, conference papers, book chapters, magazine articles and workshop papers by Konstantinos Chatzilygeroudis, with links to PDFs, code and videos.",
    "publications.html", body))
