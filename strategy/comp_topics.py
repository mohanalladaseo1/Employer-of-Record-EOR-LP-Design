# Competitor topic inventory for the EOR India category, consumed by build_ceo.py
import json, re, os, html
E = html.escape
_H = os.path.dirname(os.path.abspath(__file__))
RAW = json.load(open(os.path.join(_H, "comp_india_top_pages.json")))
NAME = {"deel.com": "Deel", "remote.com": "Remote", "rippling.com": "Rippling", "papayaglobal.com": "Papaya", "usemultiplier.com": "Multiplier",
        "velocityglobal.com": "Velocity Global", "skuad.io": "Skuad", "playroll.com": "Playroll", "wisemonk.io": "Wisemonk", "oysterhr.com": "Oyster",
        "g-p.com": "G-P", "asanify.com": "Asanify"}
# (key, topic, status, where it sits in the plan)
TOP = [
 ("eor", "Employer of Record India", "In plan", "Employer of Record India, the commercial page"),
 ("best", "Best EOR provider lists", "In plan", "Best EOR providers for India (refresh)"),
 ("peo", "PEO in India", "In plan", "PEO in India (refresh)"),
 ("hire", "Hire employees in India", "In plan", "Hire employees in India guide (refresh)"),
 ("role", "Hire developers and other roles", "In plan", "Hire [role] in India, 15 programmatic pages"),
 ("salary", "Average salaries in India", "In plan", "India salary guide in USD, 7 programmatic pages"),
 ("contractor", "Hiring contractors", "In plan", "Contractors vs employees in India (new)"),
 ("benefits", "Employee benefits and insurance", "In plan", "Employee benefits in India (new)"),
 ("maternity", "Maternity leave", "In plan", "Maternity leave guide (refresh)"),
 ("termination", "Termination, severance and final pay", "In plan", "Termination and final settlement guide (refresh)"),
 ("background", "Background checks", "In plan", "Background checks in India (new)"),
 ("overtime", "Working hours and overtime", "Added", "Working hours and overtime rules in India (new)"),
 ("minwage", "Minimum wage", "Added", "Minimum wage in India by state, in USD (new)"),
 ("leave", "Leave policy and public holidays", "Added", "Public holidays and leave in India 2026 (refresh of the 2025 holiday list)"),
 ("laws", "Labour and employment laws", "Added", "India labour laws for foreign employers (refresh of the Labour Codes article)"),
 ("salstruct", "Salary structure", "Added", "Salary structure under the Labour Codes (refresh)"),
 ("contracts", "Offer letters, contracts and NDAs", "Added", "Employment contracts, offer letters and NDAs in India (new)"),
 ("permits", "Work permits and visas", "Added", "Work permits and employment visas for foreign staff (new)"),
 ("payroll", "Payroll, payroll tax and compliance", "Linked", "Paybooks payroll pages already cover this; EOR pages link to the compliance calendar and the PF, ESI, PT and LWF guide"),
 ("entity", "Company registration and subsidiaries", "Linked", "Bridged by the EOR-to-own-entity guide; entity setup belongs to the Managed India Office offer"),
 ("offshore", "Offshore teams and development centres", "Linked", "Belongs to the Managed India Office and GCC offer; linked from the EOR page"),
]
TOPN = {t[0]: t for t in TOP}
RULES = [
 ("noise", r"indiana|moving-to-india|laptop|/jobs/|visa-pathway|recruitment-agenc|staffing|(?<!payroll-)outsourc|seo-outsourcing|accounting-outsourcing|tax-preparation|applicant-tracking|manpower|work-from-india|remote-work/india|become-a-contractor"),
 ("brand", r"\b(deel|remote|remote\.com) india\b|remote company in india|country-explorer/india\s|/en-in/country-explorer/india\s|/contractor-management\s.*remote\.com india|remote\.com india"),
 ("best", r"best-eor|10-best|20-best"),
 ("peo", r"\bpeo\b|/peo/"),
 ("contractor", r"contractor"),
 ("benefits", r"benefit|medical insurance"),
 ("role", r"developer|programmer|seo-expert|seo expert"),
 ("offshore", r"offshore"),
 ("salstruct", r"salary-structure|salary structure"),
 ("salary", r"average-salary|average salary|median salary|average-salary|india-average-salary|date income"),
 ("overtime", r"overtime|working-hours"),
 ("minwage", r"minimum-wage|minimum wage|minimum salary"),
 ("maternity", r"maternity"),
 ("leave", r"leave|holiday"),
 ("termination", r"terminat|severance|full and final"),
 ("contracts", r"offer-letter|offer letter|non-disclosure|non disclosure"),
 ("background", r"background"),
 ("permits", r"work-permit|work permit|immigration"),
 ("laws", r"labor-law|labour|employment-law|legal age"),
 ("payroll", r"payroll|countrypedia"),
 ("entity", r"register|registration|subsidiary|start a business"),
 ("eor", r"employer-of-record|employers-of-record|\beor\b|employer of record"),
 ("hire", r"hire|hiring|india-employees|indian employees"),
]
def classify(u, k):
    s = (u + " " + k).lower() + " "
    for key, rx in RULES:
        if re.search(rx, s): return key
    return "unclassified"
PAGES = {}
for d, v in RAW.items():
    for c in ("us", "in"):
        for p in v[c]:
            if not p["sum_traffic"]: continue
            key = (d, p["url"])
            r = PAGES.setdefault(key, {"d": d, "url": p["url"], "us": 0, "in": 0, "pos": 99, "kw": "", "kwv": 0, "kwc": "", "best": -1})
            r[c] = p["sum_traffic"]
            pos = p.get("top_keyword_best_position") or 99
            r["pos"] = min(r["pos"], pos)
            if p["sum_traffic"] > r["best"]:
                r["best"] = p["sum_traffic"]; r["kw"] = p["top_keyword"]; r["kwv"] = p["top_keyword_volume"]; r["kwc"] = "USA" if c == "us" else "India"
for r in PAGES.values(): r["t"] = classify(r["url"], r["kw"])
UNC = [r for r in PAGES.values() if r["t"] == "unclassified"]
REL = [r for r in PAGES.values() if r["t"] in TOPN]
NOISE = [r for r in PAGES.values() if r["t"] in ("noise", "brand")]
def vis(r): return r["us"] + r["in"]
def fmt(n): return f"{n:,}"
# topic rollup
ROLL = []
for key, name, st, plan in TOP:
    rs = [r for r in REL if r["t"] == key]
    if not rs: continue
    by = {}
    for r in rs: by.setdefault(NAME[r["d"]], []).append(r)
    top = max(rs, key=lambda r: r["kwv"])
    ROLL.append(dict(key=key, name=name, st=st, plan=plan, n=len(rs), us=sum(r["us"] for r in rs), inn=sum(r["in"] for r in rs),
                     who=sorted(((n, len(x), sum(vis(y) for y in x)) for n, x in by.items()), key=lambda z: -z[2]),
                     kw=top["kw"], kwv=top["kwv"], kwc=top["kwc"], pos=min(r["pos"] for r in rs)))
ROLL.sort(key=lambda t: -(t["us"] + t["inn"]))
N_PAGES = len(REL); N_TOPICS = len(ROLL); N_COMP = len({r["d"] for r in REL})
N_IN = sum(1 for t in ROLL if t["st"] == "In plan"); N_ADD = sum(1 for t in ROLL if t["st"] == "Added"); N_LINK = sum(1 for t in ROLL if t["st"] == "Linked")
STC = {"In plan": "#4F8A10", "Added": "#F26B1D", "Linked": "#8A94A0"}
STL = {"In plan": "In the plan", "Added": "Added now", "Linked": "Linked, other offer"}
def stag(s): return f'<span class="vt" style="--c:{STC[s]}">{STL[s]}</span>'
topic_rows = "".join(
    f'<tr><td><b>{E(t["name"])}</b><div class="mut">{t["n"]} page{"s" if t["n"]>1 else ""}</div></td>'
    f'<td class="mut">{"; ".join(E(n) + (f" ({c})" if c > 1 else "") for n, c, _ in t["who"])}</td>'
    f'<td class="n">{fmt(t["us"])}</td><td class="n">{fmt(t["inn"])}</td>'
    f'<td class="mut">{E(t["kw"])} · {fmt(t["kwv"])} a month, {t["kwc"]}</td>'
    f'<td>{stag(t["st"])}<div class="mut">{E(t["plan"])}</div></td></tr>' for t in ROLL)
# per competitor
def short(u): return u.split('//', 1)[1].replace('www.', '')
comp_blocks = []
for d in sorted({r["d"] for r in REL}, key=lambda d: -sum(vis(r) for r in REL if r["d"] == d)):
    rs = sorted([r for r in REL if r["d"] == d], key=lambda r: -vis(r))
    tv = sum(vis(r) for r in rs); nt = len({r["t"] for r in rs})
    rows = "".join(
        f'<tr><td><a href="{E(r["url"])}" target="_blank" rel="noopener"><code>{E(short(r["url"]))}</code></a></td>'
        f'<td>{E(TOPN[r["t"]][1])}</td><td class="n">{fmt(r["us"]) if r["us"] else "–"}</td><td class="n">{fmt(r["in"]) if r["in"] else "–"}</td>'
        f'<td class="mut">{E(r["kw"])} · #{r["pos"] if r["pos"] < 99 else "–"}</td></tr>' for r in rs)
    comp_blocks.append(f'<details class="blk"><summary>{E(NAME[d])} · {len(rs)} pages across {nt} topics · {fmt(tv)} visits a month</summary>'
                       f'<div class="tw"><table><thead><tr><th>Page</th><th>Topic</th><th class="n">USA visits</th><th class="n">India visits</th><th>Top search · best position</th></tr></thead><tbody>{rows}</tbody></table></div></details>')
COMP_HTML = "".join(comp_blocks)
ZERO = [NAME[d] for d in RAW if not any(r["d"] == d for r in REL)]
