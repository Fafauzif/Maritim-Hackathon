const { chromium } = require(process.env.PLAYWRIGHT_CORE);
(async () => {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const contexts = browser.contexts();
  const pages = contexts.flatMap((c) => c.pages());
  for (const page of pages) {
    const info = await page.evaluate(() => ({
      url: location.href,
      title: document.title,
      text: document.body ? document.body.innerText.replace(/\s+/g, ' ').slice(0, 1200) : '',
      cookiesEnabled: navigator.cookieEnabled,
    })).catch((e) => ({ error: e.message }));
    console.log(JSON.stringify(info, null, 1));
  }
  await browser.close().catch(() => {});
})();
