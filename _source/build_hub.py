"""Global Employer of Record hub (the site's main EOR landing page). Writes ../index.html.
Header, trust bar and reveal script come from lp_template.html (the earlier landing page)."""
import html, json, re, os
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "..", "index.html")
T = open(os.path.join(H, "lp_template.html")).read()
esc = lambda s: html.escape(s, quote=True)
HEADER = T[T.find("<body"):T.find("<main>")]
ts = T.find('<div class="trust">'); TRUST = T[ts:T.find("</div></div></div></div>", ts) + len("</div></div></div></div>")]
js0 = T.find("<script>(function(){var io="); REVEAL = T[js0:T.find("</script>", js0) + 9]
VID = ('<div class="vidhold" role="img" aria-label="Video placeholder"><div class="vh-frame"><span class="vh-mini"><svg width="16" height="16" viewBox="0 0 24 24" fill="#fff"><path d="M8 5v14l11-7z"/></svg></span>'
       '<span class="vh-cap"><b>How Paybooks EOR works</b><small>2-minute walkthrough</small></span><span class="vh-tag">Video</span></div></div>')
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>'
TICKS = '<li>No entity to set up</li><li>Local contracts and payroll</li><li>One monthly invoice</li>'
def head(n, eyebrow, h2, sub): return f'<div class="head rv"><span class="num">{n}</span><div><span class="eyebrow">{eyebrow}</span><h2>{esc(h2)}</h2><p>{sub}</p></div></div>'
def cards(items, cls="three"): return f'<ul class="cards {cls}">' + "".join(f'<li class="card"><div class="ic">{CHECK}</div><h3>{esc(h)}</h3><p>{t}</p></li>' for h, t in items) + "</ul>"
def table(hd, rows, hl=1):
    th = "".join(f'<th{" class=hl" if i == hl else ""}>{esc(h)}</th>' for i, h in enumerate(hd))
    tr = "".join("<tr>" + "".join(f'<td{" class=hl" if i == hl else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="t-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

TITLE = "Employer of Record (EOR) Services | Hire Anywhere Without an Entity | Paybooks, a TransPerfect company"
DESC = "Hire employees in other countries without setting up an entity. Paybooks becomes the legal employer and runs contracts, payroll, taxes and benefits under local law. Get a quote for a role."

hero = (f'<section class="hero v2"><div class="wrap"><div class="grid"><div><span class="cta2-tag hero-tag">Global Employer of Record</span>'
        '<h1>Hire anyone, anywhere. <em>No entity needed.</em></h1>'
        '<p class="sub">Paybooks becomes the legal employer of your people in another country. We run the local contract, payroll, taxes and benefits under that country’s law. You choose the people and direct their work.</p>'
        '<div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" href="#quote">Talk to an EOR expert</a></div>'
        f'<ul class="cta2-ticks hero-ticks">{TICKS}</ul></div>{VID}</div></div></section>{TRUST}')

how = ('<section class="sec" id="how"><div class="wrap">' + head("01", "How it works", "What an Employer of Record does",
       "An Employer of Record (EOR) is a company that legally employs people on your behalf in a country where you have no entity. The work, the team and the results stay yours.")
       + '<ul class="cparts"><li><span class="cp-n">1</span><div><b>You choose the person</b><p>Pick your hire and agree the role, pay and start date.</p></div></li>'
       '<li><span class="cp-n">2</span><div><b>Paybooks employs them</b><p>We sign the local employment contract and run payroll, taxes and benefits under local law.</p></div></li>'
       '<li><span class="cp-n">3</span><div><b>They work for you</b><p>You manage their work. You get one monthly invoice for salary, employer costs and our fee.</p></div></li></ul>'
       '<div class="raci" style="margin-top:28px"><div class="col you"><h3>You decide</h3><ul>'
       + "".join(f'<li><div><b>{esc(a)}</b><span>{esc(b)}</span></div></li>' for a, b in [
           ("Who to hire and what to pay", "We quote the full monthly cost first"), ("Day-to-day work, reviews, promotions", "Managers are yours"),
           ("Work hours, leave and remote rules", "Your policies, within local law"), ("Raises, bonuses, equity", "Processed in the next payroll"),
           ("When to part ways", "We follow the local rules"), ("When to open your own entity", "Your team moves over")])
       + '</ul></div><div class="col us"><h3>We take care of</h3><ul>'
       + "".join(f'<li><div><b>{esc(a)}</b><span>{esc(b)}</span></div></li>' for a, b in [
           ("The employment contract and legal liability", "Under the country’s labor law"), ("Payroll in local currency", "Paid on time, every month"),
           ("Taxes and social security", "Calculated, filed and paid"), ("Statutory benefits", "Plus any extras you choose"),
           ("Registrations and filings", "With the local authorities"), ("Exits and final pay", "Notice, severance and documents")])
       + '</ul></div></div></div></section>')

fit = ('<section class="sec alt" id="fit"><div class="wrap">' + head("02", "Start here", "Is an Employer of Record right for you?", "Find your situation to see which way of hiring fits best.")
       + table(["If you are", "Best option", "Why it fits", "Not recommended"], [
           ["Hiring 1 to 20 people in a country where you have no entity", "<b>Employer of Record</b>", "Hire within days. No entity to set up or close.", "Opening an entity first"],
           ["Testing a new market", "<b>Employer of Record</b>", "Hire now, decide on an entity once the market proves itself.", "Committing to an entity too early"],
           ["Paying contractors who work full time for you", "<b>EOR conversion</b>", "Removes the risk of treating employees as contractors.", "Leaving them as contractors"],
           ["Building a large team in one country", "<b>Your own entity, with Paybooks payroll</b>", "At scale, owning an entity usually costs less per person.", "EOR at any size"],
           ["Building a team in India", "<b>EOR, or a Managed India Office</b>", "Start on EOR. Move to your own India entity, run by Paybooks, as the team grows.", "Waiting to hire until an entity is ready"],
           ["Running your own entities in several countries", "<b>Multi-Country Payroll</b>", "One provider and one report for payroll in every country.", "A different payroll vendor per country"],
       ]) + '</div></section>')

COUNTRIES = [("India", "employer-of-record/india/", True), ("Philippines", "", False), ("Singapore", "", False), ("Poland", "", False),
             ("Germany", "", False), ("Switzerland", "", False), ("France", "", False), ("United Kingdom", "", False), ("Australia", "", False)]
cgrid = "".join(
    (f'<a class="cty live" href="{u}"><b>{c}</b><span>Employer costs, contracts and rules</span><em>Read the guide →</em></a>' if live else
     f'<div class="cty"><b>{c}</b><span>Employer costs, contracts and rules</span><em>Guide coming soon</em></div>') for c, u, live in COUNTRIES)
countries = ('<section class="sec" id="countries"><div class="wrap">' + head("03", "Countries", "Hire in the country you need",
             "Each country guide covers what it costs to employ someone there, the contract and benefits, notice and termination rules, and how long hiring takes.")
             + f'<div class="cgrid">{cgrid}</div></div></section>')

hire = ('<section class="sec alt" id="experience"><div class="wrap">' + head("04", "Your hire", "What your hire gets", "A real local job with a real local employer, from day one.")
        + cards([("A local employment contract", "In line with the country’s labor law, with your company, manager and role named."),
                 ("Pay on time, in their currency", "Salary paid on the local payroll date, with payslips and tax forms in one app."),
                 ("Statutory benefits and more", "Everything the law requires, plus health cover or other extras you choose to offer."),
                 ("Your equity plan", "Stock options can be granted through your company’s plan. Raises and bonuses go through payroll."),
                 ("Onboarding that works", "Contract, documents and registrations done before day one, so they start ready."),
                 ("People to ask", "Our HR team answers their questions on pay, benefits and leave.")]) + '</div></section>')

comp = ('<section class="sec" id="compliance"><div class="wrap">' + head("05", "Compliance", "Local law, handled in every country", "Employment rules differ in every country. Getting them right is our job, not yours.")
        + cards([("Contracts under local law", "Notice periods, probation, working hours and leave written the way the country requires."),
                 ("Taxes and social security", "Withheld, filed and paid on time, with proof of every filing."),
                 ("Misclassification risk removed", "Full-time workers employed properly, not paid as contractors."),
                 ("Exits done right", "Notice, severance and final pay calculated under local rules."),
                 ("IP assigned to you", "Every contract assigns the work and the intellectual property to your company."),
                 ("Tax risk flagged early", "We flag roles that could create a taxable presence for your company before you hire.")])
        + '<div class="clause" style="margin-top:24px"><b>In India:</b> Paybooks’ published promise of no penalties ever on the filings and payments it handles. <a href="employer-of-record/india/">See Employer of Record India</a>.</div></div></section>')

cost = ('<section class="sec alt" id="cost"><div class="wrap">' + head("06", "Cost", "What it costs", "Three parts, the same in every country. The amounts depend on the country and the pay.")
        + '<ul class="cparts"><li><span class="cp-n">1</span><div><b>Salary</b><p>The pay you agree with your hire, paid in their local currency.</p></div></li>'
        '<li><span class="cp-n">2</span><div><b>Employer costs</b><p>Social security, pension and other contributions the law requires. They vary by country and are the same with any provider.</p></div></li>'
        '<li><span class="cp-n">3</span><div><b>Our fee</b><p>A monthly fee per employee, set by country and shown in your quote.</p></div></li></ul>'
        '<div class="clause" style="margin-top:24px"><b>Example, India:</b> salary, plus about 8 to 9% in employer costs, plus Paybooks’ fee from $199 per employee a month. <a href="employer-of-record/india/">See the India cost breakdown</a>.</div></div></section>')

timeline = ('<section class="sec tight" id="timeline"><div class="wrap"><div class="split">' + head("07", "Timeline", "From offer to first day", "How long it takes depends on the country. Your quote confirms the start date.")
            + '<ul class="tl">' + "".join(f'<li><span class="d">{esc(a)}</span><div><p>{b}</p></div></li>' for a, b in [
                ("Step 1", "You send the role, country and pay. We send the full cost and the contract terms."),
                ("Step 2", "You approve. We issue the local contract and your hire signs."),
                ("Step 3", "We collect documents and complete the registrations."),
                ("Step 4", "Any background checks you choose are completed."),
                ("Step 5", "First day."),
                ("Monthly", "Salary paid on the local date, filings done, and one invoice to you.")]) + '</ul></div></div></section>')

grow = ('<section class="sec alt" id="exits"><div class="wrap">' + head("08", "Grow", "Change course whenever you need to", "Letting one person go, or moving your team to your own entity. We handle both.")
        + '<div class="split" style="grid-template-columns:1fr 1fr">'
        + "".join(f'<div><h3 style="margin-bottom:12px">{h3}</h3><ul class="tl">' + "".join(f'<li><span class="d">{esc(a)}</span><div><p>{b}</p></div></li>' for a, b in items) + '</ul></div>' for h3, items in [
            ("Letting someone go", [("Decide", "You tell us. We confirm the notice and severance the country requires."), ("Notice", "We issue the termination under local law."), ("Last day", "Final pay, unused leave and any severance due."), ("After", "Tax forms, documents and equipment return.")]),
            ("Moving to your own entity", [("Decide", "Usually once a country team is large enough to justify an entity."), ("Set up", "Your entity is set up. New hires keep joining through us."), ("Switch day", "Contracts move to your entity. Service continues."), ("After", "Paybooks can keep running payroll for your entity.")])])
        + '</div></div></section>')

proof = ('<section class="dark" id="proof"><div class="wrap">' + '<div class="head rv"><span class="num">09</span><div><span class="eyebrow">Why Paybooks</span><h2>Payroll depth. A global parent.</h2></div></div>'
         '<ul class="cards">' + "".join(f'<li class="card"><h3>{esc(a)}</h3><p>{b}</p><div class="chips">' + "".join(f"<span>{esc(z)}</span>" for z in ch) + '</div></li>' for a, b, ch in [
             ("Payroll since 2012", "3,000+ employers. 1.5 million paychecks a year. $1B+ in salaries paid a year.", ["Payroll", "Taxes", "Benefits", "Compliance"]),
             ("A $1.32 billion parent", "TransPerfect bought Paybooks in 2024. 150+ cities on six continents. Trusted by 90% of the Fortune 500.", ["ISO 27001:2022", "SOC 2 Type II", "GDPR"])])
         + '</ul></div></section>')

FAQ = [("What is an Employer of Record?", "A company that legally employs people on your behalf in a country where you have no entity. It runs the contract, payroll, taxes and benefits under local law, while you manage the work."),
       ("Is it legal to hire through an EOR?", "Yes. The EOR is the legal employer under the country’s law and provides your hire’s services to you. It is a standard way to hire abroad."),
       ("How is an EOR different from a PEO?", "A PEO shares employer duties with a company that already has its own entity in the country. An EOR needs no entity: it is the employer."),
       ("What does an EOR cost?", "Salary, plus the employer costs the country requires, plus a monthly fee per employee. Your quote shows every line for your country."),
       ("How fast can someone start?", "It depends on the country and on whether a work permit is needed. Your quote confirms the start date."),
       ("Can you convert our contractors into employees?", "Yes. We move full-time contractors onto local employment contracts, which removes the misclassification risk."),
       ("Can EOR employees get our stock options?", "Yes, through your company’s equity plan."),
       ("Who owns the IP?", "You do. Every contract assigns it to your company."),
       ("What happens when we open our own entity?", "Your people move to your entity’s contracts. Paybooks can keep running their payroll."),
       ("Which countries do you cover?", "See the country guides above, or send us the country you need with your quote request.")]
faq = ('<section class="sec" id="faq"><div class="wrap"><div class="faq"><div class="sticky"><span class="eyebrow">FAQ</span><h2>Your questions, answered</h2><p style="color:var(--muted);margin:14px 0 22px">What to know before you hire abroad.</p><a class="btn" href="#quote">Talk to an EOR expert</a></div><div>'
       + "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in FAQ) + '</div></div></div></section>')

cta = ('<section class="cta2" id="quote"><div class="wrap"><div class="cta2-card"><div class="cta2-copy"><span class="cta2-tag">Get started</span><h2>Send us one role. <em>Get the full cost back.</em></h2>'
       '<p>Tell us the country, the role and the pay. You get the full monthly cost, the contract terms and a start date. No commitment.</p>'
       '<div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" href="#quote">Talk to an EOR expert</a></div>'
       f'<ul class="cta2-ticks">{TICKS}</ul></div>'
       '<div class="cta2-quote" aria-hidden="true"><div class="q-head"><span>Example quote</span><em>India</em></div>'
       '<div class="q-role"><b>Senior Software Engineer</b><small>Bengaluru · $26,000 a year</small></div>'
       '<ul class="q-rows"><li><span>Monthly cost, all-in</span><b>$2,550</b></li><li><span>Employer costs</span><b>$184</b></li><li><span>Paybooks fee</span><b>$199</b></li><li><span>Start date</span><b>Confirmed in your quote</b></li></ul>'
       '<div class="q-docs"><span>Contract terms</span><span>Sample offer letter</span></div></div></div></div></section>')

EXTRA_CSS = ('<style>.cgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.cty{display:flex;flex-direction:column;gap:6px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 22px;text-decoration:none;color:inherit}'
             '.cty b{font-family:var(--head);font-size:19px}.cty span{font-size:14px;color:var(--muted)}.cty em{font-style:normal;font-size:13.5px;font-weight:600;color:#98A2B3;margin-top:4px}'
             '.cty.live{border-color:var(--green);box-shadow:0 10px 30px -18px rgba(79,138,16,.6)}.cty.live em{color:var(--green)}.cty.live:hover{transform:translateY(-2px);transition:transform .15s}'
             '@media(max-width:860px){.cgrid{grid-template-columns:1fr 1fr}}@media(max-width:560px){.cgrid{grid-template-columns:1fr}}</style>')
schema = [
    {"@context": "https://schema.org", "@type": "Organization", "name": "Paybooks, a TransPerfect company", "url": "https://www.paybooks.in/", "parentOrganization": {"@type": "Organization", "name": "TransPerfect", "url": "https://www.transperfect.com/"}},
    {"@context": "https://schema.org", "@type": "Service", "name": "Employer of Record services", "serviceType": "Employer of Record", "provider": {"@type": "Organization", "name": "Paybooks, a TransPerfect company"}},
    {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.paybooks.in/"}, {"@type": "ListItem", "position": 2, "name": "Employer of Record", "item": "https://www.paybooks.in/employer-of-record/"}]},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
HEAD = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{esc(TITLE)}</title><meta name="description" content="{esc(DESC)}"><link rel="canonical" href="https://www.paybooks.in/employer-of-record/"><meta name="robots" content="noindex,nofollow">'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@500;600;700&family=Inter:wght@400;500;600;700&family=Zilla+Slab:wght@300;400&display=swap" rel="stylesheet"><link rel="stylesheet" href="assets/pb.css">'
        + "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in schema) + EXTRA_CSS + '</head>')
FOOT = ('<footer class="ftr"><div class="wrap" style="grid-template-columns:1fr"><div><h4>Paybooks, a TransPerfect company</h4><p>Employer of Record, Multi-Country Payroll, Managed India Office and Global HCM for companies building teams across borders.</p></div></div></footer>'
        '<script src="assets/protect.js" defer></script></body></html>')
page = HEAD + HEADER + "<main>" + hero + how + fit + countries + hire + comp + cost + timeline + grow + proof + faq + cta + REVEAL + "</main>" + FOOT
open(OUT, "w", encoding="utf-8").write(page)
print("hub written", len(page))
