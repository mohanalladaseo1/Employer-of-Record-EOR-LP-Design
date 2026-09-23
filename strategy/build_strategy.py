"""Employer of Record India: competitor research and SERP strategy.
Inputs (all from this session's pulls, 23 to 24 Sep 2026):
  serps.json          Ahrefs SERP overview, 18 queries (6 returned live results)
  pages.json          page-one URLs opened and measured
  india_urls.json     competitor sitemaps, English India URLs, deduped later
  playbooks.json      India URL counts per competitor by topic
  comp_keywords.json  Ahrefs organic keywords (US, 'india') for Deel, Papaya, Skuad, Rippling
  keywords_clean.csv  the original Ahrefs keyword pull
"""
import json, csv, re, html, os, collections
H = os.path.dirname(os.path.abspath(__file__))
E = html.escape
def fmt(n): return f"{int(n):,}"
serps = json.load(open(f"{H}/serps.json"))
pages = json.load(open(f"{H}/pages.json"))
play = json.load(open(f"{H}/playbooks.json"))
compk = json.load(open(f"{H}/comp_keywords.json"))
SRC = "/Users/mohankumarallada/Claude_Code_Projects/TransPerfect Paybooks Proposal/research/keywords_clean.csv"
ours = [r for r in csv.DictReader(open(SRC, encoding="utf-8")) if r["category"] == "eor"]

# ---------- keyword universe: our EOR pull + competitor gap keywords ----------
KW = {}
def add(kw, ctry, vol, kd, src):
    kw = kw.strip().lower(); key = (kw, ctry)
    try: vol = int(float(vol or 0))
    except: vol = 0
    kd = None if kd in ("", None) else int(float(kd))
    if key in KW:
        KW[key]["vol"] = max(KW[key]["vol"], vol)
        if KW[key]["kd"] is None: KW[key]["kd"] = kd
        return
    KW[key] = dict(kw=kw, ctry=ctry, vol=vol, kd=kd, src=src)
for r in ours: add(r["keyword"], r["country"], r["volume"], r["kd"], "Ahrefs pull")
for dom, ks in compk.items():
    for k in ks:
        kw = k["keyword"].lower()
        if "indiana" in kw or re.search(r"moving to|move to|immigrate|nurse|medical assistant|laptop", kw): continue
        add(kw, "us", k["volume"], k.get("keyword_difficulty"), "competitor gap")

def has(k, p): return re.search(p, k) is not None
COUNTRY = r"philippines|france|\buk\b|australia|china|canada|singapore|germany|netherlands|vietnam|uae|switzerland|mexico|poland|slovakia|brazil|turkey|thailand|czech|\busa\b|portugal|luxembourg|south korea|guatemala|honduras|belgium|denmark|costa rica|middle east|\bgcc\b|mena|krakow"
def cluster(k):
    if has(k, r"news|\bior\b|^deel |^rippling |^papaya |immigrat|green card|work remotely for a us company|nanny"): return "X"
    if has(k, COUNTRY) and "india" not in k: return "C9"
    if has(k, r"developer|programmer|coder|engineer|seo expert|wordpress"): return "C5"
    if has(k, r"\bpeo\b|professional employer|staffing"): return "C3"
    if has(k, r"what is|what's an|meaning|pros and cons|how do .*work"): return "C7"
    if has(k, r"best way|best website|best platform"): return "C2"
    if has(k, r"best|top |most reliable|leading|which hr"): return "C4"
    if has(k, r"\bvs\b") and "entity" in k: return "C8"
    if has(k, r"start a business|open business|setting up (a )?(business|company)|company registration|company setup|register a company|start a company|starting a business|how to start a business|starting a company|payroll in india|india payroll|payroll compliance|payroll process|payroll tax"): return "C10"
    if not has(k, r"employer of record|\beor\b") and has(k, r"benefit|maternity|leave|background|contractor|work permit|salary|termination|notice period"): return "C6"
    if has(k, r"hire|hiring|without|how to|can a foreign|startup|small business|through (an )?eor"): return "C2"
    if has(k, r"\bcost\b|much does|price|pricing"): return "C1"
    if "india" in k: return "C1"
    return "C7g"   # generic global EOR head terms

for k in KW.values(): k["c"] = cluster(k["kw"])

CL = [
 ("C1", "EOR India: the commercial core", "One page", "/employer-of-record-india/",
  "\"employer of record india\", \"eor india\" and the India-market query share 6 of 10 page-one URLs. Google treats them as one intent. The cost query's top results are the same India EOR pages, so cost is a section here, not a separate page.",
  "Papaya's guide (DR 72) earns the most traffic, about 240 visits a month from 960 searches. Skuad's 8,658-word country page is the deepest. Deel, Multiplier, Rippling and Safeguard follow. Infotree ranks #5 to #8 at DR 29.",
  "Match Skuad's depth, beat everyone on proof: 5,000+ words, 20+ question headings, 10+ HTML tables, the $199 price with every statutory line in USD, a live calculator, and the no-penalty guarantee no competitor offers."),
 ("C2", "Hire employees in India", "One page", "/hire-employees-in-india/",
  "A different intent: the top results are how-to guides on different URLs (Papaya's how-to guide, Rippling's country-hiring page, Skuad's hire-a-team page), not EOR service pages.",
  "Papaya #2, Rippling #3, Skuad #4, then Indeed, Wise and India Briefing. Page one is guides of about 2,500 to 3,500 words.",
  "A step-by-step hiring guide that compares the three routes (contractor, EOR, own entity) in one table, with timelines, costs and the paperwork at each step. It is the guide the commercial page links to, and vice versa."),
 ("C3", "PEO in India, and EOR vs PEO", "One page", "/peo-india/",
  "Missing from the original pull. Six PEO India variants add up to about 570 searches a month at keyword difficulty 0 to 1. Deel, Rippling and Skuad each run a dedicated page.",
  "Deel's \"PEO vs EOR services in India\" guide ranks #1. Low-authority vendors rank #3 to #10 (DR 12 to 37).",
  "Answer the question buyers actually have: India has no co-employment model, so what they call PEO is an EOR. One page that says so, compares both, and routes to the EOR page."),
 ("C4", "Best EOR providers for India", "One page", "/best-employer-of-record-india/",
  "Comparison intent. Skuad's \"10 best EOR services in India\" and Papaya's list both rank, and AI Overviews cite a Reddit comparison thread.",
  "Skuad, Papaya and Asanify lists; each vendor ranks itself first.",
  "The only list with a stated method and published prices for every provider. Paybooks appears once, on the evidence."),
 ("C5", "Hire developers and other roles in India", "Template, 5 pages first", "/hire-[role]-in-india/",
  "Rippling's single biggest India page is \"hire software developer in India\" (1,590 searches across its keywords). These searches were wrongly treated as staffing noise in the first pass. An EOR vendor wins them.",
  "Rippling ranks #1 to #6 across developer terms. Skuad and Wisemonk publish role guides too.",
  "Five role pages built from one template: software developers, data and AI engineers, finance and accounting, customer support, sales. Each carries salary bands, the all-in EOR cost, and a hire-in-10-days path."),
 ("C6", "Employing in India: the guides foreign employers need", "8 guides", "/guides/",
  "Supporting demand competitors monetize: benefits (about 270 searches), maternity leave (200), background checks (150), paying contractors (100), plus the Labour Codes and permanent establishment questions from buyer research.",
  "Papaya and Rippling benefits guides, Rippling contractor and termination guides, Remote's 20-page India country explorer.",
  "Guides written for the foreign employer, each ending in the EOR page. Labour Codes and state-rule changes are the edge: nobody writes them for a foreign buyer."),
 ("C7", "What an EOR is", "Glossary entry + FAQ", "/glossary/employer-of-record/",
  "Definition intent (\"what is an employer of record\", 600 searches). Page one is ADP, Wikipedia and global vendors, and an AI Overview answers it before any click.",
  "ADP (DR 91), Wikipedia, Deel, Remote.",
  "Not a traffic play. One short, answer-first definition that AI Overviews and assistants can cite, linked from every page."),
 ("C8", "Tools that answer the money question", "2 tools", "/tools/",
  "Every ranking EOR vendor has a cost calculator. Deel and Wisemonk also run an EOR vs entity calculator.",
  "Deel, Papaya, Rippling, Wisemonk calculators.",
  "The India employee cost calculator (already built on the sample page) and an EOR vs own-entity break-even calculator."),
]
CN = {c[0]: c for c in CL}

def cl_kws(cid): return sorted([k for k in KW.values() if k["c"] == cid], key=lambda k: -k["vol"])
agg = {cid: (len(cl_kws(cid)), sum(k["vol"] for k in cl_kws(cid))) for cid in list(CN) + ["C7g", "C9", "C10", "X"]}

# ---------- SERP tables ----------
def dom(u): return re.sub(r"^www\.", "", u.split("//")[1].split("/")[0])
def ptype(u, t):
    u = u.lower()
    if re.search(r"/blog|/library|/resources|/post/|/pulse|/academy|/articles|/insights|/co/run", u): return "Guide"
    if re.search(r"/country|/employer-of-record/|/india/|/hire|/peo|/country-hiring|/eor$", u): return "Service / country page"
    if u.rstrip("/").count("/") <= 2: return "Homepage"
    return "Service / country page"
SERPQ = ["employer of record india|us", "eor india|us", "employer of record india cost|us", "hire employees in india|us", "peo india|us", "employer of record india|in"]
serp_html = []
for q in SERPQ:
    kw, c = q.split("|")
    rows = [p for p in serps[q] if "organic" in (p.get("type") or []) and p.get("url") and "google.com/goto" not in p["url"]]
    ai = sum(1 for p in serps[q] if "ai_overview_sitelink" in (p.get("type") or []))
    tr = "".join(f'<tr><td class="n">{p["position"]}</td><td>{E(dom(p["url"]))}</td><td class="n">{int(p["domain_rating"] or 0)}</td><td>{ptype(p["url"], p.get("title"))}</td><td class="n">{"–" if p.get("traffic") is None else fmt(p["traffic"])}</td></tr>' for p in rows[:8])
    low = [p for p in rows if (p.get("domain_rating") or 100) < 45]
    note = f'{len(low)} of the page-one results sit below DR 45, the lowest at DR {int(min(p["domain_rating"] for p in low))}.' if low else "Every page-one result is DR 45 or above."
    serp_html.append(f'<details class="topic"><summary><span class="tt">"{E(kw)}"</span><span class="tag lp">{"Google USA" if c == "us" else "Google India"}</span><span class="cnt">{("AI Overview cites " + str(ai) + " sources · ") if ai else ""}{E(note)}</span></summary>'
                     f'<div class="tbody"><div class="tw"><table><thead><tr><th class="n">#</th><th>Site</th><th class="n">DR</th><th>Page type</th><th class="n">Est. visits / mo</th></tr></thead><tbody>{tr}</tbody></table></div></div></details>')

# ---------- page quality benchmark ----------
BENCH = [
 ("skuad.io/employer-of-record/india", "Skuad", "Country page", 8658, 35, 20, 19, True, "$199 / month"),
 ("wisemonk.io/eor", "Wisemonk", "Service page", 3921, 25, 14, 3, True, "$99 to $699"),
 ("deel.com/blog/employer-of-record-india", "Deel", "Guide", 3824, 11, 4, 2, True, "none on page"),
 ("rippling.com/blog/employer-of-record-guide-india", "Rippling", "Guide", 3086, 9, 1, 3, True, "none on page"),
 ("oysterhr.com/library/employers-of-record-in-india", "Oyster", "Guide", 3233, 28, 1, 1, True, "none on page"),
 ("infotreeglobal.com/employer-of-record-india", "Infotree (DR 29)", "Service page", 2886, 3, 0, 0, True, "none on page"),
 ("papayaglobal.com/blog/employer-of-record-in-india", "Papaya", "Guide", 2146, 13, 0, 1, True, "none on page"),
 ("safeguardglobal.com/country/india/eor", "Safeguard", "Country page", 1034, 5, 1, 0, False, "none on page"),
]
bench_rows = "".join(f'<tr><td><b>{E(n)}</b><br><span class="mut">{E(u)}</span></td><td>{E(t)}</td><td class="n">{fmt(w)}</td><td class="n">{h}</td><td class="n">{q}</td><td class="n">{tb}</td><td>{"Yes" if f else "No"}</td><td>{E(pr)}</td></tr>' for u, n, t, w, h, q, tb, f, pr in BENCH)
bench_rows += '<tr class="me"><td><b>Paybooks target (new page)</b><br><span class="mut">Replaces the current paybooks.in/eor/ and /eor-2/</span></td><td>Service page</td><td class="n">5,000+</td><td class="n">20+</td><td class="n">15+</td><td class="n">10+</td><td>Yes, with schema</td><td>$199, every line in USD</td></tr>'

# ---------- competitor playbooks ----------
PB = [
 ("Wisemonk", "wisemonk.io", 45, "Volume without traction", "666 India URLs: service pages for every term, 11 tools, and hundreds of role and country-of-origin blogs (\"Australian startup hiring support engineers in India\").", "Little of it earns traffic. Its top US India page is a public-holidays blog, and its EOR page reaches only #10 in India for the head term. Scale without depth or authority does not win."),
 ("Skuad", "skuad.io", 60, "One very deep page", "21 India URLs, but one 8,658-word country page with 35 headings, 19 tables and a $199 price carries the cluster. Separate PEO, company-registration and role pages.", "Ranks #1 for the cost query and #4 for the head term with only 21 pages. Depth on the money page is what works."),
 ("Papaya Global", "papayaglobal.com", 72, "Guides that answer the question", "17 India URLs, almost all blog guides: EOR in India, how to hire, benefits, paying employees.", "Top traffic winner: its EOR India guide earns about 240 visits a month, its hiring guide 70. Guides outrank service pages on these queries."),
 ("Deel", "deel.com", 81, "Authority plus a few guides", "17 India URLs: two EOR India guides, a PEO vs EOR guide, payroll, costs, and a product landing page at $599.", "Ranks #1 for PEO India and page one for the head term, but no India cost page, no city or state content, and a price three times Paybooks'."),
 ("Rippling", "rippling.com", 84, "Role-based hiring guides", "20 India URLs: EOR, PEO, benefits, termination, contractors, and \"hire software developers in India\".", "Its biggest India page is the developer-hiring guide. It proves EOR vendors win role-based hiring searches."),
 ("Remote", "remote.com", 80, "Country explorer", "39 India URLs, mostly a templated country explorer: EOR, payroll, taxes, leave, termination, equity, and 8 benefits pages.", "Broad but templated; does not place on page one for the India head terms measured."),
 ("Multiplier", "usemultiplier.com", 68, "Templated country microsite", "52 India URLs from a template used for 100+ countries: EOR, payroll, laws, visas, subsidiary, compliance calendar.", "Page one for the head term (#6) on template alone. Blocks crawlers, so pages were counted from its sitemap only."),
 ("Asanify", "asanify.com", 48, "India specialist, blog-heavy", "139 India URLs: EOR cost, permanent establishment, onboarding, contractor payments by origin country, and 60+ role-hiring blogs.", "Ranks #5 for the cost query with a dedicated cost page. Shows the India-specialist angle works on long-tail terms."),
]
pb_html = "".join(f'<div class="pb"><div class="pbh"><b>{E(n)}</b><span class="dr">DR {dr}</span><span class="pill">{E(tag)}</span></div><p><b>What they built.</b> {E(built)}</p><p><b>What it tells us.</b> {E(lesson)}</p></div>' for n, d, dr, tag, built, lesson in PB)

# ---------- page plan ----------
PLAN = [
 ("Wave 1", "1", "EOR India: the commercial page", "/employer-of-record-india/", "C1", "Sample design built; replaces paybooks.in/eor/ and /eor-2/, which redirect here"),
 ("Wave 1", "2", "India employee cost calculator", "/tools/india-employee-cost-calculator/", "C8", "Built into the sample design"),
 ("Wave 1", "3", "Hire employees in India: the guide", "/hire-employees-in-india/", "C2", "To build"),
 ("Wave 1", "4", "PEO in India vs EOR", "/peo-india/", "C3", "To build"),
 ("Wave 1", "5", "Best EOR providers for India", "/best-employer-of-record-india/", "C4", "To build"),
 ("Wave 2", "6", "EOR vs own entity calculator", "/tools/eor-vs-entity-calculator/", "C8", "To build"),
 ("Wave 2", "7–11", "Hire [role] in India: 5 role pages", "/hire-[role]-in-india/", "C5", "To build"),
 ("Wave 2", "12–19", "8 employer guides", "/guides/", "C6", "Benefits · maternity and leave · background checks · contractors vs employees · termination · Labour Codes for foreign employers · permanent establishment risk · moving from EOR to your own entity"),
 ("Wave 2", "20", "What is an employer of record", "/glossary/employer-of-record/", "C7", "To build"),
]
plan_rows = "".join(f'<tr><td>{w}</td><td class="n">{n}</td><td><b>{E(t)}</b><br><code>{E(u)}</code></td><td class="n">{fmt(agg[c][0])}</td><td class="n">{fmt(agg[c][1])}</td><td>{E(s)}</td></tr>' for w, n, t, u, c, s in PLAN)

def kw_table(ks):
    if not ks: return '<p class="mut">Targets come from competitor and buyer-question research.</p>'
    tr = "".join(f'<tr><td>{E(k["kw"])}</td><td>{"USA" if k["ctry"] == "us" else "India"}</td><td class="n">{fmt(k["vol"])}</td><td class="n">{"–" if k["kd"] is None else k["kd"]}</td><td>{"New from competitors" if k["src"] == "competitor gap" else ""}</td></tr>' for k in ks)
    return f'<div class="tw"><table><thead><tr><th>Keyword</th><th>Google market</th><th class="n">Searches / mo</th><th class="n">KD</th><th></th></tr></thead><tbody>{tr}</tbody></table></div>'

cl_html = []
for cid, name, pg, url, why, who, win in CL:
    n, v = agg[cid]
    cl_html.append(f'<details class="topic"><summary><span class="tag lp">{E(pg)}</span><span class="tt">{E(name)}</span><span class="cnt">{n} keyword{"s" if n != 1 else ""} · {fmt(v)} searches / mo</span></summary>'
                   f'<div class="tbody"><div class="cl3"><div><h4>Why it is one cluster</h4><p>{E(why)}</p></div><div><h4>Who wins it today</h4><p>{E(who)}</p></div><div><h4>How Paybooks wins it</h4><p>{E(win)}</p><p class="mut">Proposed URL: <code>{E(url)}</code></p></div></div>'
                   f'<details class="inner"><summary>Target keywords</summary>{kw_table(cl_kws(cid))}</details></div></details>')
glob = cl_kws("C7g") + cl_kws("C7")
nopursue = cl_kws("C9")
cl_html.append(f'<details class="topic"><summary><span class="tag x">Supported, not a page</span><span class="tt">Generic global EOR terms</span><span class="cnt">{len(cl_kws("C7g"))} keywords · {fmt(agg["C7g"][1])} searches / mo</span></summary><div class="tbody"><p>"employer of record", "eor services" and similar are won by ADP (DR 91) and global platforms selling 100+ countries. Paybooks sells India. These terms are served by the EOR India page and the glossary entry, and become a real target in year two once transperfect.com links lift authority.</p><details class="inner"><summary>Keywords</summary>{kw_table(cl_kws("C7g"))}</details></div></details>')
cl_html.append(f'<details class="topic"><summary><span class="tag x">Handled by other categories</span><span class="tt">Business setup and India payroll searches</span><span class="cnt">{agg["C10"][0]} keywords · {fmt(agg["C10"][1])} searches / mo</span></summary><div class="tbody"><p>Competitors like Skuad and Rippling rank for "company registration in india" and "payroll in india" from their EOR clusters. For Paybooks these belong to the Managed India Office and Multi-Country Payroll categories, which own them and link across to the EOR page.</p><details class="inner"><summary>Keywords</summary>{kw_table(cl_kws("C10"))}</details></div></details>')
cl_html.append(f'<details class="topic"><summary><span class="tag x">Not pursued</span><span class="tt">Other-country EOR pages</span><span class="cnt">{agg["C9"][0]} keywords · {fmt(agg["C9"][1])} searches / mo</span></summary><div class="tbody"><p>Real demand at keyword difficulty 0 to 1, but Paybooks cannot deliver EOR outside India today. Building these pages would promise a service it does not sell. Revisit only if TransPerfect adds other-country EOR.</p><details class="inner"><summary>Keywords</summary>{kw_table(nopursue)}</details></div></details>')

tgt = sum(agg[c][1] for c in ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"])
tgt_n = sum(agg[c][0] for c in ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"])
gap_n = sum(1 for k in KW.values() if k["src"] == "competitor gap" and k["c"] not in ("X", "C9"))

CSS = """
:root{--ink:#101828;--ink2:#344054;--muted:#667085;--line:#E4E9E1;--bg:#F6F8F3;--green:#4F8A10;--g600:#3E6E0C;--g100:#E9F3DC;--forest:#0B1F14;--orange:#F26B1D;--o100:#FDEBDD}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 Inter,system-ui,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header{background:var(--forest);color:#fff;padding:46px 0 38px}header h1{font:700 38px/1.1 "Instrument Sans",sans-serif;margin:0 0 12px;letter-spacing:-.02em;max-width:900px}
header p{color:#C9D9C2;margin:0;max-width:860px;font-size:16px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:26px}.kpi{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:14px 16px}
.kpi b{display:block;font:700 26px "Instrument Sans";color:#9FD35C}.kpi span{font-size:12.5px;color:#BFD3B9}
nav{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid var(--line)}nav .wrap{display:flex;gap:2px;overflow:auto}
nav a{padding:14px 13px;color:var(--ink2);text-decoration:none;font-weight:600;font-size:14px;white-space:nowrap}nav a:hover{color:var(--g600)}
section{padding:40px 0 6px}h2{font:700 26px "Instrument Sans";margin:0 0 6px;letter-spacing:-.01em}.lead{color:var(--muted);margin:0 0 18px;max-width:880px}
.verdict{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.verdict div{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px}
.verdict b{display:block;font:700 17px/1.3 "Instrument Sans";margin-bottom:6px}.verdict p{margin:0;color:var(--ink2);font-size:14px}
table{width:100%;border-collapse:collapse;font-size:13.5px}th{text-align:left;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:9px 10px;border-bottom:1px solid var(--line);background:#FAFBF8}
td{padding:8px 10px;border-bottom:1px solid #EEF1EC;vertical-align:top}.n{text-align:right;white-space:nowrap}.tw{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:#fff}
tr.me td{background:var(--g100);font-weight:600}.mut{color:var(--muted);font-size:12.5px}code{font-size:12.5px;background:#F2F5EE;border-radius:6px;padding:1px 6px;color:var(--g600)}
details{border-radius:14px}summary{cursor:pointer;list-style:none}summary::-webkit-details-marker{display:none}
.topic{border:1px solid var(--line);margin:8px 0;background:#fff}.topic>summary{display:flex;align-items:center;gap:12px;padding:13px 15px;flex-wrap:wrap}
.topic>summary::before{content:"›";font:700 18px Inter;color:var(--green);transition:transform .2s}.topic[open]>summary::before{transform:rotate(90deg)}
.tt{font-weight:600}.cnt{margin-left:auto;font-size:12.5px;color:var(--muted)}
.tag{font-size:11px;font-weight:700;border-radius:999px;padding:3px 9px;white-space:nowrap}.tag.lp{background:var(--g100);color:var(--g600)}.tag.x{background:#F2F4F7;color:#475467}
.tbody{padding:0 15px 15px}.cl3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:10px}.cl3 h4{margin:0 0 6px;font:700 13.5px "Instrument Sans"}.cl3 p{margin:0 0 6px;font-size:13.5px;color:var(--ink2)}
.inner{border:1px dashed var(--line);background:#FCFDFB;margin-top:6px}.inner>summary{padding:10px 12px;font-weight:600;color:var(--g600);font-size:13.5px}.inner>summary::after{content:" +";}.inner[open]>summary::after{content:" −"}.inner .tw{margin:0 12px 12px}
.pbs{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.pb{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px}.pb p{margin:6px 0 0;font-size:13.5px;color:var(--ink2)}
.pbh{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.pbh b{font:700 16px "Instrument Sans"}.dr{font-size:12px;color:var(--muted)}.pill{margin-left:auto;font-size:11px;font-weight:700;background:var(--o100);color:#B54708;border-radius:999px;padding:3px 9px}
.why{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.why div{background:#fff;border:1px solid var(--line);border-left:4px solid var(--green);border-radius:12px;padding:14px 16px}.why b{display:block;margin-bottom:4px}.why p{margin:0;font-size:13.5px;color:var(--ink2)}
.note{font-size:13px;color:var(--muted)}a.dl{display:inline-block;margin-top:10px;background:var(--forest);color:#fff;text-decoration:none;padding:10px 16px;border-radius:10px;font-weight:600;font-size:14px}
footer{padding:36px 0 50px;color:var(--muted);font-size:13px}
@media(max-width:860px){.kpis,.verdict,.cl3,.pbs,.why{grid-template-columns:1fr}}
"""

PAGE = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EOR India Strategy</title><meta name="robots" content="noindex,nofollow">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>
<header><div class="wrap"><h1>How Paybooks wins "Employer of Record India" search</h1>
<p>Competitor research and search strategy for the Employer of Record category. Built from live Ahrefs search results, twelve competitors' sitemaps, and every page-one page opened and measured on 24 September 2026.</p>
<div class="kpis"><div class="kpi"><b>{fmt(sum(v["n"] for v in play.values()))}</b><span>competitor India pages mapped from 12 sitemaps</span></div>
<div class="kpi"><b>{len(SERPQ)}</b><span>live page-one results analyzed, US and India</span></div>
<div class="kpi"><b>{fmt(tgt_n)}</b><span>target keywords in 8 clusters, {gap_n} new from competitors</span></div>
<div class="kpi"><b>20</b><span>pages to build: 4 core, 2 tools, 5 role pages, 9 guides</span></div></div></div></header>
<nav><div class="wrap"><a href="#verdict">The verdict</a><a href="#serps">Who ranks today</a><a href="#bench">What wins</a><a href="#playbooks">Competitor playbooks</a><a href="#clusters">Keyword clusters</a><a href="#plan">Page plan</a><a href="#confidence">Why Paybooks wins</a><a href="#method">Method</a></div></nav>
<main class="wrap">
<section id="verdict"><h2>The verdict</h2><p class="lead">Three findings decide the strategy.</p>
<div class="verdict"><div><b>Authority is not what decides this category.</b><p>On "employer of record india", page one runs from DR 81 (Deel) down to DR 29 (Infotree). For "PEO India", sites at DR 12 to 37 hold #3 to #10. Paybooks at DR 41 is already strong enough to rank.</p></div>
<div><b>Depth on the right page decides it.</b><p>Skuad ranks #1 for the cost query with one 8,658-word page, 35 headings and 19 tables. Wisemonk published 666 India pages, and its EOR page reaches only #10 in India. One deep page per real intent beats hundreds of thin ones.</p></div>
<div><b>No competitor covers all five India intents well.</b><p>The commercial page, hiring guide, PEO question, provider comparison and role-based hiring are each won by a different competitor. Paybooks can be the one site that answers all five, with the lowest published price and 12 years of India payroll behind it.</p></div></div></section>
<section id="serps"><h2>Who ranks today</h2><p class="lead">Live Ahrefs results for the queries with enough volume to return a stored page one. DR is Ahrefs Domain Rating, 0 to 100. Open a query to see its top results.</p>{"".join(serp_html)}
</section>
<section id="bench"><h2>What a winning page looks like</h2><p class="lead">Every page-one result for the head term, opened and measured. Multiplier blocks crawlers, so it is counted from its sitemap only.</p>
<div class="tw"><table><thead><tr><th>Page</th><th>Type</th><th class="n">Words</th><th class="n">Headings</th><th class="n">Question headings</th><th class="n">Tables</th><th>FAQ</th><th>Price shown</th></tr></thead><tbody>{bench_rows}</tbody></table></div>
<p class="note">The Paybooks target matches the deepest competitor and adds what none of them show together: a published price broken down line by line, a live calculator, and a written no-penalty guarantee.</p></section>
<section id="playbooks"><h2>Competitor playbooks</h2><p class="lead">What each competitor built for India, from its sitemap, and what the rankings say about whether it works.</p><div class="pbs">{pb_html}</div></section>
<section id="clusters"><h2>Keyword clusters</h2><p class="lead">Keywords are grouped by what Google shows for them, not by wording. Where two queries share page-one URLs, they are one intent and one page. Open a cluster for the evidence, the competitor to beat, and every target keyword.</p>{"".join(cl_html)}</section>
<section id="plan"><h2>The page plan</h2><p class="lead">Twenty pages in two waves. Every URL here is proposed for the new site; none exists on paybooks.in yet. Paybooks today has one EOR page, paybooks.in/eor/, with a near-duplicate at /eor-2/. Wave 1 takes the commercial queries that bring buyers. Wave 2 widens the net with role-based hiring and the guides that feed the commercial page.</p>
<div class="tw"><table><thead><tr><th>Wave</th><th class="n">#</th><th>Page</th><th class="n">Keywords</th><th class="n">Searches / mo</th><th>Status</th></tr></thead><tbody>{plan_rows}</tbody></table></div>
<p class="note">Keyword and search counts are per cluster; pages sharing a cluster share its count. Each Wave 2 page links to the EOR India page, which stays the single page that sells.</p></section>
<section id="confidence"><h2>Why Paybooks can win this</h2><div class="why">
<div><b>The price is a ranking asset.</b><p>$199 a month against Deel's $599 and Remote's $699. Skuad ranks #1 for cost with $199 on the page. Paybooks can publish the same price with every statutory line in dollars, which no ranking page does.</p></div>
<div><b>Authority is already enough.</b><p>DR 41 sits above Infotree (29), Gloroots (38) and the PEO vendors (12 to 37) that already hold page one. Links from transperfect.com (DR 74) close the gap to Skuad (60) and Multiplier (68).</p></div>
<div><b>Proof competitors cannot copy.</b><p>3,000+ customers, 1.5 million payslips a year, 12 years of India payroll, and a written no-penalty guarantee. None of the eight competitors analyzed publishes a guarantee.</p></div>
<div><b>AI answers are the next battleground.</b><p>Google's AI Overview for "employer of record india" cites ten sources, including a Reddit thread and a LinkedIn post. Answer-first pages with FAQ schema and clear tables are what those answers quote.</p></div></div></section>
<section id="method"><h2>Method and sources</h2><p class="lead">Every figure on this page comes from one of these pulls, all on 23 to 24 September 2026.</p>
<div class="tw"><table><tbody>
<tr><td><b>Competitor sitemaps</b></td><td>12 domains fetched in full, about 131,000 URLs. English India pages extracted and deduplicated across translated copies: {fmt(sum(v["n"] for v in play.values()))} pages.</td></tr>
<tr><td><b>Live search results</b></td><td>Ahrefs SERP Overview for 18 India EOR queries in the US and India; 6 returned a stored page one.</td></tr>
<tr><td><b>Page measurement</b></td><td>Each page-one URL fetched and measured for word count, headings, question headings, tables, FAQ and prices shown.</td></tr>
<tr><td><b>Competitor keywords</b></td><td>Ahrefs organic keywords (US, containing "india") for Deel, Papaya, Skuad and Rippling: {gap_n} relevant keywords missing from the original pull.</td></tr>
<tr><td><b>Original keyword pull</b></td><td>Ahrefs Keywords Explorer, 161 Employer of Record keywords.</td></tr>
</tbody></table></div></section>
</main><footer class="wrap">Prepared by Mohan Kumar Allada for the TransPerfect Paybooks SEO proposal · 24 September 2026</footer></body></html>'''
os.makedirs(f"{H}/out", exist_ok=True)
open(f"{H}/out/index.html", "w", encoding="utf-8").write(PAGE)
with open(f"{H}/out/eor-keyword-clusters.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["cluster", "keyword", "market", "volume", "kd", "source"])
    NAME = {c[0]: c[1] for c in CL}; NAME.update({"C7g": "Generic global EOR terms (supported, not a page)", "C9": "Other-country EOR (not pursued)", "C10": "Business setup and India payroll (other categories)", "X": "Excluded"})
    for k in sorted(KW.values(), key=lambda k: (k["c"], -k["vol"])): w.writerow([NAME[k["c"]], k["kw"], k["ctry"].upper(), k["vol"], "" if k["kd"] is None else k["kd"], k["src"]])
print("clusters", {c: agg[c] for c in agg}, "target", tgt_n, tgt, "gap", gap_n)
