// Wait for the city generation to finish, then capture the loaded 3D view and
// any 3D asset requests observed while it settles.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(
  process.env.PLAYWRIGHT_CORE ||
    'C:\\Users\\fauzi\\AppData\\Roaming\\npm\\node_modules\\rea-agents\\node_modules\\playwright-core',
);

const ROOT = process.argv[2] || 'cityrt-audit';
const OUT = path.join(ROOT, 'evidence', 'live');
fs.mkdirSync(OUT, { recursive: true });

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const pages = browser.contexts().flatMap((context) => context.pages());
  const page = pages.find((candidate) => /cityrt\.com\/play/.test(candidate.url())) || pages[0];
  if (!page) throw new Error('no CityRT page');

  const assets = [];
  page.on('response', (response) => {
    try {
      const url = response.url();
      if (/\.(glb|gltf|ktx2|bin|wasm)$/i.test(new URL(url).pathname)) {
        assets.push({ url, status: response.status(), contentType: response.headers()['content-type'] || null });
      }
    } catch (error) {
      /* ignore */
    }
  });

  const deadline = Date.now() + 240000;
  let lastText = '';
  while (Date.now() < deadline) {
    const state = await page.evaluate(() => ({
      text: document.body ? document.body.innerText.replace(/\s+/g, ' ').slice(0, 200) : '',
      canvases: [...document.querySelectorAll('canvas')].map((canvas) => ({ id: canvas.id, width: canvas.width, height: canvas.height })),
    })).catch(() => null);
    if (state) {
      if (state.text !== lastText) {
        console.log(new Date().toISOString().slice(11, 19), state.text.slice(0, 120));
        lastText = state.text;
      }
      const loading = /Placing|Laying out|planting|painting|carving|\d+%/.test(state.text) && !/budget|population|power/i.test(state.text);
      if (!loading && state.canvases.length >= 1) {
        console.log('generation appears complete');
        break;
      }
    }
    await new Promise((resolve) => setTimeout(resolve, 4000));
  }

  await new Promise((resolve) => setTimeout(resolve, 4000));
  const finalState = await page.evaluate(() => {
    const canvas = document.querySelector('canvas#view');
    return {
      url: location.href,
      canvases: [...document.querySelectorAll('canvas')].map((entry) => ({ id: entry.id, width: entry.width, height: entry.height })),
      canvasSize: canvas ? { width: canvas.width, height: canvas.height } : null,
      bodyText: document.body ? document.body.innerText.replace(/\s+/g, ' ').slice(0, 600) : '',
    };
  });
  await page.screenshot({ path: path.join(OUT, 'city-loaded.png') });
  fs.writeFileSync(path.join(OUT, 'city-state.json'), JSON.stringify({ finalState, assets }, null, 1) + '\n');
  console.log('FINAL', JSON.stringify(finalState, null, 1).slice(0, 1200));
  console.log('3d assets seen:', assets.length);
  await browser.close().catch(() => {});
}

main().catch((error) => {
  console.error('WAIT FAILED:', error.message);
  process.exit(1);
});
