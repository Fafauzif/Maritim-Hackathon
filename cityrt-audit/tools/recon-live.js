// Recon the signed-in CityRT game page: where the canvas lives, what it loads.
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
  const contexts = browser.contexts();
  const pages = contexts.flatMap((context) => context.pages());
  const page = pages.find((candidate) => /cityrt\.com\/play/.test(candidate.url())) || pages[0];
  if (!page) throw new Error('no CityRT page');

  const responses = [];
  page.on('response', async (response) => {
    try {
      const request = response.request();
      const type = request.resourceType();
      const headers = response.headers();
      const entry = {
        url: response.url(),
        status: response.status(),
        type,
        contentType: headers['content-type'] || null,
        contentLength: Number(headers['content-length'] || 0),
      };
      if (/\.(glb|gltf|ktx2|bin|wasm|dr[ac]co)$/i.test(new URL(response.url()).pathname)) {
        entry.interesting = true;
      }
      responses.push(entry);
    } catch (error) {
      /* ignore */
    }
  });

  console.log('reloading to observe network...');
  await page.reload({ waitUntil: 'domcontentloaded', timeout: 120000 });
  await new Promise((resolve) => setTimeout(resolve, 15000));

  const dom = await page.evaluate(() => {
    const shadow = [];
    const walk = (root, depth) => {
      for (const element of root.querySelectorAll('*')) {
        if (element.shadowRoot) {
          shadow.push({ tag: element.tagName.toLowerCase(), id: element.id, children: element.shadowRoot.querySelectorAll('*').length });
          walk(element.shadowRoot, depth + 1);
        }
      }
    };
    walk(document, 0);
    const canvases = [...document.querySelectorAll('canvas')].map((canvas) => ({
      width: canvas.width,
      height: canvas.height,
      clientWidth: canvas.clientWidth,
      id: canvas.id,
      className: canvas.className,
      parent: canvas.parentElement ? canvas.parentElement.tagName.toLowerCase() : null,
    }));
    const iframes = [...document.querySelectorAll('iframe')].map((frame) => ({ src: frame.src, id: frame.id, className: frame.className }));
    const buttons = [...document.querySelectorAll('button, [role="button"], a')]
      .map((element) => ({ tag: element.tagName.toLowerCase(), text: (element.innerText || '').trim().slice(0, 60), className: element.className }))
      .filter((entry) => entry.text)
      .slice(0, 40);
    return {
      url: location.href,
      title: document.title,
      bodyClass: document.body ? document.body.className : null,
      canvases,
      iframes,
      shadowRoots: shadow,
      buttons,
      bodyText: document.body ? document.body.innerText.replace(/\s+/g, ' ').slice(0, 900) : '',
    };
  });

  fs.writeFileSync(path.join(OUT, 'dom.json'), JSON.stringify(dom, null, 2) + '\n');
  fs.writeFileSync(path.join(OUT, 'network.json'), JSON.stringify(responses, null, 1) + '\n');
  await page.screenshot({ path: path.join(OUT, 'live-view-2.png') });

  const byType = {};
  const byHost = {};
  for (const entry of responses) {
    byType[entry.type] = (byType[entry.type] || 0) + 1;
    try { const host = new URL(entry.url).host; byHost[host] = (byHost[host] || 0) + 1; } catch (error) { /* ignore */ }
  }
  console.log('DOM', JSON.stringify({ url: dom.url, bodyClass: dom.bodyClass, canvases: dom.canvases, iframes: dom.iframes, shadow: dom.shadowRoots }, null, 1));
  console.log('buttons', JSON.stringify(dom.buttons.slice(0, 15)));
  console.log('bodyText', dom.bodyText.slice(0, 300));
  console.log('responses', responses.length, 'byType', JSON.stringify(byType), 'hosts', JSON.stringify(byHost));
  const interesting = responses.filter((entry) => entry.interesting);
  console.log('3d asset responses', interesting.length, JSON.stringify(interesting.slice(0, 10)));
  await browser.close().catch(() => {});
}

main().catch((error) => {
  console.error('RECON FAILED:', error.message);
  process.exit(1);
});
