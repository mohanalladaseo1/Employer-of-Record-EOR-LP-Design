# Builds /employer-of-record/india/index.html : long-form Employer of Record India guide (sample content).
# Python 3.9 safe: no backslashes inside f-string expressions.
import json, os, re, html as H

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
FX = 88.0  # INR per USD, illustrative
V = '<span class="vf">[verify]</span>'
CANON = "https://www.paybooks.in/employer-of-record/india/"
UPDATED = "24 September 2026"

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

def T(head, rows, cap=None, cls=None, num=()):
    """head: list of header cells; rows: list of lists. First cell of each body row is a row header.
    num: column indexes to right-align. A row starting with '!' is a total row."""
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
def CALL(t, warn=False): return '<div class="g-call' + (' warn' if warn else '') + '"><p>' + t + "</p></div>"
def CTA(title, sub, btn="Get a quote for a role"):
    return '<div class="g-cta"><div><b>' + title + "</b><p>" + sub + '</p></div><a class="btn" href="#quote">' + btn + "</a></div>"

# ---------------- worked cost examples ----------------
def cost_example(gross_m, state_pt_emp, lwf_emp_y, ins_y, basic_share=0.5, pf_on_full=True):
    basic = gross_m * basic_share
    pf_wage = basic if pf_on_full else min(basic, 15000)
    lines = []
    lines.append(("Gross salary", gross_m * 12, "Agreed annual pay. Basic set at 50% of pay to meet the Labour Code wage rule."))
    lines.append(("Employer Provident Fund, 12%", pf_wage * 0.12 * 12, "12% of basic wages. Statutory minimum is 12% of wages up to ₹15,000 a month; most employers of skilled staff contribute on full basic."))
    lines.append(("EPF admin and EDLI insurance", min(pf_wage, 15000) * 0.01 * 12, "About 0.5% administration plus 0.5% deposit-linked insurance, on wages up to ₹15,000 " + V))
    esi = gross_m * 0.0325 * 12 if gross_m <= 21000 else 0
    lines.append(("Employer ESI, 3.25%", esi, "Only for employees earning ₹21,000 a month or less." if esi else "Not due: gross pay is above ₹21,000 a month."))
    bonus = min(basic, 7000) * 0.0833 * 12 if gross_m <= 21000 else 0
    lines.append(("Statutory bonus, 8.33% minimum", bonus, "Due to employees earning ₹21,000 a month or less, on a capped wage of ₹7,000 or the minimum wage, whichever is higher " + V if bonus else "Not due: pay is above the ₹21,000 eligibility limit."))
    lines.append(("Gratuity provision, 4.81%", basic * 0.0481 * 12, "Accrued monthly so the payout is funded. Paid on exit after 5 years, or after 1 year for fixed-term staff."))
    lines.append(("Labour Welfare Fund, employer share", lwf_emp_y, "State levy. Karnataka shown " + V))
    lines.append(("Group health insurance", ins_y, "Market practice, not a legal duty for most staff. Priced at cost " + V))
    return lines

EX1 = cost_example(200000, 200, 50, 18000)
EX2 = cost_example(20000, 0, 50, 9000)
FEE_Y = 199 * 12 * FX

def cost_table(lines, cap):
    rows = []
    tot = 0
    for name, amt, note in lines:
        tot += amt
        rows.append([name, inr(amt) if amt else "₹0", usd(amt) if amt else "$0", note])
    rows.append(["Paybooks EOR fee", inr(FEE_Y), "$2,388", "$199 per employee a month. Billed in USD."])
    tot += FEE_Y
    rows.append(["!Total annual cost of employment", inr(tot), usd(tot), ""])
    return T(["Cost line", "Per year (INR)", "Per year (USD)", "What it is"], rows, cap, num=(1, 2)), tot

EX1_T, EX1_TOT = cost_table(EX1, "Worked example 1. Senior software engineer, Bengaluru, ₹24 lakh a year")
EX2_T, EX2_TOT = cost_table(EX2, "Worked example 2. Customer support associate, Bengaluru, ₹2.4 lakh a year")
EX1_ON = (EX1_TOT - 2400000 - FEE_Y) / 2400000 * 100
EX2_ON = (EX2_TOT - 240000 - FEE_Y) / 240000 * 100

# ---------------- income tax worked example ----------------
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

S.append(("glance", "India at a glance", "<h2>India at a glance for employers</h2>" + P(
    "India has one of the largest skilled workforces in the world, with deep pools of engineers, analysts, finance and support talent. It is also one of the more complex places to employ people: rules are set nationally and by each state, and four new Labour Codes came into force in November 2025.",
    "The table below gives the facts most hiring managers ask for first. Each item is covered in more detail further down this guide.") + T(
    ["Item", "India"], [
        ["Currency", "Indian rupee (INR, ₹). Salaries must be paid in rupees to an Indian bank account."],
        ["Financial and tax year", "1 April to 31 March. A new Income-tax Act, 2025 applies from 1 April 2026 " + V],
        ["Payroll frequency", "Monthly. Wages are due by the 7th of the following month."],
        ["Standard working time", "8 hours a day and 48 hours a week, with overtime paid at twice the ordinary rate."],
        ["Employer social security", "Provident Fund 12% of basic wages, ESI 3.25% for lower earners, gratuity on exit."],
        ["Income tax", "Progressive, 0% to 30% plus 4% cess under the default new regime. Employer deducts monthly."],
        ["Paid leave", "Set by each state's Shops and Establishments Act, typically 12 to 21 days of earned leave " + V],
        ["Public holidays", "3 national holidays plus state and festival holidays, usually 10 to 15 days in total " + V],
        ["Probation", "Not set by law. 3 to 6 months is common."],
        ["Notice period", "Set by contract. 30 to 90 days is common for skilled roles."],
        ["Main employment laws", "Code on Wages 2019, Industrial Relations Code 2020, Code on Social Security 2020, Occupational Safety, Health and Working Conditions Code 2020."],
        ["Time to hire through Paybooks", "Contract issued in about 2 working days; employee live in about 10 working days."],
    ], "India employment facts")))

S.append(("what", "What an EOR does in India", "<h2>What an Employer of Record does in India</h2>" + P(
    "An Employer of Record (EOR) is an Indian company that becomes the legal employer of people who work for you. Paybooks signs the employment contract, runs payroll in rupees, deducts income tax, pays Provident Fund and ESI, and files every return. You choose the person, set their work and manage them day to day.",
    "This lets a company outside India hire full-time employees in India without opening a subsidiary or branch. The employee gets a proper Indian employment contract with statutory benefits. You get one monthly invoice that covers salary, employer contributions and the service fee.") +
    "<h3>What Paybooks handles and what you keep</h3>" + T(
    ["Responsibility", "Paybooks", "Your company"], [
        ["Choose the candidate and agree the pay", "Advises on market pay and structure", "Decides"],
        ["Employment contract and appointment letter", "Drafts, issues and signs under Indian law", "Approves role, pay and terms"],
        ["Monthly payroll, payslips and tax deduction", "Runs it end to end", "Approves changes such as raises"],
        ["Provident Fund, ESI, professional tax, welfare fund", "Registers, pays and files", "No action"],
        ["Benefits and health insurance", "Arranges and administers", "Chooses the plan level"],
        ["Daily work, goals and performance", "No role", "Manages directly"],
        ["Equipment and access", "Can arrange on request", "Usually provides"],
        ["Leave records and holidays", "Keeps the statutory records", "Approves leave"],
        ["Resignation, termination and final settlement", "Runs the legal process and pays dues", "Makes the decision"],
    ], "Division of responsibilities")))

S.append(("peo", "EOR vs PEO", "<h2>EOR vs PEO in India</h2>" + P(
    "In the United States, a Professional Employer Organization (PEO) shares employment with a client that already has a local entity. India has no co-employment model of that kind. When a provider in India says PEO, it almost always means an Employer of Record or a payroll service for a company that already has an Indian entity.",
    "The practical question is simple. If you do not have an Indian company, you need an EOR. If you do, you need payroll and compliance support, which Paybooks also provides.") + T(
    ["Factor", "Employer of Record", "PEO or payroll outsourcing"], [
        ["Do you need an Indian entity?", "No", "Yes"],
        ["Who is the legal employer?", "Paybooks", "Your Indian company"],
        ["Who holds statutory registrations?", "Paybooks (PF, ESI, professional tax, labour welfare)", "Your Indian company"],
        ["Who carries compliance liability?", "Paybooks, backed by a written no-penalty guarantee", "Your company, with provider support"],
        ["Best fit", "First hires in India, testing the market, teams under about 20 to 25 people", "Established teams with their own entity"],
    ], "EOR compared with PEO and payroll outsourcing")))

S.append(("entity", "EOR vs your own entity", "<h2>EOR vs setting up your own Indian entity</h2>" + P(
    "Most foreign companies that plan to stay in India eventually open a private limited company. The question is when. An entity gives you full control and can be cheaper at scale, but it takes weeks to set up and brings fixed costs from the first day: directors, a registered office, auditors, annual filings, foreign investment reporting and transfer pricing.",
    "An EOR lets you hire now and decide on an entity once the team and the plan are proven. Paybooks can later move employees to your entity with their service history intact, and our Managed India Office team can set the entity up for you.") + T(
    ["Factor", "Employer of Record", "Own private limited company"], [
        ["Time to first hire", "About 10 working days", "Typically 6 to 12 weeks including bank and tax registrations " + V],
        ["Upfront cost", "None beyond any deposit", "Incorporation, legal and registration costs"],
        ["Fixed yearly cost", "None. You pay per employee.", "Audit, company secretary, filings, office and accounting " + V],
        ["Resident director needed", "No", "Yes. At least one director must have stayed in India 182 days or more in the prior year."],
        ["Tax exposure for the parent", "Lower. Staff are employed by an Indian company. Some activities can still create a taxable presence " + V, "Profits taxed in India; transfer pricing applies"],
        ["Can sign local contracts and invoice customers", "No. The EOR only employs.", "Yes"],
        ["Exit cost", "Give notice; Paybooks handles final settlement", "Winding up a company can take a year or more " + V],
        ["When it makes sense", "0 to about 25 employees, or while the India plan is being tested", "Large or long-term teams, or when you sell to Indian customers"],
    ], "EOR compared with your own Indian company") + CALL(
    "<strong>A rule of thumb.</strong> Below about 20 to 25 employees, an EOR usually costs less than running an entity once audit, compliance staff and management time are counted. Above that, compare both on a full-cost basis. We share that comparison with every quote.")))

S.append(("contractor", "Employees vs contractors", "<h2>Employees vs independent contractors in India</h2>" + P(
    "Many companies start in India with contractors because it looks simpler. It is legal to engage genuine independent contractors, but Indian courts look at the reality of the relationship, not the label in the contract. A long-term, full-time contractor who works only for you, under your direction, is likely to be treated as an employee.",
    "If that happens, the company can owe back Provident Fund contributions with interest and damages, unpaid gratuity and leave, and may face questions about a taxable presence in India. Contractors also have no statutory benefits, which makes it harder to hire and keep good people.") + T(
    ["Factor", "Full-time employee", "Independent contractor"], [
        ["Contract", "Employment contract and appointment letter", "Service agreement for defined deliverables"],
        ["Working time", "Fixed hours under labour law", "Sets own hours"],
        ["Control", "Employer directs how and when work is done", "Contractor decides how the work is done"],
        ["Tools and equipment", "Usually provided by the employer", "Contractor's own"],
        ["Pay", "Monthly salary in rupees, tax deducted", "Invoices; handles own tax and GST"],
        ["Statutory benefits", "PF, ESI where eligible, gratuity, paid leave, maternity benefit", "None"],
        ["Intellectual property", "Employer owns work made in the course of employment", "Needs a written assignment"],
        ["Termination", "Notice and statutory dues", "As the agreement says"],
    ], "Employee and contractor compared") +
    "<h3>How Indian courts decide employment status</h3>" + P("There is no single statutory test. Courts weigh several tests together.") + T(
    ["Test", "What the court asks"], [
        ["Control test", "Does the company control what the worker does and how they do it? Set out in Dharangadhara Chemical Works v State of Saurashtra (1957)."],
        ["Integration test", "Is the worker part of the business, for example on the team, in the org chart, using company systems and email?"],
        ["Economic reality test", "Does the worker depend on this one company for their living, and who bears the risk of profit and loss?"],
        ["Multiple factor test", "Who appoints, pays and can dismiss the worker, and who supplies the tools? Courts look at the whole picture."],
    ], "Tests used to identify employment") + CALL(
    "<strong>Converting contractors is straightforward.</strong> Paybooks can move existing Indian contractors onto employment contracts, usually in one payroll cycle, so their status matches how they actually work.")))

S.append(("routes", "How to hire in India", "<h2>How to hire employees in India: three routes</h2>" + P(
    "A foreign company has three realistic ways to employ people in India. The right one depends on how many people you need, how fast, and how long you plan to stay.") + T(
    ["Route", "How it works", "Speed", "Best for"], [
        ["Own subsidiary", "Incorporate a private limited company, register for tax, PF and ESI, then employ directly", "Slowest, often 2 to 3 months", "Large, long-term operations"],
        ["Employer of Record", "Paybooks employs the person on your behalf under Indian law", "About 10 working days", "First hires, small and growing teams"],
        ["Contractors", "Engage self-employed professionals for defined projects", "Fast", "Genuinely short, project-based work"],
    ], "Ways to hire in India") +
    "<h3>Hiring through Paybooks, step by step</h3><ol>" +
    "<li><strong>Share the role, city and pay.</strong> We return the full monthly cost in dollars within two working days.</li>" +
    "<li><strong>Make the offer.</strong> We draft an offer letter that shows your company, the manager and the role.</li>" +
    "<li><strong>Onboarding.</strong> The employee submits documents online. We run background checks you choose and register them for PF and ESI.</li>" +
    "<li><strong>Contract signed.</strong> Paybooks issues the appointment letter and employment contract.</li>" +
    "<li><strong>First payroll.</strong> The employee is paid by the 7th of the following month, with a payslip and tax deducted.</li></ol>" +
    CTA("See what your first India hire will cost", "Role, city and salary in. Full monthly cost in dollars out, within two working days.")))

S.append(("onboarding", "Onboarding and contracts", "<h2>Onboarding documents and contract requirements</h2>" + P(
    "Under the Labour Codes every employee must receive a written appointment letter. Paybooks issues it together with a full employment contract. Both are in English, which is standard for professional roles in India.") + T(
    ["Document", "Indian citizens", "Foreign nationals"], [
        ["Tax identity", "PAN card (Permanent Account Number)", "PAN, applied for on arrival if needed"],
        ["Identity and address", "Aadhaar card, passport or voter ID", "Passport"],
        ["Right to work", "Not required", "Employment visa and FRRO registration where required"],
        ["Provident Fund", "Universal Account Number (UAN) if previously employed", "Covered as an international worker " + V],
        ["Education and past employment", "Degree certificates, relieving letters, last payslips", "Same, plus attested copies if requested"],
        ["Bank account", "Indian account in the employee's name", "Indian account (NRO or resident account)"],
        ["Tax declaration", "Choice of old or new tax regime, investment declarations", "Same"],
    ], "Documents needed at onboarding") +
    "<h3>What an Indian employment contract should include</h3>" + UL(
    "Job title, duties, place of work and whether remote work is allowed.",
    "Start date, probation period and confirmation terms.",
    "Salary broken into basic, allowances and variable pay, with the gross and cost-to-company figures.",
    "Working hours, leave and holidays under the applicable state law.",
    "Notice period for both sides and grounds for termination.",
    "Confidentiality, data protection and assignment of intellectual property.",
    "Non-solicitation. Note that post-employment non-compete clauses are generally unenforceable in India under Section 27 of the Indian Contract Act.") +
    "<h3>Contract types</h3>" + T(
    ["Contract type", "Use", "Key rule"], [
        ["Permanent (indefinite)", "Most roles", "Continues until resignation or termination"],
        ["Fixed-term", "Projects, seasonal or time-bound roles", "Same pay and benefits as permanent staff. Gratuity after 1 year of service."],
        ["Part-time", "Reduced hours", "Pro-rated pay and leave; social security still applies " + V],
        ["Internship", "Students and recent graduates", "Stipend; not treated as employment for most statutes " + V],
    ], "Employment contract types")))

S.append(("cost", "Cost of employment", "<h2>What it really costs to employ someone in India</h2>" + P(
    "The total cost of an employee in India has three parts: the gross salary, the employer's statutory contributions, and the EOR fee. For skilled professionals, employer contributions usually add about 9 to 10% to the salary. For employees earning ₹21,000 a month or less, ESI and statutory bonus push that to roughly 15 to 20%.",
    "Below are two worked examples in rupees and dollars at an illustrative rate of ₹" + str(int(FX)) + " to $1 " + V + ". Your quote uses the live rate on the day.") +
    EX1_T + CALL("<strong>Example 1 in one line.</strong> A ₹24 lakh salary (about " + usd(2400000) + ") costs about " + usd(EX1_TOT) + " a year in total. Employer costs other than salary and the fee add about " + format(EX1_ON, ".1f") + "%.") +
    EX2_T + CALL("<strong>Example 2 in one line.</strong> At lower salaries ESI and statutory bonus apply, so employer costs add about " + format(EX2_ON, ".1f") + "% before the fee. The flat $199 fee is a larger share of a small salary, which is why we quote every role individually.") +
    "<h3>Employer contributions at a glance</h3>" + T(
    ["Contribution", "Employer", "Employee", "Applies to"], [
        ["Employees' Provident Fund (EPF and EPS)", "12% of basic wages", "12% of basic wages", "All employees in covered establishments; wage ceiling ₹15,000 for mandatory cover"],
        ["EPF admin and EDLI", "About 1% combined", "None", "On PF wages up to ₹15,000 " + V],
        ["Employees' State Insurance (ESI)", "3.25% of gross", "0.75% of gross", "Employees earning ₹21,000 a month or less"],
        ["Statutory bonus", "8.33% to 20% of capped wages", "None", "Employees earning ₹21,000 a month or less"],
        ["Gratuity", "About 4.81% of basic, paid on exit", "None", "After 5 years, or 1 year for fixed-term staff"],
        ["Professional tax", "None (employer deducts and pays)", "Up to ₹2,500 a year", "Most states, including Karnataka and Maharashtra"],
        ["Labour Welfare Fund", "Small fixed amount", "Small fixed amount", "States that levy it " + V],
    ], "Statutory contributions") +
    CTA("Get the full cost for your role", "Every line above, for your city and salary, in dollars. No commitment.")))

S.append(("salary", "Salary structure", "<h2>How salaries are structured in India</h2>" + P(
    "Indian salaries are quoted as annual cost-to-company (CTC) and split into components. The split matters because it decides Provident Fund, gratuity and the employee's income tax.",
    "Since the Labour Codes took effect, basic pay plus dearness allowance must be at least 50% of total remuneration for statutory calculations. If allowances exceed 50%, the excess is added back to wages. In practice most employers now set basic at 50% of pay.") + T(
    ["Component", "Typical share", "Notes"], [
        ["Basic salary", "50% of gross", "Drives PF and gratuity. Must meet the 50% wage rule."],
        ["House rent allowance (HRA)", "Up to 50% of basic in metro cities", "Tax-exempt only under the old tax regime"],
        ["Special allowance", "Balance", "Fully taxable; flexible component"],
        ["Employer NPS contribution", "Up to 14% of basic", "Tax-deductible for the employee even under the new regime"],
        ["Meal, fuel or phone reimbursements", "Small, fixed", "Tax treatment depends on regime and limits " + V],
        ["Variable pay or bonus", "Often 10% to 20% of CTC for senior roles", "Paid through payroll with tax deducted"],
    ], "Typical salary components") + P(
    "Minimum wages are set by each state by skill level and zone, and the Code on Wages adds a national floor wage. Professional salaries are far above these floors, but support and operations roles must be checked against the state schedule.")))

S.append(("tax", "Income tax", "<h2>Income tax and payroll taxes in India</h2>" + P(
    "The employer must deduct income tax at source (TDS) from salary every month and deposit it with the government. Employees choose between the default new tax regime, with lower rates and few deductions, and the old regime, with higher rates and exemptions such as HRA and Section 80C investments.") + T(
    ["Taxable income (new regime)", "Rate"], [
        ["Up to ₹4,00,000", "Nil"], ["₹4,00,001 to ₹8,00,000", "5%"], ["₹8,00,001 to ₹12,00,000", "10%"],
        ["₹12,00,001 to ₹16,00,000", "15%"], ["₹16,00,001 to ₹20,00,000", "20%"], ["₹20,00,001 to ₹24,00,000", "25%"],
        ["Above ₹24,00,000", "30%"],
    ], "New regime slabs, financial year 2025-26 " + V, num=(1,)) + UL(
    "A standard deduction of ₹75,000 applies to salaried employees under the new regime.",
    "A rebate under Section 87A means no tax is payable on taxable income up to ₹12,00,000 under the new regime.",
    "A 4% health and education cess is added to the tax. A surcharge applies above ₹50 lakh.",
    "The same slabs are expected to carry into 2026-27 under the new Income-tax Act, 2025 " + V + ".") + T(
    ["Step", "Amount"], [
        ["Gross salary", inr(2400000)], ["Less standard deduction", inr(-75000)], ["Taxable income", inr(TI)],
        ["Income tax on slabs", inr(TX)], ["Health and education cess, 4%", inr(CESS)],
        ["!Total annual tax (deducted monthly)", inr(TX + CESS)], ["Monthly TDS", inr((TX + CESS) / 12)],
    ], "Worked example. Employee tax on ₹24 lakh, new regime", num=(1,)) + P(
    "There is no separate employer payroll tax in India beyond the social security contributions above. Paybooks' fee is subject to GST where applicable; for clients outside India the service is usually treated as an export " + V + ".")))

S.append(("codes", "The Labour Codes", "<h2>The four Labour Codes: what changed in November 2025</h2>" + P(
    "On 21 November 2025 India brought four Labour Codes into force, replacing 29 older central labour laws. States are still issuing their own rules under the Codes, so some details differ by state and some older state rules continue for now " + V + ".") + T(
    ["Change", "What it means for employers"], [
        ["Uniform definition of wages", "Allowances above 50% of pay are added back to wages. This raises PF and gratuity for pay structures with low basic."],
        ["Mandatory appointment letters", "Every employee must get a written appointment letter."],
        ["Gratuity for fixed-term staff", "Payable after 1 year of service instead of 5."],
        ["National floor wage", "The central government sets a floor below which no state minimum wage can fall."],
        ["Faster final settlement", "Full and final dues are due within 2 working days of the last day " + V],
        ["Leave eligibility", "Annual leave accrues after 180 days worked, down from 240 days."],
        ["Worker Re-skilling Fund", "Employers pay 15 days' wages into a fund for each retrenched worker."],
        ["Higher thresholds", "Standing orders and prior permission for layoffs apply at 300 workers, up from 100."],
        ["Social security for gig and platform workers", "Aggregators contribute to a welfare fund. Relevant if you hire through platforms."],
        ["Women at night", "Women may work night shifts with consent and safety measures."],
    ], "Key changes under the Labour Codes") + CALL(
    "<strong>What Paybooks did.</strong> We moved every client's pay structure to the new wage definition before the first payroll under the Codes, and re-issued appointment letters where needed. Existing Paybooks employees did not have to do anything.")))

S.append(("compliance", "Compliance checklist", "<h2>Key compliance requirements</h2>" + P(
    "An employer in India holds several registrations and makes filings every month, every quarter and every year. Under an EOR, Paybooks holds all of them.") + T(
    ["Requirement", "What the employer must do", "Frequency"], [
        ["Shops and Establishments registration", "Register each office under the state law and keep registers", "Once, renewed as required"],
        ["Provident Fund", "Register, pay contributions and file the electronic challan", "Monthly, by the 15th"],
        ["ESI", "Register eligible employees and pay contributions", "Monthly, by the 15th"],
        ["Income tax (TDS)", "Deduct and deposit tax; file quarterly returns (Form 24Q)", "Monthly by the 7th; quarterly returns"],
        ["Form 16", "Issue the annual tax certificate to each employee", "Yearly, by 15 June"],
        ["Professional tax", "Deduct and pay under the state law", "Monthly in most states"],
        ["Labour Welfare Fund", "Pay the employer and employee shares", "Half-yearly or yearly, by state"],
        ["Minimum wage and timely payment", "Pay at least the minimum wage, by the 7th", "Monthly"],
        ["Maternity benefit", "26 weeks' paid leave; creche for 50 or more employees", "As needed"],
        ["Prevention of sexual harassment (POSH)", "Written policy and an Internal Committee for 10 or more employees; annual report", "Ongoing and yearly"],
        ["Data protection", "Handle employee data under the Digital Personal Data Protection Act, 2023", "Ongoing " + V],
    ], "Employer compliance checklist") +
    "<h3>What happens if you get it wrong</h3>" + P(
    "Late Provident Fund payments attract interest of 12% a year plus damages that rise with the length of the delay. Missed tax deposits attract interest and penalties, and the employee's tax credit can be affected. Labour inspectors can levy fines under the Codes, and repeat offences carry higher penalties.",
    "Paybooks backs every filing with a written no-penalty guarantee. If a statutory penalty arises from our error, we pay it.") +
    CTA("Read the no-penalty guarantee", "We share the wording with your quote, alongside a sample service agreement.", "Get the guarantee")))

S.append(("payroll", "Payroll calendar", "<h2>How payroll works in India</h2>" + P(
    "Payroll in India is monthly. Paybooks collects inputs such as new joiners, leave and bonuses, calculates pay and deductions, pays employees by the 7th of the following month and deposits every statutory payment on time. Employees get an online payslip and can submit tax declarations through the Paybooks app.") + T(
    ["Deadline", "What is due"], [
        ["7th of each month", "Salary paid; income tax deducted in the previous month deposited (30 April for March)"],
        ["15th of each month", "Provident Fund and ESI contributions and returns"],
        ["State due dates", "Professional tax, for example the 20th in Karnataka " + V],
        ["31 July, 31 October, 31 January, 31 May", "Quarterly TDS returns (Form 24Q)"],
        ["15 June", "Form 16 issued to every employee for the previous year"],
        ["January and July", "Labour Welfare Fund in many states " + V],
    ], "Payroll and statutory calendar") + P(
    "You receive one invoice in USD, GBP or EUR each month covering salary, employer contributions and the fee, with a line-by-line breakdown.")))

S.append(("leave", "Leave and holidays", "<h2>Leave policy and public holidays</h2>" + P(
    "Leave in India is set mainly by each state's Shops and Establishments Act, with the Labour Codes setting a national baseline. Paybooks applies the rules for the state where the employee works, and your own policy can be more generous.") + T(
    ["Leave type", "Entitlement", "Notes"], [
        ["Earned (annual) leave", "About 1 day for every 20 days worked; 12 to 21 days a year depending on state " + V, "Can be carried forward, typically up to 30 to 45 days, and paid out on exit"],
        ["Casual leave", "Often 7 to 12 days a year", "Set by state law or company policy"],
        ["Sick leave", "Often 7 to 12 days a year", "Some states combine casual and sick leave"],
        ["Maternity leave", "26 weeks paid for the first two children; 12 weeks after that", "Also 12 weeks for adoption or surrogacy"],
        ["Paternity leave", "No statutory right in the private sector", "Most employers offer 5 to 15 days"],
        ["National holidays", "3 days: 26 January, 15 August, 2 October", "Mandatory everywhere"],
        ["Festival and state holidays", "Varies; total holidays usually 10 to 15 days", "Karnataka requires at least 10 paid holidays " + V],
    ], "Leave entitlements") + "<h3>Working hours and overtime</h3>" + T(
    ["Rule", "Standard"], [
        ["Daily and weekly limit", "8 hours a day, 48 hours a week"],
        ["Overtime", "Paid at twice the ordinary wage; quarterly caps apply " + V],
        ["Rest", "At least 1 day off a week and a break after about 5 hours"],
        ["Flexible schedules", "States may allow longer days in a shorter week within the 48-hour limit"],
        ["Managers", "Most overtime rules do not apply to managerial and supervisory staff"],
    ], "Working hours")))

S.append(("remote", "Remote and hybrid work", "<h2>Remote and hybrid work in India</h2>" + P(
    "Remote work is common in India, especially in technology. An employee can work from home anywhere in the country. Paybooks registers the right state for professional tax and applies that state's leave and holiday rules.",
    "Put remote-work terms in the contract: the work location, working hours, equipment, any internet or home-office allowance, and data security duties. Employees in Special Economic Zone units follow separate work-from-home rules " + V + ". Staff can also work from co-working spaces, and Paybooks can arrange desks through our Managed India Office service.")))

S.append(("checks", "Background checks", "<h2>Background checks when hiring in India</h2>" + P(
    "Background checks are legal and common in India, provided the candidate gives informed consent. Under the Digital Personal Data Protection Act, 2023, you must tell the candidate what you will check and why, and keep only what you need " + V + ".") + T(
    ["Check", "Common practice"], [
        ["Identity", "Verify PAN and identity documents. Use Aadhaar only where the law allows " + V],
        ["Education", "Verify degrees directly with the university or through an agency"],
        ["Employment history", "Check relieving letters and confirm with past employers"],
        ["Criminal record", "Court record search or police verification through an agency"],
        ["Credit history", "Rare; used mainly for finance roles, with consent"],
        ["Reference checks", "Common for senior hires"],
    ], "Background checks")))

S.append(("termination", "Termination and notice", "<h2>Termination, notice and severance</h2>" + P(
    "India protects employees against termination without cause, and the rules depend on whether the person is a \"worker\" under the Industrial Relations Code. Most skilled professionals in managerial or supervisory roles are not workers under the Code, so their contract and state law govern exit.") + T(
    ["Topic", "What applies"], [
        ["Resignation", "Employee gives the contractual notice, commonly 30 to 90 days; employer may accept early release"],
        ["Termination for misconduct", "Written charge, a fair inquiry and a written order; no notice pay if misconduct is proven"],
        ["Termination for performance or restructuring", "Contractual notice or pay in lieu; state law may add a minimum notice " + V],
        ["Retrenchment of workers", "1 month's notice or pay, plus 15 days' average pay for each completed year of service"],
        ["Worker Re-skilling Fund", "An additional 15 days' wages per retrenched worker"],
        ["Government permission", "Needed for layoffs in establishments with 300 or more workers"],
        ["Gratuity on exit", "15 days' last drawn wages for each year of service, after 5 years (1 year for fixed-term). Tax-free up to ₹20 lakh."],
        ["Final settlement", "Salary, leave encashment, gratuity and any bonus, paid within 2 working days " + V],
        ["Relieving letter", "Expected by every employee; needed for the next job"],
    ], "Exit rules") + CALL(
    "<strong>Paybooks runs the exit.</strong> You make the decision. We handle the legal steps, calculate the dues, pay them on time and issue the relieving letter, so the exit is clean and documented.")))

S.append(("ip", "Intellectual property", "<h2>Protecting intellectual property</h2>" + P(
    "Under Section 17 of the Copyright Act, 1957, work an employee creates in the course of employment belongs to the employer. For an EOR arrangement, the contract must make clear that rights pass to you, the client, not to Paybooks. Our contracts assign all intellectual property created for you directly to your company and include confidentiality duties.",
    "Contractors are different. Their work belongs to them unless there is a written assignment. An assignment that does not state its term or territory is treated as lasting 5 years and covering only India, so contractor agreements need careful drafting. This is one more reason to employ core staff rather than contract them.")))

S.append(("visas", "Visas for foreign nationals", "<h2>Visas and work permits for foreign nationals</h2>" + P(
    "Foreign nationals need an employment visa to work in India, sponsored by the Indian employer. Overseas Citizens of India (OCI) can work without a visa in most roles.") + T(
    ["Visa type", "Purpose", "Key conditions"], [
        ["Employment visa (E)", "Skilled work for an Indian employer", "Salary above US$25,000 a year in most cases; issued for the contract term up to 2 years, extendable to 5 " + V],
        ["Business visa (B)", "Meetings, sales and short visits", "Cannot be used to take up employment"],
        ["Project visa", "Power and steel sector projects", "Limited sectors " + V],
        ["Intern visa", "Internships with Indian companies", "Time-limited; stipend only " + V],
        ["Entry visa (X)", "Dependants of employment visa holders", "Spouse and children"],
        ["OCI card", "People of Indian origin", "Can work without a visa, with limits on some sectors"],
    ], "Visa options") + P(
    "Employment visa holders staying more than 180 days must register with the Foreigners Regional Registration Office (FRRO) within 14 days of arrival. Ask us before you make an offer to a foreign national, because sponsorship depends on the role and salary " + V + ".")))

S.append(("providers", "Choosing an EOR provider", "<h2>How to choose an EOR provider for India</h2>" + P(
    "Global EOR platforms cover India through their own entity or a local partner. An India-specialist EOR runs payroll in-house. Ask every provider the same questions: who is the legal employer, who files the returns, what the full cost is, and what happens if a filing is late.") + T(
    ["Provider", "Starting price per employee a month", "Setup", "Penalty guarantee"], [
        ["Paybooks", "$199", "India payroll in-house since 2012", "Written no-penalty guarantee"],
        ["Skuad", "$199", "Own India entity", "Not published"],
        ["Deel", "$599", "Own India entity", "Not published"],
        ["Remote", "$599 to $699", "Own India entity", "Not published"],
    ], "Published list price, Sep 2026 " + V) + "<h3>Questions to ask any EOR</h3>" + UL(
    "Is the legal employer your own Indian entity, or a partner?",
    "Is the price fixed per employee, or a percentage of salary?",
    "What deposit do you require, and when is it returned?",
    "What exchange-rate margin is applied to the invoice?",
    "Are health insurance, background checks and offboarding included?",
    "Will you pay penalties caused by your own mistakes, in writing?")))

S.append(("pricing", "Paybooks pricing", "<h2>Paybooks EOR pricing, with nothing hidden</h2>" + P(
    "Paybooks charges $199 per employee a month for Employer of Record in India. Salary and statutory contributions are passed through at cost. The table lists what is included and what can cost extra, so there are no surprises on the first invoice.") + T(
    ["Item", "Included in $199", "Extra cost"], [
        ["Employment contract, appointment letter and onboarding", "Yes", "None"],
        ["Monthly payroll, payslips, tax deduction and filings", "Yes", "None"],
        ["PF, ESI, professional tax and welfare fund registration and filing", "Yes", "Contributions passed through at cost"],
        ["Written no-penalty guarantee", "Yes", "None"],
        ["Exit handling and final settlement", "Yes", "Statutory dues passed through"],
        ["Group health insurance", "Administration included", "Premium at cost " + V],
        ["Background checks", "No", "At cost, per check " + V],
        ["Security deposit", "No", "Typically one month's employment cost, refundable " + V],
        ["Currency conversion", "Bank rate", "Bank charges on your side may apply " + V],
        ["Visa sponsorship", "No", "Quoted per case " + V],
        ["Transfer to your own entity", "No", "Quoted at the time " + V],
    ], "What the fee covers")))

S.append(("transfer", "Moving to your own entity", "<h2>Moving employees to your own entity later</h2>" + P(
    "Many clients start with Paybooks and open an Indian company once the team reaches a certain size. When that happens, employees move to your entity with their service counted from their original start date, so gratuity and leave balances carry over.",
    "Provident Fund moves with the employee through their Universal Account Number. Paybooks issues relieving letters and transfer documents, and our payroll team can keep running payroll for your new entity, so employees see no change on payday.")))

FAQ = [
    ("Is it legal for a foreign company to hire in India through an EOR?", "Yes. Paybooks is an Indian company that employs your staff under Indian law and provides their services to you. The employee has a full Indian employment contract with all statutory benefits."),
    ("How much does an employer of record cost in India?", "Paybooks charges $199 per employee a month. On top of salary, employer contributions add about 9 to 10% for skilled professionals and more for employees earning ₹21,000 a month or less. The worked examples in this guide show every line."),
    ("Can a foreign company hire employees in India without a local entity?", "Yes, through an Employer of Record. The EOR is the legal employer, so you do not need to register a company, a branch or a liaison office."),
    ("What is the difference between an EOR and a PEO in India?", "India has no co-employment model. A PEO needs you to have your own Indian entity, while an EOR employs staff for you when you do not."),
    ("Should I use an EOR or set up a company in India?", "Use an EOR for your first hires and teams of up to about 20 to 25 people, or while you test the market. Consider your own company when the team is larger or you sell to Indian customers."),
    ("Are there hidden fees when hiring through an EOR in India?", "Ask about deposits, exchange-rate margins, insurance, background checks and offboarding fees. Paybooks lists every item in its pricing table, and the no-penalty guarantee is included in the fee."),
    ("How long does it take to hire an employee through an EOR in India?", "With Paybooks, about 10 working days from accepted offer to the employee's first day, depending on the candidate's notice period and background checks."),
    ("What happens if I later want to move the employee to my own Indian entity?", "Paybooks transfers the employee with their service history intact, so gratuity and leave carry over. Provident Fund moves through the employee's Universal Account Number."),
    ("How did the 2025 Labour Codes change employment costs?", "The new wage definition means basic pay must be at least 50% of remuneration, which raises Provident Fund and gratuity for some pay structures. Fixed-term staff now earn gratuity after one year."),
    ("Can I hire contractors in India instead?", "Yes, for genuinely independent, project-based work. Long-term, full-time contractors who work under your direction risk being treated as employees, with back payments of Provident Fund and other dues."),
]
S.append(("faq", "FAQ", '<h2>Frequently asked questions</h2><div class="g-faq">' + "".join(
    "<details><summary>" + q + "</summary><div><p>" + a + "</p></div></details>" for q, a in FAQ) + "</div>"))

AUTHOR = ('<div class="g-author"><div class="g-av">PB</div><div><b>Written by [Author name], Payroll and Compliance, Paybooks</b>'
          '<p>Reviewed by [Reviewer name], [qualification], on ' + UPDATED + ' ' + V + '. This guide is general information, not legal or tax advice.</p></div></div>')
RELATED = ('<h2 style="font-size:24px;margin-bottom:14px">Related</h2><div class="g-rel">'
           '<a href="../../">Employer of Record India<small>Hire in India in 10 working days</small></a>'
           '<a href="../../strategy/">EOR India search strategy<small>The plan behind this page</small></a>'
           '<a href="#cost">India cost of employment<small>Worked examples in INR and USD</small></a></div>')

QUOTE = ('<section id="quote"><div class="g-kt" style="background:var(--green-600)"><h2>Get a quote</h2>'
         '<p style="font-size:19px;color:#fff;margin-bottom:16px">Tell us the role, city and pay. Within two working days you get the full monthly cost in dollars, the contract terms, a start date and a sample offer letter.</p>'
         '<div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" href="#quote">Talk to an EOR expert</a></div></div></section>')

KT = ('<div class="g-kt"><h2>Key takeaways</h2><ul>'
      '<li><strong>You do not need an Indian company to hire in India.</strong> Paybooks becomes the legal employer and handles payroll, tax and every filing.</li>'
      '<li><strong>Budget salary plus about 9 to 10%, plus $199 a month</strong> for a skilled professional. ESI and statutory bonus add more below ₹21,000 a month.</li>'
      '<li><strong>The Labour Codes changed the rules in November 2025.</strong> Basic pay must be at least half of pay, and fixed-term staff earn gratuity after one year.</li>'
      '<li><strong>Long-term contractors carry real risk.</strong> Courts look at how people actually work, not what the contract says.</li>'
      '<li><strong>Start in about 10 working days,</strong> and move staff to your own entity later with their service intact.</li></ul></div>')

# ---------------- page ----------------
toc = "".join('<li><a href="#' + i + '">' + lbl + "</a></li>" for i, lbl, _ in S)
body = KT + "".join('<section id="' + i + '">' + h + "</section>" for i, _l, h in S) + QUOTE + AUTHOR + RELATED

def text_of(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)
    return H.unescape(re.sub(r"<[^>]+>", " ", h))

schema = [
    {"@context": "https://schema.org", "@type": "Article", "headline": "Employer of Record in India: The Complete 2026 Guide",
     "dateModified": "2026-09-24", "author": {"@type": "Person", "name": "[Author name]"},
     "publisher": {"@type": "Organization", "name": "Paybooks, a TransPerfect company", "url": "https://www.paybooks.in/"},
     "mainEntityOfPage": CANON},
    {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.paybooks.in/"},
        {"@type": "ListItem", "position": 2, "name": "Employer of Record", "item": "https://www.paybooks.in/employer-of-record/"},
        {"@type": "ListItem", "position": 3, "name": "India", "item": CANON}]},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]
ld = "".join('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + "</script>" for s in schema)

HEAD = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Employer of Record in India: 2026 Guide to Costs, Laws and Hiring | Paybooks</title>'
        '<meta name="description" content="How to hire in India without an entity: full cost of employment in INR and USD, the 2025 Labour Codes, tax, leave, termination and visas. Paybooks EOR from $199 a month.">'
        '<link rel="canonical" href="' + CANON + '"><meta name="robots" content="noindex,nofollow">'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@500;600;700&family=Inter:wght@400;500;600;700&family=Zilla+Slab:wght@300;400&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="../../assets/pb.css"><link rel="stylesheet" href="../../assets/guide.css">' + ld + "</head><body>")

HEADER = ('<header class="hdr"><div class="wrap"><a class="brand" href="../../"><img src="../../assets/mark.png" alt="Paybooks" width="44" height="44"><span class="wm"><b>paybooks</b><small>A TransPerfect company</small></span></a>'
          '<nav class="nav"><a href="../../">Employer of Record</a><a>Payroll</a><a>India Office</a><a>HCM</a><a>Resources</a></nav>'
          '<div class="btns"><a class="btn ghost" href="#quote">Book a call</a><a class="btn" href="#quote">Get a quote</a></div></div></header>')

words_est = len(text_of(body).split())
HERO = ('<section class="g-hero"><div class="wrap"><nav class="g-crumbs" aria-label="Breadcrumb"><a href="../../">Home</a><span>/</span><a href="../../">Employer of Record</a><span>/</span>India</nav>'
        '<h1>Employer of Record in India: the complete 2026 guide</h1>'
        '<p class="g-sub">Everything a company outside India needs to hire here legally: what it costs in rupees and dollars, the new Labour Codes, tax, leave, notice and exit rules, and how an Employer of Record handles all of it.</p>'
        '<div class="g-meta"><span>Updated <b>' + UPDATED + '</b></span><span>Reviewed by <b>[Reviewer name]</b></span><span><b>' + str(round(words_est / 230)) + ' min</b> read</span></div>'
        '<p class="g-note">Sample content prepared from a few hours of product knowledge. May contain errors. Items marked [verify] need confirmation.</p>'
        '<div class="btns"><a class="btn" href="#quote">Get a quote for a role</a><a class="btn ghost" style="color:var(--ink) !important;border-color:var(--line-2)" href="#cost">See the cost breakdown</a></div></div></section>')

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
print("words", words_est, "tables", page.count("<table"), "verify", page.count('class="vf"'))
