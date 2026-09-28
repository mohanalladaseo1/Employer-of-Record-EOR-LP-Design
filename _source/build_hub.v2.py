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
def head(n, eyebrow, h2, sub): return f'<div class="head rv"><span class="num">{n}</span><div><span class="eyebrow">{eyebrow}</span><h2>{esc(h2)}</h2><p>{sub}</p></div></div>'

TITLE = "Employer of Record (EOR) Services | Hire in 42 Countries Without an Entity | Paybooks, a TransPerfect company"
DESC = "Hire employees in 42 countries without setting up an entity. Paybooks becomes the legal employer and runs contracts, payroll, taxes and benefits under local law. Estimate the cost, check your fit, get a quote."

hero = (f'<section class="hero v2"><div class="wrap"><div class="grid"><div><span class="cta2-tag hero-tag">Global Employer of Record</span>'
        '<h1>Hire in 42 countries. <em>No entity needed.</em></h1>'
        '<p class="sub">Paybooks becomes the legal employer of your people in any of 42 countries. We run the local contract, payroll, taxes and benefits under that country’s law. You choose the people and direct their work.</p>'
        '<div class="btns"><a class="btn" href="#cost">Estimate the cost</a><a class="btn ghost" href="#fit">Check your fit</a></div>'
        f'<ul class="cta2-ticks hero-ticks">{TICKS}</ul></div>{VID}</div></div></section>{TRUST}')

# ---------- 01 lifecycle stepper ----------
STAGES = [
 ("Offer", "You choose the candidate and agree the role, pay and start date. Recruiting stays with you.", "We confirm the full monthly cost for that country and send the contract terms within your quote.", "A clear offer, in their language, with your company, manager and role named."),
 ("Contract", "You approve the package.", "We sign the local employment contract on our entity: notice, probation, working hours and leave written the way the country requires. IP is assigned to you.", "A real local employment contract with a real local employer."),
 ("Onboarding", "You plan their first day and their work.", "We collect documents, complete registrations and, where you ask, run background checks.", "Contract, documents and registrations done before day one."),
 ("Payroll", "You approve raises, bonuses and equity grants.", "We pay salary on the local payroll date, in local currency, and withhold, file and pay every tax and social contribution.", "Pay on time, every month, with payslips and tax forms in one app."),
 ("Benefits", "You choose any extras above the statutory minimum.", "We enroll them in the statutory benefits and any extras you choose, and handle claims and leave.", "Everything the law requires, plus what you add."),
 ("Compliance", "You set policies within local law.", "We track every filing and rule change, keep proof of every filing, and flag roles that could create a taxable presence for you.", "An employer that never misses a filing."),
 ("Exit or transfer", "You decide when to part ways, or when to open your own entity.", "We issue the termination under local law with the notice and severance due, or move their contract to your new entity with service unbroken.", "A clean exit, or the same job under your own name."),
]
tabs = "".join(f'<button class="lc-tab{" on" if i == 0 else ""}" data-i="{i}" type="button"><span>{i+1}</span>{esc(n)}</button>' for i, (n, *_ ) in enumerate(STAGES))
panes = "".join(f'<div class="lc-pane{" on" if i == 0 else ""}" data-i="{i}"><div class="lc-col you"><small>You</small><p>{esc(y)}</p></div><div class="lc-col us"><small>Paybooks</small><p>{esc(u)}</p></div><div class="lc-col hire"><small>Your hire sees</small><p>{esc(h)}</p></div></div>' for i, (n, y, u, h) in enumerate(STAGES))
lifecycle = ('<section class="sec" id="how"><div class="wrap">' + head("01", "How it works", "Who does what, from offer to exit",
             "An Employer of Record legally employs people on your behalf in a country where you have no entity. Click a stage to see what stays with you and what Paybooks takes on.")
             + f'<div class="lc"><div class="lc-tabs">{tabs}</div>{panes}</div></div></section>')

# ---------- 02 fit finder ----------
fit = ('<section class="sec alt" id="fit"><div class="wrap">' + head("02", "Fit finder", "Is an Employer of Record right for you?", "Three questions. The answer names the right Paybooks service, and when it is not us.")
       + '''<div class="ff"><div class="ff-q"><div class="ff-step"><b>1 · Where do you stand in the country you want to hire in?</b><div class="ff-opts" data-q="entity">
<button type="button" data-v="none">No entity there</button><button type="button" data-v="own">We have our own entity</button><button type="button" data-v="india">We have an entity in India</button></div></div>
<div class="ff-step"><b>2 · How many people, in that country?</b><div class="ff-opts" data-q="size">
<button type="button" data-v="s">1 to 5</button><button type="button" data-v="m">6 to 20</button><button type="button" data-v="l">21 to 50</button><button type="button" data-v="xl">More than 50</button></div></div>
<div class="ff-step"><b>3 · What are you trying to do?</b><div class="ff-opts" data-q="goal">
<button type="button" data-v="test">Test a new market</button><button type="button" data-v="build">Build a long-term team</button><button type="button" data-v="convert">Employ contractors properly</button><button type="button" data-v="run">Run payroll in several countries</button></div></div></div>
<div class="ff-a" id="ffa"><div class="ff-empty"><b>Answer the three questions</b><p>Your recommendation appears here, with the reason and the option we would not suggest.</p></div></div></div>'''
       + '</div></section>')

# ---------- 03 country search ----------
COUNTRIES = [(c, "6A") for c in PH["6A"]] + [(c, "6B") for c in PH["6B"]] + [(c, "6C") for c in PH["6C"]]
chips = "".join((f'<a class="cc live" href="employer-of-record/india/" data-n="{esc(c)}"><b>{esc(c)}</b><span>Country guide live →</span></a>' if c == "India" else
                 f'<button type="button" class="cc" data-n="{esc(c)}"><b>{esc(c)}</b><span>Guide coming · get a quote</span></button>') for c, ph in COUNTRIES)
countries = ('<section class="sec" id="countries"><div class="wrap">' + head("03", "Countries", "Find your country", "42 countries. Type a country to check it, or pick one below.")
             + f'<div class="cs"><input id="csq" type="search" placeholder="Type a country, for example Germany" autocomplete="off" aria-label="Find your country"><span id="csn">42 countries</span></div>'
             f'<div class="cgrid" id="cgrid">{chips}</div><p class="fine" id="csmsg"></p></div></section>')

# ---------- 04 cost estimator ----------
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
QUOTE_ONLY = [c for c, _ in COUNTRIES if c not in {v["name"] for v in RATES.values()}]
opts = "".join(f'<option value="{k}">{esc(v["name"])}</option>' for k, v in RATES.items()) + "".join(f'<option value="Q:{esc(c)}">{esc(c)} · in your quote</option>' for c in QUOTE_ONLY)
cost = ('<section class="sec alt" id="cost"><div class="wrap">' + head("04", "Cost estimator", "What an employee costs, country by country",
        "Salary, the employer contributions the country's law requires, and our fee. Statutory rates come from each country's official source, linked below the result.")
        + f'''<div class="ce"><div class="ce-in"><label for="cec">Country</label><select id="cec">{opts}</select>
<label for="ces">Annual salary <span id="cesv"></span></label><input id="ces" type="range"><p class="fine" id="cenote"></p></div>
<div class="ce-out"><div class="kpis"><div class="kpi"><b id="ce_total"></b><span>all-in per month</span></div><div class="kpi"><b id="ce_stat"></b><span>employer costs on top of salary</span></div><div class="kpi"><b id="ce_year"></b><span>all-in per year</span></div></div>
<ul class="lines" id="ce_rows"></ul><p class="fine" id="ce_src"></p></div></div>
<p class="fine">Headline statutory rates. Thresholds noted in each line are applied; other caps, regional rates and any benefits you add are applied in your written quote, which is final. Paybooks’ fee for countries other than India is set by country and shown in your quote.</p></div></section>''')

# ---------- 05 compliance strip, timeline, proof, faq, cta ----------
comp = ('<section class="sec" id="compliance"><div class="wrap">' + head("05", "Compliance", "Local law, handled in every country", "Employment rules differ in every country. Getting them right is our job, not yours.")
        + '<ul class="chk">' + "".join(f'<li><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a, b in [
            ("Contracts under local law", "Notice, probation, hours and leave written as the country requires."), ("Taxes and social security", "Withheld, filed and paid on time, with proof of every filing."),
            ("Misclassification risk removed", "Full-time workers employed properly, not paid as contractors."), ("Exits done right", "Notice, severance and final pay under local rules."),
            ("IP assigned to you", "Every contract assigns the work and the intellectual property to your company."), ("Tax risk flagged early", "Roles that could create a taxable presence are flagged before you hire.")]) + '</ul>'
        '<div class="clause" style="margin-top:22px"><b>In India:</b> Paybooks’ published promise of no penalties ever on the filings and payments it handles. <a href="employer-of-record/india/">See Employer of Record India</a>.</div></div></section>')
proof = ('<section class="dark" id="proof"><div class="wrap"><div class="head rv"><span class="num">06</span><div><span class="eyebrow">Why Paybooks</span><h2>Payroll depth. A global parent.</h2></div></div>'
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
faq = ('<section class="sec alt" id="faq"><div class="wrap"><div class="faq"><div class="sticky"><span class="eyebrow">FAQ</span><h2>Your questions, answered</h2><p style="color:var(--muted);margin:14px 0 22px">What to know before you hire abroad.</p><a class="btn" href="#quote">Talk to an EOR expert</a></div><div>'
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
.lc{background:#fff;border:1px solid var(--line);border-radius:20px;overflow:hidden}
.lc-tabs{display:flex;overflow-x:auto;border-bottom:1px solid var(--line);scrollbar-width:none}.lc-tabs::-webkit-scrollbar{display:none}
.lc-tab{flex:1 0 auto;display:flex;align-items:center;gap:10px;padding:16px 18px;border:0;border-bottom:3px solid transparent;background:none;font:600 14.5px Inter,sans-serif;color:var(--muted);cursor:pointer;white-space:nowrap}
.lc-tab span{width:24px;height:24px;border-radius:50%;background:#EEF1EC;font-size:12px;display:grid;place-items:center;color:var(--ink)}
.lc-tab.on{color:var(--ink);border-bottom-color:var(--green)}.lc-tab.on span{background:var(--green);color:#fff}
.lc-pane{display:none;grid-template-columns:1fr 1fr 1fr;gap:0}.lc-pane.on{display:grid}
.lc-col{padding:26px 26px 28px}.lc-col+.lc-col{border-left:1px solid var(--line)}.lc-col small{display:block;font:700 11.5px Inter;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.lc-col.us{background:#F5F9EF}.lc-col.us small{color:var(--g600)}.lc-col p{margin:0;font-size:15.5px;line-height:1.55;color:var(--ink2)}
.ff{display:grid;grid-template-columns:1.15fr .85fr;gap:20px}.ff-q{display:grid;gap:14px}.ff-step{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px}.ff-step>b{display:block;font-family:var(--head);font-size:16.5px;margin-bottom:10px}
.ff-opts{display:flex;flex-wrap:wrap;gap:8px}.ff-opts button{border:1px solid var(--line);background:#FAFBF8;border-radius:999px;padding:9px 14px;font:500 14px Inter,sans-serif;color:var(--ink);cursor:pointer}
.ff-opts button.on{background:var(--forest);color:#fff;border-color:var(--forest)}
.ff-a{background:var(--forest);color:#fff;border-radius:20px;padding:28px;position:sticky;top:90px;align-self:start;min-height:220px}.ff-a b{font-family:var(--head)}.ff-empty b{font-size:20px;display:block;margin-bottom:8px}.ff-empty p{color:#BFD3B9;margin:0;font-size:15px}
.ff-r small{display:block;font:700 11.5px Inter;letter-spacing:.1em;text-transform:uppercase;color:var(--lime);margin-bottom:8px}.ff-r h3{font-size:26px;margin:0 0 10px;color:#fff}.ff-r p{color:#DDE8D6;font-size:15px;line-height:1.55;margin:0 0 10px}.ff-r .no{color:#BFD3B9;font-size:13.5px;border-top:1px solid rgba(255,255,255,.14);padding-top:12px;margin-top:12px}.ff-r .btn{margin-top:14px}
.cs{display:flex;gap:14px;align-items:center;margin-bottom:16px}.cs input{flex:1;height:50px;border:1px solid var(--line);border-radius:12px;padding:0 16px;font:500 16px Inter,sans-serif;background:#fff}.cs input:focus{outline:none;border-color:var(--green);box-shadow:0 0 0 3px rgba(79,138,16,.15)}.cs span{font-size:13.5px;color:var(--muted);white-space:nowrap}
.cgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.cc{display:flex;flex-direction:column;gap:3px;text-align:left;background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px;text-decoration:none;color:inherit;font:inherit;cursor:pointer}
.cc b{font-family:var(--head);font-size:16px}.cc span{font-size:12.5px;color:var(--muted)}.cc.live{border-color:var(--green);box-shadow:0 10px 30px -18px rgba(79,138,16,.6)}.cc.live span{color:var(--green);font-weight:600}.cc.hide{display:none}.cc.pick{border-color:var(--orange);background:#FFF7F1}
.ce{display:grid;grid-template-columns:.9fr 1.1fr;gap:20px;background:#0B1F14;color:#fff;border-radius:24px;padding:28px}.ce label{display:block;font:600 13px Inter;letter-spacing:.06em;text-transform:uppercase;color:#BFD3B9;margin:14px 0 8px}.ce label span{color:#fff;text-transform:none;letter-spacing:0;font-size:15px;margin-left:8px}
.ce select{width:100%;height:46px;border-radius:10px;border:1px solid rgba(255,255,255,.18);background:#143A25;color:#fff;font:500 15px Inter,sans-serif;padding:0 12px}.ce input[type=range]{width:100%;accent-color:var(--lime)}
.ce .fine{color:#8FAF86;font-size:12.5px}.ce .fine a{color:#9FD35C}.ce-out .kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.ce-out .kpi{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:12px 14px}.ce-out .kpi b{display:block;font-family:var(--head);font-size:22px;color:#9FD35C;line-height:1.1}.ce-out .kpi span{display:block;font-size:11.5px;color:#8FAF86;margin-top:3px}
.lines{list-style:none;margin:14px 0 0;padding:0}.lines li{display:flex;justify-content:space-between;gap:14px;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.08);font-size:14px}.lines li span{color:#BFD3B9}.lines li small{display:block;color:#8FAF86;font-size:12px}.lines li b{white-space:nowrap}.lines li.tot{border-bottom:0;font-weight:700;color:#fff}
.chk{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px 22px}.chk li{display:grid;grid-template-columns:20px 1fr;gap:2px 10px;padding:12px 0;border-bottom:1px solid var(--line)}.chk li::before{content:"✓";color:var(--green);font-weight:700;grid-row:span 2}.chk b{display:block;font-size:15px}.chk span{font-size:13.5px;color:var(--muted)}
@media(max-width:900px){.ff,.ce{grid-template-columns:1fr}.ff-a{position:static}.cgrid{grid-template-columns:1fr 1fr}.lc-pane.on{grid-template-columns:1fr}.lc-col+.lc-col{border-left:0;border-top:1px solid var(--line)}.chk{grid-template-columns:1fr}}
@media(max-width:560px){.cgrid{grid-template-columns:1fr}.ce-out .kpis{grid-template-columns:1fr}}
</style>'''

JS = '''<script>(function(){
var tabs=[].slice.call(document.querySelectorAll('.lc-tab')),panes=[].slice.call(document.querySelectorAll('.lc-pane'));
tabs.forEach(function(t){t.onclick=function(){tabs.forEach(function(x){x.classList.toggle('on',x===t)});panes.forEach(function(p){p.classList.toggle('on',p.dataset.i===t.dataset.i)})}});
var ans={},A=document.getElementById('ffa');
function rec(){if(!(ans.entity&&ans.size&&ans.goal))return;var r;
 if(ans.goal==='run'||(ans.entity==='own'&&ans.goal!=='convert'))r={t:'Multi-Country Payroll',w:'You already employ people through your own entity. What you need is one provider, one report and one standard for payroll in every country.',n:'An EOR, which is for hiring where you have no entity.'};
 else if(ans.entity==='india'&&(ans.size==='l'||ans.size==='xl'))r={t:'Managed India Office',w:'You have the India entity; Paybooks runs it: payroll and HR, books, tax and statutory filings, corporate and regulatory work.',n:'An EOR for a team this size when the entity already exists.'};
 else if(ans.goal==='convert')r={t:'Employer of Record, contractor conversion',w:'Full-time contractors are employed properly on local contracts, which removes the misclassification risk while you keep the same people.',n:'Leaving them as contractors.'};
 else if(ans.size==='xl'&&ans.goal==='build')r={t:'Your own entity, with Paybooks payroll',w:'Above roughly 50 people in one country, owning an entity usually costs less per person. Start on EOR if you need to hire before it exists; we move the team over when it is ready.',n:'Staying on an EOR at this size for the long term.'};
 else if(ans.entity==='none')r={t:'Employer of Record',w:(ans.goal==='test'?'Hire now and decide on an entity once the market proves itself. No entity to set up, nothing to close if you change course.':'Hire within days with no entity to set up. When the team is large enough to justify an entity, we set it up and move everyone across.'),n:(ans.goal==='test'?'Committing to an entity before the market is proven.':'Opening an entity before you have hired anyone.')};
 else r={t:'Employer of Record',w:'Hire in the new country without waiting for an entity there. Your existing entities are unaffected.',n:'Setting up another entity for a small team.'};
 A.innerHTML='<div class="ff-r"><small>Our recommendation</small><h3>'+r.t+'</h3><p>'+r.w+'</p><div class="no"><b>Not recommended:</b> '+r.n+'</div><a class="btn" href="#quote">Get a quote for a role</a></div>'}
[].slice.call(document.querySelectorAll('.ff-opts')).forEach(function(g){[].slice.call(g.children).forEach(function(b){b.onclick=function(){[].slice.call(g.children).forEach(function(x){x.classList.toggle('on',x===b)});ans[g.dataset.q]=b.dataset.v;rec()}})});
var q=document.getElementById('csq'),chips=[].slice.call(document.querySelectorAll('.cc')),n=document.getElementById('csn'),msg=document.getElementById('csmsg');
function filt(){var v=(q.value||'').trim().toLowerCase(),k=0;chips.forEach(function(c){var h=c.dataset.n.toLowerCase().indexOf(v)>-1;c.classList.toggle('hide',!h);if(h)k++});n.textContent=k+(k===1?' country':' countries');msg.textContent=(v&&!k)?'Not on the 42-country list yet. Send us the country with your quote request and we will confirm.':''}
q.addEventListener('input',filt);
chips.forEach(function(c){if(c.tagName==='BUTTON')c.onclick=function(){chips.forEach(function(x){x.classList.toggle('pick',x===c)});msg.textContent=c.dataset.n+': the country guide is on its way. Get a quote for a role there and we will send the full cost and contract terms.'}});
var R='''+json.dumps(RATES)+''',sel=document.getElementById('cec'),sl=document.getElementById('ces'),sv=document.getElementById('cesv'),note=document.getElementById('cenote');
function money(c,x){return c+Math.round(x).toLocaleString('en-US')}
function calc(k,s){var L=[];
 if(k==='IN'){var b=s/2,g=s/12;L.push(['Provident fund','12% of basic pay',b*.12]);L.push(['Gratuity','4.81% of basic pay',b*.0481]);if(g<=21000)L.push(['State insurance (ESI)','3.25% of gross, gross is ₹21,000 a month or less',s*.0325]);}
 if(k==='US'){L.push(['Social Security','6.2% up to $184,500',Math.min(s,184500)*.062]);L.push(['Medicare','1.45% of pay',s*.0145]);L.push(['Federal unemployment (FUTA)','0.6% of the first $7,000',Math.min(s,7000)*.006]);}
 if(k==='UK'){L.push(['Employer National Insurance','15% above £5,000',Math.max(0,s-5000)*.15]);L.push(['Workplace pension, employer minimum','3% of £6,240 to £50,270',Math.max(0,Math.min(s,50270)-6240)*.03]);}
 if(k==='SG'){L.push(['CPF, employer share','17% of wages, citizens and permanent residents',s*.17]);}
 if(k==='CA'){L.push(['Canada Pension Plan','5.95% of $3,500 to $74,600',Math.max(0,Math.min(s,74600)-3500)*.0595]);L.push(['Employment Insurance, employer share','2.282% up to $68,900',Math.min(s,68900)*.02282]);}
 return L}
function draw(){var k=sel.value;var out=document.querySelector('.ce-out');
 if(k.indexOf('Q:')===0){sl.disabled=true;sv.textContent='';note.textContent='';out.innerHTML='<div class="ff-r" style="padding:6px 0"><small>'+k.slice(2)+'</small><h3>Costed in your quote</h3><p style="color:#DDE8D6">We have not published '+k.slice(2)+'\\'s statutory rates here yet. Send us the role and pay and you get the full monthly cost, the contract terms and a start date.</p><a class="btn" href="#quote">Get a quote for '+k.slice(2)+'</a></div>';return}
 var r=R[k];if(sl.dataset.k!==k){sl.min=r.min;sl.max=r.max;sl.step=r.step;sl.value=r['default'];sl.dataset.k=k;sl.disabled=false;
  out.innerHTML='<div class="kpis"><div class="kpi"><b id="ce_total"></b><span>all-in per month</span></div><div class="kpi"><b id="ce_stat"></b><span>employer costs on top of salary</span></div><div class="kpi"><b id="ce_year"></b><span>all-in per year</span></div></div><ul class="lines" id="ce_rows"></ul><p class="fine" id="ce_src"></p>'}
 var s=+sl.value,L=calc(k,s),stat=L.reduce(function(a,x){return a+x[2]},0),fee=r.fee?r.fee*(r.usd||1)*12:0;
 sv.textContent=money(r.cur,s)+' '+r.code;
 var rows='<li><span>Salary<small>per month</small></span><b>'+money(r.cur,s/12)+'</b></li>'+L.map(function(x){return '<li><span>'+x[0]+'<small>'+x[1]+'</small></span><b>'+money(r.cur,x[2]/12)+'</b></li>'}).join('');
 rows+=r.fee?'<li><span>Paybooks fee<small>$'+r.fee+' per employee a month'+(r.usd>1?', shown in '+r.code:'')+'</small></span><b>'+money(r.cur,fee/12)+'</b></li>':'<li><span>Paybooks fee<small>set by country</small></span><b>In your quote</b></li>';
 rows+='<li class="tot"><span>All-in per month</span><b>'+money(r.cur,(s+stat+fee)/12)+'</b></li>';
 document.getElementById('ce_rows').innerHTML=rows;document.getElementById('ce_total').textContent=money(r.cur,(s+stat+fee)/12);document.getElementById('ce_stat').textContent=(stat/s*100).toFixed(1)+'%';document.getElementById('ce_year').textContent=money(r.cur,s+stat+fee);
 document.getElementById('ce_src').innerHTML=(r.extra?r.extra+' ':'')+(r.yearNote?r.yearNote+'. ':'')+'Sources: '+r.src.map(function(x){return '<a href="'+x[1]+'"'+(x[1].indexOf('http')===0?' rel="nofollow" target="_blank"':'')+'>'+x[0]+'</a>'}).join(', ')+'.';
 note.textContent=k==='IN'?'About $'+Math.round(s/r.usd).toLocaleString('en-US')+' a year at ₹95.7 per $1.':''}
sel.onchange=draw;sl.oninput=draw;draw();
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
page = HEAD + HEADER + "<main>" + hero + lifecycle + fit + countries + cost + comp + proof + faq + cta + REVEAL + JS + "</main>" + FOOT
open(OUT, "w", encoding="utf-8").write(page)
print("hub v2 written", len(page))
