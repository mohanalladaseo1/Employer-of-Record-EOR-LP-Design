"""Build the Paybooks keyword and topic research report.

Reads keywords_clean.csv (Ahrefs pull, 23 Sep 2026), assigns every keyword to a
topic (a target page) inside its category bucket, separates off-intent keywords
with a stated reason, and writes:
  - research/index.html          nested-dropdown report
  - research/keyword-topic-map.csv  one row per keyword with bucket, topic, page type
"""
import csv, re, html, json, os, collections

SRC = "/Users/mohankumarallada/Claude_Code_Projects/TransPerfect Paybooks Proposal/research/keywords_clean.csv"
OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)

rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
RAW = len(rows)

# ---------- dedupe: exact repeats, and the same keyword+country in two buckets ----------
ORDER = ["eor", "payroll", "india_office", "hcm"]
seen = {}
dups_exact, dups_cross = 0, 0
clean = []
for cat in ORDER:
    for r in [x for x in rows if x["category"] == cat]:
        key = (r["keyword"].strip().lower(), r["country"])
        if key in seen:
            if seen[key] == cat: dups_exact += 1
            else: dups_cross += 1
            continue
        seen[key] = cat
        clean.append(r)

def num(v):
    try: return float(v)
    except: return 0.0

for r in clean:
    r["kw"] = r["keyword"].strip().lower()
    r["vol"] = int(num(r["volume"]))
    r["kdn"] = num(r["kd"]) if r["kd"] not in ("", None) else None
    r["cpcn"] = num(r["cpc_usd"]) if r["cpc_usd"] not in ("", None) else None

def has(kw, pat): return re.search(pat, kw) is not None

CITIES = r"\b(bangalore|bengaluru|chennai|mumbai|delhi|ncr|pune|hyderabad|kolkata|gurgaon|noida)\b"

# ---------- topic plans (page sets come from the SERP research reports) ----------
# type: LP = landing page, LPS = landing page set, TOOL = interactive tool, ART = support article
PLAN = {
"eor": {
  "name": "Employer of Record", "pillar": "Employer of Record India",
  "pillar_url": "/employer-of-record-india/",
  "why": "Service-intent SERP. Skuad and Wisemonk win with 6,500 to 8,500-word country pages, question-form headings, 3 to 12 tables, a published price and 6 to 10 FAQs.",
  "topics": [
    ("hub", "LP", 1, "Employer of Record hub", "/employer-of-record/", "Generic head terms. The category page that frames India-first EOR and links out to every India page.", []),
    ("india", "LP", 1, "Employer of Record India (pillar)", "/employer-of-record-india/", "The core commercial page. Built as the sample landing page.", []),
    ("pricing", "LP", 1, "EOR India pricing and cost", "/employer-of-record-india/pricing/", "Fee table, statutory costs, worked examples in USD and INR, hidden-fee checklist.", []),
    ("hire", "LP", 1, "Hire employees in India", "/hire-employees-in-india/", "Commercial twin of the how-to guide.", []),
    ("peo", "LP", 1, "PEO India", "/peo-india/", "Wisemonk runs both EOR and PEO pages; Deel has an India-specific PEO post.", ["peo india", "peo services india", "peo vs eor india"]),
    ("segment", "LPS", 2, "Segment pages: startups, UK companies", "/eor-india-for-startups/ · /eor-india-for-uk-companies/", "Almost every ranking page is written for US buyers.", ["eor india for startups", "hire in india from uk"]),
    ("country", "LPS", 27, "Country EOR pages (Wave 3)", "/employer-of-record/[country]/", "KD 0 to 1 across 27 countries. Only worth building once Paybooks can deliver EOR outside India.", []),
    ("tool_cost", "TOOL", 1, "India employee cost calculator", "/tools/india-employee-cost-calculator/", "Every competitor has one; ours adds a Labour Codes wage-floor toggle.", ["india employee cost calculator", "ctc calculator"]),
    ("tool_entity", "TOOL", 1, "EOR vs entity calculator", "/tools/eor-vs-entity-calculator-india/", "Deel and Wisemonk both have one.", ["eor vs entity cost india"]),
    ("a_howto", "ART", 1, "How to hire employees in India without an entity", "Guide", "Three-routes table, permanent establishment and misclassification sections.", []),
    ("a_what", "ART", 1, "What is an employer of record, and how it works", "Guide", "Definition intent; feeds AI answers.", []),
    ("a_vspeo", "ART", 1, "EOR vs PEO vs staffing agency in India", "Guide", "No page-one result is India-specific.", []),
    ("a_vsentity", "ART", 1, "EOR vs your own subsidiary in India", "Guide", "Cost, timeline, and the headcount where it flips.", []),
    ("a_best", "ART", 1, "Best employer of record providers for India", "Guide", "Honest comparison; Paybooks appears once.", []),
    ("a_plan", "ART", 7, "Planned guides from buyer questions", "Guides", "Is an EOR legal in India · permanent establishment risk · contractor misclassification · Labour Codes for foreign employers · state rules when a hire moves · paying India staff from the US · moving from EOR to your own entity.", ["is eor legal in india", "permanent establishment risk india", "contractor vs employee india", "labour codes eor india", "how to pay employees in india from us", "switch from eor to entity"]),
  ]},
"payroll": {
  "name": "Multi-Country Payroll", "pillar": "Multi-Country Payroll",
  "pillar_url": "/multi-country-payroll/",
  "why": "\"payroll outsourcing india\" is a service-page SERP led by ADP India. \"global payroll\" mixes guides with ADP and Remote product pages. Nobody owns payroll for Indian companies paying staff abroad.",
  "topics": [
    ("global", "LP", 1, "Multi-country payroll (pillar)", "/multi-country-payroll/", "Global, international and multi-country payroll service and platform terms.", []),
    ("india", "LP", 1, "Payroll outsourcing India", "/payroll-outsourcing-india/", "Consolidates five overlapping live Paybooks pages. Processing, managed and comprehensive tiers.", []),
    ("managed", "LP", 1, "Managed payroll", "/managed-payroll/", "Managed service vs software, the disambiguation Paybooks needs.", []),
    ("country", "LPS", 5, "Country payroll pages", "/global-payroll/[uae | singapore | united-kingdom | united-states | india]/", "Payroll for Indian companies expanding abroad, plus India-inbound.", ["payroll in uae for indian companies", "wps payroll"]),
    ("city", "LPS", 6, "City payroll outsourcing pages", "/payroll-outsourcing-[city]/", "Paysquare and Wisemonk both run six to nine city pages.", []),
    ("tool", "TOOL", 2, "Payroll cost calculator and compliance calendar", "/tools/", "Cost per employee, India and international; one refreshed calendar.", ["payroll outsourcing cost calculator", "payroll compliance calendar"]),
    ("compare", "LPS", 3, "Compare pages", "/compare/paybooks-vs-[adp-india | paysquare | deel]/", "The vs space is owned by global EOR brands; India-first comparisons barely exist.", ["paybooks vs adp", "adp india alternatives"]),
    ("a_what", "ART", 1, "What is multi-country payroll", "Guide", "Definition intent, vs global payroll and EOR.", []),
    ("a_vs", "ART", 1, "Global payroll vs EOR vs PEO", "Guide", "Which one an Indian company needs abroad.", []),
    ("a_cost", "ART", 1, "How much payroll outsourcing costs in India", "Guide", "Per-employee bands, setup, hidden fees, GST.", []),
    ("a_why", "ART", 1, "Should you outsource payroll? Benefits, risks, and trade-offs", "Guide", "Benefits, pros and cons, break-even by headcount.", []),
    ("a_run", "ART", 1, "Running payroll across countries: compliance, tax, FX, reporting", "Guide", "The operational questions buyers ask assistants.", []),
    ("a_best_in", "ART", 1, "Top payroll outsourcing companies in India", "Guide", "Refresh of the existing Paybooks list, with a stated method.", []),
    ("a_best_gl", "ART", 1, "Best global payroll providers", "Guide", "The only India-perspective list in the space.", []),
    ("a_plan", "ART", 10, "Planned guides from buyer questions", "Guides", "UAE, Singapore, UK and US payroll how-tos · shadow payroll for deputed staff · Labour Codes CTC restructuring · PF, ESI, PT, LWF by state · payroll RFP template · consolidating payroll vendors · software vs outsourcing.", ["shadow payroll india", "labour code salary restructuring", "payroll rfp template"]),
  ]},
"india_office": {
  "name": "Managed India Office", "pillar": "Managed India Office",
  "pillar_url": "/managed-india-office/",
  "why": "The category does not exist in search yet, so the pillar ranks for adjacent terms: GCC setup, subsidiary setup, statutory compliance, HR outsourcing. The Labour Codes cluster is the single biggest opening in the study.",
  "topics": [
    ("mio", "LP", 1, "Managed India Office (pillar)", "/managed-india-office/", "Defines the category; models table of EOR, build-operate-transfer, managed entity and do-it-yourself.", ["managed gcc", "gcc as a service", "managed india operations"]),
    ("gcc", "LP", 1, "GCC setup in India", "/gcc-setup-india/", "Wisemonk's 8,500-word hub outranks ANSR's 2,200-word blog.", []),
    ("sub", "LP", 1, "India subsidiary setup", "/india-subsidiary-setup/", "Needs the six tables IndiaFilings ranks with.", []),
    ("bot", "LP", 1, "Build-operate-transfer India", "/build-operate-transfer-india/", "ANSR's page ranks; ours adds a transfer checklist.", ["build operate transfer india", "bot model gcc"]),
    ("stat", "LP", 1, "Statutory compliance outsourcing", "/statutory-compliance-outsourcing-india/", "Written for the foreign parent, not Indian HR.", []),
    ("hro", "LP", 1, "HR outsourcing services India", "/hr-outsourcing-india/", "300 + 300 India searches a month, held by domestic HR vendors.", []),
    ("rd", "LP", 1, "Resident director services", "/resident-director-services-india/", "Commenda and Treelife show real commercial intent.", ["resident director india", "nominee director india"]),
    ("labour_hub", "TOOL", 1, "Labour Codes hub and state tracker", "/labour-codes/", "31,850 searches a month answered by government PDFs and Big Four alerts. The flagship content asset.", []),
    ("tool_cal", "TOOL", 2, "Compliance calendar and GCC cost estimator", "/tools/", "Checklist, calendar and a published GCC cost model.", ["gcc setup cost india calculator"]),
    ("a_labour", "ART", 1, "New Labour Codes: gratuity, wages, and leave explained", "Guide", "The practical questions inside the Labour Codes cluster.", []),
    ("a_stat", "ART", 1, "What statutory compliance means for HR and payroll in India", "Guide", "Definition and meaning searches.", []),
    ("a_se", "ART", 1, "Shops and Establishments Act by state", "Guide", "One canonical state map, linked from EOR and payroll too.", []),
    ("a_gcc_what", "ART", 1, "What is a GCC? Definition, examples, and India's GCC landscape", "Guide", "Definition, examples and company lists.", []),
    ("a_gcc_cost", "ART", 1, "How much a GCC in India costs", "Guide", "By headcount band, city tier and entry model.", []),
    ("a_gcc_model", "ART", 1, "GCC vs EOR vs BOT vs shared services: choosing a model", "Guide", "Operating model, governance, and when each model fits.", []),
    ("a_gcc_city", "ART", 1, "Best city for a GCC in India", "Guide", "Bengaluru, Hyderabad, Pune, Chennai, NCR, and the tier-2 case.", []),
    ("a_policy", "ART", 1, "State GCC policies compared", "Guide", "Side-by-side incentives; no ranking page has this table.", []),
    ("a_hro", "ART", 1, "What HR outsourcing is, and when it makes sense", "Guide", "Definition and benefits searches.", []),
    ("a_plan", "ART", 7, "Planned guides from buyer questions", "Guides", "Liaison vs branch vs subsidiary · back office in India · first 90 days after incorporation · transfer pricing for a GCC · STPI vs SEZ · fully loaded cost of a seat · closing an India subsidiary.", ["liaison office vs branch office vs subsidiary", "fema compliance checklist", "transfer pricing gcc india"]),
  ]},
"hcm": {
  "name": "Global HCM", "pillar": "HCM and HRMS software",
  "pillar_url": "/hcm-software/",
  "why": "The category where Paybooks' credentials are thinnest and competitor clusters are deepest (Keka 1,179 pages, greytHR list and alternatives hubs). Win with comparison, pricing and the India-plus-abroad angle.",
  "topics": [
    ("hub", "LP", 1, "HCM and HRMS software (pillar)", "/hcm-software/", "Product hub with module grid and FAQ.", []),
    ("payroll", "LP", 1, "Payroll software India", "/payroll-software/", "Feature page with the statutory list: PF, ESI, PT, LWF, TDS, Form 16.", []),
    ("attendance", "LP", 1, "Attendance management software", "/attendance-management-software/", "Module page mapped to the Paybooks product.", []),
    ("leave", "LP", 1, "Leave management software", "/leave-management-software/", "Module page mapped to the Paybooks product.", []),
    ("ess", "LP", 1, "Employee self-service portal", "/employee-self-service-portal/", "Paybooks' ESS page already draws brand traffic.", []),
    ("global", "LP", 1, "Global HR software", "/global-hr-software/", "India statutory plus multi-country employee records; the differentiator.", ["global hris for indian companies"]),
    ("segment", "LPS", 5, "Segment and industry pages", "/hr-software-for-[small-business | startups | healthcare | retail | enterprise]/", "greytHR and HROne own segment pages.", []),
    ("city", "LPS", 5, "City pages (optional)", "/hr-software-[city]/", "greytHR runs ten; lower priority.", []),
    ("compare", "LPS", 8, "Alternatives and compare pages", "/alternatives/[keka | greythr | zoho-people | darwinbox | razorpayx]/ · /compare/", "Keka and HROne publish against 25+ vendors.", ["keka alternatives", "greythr alternatives"]),
    ("tools", "TOOL", 5, "Free HR calculators", "/tools/", "In-hand salary, gratuity, HRA, TDS, leave encashment.", ["in hand salary calculator", "gratuity calculator"]),
    ("a_what", "ART", 1, "HCM vs HRIS vs HRMS for Indian employers", "Guide", "Definition intent with the India compliance angle.", []),
    ("a_best_hr", "ART", 1, "Best HRMS software in India", "Guide", "Refresh of the existing list, with method and a pricing table.", []),
    ("a_best_pay", "ART", 1, "Best payroll software in India", "Guide", "Including what to do when you also hire abroad.", []),
    ("a_price", "ART", 1, "HRMS software price in India", "Guide", "What you pay at 25, 50, 100 and 250 employees.", []),
    ("a_free", "ART", 1, "Free HRMS software: what the free plans leave out", "Guide", "Free and free-download searches.", []),
    ("a_choose", "ART", 1, "How to choose HRMS software: checklist and RFP questions", "Guide", "Features, demo questions, vendor evaluation.", []),
    ("a_plan", "ART", 8, "Planned guides from buyer questions", "Guides", "HRMS vs payroll software · implementation timeline · HR software vs Excel · DPDP Act for HR data · leave rules by state · 13 types of leave · Labour Codes for your HRMS · ESS consolidation.", ["hrms implementation timeline india", "dpdp act hr data"]),
  ]},
}

# ---------- off-intent rules (checked first) ----------
NOISE = {
"eor": [
  (r"^hire .*(developer|programmer|seo expert)|developers? in india", "Developer-staffing searches, not EOR buyers"),
  (r"\bior\b", "Importer of record, a different service"),
  (r"news", "News searches"),
],
"payroll": [
  (r"papaya|gusto|\bsap\b|brinker|celonis|mdaemon|timextender|zingtree|sophos|copado|caspio|kaseya|intuit|ukg|randstad|\bey\b", "Another vendor's brand name"),
  (r"market|news|target users", "Market-research or news searches"),
],
"india_office": [
  (r"gsk|jindal|bridgestone|adani|tata steel|maximus|mishcon|tw global|\bpma\b|transunion|digi key|reveleer|randstad|\bansr\b", "A named company's own GCC"),
  (r"hybe|xai|johnson|ge healthcare|subsidiary banks|foreign banks|first subsidiary alliance|clearwater|subsidiary companies in india|holding and subsidiary|holding company and subsidiary", "Company news or unrelated subsidiary searches"),
  (r"(seo|bpo|atm machine|cold storage|solar energy|export|import|ecommerce|online|crypto|travel agency|franchise) business|set up a small business|business to set up|best business|dubai from india|manufacturing subsidiary", "Starting an unrelated local business"),
  (r"jobs|upsc|kya|meaning in (tamil|malayalam|marathi|telugu|kannada)|scholarship|photos|reviews|hospitals|gst statutory|statutory audit|vietnam|philippines|europe", "Jobs, exam, translation or off-topic searches"),
  (r"news", "News searches"),
],
"hcm": [
  (r"^hrms$|nwkrtc|patna high court|jharkhand|^hrms pay slip|^hrms ess|^ess hrms|^hrms employee self service|^hrms leave management$|crew leave|ascent employee|liberty employee|randstad employee|lms nwkrtc", "Government or employer portal logins"),
  (r"project|school|student|download", "Student projects, schools and downloads"),
  (r"pagarbook|tuio|\bsap\b|ultimate software|news", "Another vendor's brand or news"),
],
}

COUNTRIES = r"philippines|france|uk\b|australia|china|canada|singapore|germany|netherlands|vietnam|uae|switzerland|mexico|poland|slovakia|brazil|turkey|thailand|czech|usa\b|portugal|luxembourg|south korea|guatemala|honduras|belgium|denmark|costa rica|middle east|\bgcc\b|mena|krakow"

def assign(cat, kw, ctry="us"):
    for pat, why in NOISE[cat]:
        if has(kw, pat): return ("__x", why)
    if cat == "eor":
        if has(kw, r"\bvs\b|versus"): return ("a_vsentity" if "entity" in kw else "a_vspeo", None)
        if has(kw, r"\bcost\b|much does"): return ("pricing", None)
        if has(kw, r"what is|what's an|meaning|pros and cons|how do .*work"): return ("a_what", None)
        if has(kw, r"startup|small business"): return ("segment", None)
        if has(kw, r"best way|best website|best platform|what's the best way"): return ("a_howto", None)
        if has(kw, r"best|top |most reliable|leading|which hr"): return ("a_best", None)
        if has(kw, COUNTRIES) and "india" not in kw: return ("country", None)
        if has(kw, r"^how|best way|can a foreign|through (an )?eor|website|platform"): return ("a_howto", None)
        if has(kw, r"hire|hiring|without"): return ("hire", None)
        if "india" in kw: return ("india", None)
        if has(kw, r"switch"): return ("a_vsentity", None)
        return ("hub", None)
    if cat == "payroll":
        if has(kw, r"\bvs\b|with a peo|peo payroll"): return ("a_vs", None)
        if has(kw, r"cost|price"): return ("a_cost", None)
        if has(kw, r"benefit|advantage|pros and cons|what is payroll outsourcing|payroll outsourcing meaning"): return ("a_why", None)
        if has(kw, r"simplest"): return ("a_run", None)
        if has(kw, r"what is|what’s|meaning"): return ("a_what", None) if has(kw, r"global|international|multi") else ("a_why", None)
        if has(kw, r"compliance|tax|fx|currency|challenge|how to|how do|centralize|integrate|simplest|data|reporting|process$|administration|managing|for international employees|remote international"):
            return ("a_run", None) if not has(kw, r"india|services$") else ("india", None)
        if has(kw, r"best|top|leading|recommended|reviewed|rated|reliable|expert reviews|evaluate"):
            return ("a_best_in", None) if ("india" in kw or has(kw, CITIES) or (ctry == "in" and not has(kw, r"global|international|multi"))) else ("a_best_gl", None)
        if has(kw, r"middle east|\bgcc\b|mena|dubai|uae|singapore|hong kong"): return ("country", None)
        if has(kw, CITIES): return ("city", None)
        if has(kw, r"managed|third party"): return ("managed", None)
        if has(kw, r"global|international|multi.?country|payroll global|payroll international"): return ("global", None)
        return ("india", None)
    if cat == "india_office":
        if "labour code" in kw:
            return ("a_labour", None) if has(kw, r"gratuity|leave|wages|basic salary") else ("labour_hub", None)
        if "shops" in kw: return ("a_se", None)
        if "statutory" in kw:
            if has(kw, r"services|outsourcing|management|software"): return ("stat", None)
            if has(kw, r"checklist|calendar|chart|tracker|documents|forms|list"): return ("tool_cal", None)
            if has(kw, r"meaning|what|means|why|definition"): return ("a_stat", None)
            return ("stat", None)
        if "hr " in kw + " " or "hr outsourcing" in kw or kw.startswith("outsourcing hr"):
            if has(kw, r"what is|meaning|benefits|in hrm"): return ("a_hro", None)
            return ("hro", None)
        if has(kw, r"gcc|global capability"):
            if has(kw, r"policy"): return ("a_policy", None)
            if has(kw, r"cost|seat|timeline"): return ("a_gcc_cost", None)
            if has(kw, r"\bvs\b|operating model|governance|challenges|benefits"): return ("a_gcc_model", None)
            if has(kw, CITIES): return ("a_gcc_city", None)
            if has(kw, r"set ?up|setting up|starting|launch|consult|partners|guide|services|platform|solutions"): return ("gcc", None)
            return ("a_gcc_what", None)
        if has(kw, r"subsidiary|incorporat|registration|set.?up|business in india"): return ("sub", None)
        return ("mio", None)
    if cat == "hcm":
        if has(kw, r"leading|what is the best"): return ("a_best_hr", None)
        if has(kw, r"features"): return ("a_choose", None)
        if has(kw, r"what is|meaning|examples"): return ("a_what", None)
        if has(kw, r"best|top|popular|list|underrated|highly rated|gartner|comparison|reviews|leading|user-friendly"):
            if "payroll" in kw: return ("a_best_pay", None)
            if has(kw, r"attendance"): return ("attendance", None)
            if has(kw, r"leave"): return ("leave", None)
            return ("a_best_hr", None)
        if has(kw, r"pricing|price|cost"): return ("a_price", None)
        if has(kw, r"\bfree\b"): return ("a_free", None)
        if has(kw, r"small business|startups|small companies|smes|medium|mid-market|enterprise|healthcare|retail"): return ("segment", None)
        if has(kw, CITIES): return ("city", None)
        if has(kw, r"features|demo|contract negotiation|vendors|providers|companies"): return ("a_choose", None)
        if "attendance" in kw: return ("attendance", None)
        if "leave" in kw: return ("leave", None)
        if has(kw, r"self service|self employee|\bess\b"): return ("ess", None)
        if "payroll" in kw: return ("payroll", None)
        return ("hub", None)

for r in clean:
    t, why = assign(r["category"], r["kw"], r["country"])
    r["topic"], r["why_x"] = t, why

# ---------- aggregate ----------
REPORT = ["eor"]  # this report covers the Employer of Record category only
def fmt(n): return f"{n:,}"
report = {}
for cat in ORDER:
    P = PLAN[cat]
    rs = [r for r in clean if r["category"] == cat]
    kept = [r for r in rs if r["topic"] != "__x"]
    excl = [r for r in rs if r["topic"] == "__x"]
    topics = []
    for tid, ttype, npages, title, url, note, planned in P["topics"]:
        ks = sorted([r for r in kept if r["topic"] == tid], key=lambda r: -r["vol"])
        topics.append(dict(id=tid, type=ttype, pages=npages, title=title, url=url, note=note, planned=planned, kws=ks,
                           vol=sum(r["vol"] for r in ks)))
    unassigned = [r for r in kept if r["topic"] not in {t["id"] for t in topics}]
    assert not unassigned, (cat, [r["kw"] for r in unassigned][:10])
    report[cat] = dict(P=P, all=rs, kept=kept, excl=sorted(excl, key=lambda r: -r["vol"]), topics=topics)

# ---------- CSV ----------
with open(os.path.join(OUT, "keyword-topic-map.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["bucket", "topic", "page_type", "target_page", "keyword", "country", "volume", "kd", "cpc_usd", "status"])
    TYPE = {"LP": "Landing page", "LPS": "Landing page set", "TOOL": "Tool", "ART": "Support article"}
    for cat in REPORT:
        R = report[cat]
        for t in R["topics"]:
            for r in t["kws"]:
                w.writerow([R["P"]["name"], t["title"], TYPE[t["type"]], t["url"], r["keyword"], r["country"].upper(), r["vol"], r["kd"], r["cpc_usd"], "targeted"])
        for r in R["excl"]:
            w.writerow([R["P"]["name"], "", "", "", r["keyword"], r["country"].upper(), r["vol"], r["kd"], r["cpc_usd"], "excluded: " + r["why_x"]])

json.dump({cat: {"kept": len(report[cat]["kept"]), "excluded": len(report[cat]["excl"]),
                 "kept_vol": sum(r["vol"] for r in report[cat]["kept"])} for cat in ORDER},
          open(os.path.join(OUT, "summary.json"), "w"), indent=1)

# ---------- HTML ----------
E = html.escape
TYPE_LABEL = {"LP": "Landing page", "LPS": "Landing page set", "TOOL": "Tool", "ART": "Support article"}
TYPE_CLS = {"LP": "lp", "LPS": "lp", "TOOL": "tool", "ART": "art"}

def kwtable(ks):
    if not ks: return '<p class="empty">No keyword in the Ahrefs pull yet. Target phrases below come from SERP and buyer-question research.</p>'
    rows_ = "".join(f'<tr><td>{E(r["keyword"])}</td><td>{r["country"].upper()}</td><td class="n">{fmt(r["vol"])}</td><td class="n">{"–" if r["kdn"] is None else int(r["kdn"])}</td><td class="n">{"–" if not r["cpcn"] else "$%.2f" % r["cpcn"]}</td></tr>' for r in ks)
    return f'<div class="tw"><table><thead><tr><th>Keyword</th><th>Market</th><th class="n">Volume / mo</th><th class="n">KD</th><th class="n">CPC</th></tr></thead><tbody>{rows_}</tbody></table></div>'

totals = dict(raw=RAW, exact=dups_exact, cross=dups_cross)
kept_all = sum(len(report[c]["kept"]) for c in REPORT)
excl_all = sum(len(report[c]["excl"]) for c in REPORT)
vol_all = sum(sum(r["vol"] for r in report[c]["kept"]) for c in REPORT)
raw_eor = len([r for r in rows if r["category"] == "eor"])
dup_eor = raw_eor - len(report["eor"]["all"])
pages = collections.Counter()
for c in REPORT:
    for t in report[c]["topics"]:
        pages[TYPE_CLS[t["type"]]] += t["pages"]

bucket_html = []
plan_rows = []
for i, cat in enumerate(REPORT, 1):
    R = report[cat]; P = R["P"]
    lp = sum(t["pages"] for t in R["topics"] if t["type"] in ("LP", "LPS"))
    tl = sum(t["pages"] for t in R["topics"] if t["type"] == "TOOL")
    ar = sum(t["pages"] for t in R["topics"] if t["type"] == "ART")
    kv = sum(r["vol"] for r in R["kept"])
    plan_rows.append(f'<tr><td><b>{E(P["name"])}</b></td><td>{E(P["pillar"])}<br><code>{E(P["pillar_url"])}</code></td><td class="n">{lp}</td><td class="n">{tl}</td><td class="n">{ar}</td><td class="n">{len(R["kept"])}</td><td class="n">{fmt(kv)}</td></tr>')
    topics_html = []
    for t in R["topics"]:
        planned = "".join(f"<li>{E(p)}</li>" for p in t["planned"])
        planned_html = f'<div class="planned"><b>Target phrases from research</b><ul>{planned}</ul></div>' if planned else ""
        cnt = f'{len(t["kws"])} keyword{"s" if len(t["kws"]) != 1 else ""} · {fmt(t["vol"])} / mo' if t["kws"] else "Planned from research"
        pg = f' · {t["pages"]} pages' if t["pages"] > 1 else ""
        topics_html.append(
            f'<details class="topic"><summary><span class="tag {TYPE_CLS[t["type"]]}">{TYPE_LABEL[t["type"]]}{pg}</span>'
            f'<span class="tt">{E(t["title"])}</span><span class="cnt">{cnt}</span></summary>'
            f'<div class="tbody"><p class="meta"><code>{E(t["url"])}</code> · {E(t["note"])}</p>{kwtable(t["kws"])}{planned_html}</div></details>')
    excl = R["excl"]
    reasons = collections.Counter(r["why_x"] for r in excl)
    excl_html = ""
    if excl:
        rs_ = "".join(f'<tr><td>{E(r["keyword"])}</td><td>{r["country"].upper()}</td><td class="n">{fmt(r["vol"])}</td><td>{E(r["why_x"])}</td></tr>' for r in excl)
        excl_html = (f'<details class="topic excl"><summary><span class="tag x">Excluded</span><span class="tt">Off-intent keywords removed from this bucket</span>'
                     f'<span class="cnt">{len(excl)} keywords</span></summary><div class="tbody"><p class="meta">'
                     + " · ".join(f"{E(k)}: {v}" for k, v in reasons.most_common()) +
                     f'</p><div class="tw"><table><thead><tr><th>Keyword</th><th>Market</th><th class="n">Volume / mo</th><th>Reason</th></tr></thead><tbody>{rs_}</tbody></table></div></div></details>')
    bucket_html.append(
        f'<details class="bucket" {"open" if i == 1 else ""}><summary><span class="bn">0{i}</span><span class="btitle">{E(P["name"])}</span>'
        f'<span class="bstats"><b>{len(R["kept"])}</b> keywords · <b>{fmt(kv)}</b> searches / mo · <b>{lp}</b> landing pages · <b>{tl}</b> tools · <b>{ar}</b> articles</span></summary>'
        f'<div class="bbody"><div class="pillar"><div><span class="lab">Main topic</span><b>{E(P["pillar"])}</b> <code>{E(P["pillar_url"])}</code></div><p>{E(P["why"])}</p></div>'
        + "".join(topics_html) + excl_html + '</div></details>')

COMP = [
 ("Employer of Record", [
   ("Wisemonk (DR 45)", "40+ India URLs: a service page for every commercial term, 10 tools, a blog for every objection. Outranks Deel, Remote and Multiplier on India cost and entity terms. The template to beat."),
   ("Skuad (DR 60)", "One 8,500-word India page with 24 question headings and 12 tables carries the cluster; thin support around it."),
   ("Deel (DR 81)", "One India landing page ($599), three India blogs, global calculators. No India cost page, no city or state pages."),
   ("Multiplier (DR 68) · Remote (DR 80)", "Templated country microsites and a 9,000-word country catalogue. No India cost or Labour Codes page."),
  ], ["Labour Codes for EOR buyers, state by state", "State compliance from the foreign employer's chair", "Cost shown in both USD and INR with the FX rate stated", "The EOR-to-entity move, step by step", "Questions the India hire asks about being on an EOR"]),
 ("Multi-Country Payroll", [
   ("ADP India (DR 91)", "The only big brand with India service pages ranking for the head term; three service tiers."),
   ("Deel · Remote · Papaya · Multiplier", "Country hubs, glossaries, compare hubs, calculators, RFP templates. All written for companies hiring into India."),
   ("Paysquare · Ascent HR", "Service, international country and city pages; Ascent adds a deep Labour Codes library."),
   ("Keka · greytHR · Zoho · RazorpayX", "Software clusters with free calculators, list and alternatives hubs; not managed payroll."),
  ], ["Payroll for Indian companies paying staff in UAE, US, UK, Singapore", "Shadow payroll for deputed staff", "One cost calculator reconciling India and global fees, FX and GST", "A Labour Codes CTC restructuring tool", "One statutory calendar across India and four countries"]),
 ("Managed India Office", [
   ("ANSR (DR 46)", "About 400 URLs: GCC glossary, service, BOT and EOR pages, city strategy. No cost page, no calculators."),
   ("Zinnov (DR 63)", "Location analysis and market sizing; owns \"which city\", not \"how much\" or \"how to\"."),
   ("India Briefing", "Encyclopaedic entity and HR reference; no pricing, no tools, dated formatting."),
   ("Wisemonk · Commenda", "The only pages that frame a single managed operating layer for an India office."),
  ], ["\"Managed India Office\" as a category", "GCC cost with a stated method", "State GCC policies side by side", "The first 90 days after incorporation", "Compliance reporting for the foreign parent"]),
 ("Global HCM", [
   ("Keka (DR 77)", "The most complete India HCM cluster: product, 400-term glossary, alternatives against 25+ vendors, compliance acts, calculators."),
   ("greytHR (DR 73)", "List hub, alternatives hub, pricing and ROI calculators, city pages, Middle East mirror."),
   ("HROne", "The most aggressive comparison publisher in India, plus Labour Codes content."),
   ("Darwinbox (DR 75) · Zoho (DR 92)", "Enterprise thought leadership, glossaries, module pages; few vs pages."),
  ], ["HCM vs HRIS vs HRMS from an India compliance view", "HR software for Indian companies with staff abroad", "Normalized cost per employee at 25, 50, 100, 250 people", "Implementation realism for Indian master data", "Leave rules by state as a real table"]),
]
comp_html = []
for name, rows_, gaps in [c for c in COMP if c[0] == "Employer of Record"]:
    who = "".join(f'<li><b>{E(a)}</b> {E(b)}</li>' for a, b in rows_)
    gp = "".join(f"<li>{E(g)}</li>" for g in gaps)
    comp_html.append(f'<details class="topic"><summary><span class="tt">{E(name)}</span><span class="cnt">{len(rows_)} competitor sets · {len(gaps)} gaps</span></summary>'
                     f'<div class="tbody cols"><div><h4>Who holds the SERP</h4><ul>{who}</ul></div><div><h4>Gaps nobody covers well</h4><ul>{gp}</ul></div></div></details>')

DR = [("rippling.com", 84), ("deel.com", 81), ("remote.com", 80), ("transperfect.com", 74), ("papayaglobal.com", 72), ("usemultiplier.com", 68),
      ("velocityglobal.com", 66), ("skuad.io", 60), ("playroll.com", 59), ("wisemonk.io", 45), ("paybooks.in", 41)]
dr_rows = "".join(f'<tr{" class=me" if d == "paybooks.in" else ""}><td>{d}</td><td class="n">{v}</td><td><i style="width:{v}%"></i></td></tr>' for d, v in DR)

HTML = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EOR Keyword Research</title><meta name="robots" content="noindex,nofollow">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--ink:#101828;--ink2:#344054;--muted:#667085;--line:#E4E9E1;--bg:#F6F8F3;--card:#fff;--green:#4F8A10;--g600:#3E6E0C;--g100:#E9F3DC;--forest:#0B1F14;--orange:#F26B1D;--o100:#FDEBDD}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Inter,system-ui,sans-serif}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 20px}}
header{{background:var(--forest);color:#fff;padding:44px 0 36px}}header h1{{font:700 36px/1.1 "Instrument Sans",sans-serif;margin:0 0 10px;letter-spacing:-.02em}}
header p{{color:#BFD3B9;margin:0;max-width:820px}}
.kpis{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:26px}}
.kpi{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:14px 16px}}
.kpi b{{display:block;font:700 26px "Instrument Sans";color:#9FD35C}}.kpi span{{font-size:12.5px;color:#BFD3B9}}
nav{{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid var(--line)}}nav .wrap{{display:flex;gap:4px;overflow:auto}}
nav a{{padding:14px 14px;color:var(--ink2);text-decoration:none;font-weight:600;font-size:14px;white-space:nowrap;border-bottom:2px solid transparent}}nav a:hover{{color:var(--g600);border-color:var(--green)}}
section{{padding:40px 0 8px}}h2{{font:700 26px "Instrument Sans";margin:0 0 6px;letter-spacing:-.01em}}.lead{{color:var(--muted);margin:0 0 18px;max-width:860px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px 22px}}
.funnel{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}.funnel div{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px}}
.funnel b{{display:block;font:700 22px "Instrument Sans"}}.funnel span{{font-size:13px;color:var(--muted)}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}th{{text-align:left;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:9px 10px;border-bottom:1px solid var(--line);background:#FAFBF8}}
td{{padding:8px 10px;border-bottom:1px solid #EEF1EC;vertical-align:top}}.n{{text-align:right;white-space:nowrap}}.tw{{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:#fff}}
code{{font-size:12.5px;background:#F2F5EE;border-radius:6px;padding:1px 6px;color:var(--g600)}}
details{{border-radius:16px}}summary{{cursor:pointer;list-style:none}}summary::-webkit-details-marker{{display:none}}
.bucket{{background:#fff;border:1px solid var(--line);margin:0 0 14px;box-shadow:0 10px 26px -22px rgba(16,40,20,.35)}}
.bucket>summary{{display:flex;align-items:center;gap:14px;padding:18px 22px;flex-wrap:wrap}}
.bucket>summary::after{{content:"+";margin-left:auto;font:600 22px Inter;color:var(--green)}}.bucket[open]>summary::after{{content:"−"}}
.bn{{font:700 13px "Instrument Sans";color:#fff;background:var(--green);border-radius:8px;padding:4px 8px}}.btitle{{font:700 20px "Instrument Sans"}}
.bstats{{font-size:13.5px;color:var(--muted)}}.bstats b{{color:var(--ink)}}
.bbody{{padding:0 22px 20px}}.pillar{{background:var(--g100);border-radius:12px;padding:14px 16px;margin-bottom:12px}}.pillar p{{margin:6px 0 0;color:var(--ink2);font-size:14px}}
.lab{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g600);font-weight:700;margin-right:8px}}
.topic{{border:1px solid var(--line);margin:8px 0;background:#FCFDFB}}.topic>summary{{display:flex;align-items:center;gap:12px;padding:12px 14px;flex-wrap:wrap}}
.topic>summary::before{{content:"›";font:700 18px Inter;color:var(--green);transition:transform .2s}}.topic[open]>summary::before{{transform:rotate(90deg)}}
.tt{{font-weight:600}}.cnt{{margin-left:auto;font-size:12.5px;color:var(--muted)}}
.tag{{font-size:11px;font-weight:700;letter-spacing:.04em;border-radius:999px;padding:3px 9px;white-space:nowrap}}.tag.lp{{background:var(--g100);color:var(--g600)}}.tag.art{{background:#EEF2FF;color:#3538CD}}.tag.tool{{background:var(--o100);color:#B54708}}.tag.x{{background:#F2F4F7;color:#475467}}
.tbody{{padding:0 14px 14px}}.meta{{font-size:13px;color:var(--ink2);margin:0 0 10px}}.empty{{font-size:13px;color:var(--muted);margin:0 0 8px}}
.planned{{margin-top:10px;font-size:13px}}.planned ul{{margin:6px 0 0;padding-left:18px;color:var(--ink2)}}
.cols{{display:grid;grid-template-columns:1.3fr 1fr;gap:18px}}.cols h4{{margin:4px 0 8px;font:700 14px "Instrument Sans"}}.cols ul{{margin:0;padding-left:18px}}.cols li{{margin:0 0 8px;font-size:13.5px;color:var(--ink2)}}
.dr i{{display:block;height:8px;border-radius:4px;background:#CFE3B5}}.dr tr.me td{{font-weight:700;color:var(--g600)}}.dr tr.me i{{background:var(--orange)}}
.note{{font-size:13px;color:var(--muted)}}a.dl{{display:inline-block;margin-top:10px;background:var(--forest);color:#fff;text-decoration:none;padding:10px 16px;border-radius:10px;font-weight:600;font-size:14px}}
footer{{padding:36px 0 50px;color:var(--muted);font-size:13px}}
@media(max-width:800px){{.kpis{{grid-template-columns:1fr 1fr}}.funnel{{grid-template-columns:1fr 1fr}}.cols{{grid-template-columns:1fr}}}}
</style></head><body>
<header><div class="wrap"><h1>Employer of Record: keyword, topic and competitor research</h1>
<p>Supporting research for the TransPerfect Paybooks SEO proposal, worked in full for one category as the model for the other three. Every Employer of Record keyword from the Ahrefs pull is placed in a topic, and each topic is a page to build: a landing page, a tool, or a support article.</p>
<div class="kpis"><div class="kpi"><b>{fmt(kept_all)}</b><span>keywords targeted</span></div><div class="kpi"><b>{fmt(vol_all)}</b><span>searches a month, US and India</span></div>
<div class="kpi"><b>{pages["lp"]}</b><span>landing pages, incl. page sets</span></div><div class="kpi"><b>{pages["tool"]}</b><span>interactive tools</span></div><div class="kpi"><b>{pages["art"]}</b><span>support articles</span></div></div></div></header>
<nav><div class="wrap"><a href="#method">Method</a><a href="#plan">Topic plan</a><a href="#buckets">Keywords by topic</a><a href="#competitors">Competitor analysis</a><a href="#download">Download</a></div></nav>
<main class="wrap">
<section id="method"><h2>How the keyword list was built</h2><p class="lead">Ahrefs Keywords Explorer, 23 September 2026. Five Employer of Record seed terms pulled for the US and India, then cleaned in three passes.</p>
<div class="funnel"><div><b>{fmt(raw_eor)}</b><span>Employer of Record keywords pulled from Ahrefs</span></div>
<div><b>−{excl_all}</b><span>off-intent keywords excluded, each with a reason: developer-staffing searches, news, and importer-of-record services</span></div>
<div><b>{fmt(kept_all)}</b><span>keywords targeted, each mapped to one page</span></div></div>
<p class="note" style="margin-top:12px">The deck quotes 161 Employer of Record keywords, the raw pull. This report removes duplicates and every off-intent keyword, so its targeted count is lower and exact. The same method applies to Multi-Country Payroll, Managed India Office and Global HCM. Keyword difficulty (KD) is Ahrefs' 0 to 100 score, and a dash means Ahrefs returned no value; "reachable" in the deck means KD 15 or under with 100+ searches a month.</p></section>
<section id="plan"><h2>Topic plan: what we build to own the category</h2><p class="lead">One main topic, with the landing pages, tools and support articles needed to dominate its search results. Page sets count every page they contain; for example, the 27 country pages count as 27.</p>
<div class="tw"><table><thead><tr><th>Category</th><th>Main topic and pillar page</th><th class="n">Landing pages</th><th class="n">Tools</th><th class="n">Support articles</th><th class="n">Keywords</th><th class="n">Searches / mo</th></tr></thead><tbody>{"".join(plan_rows)}
</tbody></table></div>
<p class="note" style="margin-top:10px">The 27 country pages are a wave-three option, only worth building once Paybooks can deliver EOR outside India. Without them, the plan is {pages["lp"] - 27} landing pages.</p></section>
<section id="buckets"><h2>Keywords by topic</h2><p class="lead">Open the category to see its topics. Open a topic to see the target page and every keyword it targets, sorted by monthly searches. Topics marked "planned from research" come from SERP and buyer-question research where Ahrefs returned no volume yet.</p>
{"".join(bucket_html)}</section>
<section id="competitors"><h2>Competitor analysis</h2><p class="lead">Ranking pages opened and measured for the EOR head queries, and competitor sitemaps mapped into India clusters.</p>
<div class="cols" style="grid-template-columns:1fr 1.4fr;align-items:start"><div class="card"><h4 style="margin:0 0 10px;font:700 15px 'Instrument Sans'">Domain Rating (Ahrefs)</h4><table class="dr"><tbody>{dr_rows}</tbody></table>
<p class="note">Depth beats authority on India terms: Wisemonk at DR 45 outranks Deel, Remote and Multiplier with a 40-URL India cluster. Authority decides only the global head terms.</p></div>
<div>{"".join(comp_html)}</div></div></section>
<section id="download"><h2>Download</h2><p class="lead">Every keyword with its bucket, topic, page type, target page, market, volume, KD and CPC, including excluded keywords and the reason.</p>
<a class="dl" href="keyword-topic-map.csv" download>Download keyword-topic-map.csv</a></section>
</main><footer class="wrap">Prepared by Mohan Kumar Allada for the TransPerfect Paybooks SEO proposal · Ahrefs data pulled 23 September 2026 · SERP research files in the proposal's research folder.</footer>
</body></html>'''
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(HTML)
print("raw", RAW, "exact", dups_exact, "cross", dups_cross, "kept", kept_all, "excluded", excl_all, "vol", vol_all, dict(pages))
for c in ORDER:
    R = report[c]
    print(c, "kept", len(R["kept"]), "excl", len(R["excl"]), [(t["id"], len(t["kws"])) for t in R["topics"]])
