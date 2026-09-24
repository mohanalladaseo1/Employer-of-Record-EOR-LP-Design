# Builds /deck/: the pitch deck as slide images (no selectable text) with clickable link areas.
# Slide images are rendered at 1920x1080 from the deck source; links are measured in the same render.
import json
W, H = 1920, 1080
TITLES = ["Dominate SERPs for 4 categories", "Where Paybooks stands", "The prize", "Category 1 research",
          "Diagnosis", "Category 1 strategy", "Proof of work", "Scope and ongoing support", "Deliverables and timeline",
          "Who you get", "Track record", "In their words", "Quotation", "Next step"]
S = "https://employer-of-record-eor-lp-design-livid.vercel.app/"
LINKS = {
    4: [(S + "strategy/", [[642, 988, 662, 27]])],
    5: [("https://paybooks.in/article/employer-of-record-in-india-fast-compliant-expansion-for-startups/", [[887, 456, 477, 28]]),
        ("https://paybooks.in/article/why-global-tech-startups-are-using-employer-of-record-india-in-2026/", [[1437, 456, 333, 28], [878, 491, 275, 28]]),
        ("https://paybooks.in/eor/", [[878, 580, 183, 28]]),
        ("https://paybooks.in/eor-2/", [[1117, 580, 206, 28]]),
        ("https://paybooks.in/article/what-does-an-eor-in-india-actually-cost/", [[887, 828, 385, 28]])],
    7: [(S + "strategy/", [[169, 697, 241, 27]]), (S, [[733, 649, 197, 27]]), (S + "employer-of-record/india/", [[1297, 686, 205, 27]])],
    10: [("https://www.linkedin.com/in/mohankumarallada/", [[252, 988, 400, 27]])],
    12: [("https://www.linkedin.com/in/mohankumarallada/", [[392, 988, 99, 27]])],
    14: [("https://www.linkedin.com/in/mohankumarallada/", [[1325, 920, 467, 31]])],
}

def pct(v, t): return f"{v / t * 100:.3f}%"

slides = ""
for i in range(1, 15):
    hot = ""
    for href, rects in LINKS.get(i, []):
        for x, y, w, h in rects:
            pad = 6
            hot += (f'<a class="hot" href="{href}" target="_blank" rel="noopener" aria-label="Open link" '
                    f'style="left:{pct(x - pad, W)};top:{pct(y - pad, H)};width:{pct(w + 2 * pad, W)};height:{pct(h + 2 * pad, H)}"></a>')
    load = 'eager' if i <= 2 else 'lazy'
    slides += (f'<figure class="slide{" on" if i == 1 else ""}" data-i="{i}" aria-label="Slide {i}: {TITLES[i - 1]}">'
               f'<img src="slides/slide-{i:02d}.jpg" width="{W}" height="{H}" alt="Slide {i}: {TITLES[i - 1]}" loading="{load}" draggable="false">{hot}</figure>')

dots = "".join(f'<button class="dot{" on" if i == 1 else ""}" data-go="{i}" aria-label="Go to slide {i}"></button>' for i in range(1, 15))

page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paybooks SEO Pitch</title><meta name="robots" content="noindex,nofollow">
<meta name="description" content="Scope and pitch: SEO for the new paybooks.in across four categories.">
<link rel="icon" href="../assets/mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#0B0F0D;--panel:#141A17;--line:#26302B;--ink:#F2F1EC;--mute:#8A958E;--lime:#C5F04A}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif}
body{display:flex;flex-direction:column;min-height:100vh}
.top{display:flex;align-items:center;justify-content:space-between;padding:14px 24px;border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:10px;font-weight:600;font-size:15px}
.brand img{width:28px;height:28px;border-radius:8px}
.brand small{color:var(--mute);font-weight:500}
.links{display:flex;gap:6px;flex-wrap:wrap}
.links a{color:var(--ink);text-decoration:none;font-size:13px;font-weight:500;padding:7px 12px;border:1px solid var(--line);border-radius:999px}
.links a:hover{border-color:var(--lime);color:var(--lime)}
.stage{flex:1;display:flex;align-items:center;justify-content:center;padding:24px;min-height:0}
.frame{position:relative;width:min(100%, calc((100vh - 170px) * 16 / 9));aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#000;box-shadow:0 30px 80px -30px rgba(0,0,0,.8),0 0 0 1px var(--line)}
.slide{position:absolute;inset:0;opacity:0;visibility:hidden;transition:opacity .35s ease,visibility .35s}
.slide.on{opacity:1;visibility:visible}
.slide img{display:block;width:100%;height:100%;pointer-events:none}
.hot{position:absolute;border-radius:6px;transition:background .15s}
.hot:hover{background:rgba(197,240,74,.18)}
.bar{display:flex;align-items:center;justify-content:center;gap:18px;padding:0 24px 22px}
.nav{width:42px;height:42px;border-radius:50%;border:1px solid var(--line);background:var(--panel);color:var(--ink);font-size:18px;cursor:pointer;display:grid;place-items:center}
.nav:hover{border-color:var(--lime);color:var(--lime)}
.nav:disabled{opacity:.35;cursor:default;border-color:var(--line);color:var(--ink)}
.dots{display:flex;gap:6px}
.dot{width:8px;height:8px;border-radius:999px;border:0;background:#3A4540;cursor:pointer;transition:width .25s,background .25s}
.dot.on{width:26px;background:var(--lime)}
.count{font-size:13px;color:var(--mute);min-width:52px;text-align:center;font-variant-numeric:tabular-nums}
.fs{font-size:13px;font-weight:500}
.tip{display:none;text-align:center;color:var(--mute);font-size:12.5px;padding:10px 16px 0}
@media (max-width:700px){.top{flex-direction:column;gap:10px;padding:12px 16px}.stage{padding:16px}.frame{width:100%;border-radius:10px}.dots{display:none}.bar{padding:0 16px 18px}}
/* Phone, upright: every slide stacked at full width */
@media (max-width:700px) and (orientation:portrait){.stage{display:block;padding:16px}.frame{aspect-ratio:auto;background:none;box-shadow:none;overflow:visible;border-radius:0}.slide{position:relative;inset:auto;opacity:1;visibility:visible;margin-bottom:14px;border-radius:10px;overflow:hidden;box-shadow:0 0 0 1px var(--line)}.slide img{height:auto}.bar{display:none}.tip{display:block}}
/* Phone, sideways: the slide fills the screen; tap or swipe to move */
@media (max-height:520px) and (orientation:landscape){.top,.bar{display:none}.stage{padding:0}.frame{width:min(100vw,calc(100vh * 16 / 9));border-radius:0;box-shadow:none}}
</style></head><body>
<header class="top"><div class="brand"><img src="../assets/mark.png" alt="">Paybooks SEO pitch <small>· September 2026</small></div>
<nav class="links"><a href="../strategy/">Category 1 research</a><a href="../">Landing page</a><a href="../employer-of-record/india/">EOR India guide</a></nav></header>
<p class="tip">Turn your phone sideways for a larger view.</p><main class="stage"><div class="frame" id="frame">''' + slides + '''</div></main>
<div class="bar"><button class="nav" id="prev" aria-label="Previous slide">&#8592;</button><div class="dots">''' + dots + '''</div>
<span class="count" id="count">1 / 14</span><button class="nav" id="next" aria-label="Next slide">&#8594;</button>
<button class="nav fs" id="fs" aria-label="Full screen" title="Full screen">&#x26F6;</button></div>
<script>
(function(){var s=[].slice.call(document.querySelectorAll('.slide')),d=[].slice.call(document.querySelectorAll('.dot')),n=s.length,c=0,
cnt=document.getElementById('count'),pv=document.getElementById('prev'),nx=document.getElementById('next'),fr=document.getElementById('frame');
function go(i){c=Math.max(0,Math.min(n-1,i));s.forEach(function(e,k){e.classList.toggle('on',k===c)});d.forEach(function(e,k){e.classList.toggle('on',k===c)});
cnt.textContent=(c+1)+' / '+n;pv.disabled=c===0;nx.disabled=c===n-1;var im=s[Math.min(n-1,c+1)].querySelector('img');im.loading='eager';
try{history.replaceState(null,'','#'+(c+1))}catch(e){}}
pv.onclick=function(){go(c-1)};nx.onclick=function(){go(c+1)};
d.forEach(function(e){e.onclick=function(){go(+e.dataset.go-1)}});
document.addEventListener('keydown',function(e){if(['ArrowRight','PageDown',' '].indexOf(e.key)>-1){e.preventDefault();go(c+1)}
else if(['ArrowLeft','PageUp'].indexOf(e.key)>-1){e.preventDefault();go(c-1)}else if(e.key==='Home')go(0);else if(e.key==='End')go(n-1)});
fr.addEventListener('click',function(e){if(e.target.closest('.hot'))return;var r=fr.getBoundingClientRect();go(e.clientX-r.left<r.width/3?c-1:c+1)});
var x0=null;fr.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
fr.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)go(dx<0?c+1:c-1);x0=null});
document.getElementById('fs').onclick=function(){var el=document.documentElement;if(!document.fullscreenElement){(el.requestFullscreen||el.webkitRequestFullscreen).call(el)}else{document.exitFullscreen()}};
var h=parseInt(location.hash.slice(1),10);go(h>0?h-1:0)})();
</script>
<script src="../assets/protect.js" defer></script></body></html>'''
open("index.html", "w", encoding="utf-8").write(page)
print(len(page))
