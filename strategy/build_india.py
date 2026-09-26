"""CEO-grade presentation of the EOR India strategy.
Runs build_strategy.py for the data and detail blocks, then writes a new
narrative index.html: answer first, charts, page map, asks, appendix.
"""
import os, re, json, html
H = os.path.dirname(os.path.abspath(__file__))
ns = {"__file__": f"{H}/build_strategy.py"}
exec(open(f"{H}/build_strategy.py").read(), ns)
g = ns; E = html.escape; fmt = g["fmt"]
agg, CL, serps, SERPQ, play = g["agg"], g["CL"], g["serps"], g["SERPQ"], g["play"]
inv = {"__file__": f"{H}/inventory.py"}; exec(open(f"{H}/inventory.py").read(), inv)
INV, REUSE, NEW, CC, CDEM, PGW, GAPV = inv["INV"], inv["REUSE"], inv["NEW"], inv["COMPARE_COUNTS"], inv["COMPARE_DEMAND"], inv["W"], inv["GAPV"]
ct = {"__file__": f"{H}/comp_topics.py"}; exec(open(f"{H}/comp_topics.py").read(), ct)
CT_ROWS, CT_COMP, CT_NP, CT_NT, CT_IN, CT_ADD, CT_LINK = ct["topic_rows"], ct["COMP_HTML"], ct["N_PAGES"], ct["N_TOPICS"], ct["N_IN"], ct["N_ADD"], ct["N_LINK"]
CT_NOISE, CT_ZERO, CT_NC = len(ct["NOISE"]), " and ".join(ct["ZERO"]), ct["N_COMP"]

# ---------- chart 1: the prize, searches by cluster ----------
SHORT = {"C1": "EOR India (the commercial page)", "C2": "Hire employees in India", "C3": "PEO in India", "C4": "Best EOR providers",
         "C5": "Hire developers and other roles", "C6": "Employer guides", "C7": "What an EOR is", "C8": "Cost and entity tools"}
prize = [(SHORT[c], agg[c][1] + (GAPV if c == "C6" else 0), agg[c][0], c) for c in ["C5", "C1", "C4", "C3", "C2", "C7", "C6", "C8"]]
prize.insert(1, ("Competitor comparisons", CDEM, 11, "CMP"))
RV, SV = 16350, 5800
prize = [(("Hire [role] in India (programmatic)", RV, 95, "C5") if x[3] == "C5" else x) for x in prize]
prize.insert(2, ("India salary guide (programmatic)", SV, 21, "SAL"))
mx = max(v for _, v, _, _ in prize)
rows = []
for i, (lab, v, n, c) in enumerate(prize):
    y = i * 46; w = max(4, 560 * v / mx)
    col = "#4F8A10" if c in ("C1", "C2", "C3", "C4", "CMP", "SAL") else "#9FC76A"
    rows.append(f'<text x="0" y="{y+22}" class="lb">{E(lab)}</text><rect x="300" y="{y+6}" width="{w:.0f}" height="26" rx="6" fill="{col}"/>'
                f'<text x="{300+w+10:.0f}" y="{y+24}" class="vl">{fmt(v)}</text>')
chart_prize = f'<svg viewBox="0 0 980 {len(prize)*46}" class="chart" role="img" aria-label="Monthly searches by keyword cluster">{"".join(rows)}</svg>'

# ---------- chart 2: who ranks, DR of page-one results per query ----------
LABQ = {"employer of record india|us": "employer of record india (USA)", "eor india|us": "eor india (USA)",
        "employer of record india cost|us": "employer of record india cost (USA)", "hire employees in india|us": "hire employees in india (USA)",
        "peo india|us": "peo india (USA)", "employer of record india|in": "employer of record india (India)"}
X0, XW = 330, 600
def xdr(dr): return X0 + XW * dr / 100
dots = []
for i, q in enumerate(SERPQ):
    y = 40 + i * 52
    dots.append(f'<text x="0" y="{y+5}" class="lb">{E(LABQ[q])}</text><line x1="{X0}" x2="{X0+XW}" y1="{y}" y2="{y}" class="gl"/>')
    for p in serps[q]:
        if "organic" in (p.get("type") or []) and p.get("domain_rating") is not None and "google.com" not in p["url"]:
            dr = p["domain_rating"]; low = dr < 45
            dots.append(f'<circle cx="{xdr(dr):.0f}" cy="{y}" r="9" fill="{"#F26B1D" if low else "#B8C7AE"}" fill-opacity=".9"><title>#{p["position"]} {E(g["dom"](p["url"]))} · DR {int(dr)}</title></circle>')
ybot = 40 + len(SERPQ) * 52
axis = "".join(f'<text x="{xdr(t):.0f}" y="{ybot+14}" class="ax" text-anchor="middle">{t}</text>' for t in range(0, 101, 20))
pb = xdr(41)
chart_serp = (f'<svg viewBox="0 0 980 {ybot+60}" class="chart" role="img" aria-label="Domain Rating of page-one results">'
              f'<rect x="{xdr(0):.0f}" y="14" width="{pb-xdr(0):.0f}" height="{ybot-14}" fill="#FDEBDD" opacity=".55"/>'
              f'{"".join(dots)}<line x1="{pb:.0f}" x2="{pb:.0f}" y1="10" y2="{ybot}" stroke="#0B1F14" stroke-width="2" stroke-dasharray="5 4"/>'
              f'<text x="{pb+8:.0f}" y="24" class="pbl">Paybooks today, DR 41</text>{axis}'
              f'<text x="{X0+XW/2:.0f}" y="{ybot+40}" class="ax" text-anchor="middle">Domain Rating of each page-one result (Ahrefs, 0 to 100)</text></svg>')

# ---------- chart 3: depth vs volume ----------
ck = json.load(open(f"{H}/comp_keywords.json"))
def eor_traffic(d):
    ks = ck.get(d, [])
    return sum(k.get("sum_traffic") or 0 for k in ks if re.search(r"employer of record|\beor\b|\bpeo\b|hire employees|hiring employees|hire in india", k["keyword"]))
DV = [("Wisemonk", play["wisemonk.io"]["n"], 0, "DR 45"), ("Skuad", play["skuad.io"]["n"], eor_traffic("skuad.io"), "DR 60"),
      ("Deel", play["deel.com"]["n"], eor_traffic("deel.com"), "DR 81"), ("Rippling", play["rippling.com"]["n"], eor_traffic("rippling.com"), "DR 84"),
      ("Papaya Global", play["papayaglobal.com"]["n"], eor_traffic("papayaglobal.com"), "DR 72")]
pmx = max(p for _, p, _, _ in DV); tmx = max(t for _, _, t, _ in DV)
dv = ['<text x="210" y="14" class="hd">India pages published</text><text x="600" y="14" class="hd">EOR search visits a month (USA)</text>']
for i, (n, pgs, tr, dr) in enumerate(DV):
    y = 34 + i * 50
    wp = max(3, 330 * pgs / pmx); wt = max(3, 330 * tr / tmx)
    dv.append(f'<text x="0" y="{y+19}" class="lb"><tspan font-weight="700">{E(n)}</tspan> <tspan class="mutt">{dr}</tspan></text>'
              f'<rect x="210" y="{y}" width="{wp:.0f}" height="28" rx="6" fill="#B8C7AE"/><text x="{210+wp+8:.0f}" y="{y+20}" class="vl">{fmt(pgs)}</text>'
              f'<rect x="600" y="{y}" width="{wt:.0f}" height="28" rx="6" fill="#4F8A10"/><text x="{600+wt+8:.0f}" y="{y+20}" class="vl">{"about 0" if tr == 0 else fmt(tr)}</text>')
chart_depth = f'<svg viewBox="0 0 980 {34+len(DV)*50}" class="chart" role="img" aria-label="India pages published versus EOR search visits">{"".join(dv)}</svg>'

# ---------- chart 4: the winning page ----------
BW = [("Skuad", 8658, 19, "#B8C7AE"), ("Wisemonk", 3921, 3, "#B8C7AE"), ("Deel", 3824, 2, "#B8C7AE"), ("Rippling", 3086, 3, "#B8C7AE"),
      ("Papaya", 2146, 1, "#B8C7AE"), ("Paybooks target", 5000, 10, "#F26B1D")]
LNK = {"Skuad": "https://www.skuad.io/employer-of-record/india", "Wisemonk": "https://www.wisemonk.io/eor",
       "Deel": "https://www.deel.com/blog/employer-of-record-india/", "Rippling": "https://www.rippling.com/blog/employer-of-record-guide-india",
       "Papaya": "https://www.papayaglobal.com/blog/employer-of-record-in-india/", "Paybooks target": "https://employer-of-record-eor-lp-design-livid.vercel.app/"}
bw = ['<text x="150" y="14" class="hd">Words on the page</text><text x="600" y="14" class="hd">HTML tables</text>']
for i, (n, w, t, c) in enumerate(BW):
    y = 30 + i * 44; me = n.startswith("Paybooks")
    fw = ' font-weight="700"' if me else ""
    lk = LNK[n]
    bw.append(f'<a href="{lk}" target="_blank" rel="noopener"><text x="0" y="{y+19}" class="lb lnk"{fw}>{E(n)} \u2197</text></a>'
              f'<rect x="150" y="{y}" width="{360*w/8658:.0f}" height="26" rx="6" fill="{c}"/><text x="{150+360*w/8658+8:.0f}" y="{y+19}" class="vl">{fmt(w)}{"+" if me else ""}</text>'
              f'<rect x="600" y="{y}" width="{max(3,300*t/19):.0f}" height="26" rx="6" fill="{c}"/><text x="{600+max(3,300*t/19)+8:.0f}" y="{y+19}" class="vl">{t}{"+" if me else ""}</text>')
chart_page = f'<svg viewBox="0 0 980 {30+len(BW)*44}" class="chart" role="img" aria-label="Page depth of ranking pages">{"".join(bw)}</svg>'

# ---------- current page issues ----------
ISS = json.load(open(f"{H}/issues.json"))
SEVC = {"High": "#C2410C", "Medium": "#8A94A0"}
iss_rows = "".join(f'<tr><td class="n">{k}</td><td><span class="vt" style="--c:{SEVC[sv]}">{sv}</span><div><b>{E(t)}</b></div></td><td class="mut">{E(ev)}</td><td>{E(fx)}</td></tr>' for k, (sv, t, ev, fx) in enumerate(ISS, 1))

# ---------- page map: hub and spoke ----------
_gr = sum(1 for x in REUSE if x[1] == "Refresh") + 2; _gn = sum(1 for x in NEW if x[0] == "Employer guides")
cx, cy = 490, 250
SP = [("Hire employees in India", "Guide · refresh", 1, -300, -150), ("PEO in India", "Page · refresh", 1, -100, -170), ("Best EOR providers", "List · refresh", 1, 100, -170),
      ("5 comparison pages", "Alternatives, vs, pricing · new", 1, 300, -150), ("Cost calculator", "Tool · built in the sample", 1, -345, 5), ("India salary guide in USD", "Hub + 6 roles · new", 1, 345, 5),
      ("15 hire-a-role pages", "Programmatic · new", 2, -345, 175), (f"{_gr + _gn} employer guides", f"{_gr} refresh · {_gn} new", 2, -115, 190), ("EOR vs entity calculator", "Tool · new", 2, 115, 190), ("What is an EOR", "Glossary · refresh", 2, 345, 175)]
sp = []
for lab, sub, w, dx, dy in SP:
    x, y = cx + dx, cy + dy
    col = "#4F8A10" if w == 1 else "#8FB35E"
    dash = "" if w == 1 else 'stroke-dasharray="6 5"'
    sp.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{col}" stroke-width="{2.5 if w==1 else 1.5}" {dash}/>')
nodes = []
for lab, sub, w, dx, dy in SP:
    x, y = cx + dx, cy + dy
    nodes.append(f'<g><rect x="{x-92}" y="{y-30}" width="184" height="60" rx="14" fill="#fff" stroke="{"#4F8A10" if w==1 else "#B8C7AE"}" stroke-width="1.5"/>'
                 f'<text x="{x}" y="{y-4}" text-anchor="middle" class="nt">{E(lab)}</text><text x="{x}" y="{y+16}" text-anchor="middle" class="ns">{E(sub)}</text></g>')
hub = (f'<g><rect x="{cx-175}" y="{cy-44}" width="350" height="88" rx="18" fill="#0B1F14"/>'
       f'<text x="{cx}" y="{cy-10}" text-anchor="middle" class="ht">Employer of Record India</text><text x="{cx}" y="{cy+14}" text-anchor="middle" class="hs">Guide depth + the page that sells · $199</text>'
       f'<text x="{cx}" y="{cy+32}" text-anchor="middle" class="hs2">/employer-of-record/india/ · replaces /eor/ and /eor-2/</text></g>')
LINKED = ["Payroll compliance", "Company registration", "Offshore teams and GCCs"]
lk = ['<text x="490" y="506" text-anchor="middle" class="ns">Linked out to other Paybooks offers, not duplicated</text>']
for k, name in enumerate(LINKED):
    x = 490 + (k - 1) * 230
    lk.append(f'<rect x="{x-105}" y="516" width="210" height="34" rx="17" fill="#F1F3F0" stroke="#C9D0C5"/><text x="{x}" y="538" text-anchor="middle" class="ns">{E(name)}</text>')
chart_map = (f'<svg viewBox="0 0 980 615" class="chart map" role="img" aria-label="Hub and spoke page map">{"".join(sp)}{hub}{"".join(nodes)}{"".join(lk)}'
             f'<g transform="translate(20,598)"><line x1="0" y1="0" x2="34" y2="0" stroke="#4F8A10" stroke-width="2.5"/><text x="42" y="5" class="ns">Wave 1: ships with the new site</text>'
             f'<line x1="270" y1="0" x2="304" y2="0" stroke="#8FB35E" stroke-width="1.5" stroke-dasharray="6 5"/><text x="312" y="5" class="ns">Wave 2: follows after launch</text></g></svg>')

tgt_vol = sum(agg[c][1] for c in ["C1", "C2", "C3", "C4", "C6", "C7", "C8"]) + CDEM + RV + SV + GAPV
tgt_n = sum(agg[c][0] for c in ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"])
w1_vol = sum(agg[c][1] for c in ["C1", "C2", "C3", "C4"])

# ---------- inventory table ----------
VC = {"Refresh": "#4F8A10", "Merge": "#8FB35E", "Redirect": "#F26B1D", "Create": "#0B1F14"}
def vtag(v): return f'<span class="vt" style="--c:{VC[v]}">{v}</span>'
inv_rows = "".join(f'<tr><td><code>{E(u)}</code><div class="mut">{fmt(PGW(u))} words</div></td><td>{vtag(v)}</td><td><b>{E(b)}</b><div class="mut">{E(r)}</div></td></tr>' for u, v, b, r in INV)
reuse_rows = "".join(f'<tr><td><code>{E(u)}</code></td><td>{vtag(v)}</td><td><b>{E(b)}</b><div class="mut">{E(r)}</div></td></tr>' for u, v, b, r in REUSE)
new_rows = "".join(f'<tr><td>{E(t)}</td><td><b>{E(n)}</b><div class="mut"><code>{E(u)}</code></div></td><td class="mut">{E(k)}</td><td class="n">{fmt(v) if v else "–"}</td></tr>' for t, n, u, k, v in NEW)
nref = sum(1 for x in INV + REUSE if x[1] == "Refresh"); nmer = sum(1 for x in INV + REUSE if x[1] in ("Merge", "Redirect")); nnew = len(NEW) + 14 + 6
total_pages = nref + nnew
W1N = 17; W1V = w1_vol + CDEM + SV; W2V = tgt_vol - W1V
g_ref = sum(1 for x in REUSE if x[1] == "Refresh") + 2; g_new = sum(1 for x in NEW if x[0] == "Employer guides"); w2_n = total_pages - W1N
eor_words = sum(PGW(u) for u, *_ in INV)

# ---------- chart: comparison layer ----------
cmx = max(n for _, n in CC)
cc = ['<text x="170" y="14" class="hd">Alternatives, "vs" and "best" pages</text>']
for i, (n, c) in enumerate(CC):
    y = 30 + i * 40; me = n == "Paybooks"; w = max(4, 620 * c / cmx)
    fw = ' font-weight="700"' if me else ""
    cc.append(f'<text x="0" y="{y+18}" class="lb"{fw}>{E(n)}</text><rect x="170" y="{y}" width="{w:.0f}" height="24" rx="6" fill="{"#F26B1D" if me else "#B8C7AE"}"/>'
              f'<text x="{170+w+8:.0f}" y="{y+18}" class="vl">{c}</text>')
chart_cmp = f'<svg viewBox="0 0 980 {30+len(CC)*40}" class="chart" role="img" aria-label="Comparison pages per competitor">{"".join(cc)}</svg>'

# ---------- programmatic SEO ----------
roles = json.load(open(f"{H}/pseo_roles.json"))
rmx = max(r["vol"] for r in roles)
rr = []
for i, r in enumerate(roles):
    y = i * 34; w = max(4, 400 * r["vol"] / rmx); wave = "#4F8A10" if i < 5 else "#9FC76A"
    kd = f'KD {r["kdmin"]}–{r["kdmax"]}' if r["kdmin"] is not None else "KD –"
    rr.append(f'<text x="0" y="{y+18}" class="lb">{E(r["name"])}</text><rect x="380" y="{y+4}" width="{w:.0f}" height="20" rx="5" fill="{wave}"/>'
              f'<text x="{380+w+8:.0f}" y="{y+19}" class="vl">{fmt(r["vol"])}</text><text x="975" y="{y+19}" class="ax" text-anchor="end">{r["n"]} kw · {kd}</text>')
chart_roles = f'<svg viewBox="0 0 980 {len(roles)*34}" class="chart" role="img" aria-label="Hire role in India demand by role">{"".join(rr)}</svg>'

CSS = """
:root{--ink:#101828;--ink2:#344054;--muted:#667085;--line:#E4E9E1;--bg:#F6F8F3;--green:#4F8A10;--g600:#3E6E0C;--g100:#E9F3DC;--forest:#0B1F14;--lime:#9FD35C;--orange:#F26B1D;--o100:#FDEBDD}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
.hero{background:radial-gradient(900px 420px at 85% 0%,rgba(79,138,16,.35),transparent 60%),var(--forest);color:#fff;padding:72px 0 64px}
.eyebrow{font:700 12px/1 Inter;letter-spacing:.14em;text-transform:uppercase;color:var(--lime)}
.hero h1{font:600 clamp(40px,5vw,62px)/1.04 "Instrument Sans",sans-serif;letter-spacing:-.035em;margin:16px 0 18px;max-width:880px}
.hero h1 em{font-style:normal;color:var(--lime)}.hero p.sub{font-size:19px;color:#C9D9C2;max-width:760px;margin:0}
.kp{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,.12);border-radius:18px;overflow:hidden;margin-top:40px}
.kp div{background:#0F2A1B;padding:20px 22px}.kp b{display:block;font:600 34px/1.1 "Instrument Sans";color:var(--lime)}.kp span{font-size:13.5px;color:#BFD3B9}
.toc{position:fixed;right:18px;top:50%;transform:translateY(-50%);z-index:30;display:flex;flex-direction:column;align-items:flex-end;gap:2px}
.toc a{position:relative;display:flex;align-items:center;justify-content:flex-end;width:40px;height:20px;text-decoration:none}
.toc a::after{content:"";display:block;width:16px;height:3px;border-radius:2px;background:#C9CED6;transition:width .2s,background .2s}
.toc a:hover::after{width:24px;background:#8A94A0}
.toc a.on::after{width:28px;background:#8A94A0}
.toc a span{position:absolute;right:48px;top:50%;transform:translate(6px,-50%);opacity:0;pointer-events:none;white-space:nowrap;background:#fff;color:var(--ink);font:500 15px Inter,sans-serif;padding:8px 14px;border-radius:10px;box-shadow:0 8px 24px -8px rgba(20,26,31,.22),0 1px 2px rgba(20,26,31,.06);transition:opacity .15s,transform .15s}
.toc a:hover span,.toc a:focus-visible span,.toc a.on span{opacity:1;transform:translate(0,-50%)}.toc a.on span{font-weight:600}
@media(max-width:900px){.toc{display:none}}
section{padding:72px 0 16px}.num{font:600 13px "Instrument Sans";color:var(--green);letter-spacing:.08em}
h2{font:600 clamp(30px,3.2vw,44px)/1.1 "Instrument Sans",sans-serif;letter-spacing:-.03em;margin:8px 0 12px;max-width:820px}
.lead{font-size:17.5px;line-height:1.65;color:#5B6470;max-width:780px;margin:0 0 28px}
.take{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.take div{background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px}
.take i{font:600 13px "Instrument Sans";font-style:normal;color:#fff;background:var(--green);border-radius:8px;padding:3px 9px}.take b{display:block;font:600 20px/1.25 "Instrument Sans";margin:0 0 8px}.take p{margin:0;color:var(--ink2);font-size:15px}
.panel{background:#fff;border:1px solid var(--line);border-radius:20px;padding:28px 30px}
.chart{width:100%;height:auto;display:block}.chart .lb{font:500 14px Inter;fill:#344054}.chart .vl{font:700 14px Inter;fill:#101828}.chart .ax{font:12px Inter;fill:#667085}
.chart .hd{font:700 12px Inter;fill:#667085;letter-spacing:.06em;text-transform:uppercase}.chart .gl{stroke:#E4E9E1;stroke-width:1}.chart .pbl{font:700 13px Inter;fill:#0B1F14}.chart .mutt{fill:#98A2B3;font-size:12.5px}
.map .nt{font:600 14px "Instrument Sans";fill:#101828}.map .ns{font:12.5px Inter;fill:#667085}.map .ht{font:600 20px "Instrument Sans";fill:#fff}.map .hs{font:600 13px Inter;fill:#9FD35C}.map .hs2{font:12px Inter;fill:#BFD3B9}
.callout{display:flex;gap:18px;align-items:flex-start;background:var(--g100);border-radius:16px;padding:18px 22px;margin-top:18px}.callout b{font:600 28px/1 "Instrument Sans";color:var(--g600);white-space:nowrap}.callout p{margin:0;color:var(--ink2);font-size:15px}
.legend{display:flex;gap:18px;flex-wrap:wrap;font-size:13.5px;color:var(--muted);margin-top:10px}.legend span::before{content:"";display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px;vertical-align:-1px;background:var(--c)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px 24px}.card b{display:block;font:600 18px/1.3 "Instrument Sans";margin-bottom:6px}.card p{margin:0;font-size:15px;color:var(--ink2)}
.card.acc{border-left:5px solid var(--green)}
.subh{margin:26px 0 10px;font:600 21px "Instrument Sans";letter-spacing:-.02em}
.waves{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:18px}.wave{border-radius:18px;padding:22px 24px}.wave.w1{background:var(--forest);color:#fff}.wave.w2{background:#fff;border:1px solid var(--line)}
.wave h3{margin:0 0 4px;font:600 20px "Instrument Sans"}.wave .m{font-size:13.5px;margin-bottom:12px}.wave.w1 .m{color:var(--lime)}.wave.w2 .m{color:var(--g600)}
.wave ul{margin:0;padding-left:18px}.wave li{margin:6px 0;font-size:15px}.wave.w1 li{color:#DDE8D6}
.asks{counter-reset:a;list-style:none;padding:0;margin:0;display:grid;gap:10px}.asks li{counter-increment:a;background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px 16px 58px;position:relative;font-size:15.5px}
.asks li::before{content:counter(a);position:absolute;left:18px;top:14px;width:28px;height:28px;border-radius:50%;background:var(--orange);color:#fff;font:600 14px/28px "Instrument Sans";text-align:center}.asks b{display:block}
.blk{background:#fff;border:1px solid var(--line);border-radius:16px;margin:10px 0}.blk>summary{cursor:pointer;list-style:none;padding:16px 20px;font:600 16px "Instrument Sans";display:flex;justify-content:space-between}.blk>summary::-webkit-details-marker{display:none}.blk>summary::after{content:"+";color:var(--green);font-size:20px}.blk[open]>summary::after{content:"−"}.blk .tw,.blk .note{margin:0 16px 16px}
.appx{padding-bottom:40px}.appx>details{background:#fff;border:1px solid var(--line);border-radius:16px;margin:10px 0}.appx>details>summary{cursor:pointer;list-style:none;padding:18px 22px;font:600 17px "Instrument Sans";display:flex;justify-content:space-between}
.appx>details>summary::-webkit-details-marker{display:none}.appx>details>summary::after{content:"+";color:var(--green);font-size:22px}.appx>details[open]>summary::after{content:"−"}.appx .in{padding:0 22px 22px}
table{width:100%;border-collapse:collapse;font-size:13.5px}th{text-align:left;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:9px 10px;border-bottom:1px solid var(--line);background:#FAFBF8}
td{padding:8px 10px;border-bottom:1px solid #EEF1EC;vertical-align:top}.n{text-align:right;white-space:nowrap}.tw{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:#fff}tr.me td{background:var(--g100);font-weight:600}
.mut{color:var(--muted);font-size:12.5px}code{font-size:12.5px;background:#F2F5EE;border-radius:6px;padding:1px 6px;color:var(--g600)}
details.topic{border:1px solid var(--line);border-radius:12px;margin:8px 0;background:#FCFDFB}details.topic>summary{cursor:pointer;list-style:none;display:flex;gap:10px;align-items:center;padding:12px 14px;flex-wrap:wrap}
details.topic>summary::-webkit-details-marker{display:none}.tt{font-weight:600}.cnt{margin-left:auto;font-size:12.5px;color:var(--muted)}.tag{font-size:11px;font-weight:700;border-radius:999px;padding:3px 9px}.tag.lp{background:var(--g100);color:var(--g600)}.tag.x{background:#F2F4F7;color:#475467}
.tbody{padding:0 14px 14px}.cl3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.cl3 h4{margin:0 0 6px;font:600 13.5px "Instrument Sans"}.cl3 p{margin:0 0 6px;font-size:13.5px;color:var(--ink2)}
details.inner{border:1px dashed var(--line);border-radius:10px;margin-top:6px}details.inner>summary{cursor:pointer;padding:9px 12px;font-weight:600;color:var(--g600);font-size:13.5px}details.inner .tw{margin:0 10px 10px}
.pbs{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pb{border:1px solid var(--line);border-radius:12px;padding:14px 16px}.pb p{margin:6px 0 0;font-size:13.5px;color:var(--ink2)}.pbh{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.pbh b{font:600 15px "Instrument Sans"}.dr{font-size:12px;color:var(--muted)}.pill{margin-left:auto;font-size:11px;font-weight:700;background:var(--o100);color:#B54708;border-radius:999px;padding:2px 8px}
.note{font-size:13px;color:var(--muted);margin-top:12px}
.vt{display:inline-block;font:700 11.5px Inter;color:#fff;background:var(--c);border-radius:999px;padding:3px 10px}
.big3{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border-radius:18px;overflow:hidden;margin-bottom:18px}.big3 div{background:#fff;padding:20px 22px}.big3 b{display:block;font:600 32px/1.1 "Instrument Sans";color:var(--ink)}.big3 span{font-size:14px;color:var(--muted)}.big3 .bad b{color:var(--orange)}
.rc{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:18px}.rc div{border-radius:16px;padding:18px 20px;color:#fff}.rc b{display:block;font:600 34px/1 "Instrument Sans"}.rc span{font-size:14px}
footer{background:var(--forest);color:#BFD3B9;padding:32px 0;font-size:13.5px;margin-top:40px}
@media(max-width:820px){.big3,.rc,.kp,.take,.two,.waves,.cl3,.pbs{grid-template-columns:1fr}.panel{padding:18px}}
@media(max-width:700px){.tw table{min-width:640px}svg.chart{min-width:620px}*:has(> svg.chart){overflow-x:auto;-webkit-overflow-scrolling:touch}}
"""

PAGE = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EOR India Deep Dive</title><meta name="robots" content="noindex,nofollow">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><style>{CSS}.lnk{{text-decoration:underline;text-decoration-color:#9AA3AF;cursor:pointer}}a:hover .lnk{{fill:#F26B1D}}
</style></head><body>
<header class="hero"><div class="wrap"><a href="../" style="display:inline-block;margin-bottom:18px;color:#C9D9C2;font-size:14px;text-decoration:none">← Global Employer of Record strategy</a><br><span class="eyebrow">Employer of Record · Country deep dive · India</span>
<h1>Employer of Record in India: <em>country deep dive</em></h1>
<p class="sub">India is the first country page in the global Employer of Record plan, and the one Paybooks knows best. The top results are not held by the biggest brands. They are held by the deepest pages. {total_pages} well-built pages, in two waves, put Paybooks at the top of the searches that bring foreign companies hiring in India.</p>
<div class="kp"><div><b>{fmt(tgt_vol)}</b><span>monthly searches the plan targets, USA and India</span></div><div><b>{total_pages}</b><span>pages: {nref} refreshed from what Paybooks has, {nnew} new</span></div>
<div><b>DR 29</b><span>the lowest-authority site on page one today. Paybooks is DR 41</span></div><div><b>1,043</b><span>competitor India pages studied across 12 sites</span></div></div></div></header>
<nav class="toc" aria-label="Sections"><a href="#answer" aria-label="Findings"><span>Findings</span></a><a href="#prize" aria-label="Topic potential"><span>Topic potential</span></a><a href="#lesson" aria-label="What works"><span>What works</span></a><a href="#today" aria-label="Paybooks today"><span>Paybooks today</span></a><a href="#topics" aria-label="Competitor topics"><span>Competitor topics</span></a><a href="#page" aria-label="The winning page"><span>The winning page</span></a><a href="#plan" aria-label="The plan"><span>The plan</span></a><a href="#build" aria-label="Refresh or create"><span>Refresh or create</span></a><a href="#pseo" aria-label="Programmatic SEO"><span>Programmatic SEO</span></a><a href="#appendix" aria-label="Evidence"><span>Evidence</span></a></nav>
<main class="wrap">
<section id="answer"><span class="num">FINDINGS</span><h2>Three findings decide the strategy.</h2>
<div class="take"><div><b>Authority is not what decides this category.</b><p>On "employer of record india", page one runs from DR 81 (Deel) down to DR 29 (Infotree). For "PEO India", sites at DR 12 to 37 hold #3 to #10. Paybooks at DR 41 is already strong enough to rank.</p></div>
<div><b>Depth on the right page decides it.</b><p>Skuad ranks #1 for the cost query with one 8,658-word page, 35 headings and 19 tables. Wisemonk published 666 India pages, and its EOR page reaches only #10 in India. One deep page per real intent beats hundreds of thin ones.</p></div>
<div><b>No competitor covers all five India intents well.</b><p>The commercial page, hiring guide, PEO question, provider comparison and role-based hiring are each won by a different competitor. Paybooks can be the one site that answers all five, with the lowest published price and 12 years of India payroll behind it.</p></div></div></section>

<section id="prize"><span class="num">01 · TOPIC POTENTIAL</span><h2>{fmt(tgt_vol)} monthly searches from buyers hiring in India.</h2><p class="lead">Grouped by what the searcher wants. The dark-green groups ship first: the commercial core plus the salary guide, the topic that earns competitors the most visits. Together they carry {fmt(W1V)} searches a month.</p>
<div class="panel">{chart_prize}</div>
</section>



<section id="lesson"><span class="num">02 · WHAT WORKS</span><h2>Publishing more pages is not what wins.</h2><p class="lead">Wisemonk built 30 times more India pages than anyone else and earns almost nothing from EOR searches. Papaya built 17, each one a real answer, and earns the most.</p>
<div class="panel">{chart_depth}</div><p class="note">Visits are Ahrefs estimates for USA searches containing "employer of record", "EOR", "PEO" or "hire employees" plus "India", from each site's top 50 India keywords. Page counts come from each site's sitemap.</p></section>

<section id="today"><span class="num">03 · PAYBOOKS TODAY</span><h2>Paybooks already wrote the content. Search can't find it.</h2>
<p class="lead">Paybooks has {len(INV)} pages on Employer of Record, about {fmt(eor_words)} words in total. Together they rank for one keyword. The problem is not effort; it is structure.</p>
<div class="big3"><div><b>{len(INV)}</b><span>EOR pages on paybooks.in today</span></div><div><b>{fmt(eor_words)}</b><span>words of EOR content</span></div><div class="bad"><b>1</b><span>keyword ranking, "eor solutions" at #8 in India. Nothing in Google USA</span></div></div>
<h3 class="subh">Top issues on the current pages</h3>
<details class="blk" open><summary>{len(ISS)} issues, most damaging first</summary><div class="tw"><table><thead><tr><th class="n">#</th><th>Issue</th><th>Evidence</th><th>Fix in the plan</th></tr></thead><tbody>{iss_rows}</tbody></table></div></details>
<p class="note">Checked on the live pages on 24 Sep 2026: page source, sitemap, and word-level text comparison. Rankings from Ahrefs.</p></div></section>
<section id="topics"><span class="num">04 · COMPETITOR TOPICS</span><h2>Every topic that earns competitors traffic is now in the plan.</h2>
<p class="lead">{CT_NP} competitor pages earn search traffic in this category, spread across {CT_NT} topics and {CT_NC} competitors. {CT_IN} topics were already in the plan. {CT_ADD} are added now as new or refreshed employer guides. {CT_LINK} belong to other Paybooks offers, so the EOR pages link to them.</p>
<div class="rc"><div style="background:#4F8A10"><b>{CT_IN}</b><span>topics already in the plan</span></div><div style="background:#F26B1D"><b>{CT_ADD}</b><span>topics added now</span></div><div style="background:#8A94A0"><b>{CT_LINK}</b><span>topics linked to other Paybooks offers</span></div></div>
<details class="blk" open><summary>Topics ranked by competitor visits</summary><div class="tw"><table><thead><tr><th>Topic</th><th>Competitors earning traffic</th><th class="n">USA visits / mo</th><th class="n">India visits / mo</th><th>Biggest search</th><th>Where it sits in the plan</th></tr></thead><tbody>{CT_ROWS}</tbody></table></div></details>
<h3 class="subh">Each competitor's working pages</h3>
{CT_COMP}
<p class="note">Source: Ahrefs top pages, 20 Sep 2026. Google USA (top 15 India pages per site) and Google India (top 10), where the URL or the top search mentions India. Visits are Ahrefs estimates. {CT_NOISE} pages are left out: Indiana state pages, relocation, job listings, outsourcing and staffing services, and the competitors' own brand searches. {CT_ZERO} have no India page with traffic.</p></section>




<section id="page"><span class="num">05 · THE WINNING PAGE</span><h2>One deep page per intent, built better than Skuad's.</h2><p class="lead">The page that wins the commercial search is long, answers questions in its headings, and shows its numbers in tables. The Paybooks page adds what none of them combine: a published price broken down line by line, a live calculator, and Paybooks' "no penalties ever" promise.</p>
<div class="panel">{chart_page}</div></section>

<section id="plan"><span class="num">06 · THE PLAN</span><h2>One page that sells, surrounded by pages that feed it.</h2><p class="lead">Every other page answers one kind of search and links to the Employer of Record India page. All URLs are proposed for the new site; each refreshed page redirects from its current address.</p>
<div class="panel">{chart_map}</div>
<div class="waves"><div class="wave w1"><h3>Wave 1 · the commercial core</h3><div class="m">{W1N} pages · {fmt(W1V)} searches a month · ships with the new site</div><ul>
<li>Employer of Record India at /employer-of-record/india/: the deep guide and the page that sells in one, replacing /eor/ and /eor-2/ (sample built)</li><li>India employee cost calculator (built into the sample)</li><li>Hire employees in India, the step-by-step guide (refresh)</li><li>PEO in India, and why it means EOR (refresh)</li><li>Best EOR providers for India, with published prices (refresh)</li><li>5 comparison pages: Deel and Remote alternatives, Paybooks vs Deel, Deel vs Remote vs Rippling, EOR pricing compared (new)</li><li>India salary guide in USD, hub + 6 role pages (new). Moved up: average salary is the topic that earns competitors the most visits, about 1,100 a month</li><li>7 overlapping EOR pages merged in and redirected, including the duplicate /eor-2/</li></ul></div>
<div class="wave w2"><h3>Wave 2 · widening the net</h3><div class="m">{w2_n} pages · {fmt(W2V)} searches a month · follows after launch</div><ul>
<li>15 "hire [role] in India" pages, launched 5 at a time (new)</li><li>{g_ref + g_new} employer guides: {g_ref} refreshed from existing Paybooks articles, {g_new} new. Launched in order of competitor visits: working hours and overtime · employee benefits · termination and final pay · holidays and leave · minimum wage · contractors vs employees · contracts, offer letters and NDAs · maternity leave · labor laws · background checks · work permits and visas · salary structure · compliance checklist · hiring mistakes · permanent establishment risk · moving to your own entity</li><li>EOR vs own-entity calculator (new)</li><li>A short "what is an EOR" answer built for AI Overviews (refresh)</li><li>1 more merge: the leave-rules article folds into the holiday guide</li><li>Links out, not new pages: payroll compliance, company registration and offshore teams go to Paybooks' payroll and India office pages</li></ul></div></div></section>

<section id="build"><span class="num">07 · REFRESH OR CREATE</span><h2>What to refresh, what to merge, what to create.</h2>
<p class="lead">Every existing EOR page has a decision. Refreshing keeps the URL history and the work already paid for; merging stops pages competing; new pages fill what no Paybooks page covers.</p>
<div class="rc"><div style="background:#4F8A10"><b>{nref}</b><span>pages to refresh</span></div><div style="background:#8FB35E"><b>{nmer}</b><span>pages to merge and redirect</span></div><div style="background:#0B1F14"><b>{nnew}</b><span>pages to create</span></div></div>
<details class="blk" open><summary>Existing EOR pages: the verdict on each</summary><div class="tw"><table><thead><tr><th>Current page</th><th>Verdict</th><th>Becomes · why</th></tr></thead><tbody>{inv_rows}</tbody></table></div></details>
<details class="blk"><summary>Existing payroll articles to repurpose for EOR buyers</summary><div class="tw"><table><thead><tr><th>Current page</th><th>Verdict</th><th>Becomes · why</th></tr></thead><tbody>{reuse_rows}</tbody></table></div></details>
<details class="blk"><summary>New pages to create</summary><div class="tw"><table><thead><tr><th>Type</th><th>Page · proposed URL</th><th>Target searches</th><th class="n">Searches / mo</th></tr></thead><tbody>{new_rows}</tbody></table></div><p class="note">The programmatic sets count as 15 and 7 pages. Search volumes are Google USA from Ahrefs; guides with no volume are drawn from buyer-question research.</p></details></section>

<section id="pseo"><span class="num">08 · PROGRAMMATIC SEO</span><h2>One template, fifteen roles: the biggest demand in the category.</h2>
<p class="lead">Buyers search by the job they need to fill: "hire react native developers india", "hire .NET developers india". Rippling's biggest India page is exactly this. One template, filled with real data per role, covers {fmt(RV)} searches a month across 95 keywords, most at keyword difficulty 0 to 16. Some of these searchers want an agency; each page wins them by showing why hiring your own full-time employee through an EOR costs less and keeps the IP.</p>
<div class="panel">{chart_roles}<div class="legend"><span style="--c:#4F8A10">First 5 roles, launched in Wave 2</span><span style="--c:#9FC76A">Next 10, added once the first 5 rank</span></div></div>
<div class="two" style="margin-top:18px"><div class="card acc"><b>Template 1 · Hire [role] in India</b><p>15 pages at /hire-in-india/[role]/. Each carries data no one else combines: the salary band in USD, the all-in monthly cost from the calculator at that salary, where the talent concentrates, notice periods, a 10-day hiring timeline, and an FAQ. Similar roles share a page (PHP, Laravel and CodeIgniter are one page), so no two pages compete.</p></div>
<div class="card acc"><b>Template 2 · India salary guide in USD</b><p>A hub for "average salary in India" and "India average salary in USD" ({fmt(SV)} searches a month with its role pages), plus 6 role salary pages: software engineer, data analyst, data scientist, AI engineer, accountant, digital marketing. Every salary page links to its hire page and the calculator.</p></div></div>
<details class="blk" style="margin-top:14px"><summary>Templates we checked and are not building</summary><div class="tw"><table><thead><tr><th>Template</th><th>Who runs it</th><th>Demand (Google USA)</th><th>Decision</th></tr></thead><tbody>
<tr><td><b>Hire in [Indian city]</b></td><td>Wisemonk, 25 pages</td><td>"hire developers in bangalore": 0 a month</td><td>Not built. Cities go inside each role page instead.</td></tr>
<tr><td><b>[Buyer country] company hiring in India</b></td><td>Wisemonk, 118 pages</td><td>"us company hiring employees in india": 90 a month; UK, Australia, Canada: no measurable volume</td><td>Not built as a set. One section on the hiring guide covers it.</td></tr>
<tr><td><b>Cost to hire [role] in India</b></td><td>Wisemonk, Oyster</td><td>Every variant 10 a month or less</td><td>Not built. Cost sits on every role page.</td></tr>
<tr><td><b>EOR in [other country]</b></td><td>Remote, Playroll, Skuad, Multiplier and others</td><td>Covered by the global plan</td><td>Built in the global country layer: one product page per country. <a href="../">See the global strategy</a>.</td></tr>
</tbody></table></div><p class="note">Wisemonk built 143 city and buyer-country pages and earns almost no EOR traffic from them: the evidence that templates without demand or unique data do not pay back.</p></details>
<details class="blk"><summary>Quality rules for every programmatic page</summary><div class="tw"><table><tbody>
<tr><td><b>Unique data, not swapped words</b></td><td>Each page must carry its own salary band, cost and FAQ. A page without them stays unpublished.</td></tr>
<tr><td><b>Launch in batches</b></td><td>5 roles first. Add the next 10 only when the first 5 are indexed and ranking.</td></tr>
<tr><td><b>One hub, clear links</b></td><td>/hire-in-india/ lists every role and links to the Employer of Record India page, the calculator and the salary guide.</td></tr>
<tr><td><b>Refreshed yearly</b></td><td>Salary and cost data updated each year, with the date shown on the page.</td></tr>
</tbody></table></div></details></section>





<section id="appendix" class="appx"><span class="num">APPENDIX · THE EVIDENCE</span><h2>Everything behind the numbers.</h2>
<details><summary>Live search results, query by query</summary><div class="in">{"".join(g["serp_html"])}</div></details>
<details><summary>Page-one pages, measured</summary><div class="in"><div class="tw"><table><thead><tr><th>Page</th><th>Type</th><th class="n">Words</th><th class="n">Headings</th><th class="n">Question headings</th><th class="n">Tables</th><th>FAQ</th><th>Price shown</th></tr></thead><tbody>{g["bench_rows"]}</tbody></table></div></div></details>
<details><summary>Competitor playbooks</summary><div class="in"><div class="pbs">{g["pb_html"]}</div></div></details>
<details><summary>Keyword clusters and every target keyword</summary><div class="in">{"".join(g["cl_html"])}<p class="note"><a href="eor-keyword-clusters.csv" download>Download all keywords with their clusters (CSV)</a></p></div></details>

<details><summary>Method and sources</summary><div class="in"><div class="tw"><table><tbody>
<tr><td><b>Competitor sitemaps</b></td><td>12 sites fetched in full, about 131,000 URLs; 1,043 English India pages after removing translated copies.</td></tr>
<tr><td><b>Live search results</b></td><td>Ahrefs SERP Overview for India EOR searches in Google USA and Google India, 24 September 2026.</td></tr>
<tr><td><b>Page measurement</b></td><td>Every page-one URL fetched and measured for words, headings, tables, FAQ and prices.</td></tr>
<tr><td><b>Competitor keywords</b></td><td>Ahrefs organic keywords containing "india" for Deel, Papaya, Skuad and Rippling; {g["gap_n"]} relevant keywords added to the original pull.</td></tr>
<tr><td><b>Keyword pull</b></td><td>Ahrefs Keywords Explorer, 161 Employer of Record keywords, 23 September 2026; {fmt(tgt_n)} targeted after clustering.</td></tr>
</tbody></table></div></div></details></section>
</main><footer><div class="wrap">Prepared by Mohan Kumar Allada for the TransPerfect Paybooks SEO proposal · 24 September 2026 · Data: Ahrefs, competitor sitemaps, live page measurement</div></footer><script>(function(){{var L=[].slice.call(document.querySelectorAll('.toc a'));var S=L.map(function(a){{return document.querySelector(a.getAttribute('href'))}});function f(){{var y=window.scrollY+window.innerHeight*0.35,k=0;S.forEach(function(e,i){{if(e&&e.offsetTop<=y)k=i}});L.forEach(function(a,i){{a.classList.toggle('on',i===k)}})}}window.addEventListener('scroll',f,{{passive:true}});f()}})();</script><script src="../../assets/protect.js" defer></script></body></html>'''
os.makedirs(f"{H}/out/india", exist_ok=True); open(f"{H}/out/india/index.html", "w", encoding="utf-8").write(PAGE)
print("ceo page written", tgt_vol, w1_vol, [(n, p, t) for n, p, t, _ in DV])
