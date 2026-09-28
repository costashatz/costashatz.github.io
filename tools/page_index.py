# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site import shell, write, PUBS, esc_amp, PREPRINTS, preprint_card, authors_line as _shared_authors_line

def find(key):
    for sec in PUBS:
        for it in sec['items']:
            if it['key'] == key:
                return it
    raise KeyError(key)

def pub_mini(key):
    it = find(key)
    url = esc_amp(it['url'] or (f"https://doi.org/{it['doi']}" if it['doi'] else '#'))
    venue = it['venue']
    return f'''<div class="pub-card">
  <span class="badge">{it['badge']} &middot; {it['year']}</span>
  <div class="pub-title"><a href="{url}" target="_blank" rel="noopener">{it['title']}</a></div>
  <div class="pub-authors">{_shared_authors_line(it["authors"])}</div>
  <div class="pub-venue">{venue} &middot; {it['year']}</div>
</div>'''

body = f'''
<div class="container">

  <div class="hero">
    <img class="avatar" src="assets/images/profile.jpg" alt="Konstantinos Chatzilygeroudis">
    <div>
      <h1>Konstantinos Chatzilygeroudis</h1>
      <div class="role-line">Assistant Professor in Robotics</div>
      <div class="affil-line">Electrical &amp; Computer Engineering Dept., University of Patras, Greece</div>
      <p class="tagline">I build robots that learn, adapt and act safely in the real world &mdash; combining reinforcement learning, evolutionary optimization and optimal control, and testing the results on physical hardware.</p>
      <div class="pill-row">
        <a class="pill" href="mailto:costashatz@upatras.gr">Email</a>
        <a class="pill" href="https://scholar.google.com/citations?user=tnf6B-EAAAAJ&amp;hl=en" target="_blank" rel="noopener">Google Scholar</a>
        <a class="pill" href="https://github.com/costashatz" target="_blank" rel="noopener">GitHub</a>
        <a class="pill" href="https://www.linkedin.com/in/konstantinoschatzilygeroudis" target="_blank" rel="noopener">LinkedIn</a>
        <a class="pill" href="https://orcid.org/0000-0003-3585-1027" target="_blank" rel="noopener">ORCID</a>
      </div>
    </div>
  </div>

  <div class="section prose" style="max-width:700px;">
    <p>I lead the robot-learning work of the <a href="https://lar.upatras.gr/" target="_blank" rel="noopener">Laboratory of Automation &amp; Robotics (LAR)</a> at the University of Patras. My group designs algorithms &mdash; from Quality-Diversity search to structure-exploiting trajectory optimization &mdash; and evaluates them on physical robots, from legged platforms to manipulators.</p>
    <p>Previously, I was a post-doctoral fellow at <a href="http://lasa.epfl.ch/" target="_blank" rel="noopener">LASA, EPFL</a> and at the <a href="http://cilab.math.upatras.gr/" target="_blank" rel="noopener">Computational Intelligence Laboratory</a>, University of Patras, where I was Principal Investigator of the H.F.R.I.-funded <a href="https://nosalro.github.io/" target="_blank" rel="noopener">NOSALRO</a> project (2022&ndash;2025). I hold a PhD in Robotics and Machine Learning from the University of Lorraine / Inria Nancy (LARSEN team).</p>
  </div>

  <div class="section">
    <div class="section-label">Highlights</div>
    <ul class="highlights">
      <li><strong>Winner</strong>, both Pendubot and Acrobot tracks &mdash; 4th AI Olympics with RealAIGym, IJCAI&ndash;ECAI 2026</li>
      <li><strong>Co-Chair</strong>, IEEE&ndash;RAS Technical Committee on Optimization for Robotics &middot; <strong>Associate Editor</strong>, IEEE RA-L</li>
      <li><strong>Best Paper Award</strong>, Complex Systems Track &mdash; GECCO 2022</li>
      <li><strong>H.F.R.I.</strong> grant recipient for Post-Doctoral Researchers (2022)</li>
    </ul>
  </div>

  <div class="section">
    <div class="section-label">Recent preprint</div>
    {preprint_card(PREPRINTS[0])}
  </div>

  <div class="section">
    <div class="section-label">Selected publications</div>
    <div class="pub-list">
{pub_mini('ntagkas2026pgtt')}
{pub_mini('tsakonas2025vqelites')}
{pub_mini('tsikelis2025ahmp')}
{pub_mini('allard2023damage')}
    </div>
    <a class="view-all" href="publications.html">View all publications &rarr;</a>
  </div>

  <div class="section">
    <div class="section-label">Research</div>
    <p class="lede">Robot learning, evolutionary optimization and optimal control &mdash; algorithms that work on physical robots, not only in simulation.</p>
    <div class="pill-row" style="margin-top:6px;">
      <a class="topic-pill" href="research.html#quality-diversity">Quality-Diversity</a>
      <a class="topic-pill" href="research.html#optimization">Optimization &amp; MPC</a>
      <a class="topic-pill" href="research.html#data-efficient-learning">Data-Efficient RL</a>
      <a class="topic-pill" href="research.html#adaptation">Adaptation &amp; Safety</a>
      <a class="topic-pill" href="research.html#software">Simulation &amp; Software</a>
    </div>
  </div>

</div>
'''

write('index.html', shell(
    "Konstantinos Chatzilygeroudis",
    "Assistant Professor in Robotics at the University of Patras. Robot learning, evolutionary optimization and optimal control.",
    "index.html", body))
