// Fetch the lazily-loaded client chunks (city/simulation/geometry/render modules)
// from the authenticated page context.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(
  process.env.PLAYWRIGHT_CORE ||
    'C:\\Users\\fauzi\\AppData\\Roaming\\npm\\node_modules\\rea-agents\\node_modules\\playwright-core',
);

const ROOT = process.argv[2] || 'cityrt-audit';
const OUT = path.join(ROOT, 'evidence', 'game-bundles');
fs.mkdirSync(OUT, { recursive: true });
const list = fs
  .readFileSync(path.join(ROOT, 'evidence', 'live', 'missing-chunks.txt'), 'utf8')
  .split('\n')
  .map((line) => line.trim())
  .filter(Boolean);

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const pages = browser.contexts().flatMap((context) => context.pages());
  const page = pages.find((candidate) => /cityrt\.com/.test(candidate.url())) || pages[0];
  if (!page) throw new Error('no CityRT page');

  let ok = 0;
  const failed = [];
  for (const name of list) {
    const url = `https://cityrt.com/play/assets/${name}.js`;
    const file = path.join(OUT, `${name}.js`);
    if (fs.existsSync(file) && fs.statSync(file).size > 0) { ok += 1; continue; }
    try {
      const result = await page.evaluate(async (target) => {
        const response = await fetch(target, { credentials: 'same-origin' });
        if (!response.ok) return { error: 'HTTP ' + response.status };
        return { text: await response.text() };
      }, url);
      if (result.error) { failed.push({ name, error: result.error }); continue; }
      fs.writeFileSync(file, result.text);
      ok += 1;
    } catch (error) {
      failed.push({ name, error: error.message });
    }
  }
  fs.writeFileSync(path.join(OUT, 'missing-download-report.json'), JSON.stringify({ total: list.length, ok, failed }, null, 2) + '\n');
  console.log(`fetched ${ok}/${list.length} extra chunks; failed ${failed.length}`);
  if (failed.length) console.log(JSON.stringify(failed.slice(0, 8), null, 1));
  await browser.close().catch(() => {});
}

main().catch((error) => {
  console.error('FETCH FAILED:', error.message);
  process.exit(1);
});
