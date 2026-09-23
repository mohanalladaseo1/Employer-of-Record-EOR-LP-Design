# Paybooks EOR inventory decisions + comparison layer, consumed by build_ceo.py
import json
PG = json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "paybooks_eor_pages.json")))
def W(p): return PG.get("https://paybooks.in" + p, {}).get("words", 0)
def T(p): return PG.get("https://paybooks.in" + p, {}).get("tables", 0)
# (current url, verdict, becomes, reason)
INV = [
 ("/eor/", "Refresh", "EOR India commercial page", "The service page. Holds all 265 internal links but shows no price, no tables, and 1,697 words against Skuad's 8,658. Rebuilt as the sample page; its URL redirects into the new one."),
 ("/eor-2/", "Redirect", "EOR India commercial page", "A 479-word duplicate of /eor/ competing with it. Redirect and remove."),
 ("/article/featured-article/how-to-hire-employees-in-india-without-setting-up-a-company-2026-eor-guide/", "Refresh", "Hire employees in India guide", "The strongest existing asset: 5,210 words, 6 tables, FAQ. Retarget to the hiring searches Papaya and Rippling win."),
 ("/article/15-top-companies-for-eor-in-india-2025-paybooks/", "Refresh", "Best EOR providers for India", "The only EOR page that ranks today (#8 India, \"eor solutions\"). Dated 2025, no tables, no prices. Update to 2026 with a price table and a stated method."),
 ("/article/eor-vs-subsidiary-vs-peo-in-india-which-structure-is-right-in-2026/", "Refresh", "PEO in India vs EOR", "Already compares the models with 7 tables. Refocus on the PEO searches Deel ranks #1 for."),
 ("/article/employer-of-record-eor-guide-2026-costs-risks-use-cases/", "Refresh", "What is an EOR (glossary)", "6,836 generic global words. Cut to a short, answer-first definition that AI Overviews can quote."),
 ("/article/eor-india-compliance-checklist/", "Refresh", "Employer guide: India compliance checklist", "Good depth (3,055 words, 11 tables). Add FAQ, dates and a link to the commercial page."),
 ("/article/top-mistakes-global-companies-make-when-hiring-in-india/", "Refresh", "Employer guide: hiring mistakes to avoid", "20 tables of useful detail. Keep, tighten, and link it into the hiring guide."),
 ("/article/what-does-an-eor-in-india-actually-cost/", "Merge", "EOR India commercial page, pricing section", "Cost searches return the same pages as the head term, so cost belongs on the commercial page. Move its 7 tables there and redirect."),
 ("/article/employer-of-record-vs-local-entity-vs-freelancers-global-hiring-guide-2026/", "Merge", "Hire employees in India guide", "Its three-routes comparison is the core of the hiring guide. Move the tables in and redirect."),
 ("/article/employer-of-record-in-india-fast-compliant-expansion-for-startups/", "Merge", "EOR India commercial page", "One of three near-identical startup articles splitting the same intent. Fold the best section in and redirect."),
 ("/article/why-global-tech-startups-are-using-employer-of-record-india-in-2026/", "Merge", "EOR India commercial page", "Same startup intent as the article above. Redirect."),
 ("/article/why-employer-of-record-eor-are-services-an-ideal-option-for-startup-expansion/", "Merge", "EOR India commercial page", "2024 article on the same startup intent, 1,417 words. Redirect."),
 ("/article/what-is-employer-of-record-eor-services-how-can-it-help-you/", "Merge", "What is an EOR (glossary)", "2024 definition article that duplicates the 2026 guide. Redirect."),
]
# existing payroll articles repurposed for EOR buyers
REUSE = [
 ("/article/labour-code-implementation-in-india/", "Refresh", "Employer guide: Labour Codes for foreign employers", "Paybooks already covers the Labour Codes for Indian HR. Rewrite the angle for a foreign employer; nobody ranks with that angle."),
 ("/article/how-the-maternity-benefit-act-impacts-employers-and-employees-in-india/", "Refresh", "Employer guide: maternity and leave rules", "Maternity leave in India gets about 200 searches a month; Rippling ranks for it. Retarget for foreign employers."),
 ("/article/how-to-handle-gratuity-bonus-and-ff-settlement-without-getting-it-wrong/", "Refresh", "Employer guide: termination and final settlement", "Termination is a top buyer question. Reuse this gratuity and final-pay content for foreign employers."),
]
# new pages
NEW = [
 ("Comparison", "Deel alternatives for hiring in India", "/compare/deel-alternatives/", "deel alternatives · deel competitors", 700),
 ("Comparison", "Paybooks vs Deel", "/compare/paybooks-vs-deel/", "deel pricing · deel india", 540),
 ("Comparison", "Remote alternatives for hiring in India", "/compare/remote-alternatives/", "remote alternatives · remote.com alternatives · remote pricing", 670),
 ("Comparison", "Deel vs Remote vs Rippling for India hiring", "/compare/deel-vs-remote-vs-rippling/", "deel vs rippling · deel vs remote · remote vs deel · deel vs multiplier", 1350),
 ("Comparison", "EOR pricing compared: Deel, Remote, Multiplier, Skuad, Paybooks", "/compare/eor-pricing/", "eor pricing comparison · multiplier pricing · cheapest eor", 130),
 ("Tool", "India employee cost calculator", "/tools/india-employee-cost-calculator/", "built into the sample page", 0),
 ("Tool", "EOR vs own-entity calculator", "/tools/eor-vs-entity-calculator/", "entity vs eor india", 30),
 ("Role pages", "Hire software developers in India (+4 more roles)", "/hire-[role]-in-india/", "hire developers in india and 46 role searches", 6700),
 ("Employer guides", "Employee benefits in India", "/guides/employee-benefits-india/", "india benefits · employee benefits in india", 280),
 ("Employer guides", "Background checks in India", "/guides/background-checks-india/", "india background check · background check in india", 190),
 ("Employer guides", "Contractors vs employees in India", "/guides/contractors-vs-employees-india/", "hiring independent contractors in india", 100),
 ("Employer guides", "Permanent establishment risk in India", "/guides/permanent-establishment-risk-india/", "buyer-question research", 0),
 ("Employer guides", "Moving from an EOR to your own entity", "/guides/eor-to-own-entity/", "buyer-question research", 0),
]
COMPARE_COUNTS = [("Multiplier", 172), ("Asanify", 95), ("Deel", 108), ("Skuad", 118), ("Wisemonk", 114), ("Rippling", 76), ("G-P", 136), ("Paybooks", 1)]
COMPARE_DEMAND = sum(v for t, _n, _u, _k, v in NEW if t == "Comparison")
