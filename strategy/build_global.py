"""Global Employer of Record strategy (Category 1). Writes out/index.html.
Data: global_demand.json (Ahrefs, 161 EOR keywords, 23 Sep 2026), global_footprint.json
(competitor sitemaps, about 131,000 URLs), issues.json and inventory.py (Paybooks audit)."""
import os, re, json, html
H = os.path.dirname(os.path.abspath(__file__)); E = html.escape
fmt = lambda n: f"{n:,}"
D = json.load(open(f"{H}/global_demand.json")); F = json.load(open(f"{H}/global_footprint.json"))
ISS = json.load(open(f"{H}/issues.json"))
inv = {"__file__": f"{H}/inventory.py"}; exec(open(f"{H}/inventory.py").read(), inv)
INV, PGW = inv["INV"], inv["W"]; EOR_WORDS = sum(PGW(u) for u, *_ in INV)
CSS = re.search(r'CSS = """(.*?)"""', open(f"{H}/build_ceo.py").read(), re.S).group(1)

BT = D["bucket_totals"]; TOTAL = sum(BT.values()); NKW = sum(len(v) for v in D["buckets"].values())
CTRY = [c for c in D["countries"] if "(region)" not in c["country"]]
REG = [c for c in D["countries"] if "(region)" in c["country"]]
TOP9 = CTRY[:9]; NEXT = CTRY[9:]
TOP9V = sum(c["volume"] for c in TOP9); NEXTV = sum(c["volume"] for c in NEXT); REGV = sum(c["volume"] for c in REG)
CORE_V = BT["core"] + BT["best"] + BT["what"] + BT["compare"]
assert CORE_V + BT["india"] + TOP9V + NEXTV + REGV == TOTAL

# ---------- chart: demand by intent ----------
GROUPS = [("Core EOR service searches", BT["core"], "employer of record · EOR services · global EOR"),
          ("“Employer of record [country]”", BT["country"], f"{len(CTRY)} countries in the sample"),
          ("India EOR searches", BT["india"], "the country Paybooks serves today"),
          ("Best EOR providers", BT["best"], "best employer of record · EOR companies"),
          ("What an EOR is", BT["what"], "meaning · how it works"),
          ("EOR vs PEO and other comparisons", BT["compare"], "EOR vs PEO · EOR vs staffing agency")]
mx = max(v for _, v, _ in GROUPS); rows = []
for i, (lab, v, sub) in enumerate(GROUPS):
    y = i * 58; w = max(4, 470 * v / mx); col = "#4F8A10" if i < 3 else "#9FC76A"
    rows.append(f'<text x="0" y="{y+20}" class="lb">{E(lab)}</text><text x="0" y="{y+38}" class="ax">{E(sub)}</text>'
                f'<rect x="360" y="{y+8}" width="{w:.0f}" height="26" rx="6" fill="{col}"/><text x="{360+w+10:.0f}" y="{y+26}" class="vl">{fmt(v)}</text>')
chart_demand = f'<svg viewBox="0 0 980 {len(GROUPS)*58}" class="chart" role="img" aria-label="Monthly searches by intent">{"".join(rows)}</svg>'

# ---------- chart: country demand ----------
cm = max(c["volume"] for c in CTRY); cr = []
for i, c in enumerate(CTRY):
    col, x0 = ("#4F8A10" if i < 9 else "#9FC76A"), (0 if i < 13 else 500); yy = (i if i < 13 else i - 13) * 34
    w = max(4, 250 * c["volume"] / cm)
    cr.append(f'<text x="{x0}" y="{yy+18}" class="lb">{E(c["country"])}</text><rect x="{x0+170}" y="{yy+5}" width="{w:.0f}" height="20" rx="5" fill="{col}"/>'
              f'<text x="{x0+170+w+8:.0f}" y="{yy+20}" class="vl">{fmt(c["volume"])}</text>')
chart_ctry = f'<svg viewBox="0 0 980 {13*34}" class="chart" role="img" aria-label="Employer of record searches by country">{"".join(cr)}</svg>'

# ---------- competitor footprint ----------
NAME = {"usemultiplier.com": "Multiplier", "remote.com": "Remote", "playroll.com": "Playroll", "papayaglobal.com": "Papaya Global",
        "skuad.io": "Skuad", "g-p.com": "G-P", "velocityglobal.com": "Velocity Global", "asanify.com": "Asanify", "deel.com": "Deel",
        "rippling.com": "Rippling", "oysterhr.com": "Oyster"}
fam = F["families"]; cov = F["country_coverage"]
def topic(d):
    f = fam[d]; return sum(v for k, v in f.items() if k in ("Country x topic", "Country payroll page", "Country cost page", "Country PEO page"))
def contr(d): return fam[d].get("Country hiring (contractors)", 0)
def roles(d): return fam[d].get("Role pages", 0)
comp = sorted(NAME, key=lambda d: -cov.get(d, 0))
cmx = max(cov[d] for d in comp)
frows = "".join(
    f'<tr><td><b>{NAME[d]}</b></td><td><div style="display:flex;align-items:center;gap:10px"><span style="display:inline-block;height:10px;border-radius:5px;background:#4F8A10;width:{120*cov[d]/cmx:.0f}px"></span><b>{cov[d]}</b></div></td>'
    f'<td class="n">{fmt(topic(d)) if topic(d) else "–"}</td><td class="n">{contr(d) or "–"}</td><td class="n">{roles(d) or "–"}</td></tr>' for d in comp)
frows += '<tr class="me"><td><b>Paybooks today</b></td><td><b>1</b> (India)</td><td class="n">–</td><td class="n">–</td><td class="n">–</td></tr>'
NLEAD = len([d for d in comp if cov[d] >= 100]); CMIN = min(cov[d] for d in comp if cov[d] >= 100); CMAX = cmx
DEEP = sorted([topic(d) for d in comp if topic(d) >= 700]); ND = len(DEEP)

# ---------- plan numbers ----------
CORE_PAGES = ["The global EOR hub, /employer-of-record/ (sample built)", "Countries index, /employer-of-record/countries/",
              "What an employer of record is", "EOR vs PEO", "Best EOR providers, with published prices",
              "Paybooks vs Deel", "Paybooks vs Remote", "Paybooks vs Multiplier", "Paybooks vs Skuad", "Paybooks vs Rippling",
              "Employer cost calculator for every country"]
GUIDES = ["Hiring guide", "Employer cost", "Payroll and taxes", "Benefits", "Leave and holidays", "Termination and severance", "Work permits and visas", "Minimum wage and salaries"]
PER = len(GUIDES) + 3  # EOR page + guides + payroll + contractors
ROLES = ["Software developers", "Sales representatives", "Customer support", "Accountants", "Data analysts"]
INDIA_W1, INDIA_W2 = 17, 33
W1 = len(CORE_PAGES) + len(TOP9) + INDIA_W1
W2 = len(TOP9) * (PER - 1) + INDIA_W2
W3 = len(NEXT) * PER + len(ROLES) * len(TOP9)
TOTALP = W1 + W2 + W3
W1V = CORE_V + BT["india"] + TOP9V
top9s = ", ".join(c["country"] for c in TOP9); nexts = ", ".join(c["country"] for c in NEXT)
json.dump({"total_searches": TOTAL, "keywords": NKW, "core": CORE_V, "country": BT["country"], "india": BT["india"], "n_countries": len(CTRY),
           "w1": W1, "w2": W2, "w3": W3, "total_pages": TOTALP, "w1_searches": W1V, "per_country": PER, "top9": [c["country"] for c in TOP9],
           "next": [c["country"] for c in NEXT], "leaders": NLEAD, "cov_min": CMIN, "cov_max": CMAX}, open(f"{H}/global_numbers.json", "w"), indent=1)

SEVC = {"High": "#C2410C", "Medium": "#8A94A0"}
iss_rows = "".join(f'<tr><td class="n">{k}</td><td><span class="vt" style="--c:{SEVC.get(sv, "#8A94A0")}">{sv}</span><div><b>{E(t)}</b></div></td><td class="mut">{E(ev)}</td><td>{E(fx)}</td></tr>' for k, (sv, t, ev, fx) in enumerate(ISS, 1))

tier = lambda n, t, url, body, ex="": (f'<div class="tier"><div class="tn">{n}</div><div><b>{t}</b><code>{url}</code><p>{body}</p>'
                                      + (f'<p class="mut">{ex}</p>' if ex else "") + '</div></div>')
ARCH = "".join([
  tier("1", "Global EOR hub", "/employer-of-record/", "The page for the head searches: what Paybooks does, how it works, who it fits, what it costs, and a country picker. Every other page links up to it.", "Sample built: the landing page in this proposal."),
  tier("2", "Country product pages", "/employer-of-record/[country]/", "One page per country Paybooks covers: hire there without an entity, the local contract, benefits and costs, timeline, and a quote form. This is the product page buyers compare.", "Sample built: Employer of Record India, the depth every country page follows."),
  tier("3", "Services in each country", "/payroll/[country]/ · /contractors/[country]/", "The other Paybooks services per country, cross-linked with the EOR page: payroll for companies with their own entity, and hiring or converting contractors.", "Links Category 1 to Category 2 (Multi-Country Payroll) and, in India, to Category 3 (Managed India Office)."),
  tier("4", "Country guides", "/employer-of-record/[country]/[topic]/", f"{len(GUIDES)} guides per country: " + ", ".join(g.lower() for g in GUIDES) + ". They answer the questions buyers ask before they hire.", f"The leaders run {min(DEEP):,} to {max(DEEP):,} of these pages each."),
  tier("5", "Role × country pages", "/hire/[role]/[country]/", "“Hire a software developer in Poland.” One template, filled with each country's salary band, all-in cost and notice rules.", "India alone carries 16,350 searches a month across 15 roles (India deep dive)."),
  tier("6", "Tools, comparisons and glossary", "/tools/ · /compare/ · /glossary/", "Employer cost calculator for every country, salary benchmarks, Paybooks vs each competitor, best EOR providers, EOR vs PEO, and a glossary built to be quoted by AI answers.", ""),
])

PAGE = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Global EOR Strategy</title><meta name="robots" content="noindex,nofollow">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><style>{CSS}
.tiers{{display:grid;gap:10px}}.tier{{display:grid;grid-template-columns:44px 1fr;gap:16px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px}}
.tn{{width:36px;height:36px;border-radius:10px;background:var(--forest);color:var(--lime);font:600 17px/36px "Instrument Sans";text-align:center}}
.tier b{{font:600 18px "Instrument Sans";margin-right:10px}}.tier p{{margin:6px 0 0;font-size:15px;color:var(--ink2)}}.tier .mut{{font-size:13.5px}}
.plan td b{{font-family:"Instrument Sans"}}.tier>div{{min-width:0}}.tier code{{overflow-wrap:anywhere;display:inline-block;max-width:100%}}@media(max-width:560px){{.tier{{grid-template-columns:1fr;gap:10px}}}}
</style></head><body>
<header class="hero"><div class="wrap"><span class="eyebrow">Employer of Record · Search strategy · Paybooks</span>
<h1>Category 1: <em>Employer of Record (EOR)</em></h1>
<p class="sub">An employer of record lets a company hire people in any country where it has no entity. Buyers search country by country, and the leaders answer with a page for every country, every service in it and every role hired there. Paybooks covers one country today. This is the plan to build the global footprint.</p>
<div class="kp"><div><b>{fmt(TOTAL)}</b><span>monthly searches measured across {NKW} EOR keywords, Google USA and India</span></div><div><b>{CMIN}–{CMAX}</b><span>countries covered by each global leader's pages</span></div>
<div><b>1</b><span>country Paybooks covers on its site today: India</span></div><div><b>{fmt(TOTALP)}</b><span>pages in three waves, from {len(TOP9)+1} countries to {len(CTRY)+1}</span></div></div></div></header>
<nav class="toc" aria-label="Sections"><a href="#answer" aria-label="Findings"><span>Findings</span></a><a href="#demand" aria-label="Demand"><span>Demand</span></a><a href="#leaders" aria-label="What leaders built"><span>What leaders built</span></a><a href="#today" aria-label="Paybooks today"><span>Paybooks today</span></a><a href="#arch" aria-label="Site architecture"><span>Site architecture</span></a><a href="#plan" aria-label="The plan"><span>The plan</span></a><a href="#pseo" aria-label="Programmatic rules"><span>Programmatic rules</span></a><a href="#india" aria-label="India deep dive"><span>India deep dive</span></a><a href="#appendix" aria-label="Evidence"><span>Evidence</span></a></nav>
<main class="wrap">
<section id="answer"><span class="num">FINDINGS</span><h2>Three findings decide the strategy.</h2>
<div class="take"><div><b>Buyers search country by country.</b><p>“Employer of record [country]” searches add up to {fmt(BT["country"])} a month across {len(CTRY)} countries, almost as much as the core “employer of record” searches ({fmt(BT["core"])}). India adds {fmt(BT["india"])}. The country page is the product page.</p></div>
<div><b>Every global leader builds a page per country.</b><p>{NLEAD} of {len(comp)} competitors publish pages for {CMIN} to {CMAX} countries. {ND} go further, with {min(DEEP):,} to {max(DEEP):,} country guides each on payroll, benefits, termination and work permits. Skuad adds {roles("skuad.io")} role pages.</p></div>
<div><b>Paybooks starts from one country.</b><p>Paybooks has {len(INV)} Employer of Record pages, all about India, and they rank for one keyword. Outside India there is no page to fix, so the new site can be built right from day one.</p></div></div></section>

<section id="demand"><span class="num">01 · DEMAND</span><h2>{fmt(TOTAL)} monthly searches, and country searches are a third of them.</h2>
<p class="lead">Grouped by what the searcher wants. The dark-green groups ship first. This is a floor: it counts only the {NKW} keywords measured, before country guides and role pages.</p>
<div class="panel">{chart_demand}</div>
<h3 class="subh">“Employer of record [country]”: searches by country</h3>
<div class="panel">{chart_ctry}<div class="legend"><span style="--c:#4F8A10">Wave 1 countries: the 9 with the most searches, plus India</span><span style="--c:#9FC76A">Wave 3 countries</span></div></div>
<p class="note">Ahrefs Keywords Explorer, Google USA, 23 September 2026. {"Regional searches (" + ", ".join(c["country"].replace(" (region)", "") for c in REG) + f", {fmt(REGV)} a month) are left off the chart and are served by the country pages in that region." if REG else ""}</p></section>

<section id="leaders"><span class="num">02 · WHAT LEADERS BUILT</span><h2>Country pages are the product. Guides are the depth.</h2>
<p class="lead">Every competitor's sitemap was fetched and each URL sorted by template. The pattern is the same everywhere: one product page per country, guides under it, and role or contractor pages as the long tail.</p>
<div class="tw"><table><thead><tr><th>Competitor</th><th>Countries with a page</th><th class="n">Country guides</th><th class="n">Contractor country pages</th><th class="n">Role pages</th></tr></thead><tbody>{frows}</tbody></table></div>
<p class="note">English pages only, translated copies removed. “Country guides” counts pages such as payroll, benefits, costs and work permits under a country. Source: competitor sitemaps, about 131,000 URLs across 13 sites, September 2026.</p></section>

<section id="today"><span class="num">03 · PAYBOOKS TODAY</span><h2>One country, fourteen pages, one keyword.</h2>
<p class="lead">Paybooks' Employer of Record content covers India only: {len(INV)} pages and about {fmt(EOR_WORDS)} words, ranking for one keyword. The faults below are fixed in the India country cluster.</p>
<div class="big3"><div><b>1</b><span>country with an EOR page today</span></div><div><b>{len(INV)}</b><span>EOR pages, all about India</span></div><div class="bad"><b>1</b><span>keyword ranking, “eor solutions” at #8 in India</span></div></div>
<details class="blk"><summary>{len(ISS)} issues on the current pages, most damaging first</summary><div class="tw"><table><thead><tr><th class="n">#</th><th>Issue</th><th>Evidence</th><th>Fix in the plan</th></tr></thead><tbody>{iss_rows}</tbody></table></div></details>
<p class="note">Checked on the live pages, 24 September 2026. Rankings from Ahrefs.</p></section>

<section id="arch"><span class="num">04 · SITE ARCHITECTURE</span><h2>One hub, a product page per country, and everything under it.</h2>
<p class="lead">Six layers, each answering a different search. Links run down from the hub to every country, across between a country's pages, and back up to the hub.</p>
<div class="tiers">{ARCH}</div></section>

<section id="plan"><span class="num">05 · THE PLAN</span><h2>{fmt(TOTALP)} pages in three waves.</h2>
<p class="lead">Countries are chosen by measured searches. The final list follows where Paybooks can employ; each added country brings {PER} pages from the same templates.</p>
<div class="tw plan"><table><thead><tr><th>Wave</th><th>What ships</th><th class="n">Pages</th><th class="n">Measured searches / mo</th></tr></thead><tbody>
<tr><td><b>Wave 1 · at launch</b></td><td>The global hub and {len(CORE_PAGES)-1} core pages · EOR product pages for {top9s} · the India cluster's first {INDIA_W1} pages</td><td class="n"><b>{W1}</b></td><td class="n"><b>{fmt(W1V)}</b></td></tr>
<tr><td><b>Wave 2 · depth</b></td><td>{len(GUIDES)} country guides, a payroll page and a contractor page for each Wave 1 country · the India cluster's other {INDIA_W2} pages</td><td class="n"><b>{W2}</b></td><td class="n">Long tail, not in the sample</td></tr>
<tr><td><b>Wave 3 · reach</b></td><td>{len(NEXT)} more countries, {PER} pages each: {nexts} · “Hire a [role] in [country]” for {len(ROLES)} roles in the Wave 1 countries</td><td class="n"><b>{W3}</b></td><td class="n"><b>{fmt(NEXTV)}</b></td></tr>
<tr class="me"><td><b>Total</b></td><td>{len(CTRY)+1} countries covered</td><td class="n"><b>{fmt(TOTALP)}</b></td><td class="n"><b>{fmt(W1V+NEXTV)}</b></td></tr>
</tbody></table></div>
<div class="two" style="margin-top:18px"><div class="card acc"><b>Core pages in Wave 1</b><p>{" · ".join(E(p) for p in CORE_PAGES)}</p></div>
<div class="card acc"><b>{PER} pages per country</b><p>The EOR product page · {" · ".join(g.lower() for g in GUIDES)} · payroll in [country] · contractors in [country]. Roles for Wave 3: {", ".join(r.lower() for r in ROLES)}.</p></div></div>
<p class="note">Measured searches are from the {NKW}-keyword sample. {fmt(REGV)} regional searches are not assigned to a wave.</p></section>

<section id="pseo"><span class="num">06 · PROGRAMMATIC RULES</span><h2>Hundreds of pages, none of them thin.</h2>
<p class="lead">Templates make the scale possible. These rules keep every page worth ranking.</p>
<div class="tw"><table><tbody>
<tr><td><b>Real data on every page</b></td><td>Each country page carries its own employer costs, contract rules, benefits, notice periods and payroll dates, taken from the country's official sources and dated. A page without them stays unpublished.</td></tr>
<tr><td><b>Only countries Paybooks serves</b></td><td>A country goes live only when Paybooks can employ there. Every page states what Paybooks does in that country.</td></tr>
<tr><td><b>Launch in batches</b></td><td>Wave 1 countries first. The next batch ships once the first is indexed and ranking.</td></tr>
<tr><td><b>Links in three directions</b></td><td>Down from the hub to each country, across between a country's pages, and up from every page to the hub and the quote form.</td></tr>
<tr><td><b>Built for AI answers</b></td><td>A short answer at the top of each page, question headings, tables and FAQ markup, so answer engines can quote Paybooks.</td></tr>
<tr><td><b>Refreshed every year</b></td><td>Rates, thresholds and holidays updated each year, with the review date shown on the page.</td></tr>
</tbody></table></div></section>

<section id="india"><span class="num">07 · INDIA DEEP DIVE</span><h2>India: the first country cluster, already researched.</h2>
<p class="lead">India is where Paybooks has run payroll since 2012, so its cluster goes furthest: 50 pages, including 15 “hire [role] in India” pages and an India salary guide. The research, page-one analysis, competitor topics and the verdict on every existing page are in the deep dive.</p>
<div class="two"><div class="card acc"><b>India deep dive</b><p>Search results, competitor topics, the 50-page India plan and what to refresh or merge. <a href="india/">Open the India deep dive →</a></p></div>
<div class="card acc"><b>Country page sample</b><p>Employer of Record India, the depth every country page follows. <a href="../employer-of-record/india/">Open the India country page →</a></p></div></div></section>

<section id="appendix" class="appx"><span class="num">APPENDIX · THE EVIDENCE</span><h2>Everything behind the numbers.</h2>
<details><summary>Every measured keyword, by group</summary><div class="in">{"".join(f'<h4 class="subh" style="font-size:16px">{E(lab)} · {fmt(v)} a month</h4><div class="tw"><table><thead><tr><th>Keyword</th><th class="n">Searches / mo</th><th class="n">KD</th><th>Market</th></tr></thead><tbody>' + "".join(f'<tr><td>{E(k["keyword"])}</td><td class="n">{fmt(k["volume"])}</td><td class="n">{k["kd"] or "–"}</td><td>{"Google USA" if k["market"]=="us" else "Google India"}</td></tr>' for k in sorted(D["buckets"][key], key=lambda k: -k["volume"])) + '</tbody></table></div>' for (lab, v, _), key in zip(GROUPS, ["core", "country", "india", "best", "what", "compare"]))}</div></details>
<details><summary>Method and sources</summary><div class="in"><div class="tw"><table><tbody>
<tr><td><b>Keyword demand</b></td><td>Ahrefs Keywords Explorer, {NKW} Employer of Record keywords, Google USA and Google India, 23 September 2026.</td></tr>
<tr><td><b>Competitor footprint</b></td><td>Sitemaps of 13 EOR providers fetched in full, about 131,000 URLs. English pages only; each URL sorted by template (country page, country guide, contractor page, role page).</td></tr>
<tr><td><b>Paybooks audit</b></td><td>Every Employer of Record page on paybooks.in fetched and measured, 24 September 2026; rankings from Ahrefs.</td></tr>
</tbody></table></div></div></details></section>
</main><footer><div class="wrap">Prepared by Mohan Kumar Allada for the TransPerfect Paybooks SEO proposal · September 2026 · Data: Ahrefs, competitor sitemaps, live page measurement</div></footer>
<script>(function(){{var L=[].slice.call(document.querySelectorAll('.toc a'));var S=L.map(function(a){{return document.querySelector(a.getAttribute('href'))}});function f(){{var y=window.scrollY+window.innerHeight*0.35,k=0;S.forEach(function(e,i){{if(e&&e.offsetTop<=y)k=i}});L.forEach(function(a,i){{a.classList.toggle('on',i===k)}})}}window.addEventListener('scroll',f,{{passive:true}});f()}})();</script><script src="../assets/protect.js" defer></script>
</body></html>'''
open(f"{H}/out/index.html", "w", encoding="utf-8").write(PAGE)
print(json.dumps(json.load(open(f"{H}/global_numbers.json"))))
