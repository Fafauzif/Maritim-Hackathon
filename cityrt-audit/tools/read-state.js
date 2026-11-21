// Read the current CityRT error/state page: text, buttons, and any error code.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(
  process.env.PLAYWRIGHT_CORE ||
    'C:\\Users\\fauzi\\AppData\\Roaming\\npm\\node_modules\\rea-agents\\node_modules\\playwright-core',
);

const ROOT = process.argv[2] || 'cityrt-audit';
const OUT = path.join(ROOT, 'evidence', 'live');

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const pages = browser.contexts().flatMap((context) => context.pages());
  const results = [];
  for (const page of pages) {
    const state = await page.evaluate(() => ({
      url: location.href,
      title: document.title,
      text: document.body ? document.body.innerText.replace(/\s+/g, ' ').slice(0, 1200) : '',
      buttons: [...document.querySelectorAll('button, a')]
        .map((element) => ({ tag: element.tagName.toLowerCase(), text: (element.innerText || '').trim().slice(0, 60), href: element.getAttribute('href') || null }))
        .filter((entry) => entry.text)
        .slice(0, 25),
    })).catch((error) => ({ error: error.message }));
    results.push(state);
    const safe = page.url().replace(/[^a-z0-9]+/gi, '-').slice(0, 40);
    await page.screenshot({ path: path.join(OUT, `error-${safe}.png`) }).catch(() => {});
  }
  fs.writeFileSync(path.join(OUT, 'error-state.json'), JSON.stringify(results, null, 2) + '\n');
  console.log(JSON.stringify(results, null, 1).slice(0, 2500));
  await browser.close().catch(() => {});
}

main().catch((error) => {
  console.error('STATE FAILED:', error.message);
  process.exit(1);
});
