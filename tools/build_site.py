# -*- coding: utf-8 -*-
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root (parent of tools/)
SITE = ROOT
PUBS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pubs_final.json'), encoding='utf-8'))

PREPRINTS = [
    dict(
        key='karydakis2026mpc',
        title='Real-Time Nonlinear MPC via Sequential Quadratic Programming with Structure-Exploiting ADMM and Interior-Point Methods for Underactuated Double-Pendulum Swing-Up',
        authors=[dict(name='Nick Karydakis', self=False, equal=False),
                 dict(name='Konstantinos Chatzilygeroudis', self=True, equal=False)],
        arxiv='2608.09272',
        year='2026',
        blurb='The real-time NMPC controller &mdash; built on a structure-exploiting SQP solver combining ADMM and interior-point methods &mdash; that won both tracks of the 4th AI Olympics with RealAIGym, evaluated on remote CloudPendulum hardware without prior knowledge of the system parameters.',
    ),
    dict(
        key='printzios2026hyal',
        title='Hybrid Augmented Lagrangian Method for General Constrained Optimization via Evolutionary Algorithms',
        authors=[dict(name='Lampros Printzios', self=False, equal=False),
                 dict(name='Konstantinos Chatzilygeroudis', self=True, equal=False)],
        arxiv='2607.16876',
        year='2026',
        blurb='Extended journal version of our <a href="https://doi.org/10.1145/3795101.3805360" target="_blank" rel="noopener">GECCO 2026</a> paper. Evolutionary algorithms are embedded within an Augmented Lagrangian loop, combining gradient-free exploration with systematic constraint handling on ten benchmark problems, including high-dimensional cases.',
    ),
]

def esc_amp(url):
    if not url:
        return url
    return re.sub(r"&(?!amp;|#\d+;|[a-zA-Z]+;)", "&amp;", url)

NAV = [
    ("Home", "index.html"),
    ("Research", "research.html"),
    ("Publications", "publications.html"),
    ("CV", "files/Konstantinos_Chatzilygeroudis_CV.pdf"),
    ("Contact", "contact.html"),
]

def nav_html(active):
    links = []
    for label, href in NAV:
        cls = ' class="active"' if href == active else ''
        target = ' target="_blank" rel="noopener"' if href.startswith('files/') else ''
        links.append(f'<a href="{href}"{cls}{target}>{label}</a>')
    return "\n".join(links)

def shell(title, description, active, body, extra_head=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="description" content="{description}">
<title>{title}</title>
<link rel="shortcut icon" href="assets/images/favicon.gif">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap">
<link rel="stylesheet" href="assets/css/main.css">
{extra_head}</head>
<body>

<header class="site-header">
  <div class="container">
    <a href="index.html" class="brand">
      <span class="brand-mark">KC</span>
      <span class="brand-name">Konstantinos Chatzilygeroudis</span>
    </a>
    <nav class="nav-links">
{nav_html(active)}
    </nav>
  </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
  <div class="container">
    <span>&copy; 2015&ndash;2026 Konstantinos Chatzilygeroudis &middot; Patras, Greece</span>
    <span class="footer-links">
      <a href="mailto:costashatz@upatras.gr">Email</a>
      <a href="https://scholar.google.com/citations?user=tnf6B-EAAAAJ&amp;hl=en" target="_blank" rel="noopener">Scholar</a>
      <a href="https://github.com/costashatz" target="_blank" rel="noopener">GitHub</a>
      <a href="https://www.linkedin.com/in/konstantinoschatzilygeroudis" target="_blank" rel="noopener">LinkedIn</a>
      <a href="https://orcid.org/0000-0003-3585-1027" target="_blank" rel="noopener">ORCID</a>
      <a href="https://www.youtube.com/@upatras-lar" target="_blank" rel="noopener">LAR on YouTube</a>
    </span>
  </div>
</footer>

</body>
</html>
'''

def authors_line(authors):
    names = []
    for a in authors:
        n = a['name']
        if a['self']:
            n = f'<span class="self">{n}</span>'
        if a['equal']:
            n += '*'
        names.append(n)
    return ", ".join(names)

def preprint_card(p):
    return f'''<div class="card preprint-card">
  <span class="badge">arXiv &middot; {p['year']}</span>
  <div class="pub-title"><a href="https://arxiv.org/abs/{p['arxiv']}" target="_blank" rel="noopener">{p['title']}</a></div>
  <div class="pub-authors">{authors_line(p['authors'])}</div>
  <p style="margin:2px 0 0; font-size:13px; color:var(--text-sub); line-height:1.5;">{p['blurb']}</p>
</div>'''

def write(name, html):
    with open(os.path.join(SITE, name), 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', name, len(html))
