// Password gate for the whole site (Vercel Routing Middleware, runs before every request).
// Only a salted PBKDF2 hash of the password is stored here, never the password itself.
export const config = { matcher: '/:path*' };

const SALT = '2454a1b8e5f2e12c77d7199446f592c1';
const ITER = 150000;
const HASH = 'b757aff1a61bd0cadd61194ff167758c93ef72ace34dbb6b071257455bed980c';
const TOKEN = '3977826b07fca6ea50997dbfb3955c54656bbe05a20c756d2814ae6eb7eecac7';
const COOKIE = 'pb_gate';

const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
const bytes = (h) => new Uint8Array(h.match(/.{2}/g).map((x) => parseInt(x, 16)));

async function derive(pw) {
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(pw), 'PBKDF2', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt: bytes(SALT), iterations: ITER }, key, 256);
  return hex(bits);
}

function safeNext(n) {
  return typeof n === 'string' && n.startsWith('/') && !n.startsWith('//') ? n : '/';
}

function page(next, failed) {
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Private proposal</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{min-height:100vh;display:grid;place-items:center;padding:24px 16px;background:#0B1F14;background-image:radial-gradient(60% 50% at 80% 0%,rgba(159,211,92,.18),transparent 70%),linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:auto,48px 48px,48px 48px;font-family:Inter,system-ui,sans-serif;color:#F2F1EC}
.card{width:100%;max-width:420px;background:#12281B;border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:36px 32px;box-shadow:0 30px 80px -30px rgba(0,0,0,.7)}
.tag{display:inline-block;font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#C5F04A;border:1px solid rgba(197,240,74,.35);border-radius:999px;padding:6px 12px;margin-bottom:18px}
h1{font-family:'Instrument Sans',Inter,sans-serif;font-weight:600;font-size:30px;line-height:1.1;letter-spacing:-.02em;margin-bottom:10px}
p{font-size:15px;line-height:1.55;color:#B9C8BD;margin-bottom:22px}
label{display:block;font-size:13px;font-weight:600;color:#DDE6DF;margin-bottom:8px}
input{width:100%;height:48px;border-radius:12px;border:1px solid rgba(255,255,255,.16);background:#0B1F14;color:#F2F1EC;font:500 16px Inter,sans-serif;padding:0 14px;outline:none}
input:focus{border-color:#9FD35C;box-shadow:0 0 0 3px rgba(159,211,92,.2)}
button{margin-top:14px;width:100%;height:48px;border:0;border-radius:12px;background:#F26B1D;color:#fff;font:600 16px Inter,sans-serif;cursor:pointer}
button:hover{background:#E05E12}
.err{margin-top:12px;font-size:14px;color:#FFB08A}
</style></head><body><main class="card">
<span class="tag">Private proposal</span>
<h1>TransPerfect Paybooks SEO proposal</h1>
<p>This proposal is shared privately. Enter the password to continue.</p>
<form method="POST" action="/__auth"><input type="hidden" name="next" value="${next.replace(/"/g, '&quot;')}">
<label for="pw">Password</label><input id="pw" name="password" type="password" autocomplete="current-password" required autofocus>
<button type="submit">View proposal</button>${failed ? '<div class="err">That password is not right. Try again.</div>' : ''}</form>
</main></body></html>`;
  return new Response(html, {
    status: 401,
    headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'x-robots-tag': 'noindex, nofollow' },
  });
}

export default async function middleware(request) {
  const url = new URL(request.url);
  const cookie = request.headers.get('cookie') || '';
  const m = cookie.match(new RegExp('(?:^|;\\s*)' + COOKIE + '=([a-f0-9]{64})'));
  if (m && m[1] === TOKEN) {
    return new Response(null, { headers: { 'x-middleware-next': '1' } });
  }
  if (url.pathname === '/__auth' && request.method === 'POST') {
    const form = await request.formData();
    const next = safeNext(form.get('next'));
    if ((await derive(String(form.get('password') || ''))) === HASH) {
      return new Response(null, {
        status: 303,
        headers: {
          location: next,
          'set-cookie': `${COOKIE}=${TOKEN}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=2592000`,
          'cache-control': 'no-store',
        },
      });
    }
    return page(next, true);
  }
  return page(safeNext(url.pathname + url.search), false);
}
