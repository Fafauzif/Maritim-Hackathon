// Enter the city from the menu with the WebGL probe already installed, then capture
// renderer identity, shader sources, draw calls and a screenshot.
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
  const contexts = browser.contexts();
  const pages = contexts.flatMap((context) => context.pages());
  const page = pages.find((candidate) => /cityrt\.com\/play/.test(candidate.url())) || pages[0];
  if (!page) throw new Error('no CityRT page');

  const assets = [];
  page.on('response', (response) => {
    const url = response.url();
    if (/\.(glb|gltf|ktx2|bin|wasm|json)$/i.test(new URL(url).pathname)) {
      assets.push({ url, status: response.status(), type: response.request().resourceType() });
    }
  });

  // Install hooks into the live page before the game creates its WebGL context.
  await page.evaluate(installInPage);
  console.log('probe injected into live page');

  const playButton = page.locator('button.mn-btn.primary.go').first();
  const hasPlay = (await playButton.count()) > 0;
  console.log('play button present:', hasPlay);
  if (hasPlay) await playButton.click();
  await new Promise((resolve) => setTimeout(resolve, 12000));

  const midState = await page.evaluate(() => {
    const canvases = [...document.querySelectorAll('canvas')].map((canvas) => ({ width: canvas.width, height: canvas.height, id: canvas.id, className: canvas.className }));
    return {
      url: location.href,
      canvases,
      probe: window.__cityrtProbe
        ? { drawCalls: window.__cityrtProbe.drawCalls, frames: window.__cityrtProbe.frames, shaders: window.__cityrtProbe.shaders.length }
        : null,
      bodyText: document.body ? document.body.innerText.replace(/\s+/g, ' ').slice(0, 400) : '',
      buttons: [...document.querySelectorAll('button')].map((b) => (b.innerText || '').trim().slice(0, 40)).filter(Boolean).slice(0, 20),
    };
  });
  console.log('STATE', JSON.stringify(midState, null, 1));

  const probe = await dumpProbe(page).catch(() => null);
  if (probe) {
    console.log(
      'PROBE',
      JSON.stringify(
        {
          renderer: probe.renderer,
          unmaskedRenderer: probe.unmaskedRenderer,
          drawCalls: probe.drawCalls,
          frames: probe.frames,
          shaderCount: probe.shaders.length,
          canvas: probe.canvas,
        },
        null,
        1,
      ),
    );
    fs.writeFileSync(path.join(OUT, 'game-probe.json'), JSON.stringify({ midState, probe }, null, 1) + '\n');
    if (probe.shaders.length) {
      fs.writeFileSync(
        path.join(OUT, 'game-shaders.json'),
        JSON.stringify(
          probe.shaders.map((shader) => ({ hash: shader.hash, vertexLength: shader.vertex.length, fragmentLength: shader.fragment.length, vertex: shader.vertex, fragment: shader.fragment })),
          null,
          1,
        ) + '\n',
      );
    }
  }
  await page.screenshot({ path: path.join(OUT, 'game-view.png') });
  fs.writeFileSync(path.join(OUT, 'game-assets.json'), JSON.stringify(assets, null, 1) + '\n');
  console.log('asset-like responses during entry:', assets.length, JSON.stringify(assets.slice(0, 8)));
  await browser.close().catch(() => {});
}

main().catch((error) => {
  console.error('ENTER FAILED:', error.message);
  process.exit(1);
});
