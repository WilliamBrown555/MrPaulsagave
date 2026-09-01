# -*- coding: utf-8 -*-
"""Builds the Mr. Paul's agave list website — one self-contained index.html."""
import html, re, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'Agave Website')
CREST = io.open(os.path.join(HERE, 'crest.svg'), encoding='utf-8').read()
CREST = CREST.replace('class="crest"', 'class="crest" aria-hidden="true" focusable="false"')

# name, half, full, abv, batch?, house, agave, tag
T = [
 ("Arette Artesanal Fuerte", 12, 21, "50.5%", 0, "Tequila Arette · Tequila, Jalisco", "Blue Weber · Los Valles", "Brick oven, cement-tank ferment"),
 ("Arette Reposado", 8, 15, "40%", 0, "Tequila Arette · Tequila, Jalisco", "Blue Weber · Los Valles", ""),
 ("Arette Silver", 7, 13, "40%", 0, "Tequila Arette · Tequila, Jalisco", "Blue Weber · Los Valles", ""),
 ("Casamigos Blanco", 11, 20, "40%", 0, "Diageo México · Atotonilco el Alto, Jalisco", "Blue Weber · Los Altos", ""),
 ("Casamigos Reposado", 13, 25, "40%", 0, "Diageo México · Atotonilco el Alto, Jalisco", "Blue Weber · Los Altos", ""),
 ("Clase Azul Reposado", 20, 38, "40%", 0, "Casa Tradición · Tlajomulco de Zúñiga, Jalisco", "Blue Weber · Los Altos", ""),
 ("Corazon Reposado", 6, 12, "40%", 0, "Casa San Matías · Los Altos, Jalisco", "Blue Weber · Los Altos estate", ""),
 ("Don Fulano Anejo", 13, 25, "40%", 0, "La Tequileña · Tequila, Jalisco", "Blue Weber · Los Altos", ""),
 ("Don Fulano Reposado", 12, 22, "40%", 0, "La Tequileña · Tequila, Jalisco", "Blue Weber · Los Altos", ""),
 ("Don Julio 1942", 15, 29, "40%", 0, "Destilería Don Julio · Atotonilco el Alto, Jalisco", "Blue Weber · Los Altos", ""),
 ("Don Julio Anejo", 12, 23, "40%", 0, "Destilería Don Julio · Atotonilco el Alto, Jalisco", "Blue Weber · Los Altos", ""),
 ("El Jimador Reposado", 7, 13, "40%", 0, "Casa Herradura · Amatitán, Jalisco", "Blue Weber · Los Valles", ""),
 ("El Jimador Silver", 6, 11, "40%", 0, "Casa Herradura · Amatitán, Jalisco", "Blue Weber · Los Valles", ""),
 ("El Tesoro Anejo", 14, 27, "40%", 0, "Destilería La Alteña · Arandas, Jalisco", "Blue Weber · Los Altos", "Tahona-crushed"),
 ("El Tesoro Blanco", 9, 17, "40%", 0, "Destilería La Alteña · Arandas, Jalisco", "Blue Weber · Los Altos", "Tahona-crushed"),
 ("El Tesoro Reposado", 10, 19, "40%", 0, "Destilería La Alteña · Arandas, Jalisco", "Blue Weber · Los Altos", "Tahona-crushed"),
 ("Herradura Anejo", 12, 22, "40%", 0, "Casa Herradura · Amatitán, Jalisco", "Blue Weber · Los Valles", ""),
 ("Herradura Blanco", 8, 16, "40%", 0, "Casa Herradura · Amatitán, Jalisco", "Blue Weber · Los Valles", ""),
 ("Herradura Reposado", 11, 20, "40%", 0, "Casa Herradura · Amatitán, Jalisco", "Blue Weber · Los Valles", ""),
 ("La Gritona Reposado", 9, 17, "40%", 0, "Destilería Raza Azteca · Valle de Guadalupe, Jalisco", "Blue Weber · Los Altos", "Distilled by Melly Barajas"),
 ("Lalo", 8, 15, "40%", 0, "Grupo Tequilero México · Arandas, Jalisco", "Blue Weber · Los Altos", "Additive-free blanco"),
 ("Mi Casa 9yr Extra Anejo", 25, 50, "43%", 1, "Casa Tequilera de Arandas · Arandas, Jalisco", "Blue Weber · El Cucuno estate, Michoacán", ""),
 ("Mijenta Blanco", 7, 14, "40%", 0, "Casa Tequilera de Arandas · Arandas, Jalisco", "Blue Weber · Los Altos", "Additive-free"),
 ("Mijenta Reposado", 9, 18, "40%", 0, "Casa Tequilera de Arandas · Arandas, Jalisco", "Blue Weber · Los Altos", "Additive-free"),
 ("Paladar Amburana", 12, 23, "40%", 0, "Tequila Arette · Tequila, Jalisco", "Blue Weber · Los Valles", "Destilado de agave — amburana cask"),
 ("Paladar Still Strength", 11, 21, "50%", 0, "Tequila Arette · Tequila, Jalisco", "Blue Weber · Los Valles", "Undiluted off the still"),
 ("Patron Silver", 9, 17, "40%", 0, "Hacienda Patrón · Atotonilco el Alto, Jalisco", "Blue Weber · Los Altos", ""),
 ("Riazul Reposado", 12, 22, "40%", 0, "Compañía Tequilera de Arandas · Arandas, Jalisco", "Blue Weber · Arandas estate", ""),
]

M = [
 ("5 Sentidos Pechuga De Mole", 22, 42, "48%", 1, "Delfino Tobón Mejía · San Pablo Ameyaltepec, Puebla", "Wild papalome & pizoma · Mixteca Poblana", "Single batch — distilled with mole"),
 ("Ilegal Mezcal", 8, 15, "40%", 0, "Familia Hernández · Santiago Matatlán, Oaxaca", "Espadín · Santiago Matatlán", ""),
 ("La Luna", 7, 13, "46%", 1, "Familia Pérez Escot, Las Azucenas · Etúcuaro, Michoacán", "Cupreata · Michoacán", ""),
 ("Madre Ancestral", 22, 40, "47%", 0, "Moisés Martínez · Santa Catarina Minas, Oaxaca", "Espadín & Tobasiche · Ocotlán, Oaxaca", "Clay-pot still"),
 ("Madre Espadin", 7, 14, "40%", 0, "Carlos Méndez Blas · Santiago Matatlán, Oaxaca", "Espadín · Valles Centrales", ""),
 ("Madre Red Ensamble", 9, 16, "45%", 0, "Méndez Blas & José García Morales · Santiago Matatlán, Oaxaca", "Espadín & Cuishe · Valles Centrales", ""),
 ("Real Minero Espadin", 20, 38, "46%", 1, "Familia Ángeles · Santa Catarina Minas, Oaxaca", "Espadín · Santa Catarina Minas", "Clay-pot still"),
 ("Rey Campero Joven", 16, 32, "48%", 1, "Vicente Sánchez Parada · Candelaria Yegolé, Oaxaca", "Espadín · Sierra Sur, Oaxaca", ""),
 ("Yoowe Bacanora", 9, 18, "43%", 1, "Ramón Miranda · Álamos, Sonora", "Maguey Pacífica · southern Sonora", "Bacanora"),
 ("Yuu Baal Joven Pechuga", 9, 17, "48%", 0, "Martimiano Hernández · San Juan del Río, Oaxaca", "Espadín · Valles Centrales", "Distilled with fruit & turkey breast"),
]

O = [
 ("Caballito Cerrero", 11, 20, "46%", 0, "Fábrica Santa Rita · Amatitán, Jalisco", "Agave azul · Amatitán valley", "Destilado de agave — uncertified by choice"),
 ("Comiteco Blanco", 8, 15, "42%", 0, "Casa Córdoba y Guillén · Comitán de Domínguez, Chiapas", "Maguey comiteco sap · Comitán", "Comiteco — made from sap"),
 ("El Guel Sotol", 8, 15, "45%", 0, "El Güel · Aldama, Chihuahua", "Wild dasylirion · Chihuahuan desert", ""),
 ("El Popo Avila Blanco", 7, 13, "44%", 0, "Noe Avila · Morelos", "Agave azul · slopes of Popocatépetl", "Destilado de agave"),
 ("El Popo Avila Reposado", 8, 15, "44%", 0, "Noe Avila · Morelos", "Agave azul · slopes of Popocatépetl", "Destilado de agave"),
 ("Revel Blanco", 6, 12, "40%", 0, "Revel Spirits, Noe Avila · Morelos", "Agave azul · Morelos", "Destilado de agave"),
 ("Sol2Noches", 8, 15, "40%", 0, "Gerardo Ruelas · Chihuahua", "Wild dasylirion · Chihuahuan desert", "Sotol"),
]

SECTIONS = [("Tequila", T), ("Mezcal", M), ("Other Agave", O)]

def e(s): return html.escape(s, quote=True)
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def rows(items):
    out = []
    for nm, half, full, abv, batch, house, agave, tag in items:
        key = ' '.join([nm, house, agave, tag]).lower()
        key = key.replace('·', ' ')
        mark = '<span class="bx" title="bottled at batch strength">◇</span>' if batch else ''
        det = f'<span class="hs">{e(house)}</span><span class="dot"> — </span><span class="ag">{e(agave)}</span>'
        if tag:
            det += f'<span class="tg">{e(tag)}</span>'
        out.append(
            f'<li class="pour" data-n="{e(key)}">'
            f'<span class="top">'
            f'<span class="nm">{e(nm)}</span>'
            f'<span class="ldr"></span>'
            f'<span class="pf">{e(abv)}{mark}</span>'
            f'<span class="pr"><span class="p1">{half}</span><span class="sl">/</span><span class="p2">{full}</span></span>'
            f'</span>'
            f'<span class="org">{det}</span>'
            f'</li>'
        )
    return ''.join(out)

secs = ''.join(
    f'<section class="sec" id="{slug(t)}">'
    f'<header class="sechd"><h2>{e(t)}</h2>'
    f'<span class="cl ca">ABV</span><span class="cl cb">Half</span><span class="cl cc">Full</span></header>'
    f'<ul class="pours">{rows(items)}</ul></section>'
    for t, items in SECTIONS
)

chips = ''.join(f'<a class="chip" href="#{slug(t)}">{e(t)}</a>' for t, _ in SECTIONS)
count = sum(len(i) for _, i in SECTIONS)

DESC = ("The agave list at Mr. Paul's Supper Club in Edina, Minnesota — "
        f"{count} bottles of tequila, mezcal, sotol, bacanora and other agave spirits, "
        "with ABV, distillery and half or full pours.")

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Mr. Paul's Agave List</title>
<meta name="description" content="{e(DESC)}">
<meta name="theme-color" content="#f3f1ee">
<meta name="color-scheme" content="light">

<!-- link preview (texts, iMessage, Facebook, Instagram bio, link tree) -->
<meta property="og:type" content="website">
<meta property="og:title" content="Mr. Paul's Agave List">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:site_name" content="Mr. Paul's Supper Club">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Mr. Paul's Agave List">
<meta name="twitter:description" content="{e(DESC)}">

<!-- crest favicon, inlined so there is no second file to upload -->
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23f3f1ee'/%3E%3Ctext x='16' y='23' font-family='Helvetica,Arial,sans-serif' font-size='19' font-weight='bold' fill='%238c2830' text-anchor='middle'%3EA%3C/text%3E%3C/svg%3E">
</head>
<body>
<style>
:root{{
  --ground:#f3f1ee; --panel:#eae5df; --panel-2:#e3ddd6;
  --wine:#8c2830; --wine-lit:#a83a41; --wine-soft:#b2646a;
  --ink:#26221f; --muted:#7b7369; --faint:#948b80;
  --rule:rgba(140,40,48,.28); --hair:rgba(140,40,48,.5);
}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:"Helvetica Neue",Helvetica,Arial,"Segoe UI",system-ui,sans-serif;
  font-size:16px; line-height:1.5;
}}
.sheet{{
  max-width:720px; margin:0 auto; padding:0 26px 84px;
  border-left:1px solid var(--hair); border-right:1px solid var(--hair);
  min-height:100vh;
}}
@media (max-width:640px){{
  .sheet{{border-left:0;border-right:0;padding:0 18px 72px}}
}}

/* ---------- masthead ---------- */
.mast{{padding:46px 0 4px;text-align:center}}
.mast h1{{
  font-weight:800;font-size:clamp(42px,12vw,66px);line-height:.95;
  letter-spacing:.01em;text-transform:uppercase;margin:0;color:var(--wine);
}}
.eyebrow{{
  font-weight:500;font-size:clamp(11px,2.6vw,13px);letter-spacing:.3em;
  text-transform:uppercase;color:var(--ink);margin:14px 0 0;
}}
.hr{{width:min(340px,72%);height:1px;background:var(--wine);opacity:.75;margin:20px auto 0}}
.tag{{
  margin:14px auto 0;max-width:46ch;color:var(--muted);
  font-style:italic;font-size:14px;line-height:1.6;
}}

/* ---------- sticky controls ---------- */
.tools{{
  position:sticky;top:0;z-index:20;margin:26px -26px 0;padding:12px 26px 10px;
  background:var(--ground);
}}
.tools::after{{content:'';position:absolute;left:0;right:0;top:100%;height:16px;pointer-events:none;
  background:linear-gradient(var(--ground),rgba(243,241,238,0))}}
@media (max-width:640px){{.tools{{margin:22px -18px 0;padding:10px 18px 8px}}}}
.search{{position:relative;display:block}}
.search svg{{position:absolute;left:13px;top:50%;transform:translateY(-50%);
  width:15px;height:15px;stroke:var(--faint);fill:none;stroke-width:1.8}}
#q{{
  width:100%;padding:11px 14px 11px 37px;border-radius:2px;
  background:#fbfaf8;border:1px solid var(--rule);color:var(--ink);
  font-family:inherit;font-size:15px;
}}
#q::placeholder{{color:var(--faint)}}
#q:focus{{outline:2px solid var(--wine);outline-offset:1px;border-color:transparent}}
.chips{{display:flex;gap:7px;overflow-x:auto;padding:10px 0 2px;scrollbar-width:none}}
.chips::-webkit-scrollbar{{display:none}}
.chip{{
  flex:0 0 auto;text-decoration:none;color:var(--wine);
  font-weight:600;font-size:12px;letter-spacing:.14em;text-transform:uppercase;
  padding:6px 11px;border:1px solid var(--rule);border-radius:2px;
  transition:color .18s,border-color .18s,background .18s;white-space:nowrap;
}}
.chip:hover,.chip:focus-visible{{color:#fff;background:var(--wine);border-color:var(--wine)}}
.legend{{
  margin:0;text-align:right;padding:9px 0 1px;
  font-weight:600;font-size:11px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--muted);
}}
.legend b{{font-weight:600;color:var(--wine)}}

/* ---------- sections ---------- */
.sec{{padding-top:40px;scroll-margin-top:118px}}
.sec.hide{{display:none}}
.sechd{{display:flex;align-items:baseline;gap:12px;
  border-bottom:1px solid var(--wine);padding-bottom:7px}}
.sechd h2{{
  font-weight:700;font-size:19px;letter-spacing:.1em;
  text-transform:uppercase;margin:0;color:var(--wine);
}}
.cl{{font-weight:600;font-size:10px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--faint);text-align:right;flex:0 0 auto}}
.ca{{margin-left:auto;width:56px}}
.cb{{width:32px}}
.cc{{width:27px}}
.pours{{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column}}
.pour{{display:flex;flex-direction:column;padding:9px 8px 10px 0;
  border-radius:2px;transition:background .16s}}
.pour.hide{{display:none}}
.pour:hover{{background:var(--panel);padding-left:8px;margin-left:-8px}}
.top{{display:flex;align-items:baseline;gap:7px}}
.nm{{font-size:15.5px;line-height:1.35;font-weight:500}}
.ldr{{
  flex:1;min-width:12px;align-self:flex-end;height:1px;margin-bottom:5px;
  background-image:radial-gradient(circle,rgba(38,34,31,.34) 1px,transparent 1.2px);
  background-size:5px 2px;background-repeat:repeat-x;background-position:bottom;
}}
.pf{{
  flex:0 0 auto;width:56px;text-align:right;font-weight:500;font-size:12px;
  letter-spacing:.02em;color:var(--muted);font-variant-numeric:tabular-nums;
  white-space:nowrap;position:relative;
}}
.bx{{color:var(--wine-soft);font-size:9px;vertical-align:2px;margin-left:2px}}
.pr{{display:flex;align-items:baseline;flex:0 0 auto;font-weight:500;font-size:15px;
  font-variant-numeric:tabular-nums;color:var(--wine);white-space:nowrap}}
.p1{{width:30px;text-align:right;color:var(--wine-soft)}}
.sl{{width:15px;text-align:center;color:var(--wine-soft);font-size:12px}}
.p2{{width:27px;text-align:right}}
.org{{margin-top:3px;font-size:12.5px;line-height:1.45;color:var(--muted);
  letter-spacing:.005em;max-width:58ch}}
.org .ag{{font-style:italic;color:#6f6659}}
.org .dot{{color:var(--faint)}}
.org .tg{{display:block;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--wine-soft);margin-top:2px;font-weight:600}}

/* ---------- empty + footer ---------- */
#empty{{display:none;padding:56px 0;text-align:center;color:var(--muted);font-style:italic}}
#empty.on{{display:block}}
.foot{{margin-top:56px;padding-top:24px;border-top:1px solid var(--rule);
  color:var(--muted);font-size:13px;line-height:1.7}}
.footmark{{width:96px;margin:0 auto 18px;color:var(--wine)}}
.footmark svg{{display:block;width:100%;height:auto}}
.foot strong{{color:var(--wine);font-weight:700;letter-spacing:.12em;
  text-transform:uppercase;font-size:11px;display:block;margin-bottom:6px}}
.foot em{{font-style:normal;color:var(--wine)}}
.links{{display:flex;flex-wrap:wrap;gap:10px 22px;margin:18px 0 0}}
.links a{{color:var(--wine);text-decoration:none;font-weight:600;font-size:12px;
  letter-spacing:.14em;text-transform:uppercase;
  border-bottom:1px solid var(--rule);padding-bottom:2px}}
.links a:hover,.links a:focus-visible{{color:var(--wine-lit);border-color:var(--wine-lit)}}
@media (max-width:520px){{.ldr{{display:none}}.top{{gap:10px}}.nm{{flex:1}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important}}}}
</style>

<div class="sheet">
  <header class="mast">
    <h1>Agave</h1>
    <p class="eyebrow">Tequila &middot; Mezcal &middot; Agave Spirits</p>
    <div class="hr"></div>
    <p class="tag">Every bottle on the back bar, with what&rsquo;s in it and where it came from. Prices are for a half pour or a full pour.</p>
  </header>

  <div class="tools">
    <label class="search" for="q">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/></svg>
      <input id="q" type="search" placeholder="Search a bottle, a distillery, an agave&hellip;" autocomplete="off" aria-label="Search the agave list">
    </label>
    <nav class="chips" aria-label="Jump to a category">{chips}</nav>
    <p class="legend"><b>Half &amp; full pour</b></p>
  </div>

  {secs}

  <p id="empty">Nothing by that name. Try a distillery, a town, or an agave.</p>

  <div class="foot">
    <div class="footmark">{CREST}</div>
    <strong>A note on the list</strong>
    Under each bottle is the house that made it, the town it was made in, and the agave it was made from. A <em>&#9671;</em> means the bottle is filled at batch strength &mdash; the ABV moves a little every time we restock, so the number on the bottle is the one that counts.<br>
    Two prices means two pours &mdash; half and full. A few of these are single-batch and finite; when they&rsquo;re gone they&rsquo;re gone. Prices subject to change.
    <p class="links">
      <a href="https://mrpaulswhiskey.netlify.app/">The whiskey list</a>
      <a href="https://www.mrpaulssupperclub.com/menu/">All menus</a>
      <a href="https://www.mrpaulssupperclub.com/">mrpaulssupperclub.com</a>
    </p>
  </div>
</div>

<script>
(function(){{
  var q = document.getElementById('q'),
      pours = [].slice.call(document.querySelectorAll('.pour')),
      secs = [].slice.call(document.querySelectorAll('.sec')),
      empty = document.getElementById('empty');
  function run(){{
    var t = q.value.trim().toLowerCase();
    pours.forEach(function(p){{
      p.classList.toggle('hide', t !== '' && p.dataset.n.indexOf(t) === -1);
    }});
    var any = false;
    secs.forEach(function(s){{
      var vis = s.querySelectorAll('.pour:not(.hide)').length;
      s.classList.toggle('hide', vis === 0);
      if (vis) any = true;
    }});
    empty.classList.toggle('on', !any);
  }}
  q.addEventListener('input', run);
  q.addEventListener('search', run);
  run();
}})();
</script>
</body>
</html>
"""

os.makedirs(OUT, exist_ok=True)
with io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(HTML)
print("bottles:", count, "bytes:", len(HTML.encode('utf-8')))
