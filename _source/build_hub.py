"""Global Employer of Record hub, interactive version. Writes ../index.html.
Header, trust bar and reveal script come from lp_template.html. Statutory rates carry their official source."""
import html, json, os
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "..", "index.html")
T = open(os.path.join(H, "lp_template.html")).read()
esc = lambda s: html.escape(s, quote=True)
HEADER = T[T.find("<body"):T.find("<main>")]
ts = T.find('<div class="trust">'); TRUST = T[ts:T.find("</div></div></div></div>", ts) + len("</div></div></div></div>")]
js0 = T.find("<script>(function(){var io="); REVEAL = T[js0:T.find("</script>", js0) + 9]
VID = ('<div class="vidhold" role="img" aria-label="Video placeholder"><div class="vh-frame"><span class="vh-mini"><svg width="16" height="16" viewBox="0 0 24 24" fill="#fff"><path d="M8 5v14l11-7z"/></svg></span>'
       '<span class="vh-cap"><b>How Paybooks EOR works</b><small>2-minute walkthrough</small></span><span class="vh-tag">Video</span></div></div>')
TICKS = '<li>No entity to set up</li><li>Local contracts and payroll</li><li>One monthly invoice</li>'
PH = json.load(open(os.path.join(H, "..", "strategy", "paybooks_phases.json")))
i0 = T.find('<div class="letter">'); i1 = T.find('</div><ul class="cards"', i0)
LETTER = T[i0:i1]
def head(n, eyebrow, h2, sub):
    cls = "eyebrow"
    return f'<div class="head rv"><span class="num">{n}</span><div><span class="{cls}">{eyebrow}</span><h2>{esc(h2)}</h2><p>{sub}</p></div></div>'

TITLE = "Employer of Record (EOR) Services | Hire From Any Country Without an Entity | Paybooks, a TransPerfect company"
DESC = "Hire employees in 42 countries without setting up an entity. Paybooks becomes the legal employer and runs contracts, payroll, taxes and benefits under local law. Estimate the cost, check your fit, get a quote."

hero = (f'<section class="hero v2"><div class="wrap"><div class="grid"><div><span class="cta2-tag hero-tag">Your first international hire, live within days</span>'
        '<h1>Hire from any country. <em>No entity needed.</em></h1>'
        '<p class="sub">Wherever your company is based, Paybooks becomes the legal employer of your people in any of 42 countries. We run the local contract, payroll, taxes and benefits under that country’s law. You choose the people and direct their work.</p>'
        '<div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" href="#quote">Talk to an EOR expert</a></div>'
        f'<ul class="cta2-ticks hero-ticks">{TICKS}</ul></div>{VID}</div></div></section>{TRUST}')

# ---------- 01 lifecycle stepper ----------
OUTCOME = ["The full cost and contract terms, before anyone signs", "A local contract, signed in days", "Registered and ready before day one", "Paid on the local date, every month", "Statutory benefits from day one, plus your extras", "Every filing done, and proven", "A clean exit, or the same job under your own name"]
STAGES = [
 ("Offer", "You choose the candidate and agree the role, pay and start date. Recruiting stays with you.", "We confirm the full monthly cost for that country and send the contract terms within your quote.", "A clear offer, in their language, with your company, manager and role named."),
 ("Contract", "You approve the package.", "We sign the local employment contract on our entity: notice, probation, working hours and leave written the way the country requires. IP is assigned to you.", "A real local employment contract with a real local employer."),
 ("Onboarding", "You plan their first day and their work.", "We collect documents, complete registrations and, where you ask, run background checks.", "Contract, documents and registrations done before day one."),
 ("Payroll", "You approve raises, bonuses and equity grants.", "We pay salary on the local payroll date, in local currency, and withhold, file and pay every tax and social contribution.", "Pay on time, every month, with payslips and tax forms in one app."),
 ("Benefits", "You choose any extras above the statutory minimum.", "We enroll them in the statutory benefits and any extras you choose, and handle claims and leave.", "Everything the law requires, plus what you add."),
 ("Compliance", "You set policies within local law.", "We track every filing and rule change, keep proof of every filing, and flag roles that could create a taxable presence for you.", "An employer that never misses a filing."),
 ("Exit or transfer", "You decide when to part ways, or when to open your own entity.", "We issue the termination under local law with the notice and severance due, or move their contract to your new entity with service unbroken.", "A clean exit, or the same job under your own name."),
]
ICON = {"you": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
        "us": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
        "hire": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>'}
track = "".join(f'<button class="lc-node{" on" if i == 0 else ""}" data-i="{i}" type="button" aria-label="Stage {i+1}: {esc(n)}"><span class="lc-dot">{i+1}</span><span class="lc-lab">{esc(n)}</span></button>' for i, (n, *_ ) in enumerate(STAGES))
panes = "".join(f'<div class="lc-pane{" on" if i == 0 else ""}" data-i="{i}"><div class="lc-head"><span class="lc-k">Stage {i+1} of {len(STAGES)}</span><h3>{esc(n)}</h3><p class="lc-out">{esc(OUTCOME[i])}</p></div>'
                f'<div class="lc-rows"><div class="lc-row you"><i>{ICON["you"]}</i><div><small>You</small><p>{esc(y)}</p></div></div>'
                f'<div class="lc-row us"><i>{ICON["us"]}</i><div><small>Paybooks</small><p>{esc(u)}</p></div></div>'
                f'<div class="lc-row hire"><i>{ICON["hire"]}</i><div><small>Your hire sees</small><p>{esc(h)}</p></div></div></div></div>' for i, (n, y, u, h) in enumerate(STAGES))
nav = '<div class="lc-nav"><button type="button" class="lc-prev" aria-label="Previous stage">← Previous</button><span class="lc-pos"></span><button type="button" class="lc-next" aria-label="Next stage">Next stage →</button></div>'
lifecycle = ('<section class="sec" id="how"><div class="wrap">' + head("01", "Pain point: setting up an entity takes months and a local team", "Who does what, from offer to exit",
             "An Employer of Record legally employs people on your behalf in a country where you have no entity, so you hire in days, not months. Click a stage to see what stays with you and what Paybooks takes on.")
             + f'<div class="lc"><div class="lc-track"><span class="lc-line"><span class="lc-fill"></span></span>{track}</div><div class="lc-body">{panes}</div></div>'
             '<div class="midcta"><div><b>Want to see it in writing?</b><span>We will share a sample service agreement with your quote.</span></div><div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" href="#quote">Talk to an EOR expert</a></div></div></div></section>')

# ---------- 02 fit finder ----------
fit = ('<section class="sec alt" id="fit"><div class="wrap">' + head("02", "Pain point: EOR, PEO, entity or contractors, and every vendor says theirs", "Is an Employer of Record right for you?", "Three questions. The answer names the right Paybooks service, and says when it is not us.")
       + '''<div class="ff"><div class="ff-q"><div class="ff-step"><b>1 · Where do you stand in the country you want to hire in?</b><div class="ff-opts" data-q="entity">
<button type="button" data-v="none">No entity there</button><button type="button" data-v="own">We have our own entity</button><button type="button" data-v="india">We have an entity in India</button></div></div>
<div class="ff-step"><b>2 · How many people, in that country?</b><div class="ff-opts" data-q="size">
<button type="button" data-v="s">1 to 5</button><button type="button" data-v="m">6 to 20</button><button type="button" data-v="l">21 to 50</button><button type="button" data-v="xl">More than 50</button></div></div>
<div class="ff-step"><b>3 · What are you trying to do?</b><div class="ff-opts" data-q="goal">
<button type="button" data-v="test">Test a new market</button><button type="button" data-v="build">Build a long-term team</button><button type="button" data-v="convert">Employ contractors properly</button><button type="button" data-v="run">Run payroll in several countries</button></div></div></div>
<div class="ff-a" id="ffa"><div class="ff-empty"><b>Answer the three questions</b><p>Your recommendation appears here, with the reason and the option we would not suggest.</p></div></div></div>'''
       + '</div></section>')


def table(hd, rows, hl=1):
    th = "".join(f'<th{" class=hl" if i == hl else ""}>{esc(h)}</th>' for i, h in enumerate(hd))
    tr = "".join("<tr>" + "".join(f'<td{" class=hl" if i == hl else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="t-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
fit = ('<section class="sec" id="fit"><div class="wrap">' + head("01", "Start here", "Is an Employer of Record right for you?", "Find your situation below to see which way of hiring fits you best.")
       + table(["If you have", "Best option", "Why it fits", "Not recommended"], [
           ["1 to 20 hires in a country where you have no entity", "<b>Employer of Record</b>", "Live within days. No entity to set up or close.", "Opening an entity first"],
           ["A new market to test", "<b>Employer of Record</b>", "Hire now; decide on an entity once the market proves itself.", "Committing to an entity too early"],
           ["Contractors working full time for you", "<b>EOR conversion</b>", "Removes the risk of treating employees as contractors.", "Leaving them as contractors"],
           ["A large team in one country, or IP-heavy work", "<b>Your own entity, with Paybooks payroll</b>", "At scale, owning an entity usually costs less per person.", "EOR at any size"],
           ["A team to build in India", "<b>EOR now, Managed India Office later</b>", "Start on EOR. Move to your own India entity, run by Paybooks, as the team grows.", "Waiting to hire until an entity is ready"],
           ["Your own entities in several countries", "<b>Multi-Country Payroll</b>", "One provider and one report for payroll in every country.", "A different payroll vendor per country"]]) + '</div></section>')
def col(cls, h3, items): return f'<div class="col {cls}"><h3>{esc(h3)}</h3><ul>' + "".join(f'<li><div><b>{esc(a)}</b><span>{esc(b)}</span></div></li>' for a, b in items) + '</ul></div>'
control = ('<section class="sec" id="control"><div class="wrap">' + head("04", "Who does what", "You manage the work. We handle the employer duties.", "Exactly who handles what, as written in your service agreement.")
           + '<div class="raci">' + col("you", "You decide", [("Who to hire and what to pay", "We quote the full monthly cost first"), ("Day-to-day work, reviews, promotions", "Managers are yours"),
               ("Work hours, leave and remote rules", "Your policies, within local law"), ("Raises, bonuses, equity", "Processed in the next payroll, no fee"), ("When to part ways", "We handle it under local law"), ("When to own your entity", "Your team moves over. Nothing restarts.")])
           + col("us", "We take care of", [("The employment contract and legal liability", "Under the country’s labor law"), ("Payroll and every government payment", "Taxes and social contributions: we calculate, file and pay"),
               ("Registrations and inspections", "With the local authorities"), ("Benefits", "Statutory benefits, plus any extras you choose"), ("Exits and final pay", "Notice, severance and documents"), ("Data security", "ISO 27001:2022. SOC 2 Type II. GDPR.")]) + '</div>'
           + '<div class="midcta"><div><b>Want to see it in writing?</b><span>We will share a sample service agreement with your quote.</span></div><div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" href="#quote">Talk to an EOR expert</a></div></div></div></section>')

# ---------- countries by region (unused in v4 flow) ----------
REGIONS = [("Europe", ["United Kingdom", "Germany", "Netherlands", "Ireland", "Switzerland", "France", "Sweden", "Denmark", "Finland", "Norway", "Belgium", "Austria", "Italy", "Spain", "Portugal", "Czech Republic", "Poland", "Hungary", "Romania", "Turkey"]),
           ("Americas", ["United States", "Canada", "Brazil", "Mexico", "Argentina", "Colombia", "Costa Rica", "Dominican Republic"]),
           ("Asia-Pacific", ["India", "Singapore", "Australia", "Hong Kong", "Japan", "South Korea", "China", "Thailand", "Philippines"]),
           ("Middle East and Africa", ["UAE", "Saudi Arabia", "South Africa", "Kenya", "Nigeria"])]
ALL42 = PH["6A"] + PH["6B"] + PH["6C"]; assert sorted(c for _, L in REGIONS for c in L) == sorted(ALL42)
regions = "".join(f'<div class="rg"><h4>{esc(r)} <span>{len(L)}</span></h4><div class="rg-pills">' + "".join(f'<button type="button" class="cp{" on" if c == "India" else ""}" data-n="{esc(c)}" data-r="{esc(r)}">{esc(c)}</button>' for c in L) + '</div></div>' for r, L in REGIONS)
countries = ('<section class="sec alt" id="countries"><div class="wrap">' + head("02", "Countries", "Hire in 42 countries",
             "Local contracts, payroll and compliance handled in each one. Pick a country to see what an employee costs there.")
             + f'<div class="cw"><div><div class="cs"><input id="csq" type="search" placeholder="Search a country" autocomplete="off" aria-label="Search a country"><span id="csn">42 countries</span></div><div class="rgs">{regions}</div></div>'
             '<aside class="cpanel" id="cpanel"></aside></div></div></section>')

HIRE_CARDS = [("Your name on the letter", "Paybooks is the employer. Your company, manager and role are on page one."),
              ("Real benefits from day one", "The statutory benefits of the country, plus any extras you choose. Payslips and tax forms in one app."),
              ("Ready on day one", "Contract, documents and registrations done before the start date. A welcome call with you and our HR team."),
              ("Stock options and raises", "Your equity plan can cover them. Raises and bonuses go through in the next payroll, no fee."),
              ("Their LinkedIn profile", "They list your company as their employer. We explain how Paybooks shows up before the offer."),
              ("People to ask", "Our HR team answers their payslip, insurance and leave questions.")]
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>'
hire = ('<section class="sec alt" id="experience"><div class="wrap">' + head("03", "Your hire", "What your hire sees", "The offer letter, benefits and support your new hire gets from day one, in their country.")
        + '<div class="split"><div class="sticky"><p class="fine" style="margin:0 0 10px;color:var(--g600);font-weight:600">Example offer letter · India</p>' + LETTER + '</div>'
        + '<ul class="cards" style="grid-template-columns:1fr 1fr">' + "".join(f'<li class="card"><div class="ic">{CHECK}</div><h3>{esc(h)}</h3><p>{t}</p></li>' for h, t in HIRE_CARDS) + '</ul></div></div></section>')

# ---------- 05 cost calculator ----------
RATES = {
 "IN": {"name": "India", "cur": "₹", "code": "INR", "default": 1500000, "min": 300000, "max": 6000000, "step": 50000, "fee": 199, "feeCur": "$", "usd": 95.7, "yearNote": "Converted at ₹95.7 per $1 (Sep 23, 2026)",
        "lines": [["Provident fund", "12% of basic pay (basic is half of gross)"], ["Gratuity", "4.81% of basic pay, due after one year"], ["State insurance (ESI)", "3.25% of gross when gross is ₹21,000 a month or less"]],
        "src": [["Paybooks India cost breakdown", "employer-of-record/india/#cost"]]},
 "US": {"name": "United States", "cur": "$", "code": "USD", "default": 90000, "min": 30000, "max": 300000, "step": 1000, "fee": None, "usd": 1,
        "lines": [["Social Security", "6.2% of pay up to $184,500 (2026)"], ["Medicare", "1.45% of all pay"], ["Federal unemployment (FUTA)", "0.6% of the first $7,000"]], "extra": "State unemployment insurance is added in your quote; it varies by state.",
        "src": [["IRS, Topic 751", "https://www.irs.gov/taxtopics/tc751"]]},
 "UK": {"name": "United Kingdom", "cur": "£", "code": "GBP", "default": 55000, "min": 20000, "max": 200000, "step": 1000, "fee": None,
        "lines": [["Employer National Insurance", "15% of pay above £5,000 a year (2026 to 2027)"], ["Workplace pension, employer minimum", "3% of earnings between £6,240 and £50,270"]],
        "src": [["GOV.UK, rates and thresholds 2026 to 2027", "https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027"], ["GOV.UK, workplace pensions", "https://www.gov.uk/workplace-pensions/what-you-your-employer-and-the-government-pay"]]},
 "SG": {"name": "Singapore", "cur": "S$", "code": "SGD", "default": 84000, "min": 30000, "max": 300000, "step": 1000, "fee": None,
        "lines": [["CPF, employer share", "17% of wages for citizens and permanent residents aged 55 and below (from 1 January 2026)"]], "extra": "The CPF wage ceiling is applied in your quote. Foreign employees do not receive CPF.",
        "src": [["CPF Board, employer contributions", "https://www.cpf.gov.sg/employer/employer-obligations/how-much-cpf-contributions-to-pay"]]},
 "CA": {"name": "Canada", "cur": "C$", "code": "CAD", "default": 85000, "min": 30000, "max": 250000, "step": 1000, "fee": None,
        "lines": [["Canada Pension Plan", "5.95% of pay above $3,500 up to $74,600 (2026)"], ["Employment Insurance, employer share", "1.4 × 1.63% of pay up to $68,900 (2026)"]], "extra": "The second CPP tier and provincial plans are applied in your quote.",
        "src": [["Canada Revenue Agency, CPP rates", "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/payroll/payroll-deductions-contributions/canada-pension-plan-cpp/cpp-contribution-rates-maximums-exemptions.html"], ["Canada Revenue Agency, EI premiums", "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/payroll/payroll-deductions-contributions/employment-insurance-ei/ei-premium-rates-maximums.html"]]},
}
QUOTE_ONLY = [c for c in ALL42 if c not in {v["name"] for v in RATES.values()}]
opts = "".join(f'<option value="{k}">{esc(v["name"])}</option>' for k, v in RATES.items()) + "".join(f'<option value="Q:{esc(c)}">{esc(c)} · in your quote</option>' for c in QUOTE_ONLY)
cost = ('<section class="sec" id="cost"><div class="wrap">' + head("06", "Cost", "What it costs, line by line",
        "Salary, the employer contributions the country's law requires, and our fee, in the open. Statutory rates come from each country's official source, linked below the result.")
        + '<ul class="cparts"><li><span class="cp-n">1</span><div><b>Salary</b><p>The pay you agree with your hire, paid in their local currency on the local payroll date.</p></div></li>'
        '<li><span class="cp-n">2</span><div><b>Employer costs</b><p>Social security, pension and other contributions the law requires. They vary by country and are the same with any provider.</p></div></li>'
        '<li><span class="cp-n">3</span><div><b>Our fee</b><p>A monthly fee per employee, set by country. In India, from $199 a month plus a one-time $50 onboarding fee.</p></div></li></ul>'
        + f'<div class="calc calc2"><div class="calc-in"><h3>Employee cost calculator</h3><p class="calc-note">Based on September 2026 rules. This is an estimate. Your written quote is final.</p>'
        f'<div class="calc-row" style="margin:0 0 22px;padding-bottom:18px;border-bottom:1px solid rgba(255,255,255,.1)"><label for="cec">Hiring country</label><select id="cec">{opts}</select></div>'
        '<label>Annual pay <span id="cesv"></span></label><input id="ces" type="range">'
        '<label>Employees <span id="nv"></span></label><input id="n" type="range" min="1" max="100" step="1" value="5">'
        '<div class="calc-row" id="strow"><label>State</label><select id="st"><option value="200">Karnataka (about $2 professional tax)</option><option value="200">Maharashtra (about $2 professional tax)</option><option value="0">Delhi / Haryana (no professional tax)</option><option value="200">Telangana (about $2 professional tax)</option><option value="208">Tamil Nadu (about $2 professional tax)</option></select></div>'
        '<div class="calc-row"><label>Our fee</label><span class="fee-pill" id="feepill"></span></div><p class="fine" id="cenote"></p></div>'
        '<div class="calc-out" id="ceout"><div class="kpis"><div class="kpi"><b id="ce_total"></b><span>per employee per month</span></div><div class="kpi"><b id="ce_year"></b><span id="ce_year_l">a year for your team</span></div><div class="kpi"><b id="ce_stat"></b><span>employer costs on top of salary</span></div></div>'
        '<ul class="lines" id="ce_rows"></ul><p class="fine" id="ce_src"></p></div></div>'
        '<p class="fine">Headline statutory rates. Thresholds noted in each line are applied; other caps, regional rates and any benefits you add are applied in your written quote, which is final. Professional tax in India is withheld from the employee’s pay and shown for completeness. Paybooks’ fee outside India is set by country and shown in your quote.</p></div></section>')

# ---------- 06 compare ----------
CMP_HEAD = ["", "Paybooks", "Deel", "Remote", "Multiplier"]
CMP_ROWS = [["Monthly fee per employee, India", "<b>From $199</b>", "$599", "$699", "about $459 to $499"],
            ["One-time onboarding fee, India", "<b>$50</b>", "Not published", "Not published", "Not published"],
            ["Countries with a hiring page on their site", "<b>42 planned</b>", "113", "181", "186"],
            ["Parent company", "<b>TransPerfect, $1.32B revenue</b>", "Venture-backed", "Venture-backed", "Venture-backed"],
            ["Sets up and runs your own entity", "<b>Yes, in India (Managed India Office)</b>", "Not published", "Not published", "Not published"],
            ["Pages in the buyer’s language", "<b>In-house: localization is TransPerfect’s core business</b>", "12 languages", "10 languages", "English only"]]
def ctable():
    th = "".join(f'<th{" class=hl" if i == 1 else ""}>{esc(h)}</th>' for i, h in enumerate(CMP_HEAD))
    tr = "".join("<tr>" + "".join(f'<td{" class=hl" if i == 1 else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in CMP_ROWS)
    return f'<div class="t-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
compare = ('<section class="sec alt" id="compare"><div class="wrap">' + head("07", "Compare", "Compare EOR providers: choose the best", "How Paybooks compares with the platforms you will be quoted by. Prices are the published India rates; fees for other countries come in your quote.")
           + ctable() + '<p class="fine">Fees published September 23, 2026: <a href="https://www.deel.com/pricing/" rel="nofollow" target="_blank">Deel</a>, <a href="https://remote.com/pricing" rel="nofollow" target="_blank">Remote</a>, <a href="https://remotepeople.com/blog/employer-of-record-cost/" rel="nofollow" target="_blank">Multiplier</a>; Paybooks from <a href="https://paybooks.in/eor/" rel="nofollow" target="_blank">paybooks.in/eor</a>. Country pages and languages counted from each site’s sitemap, September 2026. “Not published” means the company does not state it publicly.</p></div></section>')

# ---------- 05 compliance strip, timeline, proof, faq, cta ----------
comp = ('<section class="sec alt" id="compliance"><div class="wrap">' + head("05", "Compliance", "Local law, handled in every country", "Employment rules differ in every country. Getting them right is our job, not yours.")
        + '<ul class="chk">' + "".join(f'<li><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a, b in [
            ("Contracts under local law", "Notice, probation, hours and leave written as the country requires."), ("Taxes and social security", "Withheld, filed and paid on time, with proof of every filing."),
            ("Misclassification risk removed", "Full-time workers employed properly, not paid as contractors."), ("Exits done right", "Notice, severance and final pay under local rules."),
            ("IP assigned to you", "Every contract assigns the work and the intellectual property to your company."), ("Tax risk flagged early", "Roles that could create a taxable presence are flagged before you hire.")]) + '</ul>'
        '<div class="clause" style="margin-top:22px"><b>In India:</b> Paybooks’ published promise of no penalties ever on the filings and payments it handles. <a href="employer-of-record/india/">See Employer of Record India</a>.</div></div></section>')

exits = ('<section class="sec" id="exits"><div class="wrap">' + head("08", "Exits", "Clean exits, whenever you need them", "Letting one person go, or moving your team to your own entity. We handle both, under local law.")
        + '<div class="split" style="grid-template-columns:1fr 1fr">'
        + "".join(f'<div><h3 style="margin-bottom:12px">{h3}</h3><ul class="tl">' + "".join(f'<li><span class="d">{esc(a)}</span><div><p>{b}</p></div></li>' for a, b in items) + '</ul></div>' for h3, items in [
            ("Letting someone go", [("Decide", "You tell us. We confirm the notice and severance the country requires."), ("Notice", "We issue the termination under local law: notice, or pay in place of notice."), ("Last day", "Final pay: salary, unused leave and any severance due."), ("After", "Tax forms, documents and equipment return.")]),
            ("Moving to your own entity", [("Decide", "Usually once a country team is large enough to justify an entity. In India, Paybooks sets it up and runs it for you."), ("Set up", "Your entity is set up. New hires keep joining through us."), ("Switch day", "Contracts move to your entity. Service continues, same payslip app."), ("After", "Paybooks can keep running payroll for your entity.")])])
        + '</div></div></section>')
service = ('<section class="sec alt" id="service"><div class="wrap">' + head("09", "Working with us", "How we work with you", "One team, one monthly report and one invoice for your whole international team.")
           + '<ul class="cards three">' + "".join(f'<li class="card"><div class="ic">{CHECK}</div><h3>{esc(h)}</h3><p>{t}</p></li>' for h, t in [
               ("One account manager", "With a payroll and compliance specialist for each country behind them."), ("Reply within one working day", "With overlap for calls across US, UK and Asia-Pacific hours."),
               ("One monthly report", "Payroll summary, filing proof and cost in your currency, every country on one page."), ("One invoice", "In USD, GBP or EUR at the bank rate. Salary, employer costs and our fee."),
               ("Integrations", "Employee and cost data flows to your HR or finance system. Single sign-on for the employee app."), ("Security", "ISO 27001:2022. SOC 2 Type II. GDPR.")]) + '</ul></div></section>')
timeline = ('<section class="sec tight" id="timeline"><div class="wrap"><div class="split">' + head("10", "Timeline", "From offer to first day, within days", "In India it is days, not months. Elsewhere your quote confirms the start date.")
            + '<ul class="tl">' + "".join(f'<li><span class="d">{esc(a)}</span><div><p>{b}</p></div></li>' for a, b in [
                ("Step 1", "You send the role, country and pay. We send the full cost and the contract terms."), ("Step 2", "You approve. We issue the local contract and your hire signs."),
                ("Step 3", "We collect documents and complete the registrations."), ("Step 4", "Any background checks you choose are completed."), ("Step 5", "First day."),
                ("Monthly", "Salary paid on the local date, filings done, and one invoice to you.")]) + '</ul></div></div></section>')

proof = ('<section class="dark" id="proof"><div class="wrap"><div class="head rv"><span class="num">11</span><div><span class="eyebrow">Why Paybooks</span><h2>Payroll depth. A global parent.</h2></div></div>'
         '<ul class="cards">' + "".join(f'<li class="card"><h3>{esc(a)}</h3><p>{b}</p><div class="chips">' + "".join(f"<span>{esc(z)}</span>" for z in ch) + '</div></li>' for a, b, ch in [
             ("Payroll since 2012", "3,000+ employers. 1.5 million paychecks a year. $1B+ in salaries paid a year.", ["Payroll", "Taxes", "Benefits", "Compliance"]),
             ("A $1.32 billion parent", "TransPerfect bought Paybooks in 2024. 150+ cities on six continents. Trusted by 90% of the Fortune 500.", ["ISO 27001:2022", "SOC 2 Type II", "GDPR"])]) + '</ul></div></section>')
FAQ = [("What is an Employer of Record?", "A company that legally employs people on your behalf in a country where you have no entity. It runs the contract, payroll, taxes and benefits under local law, while you manage the work."),
       ("Do you find the candidates?", "No. You choose the candidate; Paybooks hires your chosen candidates on its entity and takes it from there. Recruiting stays with you."),
       ("Is it legal to hire through an EOR?", "Yes. The EOR is the legal employer under the country’s law and provides your hire’s services to you. It is a standard way to hire abroad."),
       ("How is an EOR different from a PEO?", "A PEO shares employer duties with a company that already has its own entity in the country. An EOR needs no entity: it is the employer."),
       ("What does an EOR cost?", "Salary, plus the employer costs the country requires, plus a monthly fee per employee. The estimator above shows the first two for five countries; your quote shows every line for your country."),
       ("How fast can someone start?", "It depends on the country and on whether a work permit is needed. In India, Paybooks onboards within days. Your quote confirms the start date."),
       ("Can you convert our contractors into employees?", "Yes. We move full-time contractors onto local employment contracts, which removes the misclassification risk."),
       ("Can EOR employees get our stock options?", "Yes, through your company’s equity plan."),
       ("Who owns the IP?", "You do. Every contract assigns it to your company."),
       ("What happens when we open our own entity?", "Your people move to your entity’s contracts with service unbroken. Paybooks can keep running their payroll."),
       ("Which countries do you cover?", "42 countries across Europe, the Americas, the Middle East, Africa and Asia-Pacific. Use the country finder above, or send us the country you need with your quote request.")]
faq = ('<section class="sec alt" id="faq"><div class="wrap"><div class="faq"><div class="sticky"><span class="eyebrow">FAQ</span><h2>Your questions, answered</h2><p style="color:var(--muted);margin:14px 0 22px">What to know before you hire in another country.</p><a class="btn" href="#quote">Talk to an EOR expert</a></div><div>'
       + "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in FAQ) + '</div></div></div></section>')
cta = ('<section class="cta2" id="quote"><div class="wrap"><div class="cta2-card"><div class="cta2-copy"><span class="cta2-tag">Get started</span><h2>Send us one role. <em>Get the full cost back.</em></h2>'
       '<p>Tell us the country, the role and the pay. You get the full monthly cost, the contract terms and a start date. No commitment.</p>'
       '<div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" href="#quote">Talk to an EOR expert</a></div>'
       f'<ul class="cta2-ticks">{TICKS}</ul></div>'
       '<div class="cta2-quote" aria-hidden="true"><div class="q-head"><span>Example quote</span><em>India</em></div>'
       '<div class="q-role"><b>Senior Software Engineer</b><small>Bengaluru · $26,000 a year</small></div>'
       '<ul class="q-rows"><li><span>Monthly cost, all-in</span><b>$2,550</b></li><li><span>Employer costs</span><b>$184</b></li><li><span>Paybooks fee</span><b>$199</b></li><li><span>Start date</span><b>Confirmed in your quote</b></li></ul>'
       '<div class="q-docs"><span>Contract terms</span><span>Sample offer letter</span></div></div></div></div></section>')

EXTRA_CSS = '''<style>
.calc .calc-row select{background:#F2F1EC!important;color:#0E1411!important;border:1px solid #DAD8CF!important;padding:8px 10px;font-size:13.5px;border-radius:10px}.calc .calc-row select:focus{outline:none;box-shadow:0 0 0 3px rgba(159,211,92,.35)}
.sec .head .eyebrow.pain,.dark .head .eyebrow.pain{display:inline-flex;text-transform:none;letter-spacing:0;font-size:14.5px;font-weight:600;color:#B4530F;margin-bottom:10px}.eyebrow.pain::before{background:#F26B1D}.dark .eyebrow.pain,#cost .eyebrow.pain,#compare .eyebrow.pain{color:#FFB08A}.dark .eyebrow.pain::before,#cost .eyebrow.pain::before,#compare .eyebrow.pain::before{background:#F26B1D}
.lc{display:grid;grid-template-columns:270px 1fr;background:#fff;border:1px solid var(--line);border-radius:22px;overflow:hidden}
.lc-track{position:relative;display:flex;flex-direction:column;gap:6px;padding:24px 18px;border-right:1px solid var(--line);background:#FAFBF8}
.lc-line{position:absolute;left:35px;top:44px;bottom:44px;width:3px;background:#E4E9E1;border-radius:2px}.lc-fill{display:block;width:100%;height:0;background:var(--green);border-radius:2px;transition:height .3s}
.lc-node{position:relative;z-index:1;display:grid;grid-template-columns:36px 1fr;gap:12px;align-items:center;text-align:left;background:none;border:0;border-radius:12px;cursor:pointer;font:inherit;color:var(--muted);padding:8px 8px 8px 0}
.lc-node:hover .lc-lab{color:var(--ink)}
.lc-dot{width:36px;height:36px;border-radius:50%;background:#fff;border:2px solid #D5DBD2;display:grid;place-items:center;font:600 13px Inter,sans-serif;color:var(--ink);transition:all .2s}
.lc-lab{font:600 15px Inter,sans-serif}
.lc-node.done .lc-dot{background:var(--green);border-color:var(--green);color:#fff}.lc-node.on{background:#fff;box-shadow:0 1px 2px rgba(20,26,31,.06),0 0 0 1px var(--line)}.lc-node.on .lc-dot{background:var(--forest);border-color:var(--forest);color:#9FD35C;box-shadow:0 0 0 5px rgba(79,138,16,.15)}.lc-node.on .lc-lab{color:var(--ink)}
.lc-node:focus-visible{outline:none}.lc-node:focus-visible .lc-dot{box-shadow:0 0 0 4px rgba(79,138,16,.35)}
.lc-body{padding:28px 30px 22px;min-width:0}.lc-pane{display:none}.lc-pane.on{display:block;animation:lcin .25s ease}
@keyframes lcin{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.lc-head{margin-bottom:18px}.lc-k{display:inline-block;font:700 11.5px Inter;letter-spacing:.1em;text-transform:uppercase;color:var(--green-600);margin-bottom:8px}.lc-head h3{font-family:var(--head);font-size:30px;letter-spacing:-.02em;margin:0 0 8px}.lc-out{font-size:17px;color:var(--ink2);margin:0;line-height:1.5;border-left:3px solid #9FD35C;padding-left:14px}
.lc-rows{display:grid;gap:10px}.lc-row{display:grid;grid-template-columns:40px 1fr;gap:14px;align-items:start;border:1px solid var(--line);border-radius:14px;padding:14px 16px;background:#fff}
.lc-row i{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;background:#F2F5EE;color:var(--ink2)}.lc-row i svg{width:20px;height:20px}
.lc-row small{display:block;font:700 11px Inter;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}.lc-row p{margin:0;font-size:15px;line-height:1.5;color:var(--ink2)}
.lc-row.us{background:var(--forest);border-color:var(--forest)}.lc-row.us i{background:rgba(159,211,92,.18);color:#9FD35C}.lc-row.us small{color:#9FD35C}.lc-row.us p{color:#EAF2E4}
.lc-nav{display:flex;justify-content:space-between;align-items:center;margin-top:18px;padding-top:16px;border-top:1px solid var(--line)}.lc-nav button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:9px 16px;font:600 14px Inter,sans-serif;color:var(--ink);cursor:pointer}.lc-nav button:disabled{opacity:.4;cursor:default}.lc-pos{font-size:13px;color:var(--muted)}
@media(max-width:900px){.lc{grid-template-columns:1fr}.lc-track{flex-direction:row;overflow-x:auto;gap:4px;padding:14px 12px;border-right:0;border-bottom:1px solid var(--line);scrollbar-width:none}.lc-track::-webkit-scrollbar{display:none}.lc-line{display:none}.lc-node{grid-template-columns:28px auto;gap:8px;padding:6px 10px 6px 4px;flex:0 0 auto}.lc-dot{width:28px;height:28px;font-size:12px}.lc-lab{font-size:13px;white-space:nowrap}.lc-head h3{font-size:24px}}
.ff{display:grid;grid-template-columns:1.15fr .85fr;gap:20px}.ff-q{display:grid;gap:14px}.ff-step{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px}.ff-step>b{display:block;font-family:var(--head);font-size:16.5px;margin-bottom:10px}
.ff-opts{display:flex;flex-wrap:wrap;gap:8px}.ff-opts button{border:1px solid var(--line);background:#FAFBF8;border-radius:999px;padding:9px 14px;font:500 14px Inter,sans-serif;color:var(--ink);cursor:pointer}
.ff-opts button.on{background:var(--forest);color:#fff;border-color:var(--forest)}
.ff-a{background:var(--forest);color:#fff;border-radius:20px;padding:28px;position:sticky;top:90px;align-self:start;min-height:220px}.ff-a b{font-family:var(--head)}.ff-empty b{font-size:20px;display:block;margin-bottom:8px}.ff-empty p{color:#BFD3B9;margin:0;font-size:15px}
.ff-r small{display:block;font:700 11.5px Inter;letter-spacing:.1em;text-transform:uppercase;color:#9FD35C;margin-bottom:8px}.ff-r h3{font-size:26px;margin:0 0 10px;color:#fff}.ff-r p{color:#DDE8D6;font-size:15px;line-height:1.55;margin:0 0 10px}.ff-r .no{color:#BFD3B9;font-size:13.5px;border-top:1px solid rgba(255,255,255,.14);padding-top:12px;margin-top:12px}.ff-r .btn{margin-top:14px}
.cs{display:flex;gap:14px;align-items:center;margin-bottom:18px}.cs input{flex:1;height:46px;border:1px solid var(--line);border-radius:12px;padding:0 16px;font:500 15px Inter,sans-serif;background:#fff}.cs input:focus{outline:none;border-color:var(--green);box-shadow:0 0 0 3px rgba(79,138,16,.15)}.cs span{font-size:13px;color:var(--muted);white-space:nowrap}
.cw{display:grid;grid-template-columns:1.4fr .8fr;gap:22px;align-items:start}.rgs{display:grid;gap:14px}.rg h4{margin:0 0 8px;font:600 13px Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}.rg h4 span{font-weight:500;color:#98A2B3;margin-left:6px}
.rg-pills{display:flex;flex-wrap:wrap;gap:6px}.cp{border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 13px;font:500 13.5px Inter,sans-serif;color:var(--ink);cursor:pointer;transition:all .15s}.cp:hover{border-color:var(--green)}.cp.on{background:var(--forest);color:#fff;border-color:var(--forest)}.cp.dim{opacity:.28}.cp.hit{border-color:var(--green);box-shadow:0 0 0 3px rgba(79,138,16,.15)}
.cpanel{position:sticky;top:90px;background:var(--forest);color:#fff;border-radius:20px;padding:26px 26px 24px}.cpanel small{display:block;font:700 11.5px Inter;letter-spacing:.1em;text-transform:uppercase;color:#9FD35C;margin-bottom:8px}.cpanel h3{font-family:var(--head);font-size:28px;margin:0 0 4px;color:#fff}.cpanel .rgn{color:#BFD3B9;font-size:14px;margin:0 0 16px}
.cpanel .st{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px}.cpanel .st div{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:12px 14px}.cpanel .st b{display:block;font-family:var(--head);font-size:22px;color:#9FD35C;line-height:1.1}.cpanel .st span{display:block;font-size:11.5px;color:#8FAF86;margin-top:3px}
.cpanel p{color:#DDE8D6;font-size:14.5px;line-height:1.5;margin:0 0 16px}.cpanel .btns{display:flex;flex-wrap:wrap;gap:10px}.cpanel .btn.ghost{background:transparent!important;color:#fff!important;border-color:rgba(255,255,255,.35)!important}
@media(max-width:900px){.cw{grid-template-columns:1fr}.cpanel{position:static}}
.ce{display:grid;grid-template-columns:.9fr 1.1fr;gap:20px;background:#0B1F14;color:#fff;border-radius:24px;padding:28px}.ce label{display:block;font:600 13px Inter;letter-spacing:.06em;text-transform:uppercase;color:#BFD3B9;margin:14px 0 8px}.ce label span{color:#fff;text-transform:none;letter-spacing:0;font-size:15px;margin-left:8px}
.ce select{width:100%;height:46px;border-radius:10px;border:1px solid rgba(255,255,255,.18);background:#143A25;color:#fff;font:500 15px Inter,sans-serif;padding:0 12px}.ce input[type=range]{width:100%;accent-color:var(--lime)}
.ce .fine{color:#8FAF86;font-size:12.5px}.ce .fine a{color:#9FD35C}.ce-out .kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.ce-out .kpi{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:12px 14px}.ce-out .kpi b{display:block;font-family:var(--head);font-size:22px;color:#9FD35C;line-height:1.1}.ce-out .kpi span{display:block;font-size:11.5px;color:#8FAF86;margin-top:3px}
.lines{list-style:none;margin:14px 0 0;padding:0}.lines li{display:flex;justify-content:space-between;gap:14px;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.08);font-size:14px}.lines li span{color:#BFD3B9}.lines li small{display:block;color:#8FAF86;font-size:12px}.lines li b{white-space:nowrap}.lines li.tot{border-bottom:0;font-weight:700;color:#fff}
.chk{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px 22px}.chk li{display:grid;grid-template-columns:20px 1fr;gap:2px 10px;padding:12px 0;border-bottom:1px solid var(--line)}.chk li::before{content:"✓";color:var(--green);font-weight:700;grid-row:span 2}.chk b{display:block;font-size:15px}.chk span{font-size:13.5px;color:var(--muted)}
@media(max-width:900px){.ff,.ce{grid-template-columns:1fr}.ff-a{position:static}.cgrid{grid-template-columns:1fr 1fr}.lc-pane.on{grid-template-columns:1fr}.lc-col+.lc-col{border-left:0;border-top:1px solid var(--line)}.chk{grid-template-columns:1fr}}
@media(max-width:560px){.cgrid{grid-template-columns:1fr}.ce-out .kpis{grid-template-columns:1fr}}
</style>'''

JS = '''<script>(function(){
if(document.querySelector('.lc')){var nodes=[].slice.call(document.querySelectorAll('.lc-node')),panes=[].slice.call(document.querySelectorAll('.lc-pane')),fill=document.querySelector('.lc-fill'),cur=0;
function go(i){cur=Math.max(0,Math.min(nodes.length-1,i));nodes.forEach(function(n,k){n.classList.toggle('on',k===cur);n.classList.toggle('done',k<cur)});panes.forEach(function(p,k){p.classList.toggle('on',k===cur)});fill.style.height=(cur/(nodes.length-1)*100)+'%'}
nodes.forEach(function(n){n.onclick=function(){go(+n.dataset.i)}});
document.querySelector('.lc').addEventListener('keydown',function(e){if(e.key==='ArrowRight')go(cur+1);if(e.key==='ArrowLeft')go(cur-1)});go(0);}
var RR,CALC;var q=document.getElementById('csq')||{addEventListener:function(){}},pills=[].slice.call(document.querySelectorAll('.cp')),cn=document.getElementById('csn'),panel=document.getElementById('cpanel');
var KEY={'India':'IN','United States':'US','United Kingdom':'UK','Singapore':'SG','Canada':'CA'};
function pct(k){var r=RR[k];if(!r)return null;var s=r['default'],L=CALC(k,s);return (L.reduce(function(a,x){return a+x[2]},0)/s*100).toFixed(1)}
function show(n,rg){pills.forEach(function(p){p.classList.toggle('on',p.dataset.n===n)});var k=KEY[n],pc=k?pct(k):null;
 panel.innerHTML='<small>Hire in</small><h3>'+n+'</h3><p class="rgn">'+rg+' · local contract, payroll and compliance handled</p>'
 +'<div class="st"><div><b>'+(pc?pc+'%':'Quoted')+'</b><span>'+(pc?'employer costs on top of salary, at a typical salary':'employer costs, shown in your quote')+'</span></div><div><b>'+(k==='IN'?'$199':'Quoted')+'</b><span>'+(k==='IN'?'Paybooks fee per employee a month':'Paybooks fee, set by country')+'</span></div></div>'
 +'<p>'+(k?'Statutory rates from '+n+'\\'s official sources. Move the calculator sliders to see the full monthly cost for your salary.':'We have not published '+n+'\\'s statutory rates here yet. Send us the role and pay and you get the full monthly cost, the contract terms and a start date.')+'</p>'
 +'<div class="btns">'+(k?'<a class="btn" href="#cost" data-k="'+k+'">Estimate the cost in '+n+'</a>':'<a class="btn" href="#cost" data-k="Q:'+n+'">See the cost breakdown</a>')+'<a class="btn ghost" href="#quote">Get a quote</a></div>';
 var b=panel.querySelector('[data-k]');if(b)b.onclick=function(){var sel=document.getElementById('cec');sel.value=b.dataset.k;sel.onchange()}}
pills.forEach(function(p){p.onclick=function(){show(p.dataset.n,p.dataset.r)}});
function filt(){var v=(q.value||'').trim().toLowerCase(),k=0,first=null;pills.forEach(function(p){var h=!v||p.dataset.n.toLowerCase().indexOf(v)>-1;p.classList.toggle('dim',v&&!h);p.classList.toggle('hit',v&&h);if(h){k++;if(!first)first=p}});cn.textContent=v?(k?k+(k===1?' match':' matches'):'Not on the 42-country list yet. Ask us with your quote.'):'42 countries';if(v&&first&&k===1)show(first.dataset.n,first.dataset.r)}
q.addEventListener('input',filt);
var R='''+json.dumps(RATES)+''',sel=document.getElementById('cec'),sl=document.getElementById('ces'),sv=document.getElementById('cesv'),note=document.getElementById('cenote'),N=document.getElementById('n'),NV=document.getElementById('nv'),ST=document.getElementById('st'),SR=document.getElementById('strow'),FP=document.getElementById('feepill'),OUT=document.getElementById('ceout');
var OUTHTML=OUT.innerHTML;
function money(c,x){return c+Math.round(x).toLocaleString('en-US')}
function calc(k,s){var L=[];
 if(k==='IN'){var b=s/2,g=s/12;L.push(['Provident fund (employer share)','12% of basic pay, basic is half of gross',b*.12]);L.push(['Gratuity set aside','4.81% of basic pay, due after one year',b*.0481]);L.push(['State insurance (ESI)',g<=21000?'3.25% of gross, gross is ₹21,000 a month or less':'Not due above ₹21,000 a month',g<=21000?s*.0325:0]);}
 if(k==='US'){L.push(['Social Security','6.2% up to $184,500',Math.min(s,184500)*.062]);L.push(['Medicare','1.45% of pay',s*.0145]);L.push(['Federal unemployment (FUTA)','0.6% of the first $7,000',Math.min(s,7000)*.006]);}
 if(k==='UK'){L.push(['Employer National Insurance','15% above £5,000',Math.max(0,s-5000)*.15]);L.push(['Workplace pension, employer minimum','3% of £6,240 to £50,270',Math.max(0,Math.min(s,50270)-6240)*.03]);}
 if(k==='SG'){L.push(['CPF, employer share','17% of wages, citizens and permanent residents',s*.17]);}
 if(k==='CA'){L.push(['Canada Pension Plan','5.95% of $3,500 to $74,600',Math.max(0,Math.min(s,74600)-3500)*.0595]);L.push(['Employment Insurance, employer share','2.282% up to $68,900',Math.min(s,68900)*.02282]);}
 return L}
function draw(){var k=sel.value,n=+N.value;NV.textContent=n;
 if(k.indexOf('Q:')===0){sl.disabled=true;sv.textContent='';note.textContent='';SR.style.display='none';FP.textContent='In your quote';OUT.innerHTML='<div class="ff-r" style="padding:6px 0"><small>'+k.slice(2)+'</small><h3>Costed in your quote</h3><p style="color:#DDE8D6">We have not published '+k.slice(2)+'\\'s statutory rates here yet. Send us the role and pay and you get the full monthly cost, the contract terms and a start date.</p><a class="btn" href="#quote">Get a quote for '+k.slice(2)+'</a></div>';return}
 var r=R[k];if(sl.dataset.k!==k){sl.min=r.min;sl.max=r.max;sl.step=r.step;sl.value=r['default'];sl.dataset.k=k;sl.disabled=false;OUT.innerHTML=OUTHTML}
 SR.style.display=k==='IN'?'':'none';FP.textContent=r.fee?'$'+r.fee+' per employee a month':'Set by country, in your quote';
 var s=+sl.value,L=calc(k,s),stat=L.reduce(function(a,x){return a+x[2]},0),fee=r.fee?r.fee*(r.usd||1)*12:0,pt=k==='IN'?(+ST.value)*12:0;
 sv.textContent=money(r.cur,s)+' '+r.code;
 var rows='<li><span>Gross salary<small>per month</small></span><b>'+money(r.cur,s/12)+'</b></li>'+L.map(function(x){return '<li><span>'+x[0]+'<small>'+x[1]+'</small></span><b>'+money(r.cur,x[2]/12)+'</b></li>'}).join('');
 if(k==='IN')rows+='<li><span>Professional tax<small>withheld from the employee\\'s pay</small></span><b>'+money(r.cur,pt/12)+'</b></li>';
 rows+=r.fee?'<li><span>Paybooks fee<small>$'+r.fee+' per employee a month'+(r.usd>1?', shown in '+r.code:'')+'</small></span><b>'+money(r.cur,fee/12)+'</b></li>':'<li><span>Paybooks fee<small>set by country</small></span><b>In your quote</b></li>';
 rows+='<li class="tot"><span>Total per employee, per month</span><b>'+money(r.cur,(s+stat+fee)/12)+'</b></li>';
 document.getElementById('ce_rows').innerHTML=rows;document.getElementById('ce_total').textContent=money(r.cur,(s+stat+fee)/12);document.getElementById('ce_stat').textContent=(stat/s*100).toFixed(1)+'%';document.getElementById('ce_year').textContent=money(r.cur,(s+stat+fee)*n);document.getElementById('ce_year_l').textContent='a year for '+n+(n===1?' hire':' hires');
 document.getElementById('ce_src').innerHTML=(r.extra?r.extra+' ':'')+(r.yearNote?r.yearNote+'. ':'')+'Sources: '+r.src.map(function(x){return '<a href="'+x[1]+'"'+(x[1].indexOf('http')===0?' rel="nofollow" target="_blank"':'')+'>'+x[0]+'</a>'}).join(', ')+'.';
 note.textContent=k==='IN'?'About $'+Math.round(s/r.usd).toLocaleString('en-US')+' a year at ₹95.7 per $1.':''}
N.oninput=draw;ST.onchange=draw;RR=R;CALC=calc;if(panel)show('India','Asia-Pacific');sel.onchange=draw;sl.oninput=draw;draw();
})();</script>'''

schema = [
    {"@context": "https://schema.org", "@type": "Organization", "name": "Paybooks, a TransPerfect company", "url": "https://paybooks.transperfect.com/", "parentOrganization": {"@type": "Organization", "name": "TransPerfect", "url": "https://www.transperfect.com/"}},
    {"@context": "https://schema.org", "@type": "Service", "name": "Employer of Record services", "serviceType": "Employer of Record", "areaServed": "42 countries", "provider": {"@type": "Organization", "name": "Paybooks, a TransPerfect company"}},
    {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://paybooks.transperfect.com/"}, {"@type": "ListItem", "position": 2, "name": "Employer of Record", "item": "https://paybooks.transperfect.com/employer-of-record/"}]},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
HEAD = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{esc(TITLE)}</title><meta name="description" content="{esc(DESC)}"><link rel="canonical" href="https://paybooks.transperfect.com/employer-of-record/"><meta name="robots" content="noindex,nofollow">'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@500;600;700&family=Inter:wght@400;500;600;700&family=Zilla+Slab:wght@300;400&display=swap" rel="stylesheet"><link rel="stylesheet" href="assets/pb.css">'
        + "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in schema) + EXTRA_CSS + '</head>')
FOOT = ('<footer class="ftr"><div class="wrap" style="grid-template-columns:1fr"><div><h4>Paybooks, a TransPerfect company</h4><p>Employer of Record, Multi-Country Payroll, Managed India Office and Global HCM for companies building teams across borders.</p></div></div></footer>'
        '<script src="assets/protect.js" defer></script></body></html>')
page = HEAD + HEADER + "<main>" + hero + fit + countries + hire + control + comp + cost + compare + exits + service + timeline + proof + faq + cta + REVEAL + JS + "</main>" + FOOT
open(OUT, "w", encoding="utf-8").write(page)
print("hub v2 written", len(page))
