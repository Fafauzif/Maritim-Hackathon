// Download the authenticated game client bundles from the live page context.
// The page can fetch /play/assets/*.js (200) while an anonymous client gets 404.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(
  process.env.PLAYWRIGHT_CORE ||
    'C:\\Users\\fauzi\\AppData\\Roaming\\npm\\node_modules\\rea-agents\\node_modules\\playwright-core',
);

const ROOT = process.argv[2] || 'cityrt-audit';
const OUT = path.join(ROOT, 'evidence', 'game-bundles');
fs.mkdirSync(OUT, { recursive: true });

const urls = fs
  .readFileSync(path.join(ROOT, 'evidence', 'live', 'script-urls.txt'), 'utf8')
  .split('\n')
  .map((line) => line.trim())
  .filter(Boolean);

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const pages = browser.contexts().flatMap((context) => context.pages());
  const page = pages.find((candidate) => /cityrt\.com/.test(candidate.url())) || pages[0];
  if (!page) throw new Error('no CityRT page');

  let ok = 0;
  let failed = [];
  let totalBytes = 0;
  for (const url of urls) {
    const name = path.basename(new URL(url).pathname);
    const file = path.join(OUT, name);
    if (fs.existsSync(file) && fs.statSync(file).size > 0) {
      ok += 1;
      continue;
    }
    try {
      const base64 = await page.evaluate(async (target) => {
        const response = await fetch(target, { credentials: 'same-origin' });
        if (!response.ok) return { error: 'HTTP ' + response.status };
        const buffer = new Uint8Array(await response.arrayBuffer());
        let binary = '';
        const chunk = 0x8000;
        for (let i = 0; i < buffer.length; i += chunk) {
          binary += String.fromCharCode.apply(null, buffer.subarray(i, i + chunk));
        }
        return { data: btoa(binary) };
      }, url);
      if (base64.error) {
        failed.push({ url, error: base64.error });
        continue;
      }
      const bytes = Buffer.from(base64.data, 'base64');
      fs.writeFileSync(file, bytes);
      totalBytes += bytes.length;
      ok += 1;
    } catch (error) {
      failed.push({ url, error: error.message });
    }
  }
  fs.writeFileSync(path.join(OUT, 'download-report.json'), JSON.stringify({ total: urls.length, ok, failed, totalBytes }, null, 2) + '\n');
  console.log(`downloaded ${ok}/${urls.length} bundles, ${(totalBytes / 1024 / 1024).toFixed(2)} MB, failed ${failed.length}`);
  if (failed.length) console.log(JSON.stringify(failed.slice(0, 5)));
  await browser.close().catch(() => {});
}

main().catch((error) => {
  console.error('DOWNLOAD FAILED:', error.message);
  process.exit(1);
});
