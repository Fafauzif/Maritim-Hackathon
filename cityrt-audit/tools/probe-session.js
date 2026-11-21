const { chromium } = require(process.env.PLAYWRIGHT_CORE);
(async () => {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const pages = browser.contexts().flatMap((c) => c.pages());
  const page = pages.find((p) => /cityrt\.com\/play/.test(p.url())) || pages[0];
  const result = await page.evaluate(async () => {
    const out = { me: null, asset: null, cookies: document.cookie.slice(0, 200) };
    try {
      const me = await fetch('/api/me', { credentials: 'same-origin' });
      out.me = { status: me.status, body: (await me.text()).slice(0, 300) };
    } catch (e) { out.me = { error: e.message }; }
    try {
      const asset = await fetch('/play/assets/index-DkWGfb4u.js', { credentials: 'same-origin' });
      out.asset = { status: asset.status, length: (await asset.text()).length };
    } catch (e) { out.asset = { error: e.message }; }
    return out;
  });
  console.log(JSON.stringify(result, null, 1));
  await browser.close().catch(() => {});
})();
