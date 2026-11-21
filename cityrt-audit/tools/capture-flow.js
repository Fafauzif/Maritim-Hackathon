// Full live capture flow: focus the window, install hooks before the document loads,
// enter the city, and capture renderer/shader/draw-call evidence once it renders.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(
  process.env.PLAYWRIGHT_CORE ||
    'C:\\Users\\fauzi\\AppData\\Roaming\\npm\\node_modules\\rea-agents\\node_modules\\playwright-core',
);
const { installInPage, dumpProbe } = require('./browser/probe.js');

const ROOT = process.argv[2] || 'cityrt-audit';
const OUT = path.join(ROOT, 'evidence', 'live');
fs.mkdirSync(OUT, { recursive: true });

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const pages = browser.contexts().flatMap((context) => context.pages());
  const page = pages.find((candidate) => /cityrt\.com/.test(candidate.url())) || pages[0];
  if (!page) throw new Error('no CityRT page');

  await page.bringToFront();
  await page.addInitScript(installInPage);
  console.log('hooks registered for next document; reloading');
  await page.reload({ waitUntil: 'domcontentloaded', timeout: 120000 });
  await page.bringToFront();
  await new Promise((resolve) => setTimeout(resolve, 6000));

  const playButton = page.locator('button.mn-btn.primary.go').first();
  if ((await playButton.count()) === 0) {
    console.log('no Play button; current state:', await page.evaluate(() => document.body.innerText.replace(/\s+/g, ' ').slice(0, 200)));
  } else {
    await playButton.click();
    console.log('clicked Play');
  }

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

  const deadline = Date.now() + 300000;
  let snapshot = null;
  let lastLog = '';
  while (Date.now() < deadline) {
    const state = await page.evaluate(() => {
      const probe = window.__cityrtProbe || null;
      return {
        text: document.body ? document.body.innerText.replace(/\s+/g, ' ').slice(0, 260) : '',
        canvas: document.querySelector('canvas#view') ? document.querySelector('canvas#view').width : null,
        probe: probe ? { drawCalls: probe.drawCalls, frames: probe.frames, shaders: probe.shaders.length, renderer: probe.renderer } : null,
      };
    }).catch(() => null);
    if (state) {
      const progress = (state.text.match(/(\d+)%/) || [])[1] || '-';
      const log = `${progress}% canvas=${state.canvas} draws=${state.probe ? state.probe.drawCalls : 'n/a'} shaders=${state.probe ? state.probe.shaders.length : 'n/a'}`;
      if (log !== lastLog) {
        console.log(new Date().toISOString().slice(11, 19), log);
        lastLog = log;
      }
      snapshot = state;
      if (state.canvas && state.probe && state.probe.drawCalls > 50) {
        console.log('rendering detected');
        break;
      }
      if (state.canvas && /HUD|budget|population/i.test(state.text) && state.probe && state.probe.drawCalls > 0) break;
    }
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }

  await new Promise((resolve) => setTimeout(resolve, 6000));
  const probe = await dumpProbe(page).catch(() => null);
  await page.screenshot({ path: path.join(OUT, 'city-3d.png') });
  const payload = { snapshot, probe: probe ? { renderer: probe.renderer, unmaskedRenderer: probe.unmaskedRenderer, drawCalls: probe.drawCalls, frames: probe.frames, canvas: probe.canvas, shaderCount: probe.shaders.length } : null, assets };
  fs.writeFileSync(path.join(OUT, 'capture-flow.json'), JSON.stringify(payload, null, 1) + '\n');
  if (probe && probe.shaders.length) {
    fs.writeFileSync(
      path.join(OUT, 'game-shaders.json'),
      JSON.stringify(probe.shaders.map((shader) => ({ hash: shader.hash, vertexLength: shader.vertex.length, fragmentLength: shader.fragment.length, vertex: shader.vertex, fragment: shader.fragment })), null, 1) + '\n',
    );
  }
  console.log('RESULT', JSON.stringify(payload.probe, null, 1));
  console.log('text:', snapshot ? snapshot.text.slice(0, 200) : null);
  await browser.close().catch(() => {});
}

main().catch((error) => {
  console.error('FLOW FAILED:', error.message);
  process.exit(1);
});
