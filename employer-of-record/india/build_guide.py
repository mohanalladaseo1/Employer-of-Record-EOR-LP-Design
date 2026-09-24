# Builds /employer-of-record/india/index.html : Employer of Record India guide (sample content).
# v2: keyword-targeted, plain US English, no visible review tags (they are listed in verify-list.md instead).
# Python 3.9 safe: no backslashes inside f-string expressions.
import json, os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "index.html")
FX = 95.7  # INR per USD, September 23, 2026 (same rate as the landing page calculator)
CANON = "https://www.paybooks.in/employer-of-record/india/"
UPDATED = "September 24, 2026"
PUBLISHED = "September 24, 2026"
# Bylines. Add real people here (name, job title, LinkedIn URL); leave None to credit the team.
WRITER = None      # e.g. ("Full name", "Payroll Compliance Lead", "https://www.linkedin.com/in/...")
REVIEWER = None    # e.g. ("Full name", "Head of Compliance", "https://www.linkedin.com/in/...")
TEAM = "Paybooks Payroll and Compliance team"
LI = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#0A66C2"/><path fill="#fff" d="M7.1 9.5h2.6V18H7.1zM8.4 5.6a1.5 1.5 0 110 3 1.5 1.5 0 010-3zM11.3 9.5h2.5v1.2c.4-.7 1.3-1.4 2.7-1.4 2.8 0 3.3 1.8 3.3 4.2V18h-2.6v-4c0-1 0-2.2-1.4-2.2s-1.6 1.1-1.6 2.1V18h-2.6z"/></svg>'
def person(role, who):
    if not who:
        return '<span class="g-by">' + role + ' <b>' + TEAM + '</b></span>'
    name, title, url = who
    link = ' <a class="g-li" href="' + url + '" target="_blank" rel="noopener" aria-label="' + name + ' on LinkedIn">' + LI + '</a>' if url else ''
    return '<span class="g-by">' + role + ' <b>' + name + '</b> <em>' + title + '</em>' + link + '</span>'
def BYLINE(read_min):
    parts = [person("Written by", WRITER)]
    if REVIEWER: parts.append(person("Reviewed by", REVIEWER))
    parts.append('<span class="g-by">Published: <b>Sep 24, 2026</b></span>')
    parts.append('<span class="g-by">Last updated: <b>Sep 24, 2026</b></span>')
    parts.append('<span class="g-by"><b>' + str(read_min) + ' min</b> read</span>')
    return '<div class="g-bybar">' + '<i class="g-dot"></i>'.join(parts) + '</div>'


# Claims Paybooks must confirm before publishing. Not shown on the page.
VERIFY = []
def V(note):
    VERIFY.append(note)
    return ""

def inr(x):
    x = int(round(x)); s = str(abs(x))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return ("-" if x < 0 else "") + "₹" + s

def usd(x):
    return "$" + format(int(round(x / FX)), ",")

def T(head, rows, cap=None, num=()):
    out = ['<div class="g-tw"><table>']
    if cap: out.append("<caption>" + cap + "</caption>")
    out.append("<thead><tr>" + "".join(
        '<th class="n">' + h + "</th>" if i in num else "<th>" + h + "</th>" for i, h in enumerate(head)) + "</tr></thead><tbody>")
    for r in rows:
        tot = r[0].startswith("!")
        first = r[0][1:] if tot else r[0]
        cells = ['<th scope="row">' + first + "</th>"]
        for i, c in enumerate(r[1:], 1):
            cells.append('<td class="n">' + c + "</td>" if i in num else "<td>" + cell(c) + "</td>")
        out.append('<tr class="tot">' if tot else "<tr>")
        out.append("".join(cells) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)

SRC = {}
def src(key, label, url):
    SRC[key] = (label, url)
    return ' <a class="g-src" href="' + H.escape(url) + '" rel="nofollow noopener" target="_blank">[' + label + ']</a>'
PB = "https://paybooks.in/article/"
def IL(text, slug):
    return '<a href="' + PB + slug + '/">' + text + '</a>'
PILL = {"Yes": "g-yes", "No": "g-no", "None": "g-na", "Not needed": "g-no", "Required": "g-yes"}
def cell(c):
    return '<span class="g-pill-s ' + PILL[c] + '">' + c + '</span>' if c in PILL else c
def CARDS(items):
    return '<div class="g-facts">' + "".join('<div class="g-fact"><small>' + k + '</small><p>' + v + '</p></div>' for k, v in items) + '</div>'
def BAR(title, parts, total_label):
    tot = sum(v for _l, v, _c in parts)
    segs = "".join('<span style="width:' + format(v / tot * 100, ".2f") + '%;background:' + c + '"></span>' for _l, v, c in parts)
    keys = "".join('<li><i style="background:' + c + '"></i>' + l + ' <b>' + usd(v) + '</b></li>' for l, v, c in parts)
    return ('<div class="g-bar"><div class="g-bar-h"><b>' + title + '</b><span>' + total_label + ' <strong>' + usd(tot) + '</strong></span></div>'
            '<div class="g-bar-t">' + segs + '</div><ul>' + keys + '</ul></div>')
def P(*ps): return "".join("<p>" + p + "</p>" for p in ps)
def UL(*xs): return "<ul>" + "".join("<li>" + x + "</li>" for x in xs) + "</ul>"
def CALL(t): return '<div class="g-call"><p>' + t + "</p></div>"
def CTA(title, sub, btn="Get a quote for a role"):
    return '<div class="g-cta"><div><b>' + title + "</b><p>" + sub + '</p></div><a class="btn" href="#quote">' + btn + "</a></div>"

# ---------------- worked cost examples ----------------
def cost_example(gross_m, lwf_emp_y):
    basic = gross_m * 0.5
    lines = [("Gross salary", gross_m * 12, "Agreed yearly pay. Basic pay set at 50% to meet the labor code wage rule.")]
    lines.append(("Employer Provident Fund, 12%", basic * 0.12 * 12, "12% of basic pay. Required on pay up to ₹25,000 a month (from September 17, 2026); most employers pay on full basic."))
    lines.append(("PF admin and EDLI insurance", min(basic, 25000) * 0.01 * 12, "0.5% admin charge plus 0.5% EDLI insurance, on pay up to ₹25,000 a month."))
    esi = gross_m * 0.0325 * 12 if gross_m <= 21000 else 0
    lines.append(("Employer ESI, 3.25%", esi, "Only for staff earning ₹21,000 a month or less." if esi else "Not due. Pay is above ₹21,000 a month."))
    bonus = min(basic, 7000) * 0.0833 * 12 if gross_m <= 21000 else 0
    lines.append(("Statutory bonus, 8.33% minimum", bonus, "Only for staff earning ₹21,000 a month or less, on capped pay." if bonus else "Not due. Pay is above the ₹21,000 limit."))
    lines.append(("Gratuity provision, 4.81%", basic * 0.0481 * 12, "Set aside monthly. Paid on exit after 5 years, or 1 year for fixed-term staff."))
    lines.append(("Labor Welfare Fund, employer share", lwf_emp_y, "Karnataka: ₹100 a year from the employer, ₹50 from the employee."))
    return lines

EX1 = cost_example(200000, 100)
EX2 = cost_example(20000, 100)
FEE_Y = 199 * 12 * FX

def cost_table(lines, cap):
    rows, tot = [], 0
    for name, amt, note in lines:
        tot += amt
        rows.append([name, inr(amt) if amt else "₹0", usd(amt) if amt else "$0", note])
    rows.append(["Paybooks EOR fee", inr(FEE_Y), "$2,388", "From $199 per employee a month, priced in USD. A one-time $50 onboarding fee is not included."])
    tot += FEE_Y
    rows.append(["!Total yearly cost", inr(tot), usd(tot), ""])
    return T(["Cost line", "Per year (INR)", "Per year (USD)", "What it is"], rows, cap, num=(1, 2)), tot

EX1_T, EX1_TOT = cost_table(EX1, "Example 1: senior software engineer in Bengaluru, ₹24 lakh (₹2.4 million) a year")
EX2_T, EX2_TOT = cost_table(EX2, "Example 2: customer support associate in Bengaluru, ₹2.4 lakh (₹240,000) a year")
EX1_ON = (EX1_TOT - 2400000 - FEE_Y) / 2400000 * 100
EX2_ON = (EX2_TOT - 240000 - FEE_Y) / 240000 * 100

SLABS = [(0, 400000, 0), (400000, 800000, 5), (800000, 1200000, 10), (1200000, 1600000, 15),
         (1600000, 2000000, 20), (2000000, 2400000, 25), (2400000, None, 30)]
def tax(gross):
    t_inc = gross - 75000
    t = 0
    for lo, hi, r in SLABS:
        if t_inc > lo:
            top = min(t_inc, hi) if hi else t_inc
            t += (top - lo) * r / 100
    if t_inc <= 1200000: t = 0
    return t_inc, t, t * 0.04
TI, TX, CESS = tax(2400000)

# ---------------- sections ----------------
S = []  # (id, toc label, html)

LEAD = ('<div class="g-takeaways"><span class="g-tag">TL;DR</span>'
        '<p class="g-ans">An <strong>employer of record in India</strong> is an Indian company that legally employs your staff for you. '
        'It issues the contract, pays salary in rupees, withholds income tax, pays Provident Fund and ESI, and files every return. '
        'You choose the person and manage their work. <strong>Budget salary, plus about 8 to 9% in employer contributions for skilled staff, plus the EOR fee</strong> (Paybooks: from $199 per employee a month).</p><ul>'
        '<li><strong>No Indian company needed.</strong> Hire within days, and move staff to your own entity later with their service history intact.</li>'
        '<li><strong>New labor codes since November 21, 2025.</strong> Basic pay must be at least half of total pay, and fixed-term staff earn gratuity after one year.</li>'
        '<li><strong>Long-term contractors are risky.</strong> Courts judge how people actually work, not what the contract calls them.</li></ul></div>')
KT = ""

S.append(("glance", "India at a glance", "<h2>India employment facts at a glance</h2>" + P(
    "India has a large skilled workforce and detailed employment rules. Rules come from both the national government and each state. Here is what employers ask about first.") + CARDS([
        ["Currency", "Indian rupee (INR, ₹). Salary must be paid in rupees to an Indian bank account."],
        ["Tax year", "April 1 to March 31. The new Income-tax Act, 2025 applies from April 1, 2026." + src("it25","PIB","https://www.pib.gov.in/PressReleasePage.aspx?PRID=2248005&reg=3&lang=1")],
        ["Pay frequency", "Monthly. Salary is due by the 7th of the next month."],
        ["Working time", "8 hours a day, 48 hours a week. Overtime is paid at twice the normal rate."],
        ["Employer social security", "Provident Fund at 12% of basic pay, ESI at 3.25% for staff earning up to ₹21,000 a month, gratuity on exit."],
        ["Income tax", "0% to 30%, plus 4% cess, under the default new regime. The employer withholds it monthly."],
        ["Paid leave", "1 day of paid leave for every 20 days worked, after 180 days of work in a year, under the OSH Code."],
        ["Public holidays", "3 national holidays plus state and festival holidays set by each state."],
        ["Probation", "Not set by law. 3 to 6 months is common."],
        ["Notice period", "Set by the contract. 30 to 90 days is common for skilled roles."],
        ["Main laws", "The four labor codes: Wages, Industrial Relations, Social Security, and Occupational Safety, Health and Working Conditions."],
        ["Time to hire with Paybooks", "Within days, with no entity to set up."],
    ])))

S.append(("what", "What an EOR does", "<h2>What does an employer of record do in India?</h2>" + P(
    "An employer of record (EOR) is the legal employer on paper. In India, Paybooks signs the employment contract, pays salary in rupees, withholds income tax, pays Provident Fund and ESI, and files all returns. You choose the candidate, set their work and manage them every day.",
    "You get one monthly invoice for salary, employer contributions and the fee. Your employee gets an Indian employment contract with full statutory benefits.") +
    "<h3>How EOR services in India split the work</h3>" + T(
    ["Task", "Paybooks", "Your company"], [
        ["Choose the candidate and set pay", "Advises on market pay", "Decides"],
        ["Employment contract and appointment letter", "Drafts, issues and signs under Indian law", "Approves role, pay and terms"],
        ["Monthly payroll, payslips and tax", "Runs it end to end", "Approves changes such as raises"],
        ["Provident Fund, ESI, professional tax, welfare fund", "Registers, pays and files", "Nothing to do"],
        ["Benefits and health insurance", "Sets up and runs", "Chooses the plan"],
        ["Daily work and performance", "No role", "Manages directly"],
        ["Laptop and system access", "Can arrange on request", "Usually provides"],
        ["Leave and holidays", "Keeps the legal records", "Approves leave"],
        ["Resignation, termination and final pay", "Runs the legal process and pays dues", "Makes the decision"],
    ], "Who does what")))

S.append(("peo", "EOR vs PEO", "<h2>EOR vs PEO in India: which do you need?</h2>" + P(
    "In the US, a professional employer organization (PEO) co-employs staff with a company that already has a local entity. India has no co-employment model like this. When a provider sells \"PEO services in India,\" it usually means an EOR, or payroll outsourcing for a company that already has an Indian entity.",
    "The rule is simple. No Indian entity? You need an EOR. Already have one? You need payroll and compliance support, which Paybooks also provides.") + T(
    ["Question", "Employer of record", "PEO or payroll outsourcing"], [
        ["Do you need an Indian entity?", "No", "Yes"],
        ["Who is the legal employer?", "Paybooks", "Your Indian company"],
        ["Who holds the government registrations?", "Paybooks (PF, ESI, professional tax, labor welfare)", "Your Indian company"],
        ["Who carries compliance risk?", "Paybooks, backed by its \u201cno penalties ever\u201d promise", "Your company, with provider support"],
        ["Best fit", "First hires, testing the market, teams under about 20 to 25 people", "Established teams with their own entity"],
    ], "EOR vs PEO in India")))

S.append(("entity", "EOR vs own entity", "<h2>EOR vs setting up your own entity in India</h2>" + P(
    "Most foreign companies that stay in India open a private limited company at some point. The question is when. An entity gives you full control and can cost less at scale. But it takes weeks to set up and has fixed costs from day one: a resident director, an office address, an auditor, yearly filings and transfer pricing.",
    "An EOR lets you hire now and decide on an entity once the team is proven. Paybooks can later move your employees to your entity with their service history intact. For a deeper comparison, see our guide to " + IL("EOR vs subsidiary vs PEO in India", "eor-vs-subsidiary-vs-peo-in-india-which-structure-is-right-in-2026") + ".") + T(
    ["Question", "Employer of record", "Own private limited company"], [
        ["Time to first hire", "Within days", "Several weeks at best, often a few months once bank, tax and labor registrations are done"],
        ["Upfront cost", "None beyond any deposit", "Incorporation, legal and registration costs"],
        ["Fixed yearly cost", "None. You pay per employee.", "Audit, company secretary, filings, office and accounting"],
        ["Resident director", "Not needed", "Required. At least one director must stay in India for 182 days or more in the financial year (Companies Act, Section 149(3))."],
        ["Tax exposure for the parent", "Lower, since staff work for an Indian company. Some activities can still create a taxable presence.", "Profits taxed in India; transfer pricing applies"],
        ["Can sign local contracts and bill Indian customers", "No. The EOR only employs.", "Yes"],
        ["Exit", "Give notice; Paybooks handles final pay", "Closing a company is slow and costly"],
        ["Best fit", "Up to about 25 employees, or while you test India", "Large, long-term teams, or selling to Indian customers"],
    ], "EOR vs own entity in India") + CALL(
    "<strong>Rule of thumb.</strong> Below about 20 to 25 employees, an EOR usually costs less than your own entity once audit, compliance staff and management time are counted. Above that, compare the full cost of both.")))

S.append(("contractor", "Contractors vs employees", "<h2>Can you hire contractors in India instead?</h2>" + P(
    "Yes, for genuine project work. But Indian courts look at how the person actually works, not what the contract says. A long-term, full-time contractor who works only for you, under your direction, is likely to count as an employee.",
    "If that happens, you can owe back Provident Fund with interest and damages, unpaid gratuity and leave, and you may face questions about a taxable presence in India. Contractors also get no statutory benefits, which makes good people harder to hire and keep. Misclassification is one of the " + IL("costly mistakes foreign companies make when hiring in India", "top-mistakes-global-companies-make-when-hiring-in-india") + ".") + T(
    ["Question", "Full-time employee", "Independent contractor"], [
        ["Contract", "Employment contract and appointment letter", "Service agreement for set deliverables"],
        ["Working hours", "Fixed hours under labor law", "Sets own hours"],
        ["Control", "Employer directs how and when work is done", "Contractor decides how the work is done"],
        ["Tools", "Usually provided by the employer", "Contractor's own"],
        ["Pay", "Monthly salary in rupees, tax withheld", "Sends invoices; handles own tax and GST"],
        ["Statutory benefits", "PF, ESI where eligible, gratuity, paid leave, maternity benefit", "None"],
        ["Intellectual property", "Employer owns work done on the job", "Needs a written assignment"],
        ["Ending the relationship", "Notice and statutory dues", "As the agreement says"],
    ], "Employee vs contractor in India") +
    "<h3>How Indian courts decide who is an employee</h3>" + P("There is no single test in the law. Courts weigh several together.") + T(
    ["Test", "What the court asks"], [
        ["Control test", "Does the company control what the worker does and how? Affirmed in Dharangadhara Chemical Works v State of Saurashtra (AIR 1957 SC 264)." + src("dcw","Indian Kanoon","https://indiankanoon.org/doc/1996477/")],
        ["Integration test", "Is the worker part of the business, for example on the team, in the org chart, using company email?"],
        ["Economic reality test", "Does the worker depend on this one company for a living, and who carries the business risk?"],
        ["Multiple factor test", "Who hires, pays and can fire the worker, and who supplies the tools?"],
    ], "Employment status tests") + CALL(
    "<strong>Switching contractors to employees is simple.</strong> Paybooks can move your Indian contractors onto employment contracts.")))

S.append(("routes", "How to hire in India", "<h2>How to hire employees in India</h2>" + P(
    "A foreign company has three ways to hire employees in India. The right one depends on team size, speed and how long you plan to stay. Our " + IL("step-by-step guide to hiring in India without a company", "featured-article/how-to-hire-employees-in-india-without-setting-up-a-company-2026-eor-guide") + " covers each route in detail.") + T(
    ["Route", "How it works", "Speed", "Best for"], [
        ["Own subsidiary", "Set up a private limited company, register for tax, PF and ESI, then hire directly", "Slowest: weeks to months", "Large, long-term teams"],
        ["Employer of record", "Paybooks employs the person for you under Indian law", "Within days", "First hires, small and growing teams"],
        ["Contractors", "Engage self-employed professionals for set projects", "Fast", "Genuinely short, project-based work"],
    ], "Ways to hire in India") +
    "<h3>Hiring through Paybooks, step by step</h3><ol>" +
    "<li><strong>Share the role, city and pay.</strong> We send the full monthly cost in dollars.</li>" +
    "<li><strong>Make the offer.</strong> We draft an offer letter that names your company, the manager and the role.</li>" +
    "<li><strong>Onboard.</strong> The employee uploads documents online. We run the background checks you choose and register them for PF and ESI.</li>" +
    "<li><strong>Sign.</strong> Paybooks issues the appointment letter and employment contract.</li>" +
    "<li><strong>First payroll.</strong> The employee is paid by the 7th of the next month, with a payslip and tax withheld.</li></ol>" +
    CTA("See what your first India hire will cost", "Send the role, city and salary. Get the full monthly cost in dollars.")))

S.append(("onboarding", "Documents and contracts", "<h2>Onboarding documents and employment contracts</h2>" + P(
    "The OSH Code requires a written appointment letter for every employee in covered establishments, including existing staff." + src("osh","OSH Code","https://dgfasli.gov.in/public/Admin/Cms/AllPdf/OSH_Gazette.pdf") + " Paybooks issues it with a full employment contract, both in English.") + T(
    ["Document", "Indian citizens", "Foreign nationals"], [
        ["Tax ID", "PAN card (Permanent Account Number)", "PAN, applied for on arrival if needed"],
        ["Identity and address", "Aadhaar card, passport or voter ID", "Passport"],
        ["Right to work", "Not needed", "Employment visa and FRRO registration where required"],
        ["Provident Fund", "Universal Account Number (UAN) if employed before", "Contributes as an international worker: 12% on full salary, no ceiling. Workers from Social Security Agreement countries are exempt with a certificate of coverage."],
        ["Education and work history", "Degree certificates, relieving letters, last payslips", "Same, plus attested copies if asked"],
        ["Bank account", "Indian account in the employee's name", "Indian account (NRO or resident)"],
        ["Tax declaration", "Choice of old or new tax regime, investment proofs", "Same"],
    ], "Documents needed at onboarding") +
    "<h3>What an Indian employment contract should cover</h3>" + UL(
    "Job title, duties, work location and remote-work terms.",
    "Start date, probation period and confirmation terms.",
    "Salary split into basic pay, allowances and variable pay, with gross and cost-to-company (CTC) figures.",
    "Working hours, leave and holidays under the state law that applies.",
    "Notice period for both sides and grounds for termination.",
    "Confidentiality, data protection and assignment of intellectual property.",
    "Non-solicitation. Non-compete clauses after employment are void in India under Section 27 of the Indian Contract Act; restraints during employment and confidentiality terms are enforceable.") +
    "<h3>Contract types</h3>" + T(
    ["Type", "Use", "Key rule"], [
        ["Permanent", "Most roles", "Runs until resignation or termination"],
        ["Fixed-term", "Projects or time-bound roles", "Same pay and benefits as permanent staff. Gratuity after 1 year."],
        ["Part-time", "Reduced hours", "Pay and leave in proportion to hours; the Code on Social Security has no minimum-hours test, so social security still applies"],
        ["Internship or apprenticeship", "Students and recent graduates", "Apprentices under the Apprentices Act are excluded from social security; paid interns who work like employees are treated as employees"],
    ], "Employment contract types")))

S.append(("cost", "EOR cost in India", "<h2>How much does an employer of record in India cost?</h2>" + P(
    "The total cost has three parts: gross salary, employer contributions and the EOR fee. For skilled staff, employer contributions add about 8 to 9% to salary. For staff earning ₹21,000 a month or less, ESI and statutory bonus push that to about 15%.",
    "Here are two worked examples at ₹95.7 to $1 (September 23, 2026). Your quote uses the live exchange rate. Health insurance is optional and priced per plan, so it is left out. See our " + IL("state-by-state guide to PF, ESI, PT and LWF", "pf-esi-pt-and-lwf-a-state-by-state-compliance-guide-for-indian-payroll") + " for rates in every state.") +
    BAR("Example 1: senior engineer, ₹24 lakh", [("Salary", 2400000, "#0F2E1A"), ("Employer contributions", EX1_TOT - 2400000 - FEE_Y, "#7DB23A"), ("EOR fee", FEE_Y, "#F26B1D")], "Total a year") +
    EX1_T + CALL("<strong>Example 1 in one line.</strong> A ₹24 lakh salary (about " + usd(2400000) + ") costs about " + usd(EX1_TOT) + " a year in total. Employer costs beyond salary and the fee add about " + format(EX1_ON, ".1f") + "%.") +
    BAR("Example 2: support associate, ₹2.4 lakh", [("Salary", 240000, "#0F2E1A"), ("Employer contributions", EX2_TOT - 240000 - FEE_Y, "#7DB23A"), ("EOR fee", FEE_Y, "#F26B1D")], "Total a year") +
    EX2_T + CALL("<strong>Example 2 in one line.</strong> At lower pay, ESI and statutory bonus apply, so employer costs add about " + format(EX2_ON, ".1f") + "% before the fee. The $199 starting fee is a bigger share of a small salary, so we quote every role separately.") +
    "<h3>Employer contributions in India</h3>" + T(
    ["Contribution", "Employer pays", "Employee pays", "Who it covers"], [
        ["Provident Fund (EPF and EPS)", "12% of basic pay (8.33% to pension, 3.67% to EPF)", "12% of basic pay", "Required on pay up to ₹25,000 a month from September 17, 2026" + src("epf","BDO","https://www.bdo.in/en-gb/insights/alerts-updates/alert-new-epf-ceiling-hiked")],
        ["PF admin and EDLI", "0.5% + 0.5%", "None", "On PF pay up to the ceiling"],
        ["Employees' State Insurance (ESI)", "3.25% of gross", "0.75% of gross", "Staff earning ₹21,000 a month or less" + src("esic","ESIC","https://esic.gov.in/coverage")],
        ["Statutory bonus", "8.33% to 20%, on ₹7,000 or the minimum wage, whichever is higher", "None", "Staff earning ₹21,000 a month or less"],
        ["Gratuity", "About 4.81% of basic, paid on exit", "None", "After 5 years, or 1 year for fixed-term staff"],
        ["Professional tax", "None (employer withholds and pays)", "Up to ₹2,500 a year. Karnataka: ₹200 a month on pay of ₹25,000 or more, ₹300 in February", "Most states, including Karnataka and Maharashtra"],
        ["Labor Welfare Fund", "Small fixed amount (Karnataka: ₹100 a year)", "Small fixed amount (Karnataka: ₹50 a year)", "States that charge it" + src("klwf","Karnataka LWF Act 2024","https://prsindia.org/files/bills_acts/bills_states/karnataka/2024/Bill44of2024KA.pdf")],
    ], "Statutory contributions in India") +
    CTA("Get the full cost for your role", "Every line above, for your city and salary, in dollars. No commitment.")))

S.append(("salary", "Salary structure", "<h2>How salaries are structured in India</h2>" + P(
    "Indian salaries are quoted as a yearly cost-to-company (CTC) figure, split into parts. The split matters because it sets Provident Fund, gratuity and the employee's income tax.",
    "Under the labor codes, basic pay plus dearness allowance must be at least 50% of total pay. If allowances go above 50%, the extra counts as wages for PF and gratuity. Most employers now set basic pay at 50%." + src("cow","Code on Wages","https://www.labour.gov.in/static/uploads/2025/07/b0620548445580767b5c0d18c95c26f7.pdf") + " More on " + IL("salary structure rules under the labor codes", "salary-structure-compliance-risk-india") + ".") + T(
    ["Part", "Typical share", "Notes"], [
        ["Basic salary", "50% of gross", "Sets PF and gratuity. Must meet the 50% wage rule."],
        ["House rent allowance (HRA)", "Up to 50% of basic in metro cities", "Tax-free only under the old tax regime"],
        ["Special allowance", "The balance", "Fully taxable; flexible"],
        ["Employer NPS contribution", "Up to 14% of basic", "Tax-deductible for the employee, even under the new regime"],
        ["Meal, fuel or phone allowances", "Small, fixed", "Tax treatment depends on regime and limits"],
        ["Variable pay or bonus", "Often 10 to 20% of CTC for senior roles", "Paid through payroll with tax withheld"],
    ], "Typical salary structure in India") + P(
    "Each state sets minimum wages by skill level and zone. The Code on Wages lets the national government set a floor wage that no state can go below; the amount has not yet been announced. Professional salaries are far above these floors. Support and operations roles should be checked against the state table.")))

S.append(("tax", "Income tax", "<h2>Income tax and payroll taxes in India</h2>" + P(
    "The employer withholds income tax (TDS) from salary every month and deposits it with the government. Employees choose the default new regime, with lower rates and few deductions, or the old regime, with higher rates and exemptions such as HRA and Section 80C investments. Compare them in our " + IL("new vs old tax regime guide", "new-tax-regime-vs-old-tax-regime") + ".") + T(
    ["Taxable income (new regime)", "Rate"], [
        ["Up to ₹4,00,000", "0%"], ["₹4,00,001 to ₹8,00,000", "5%"], ["₹8,00,001 to ₹12,00,000", "10%"],
        ["₹12,00,001 to ₹16,00,000", "15%"], ["₹16,00,001 to ₹20,00,000", "20%"], ["₹20,00,001 to ₹24,00,000", "25%"],
        ["Above ₹24,00,000", "30%"],
    ], "New regime tax rates, tax year 2026-27", num=(1,)) + UL(
    "Salaried employees get a ₹75,000 standard deduction under the new regime.",
    "A rebate means no tax on taxable income up to ₹12,00,000 under the new regime (Section 156 of the 2025 Act, formerly Section 87A).",
    "A 4% health and education cess is added to the tax. A surcharge applies above ₹50 lakh, capped at 25% under the new regime." + src("kpmg","KPMG","https://kpmg.com/xx/en/our-insights/gms-flash-alert/2026/flash-alert-2026-037.html")) + T(
    ["Step", "Amount"], [
        ["Gross salary", inr(2400000)], ["Less standard deduction", inr(-75000)], ["Taxable income", inr(TI)],
        ["Income tax on the slabs", inr(TX)], ["Health and education cess, 4%", inr(CESS)],
        ["!Total yearly tax", inr(TX + CESS)], ["Withheld each month", inr((TX + CESS) / 12)],
    ], "Worked example: employee tax on ₹24 lakh, new regime", num=(1,)) + P(
    "India has no separate employer payroll tax beyond the contributions above.")))

S.append(("codes", "India's labor codes", "<h2>India's new labor codes: what changed in November 2025</h2>" + P(
    "On November 21, 2025, four labor codes (called the Labour Codes in Indian law) replaced 29 older national labor laws." + src("pib","PIB","https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251121701501.pdf") + " The central rules followed in May 2026, and states issue their own rules, so some details differ by state. Read our " + IL("labor code implementation guide", "labour-code-implementation-in-india") + " for the detail.") + T(
    ["Change", "What it means for employers"], [
        ["One definition of wages", "Allowances above 50% of pay count as wages. This raises PF and gratuity where basic pay was low."],
        ["Appointment letters", "Every employee in a covered establishment must get a written appointment letter."],
        ["Gratuity for fixed-term staff", "Due after 1 year of service instead of 5."],
        ["National floor wage", "The national government will set a floor that no state minimum wage can go below."],
        ["Faster final pay", "Wages are due within 2 working days of resignation, removal or dismissal (Code on Wages, Section 17(2))."],
        ["Leave eligibility", "Workers earn annual leave after 180 days worked in a year, down from 240."],
        ["Worker Re-skilling Fund", "Employers pay 15 days' last-drawn wages into a fund for each laid-off worker, within 10 days."],
        ["Higher thresholds", "Standing orders, and government permission for layoffs in industrial establishments, now apply at 300 workers, up from 100."],
        ["Gig and platform workers", "Platforms pay into a welfare fund. Relevant if you hire through platforms."],
        ["Women at night", "Women may work night shifts with consent and safety measures."],
    ], "Key changes under India's labor codes") + CALL(
    "<strong>What this means with an EOR.</strong> Paybooks sets pay structures to the new wage definition and issues the appointment letters, so you do not have to track the changes yourself.")))

S.append(("compliance", "Compliance checklist", "<h2>Employer compliance checklist for India</h2>" + P(
    "An employer in India holds several registrations and files returns every month, quarter and year. With an EOR, Paybooks holds and files all of them. Our " + IL("EOR India compliance checklist", "eor-india-compliance-checklist") + " goes deeper.") + T(
    ["Requirement", "What the employer must do", "How often"], [
        ["Shops and Establishments registration", "Register each office under state law and keep registers", "Once, renewed as required"],
        ["Provident Fund", "Register, pay contributions and file the online challan", "Monthly, by the 15th"],
        ["ESI", "Register eligible staff and pay contributions", "Monthly, by the 15th"],
        ["Income tax (TDS)", "Withhold and deposit tax; file the quarterly return (Form 138, formerly Form 24Q)", "Monthly by the 7th; quarterly returns"],
        ["Form 130 (formerly Form 16)", "Issue the yearly tax certificate to each employee", "Yearly, by June 15"],
        ["Professional tax", "Withhold and pay under state law", "Monthly in most states"],
        ["Labor Welfare Fund", "Pay employer and employee shares", "Twice a year or yearly, by state"],
        ["Minimum wage and on-time pay", "Pay at least the minimum wage, by the 7th", "Monthly"],
        ["Maternity benefit", "26 weeks' paid leave; a creche at 50 or more employees", "As needed"],
        ["Anti-harassment (POSH)", "Written policy and an Internal Committee at 10 or more employees; yearly report", "Ongoing and yearly"],
        ["Data protection", "Handle employee data under the Digital Personal Data Protection Act, 2023; most duties apply from May 2027", "Ongoing" + src("dpdp","PIB","https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190014&reg=3&lang=2")],
    ], "Employer compliance checklist for India") +
    "<h3>What happens if you get it wrong</h3>" + P(
    "Late Provident Fund payments carry 12% yearly interest plus damages that grow with the delay. Missed tax deposits bring interest and penalties, and can affect the employee's tax credit. Labor inspectors can fine employers under the codes, with higher fines for repeat offenses.",
    "Paybooks promises \u201cno penalties ever\u201d on the filings it handles.") +
    CTA("See how Paybooks handles compliance", "Every registration, payment and filing in one monthly service.", "Get a quote for a role")))

S.append(("payroll", "Payroll calendar", "<h2>How payroll works in India</h2>" + P(
    "Payroll in India is monthly. See our " + IL("India payroll compliance calendar 2026", "india-payroll-compliance-calendar-2026") + " for every date. Paybooks collects changes such as new joiners, leave and bonuses, calculates pay and deductions, pays staff by the 7th of the next month and makes every government payment on time. Employees get an online payslip and submit tax declarations in the Paybooks app.") + T(
    ["Deadline", "What is due"], [
        ["7th of each month", "Salary paid; last month's withheld tax deposited (April 30 for March)"],
        ["15th of each month", "Provident Fund and ESI payments and returns" + src("esicc","ESIC","https://esic.gov.in/contribution")],
        ["State due dates", "Professional tax, for example the 20th in Karnataka"],
        ["July 31, October 31, January 31, May 31", "Quarterly TDS returns (Form 138, formerly Form 24Q)"],
        ["June 15", "Form 130 (formerly Form 16) issued to every employee"],
        ["January 15 in Karnataka", "Labor Welfare Fund; other states use their own dates"],
    ], "India payroll calendar") + P(
    "You get one monthly invoice covering salary, employer contributions and the fee, line by line.")))

S.append(("leave", "Leave and holidays", "<h2>Leave, holidays and working hours in India</h2>" + P(
    "Leave is set by the OSH Code and each state's Shops and Establishments Act. Paybooks applies the rules of the state where the employee works. Your own policy can be more generous.") + T(
    ["Leave type", "Entitlement", "Notes"], [
        ["Earned (annual) leave", "1 day for every 20 days worked, after 180 days of work in a year", "Up to 30 days can be carried over; paid out on exit"],
        ["Casual leave", "Often 7 to 12 days a year", "Set by state law or company policy"],
        ["Sick leave", "Often 7 to 12 days a year", "Some states combine casual and sick leave"],
        ["Maternity leave", "26 weeks paid for the first two children; 12 weeks after that", "Also 12 weeks for adopting and commissioning mothers. See our " + IL("maternity benefit guide", "how-the-maternity-benefit-act-impacts-employers-and-employees-in-india") + "."],
        ["Paternity leave", "No legal right in the private sector", "Most employers give 5 to 15 days"],
        ["National holidays", "3 days: January 26, August 15, October 2", "Required everywhere"],
        ["Festival and state holidays", "Varies by state", "Karnataka requires at least 10 paid national and festival holidays. See our " + IL("India holiday list", "leave-policy-in-india-complete-holiday-list-of-2025-in-india") + "."],
    ], "Leave in India") + "<h3>Working hours and overtime</h3>" + T(
    ["Rule", "Standard"], [
        ["Daily and weekly limit", "8 hours a day, 48 hours a week"],
        ["Overtime", "Paid at twice the normal rate; the central rules cap it at 144 hours a quarter, and states set their own caps" + src("kpmg2","KPMG","https://kpmg.com/xx/en/our-insights/gms-flash-alert/2026/flash-alert-2026-127.html")],
        ["Rest", "At least 1 day off a week and a break after about 5 hours"],
        ["Flexible schedules", "Some states allow longer days in a shorter week, within 48 hours"],
        ["Managers", "Most overtime rules do not apply to managers and supervisors"],
    ], "Working hours in India")))

S.append(("remote", "Remote work", "<h2>Remote work in India</h2>" + P(
    "Remote work is common in India, especially in tech. Employees can work from home anywhere in the country. Paybooks registers the right state for professional tax and applies that state's leave and holiday rules.",
    "Put remote-work terms in the contract: work location, hours, equipment, any internet or home-office allowance, and data security duties. Staff in IT and ITeS units in Special Economic Zones can work hybrid under Rule 43A of the SEZ Rules, extended to December 31, 2027." + src("sez","Grant Thornton","https://www.grantthornton.in/globalassets/1.-member-firms/india/assets/pdfs/alerts/permission_for_hybrid_work_model_for_sez_employees_extended_up_to_31_december_2027.pdf"))))

S.append(("checks", "Background checks", "<h2>Background checks in India</h2>" + P(
    "Background checks are legal and common in India if the candidate gives informed consent. Under the Digital Personal Data Protection Act, 2023, tell the candidate what you will check and why, and keep only what you need.") + T(
    ["Check", "Common practice"], [
        ["Identity", "Verify PAN and ID documents. Private employers can run Aadhaar authentication only with government approval; otherwise use a masked Aadhaar or offline QR check with consent." + src("aadhaar","PIB","https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098223&reg=48&lang=2")],
        ["Education", "Verify degrees with the university or through an agency"],
        ["Work history", "Check relieving letters and confirm with past employers"],
        ["Criminal record", "Court record search or police verification through an agency"],
        ["Credit history", "Rare; mainly for finance roles, with consent"],
        ["References", "Common for senior hires"],
    ], "Background checks in India")))

S.append(("termination", "Termination and notice", "<h2>Termination, notice and severance in India</h2>" + P(
    "India protects employees from termination without cause. The rules depend on whether the person is a \"worker\" under the Industrial Relations Code. Most skilled staff in managerial or supervisory roles are not workers, so their contract and state law decide how exits work.") + T(
    ["Topic", "What applies"], [
        ["Resignation", "Employee gives contractual notice, usually 30 to 90 days; employer may agree to an early release"],
        ["Termination for misconduct", "Written charge, a fair inquiry and a written order; no notice pay if misconduct is proven"],
        ["Termination for performance or restructuring", "Contractual notice or pay instead of notice"],
        ["Layoff of workers (retrenchment)", "1 month's notice or pay, plus 15 days' average pay for each year of service"],
        ["Worker Re-skilling Fund", "An extra 15 days' wages per laid-off worker"],
        ["Government permission", "Needed for layoffs in industrial establishments with 300 or more workers"],
        ["Gratuity on exit", "15 days' last-drawn wages for each year of service, after 5 years (1 year for fixed-term). Tax-free up to ₹20 lakh. See how to handle " + IL("gratuity, bonus and final settlement", "how-to-handle-gratuity-bonus-and-ff-settlement-without-getting-it-wrong") + "."],
        ["Final pay", "Wages within 2 working days; gratuity, leave payout and bonus as part of the final settlement" + src("pib2","PIB","https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251123703501.pdf")],
        ["Relieving letter", "Expected by every employee and needed for the next job"],
    ], "Exit rules in India") + CALL(
    "<strong>Paybooks runs the exit.</strong> You make the decision. We handle the legal steps, calculate and pay the dues on time, and issue the relieving letter.")))

S.append(("ip", "Intellectual property", "<h2>Protecting intellectual property</h2>" + P(
    "Under Section 17 of the Copyright Act, 1957" + src("copy","Copyright Office","https://copyright.gov.in/Documents/CopyrightRules1957.pdf") + ", work an employee creates on the job belongs to the employer. With an EOR, the contract must make clear that rights pass to you, not to Paybooks. Our contracts assign all intellectual property created for you directly to your company, and include confidentiality duties.",
    "Contractors are different. Their work belongs to them unless there is a written assignment. An assignment that does not state its term or territory is treated as lasting 5 years and covering India only. This is one more reason to employ core staff rather than contract them.")))

S.append(("visas", "Work visas", "<h2>Work visas for foreign nationals in India</h2>" + P(
    "Foreign nationals need an employment visa to work in India, sponsored by the Indian employer. Overseas Citizens of India (OCI) can work without a visa in most roles.") + T(
    ["Visa", "Purpose", "Key conditions"], [
        ["Employment visa (E)", "Skilled work for an Indian employer", "Gross salary above ₹16.25 lakh a year in most cases; issued for up to 2 years or the contract term, extendable up to 5 years" + src("mha","MHA","https://www.mha.gov.in/PDF_Other/AnnexIII_01022018.pdf")],
        ["Business visa (B)", "Meetings, sales and short visits", "Cannot be used for employment"],
        ["Project visa", "Historically for power and steel projects", "Categories were reorganized in 2026; check the current one before applying"],
        ["Intern visa", "Internships with Indian companies", "Time-limited; stipend only"],
        ["Entry visa (X)", "Dependents of employment visa holders", "Spouse and children"],
        ["OCI card", "Overseas Citizens of India", "Can work without a visa; needs special permission for research, journalism, missionary work, mountaineering and work with foreign missions"],
    ], "Work visa options in India") + P(
    "Holders of an employment visa valid for more than 180 days must register with the Foreigners Regional Registration Office (FRRO) within 14 days of arrival. Talk to us before you make an offer to a foreign national, because sponsorship depends on the role, salary and current visa rules.")))

S.append(("providers", "Choosing an EOR", "<h2>How to choose an employer of record in India</h2>" + P(
    "Global EOR platforms cover India through their own entity or a local partner. An India-specialist EOR runs payroll in-house. Ask every provider the same questions: who is the legal employer, who files the returns, what the full cost is, and what happens if a filing is late.") + T(
    ["Provider", "Starting price per employee a month", "Billing note"], [
        ["Paybooks", "$199", "Plus $50 onboarding and $50 offboarding fees" + src("pbeor","paybooks.in","https://paybooks.in/eor/")],
        ["Skuad (Payoneer Workforce Management)", "$199", "Starting price" + src("skuad","skuad.io","https://www.skuad.io/pricing")],
        ["Multiplier", "$459", "Billed yearly" + src("mult","usemultiplier.com","https://www.usemultiplier.com/pricing")],
        ["Deel", "$599", "List price" + src("deel","deel.com","https://www.deel.com/pricing")],
        ["Remote", "$599 to $699", "$599 billed yearly, $699 billed monthly" + src("remote","remote.com","https://remote.com/pricing")],
    ], "Published list prices, September 2026") + "<p>For a wider comparison, see our list of " + IL("top EOR companies in India", "15-top-companies-for-eor-in-india-2025-paybooks") + ".</p>" + "<h3>Questions to ask any EOR in India</h3>" + UL(
    "Is the legal employer your own Indian entity, or a partner?",
    "Is the price a flat fee per employee, or a percentage of salary?",
    "What deposit do you need, and when is it returned?",
    "What exchange-rate margin do you add to the invoice?",
    "Are health insurance, background checks and offboarding included?",
    "Will you pay penalties caused by your own mistakes, in writing?")))

S.append(("pricing", "Paybooks pricing", "<h2>Paybooks EOR India pricing</h2>" + P(
    "Paybooks charges from $199 per employee a month for employer of record services in India, with no entity setup cost. Salary and statutory contributions are passed through at cost. The table shows what is included and what costs extra.") + T(
    ["Item", "Included in $199", "Extra cost"], [
        ["Monthly payroll, payslips, tax withholding and filings", "Yes", "None"],
        ["PF, ESI, professional tax and welfare fund registration and filing", "Yes", "Contributions passed through at cost"],
        ["Employment contract and appointment letter", "Yes", "None"],
        ["\"No penalties ever\" promise", "Yes", "None"],
        ["Onboarding a new hire", "No", "One-time fee from $50 per hire"],
        ["Offboarding and final settlement", "No", "One-time fee from $50 per exit, plus statutory dues"],
        ["Security deposit", "No", "Refundable; equal to each employee's notice-period pay"],
        ["Group health insurance", "No", "Optional; premium depends on the plan"],
        ["Visa sponsorship and entity transfer", "No", "Quoted per case"],
    ], "What the Paybooks EOR fee covers" + src("pbeor","paybooks.in","https://paybooks.in/eor/"))))

S.append(("transfer", "Moving to your own entity", "<h2>Moving from an EOR to your own entity</h2>" + P(
    "Many clients start with Paybooks and open an Indian company once the team grows. When that happens, employees move to your entity with service counted from their original start date, so gratuity and leave balances carry over.",
    "Provident Fund moves with the employee through their Universal Account Number. Paybooks issues the relieving and transfer documents, and can keep running payroll for your new entity, so employees see no change on payday.")))

FAQ = [
    ("What is an employer of record in India?", "An employer of record (EOR) in India is a local company that legally employs staff on behalf of another business. It handles the contract, payroll, tax withholding, Provident Fund, ESI and all filings, while the client manages the employee's daily work."),
    ("Is it legal to use an EOR in India?", "Yes. Paybooks is an Indian company that employs your staff under Indian law and provides their services to you. Employees get a full Indian employment contract with all statutory benefits."),
    ("How much does an employer of record cost in India?", "Paybooks charges from $199 per employee a month, plus one-time onboarding and offboarding fees from $50. On top of salary, employer contributions add about 8 to 9% for skilled staff, and more for staff earning ₹21,000 a month or less."),
    ("Can a foreign company hire employees in India without an entity?", "Yes, through an employer of record. The EOR is the legal employer, so you do not need to register a company, branch or liaison office in India."),
    ("What is the difference between an EOR and a PEO in India?", "India has no co-employment model. A PEO needs you to have your own Indian entity. An EOR employs staff for you when you do not."),
    ("Should I use an EOR or set up a company in India?", "Use an EOR for first hires and teams of up to about 20 to 25 people, or while you test the market. Consider your own company when the team is larger or you sell to Indian customers."),
    ("Are there hidden fees with an EOR in India?", "Ask about deposits, exchange-rate margins, insurance, background checks and exit fees. Paybooks publishes its onboarding and offboarding fees and deposit rule, and its \u201cno penalties ever\u201d promise is part of the service."),
    ("How long does it take to hire through an EOR in India?", "With Paybooks, within days of an accepted offer, depending on the candidate's notice period and background checks. Setting up your own entity takes weeks to months."),
    ("Can I move employees from the EOR to my own Indian entity later?", "Yes. Paybooks transfers employees with their service history intact, so gratuity and leave carry over. Provident Fund moves through the employee's Universal Account Number."),
    ("How did India's 2025 labor codes change employment costs?", "Basic pay must now be at least 50% of total pay, which raises Provident Fund and gratuity for some pay structures. Fixed-term staff now earn gratuity after one year."),
    ("Can I hire contractors in India instead of employees?", "Yes, for genuinely independent, project-based work. Long-term, full-time contractors who work under your direction risk being treated as employees, with back payments of Provident Fund and other dues."),
    ("How do I choose the best employer of record in India?", "Compare four things: whether the provider is the legal employer through its own Indian entity, the full monthly cost including deposits and exchange-rate margins, who files the statutory returns, and whether it will pay penalties caused by its own mistakes in writing."),
]
S.append(("faq", "FAQ", '<h2>Employer of record India: frequently asked questions</h2><div class="g-faq">' + "".join(
    "<details><summary>" + q + "</summary><div><p>" + a + "</p></div></details>" for q, a in FAQ) + "</div>"))

_w = WRITER[0] if WRITER else TEAM
AUTHOR = ('<div class="g-author"><div class="g-av">PB</div><div><b>Written by ' + _w + '</b>'
          '<p>Paybooks has run payroll and compliance for Indian employers since 2012. Published ' + PUBLISHED + ', last updated ' + UPDATED + '. This guide is general information, not legal or tax advice.</p></div></div>')
RELATED = ('<h2 style="font-size:24px">Keep reading</h2><div class="g-rel">'
           '<a href="../../">Employer of Record India<small>Hire in India within days</small></a>'
           '<a href="#cost">EOR cost in India<small>Worked examples in INR and USD</small></a>'
           '<a href="#peo">EOR vs PEO in India<small>Which one you need</small></a></div>')

QUOTE = ('<section id="quote"><div class="g-final"><span class="g-tag">Ready to hire in India?</span><h2>Get your EOR India quote</h2>'
         '<p>Tell us the role, city and pay. You get the full monthly cost in dollars, the contract terms and a start date.</p>'
         '<div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" href="#quote">Talk to an EOR expert</a></div></div></section>')

# ---------------- page ----------------
toc = "".join('<li><a href="#' + i + '">' + lbl + "</a></li>" for i, lbl, _ in S)
SOURCES = '<section id="sources" class="g-sources"><h2>Sources</h2><ol>' + ''.join('<li>' + l + ': <a href="' + H.escape(u) + '" rel="nofollow noopener" target="_blank">' + H.escape(u) + '</a></li>' for l, u in dict.fromkeys(SRC.values())) + '</ol></section>'
body = LEAD + KT + "".join('<section id="' + i + '"><span class="g-num">' + format(k + 1, '02d') + '</span>' + h + "</section>" for k, (i, _l, h) in enumerate(S)) + SOURCES + QUOTE + AUTHOR + RELATED

def text_of(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)
    return H.unescape(re.sub(r"<[^>]+>", " ", h))

TITLE = "Employer of Record India: EOR Costs, Laws and Hiring (2026)"
DESC = ("Hire in India without an entity. See employer of record India costs in INR and USD, labor code rules, "
        "taxes, leave and exits. Paybooks EOR from $199 a month.")
H1 = "Employer of Record India: 2026 Guide"

schema = [
    {"@context": "https://schema.org", "@type": "Article", "headline": H1,
     "description": DESC, "dateModified": "2026-09-24", "author": ({"@type": "Person", "name": WRITER[0], "jobTitle": WRITER[1]} if WRITER else {"@type": "Organization", "name": TEAM}), "datePublished": "2026-09-24",
     "publisher": {"@type": "Organization", "name": "Paybooks, a TransPerfect company", "url": "https://www.paybooks.in/"},
     "about": {"@type": "Thing", "name": "Employer of record in India"}, "mainEntityOfPage": CANON},
    {"@context": "https://schema.org", "@type": "Service", "name": "Employer of Record India", "serviceType": "Employer of record",
     "provider": {"@type": "Organization", "name": "Paybooks, a TransPerfect company", "url": "https://www.paybooks.in/"},
     "areaServed": {"@type": "Country", "name": "India"},
     "offers": {"@type": "Offer", "price": "199", "priceCurrency": "USD", "description": "From, per employee per month"}},
    {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.paybooks.in/"},
        {"@type": "ListItem", "position": 2, "name": "Employer of Record", "item": "https://www.paybooks.in/employer-of-record/"},
        {"@type": "ListItem", "position": 3, "name": "India", "item": CANON}]},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]
ld = "".join('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + "</script>" for s in schema)

HEAD = ('<!DOCTYPE html><html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>' + TITLE + '</title><meta name="description" content="' + DESC + '">'
        '<link rel="canonical" href="' + CANON + '"><meta name="robots" content="noindex,nofollow">'
        '<meta property="og:title" content="' + TITLE + '"><meta property="og:description" content="' + DESC + '"><meta property="og:type" content="article"><meta property="og:url" content="' + CANON + '">'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="../../assets/pb.css"><link rel="stylesheet" href="../../assets/guide.css">' + ld + "</head><body>")

HEADER = ('<header class="hdr"><div class="wrap"><a class="brand" href="../../"><img src="../../assets/mark.png" alt="Paybooks" width="44" height="44"><span class="wm"><b>paybooks</b><small>A TransPerfect company</small></span></a>'
          '<nav class="nav"><a href="../../">Employer of Record</a><a>Payroll</a><a>India Office</a><a>HCM</a><a>Resources</a></nav>'
          '<div class="btns"><a class="btn ghost" href="#quote">Book a call</a><a class="btn" href="#quote">Get a quote</a></div></div></header>')

words_est = len(text_of(body).split())
ILLU = ('<figure class="g-illu" role="img" aria-label="How an employer of record works: your company manages the work and pays one invoice; Paybooks employs your staff in India, pays salary in rupees and files with the government.">'
 '<svg viewBox="0 0 420 470" xmlns="http://www.w3.org/2000/svg">'
 '<defs><marker id="ga" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#C5F04A"/></marker>'
 '<linearGradient id="gpb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF6E3"/></linearGradient></defs>'
 # connectors
 '<path class="g-flow" d="M150 66 H268" stroke="#C5F04A" stroke-width="2" fill="none" marker-end="url(#ga)"/>'
 '<path class="g-flow" d="M75 112 C75 170 120 200 150 228" stroke="#C5F04A" stroke-width="2" fill="none" marker-end="url(#ga)"/>'
 '<path class="g-flow" d="M270 228 C300 200 345 170 345 114" stroke="#C5F04A" stroke-width="2" fill="none" marker-end="url(#ga)"/>'
 '<path class="g-flow" d="M210 360 V396" stroke="#C5F04A" stroke-width="2" fill="none" marker-end="url(#ga)"/>'
 # connector labels
 '<text x="210" y="56" text-anchor="middle" class="g-il">Manages work</text>'
 '<text x="6" y="178" class="g-il">One invoice</text><text x="6" y="194" class="g-il g-il2">in dollars</text>'
 '<text x="414" y="178" text-anchor="end" class="g-il">Salary</text><text x="414" y="194" text-anchor="end" class="g-il g-il2">in rupees</text>'
 '<text x="222" y="383" class="g-il">Files and pays</text>'
 # company card
 '<rect x="0" y="20" width="150" height="92" rx="18" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.16)"/>'
 '<circle cx="32" cy="52" r="16" fill="#C5F04A"/><path d="M25 60V46l7-4 7 4v14M29 60v-5h6v5M28 49h2M34 49h2" stroke="#0F2E1A" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
 '<text x="16" y="88" class="g-nt">Your company</text><text x="16" y="104" class="g-ns">Outside India</text>'
 # employee card
 '<rect x="270" y="20" width="150" height="92" rx="18" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.16)"/>'
 '<circle cx="302" cy="52" r="16" fill="#C5F04A"/><circle cx="302" cy="47" r="4.5" fill="none" stroke="#0F2E1A" stroke-width="1.8"/><path d="M294 60c1.5-4.5 4.5-6.5 8-6.5s6.5 2 8 6.5" stroke="#0F2E1A" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
 '<text x="286" y="88" class="g-nt">Your employee</text><text x="286" y="104" class="g-ns">Works in India</text>'
 # paybooks card
 '<rect x="70" y="230" width="280" height="130" rx="22" fill="url(#gpb)"/>'
 '<circle cx="104" cy="264" r="18" fill="#0F2E1A"/><text x="104" y="269" text-anchor="middle" class="g-pb">PB</text>'
 '<text x="132" y="260" class="g-nt2">Paybooks</text><text x="132" y="277" class="g-ns2">Legal employer in India</text>'
 '<rect x="90" y="298" width="112" height="24" rx="12" fill="#DDEFC6"/><text x="146" y="314" text-anchor="middle" class="g-chip">Contract</text>'
 '<rect x="210" y="298" width="120" height="24" rx="12" fill="#DDEFC6"/><text x="270" y="314" text-anchor="middle" class="g-chip">Payroll in ₹</text>'
 '<rect x="90" y="328" width="112" height="24" rx="12" fill="#DDEFC6"/><text x="146" y="344" text-anchor="middle" class="g-chip">Tax, PF, ESI</text>'
 '<rect x="210" y="328" width="120" height="24" rx="12" fill="#DDEFC6"/><text x="270" y="344" text-anchor="middle" class="g-chip">Filings</text>'
 # government card
 '<rect x="120" y="400" width="180" height="62" rx="16" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.16)"/>'
 '<path d="M142 418l12-6 12 6M144 420v14M150 420v14M158 420v14M164 420v14M141 436h26" stroke="#C5F04A" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
 '<text x="178" y="426" class="g-nt">Government</text><text x="178" y="443" class="g-ns">PF · ESI · Income tax</text>'
 '</svg></figure>')
HERO = ('<div class="g-progress" id="gprog"></div><section class="g-hero"><div class="g-hero-in"><div>'
        '<nav class="g-crumbs" aria-label="Breadcrumb"><a href="../../">Home</a><span>/</span><a href="../../">Employer of Record</a><span>/</span>India</nav>'
        '<h1>Employer of Record India: <em>2026 Guide</em></h1>'
        '<p class="g-sub">Hire in India without an entity. What it costs, which laws apply, and what an EOR handles for you.</p>' +
        '<div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" href="#cost">See EOR costs in India</a></div>'
        '</div>' + ILLU + '</div>'
        '<div class="g-bystrip"><div class="g-bystrip-in">' + BYLINE(round(words_est / 230)) + '</div></div></section>')

MTOC = '<details class="g-mtoc"><summary>On this page</summary><ol>' + toc + "</ol></details>"
TOC = ('<aside class="g-toc" aria-label="Contents"><h2>On this page</h2><ol>' + toc + '</ol>'
       '<div class="g-toc-cta"><b>What will your India hire cost?</b><p>Salary, PF, ESI, gratuity and fees in dollars, for any role and city.</p><a class="btn" href="../../#cost">Open the cost calculator</a></div></aside>')

FOOTER = ('<footer class="ftr"><div class="wrap" style="grid-template-columns:1fr"><div><h4>Paybooks, a TransPerfect company</h4>'
          '<p>Employer of Record, Multi-Country Payroll, Managed India Office, and Global HCM for companies building teams in India and beyond.</p></div></div></footer>')

SPY = ('<script>(function(){var pb=document.getElementById("gprog");function pr(){var h=document.documentElement;var m=h.scrollHeight-h.clientHeight;pb.style.width=(m>0?h.scrollTop/m*100:0)+"%"}window.addEventListener("scroll",pr,{passive:true});pr();})();(function(){var l=[].slice.call(document.querySelectorAll(".g-toc a"));var m={};l.forEach(function(a){m[a.getAttribute("href").slice(1)]=a});'
       'if(!("IntersectionObserver" in window))return;var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){l.forEach(function(a){a.classList.remove("on")});'
       'var a=m[e.target.id];if(a){a.classList.add("on");var ol=a.closest("ol");if(ol){var t=a.offsetTop-ol.offsetTop;if(t<ol.scrollTop||t>ol.scrollTop+ol.clientHeight-a.offsetHeight)ol.scrollTop=t-ol.clientHeight/2+a.offsetHeight/2}}}})},{rootMargin:"-10% 0px -80% 0px"});'
       'document.querySelectorAll(".g-body section[id]").forEach(function(s){o.observe(s)})})();</script>')

page = HEAD + HEADER + HERO + '<div class="g-layout">' + TOC + '<main class="g-body">' + MTOC + body + "</main></div>" + FOOTER + SPY + "</body></html>"
open(OUT, "w").write(page)
print("words", words_est, "tables", page.count("<table"), "sources", len(SRC), "internal links", page.count('href="https://paybooks.in/article/'))
