"""Sample site generator on the JC Website 2.0 template (Figma DPHOzmgd3Hp4BohDBKaNh2). LPs use the pain > promise > outcome schema; guides use the article schema."""
import json, os, html, pathlib, importlib, sys, re
sys.path.insert(0, os.path.dirname(__file__))
C = importlib.import_module("content")
from render_eor import render_eor
from eor_page import VIDEO_ID
OUT = pathlib.Path(__file__).resolve().parent.parent / "out"; SITE = C.SITE
def esc(s): return html.escape(s, quote=True)
def rel(d): return "../"*d
def accent(h1):  # *word* -> <em>word</em>
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", esc(h1))
def header(d):
    r=rel(d); short={"Employer of Record":"Employer of Record","Multi-Country Payroll":"Payroll","Managed India Office":"India Office","Global HCM":"HCM"}
    links="".join(f'<a href="{r}{p["slug"]}/">{esc(short.get(p["nav"],p["nav"]))}</a>' for p in C.PAGES if p.get("nav"))
    return (f'<div class="sample"><b>Sample build for pitch review</b> · Paybooks design system draft, JC 2.0 component logic · not a live property</div>'
            f'<header class="hdr"><div class="wrap"><a class="brand" href="{r}index.html"><img src="{r}assets/mark.png" alt="Paybooks" width="44" height="44"><span class="wm"><b>paybooks</b><small>A TransPerfect company</small></span></a><nav class="nav">{links}<a href="{r}resources/">Resources</a></nav>'
            f'<div class="btns"><a class="btn ghost" href="{r}contact.html">Book a call</a><a class="btn" href="{r}contact.html">Get a quote</a></div></div></header>')
def footer(d):
    r=rel(d); cols=""
    for hub in C.HUBS:
        items="".join(f'<a href="{r}{p["slug"]}/">{esc(p["nav_short"])}</a>' for p in C.PAGES if p.get("hub")==hub["id"] and p.get("nav_short"))
        cols+=f'<div><h4>{esc(hub["name"])}</h4>{items}</div>'
    return (f'<footer class="ftr"><div class="wrap"><div><h4>Paybooks, a TransPerfect company</h4><p>Employer of Record, Multi-Country Payroll, Managed India Office and Global HCM for companies building teams in India and beyond. Sample prepared by Mohan Kumar Allada, {C.DATE}.</p></div>{cols}</div></footer>')
def crumbs(page,d):
    if not page["slug"]: return ""
    r=rel(d); parts=[f'<a href="{r}index.html">Home</a>']
    if page.get("hub"):
        hub=next(h for h in C.HUBS if h["id"]==page["hub"])
        if hub["slug"]!=page["slug"]: parts.append(f'<a href="{r}{hub["slug"]}/">{esc(hub["name"])}</a>')
    if page.get("section")=="resources": parts.append(f'<a href="{r}resources/">Resources</a>')
    parts.append(esc(page["crumb"])); return '<nav class="crumbs" aria-label="Breadcrumb">'+" › ".join(parts)+"</nav>"
def schema(page,url):
    ld=[{"@context":"https://schema.org","@type":"Organization","name":"Paybooks, a TransPerfect company","url":SITE,"parentOrganization":{"@type":"Organization","name":"TransPerfect","url":"https://www.transperfect.com/"}}]
    items=[{"@type":"ListItem","position":1,"name":"Home","item":SITE}]
    if page.get("hub"):
        hub=next(h for h in C.HUBS if h["id"]==page["hub"])
        if hub["slug"]!=page["slug"]: items.append({"@type":"ListItem","position":len(items)+1,"name":hub["name"],"item":f'{SITE}{hub["slug"]}/'})
    items.append({"@type":"ListItem","position":len(items)+1,"name":page["crumb"],"item":url})
    ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items})
    if page.get("faq"): ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in page["faq"]]})
    if page.get("type")=="service": ld.append({"@context":"https://schema.org","@type":"Service","name":re.sub(r"\*","",page["h1"]),"serviceType":page.get("service_type",page["crumb"]),"provider":{"@type":"Organization","name":"Paybooks, a TransPerfect company"},"areaServed":page.get("area","India"),"description":page["description"]})
    if page.get("type")=="article": ld.append({"@context":"https://schema.org","@type":"Article","headline":page["h1"],"description":page["description"],"dateModified":C.DATE_ISO,"author":{"@type":"Organization","name":"Paybooks compliance team"},"publisher":{"@type":"Organization","name":"Paybooks, a TransPerfect company"}})
    return "".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in ld)
IC='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12l5 5L20 6"/></svg>'
def table(head,rows,cap=None,hl=None):
    th="".join(f'<th{" class=hl" if hl==i else ""}>{esc(h)}</th>' for i,h in enumerate(head))
    tr="".join("<tr>"+"".join(f'<td{" class=hl" if hl==i else ""}>{c}</td>' for i,c in enumerate(row))+"</tr>" for row in rows)
    return f'<div class="t-wrap"><table class="cmp"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'+(f'<p class="fine">{cap}</p>' if cap else "")
def lp_html(p,d):
    r=rel(d)
    cta2=('<a class="btn ghost" href="'+r+p["cta2_href"]+'">'+esc(p["cta2"])+'</a>') if p.get("cta2") else ""
    trust="".join(f"<li><b>{esc(v)}</b>{esc(l)}</li>" for v,l in p["trust"])
    hero=(f'<section class="hero"><div class="wrap">{crumbs(p,d)}<div class="badge"><span>{esc(p.get("badge","PB"))}</span></div><span class="eyebrow">{esc(p["eyebrow"])}</span>'
          f'<h1>{accent(p["h1"])}</h1><p class="sub">{p["sub"]}</p><div class="btns"><a class="btn" href="{r}contact.html">{esc(p["cta"])}</a>'
          f'{cta2}</div>'
          f'<p class="trust-t">{esc(p.get("trust_t","Trusted by 3,000+ employers since 2012"))}</p><ul class="trust">{trust}</ul></div></section>')
    pain=p["pain"]
    pain_html=(f'<section class="sec" id="problem"><div class="wrap"><div class="sec-head"><span class="eyebrow">Sounds familiar?</span><h2>{esc(pain["h2"])}</h2><p>{pain["sub"]}</p></div>'
               f'<ul class="cards">'+"".join(f'<li class="card pain">{IC}<h3>{esc(c[0])}</h3><p>{c[1]}</p></li>' for c in pain["cards"])+'</ul></div></section>')
    o=p["outcome"]
    out_html=(f'<section class="sec grey" id="outcome"><div class="wrap"><div class="sec-head"><span class="eyebrow">What changes with Paybooks</span><h2>{esc(o["h2"])}</h2><p>{o["sub"]}</p></div>'
              f'<blockquote class="quote">{o["quote"]}<cite>{esc(o["cite"])}</cite></blockquote><div class="stats">'+"".join(f"<div><b>{esc(v)}</b><span>{esc(l)}</span></div>" for v,l in o["stats"])+'</div></div></section>')
    rows=""
    for i,row in enumerate(p["how"]["rows"]):
        nl="".join(f'<li><i>{j+1:02d}</i><span><b>{esc(t)}</b> {x}</span></li>' for j,(t,x) in enumerate(row["points"]))
        vis=row["visual"]; vt="".join(f"<tr>{''.join(f'<td>{c}</td>' for c in rr)}</tr>" for rr in vis["rows"])
        vh="".join(f"<th>{esc(h)}</th>" for h in vis.get("head",[]))
        visual=f'<div class="visual"><h4>{esc(vis["title"])}</h4><p class="vs">{esc(vis["sub"])}</p>{("<p class=big>"+esc(vis["big"])+" <span class=up>"+esc(vis.get("up",""))+"</span></p>") if vis.get("big") else ""}<table>{("<thead><tr>"+vh+"</tr></thead>") if vh else ""}<tbody>{vt}</tbody></table></div>'
        rows+=f'<div class="row{" flip" if i%2 else ""}"><div class="visual-wrap visual-slot">{visual}</div><div><h3>{esc(row["h3"])}</h3><p>{row["p"]}</p><ul class="nlist">{nl}</ul></div></div>'
    how_html=f'<section class="sec" id="how"><div class="wrap"><div class="sec-head left"><div><span class="eyebrow">How it works</span><h2>{esc(p["how"]["h2"])}</h2></div><p>{p["how"]["sub"]}</p></div><div class="bento">{rows}</div></div></section>'
    cmp=p["compare"]
    cmp_html=f'<section class="sec grey" id="compare"><div class="wrap"><div class="sec-head"><span class="eyebrow">Compare</span><h2>{esc(cmp["h2"])}</h2><p>{cmp["sub"]}</p></div>{table(cmp["head"],cmp["rows"],cmp.get("cap"),cmp.get("hl"))}</div></section>'
    pr=p["proof"]
    proof_html=(f'<section class="dark" id="proof"><div class="wrap"><div class="band-head"><div><span class="eyebrow">{esc(pr["eyebrow"])}</span><h2>{esc(pr["h2"])}</h2></div><div class="btns"><a class="btn" href="{r}contact.html">{esc(p["cta"])}</a></div></div>'
                f'<ul class="cards">'+"".join(f'<li class="card"><h3>{esc(c[0])}</h3><p>{c[1]}</p>{("<div class=chips>"+"".join(f"<span>{esc(x)}</span>" for x in c[2])+"</div>") if len(c)>2 else ""}</li>' for c in pr["cards"])+'</ul>'
                f'<div class="stats">'+"".join(f"<div><b>{esc(v)}</b><span>{esc(l)}</span></div>" for v,l in pr["stats"])+'</div></div></section>')
    faq=(f'<section class="sec" id="faq"><div class="wrap"><div class="faq"><div><span class="eyebrow">FAQ</span><h2>Everything you might be wondering</h2><p class="lead">Straight answers from the team that runs this every month. Anything missing, ask us.</p><div class="btns"><a class="btn" href="{r}contact.html">{esc(p["cta"])}</a></div></div><div>'
         +"".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q,a in p["faq"])+'</div></div></div></section>')
    deeper=('<section class="sec grey"><div class="wrap"><div class="sec-head left"><div><span class="eyebrow">Go deeper</span><h2>Guides for this decision</h2></div><p>Dated, sourced and written by the compliance team, not marketing.</p></div><div class="deeper">'
            +"".join(f'<a href="{r}{q["slug"]}/"><h3>{esc(q["h1"])}</h3><p>{esc(q["description"])}</p></a>' for q in C.PAGES if q["slug"] in p.get("deeper",[]))+'</div></div></section>') if p.get("deeper") else ""
    cta=f'<section class="cta"><div class="wrap"><div class="badge"><span>PB</span></div><h2>{esc(p["cta_h"])}</h2><p>{p["cta_p"]}</p><div class="btns"><a class="btn" href="{r}contact.html">{esc(p["cta"])}</a>{cta2}</div></div></section>'
    return hero+pain_html+out_html+how_html+cmp_html+proof_html+faq+deeper+cta
def more(c,r):
    return ('<a class="more" href="'+r+c["href"]+'">'+esc(c.get("more","Read more"))+' &rarr;</a>') if c.get("href") else ""
def art_blocks(blocks,d):
    r=rel(d); out=[]
    for b in blocks:
        t=b["t"]
        if t=="h2": out.append(f'<h2>{esc(b["x"])}</h2>')
        elif t=="h3": out.append(f'<h3>{esc(b["x"])}</h3>')
        elif t=="p": out.append(f'<p>{b["x"]}</p>')
        elif t=="ul": out.append("<ul>"+"".join(f"<li>{i}</li>" for i in b["x"])+"</ul>")
        elif t=="steps": out.append('<ol class="steps">'+"".join(f"<li><b>{esc(s[0])}</b>{s[1]}</li>" for s in b["x"])+"</ol>")
        elif t=="table": out.append(table(b["head"],b["rows"],b.get("cap")))
        elif t=="cards": out.append('<ul class="cards">'+"".join(f'<li class="card">{("<span class=k>"+esc(c["k"])+"</span>") if c.get("k") else ""}<h3>{esc(c["h"])}</h3><p>{c["p"]}</p>{more(c,r)}</li>' for c in b["x"])+"</ul>")
        elif t=="notice": out.append(f'<div class="note">{b["x"]}</div>')
        elif t=="proof": out.append('<div class="proofrow">'+"".join(f"<div><b>{esc(v)}</b><span>{esc(l)}</span></div>" for v,l in b["x"])+"</div>")
        elif t=="deeper": out.append('<div class="deeper">'+"".join(f'<a href="{r}{q["slug"]}/"><h3>{esc(q["h1"])}</h3><p>{esc(q["description"])}</p></a>' for q in C.PAGES if q["slug"] in b["x"])+"</div>")
    return "\n".join(out)
def art_html(p,d):
    r=rel(d)
    hero=(f'<section class="hero"><div class="wrap">{crumbs(p,d)}<span class="eyebrow">{esc(p.get("pill","Guide"))}</span><h1>{esc(p["h1"])}</h1><p class="sub">{p["lead"]}</p>'
          f'<div class="answer">{p["answer"]}</div><p class="meta">Reviewed {C.DATE} · Paybooks compliance team · Sources linked in each section</p></div></section>')
    body="".join(f'<section class="sec{" grey" if s.get("alt") else ""}" id="{s.get("id","")}"><div class="wrap">'+(f'<h2>{esc(s["h2"])}</h2>' if s.get("h2") else "")+art_blocks(s["blocks"],d)+"</div></section>" for s in p["sections"])
    faq=(f'<section class="sec grey" id="faq"><div class="wrap"><div class="faq"><div><span class="eyebrow">FAQ</span><h2>Questions on this topic</h2></div><div>'+"".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q,a in p["faq"])+'</div></div></div></section>') if p.get("faq") else ""
    deeper=('<section class="sec"><div class="wrap"><span class="eyebrow">Related</span><h2>Go deeper</h2><div class="deeper" style="margin-top:20px">'+"".join(f'<a href="{r}{q["slug"]}/"><h3>{esc(q["h1"])}</h3><p>{esc(q["description"])}</p></a>' for q in C.PAGES if q["slug"] in p.get("deeper",[]))+'</div></div></section>') if p.get("deeper") else ""
    cta=f'<section class="cta"><div class="wrap"><div class="badge"><span>PB</span></div><h2>{esc(p.get("cta_h","Hiring or building in India?"))}</h2><p>{p.get("cta_p","Tell us the role, headcount and city. You get a fully costed answer in two working days.")}</p><div class="btns"><a class="btn" href="{r}contact.html">Talk to an expert</a></div></div></section>'
    return hero+body+faq+deeper+cta
def page_html(p):
    d=0 if p.get("type") in ("contact","home") or not p["slug"] else p["slug"].count("/")+1
    r=rel(d); url=f'{SITE}{p["slug"]}/' if p["slug"] else SITE
    body=render_eor(p,r,C,VIDEO_ID) if p.get("type")=="eor_v2" else (lp_html(p,d) if p.get("type") in ("service","home") else art_html(p,d))
    cls="art" if p.get("type") in ("article","hub","contact") else ""
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(p["title"])}</title><meta name="description" content="{esc(p["description"])}"><link rel="canonical" href="{url}"><meta name="robots" content="noindex,nofollow">'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@500;600;700&family=Inter:wght@400;500;600;700&family=Zilla+Slab:wght@300;400&display=swap" rel="stylesheet"><link rel="stylesheet" href="{r}assets/pb.css">{schema(p,url)}</head>'
            f'<body class="{cls}">{header(d)}<main>{body}</main>{footer(d)}</body></html>')
def build():
    for p in C.PAGES:
        dd=OUT/p["slug"] if p["slug"] else OUT; dd.mkdir(parents=True,exist_ok=True); (dd/"index.html").write_text(page_html(p))
    (OUT/"contact.html").write_text(page_html(C.CONTACT)); print(len(C.PAGES)+1,"pages written")
if __name__=="__main__": build()


SITE_ART="https://claude.ai/artifact/M1SdNknPs4NiqEXjwNF9RU/"
def build_standalone():
    """EOR page as its own artifact: nav anchors, guide links to the sample-site artifact, lean footer."""
    import re as _re
    p=next(x for x in C.PAGES if x.get("type")=="eor_v2")
    htmlp=page_html(p)
    htmlp=htmlp.replace('href="../index.html"','href="#top"')
    for slug,label in (("employer-of-record-india","Employer of Record"),):
        pass
    # nav: point hubs at sample-site artifact pages, keep EOR as top anchor
    htmlp=_re.sub(r'<nav class="nav">.*?</nav>', lambda m: _re.sub(r'<a href="[^"]*">','<a>',m.group(0)), htmlp, flags=_re.S)
    for slug in ("multi-country-payroll","managed-india-office","global-hcm","resources"):
        htmlp=htmlp.replace(f'href="../{slug}/"',f'href="{SITE_ART}{slug}/"')
    htmlp=htmlp.replace('href="../contact.html"','href="#faq"')
    htmlp=_re.sub(r'href="\.\./resources/([a-z0-9-]+)/"',lambda m:f'href="{SITE_ART}resources/{m.group(1)}/"',htmlp)
    htmlp=htmlp.replace('href="../assets/pb.css"','href="assets/pb.css"').replace('src="../assets/mark.png"','src="assets/mark.png"').replace('src="../assets/logos/','src="assets/logos/').replace('src="../assets/logos-t/','src="assets/logos-t/').replace('src="../assets/video-thumb.jpg"','src="assets/video-thumb.jpg"')
    htmlp=htmlp.replace('<body class="">','<body class="" id="top">')
    htmlp=_re.sub(r'<div class="sample">.*?</div>','',htmlp,count=1)
    # lean footer: drop hub columns
    htmlp=_re.sub(r'<footer class="ftr">.*?</footer>','<footer class="ftr"><div class="wrap" style="grid-template-columns:1fr"><div><h4>Paybooks, a TransPerfect company</h4><p>Employer of Record, Multi-Country Payroll, Managed India Office, and Global HCM for companies building teams in India and beyond.</p></div></div></footer>',htmlp,flags=_re.S)
    htmlp=htmlp.replace('<title>','<title>').replace('<link rel="canonical" href="https://www.paybooks.in/employer-of-record-india/">','<link rel="canonical" href="https://www.paybooks.in/employer-of-record-india/">')
    out=OUT.parent/"eor-standalone"; (out/"assets").mkdir(parents=True,exist_ok=True)
    (out/"index.html").write_text(htmlp); (out/"assets"/"pb.css").write_text((OUT/"assets"/"pb.css").read_text())
    import shutil; shutil.copytree(OUT/"assets"/"logos-t", out/"assets"/"logos-t", dirs_exist_ok=True); shutil.copy(OUT/"assets"/"video-thumb.jpg", out/"assets"/"video-thumb.jpg")
    print("standalone written", out)
if __name__=="__main__" and "standalone" in sys.argv: build_standalone()
