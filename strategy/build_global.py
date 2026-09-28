"""Global Employer of Record strategy (Category 1), aligned to Paybooks' Website Strategy Alignment Deck (Aug 2026).
Writes out/index.html. Data: global_demand.json (Ahrefs, 161 EOR keywords), global_footprint.json and
global_locales.json (competitor sitemaps), paybooks_phases.json (the deck's 42-country list), issues.json, inventory.py."""
import os, re, json, html
H = os.path.dirname(os.path.abspath(__file__)); E = html.escape
fmt = lambda n: f"{n:,}"
D = json.load(open(f"{H}/global_demand.json")); F = json.load(open(f"{H}/global_footprint.json"))
L = json.load(open(f"{H}/global_locales.json")); PH = json.load(open(f"{H}/paybooks_phases.json"))
ISS = json.load(open(f"{H}/issues.json"))
inv = {"__file__": f"{H}/inventory.py"}; exec(open(f"{H}/inventory.py").read(), inv)
INV, PGW = inv["INV"], inv["W"]; EOR_WORDS = sum(PGW(u) for u, *_ in INV)
CSS = re.search(r'CSS = """(.*?)"""', open(f"{H}/build_ceo.py").read(), re.S).group(1)

BT = D["bucket_totals"]; TOTAL = sum(BT.values()); NKW = sum(len(v) for v in D["buckets"].values())
VOL = {c["country"]: c["volume"] for c in D["countries"]}; VOL["India"] = BT["india"]
A, B, C = PH["6A"], PH["6B"], PH["6C"]; ALL42 = A + B + C; assert len(ALL42) == 42
phase_of = {c: "6A" for c in A} | {c: "6B" for c in B} | {c: "6C" for c in C}
VA, VB, VC = (sum(VOL.get(c, 0) for c in X) for X in (A, B, C))
MEAS42 = [c for c in ALL42 if c in VOL]; NOT42 = [c for c in VOL if c not in ALL42]
NOT42V = sum(VOL[c] for c in NOT42)
CORE_V = BT["core"] + BT["best"] + BT["what"] + BT["compare"]
assert CORE_V + VA + VB + VC + NOT42V == TOTAL, (CORE_V, VA, VB, VC, NOT42V, TOTAL)
CTRY = [c for c in D["countries"] if "(region)" not in c["country"]]

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

# ---------- chart: country demand, colored by Paybooks phase ----------
PCOL = {"6A": "#4F8A10", "6B": "#8FB35E", "6C": "#C9DDB3", None: "#C9CED6"}
cm = max(c["volume"] for c in CTRY); cr = []
for i, c in enumerate(CTRY):
    col = PCOL[phase_of.get(c["country"])]; x0 = 0 if i < 13 else 500; yy = (i if i < 13 else i - 13) * 34
    w = max(4, 250 * c["volume"] / cm)
    cr.append(f'<text x="{x0}" y="{yy+18}" class="lb">{E(c["country"])}</text><rect x="{x0+170}" y="{yy+5}" width="{w:.0f}" height="20" rx="5" fill="{col}"/>'
              f'<text x="{x0+170+w+8:.0f}" y="{yy+20}" class="vl">{fmt(c["volume"])}</text>')
chart_ctry = f'<svg viewBox="0 0 980 {13*34}" class="chart" role="img" aria-label="Employer of record searches by country">{"".join(cr)}</svg>'

# ---------- competitor footprint: Paybooks' named EOR competitors first ----------
NAMED = [("deel.com", "Deel"), ("remote.com", "Remote"), ("g-p.com", "G-P"), ("usemultiplier.com", "Multiplier"), ("papayaglobal.com", "Papaya Global"),
         ("oysterhr.com", "Oyster"), ("rippling.com", "Rippling"), ("wisemonk.io", "Wisemonk")]
OTHER = [("skuad.io", "Skuad"), ("playroll.com", "Playroll"), ("velocityglobal.com", "Velocity Global"), ("asanify.com", "Asanify")]
fam = F["families"]; cov = F["country_coverage"]
def guides(d): return sum(v for k, v in fam.get(d, {}).items() if k in ("Country x topic", "Country payroll page", "Country cost page", "Country PEO page"))
def tail(d):
    f = fam.get(d, {}); parts = []
    if f.get("Role pages"): parts.append(f'{f["Role pages"]} role pages')
    if f.get("Country hiring (contractors)"): parts.append(f'{f["Country hiring (contractors)"]} contractor pages')
    if f.get("India role and city pages"): parts.append(f'{f["India role and city pages"]} India role and city pages')
    return ", ".join(parts) or "–"
def langs(d):
    ls = [x for x in L[d]["languages"] if x != "lp"]; return ls
cmx = max(cov.values())
def frow(d, name, cls=""):
    n = cov.get(d, 0); ls = langs(d)
    return (f'<tr class="{cls}"><td><b>{name}</b></td><td><div style="display:flex;align-items:center;gap:10px"><span style="display:inline-block;height:10px;border-radius:5px;background:#4F8A10;width:{120*n/cmx:.0f}px"></span><b>{n if n else "1 (India)" if d=="wisemonk.io" else n}</b></div></td>'
            f'<td class="n">{fmt(guides(d)) if guides(d) else "–"}</td><td>{tail(d)}</td><td>{"<b>" + str(len(ls)) + "</b>: " + ", ".join(ls) if ls else "English only"}</td></tr>')
frows = "".join(frow(d, n) for d, n in NAMED) + "".join(frow(d, n, "mut") for d, n in OTHER)
frows += '<tr class="me"><td><b>Paybooks today</b></td><td><b>1</b> (India)</td><td class="n">–</td><td>–</td><td>English only</td></tr>'
NLANG = {n: len(langs(d)) for d, n in NAMED}; ENONLY = [n for d, n in NAMED + OTHER if not langs(d)]
DEEP = sorted([guides(d) for d, _ in NAMED + OTHER if guides(d) >= 700])

# ---------- languages: which named competitors publish each ----------
LANGPLAN = [("German", ["Germany", "Austria", "Switzerland"]), ("French", ["France", "Belgium", "Switzerland", "Canada"]),
            ("Spanish", ["Spain", "Mexico", "Argentina", "Colombia", "Costa Rica", "Dominican Republic"]), ("Portuguese", ["Brazil", "Portugal"]),
            ("Japanese", ["Japan"]), ("Korean", ["South Korea"]), ("Dutch", ["Netherlands", "Belgium"]), ("Italian", ["Italy"]),
            ("Swedish", ["Sweden"]), ("Danish", ["Denmark"]), ("Chinese", ["China", "Hong Kong"]), ("Arabic", ["UAE", "Saudi Arabia"]), ("Thai", ["Thailand"]), ("Turkish", ["Turkey"])]
def pubs(lang): return [n for d, n in NAMED + OTHER if lang in langs(d) or (lang == "Chinese" and any(x.startswith("Chinese") for x in langs(d)))]
lrows = ""
for i, (lang, mk) in enumerate(LANGPLAN):
    p = pubs(lang); wave = "Wave 1" if i < 5 else "Wave 2"
    lrows += f'<tr><td><b>{lang}</b></td><td>{", ".join(mk)}</td><td>{", ".join(p) if p else "none of them"}</td><td>{wave}</td></tr>'
LW1 = [l for l, _ in LANGPLAN[:5]]

# ---------- plan numbers ----------
MODULES = 13; TOOLS = 3
RES = ["What an employer of record is", "EOR vs PEO", "EOR vs setting up an entity", "Best EOR providers, with published prices"] + [f"Paybooks vs {n}" for _, n in NAMED]
GLOSS = 100
GUIDES = ["Hiring guide (planned)", "Employer cost", "Payroll and taxes", "Benefits", "Leave and holidays", "Termination and severance", "Work permits and visas", "Minimum wage and salaries"]
TOPICS = len(GUIDES) - 1
ROLES = ["Software developers", "Sales representatives", "Customer support", "Accountants", "Data analysts"]
INDIA = 50  # the India cluster from the deep dive, EOR page and hiring guide included
A_OTHER = [c for c in A if c != "India"]
PER_DEPTH = 2 + TOPICS + len(ROLES)  # EOR page, hiring guide, guide topics, role pages
W1 = 1 + MODULES + TOOLS + len(RES) + INDIA
W2 = len(A_OTHER) * PER_DEPTH + 1  # + the United States payroll country page in the alignment deck
W3 = (len(B) + len(C)) * 2
W4 = 0
TOTALP = W1 + W2 + W3
LOC_BASE = 1 + MODULES + 42 * 2; LOC = LOC_BASE * len(LW1)
json.dump({"total_searches": TOTAL, "keywords": NKW, "core": CORE_V, "country": BT["country"], "india": BT["india"], "n_countries": len(CTRY),
           "v6a": VA, "v6b": VB, "v6c": VC, "w1": W1, "w2": W2, "w3": W3, "total_pages": TOTALP, "per_depth": PER_DEPTH, "glossary": GLOSS,
           "localized": LOC, "languages_wave1": LW1, "deel_langs": NLANG["Deel"], "remote_langs": NLANG["Remote"], "gp_langs": NLANG["G-P"],
           "english_only": ENONLY, "cov_min": min(cov[d] for d, _ in NAMED if cov.get(d, 0) >= 100), "cov_max": cmx}, open(f"{H}/global_numbers.json", "w"), indent=1)


# ---------- what works for each competitor ----------
SERPL = json.load(open(f"{H}/ahrefs_serp_links.json")); SERPS = json.load(open(f"{H}/serps.json")); DR = json.load(open(f"{H}/ahrefs_data.json"))["dr"]
ct = {"__file__": f"{H}/comp_topics.py"}; exec(open(f"{H}/comp_topics.py").read(), ct); REL, TOPN = ct["REL"], ct["TOPN"]
def dom(u): return re.sub(r"^www\.", "", u.split("/")[2])
def kind(u):
    u = u.lower()
    if "glossary" in u: return "Glossary entry"
    if "/blog/" in u or "/articles" in u or "resources" in u: return "Explainer article"
    if "wikipedia" in u: return "Encyclopedia"
    if "youtube" in u: return "Video"
    return "Product or country page"
def serp_rows(q, src, n=10):
    seen, out = set(), []
    for r in src[q]:
        u = r.get("url")
        if not u or "organic" not in (r.get("type") or []) or u in seen: continue
        seen.add(u); out.append(r)
    return "".join(f'<tr><td class="n">#{r["position"]}</td><td>{E(dom(r["url"]))}</td><td>{kind(r["url"])}</td><td class="n">{int(r["domain_rating"]) if r.get("domain_rating") else "–"}</td><td class="n">{fmt(int(r["traffic"])) if r.get("traffic") else "–"}</td></tr>' for r in out[:n])
head_rows = serp_rows("employer of record|us", SERPL); peo_rows = serp_rows("eor vs peo|us", SERPS, 6)
AIO = [dom(r["url"]) for r in SERPL["employer of record|us"] if r.get("url") and "ai_overview_sitelink" in (r.get("type") or [])]
import collections
per = collections.defaultdict(collections.Counter)
for r in REL: per[r["d"]][TOPN[r["t"]][1]] += r["us"] + r["in"]
def invest(d):
    f = fam.get(d, {}); parts = []
    if cov.get(d): parts.append(f'{cov[d]} country pages')
    if guides(d): parts.append(f'{fmt(guides(d))} country guides')
    if f.get("Role pages"): parts.append(f'{f["Role pages"]} role pages')
    if f.get("Country hiring (contractors)"): parts.append(f'{f["Country hiring (contractors)"]} contractor pages')
    if f.get("India role and city pages"): parts.append(f'{f["India role and city pages"]} India role and city pages')
    if f.get("Glossary"): parts.append(f'{f["Glossary"]}-term glossary')
    if f.get("Comparison pages"): parts.append(f'{f["Comparison pages"]} comparison pages')
    return ", ".join(parts) or "–"
def wins(d):
    c = per.get(d)
    if not c: return "no India page with measured traffic", 0
    return "; ".join(f"{t} ({fmt(v)})" for t, v in c.most_common(3)), sum(c.values())
def crow(d, name, cls=""):
    w, tot = wins(d)
    return f'<tr class="{cls}"><td><b>{name}</b></td><td class="n">{int(DR[d]["domain_rating"]) if d in DR else "–"}</td><td>{invest(d)}</td><td>{w}</td><td class="n">{fmt(tot) if tot else "–"}</td></tr>'
crows = "".join(crow(d, n) for d, n in NAMED) + "".join(crow(d, n, "mut") for d, n in OTHER)
TOPWIN = collections.Counter()
for d in per: 
    for t, v in per[d].items(): TOPWIN[t] += v
topwin = ", ".join(f"{t} ({fmt(v)})" for t, v in TOPWIN.most_common(6))

# ---------- topics and keywords ----------
TP = json.load(open(f"{H}/global_topics.json"))
TWAVE = {"Country EOR pages": "Waves 2 and 3", "Core EOR service": "Wave 1", "India: hire employees and roles": "Wave 1", "India: EOR page": "Wave 1", "Best EOR providers": "Wave 1", "Global EOR service": "Wave 1", "What an EOR is": "Wave 1", "EOR vs PEO and staffing": "Wave 1", "EOR cost and pricing": "Wave 1", "EOR payroll services": "Wave 1"}
trows = "".join(f'<tr><td><b>{E(t["topic"])}</b></td><td><code>{E(t["page"])}</code></td><td>{", ".join(E(k) for k, _ in t["top"][:3])}</td><td class="n">{t["n"]}</td><td class="n">{fmt(t["volume"])}</td><td class="n">{t["kd_min"]}–{t["kd_max"]}</td><td>{TWAVE[t["topic"]]}</td></tr>' for t in TP)
NTOP = len(TP); KDLOW = sum(1 for k in [x for v in D["buckets"].values() for x in v] if k["kd"] not in ("", None) and int(float(k["kd"])) <= 15)

SEVC = {"High": "#C2410C", "Medium": "#8A94A0"}
iss_rows = "".join(f'<tr><td class="n">{k}</td><td><span class="vt" style="--c:{SEVC.get(sv, "#8A94A0")}">{sv}</span><div><b>{E(t)}</b></div></td><td class="mut">{E(ev)}</td><td>{E(fx)}</td></tr>' for k, (sv, t, ev, fx) in enumerate(ISS, 1))
tier = lambda n, t, url, body, tag, ex="": (f'<div class="tier"><div class="tn">{n}</div><div><b>{t}</b><code>{url}</code><span class="tg {"pl" if tag=="In the plan" else "ad"}">{tag}</span><p>{body}</p>'
                                          + (f'<p class="mut">{ex}</p>' if ex else "") + '</div></div>')
ARCH = "".join([
  tier("1", "Employer of Record product home and 13 modules", "/employer-of-record/ · /employer-of-record/[module]/", "The product pillar as planned: onboarding, payroll setup and processing, compliance, money movement, lifecycle, engagement, benefits, helpdesk, time and attendance, leave, self-service, immigration and visas.", "In the plan", "Sample built: the landing page in this proposal is the product home."),
  tier("2", "A page per country, for 42 countries", "/countries/[country]/employer-of-record/ · /countries/[country]/hiring-guide/", "The country layer as planned: an EOR product page and a hiring guide for each of the 42 countries, in phases 6A, 6B and 6C. India is the expanded hub.", "In the plan", "Sample built: the India country page, the depth every country page follows."),
  tier("3", "Tools and resources", "/tools/ · /resources/glossary/ · /resources/comparisons/", "The three calculators, the glossary, comparisons and guides as planned. Search sets the comparison list: Paybooks vs each of the eight named EOR competitors, plus EOR vs PEO and EOR vs an entity.", "In the plan"),
  tier("4", "Guide topics under each country", "/countries/[country]/hiring-guide/[topic]/", f"One hiring guide per country is planned. Search splits it into {TOPICS} topic pages per country, India first, then Phase 6A: " + ", ".join(g.lower() for g in GUIDES[1:]) + ". Each answers a question buyers search on its own.", "Added by search", f"The leaders run {min(DEEP):,} to {max(DEEP):,} of these pages each."),
  tier("5", "Role × country pages", "/countries/[country]/hire/[role]/", "“Hire a software developer in Poland.” One template filled with the country's salary band, all-in cost and notice rules, for five roles per country, India first, then Phase 6A.", "Added by search", "India alone carries 16,350 searches a month across 15 roles (India deep dive)."),
  tier("6", "The buyer's language", "/de/ · /fr/ · /es/ · /pt/ · /ja/", "The same product, country and guide pages in the languages of the buyer markets on the 42-country list. Section 07.", "Added by search"),
])

PAGE = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Global EOR Strategy</title><meta name="robots" content="noindex,nofollow">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><style>{CSS}
.tiers{{display:grid;gap:10px}}.tier{{display:grid;grid-template-columns:44px 1fr;gap:16px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px}}
.tn{{width:36px;height:36px;border-radius:10px;background:var(--forest);color:var(--lime);font:600 17px/36px "Instrument Sans";text-align:center}}
.tier b{{font:600 18px "Instrument Sans";margin-right:10px}}.tier p{{margin:6px 0 0;font-size:15px;color:var(--ink2)}}.tier .mut{{font-size:13.5px}}.tier>div{{min-width:0}}.tier code{{overflow-wrap:anywhere;display:inline-block;max-width:100%;margin-right:8px}}
.tg{{display:inline-block;font:700 11px Inter;border-radius:999px;padding:3px 9px;vertical-align:2px}}.tg.pl{{background:var(--g100);color:var(--g600)}}.tg.ad{{background:var(--o100);color:#B4530F}}
tr.mut td{{color:var(--muted)}}.plan td b{{font-family:"Instrument Sans"}}
@media(max-width:560px){{.tier{{grid-template-columns:1fr;gap:10px}}}}
</style></head><body>
<header class="hero"><div class="wrap"><span class="eyebrow">Employer of Record · Search strategy · Paybooks</span>
<h1>Category 1: <em>Employer of Record (EOR)</em></h1>
<p class="sub">A company anywhere hires people anywhere, with no entity in that country. Paybooks' website plan already has the winning shape: 42 countries, a page per country, product modules and tools. This is what search adds on top: depth under every country, the long tail of roles, and the buyer's own language.</p>
<div class="kp"><div><b>{fmt(TOTAL)}</b><span>monthly searches measured across {NKW} EOR keywords, Google USA and India</span></div><div><b>42</b><span>countries in Paybooks' plan. Phase 6A alone holds {fmt(VA)} of the measured searches</span></div>
<div><b>{NLANG["Deel"]}</b><span>languages Deel publishes in. {len(ENONLY)} of the 12 competitors studied are English-only</span></div><div><b>{fmt(TOTALP)}</b><span>pages in three waves: India first, then 41 countries, plus {fmt(LOC)} localized pages in {len(LW1)} languages</span></div></div></div></header>
<nav class="toc" aria-label="Sections"><a href="#answer" aria-label="Findings"><span>Findings</span></a><a href="#demand" aria-label="Demand"><span>Demand</span></a><a href="#leaders" aria-label="What leaders built"><span>What leaders built</span></a><a href="#works" aria-label="What works"><span>What works</span></a><a href="#today" aria-label="Paybooks today"><span>Paybooks today</span></a><a href="#topics" aria-label="Topics and keywords"><span>Topics and keywords</span></a><a href="#arch" aria-label="The site"><span>The site</span></a><a href="#intl" aria-label="International SEO"><span>International SEO</span></a><a href="#plan" aria-label="The plan"><span>The plan</span></a><a href="#pseo" aria-label="Rules"><span>Rules</span></a><a href="#india" aria-label="India deep dive"><span>India deep dive</span></a><a href="#appendix" aria-label="Evidence"><span>Evidence</span></a></nav>
<main class="wrap">
<section id="answer"><span class="num">FINDINGS</span><h2>Three findings decide the strategy.</h2>
<div class="take"><div><b>Buyers search by destination country.</b><p>“Employer of record [country]” searches add up to {fmt(BT["country"])} a month across {len(CTRY)} countries, almost as much as the core “employer of record” searches ({fmt(BT["core"])}). {len(MEAS42)} of Paybooks' 42 countries have measured demand, and Phase 6A carries {fmt(VA)} a month.</p></div>
<div><b>Leaders pair country pages with languages.</b><p>Of the eight EOR competitors Paybooks named, Deel publishes in {NLANG["Deel"]} languages, Remote in {NLANG["Remote"]} and G-P in {NLANG["G-P"]}, on top of 113 to 186 country pages each. {", ".join(ENONLY[:-1])} and {ENONLY[-1]} are English-only.</p></div>
<div><b>Paybooks' plan has the right shape.</b><p>The alignment deck's country layer, 42 countries with an EOR page and a hiring guide each, is the model the leaders win with. Search adds the depth under each country, the role pages, the comparison set, and the buyer's language, where TransPerfect's own localization business is an advantage no EOR competitor has.</p></div></div></section>

<section id="demand"><span class="num">01 · DEMAND</span><h2>{fmt(TOTAL)} monthly searches, and country searches are a third of them.</h2>
<p class="lead">Grouped by what the searcher wants. The dark-green groups ship first. This is a floor: it counts only the {NKW} keywords measured, before country guides, role pages and other languages.</p>
<div class="panel">{chart_demand}</div>
<h3 class="subh">“Employer of record [country]”: searches by country, colored by Paybooks' phase</h3>
<div class="panel">{chart_ctry}<div class="legend"><span style="--c:#4F8A10">Phase 6A · {fmt(VA)} a month with India</span><span style="--c:#8FB35E">Phase 6B · {fmt(VB)}</span><span style="--c:#C9DDB3">Phase 6C · {fmt(VC)}</span><span style="--c:#C9CED6">Not on the 42-country list · {fmt(NOT42V)}</span></div></div>
<p class="note">Ahrefs Keywords Explorer, Google USA, 23 September 2026. {", ".join(c for c in NOT42 if "(region)" not in c)} have measured demand but are not on the list: candidates for a later phase. {len(ALL42)-len(MEAS42)} listed countries did not appear in the sample; their searches are sized in the next data pull.</p></section>

<section id="leaders"><span class="num">02 · WHAT LEADERS BUILT</span><h2>Country pages are the product. Languages are the reach.</h2>
<p class="lead">Every competitor's sitemap was fetched and each URL sorted by template and language. Paybooks' eight named EOR competitors are listed first; four more global EOR sites follow in grey.</p>
<div class="tw"><table><thead><tr><th>Competitor</th><th>Countries with a page</th><th class="n">Country guides</th><th>Long tail</th><th>Languages</th></tr></thead><tbody>{frows}</tbody></table></div>
<p class="note">English pages counted for country and guide totals; language versions from each site's locale folders (20 or more pages each). “Country guides” counts pages such as payroll, benefits, costs and work permits under a country. Source: competitor sitemaps, about 131,000 URLs across 13 sites, September 2026.</p></section>


<section id="works"><span class="num">03 · WHAT WORKS FOR EACH COMPETITOR</span><h2>Explainers win the head term. Country pages win the rest.</h2>
<p class="lead">Two views. First, who holds page one for “employer of record” in Google USA today, and with what kind of page. Second, where each named competitor invests its pages and which topics earn it measured visits.</p>
<h3 class="subh">Page one for “employer of record”, Google USA</h3>
<div class="tw"><table><thead><tr><th class="n">Rank</th><th>Site</th><th>Kind of page</th><th class="n">DR</th><th class="n">Visits / mo to the page</th></tr></thead><tbody>{head_rows}</tbody></table></div>
<div class="callout"><b>Read it</b><p>Explainer articles and glossary entries hold the head term; the first product page appears at #10. A DR 57 blog sits on page one, so authority is not the barrier. The AI Overview cites {", ".join(AIO)}. Paybooks needs a definitive explainer and glossary entry for the head term, and the product home for the commercial variants (“EOR services”, “employer of record services”).</p></div>
<h3 class="subh">Page one for “EOR vs PEO”, Google USA</h3>
<div class="tw"><table><thead><tr><th class="n">Rank</th><th>Site</th><th>Kind of page</th><th class="n">DR</th><th class="n">Visits / mo to the page</th></tr></thead><tbody>{peo_rows}</tbody></table></div>
<h3 class="subh">Where each competitor invests, and what earns it visits</h3>
<div class="tw"><table><thead><tr><th>Competitor</th><th class="n">DR</th><th>Where the pages are (sitemap)</th><th>Topics earning measured visits (India sample)</th><th class="n">Visits / mo</th></tr></thead><tbody>{crows}</tbody></table></div>
<p class="note">Sitemap families from about 131,000 URLs. Measured visits are Ahrefs estimates for each site's top India pages in Google USA and India, September 2026: the one market where topic-level traffic has been pulled. Across all competitors the topics earning the most measured visits are {topwin}. Topic-level traffic for the other 41 countries is pulled in the next Ahrefs cycle (21 October) or sooner through Semrush.</p></section>

<section id="today"><span class="num">04 · PAYBOOKS TODAY</span><h2>One country, fourteen pages, one keyword.</h2>
<p class="lead">Paybooks' Employer of Record content covers India only: {len(INV)} pages and about {fmt(EOR_WORDS)} words, ranking for one keyword. The faults below are fixed in the India country cluster, and the new site starts clean everywhere else.</p>
<div class="big3"><div><b>1</b><span>country with an EOR page today</span></div><div><b>{len(INV)}</b><span>EOR pages, all about India</span></div><div class="bad"><b>1</b><span>keyword ranking, “eor solutions” at #8 in India</span></div></div>
<details class="blk"><summary>{len(ISS)} issues on the current pages, most damaging first</summary><div class="tw"><table><thead><tr><th class="n">#</th><th>Issue</th><th>Evidence</th><th>Fix in the plan</th></tr></thead><tbody>{iss_rows}</tbody></table></div></details>
<p class="note">Checked on the live pages, 24 September 2026. Rankings from Ahrefs.</p></section>


<section id="topics"><span class="num">05 · TOPICS AND KEYWORDS</span><h2>{NTOP} topics, {NKW} keywords, one target page each.</h2>
<p class="lead">Every measured keyword is grouped by the search it stands for and mapped to the page that answers it on the new site. {KDLOW} of the {NKW} keywords have a difficulty of 15 or less. The full list, keyword by keyword, is in the appendix.</p>
<div class="tw"><table><thead><tr><th>Topic</th><th>Target page</th><th>Top keywords</th><th class="n">Keywords</th><th class="n">Searches / mo</th><th class="n">KD</th><th>Wave</th></tr></thead><tbody>{trows}</tbody></table></div>
<p class="note">Searches: Ahrefs, Google USA; India rows also include Google India. Country pages: one keyword group per country, 41 keywords across 26 countries. Guide topics, role pages and the other languages are sized in the next data pull.</p></section>

<section id="arch"><span class="num">06 · THE SITE</span><h2>The plan as agreed, and what search adds to it.</h2>
<p class="lead">Six layers on paybooks.transperfect.com. Three are already in the alignment deck; three are added by this strategy. Links run down from the product home to every country, across between a country's pages, and back up.</p>
<div class="tiers">{ARCH}</div></section>

<section id="intl"><span class="num">07 · INTERNATIONAL SEO</span><h2>Every EOR search has two countries in it.</h2>
<p class="lead">The buyer sits in one country and hires in another. A German company hiring in Poland searches “Employer of Record Polen”, in German. English pages win the English-speaking buyer markets; the buyer markets on the 42-country list that search in their own language need the same pages in that language.</p>
<div class="two"><div class="card acc"><b>English first, then the buyer's language</b><p>Launch in English on paybooks.transperfect.com. Then add the product home, the 13 modules and the 42 country EOR pages and hiring guides in five languages: {", ".join(LW1)}. That is {fmt(LOC_BASE)} pages per language, {fmt(LOC)} in all, each a real translation reviewed in-market.</p></div>
<div class="card acc"><b>The advantage no competitor has</b><p>TransPerfect's business is translation and localization: GlobalLink and translation in 200+ languages for 90% of the Fortune 500. Deel, Remote and G-P pay for their {NLANG["Deel"]}, {NLANG["Remote"]} and {NLANG["G-P"]} languages. Paybooks can localize faster, better and in-house.</p></div></div>
<h3 class="subh">Language plan, matched to Paybooks' 42 countries</h3>
<div class="tw"><table><thead><tr><th>Language</th><th>Buyer markets on the 42-country list</th><th>Competitors already publishing in it</th><th>Wave</th></tr></thead><tbody>{lrows}</tbody></table></div>
<p class="note">Language wave 1 follows Phase 6A and 6B; wave 2 follows demand once each language's searches are sized (Ahrefs, next data pull). Chinese covers Simplified and Traditional; Arabic and Thai follow the Phase 6C markets.</p>
<h3 class="subh">Technical rules for every language</h3>
<div class="tw"><table><tbody>
<tr><td><b>Folders, not domains</b></td><td>One site, one authority: paybooks.transperfect.com/de/, /fr/, /es/, /pt/, /ja/. No separate country domains to build from zero.</td></tr>
<tr><td><b>hreflang on every page pair</b></td><td>Each page lists every language version of itself, plus x-default pointing to English. Only for pages that exist in that language.</td></tr>
<tr><td><b>Translated slugs and metadata</b></td><td>URLs, titles, descriptions and headings in the language, not English slugs with translated text.</td></tr>
<tr><td><b>Local currency and dates in tools</b></td><td>Calculators and cost tables show euros, yen or reais and local date formats, with the exchange date shown.</td></tr>
<tr><td><b>No redirects by location</b></td><td>Visitors and search engines choose the language; a language switcher on every page, no automatic redirects by IP.</td></tr>
<tr><td><b>Measured per language</b></td><td>A Search Console view per language folder, and rankings tracked in each market's Google, plus Naver for Korea.</td></tr>
<tr><td><b>Not built: English copies per region</b></td><td>en-gb, en-au or en-sg versions duplicate the same page. One English page serves every English-speaking buyer until content differs, such as local pricing.</td></tr>
</tbody></table></div></section>

<section id="plan"><span class="num">08 · THE PLAN</span><h2>India first, in full. Then 41 countries.</h2>
<p class="lead">Wave 1 makes India the proof: the one country that carries every Paybooks product, built to full depth. Waves 2 and 3 roll the same templates out across Paybooks' phases, in order of measured searches. The languages follow.</p>
<div class="tw plan"><table><thead><tr><th>Wave</th><th>What ships</th><th class="n">Pages</th><th class="n">Measured searches / mo</th></tr></thead><tbody>
<tr><td><b>Wave 1 · India, in full</b><br><span class="mut">Launch</span></td><td>The Employer of Record product home and {MODULES} modules · {TOOLS} tools · {len(RES)} resource pages: what an EOR is, EOR vs PEO, EOR vs an entity, best providers, Paybooks vs each of the eight named competitors · a {GLOSS}-term glossary in batches · the full India cluster of {INDIA} pages: the India EOR page, hiring guide, {TOPICS} guide topics, 15 role pages and the salary guide · alongside the India pages of the other three categories, planned in their own strategies</td><td class="n"><b>{W1}</b> + {GLOSS}</td><td class="n"><b>{fmt(CORE_V + BT["india"])}</b></td></tr>
<tr><td><b>Wave 2 · Phase 6A</b></td><td>{len(A_OTHER)} countries, {PER_DEPTH} pages each, the India depth repeated: EOR page, hiring guide, {TOPICS} guide topics and {len(ROLES)} role pages for {", ".join(A_OTHER)} · the United States payroll country page</td><td class="n"><b>{W2}</b></td><td class="n"><b>{fmt(VA - BT["india"])}</b></td></tr>
<tr><td><b>Wave 3 · Phases 6B and 6C</b></td><td>EOR page and hiring guide for the other {len(B)+len(C)} countries, in order of measured searches; guide topics and role pages added where demand shows</td><td class="n"><b>{W3}</b></td><td class="n"><b>{fmt(VB+VC)}</b></td></tr>
<tr><td><b>Languages</b></td><td>Product home, modules, country EOR pages and hiring guides in {", ".join(LW1)}</td><td class="n"><b>{fmt(LOC)}</b></td><td class="n">Sized in the next data pull</td></tr>
<tr class="me"><td><b>Total</b></td><td>42 countries in English, {len(LW1)} more languages</td><td class="n"><b>{fmt(TOTALP)}</b> + {GLOSS} + {fmt(LOC)}</td><td class="n"><b>{fmt(CORE_V+VA+VB+VC)}</b></td></tr>
</tbody></table></div>
<div class="callout"><b>4 categories</b><p>The aim is to lead all four categories, not one. India in Wave 1 is where all four meet: Employer of Record, Multi-Country Payroll, India Managed Office and HCM on one country hub. The country layer built here serves Multi-Country Payroll as well, so every country added for EOR is a country page ready for payroll.</p></div>
<p class="note">Measured searches are from the {NKW}-keyword sample; India's role and salary searches are counted in the India deep dive. {fmt(NOT42V)} a month for countries and regions off the list are not assigned. Roles: {", ".join(r.lower() for r in ROLES)}.</p></section>

<section id="pseo"><span class="num">09 · RULES</span><h2>Hundreds of pages, none of them thin.</h2>
<p class="lead">Templates make the scale possible. These rules keep every page worth ranking, in every language.</p>
<div class="tw"><table><tbody>
<tr><td><b>Real data on every page</b></td><td>Each country page carries its own employer costs, contract rules, benefits, notice periods and payroll dates, taken from the country's official sources and dated. A page without them stays unpublished.</td></tr>
<tr><td><b>Only countries Paybooks serves</b></td><td>A country goes live only when Paybooks can employ there. Every page states what Paybooks does in that country.</td></tr>
<tr><td><b>Launch in batches</b></td><td>India first, then Phase 6A countries in order of measured searches. The next batch ships once the first is indexed and ranking.</td></tr>
<tr><td><b>Links in three directions</b></td><td>Down from the product home to each country, across between a country's pages, and up from every page to the product home and the quote form.</td></tr>
<tr><td><b>Translated by people, checked in-market</b></td><td>No machine translation published unreviewed. A language goes live page by page, with hreflang added only when the page exists in that language.</td></tr>
<tr><td><b>Built for AI answers</b></td><td>A short answer at the top of each page, question headings, tables and FAQ markup, so answer engines can quote Paybooks in every language.</td></tr>
<tr><td><b>Refreshed every year</b></td><td>Rates, thresholds and holidays updated each year, with the review date shown on the page.</td></tr>
</tbody></table></div></section>

<section id="india"><span class="num">10 · INDIA DEEP DIVE</span><h2>India: Wave 1, already researched.</h2>
<p class="lead">India is the one country that carries all three products and where Paybooks has run payroll since 2012, so its cluster goes furthest: 50 pages, including 15 “hire [role] in India” pages and an India salary guide. The research, page-one analysis, competitor topics and the verdict on every existing page are in the deep dive.</p>
<div class="two"><div class="card acc"><b>India deep dive</b><p>Search results, competitor topics, the 50-page India plan and what to refresh or merge. <a href="india/">Open the India deep dive →</a></p></div>
<div class="card acc"><b>Country page sample</b><p>Employer of Record India, the depth every country page follows. <a href="../employer-of-record/india/">Open the India country page →</a></p></div></div></section>

<section id="appendix" class="appx"><span class="num">APPENDIX · THE EVIDENCE</span><h2>Everything behind the numbers.</h2>
<details><summary>Every measured keyword, by group</summary><div class="in">{"".join(f'<h4 class="subh" style="font-size:16px">{E(lab)} · {fmt(v)} a month</h4><div class="tw"><table><thead><tr><th>Keyword</th><th class="n">Searches / mo</th><th class="n">KD</th><th>Market</th></tr></thead><tbody>' + "".join(f'<tr><td>{E(k["keyword"])}</td><td class="n">{fmt(k["volume"])}</td><td class="n">{k["kd"] or "–"}</td><td>{"Google USA" if k["market"]=="us" else "Google India"}</td></tr>' for k in sorted(D["buckets"][key], key=lambda k: -k["volume"])) + '</tbody></table></div>' for (lab, v, _), key in zip(GROUPS, ["core", "country", "india", "best", "what", "compare"]))}</div></details>
<details><summary>Paybooks' 42 countries by phase</summary><div class="in"><div class="tw"><table><thead><tr><th>Phase</th><th>Countries</th><th class="n">Measured searches / mo</th></tr></thead><tbody>
<tr><td><b>6A</b></td><td>{", ".join(A)}</td><td class="n">{fmt(VA)}</td></tr><tr><td><b>6B</b></td><td>{", ".join(B)}</td><td class="n">{fmt(VB)}</td></tr><tr><td><b>6C</b></td><td>{", ".join(C)}</td><td class="n">{fmt(VC)}</td></tr>
</tbody></table></div><p class="note">Source: Website Strategy Alignment Deck, August 2026, appendix. Searches: Ahrefs, Google USA; India from Google USA and India.</p></div></details>
<details><summary>Method and sources</summary><div class="in"><div class="tw"><table><tbody>
<tr><td><b>Paybooks' plan</b></td><td>Website Strategy Alignment Deck (August 2026): information architecture, the 42-country list and phases, product modules, tools and the named competitors per category.</td></tr>
<tr><td><b>Keyword demand</b></td><td>Ahrefs Keywords Explorer, {NKW} Employer of Record keywords, Google USA and Google India, 23 September 2026.</td></tr>
<tr><td><b>Competitor footprint and languages</b></td><td>Sitemaps of 13 EOR providers fetched in full, about 131,000 URLs. Each URL sorted by template (country page, country guide, contractor page, role page) and by language folder.</td></tr>
<tr><td><b>Paybooks audit</b></td><td>Every Employer of Record page on paybooks.in fetched and measured, 24 September 2026; rankings from Ahrefs.</td></tr>
</tbody></table></div></div></details></section>
</main><footer><div class="wrap">Prepared by Mohan Kumar Allada for the TransPerfect Paybooks SEO proposal · September 2026 · Data: Paybooks' alignment deck, Ahrefs, competitor sitemaps, live page measurement</div></footer>
<script>(function(){{var L=[].slice.call(document.querySelectorAll('.toc a'));var S=L.map(function(a){{return document.querySelector(a.getAttribute('href'))}});function f(){{var y=window.scrollY+window.innerHeight*0.35,k=0;S.forEach(function(e,i){{if(e&&e.offsetTop<=y)k=i}});L.forEach(function(a,i){{a.classList.toggle('on',i===k)}})}}window.addEventListener('scroll',f,{{passive:true}});f()}})();</script><script src="../assets/protect.js" defer></script>
</body></html>'''
open(f"{H}/out/index.html", "w", encoding="utf-8").write(PAGE)
print(json.dumps(json.load(open(f"{H}/global_numbers.json"))))
