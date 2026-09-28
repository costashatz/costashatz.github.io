# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site import shell, write

body = '''
<div class="container">

  <div class="hero" style="padding-top:48px;">
    <div>
      <h1>Contact</h1>
      <p class="tagline" style="max-width:640px;">Email is the best way to reach me &mdash; for research collaboration, PhD/postdoc inquiries, media requests, or anything else.</p>
    </div>
  </div>

  <div class="section" style="max-width:640px;">
    <div class="card kv-list">
      <div class="kv-row">
        <div class="kv-key">Email</div>
        <div class="kv-val"><a href="mailto:costashatz@upatras.gr">costashatz@upatras.gr</a><br><a href="mailto:costashatz@gmail.com">costashatz@gmail.com</a></div>
      </div>
      <div class="kv-row">
        <div class="kv-key">Affiliation</div>
        <div class="kv-val"><strong>Laboratory of Automation &amp; Robotics</strong><br>Dept. of Electrical &amp; Computer Engineering<br>University of Patras, GR-26504, Patras, Greece</div>
      </div>
      <div class="kv-row">
        <div class="kv-key">Online</div>
        <div class="kv-val">
          <div class="pill-row" style="margin-top:0;">
            <a class="pill" href="https://scholar.google.com/citations?user=tnf6B-EAAAAJ&amp;hl=en" target="_blank" rel="noopener">Google Scholar</a>
            <a class="pill" href="https://github.com/costashatz" target="_blank" rel="noopener">GitHub</a>
            <a class="pill" href="https://www.linkedin.com/in/konstantinoschatzilygeroudis" target="_blank" rel="noopener">LinkedIn</a>
            <a class="pill" href="https://orcid.org/0000-0003-3585-1027" target="_blank" rel="noopener">ORCID</a>
          </div>
        </div>
      </div>
    </div>
  </div>

</div>
'''

write('contact.html', shell(
    "Contact — Konstantinos Chatzilygeroudis",
    "Contact details for Konstantinos Chatzilygeroudis, Assistant Professor in Robotics at the University of Patras.",
    "contact.html", body))
