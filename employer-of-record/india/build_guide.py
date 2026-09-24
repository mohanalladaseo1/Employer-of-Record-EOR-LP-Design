# Builds /employer-of-record/india/index.html : Employer of Record India guide (sample content).
# v2: keyword-targeted, plain US English, no visible review tags (they are listed in verify-list.md instead).
# Python 3.9 safe: no backslashes inside f-string expressions.
import json, os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "index.html")
FX = 88.0  # INR per USD, illustrative
CANON = "https://www.paybooks.in/employer-of-record/india/"
UPDATED = "September 24, 2026"

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
            cells.append('<td class="n">' + c + "</td>" if i in num else "<td>" + c + "</td>")
        out.append('<tr class="tot">' if tot else "<tr>")
        out.append("".join(cells) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)

def P(*ps): return "".join("<p>" + p + "</p>" for p in ps)
def UL(*xs): return "<ul>" + "".join("<li>" + x + "</li>" for x in xs) + "</ul>"
def CALL(t): return '<div class="g-call"><p>' + t + "</p></div>"
def CTA(title, sub, btn="Get a quote for a role"):
    return '<div class="g-cta"><div><b>' + title + "</b><p>" + sub + '</p></div><a class="btn" href="#quote">' + btn + "</a></div>"

# ---------------- worked cost examples ----------------
def cost_example(gross_m, lwf_emp_y, ins_y):
    basic = gross_m * 0.5
    lines = [("Gross salary", gross_m * 12, "Agreed yearly pay. Basic pay set at 50% to meet the labor code wage rule.")]
    lines.append(("Employer Provident Fund, 12%", basic * 0.12 * 12, "12% of basic pay. The legal minimum is on pay up to ₹15,000 a month; most employers pay on full basic."))
    lines.append(("PF admin and EDLI insurance", min(basic, 15000) * 0.01 * 12, "About 0.5% admin plus 0.5% insurance, on pay up to ₹15,000 a month."))
    esi = gross_m * 0.0325 * 12 if gross_m <= 21000 else 0
    lines.append(("Employer ESI, 3.25%", esi, "Only for staff earning ₹21,000 a month or less." if esi else "Not due. Pay is above ₹21,000 a month."))
    bonus = min(basic, 7000) * 0.0833 * 12 if gross_m <= 21000 else 0
    lines.append(("Statutory bonus, 8.33% minimum", bonus, "Only for staff earning ₹21,000 a month or less, on capped pay." if bonus else "Not due. Pay is above the ₹21,000 limit."))
    lines.append(("Gratuity provision, 4.81%", basic * 0.0481 * 12, "Set aside monthly. Paid on exit after 5 years, or 1 year for fixed-term staff."))
    lines.append(("Labor Welfare Fund", lwf_emp_y, "Small state levy. Karnataka shown." + V("Karnataka Labor Welfare Fund employer amount (₹50 a year used)")))
    lines.append(("Group health insurance", ins_y, "Market practice, not required by law for most staff. Charged at cost." + V("Group health insurance premium estimates (₹18,000 and ₹9,000 a year)")))
    return lines

EX1 = cost_example(200000, 50, 18000)
EX2 = cost_example(20000, 50, 9000)
FEE_Y = 199 * 12 * FX

def cost_table(lines, cap):
    rows, tot = [], 0
    for name, amt, note in lines:
        tot += amt
        rows.append([name, inr(amt) if amt else "₹0", usd(amt) if amt else "$0", note])
    rows.append(["Paybooks EOR fee", inr(FEE_Y), "$2,388", "$199 per employee a month, billed in USD."])
    tot += FEE_Y
    rows.append(["!Total yearly cost", inr(tot), usd(tot), ""])
    return T(["Cost line", "Per year (INR)", "Per year (USD)", "What it is"], rows, cap, num=(1, 2)), tot

EX1_T, EX1_TOT = cost_table(EX1, "Example 1: senior software engineer in Bengaluru, ₹24 lakh (₹2.4 million) a year")
EX2_T, EX2_TOT = cost_table(EX2, "Example 2: customer support associate in Bengaluru, ₹2.4 lakh (₹240,000) a year")
EX1_ON = (EX1_TOT - 2400000 - FEE_Y) / 2400000 * 100
EX2_ON = (EX2_TOT - 240000 - FEE_Y) / 240000 * 100
V("Exchange rate of ₹88 to $1 used in all dollar figures")

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

LEAD = ('<div class="g-kt" style="background:#fff;border:1px solid var(--line)"><h2 style="color:var(--ink)">Quick answer</h2>'
        '<p style="color:var(--ink-2)">An <strong style="color:var(--ink)">employer of record in India</strong> is an Indian company that legally employs your staff for you. '
        'It issues the employment contract, pays salary in rupees, withholds income tax, pays Provident Fund and ESI, and files every return. '
        'You choose the person and manage their work. With an EOR, a company outside India can hire in India in about 10 working days, without opening an Indian entity.</p>'
        '<p style="color:var(--ink-2);margin-top:10px"><strong style="color:var(--ink)">Cost:</strong> salary, plus about 9 to 10% in employer contributions for skilled staff, plus the EOR fee. '
        'Paybooks charges $199 per employee a month.</p></div>')

KT = ('<div class="g-kt"><h2>Key takeaways</h2><ul>'
      '<li><strong>You do not need an Indian company to hire in India.</strong> An EOR is the legal employer and handles payroll, tax and filings.</li>'
      '<li><strong>Budget salary plus 9 to 10%, plus $199 a month</strong> for a skilled employee. Staff earning ₹21,000 a month or less cost a little more.</li>'
      '<li><strong>India\'s new labor codes took effect on November 21, 2025.</strong> Basic pay must be at least half of total pay, and fixed-term staff earn gratuity after one year.</li>'
      '<li><strong>Long-term contractors are risky.</strong> Courts judge how people actually work, not what the contract calls them.</li>'
      '<li><strong>Start in about 10 working days.</strong> Move staff to your own entity later, with their service history intact.</li></ul></div>')

S.append(("glance", "India at a glance", "<h2>India employment facts at a glance</h2>" + P(
    "India has a large skilled workforce and detailed employment rules. Rules come from both the national government and each state. The table covers what employers ask about first.") + T(
    ["Item", "India"], [
        ["Currency", "Indian rupee (INR, ₹). Salary must be paid in rupees to an Indian bank account."],
        ["Tax year", "April 1 to March 31. The new Income-tax Act, 2025 applies from April 1, 2026."],
        ["Pay frequency", "Monthly. Salary is due by the 7th of the next month."],
        ["Working time", "8 hours a day, 48 hours a week. Overtime is paid at twice the normal rate."],
        ["Employer social security", "Provident Fund at 12% of basic pay, ESI at 3.25% for lower earners, gratuity on exit."],
        ["Income tax", "0% to 30%, plus 4% cess, under the default new regime. The employer withholds it monthly."],
        ["Paid leave", "Set by state law. Usually 12 to 21 days of earned leave a year." + V("Earned leave range of 12 to 21 days by state")],
        ["Public holidays", "3 national holidays plus state and festival holidays, usually 10 to 15 days in total."],
        ["Probation", "Not set by law. 3 to 6 months is common."],
        ["Notice period", "Set by the contract. 30 to 90 days is common for skilled roles."],
        ["Main laws", "Code on Wages 2019, Industrial Relations Code 2020, Code on Social Security 2020, Occupational Safety, Health and Working Conditions Code 2020."],
        ["Time to hire with Paybooks", "Contract ready in about 2 working days. Employee starts in about 10 working days."],
    ], "India employment facts")))

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
        ["Who carries compliance risk?", "Paybooks, backed by a written no-penalty guarantee", "Your company, with provider support"],
        ["Best fit", "First hires, testing the market, teams under about 20 to 25 people", "Established teams with their own entity"],
    ], "EOR vs PEO in India")))

S.append(("entity", "EOR vs own entity", "<h2>EOR vs setting up your own entity in India</h2>" + P(
    "Most foreign companies that stay in India open a private limited company at some point. The question is when. An entity gives you full control and can cost less at scale. But it takes weeks to set up and has fixed costs from day one: a resident director, an office address, an auditor, yearly filings and transfer pricing.",
    "An EOR lets you hire now and decide on an entity once the team is proven. Paybooks can later move your employees to your entity with their service history intact.") + T(
    ["Question", "Employer of record", "Own private limited company"], [
        ["Time to first hire", "About 10 working days", "Usually 6 to 12 weeks, including bank and tax registrations" + V("Entity setup time of 6 to 12 weeks")],
        ["Upfront cost", "None beyond any deposit", "Incorporation, legal and registration costs"],
        ["Fixed yearly cost", "None. You pay per employee.", "Audit, company secretary, filings, office and accounting"],
        ["Resident director", "Not needed", "Required. At least one director must have spent 182 days or more in India in the prior year."],
        ["Tax exposure for the parent", "Lower, since staff work for an Indian company. Some activities can still create a taxable presence.", "Profits taxed in India; transfer pricing applies"],
        ["Can sign local contracts and bill Indian customers", "No. The EOR only employs.", "Yes"],
        ["Exit", "Give notice; Paybooks handles final pay", "Closing a company can take a year or more" + V("Company closure can take a year or more")],
        ["Best fit", "Up to about 25 employees, or while you test India", "Large, long-term teams, or selling to Indian customers"],
    ], "EOR vs own entity in India") + CALL(
    "<strong>Rule of thumb.</strong> Below about 20 to 25 employees, an EOR usually costs less than your own entity once audit, compliance staff and management time are counted. Above that, compare the full cost of both. We include that comparison with every quote.")))

S.append(("contractor", "Contractors vs employees", "<h2>Can you hire contractors in India instead?</h2>" + P(
    "Yes, for genuine project work. But Indian courts look at how the person actually works, not what the contract says. A long-term, full-time contractor who works only for you, under your direction, is likely to count as an employee.",
    "If that happens, you can owe back Provident Fund with interest and damages, unpaid gratuity and leave, and you may face questions about a taxable presence in India. Contractors also get no statutory benefits, which makes good people harder to hire and keep.") + T(
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
        ["Control test", "Does the company control what the worker does and how? Set out in Dharangadhara Chemical Works v State of Saurashtra (1957)."],
        ["Integration test", "Is the worker part of the business, for example on the team, in the org chart, using company email?"],
        ["Economic reality test", "Does the worker depend on this one company for a living, and who carries the business risk?"],
        ["Multiple factor test", "Who hires, pays and can fire the worker, and who supplies the tools?"],
    ], "Employment status tests") + CALL(
    "<strong>Switching contractors to employees is simple.</strong> Paybooks can move your Indian contractors onto employment contracts, usually within one payroll cycle.")))

S.append(("routes", "How to hire in India", "<h2>How to hire employees in India</h2>" + P(
    "A foreign company has three ways to hire employees in India. The right one depends on team size, speed and how long you plan to stay.") + T(
    ["Route", "How it works", "Speed", "Best for"], [
        ["Own subsidiary", "Set up a private limited company, register for tax, PF and ESI, then hire directly", "Slowest, often 2 to 3 months", "Large, long-term teams"],
        ["Employer of record", "Paybooks employs the person for you under Indian law", "About 10 working days", "First hires, small and growing teams"],
        ["Contractors", "Engage self-employed professionals for set projects", "Fast", "Genuinely short, project-based work"],
    ], "Ways to hire in India") +
    "<h3>Hiring through Paybooks, step by step</h3><ol>" +
    "<li><strong>Share the role, city and pay.</strong> We send the full monthly cost in dollars within two working days.</li>" +
    "<li><strong>Make the offer.</strong> We draft an offer letter that names your company, the manager and the role.</li>" +
    "<li><strong>Onboard.</strong> The employee uploads documents online. We run the background checks you choose and register them for PF and ESI.</li>" +
    "<li><strong>Sign.</strong> Paybooks issues the appointment letter and employment contract.</li>" +
    "<li><strong>First payroll.</strong> The employee is paid by the 7th of the next month, with a payslip and tax withheld.</li></ol>" +
    CTA("See what your first India hire will cost", "Send the role, city and salary. Get the full monthly cost in dollars within two working days.")))

S.append(("onboarding", "Documents and contracts", "<h2>Onboarding documents and employment contracts</h2>" + P(
    "India's labor codes require a written appointment letter for every employee. Paybooks issues it with a full employment contract, both in English.") + T(
    ["Document", "Indian citizens", "Foreign nationals"], [
        ["Tax ID", "PAN card (Permanent Account Number)", "PAN, applied for on arrival if needed"],
        ["Identity and address", "Aadhaar card, passport or voter ID", "Passport"],
        ["Right to work", "Not needed", "Employment visa and FRRO registration where required"],
        ["Provident Fund", "Universal Account Number (UAN) if employed before", "Covered as an international worker" + V("PF coverage rules for international workers")],
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
    "Non-solicitation. Non-compete clauses after employment are generally unenforceable in India under Section 27 of the Indian Contract Act.") +
    "<h3>Contract types</h3>" + T(
    ["Type", "Use", "Key rule"], [
        ["Permanent", "Most roles", "Runs until resignation or termination"],
        ["Fixed-term", "Projects or time-bound roles", "Same pay and benefits as permanent staff. Gratuity after 1 year."],
        ["Part-time", "Reduced hours", "Pay and leave in proportion to hours; social security still applies" + V("Part-time social security treatment")],
        ["Internship", "Students and recent graduates", "Paid a stipend; not treated as employment under most laws" + V("Internship treatment under employment laws")],
    ], "Employment contract types")))

S.append(("cost", "EOR cost in India", "<h2>How much does an employer of record in India cost?</h2>" + P(
    "The total cost has three parts: gross salary, employer contributions and the EOR fee. For skilled staff, employer contributions add about 9 to 10% to salary. For staff earning ₹21,000 a month or less, ESI and statutory bonus push that to about 15 to 20%.",
    "Here are two worked examples at ₹" + str(int(FX)) + " to $1. Your quote uses the live exchange rate.") +
    EX1_T + CALL("<strong>Example 1 in one line.</strong> A ₹24 lakh salary (about " + usd(2400000) + ") costs about " + usd(EX1_TOT) + " a year in total. Employer costs beyond salary and the fee add about " + format(EX1_ON, ".1f") + "%.") +
    EX2_T + CALL("<strong>Example 2 in one line.</strong> At lower pay, ESI and statutory bonus apply, so employer costs add about " + format(EX2_ON, ".1f") + "% before the fee. The flat $199 fee is a bigger share of a small salary, so we quote every role separately.") +
    "<h3>Employer contributions in India</h3>" + T(
    ["Contribution", "Employer pays", "Employee pays", "Who it covers"], [
        ["Provident Fund (EPF and EPS)", "12% of basic pay", "12% of basic pay", "All employees; required on pay up to ₹15,000 a month"],
        ["PF admin and EDLI", "About 1% combined", "None", "On PF pay up to ₹15,000 a month"],
        ["Employees' State Insurance (ESI)", "3.25% of gross", "0.75% of gross", "Staff earning ₹21,000 a month or less"],
        ["Statutory bonus", "8.33% to 20% of capped pay", "None", "Staff earning ₹21,000 a month or less"],
        ["Gratuity", "About 4.81% of basic, paid on exit", "None", "After 5 years, or 1 year for fixed-term staff"],
        ["Professional tax", "None (employer withholds and pays)", "Up to ₹2,500 a year", "Most states, including Karnataka and Maharashtra"],
        ["Labor Welfare Fund", "Small fixed amount", "Small fixed amount", "States that charge it"],
    ], "Statutory contributions in India") +
    CTA("Get the full cost for your role", "Every line above, for your city and salary, in dollars. No commitment.")))

S.append(("salary", "Salary structure", "<h2>How salaries are structured in India</h2>" + P(
    "Indian salaries are quoted as a yearly cost-to-company (CTC) figure, split into parts. The split matters because it sets Provident Fund, gratuity and the employee's income tax.",
    "Under the labor codes, basic pay plus dearness allowance must be at least 50% of total pay. If allowances go above 50%, the extra counts as wages for PF and gratuity. Most employers now set basic pay at 50%.") + T(
    ["Part", "Typical share", "Notes"], [
        ["Basic salary", "50% of gross", "Sets PF and gratuity. Must meet the 50% wage rule."],
        ["House rent allowance (HRA)", "Up to 50% of basic in metro cities", "Tax-free only under the old tax regime"],
        ["Special allowance", "The balance", "Fully taxable; flexible"],
        ["Employer NPS contribution", "Up to 14% of basic", "Tax-deductible for the employee, even under the new regime"],
        ["Meal, fuel or phone allowances", "Small, fixed", "Tax treatment depends on regime and limits"],
        ["Variable pay or bonus", "Often 10 to 20% of CTC for senior roles", "Paid through payroll with tax withheld"],
    ], "Typical salary structure in India") + P(
    "Each state sets minimum wages by skill level and zone, and the Code on Wages adds a national floor wage. Professional salaries are far above these floors. Support and operations roles should be checked against the state table.")))

S.append(("tax", "Income tax", "<h2>Income tax and payroll taxes in India</h2>" + P(
    "The employer withholds income tax (TDS) from salary every month and deposits it with the government. Employees choose the default new regime, with lower rates and few deductions, or the old regime, with higher rates and exemptions such as HRA and Section 80C investments.") + T(
    ["Taxable income (new regime)", "Rate"], [
        ["Up to ₹4,00,000", "0%"], ["₹4,00,001 to ₹8,00,000", "5%"], ["₹8,00,001 to ₹12,00,000", "10%"],
        ["₹12,00,001 to ₹16,00,000", "15%"], ["₹16,00,001 to ₹20,00,000", "20%"], ["₹20,00,001 to ₹24,00,000", "25%"],
        ["Above ₹24,00,000", "30%"],
    ], "New regime tax rates" + V("2025-26 tax slabs carrying into 2026-27 under the Income-tax Act, 2025"), num=(1,)) + UL(
    "Salaried employees get a ₹75,000 standard deduction under the new regime.",
    "A Section 87A rebate means no tax on taxable income up to ₹12,00,000 under the new regime.",
    "A 4% health and education cess is added to the tax. A surcharge applies above ₹50 lakh.") + T(
    ["Step", "Amount"], [
        ["Gross salary", inr(2400000)], ["Less standard deduction", inr(-75000)], ["Taxable income", inr(TI)],
        ["Income tax on the slabs", inr(TX)], ["Health and education cess, 4%", inr(CESS)],
        ["!Total yearly tax", inr(TX + CESS)], ["Withheld each month", inr((TX + CESS) / 12)],
    ], "Worked example: employee tax on ₹24 lakh, new regime", num=(1,)) + P(
    "India has no separate employer payroll tax beyond the contributions above. GST may apply to the EOR fee; for clients outside India the service is usually treated as an export." + V("GST treatment of the EOR fee as an export of services"))))

S.append(("codes", "India's labor codes", "<h2>India's new labor codes: what changed in November 2025</h2>" + P(
    "On November 21, 2025, four labor codes (called the Labour Codes in Indian law) replaced 29 older national labor laws. States are still issuing their own rules, so some details differ by state." + V("Status of state rules under the labor codes")) + T(
    ["Change", "What it means for employers"], [
        ["One definition of wages", "Allowances above 50% of pay count as wages. This raises PF and gratuity where basic pay was low."],
        ["Appointment letters", "Every employee must get a written appointment letter."],
        ["Gratuity for fixed-term staff", "Due after 1 year of service instead of 5."],
        ["National floor wage", "No state minimum wage can fall below it."],
        ["Faster final pay", "Final dues are due within 2 working days of the last day."],
        ["Leave eligibility", "Annual leave starts after 180 days worked, down from 240."],
        ["Worker Re-skilling Fund", "Employers pay 15 days' wages into a fund for each laid-off worker."],
        ["Higher thresholds", "Standing orders and layoff permission now apply at 300 workers, up from 100."],
        ["Gig and platform workers", "Platforms pay into a welfare fund. Relevant if you hire through platforms."],
        ["Women at night", "Women may work night shifts with consent and safety measures."],
    ], "Key changes under India's labor codes") + CALL(
    "<strong>What Paybooks did.</strong> We moved every client's pay structure to the new wage definition before the first payroll under the codes, and reissued appointment letters where needed. Employees did not have to do anything.")))

S.append(("compliance", "Compliance checklist", "<h2>Employer compliance checklist for India</h2>" + P(
    "An employer in India holds several registrations and files returns every month, quarter and year. With an EOR, Paybooks holds and files all of them.") + T(
    ["Requirement", "What the employer must do", "How often"], [
        ["Shops and Establishments registration", "Register each office under state law and keep registers", "Once, renewed as required"],
        ["Provident Fund", "Register, pay contributions and file the online challan", "Monthly, by the 15th"],
        ["ESI", "Register eligible staff and pay contributions", "Monthly, by the 15th"],
        ["Income tax (TDS)", "Withhold and deposit tax; file Form 24Q", "Monthly by the 7th; quarterly returns"],
        ["Form 16", "Issue the yearly tax certificate to each employee", "Yearly, by June 15"],
        ["Professional tax", "Withhold and pay under state law", "Monthly in most states"],
        ["Labor Welfare Fund", "Pay employer and employee shares", "Twice a year or yearly, by state"],
        ["Minimum wage and on-time pay", "Pay at least the minimum wage, by the 7th", "Monthly"],
        ["Maternity benefit", "26 weeks' paid leave; a creche at 50 or more employees", "As needed"],
        ["Anti-harassment (POSH)", "Written policy and an Internal Committee at 10 or more employees; yearly report", "Ongoing and yearly"],
        ["Data protection", "Handle employee data under the Digital Personal Data Protection Act, 2023", "Ongoing" + V("DPDP Act obligations and timing for employee data")],
    ], "Employer compliance checklist for India") +
    "<h3>What happens if you get it wrong</h3>" + P(
    "Late Provident Fund payments carry 12% yearly interest plus damages that grow with the delay. Missed tax deposits bring interest and penalties, and can affect the employee's tax credit. Labor inspectors can fine employers under the codes, with higher fines for repeat offenses.",
    "Paybooks backs every filing with a written no-penalty guarantee. If a penalty comes from our mistake, we pay it.") +
    CTA("Read the no-penalty guarantee", "We share the wording with your quote, along with a sample service agreement.", "Get the guarantee")))

S.append(("payroll", "Payroll calendar", "<h2>How payroll works in India</h2>" + P(
    "Payroll in India is monthly. Paybooks collects changes such as new joiners, leave and bonuses, calculates pay and deductions, pays staff by the 7th of the next month and makes every government payment on time. Employees get an online payslip and submit tax declarations in the Paybooks app.") + T(
    ["Deadline", "What is due"], [
        ["7th of each month", "Salary paid; last month's withheld tax deposited (April 30 for March)"],
        ["15th of each month", "Provident Fund and ESI payments and returns"],
        ["State due dates", "Professional tax, for example the 20th in Karnataka"],
        ["July 31, October 31, January 31, May 31", "Quarterly TDS returns (Form 24Q)"],
        ["June 15", "Form 16 issued to every employee for the prior year"],
        ["January and July", "Labor Welfare Fund in many states"],
    ], "India payroll calendar") + P(
    "You get one invoice a month in USD, GBP or EUR, covering salary, employer contributions and the fee, line by line.")))

S.append(("leave", "Leave and holidays", "<h2>Leave, holidays and working hours in India</h2>" + P(
    "Leave is set mainly by each state's Shops and Establishments Act, with the labor codes as a national baseline. Paybooks applies the rules of the state where the employee works. Your own policy can be more generous.") + T(
    ["Leave type", "Entitlement", "Notes"], [
        ["Earned (annual) leave", "About 1 day for every 20 days worked; 12 to 21 days a year by state", "Can be carried over, usually up to 30 to 45 days, and paid out on exit"],
        ["Casual leave", "Often 7 to 12 days a year", "Set by state law or company policy"],
        ["Sick leave", "Often 7 to 12 days a year", "Some states combine casual and sick leave"],
        ["Maternity leave", "26 weeks paid for the first two children; 12 weeks after that", "Also 12 weeks for adoption or surrogacy"],
        ["Paternity leave", "No legal right in the private sector", "Most employers give 5 to 15 days"],
        ["National holidays", "3 days: January 26, August 15, October 2", "Required everywhere"],
        ["Festival and state holidays", "Varies; usually 10 to 15 days in total", "Karnataka requires at least 10 paid holidays"],
    ], "Leave in India") + "<h3>Working hours and overtime</h3>" + T(
    ["Rule", "Standard"], [
        ["Daily and weekly limit", "8 hours a day, 48 hours a week"],
        ["Overtime", "Paid at twice the normal rate; states set a quarterly cap" + V("Quarterly overtime caps by state")],
        ["Rest", "At least 1 day off a week and a break after about 5 hours"],
        ["Flexible schedules", "Some states allow longer days in a shorter week, within 48 hours"],
        ["Managers", "Most overtime rules do not apply to managers and supervisors"],
    ], "Working hours in India")))

S.append(("remote", "Remote work", "<h2>Remote work in India</h2>" + P(
    "Remote work is common in India, especially in tech. Employees can work from home anywhere in the country. Paybooks registers the right state for professional tax and applies that state's leave and holiday rules.",
    "Put remote-work terms in the contract: work location, hours, equipment, any internet or home-office allowance, and data security duties. Staff in Special Economic Zone units follow separate work-from-home rules." + V("SEZ work-from-home rules"))))

S.append(("checks", "Background checks", "<h2>Background checks in India</h2>" + P(
    "Background checks are legal and common in India if the candidate gives informed consent. Under the Digital Personal Data Protection Act, 2023, tell the candidate what you will check and why, and keep only what you need." + V("Consent and data-minimization rules for background checks")) + T(
    ["Check", "Common practice"], [
        ["Identity", "Verify PAN and ID documents. Use Aadhaar only where the law allows." + V("When Aadhaar may be used for verification")],
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
        ["Termination for performance or restructuring", "Contractual notice or pay instead of notice; state law may set a minimum" + V("State minimum notice for termination")],
        ["Layoff of workers (retrenchment)", "1 month's notice or pay, plus 15 days' average pay for each year of service"],
        ["Worker Re-skilling Fund", "An extra 15 days' wages per laid-off worker"],
        ["Government permission", "Needed for layoffs at 300 or more workers"],
        ["Gratuity on exit", "15 days' last-drawn wages for each year of service, after 5 years (1 year for fixed-term). Tax-free up to ₹20 lakh."],
        ["Final pay", "Salary, leave payout, gratuity and any bonus, within 2 working days"],
        ["Relieving letter", "Expected by every employee and needed for the next job"],
    ], "Exit rules in India") + CALL(
    "<strong>Paybooks runs the exit.</strong> You make the decision. We handle the legal steps, calculate and pay the dues on time, and issue the relieving letter.")))

S.append(("ip", "Intellectual property", "<h2>Protecting intellectual property</h2>" + P(
    "Under Section 17 of the Copyright Act, 1957, work an employee creates on the job belongs to the employer. With an EOR, the contract must make clear that rights pass to you, not to Paybooks. Our contracts assign all intellectual property created for you directly to your company, and include confidentiality duties.",
    "Contractors are different. Their work belongs to them unless there is a written assignment. An assignment that does not state its term or territory is treated as lasting 5 years and covering India only. This is one more reason to employ core staff rather than contract them.")))

S.append(("visas", "Work visas", "<h2>Work visas for foreign nationals in India</h2>" + P(
    "Foreign nationals need an employment visa to work in India, sponsored by the Indian employer. Overseas Citizens of India (OCI) can work without a visa in most roles.") + T(
    ["Visa", "Purpose", "Key conditions"], [
        ["Employment visa (E)", "Skilled work for an Indian employer", "Salary above $25,000 a year in most cases; issued for the contract term, up to 2 years, and extendable up to 5"],
        ["Business visa (B)", "Meetings, sales and short visits", "Cannot be used for employment"],
        ["Project visa", "Power and steel sector projects", "Limited sectors"],
        ["Intern visa", "Internships with Indian companies", "Time-limited; stipend only"],
        ["Entry visa (X)", "Dependents of employment visa holders", "Spouse and children"],
        ["OCI card", "People of Indian origin", "Can work without a visa, with limits in some sectors"],
    ], "Work visa options in India") + P(
    "Employment visa holders staying more than 180 days must register with the Foreigners Regional Registration Office (FRRO) within 14 days of arrival. Ask us before you make an offer to a foreign national, because sponsorship depends on the role and salary." + V("Whether Paybooks can sponsor employment visas"))))

S.append(("providers", "Choosing an EOR", "<h2>How to choose an employer of record in India</h2>" + P(
    "Global EOR platforms cover India through their own entity or a local partner. An India-specialist EOR runs payroll in-house. Ask every provider the same questions: who is the legal employer, who files the returns, what the full cost is, and what happens if a filing is late.") + T(
    ["Provider", "Starting price per employee a month", "Setup", "Penalty guarantee"], [
        ["Paybooks", "$199", "India payroll in-house since 2012", "Written no-penalty guarantee"],
        ["Skuad", "$199", "Own India entity", "Not published"],
        ["Deel", "$599", "Own India entity", "Not published"],
        ["Remote", "$599 to $699", "Own India entity", "Not published"],
    ], "Published list prices, September 2026" + V("Competitor list prices and guarantee status, September 2026")) + "<h3>Questions to ask any EOR in India</h3>" + UL(
    "Is the legal employer your own Indian entity, or a partner?",
    "Is the price a flat fee per employee, or a percentage of salary?",
    "What deposit do you need, and when is it returned?",
    "What exchange-rate margin do you add to the invoice?",
    "Are health insurance, background checks and offboarding included?",
    "Will you pay penalties caused by your own mistakes, in writing?")))

S.append(("pricing", "Paybooks pricing", "<h2>Paybooks EOR India pricing</h2>" + P(
    "Paybooks charges $199 per employee a month for employer of record services in India. Salary and statutory contributions are passed through at cost. The table shows what is included and what costs extra.") + T(
    ["Item", "Included in $199", "Extra cost"], [
        ["Employment contract, appointment letter and onboarding", "Yes", "None"],
        ["Monthly payroll, payslips, tax withholding and filings", "Yes", "None"],
        ["PF, ESI, professional tax and welfare fund registration and filing", "Yes", "Contributions passed through at cost"],
        ["Written no-penalty guarantee", "Yes", "None"],
        ["Exit handling and final pay", "Yes", "Statutory dues passed through"],
        ["Group health insurance", "Administration included", "Premium at cost"],
        ["Background checks", "No", "At cost, per check"],
        ["Security deposit", "No", "Usually one month's employment cost, refundable"],
        ["Currency conversion", "Bank rate", "Your bank's charges may apply"],
        ["Visa sponsorship", "No", "Quoted per case"],
        ["Transfer to your own entity", "No", "Quoted at the time"],
    ], "What the Paybooks EOR fee covers" + V("Paybooks pricing extras: insurance premium, background checks, deposit, currency conversion, visa sponsorship, entity transfer"))))

S.append(("transfer", "Moving to your own entity", "<h2>Moving from an EOR to your own entity</h2>" + P(
    "Many clients start with Paybooks and open an Indian company once the team grows. When that happens, employees move to your entity with service counted from their original start date, so gratuity and leave balances carry over.",
    "Provident Fund moves with the employee through their Universal Account Number. Paybooks issues the relieving and transfer documents, and can keep running payroll for your new entity, so employees see no change on payday.")))

FAQ = [
    ("What is an employer of record in India?", "An employer of record (EOR) in India is a local company that legally employs staff on behalf of another business. It handles the contract, payroll, tax withholding, Provident Fund, ESI and all filings, while the client manages the employee's daily work."),
    ("Is it legal to use an EOR in India?", "Yes. Paybooks is an Indian company that employs your staff under Indian law and provides their services to you. Employees get a full Indian employment contract with all statutory benefits."),
    ("How much does an employer of record cost in India?", "Paybooks charges $199 per employee a month. On top of salary, employer contributions add about 9 to 10% for skilled staff, and more for staff earning ₹21,000 a month or less."),
    ("Can a foreign company hire employees in India without an entity?", "Yes, through an employer of record. The EOR is the legal employer, so you do not need to register a company, branch or liaison office in India."),
    ("What is the difference between an EOR and a PEO in India?", "India has no co-employment model. A PEO needs you to have your own Indian entity. An EOR employs staff for you when you do not."),
    ("Should I use an EOR or set up a company in India?", "Use an EOR for first hires and teams of up to about 20 to 25 people, or while you test the market. Consider your own company when the team is larger or you sell to Indian customers."),
    ("Are there hidden fees with an EOR in India?", "Ask about deposits, exchange-rate margins, insurance, background checks and exit fees. Paybooks lists every item in its pricing table, and the no-penalty guarantee is included in the fee."),
    ("How long does it take to hire through an EOR in India?", "With Paybooks, about 10 working days from accepted offer to first day, depending on the candidate's notice period and background checks."),
    ("Can I move employees from the EOR to my own Indian entity later?", "Yes. Paybooks transfers employees with their service history intact, so gratuity and leave carry over. Provident Fund moves through the employee's Universal Account Number."),
    ("How did India's 2025 labor codes change employment costs?", "Basic pay must now be at least 50% of total pay, which raises Provident Fund and gratuity for some pay structures. Fixed-term staff now earn gratuity after one year."),
    ("Can I hire contractors in India instead of employees?", "Yes, for genuinely independent, project-based work. Long-term, full-time contractors who work under your direction risk being treated as employees, with back payments of Provident Fund and other dues."),
    ("How do I choose the best employer of record in India?", "Compare four things: whether the provider is the legal employer through its own Indian entity, the full monthly cost including deposits and exchange-rate margins, who files the statutory returns, and whether it will pay penalties caused by its own mistakes in writing."),
]
S.append(("faq", "FAQ", '<h2>Employer of record India: frequently asked questions</h2><div class="g-faq">' + "".join(
    "<details><summary>" + q + "</summary><div><p>" + a + "</p></div></details>" for q, a in FAQ) + "</div>"))

V("Author and reviewer names and credentials in the author box")
AUTHOR = ('<div class="g-author"><div class="g-av">PB</div><div><b>Written by [Author name], Payroll and Compliance, Paybooks</b>'
          '<p>Reviewed by [Reviewer name], [qualification], on ' + UPDATED + '. This guide is general information, not legal or tax advice.</p></div></div>')
RELATED = ('<h2 style="font-size:24px;margin-bottom:14px">Related</h2><div class="g-rel">'
           '<a href="../../">Employer of Record India<small>Hire in India in 10 working days</small></a>'
           '<a href="#cost">EOR cost in India<small>Worked examples in INR and USD</small></a>'
           '<a href="#peo">EOR vs PEO in India<small>Which one you need</small></a></div>')

QUOTE = ('<section id="quote"><div class="g-kt" style="background:var(--green-600)"><h2>Get an EOR India quote</h2>'
         '<p style="font-size:19px;color:#fff;margin-bottom:16px">Tell us the role, city and pay. Within two working days you get the full monthly cost in dollars, the contract terms, a start date and a sample offer letter.</p>'
         '<div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" href="#quote">Talk to an EOR expert</a></div></div></section>')

# ---------------- page ----------------
toc = "".join('<li><a href="#' + i + '">' + lbl + "</a></li>" for i, lbl, _ in S)
body = LEAD + KT + "".join('<section id="' + i + '">' + h + "</section>" for i, _l, h in S) + QUOTE + AUTHOR + RELATED

def text_of(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)
    return H.unescape(re.sub(r"<[^>]+>", " ", h))

TITLE = "Employer of Record India: EOR Costs, Laws and Hiring (2026)"
DESC = ("Hire in India without an entity. See employer of record India costs in INR and USD, labor code rules, "
        "taxes, leave and exits. Paybooks EOR from $199 a month.")
H1 = "Employer of Record India: the 2026 guide to EOR costs, laws and hiring"

schema = [
    {"@context": "https://schema.org", "@type": "Article", "headline": H1,
     "description": DESC, "dateModified": "2026-09-24", "author": {"@type": "Person", "name": "[Author name]"},
     "publisher": {"@type": "Organization", "name": "Paybooks, a TransPerfect company", "url": "https://www.paybooks.in/"},
     "about": {"@type": "Thing", "name": "Employer of record in India"}, "mainEntityOfPage": CANON},
    {"@context": "https://schema.org", "@type": "Service", "name": "Employer of Record India", "serviceType": "Employer of record",
     "provider": {"@type": "Organization", "name": "Paybooks, a TransPerfect company", "url": "https://www.paybooks.in/"},
     "areaServed": {"@type": "Country", "name": "India"},
     "offers": {"@type": "Offer", "price": "199", "priceCurrency": "USD", "description": "Per employee per month"}},
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
HERO = ('<section class="g-hero"><div class="wrap"><nav class="g-crumbs" aria-label="Breadcrumb"><a href="../../">Home</a><span>/</span><a href="../../">Employer of Record</a><span>/</span>India</nav>'
        '<h1>' + H1 + '</h1>'
        '<p class="g-sub">How a company outside India can hire here legally: the cost in rupees and dollars, the new labor codes, tax, leave, notice and exit rules, and what an employer of record handles for you.</p>'
        '<div class="g-meta"><span>Updated <b>' + UPDATED + '</b></span><span>Reviewed by <b>[Reviewer name]</b></span><span><b>' + str(round(words_est / 230)) + ' min</b> read</span></div>'
        '<p class="g-note">Sample content prepared from a few hours of product knowledge. May contain errors.</p>'
        '<div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" style="color:var(--ink) !important;border-color:var(--line-2)" href="#cost">See EOR costs in India</a></div></div></section>')

MTOC = '<details class="g-mtoc"><summary>On this page</summary><ol>' + toc + "</ol></details>"
TOC = ('<aside class="g-toc" aria-label="Contents"><h2>On this page</h2><ol>' + toc + '</ol>'
       '<div class="g-toc-cta"><p>Full monthly cost for your role, in dollars, in 2 working days.</p><a class="btn" href="#quote">Get a quote</a></div></aside>')

FOOTER = ('<footer class="ftr"><div class="wrap" style="grid-template-columns:1fr"><div><h4>Paybooks, a TransPerfect company</h4>'
          '<p>Employer of Record, Multi-Country Payroll, Managed India Office, and Global HCM for companies building teams in India and beyond.</p></div></div></footer>')

SPY = ('<script>(function(){var l=[].slice.call(document.querySelectorAll(".g-toc a"));var m={};l.forEach(function(a){m[a.getAttribute("href").slice(1)]=a});'
       'if(!("IntersectionObserver" in window))return;var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){l.forEach(function(a){a.classList.remove("on")});'
       'var a=m[e.target.id];if(a)a.classList.add("on")}})},{rootMargin:"-10% 0px -80% 0px"});'
       'document.querySelectorAll(".g-body section[id]").forEach(function(s){o.observe(s)})})();</script>')

page = HEAD + HEADER + HERO + '<div class="g-layout">' + TOC + '<main class="g-body">' + MTOC + body + "</main></div>" + FOOTER + SPY + "</body></html>"
open(OUT, "w").write(page)
with open(os.path.join(HERE, "verify-list.md"), "w") as f:
    f.write("# Claims to confirm before publishing\n\nThese are not shown on the page. Paybooks should confirm each one.\n\n")
    for n in dict.fromkeys(VERIFY): f.write("- " + n + "\n")
print("words", words_est, "tables", page.count("<table"), "verify items", len(dict.fromkeys(VERIFY)))
