// Attach to the signed-in CityRT page over CDP, inspect what is actually running,
// then reload with the WebGL probe installed and capture renderer + shader evidence.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(
  process.env.PLAYWRIGHT_CORE ||
    'C:\\Users\\fauzi\\AppData\\Roaming\\npm\\node_modules\\rea-agents\\node_modules\\playwright-core',
);
const { installProbe, dumpProbe } = require('./browser/probe.js');

const ROOT = process.argv[2] || 'cityrt-audit';
const OUT = path.join(ROOT, 'evidence', 'live');
fs.mkdirSync(OUT, { recursive: true });

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const contexts = browser.contexts();
  const pages = contexts.flatMap((context) => context.pages());
  const page = pages.find((candidate) => /cityrt\.com/.test(candidate.url())) || pages[0];
  if (!page) throw new Error('no CityRT page found over CDP');

  const before = await page.evaluate(() => {
    const canvas = document.querySelector('canvas');
    return {
      url: location.href,
      title: document.title,
      canvas: canvas ? { width: canvas.width, height: canvas.height, clientWidth: canvas.clientWidth } : null,
      hasWebgl2: !!document.createElement('canvas').getContext('webgl2'),
      bodyClasses: document.body ? document.body.className : null,
    };
  });
  console.log('BEFORE', JSON.stringify(before));

  await installProbe(page);
  console.log('probe installed; reloading page');
  await page.reload({ waitUntil: 'domcontentloaded', timeout: 120000 });
  await new Promise((resolve) => setTimeout(resolve, 12000));

  const after = await page.evaluate(() => {
    const canvas = document.querySelector('canvas');
    return {
      url: location.href,
      title: document.title,
      canvas: canvas ? { width: canvas.width, height: canvas.height } : null,
      probe: window.__cityrtProbe
        ? { drawCalls: window.__cityrtProbe.drawCalls, frames: window.__cityrtProbe.frames, shaders: window.__cityrtProbe.shaders.length, renderer: window.__cityrtProbe.renderer }
        : null,
    };
  });
  console.log('AFTER', JSON.stringify(after));

  const probe = await dumpProbe(page);
  fs.writeFileSync(path.join(OUT, 'probe.json'), JSON.stringify({ before, after, probe }, null, 1) + '\n');
  await page.screenshot({ path: path.join(OUT, 'live-view.png') });
  console.log(
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
  fs.writeFileSync(
    path.join(OUT, 'shaders.json'),
    JSON.stringify(
      probe.shaders.map((shader) => ({ hash: shader.hash, vertexLength: shader.vertex.length, fragmentLength: shader.fragment.length, vertex: shader.vertex, fragment: shader.fragment })),
      null,
      1,
    ) + '\n',
  );
  await browser.close().catch(() => {});
}

main().catch((error) => {
  console.error('CAPTURE FAILED:', error.message);
  process.exit(1);
});
