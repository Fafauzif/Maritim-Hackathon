// Reachability harness: classify what the page actually is (game / landing /
// challenge), keep a persistent profile so a human-cleared anti-bot pass is
// reused, and expose CDP so REA inspects the same session.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(
  process.env.PLAYWRIGHT_CORE ||
    'C:\\Users\\fauzi\\AppData\\Roaming\\npm\\node_modules\\rea-agents\\node_modules\\playwright-core',
);
const { installProbe, dumpProbe } = require('./probe.js');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const CHALLENGE_TEXT =
  /anti-bot|captcha|verify you are human|i am not a robot|проверка|капча|подтвердите/i;

async function classifyPage(page) {
  const url = page.url();
  const signals = await page
    .evaluate(() => {
      const canvas = document.querySelector('canvas');
      return {
        bodyText: document.body ? document.body.innerText.slice(0, 20000) : '',
        canvas: canvas ? { width: canvas.width, height: canvas.height } : null,
        drawCalls: window.__cityrtProbe ? window.__cityrtProbe.drawCalls : 0,
      };
    })
    .catch(() => ({ bodyText: '', canvas: null, drawCalls: 0 }));

  const live3d = !!signals.canvas && signals.canvas.width > 0 && signals.drawCalls >= 100;
  if (live3d) return 'game';
  const challenge = CHALLENGE_TEXT.test(signals.bodyText) || /\/pass(\/|\?|$)/i.test(url);
  if (challenge) return 'challenge';
  return 'landing';
}

async function openSession({ profileDir, harPath, headless = false, debugPort = 9222, url }) {
  if (harPath) fs.mkdirSync(path.dirname(harPath), { recursive: true });
  const context = await chromium.launchPersistentContext(profileDir, {
    executablePath: CHROME,
    headless,
    viewport: { width: 1440, height: 900 },
    recordHar: harPath ? { path: harPath, mode: 'full', content: 'embed' } : undefined,
    args: [
      `--remote-debugging-port=${debugPort}`,
      '--window-size=1440,900',
      '--disable-dev-shm-usage',
    ],
  });
  const page = context.pages()[0] || (await context.newPage());
  await installProbe(page);
  if (url) await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  return { context, page };
}

async function classifyLive({ url, profileDir, harPath, outDir, humanTimeoutMs = 300000 }) {
  fs.mkdirSync(outDir, { recursive: true });
  const { context, page } = await openSession({ profileDir, harPath, headless: false, url });
  try {
    console.log('waiting 8s for the page to settle...');
    await new Promise((resolve) => setTimeout(resolve, 8000));
    await page.waitForLoadState('domcontentloaded').catch(() => {});
    let classification = await classifyPage(page);
    console.log(`classification: ${classification}`);

    if (classification === 'challenge') {
      console.log(
        'CHALLENGE: complete the anti-bot pass in the visible Chrome window. Polling every 5s...',
      );
      const deadline = Date.now() + humanTimeoutMs;
      while (classification === 'challenge' && Date.now() < deadline) {
        await new Promise((resolve) => setTimeout(resolve, 5000));
        classification = await classifyPage(page);
      }
      console.log(`classification after wait: ${classification}`);
    }

    const probe = await dumpProbe(page).catch(() => null);
    await page.screenshot({ path: path.join(outDir, 'page.png'), fullPage: false }).catch(() => {});
    const report = {
      requestedUrl: url,
      finalUrl: page.url(),
      classification,
      title: await page.title().catch(() => null),
      probe: probe
        ? {
            renderer: probe.renderer,
            unmaskedRenderer: probe.unmaskedRenderer,
            drawCalls: probe.drawCalls,
            frames: probe.frames,
            canvas: probe.canvas,
            shaderCount: probe.shaders.length,
          }
        : null,
      capturedAt: new Date().toISOString(),
      cdpEndpoint: 'http://127.0.0.1:9222',
    };
    fs.writeFileSync(path.join(outDir, 'report.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify(report, null, 2));
    return { report, page, context };
  } catch (error) {
    await context.close().catch(() => {});
    throw error;
  }
}

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === '--open') out.url = argv[++i];
    else if (token === '--profile') out.profileDir = argv[++i];
    else if (token === '--har') out.harPath = argv[++i];
    else if (token === '--out') out.outDir = argv[++i];
    else if (token === '--hold') out.hold = true;
  }
  return out;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const result = await classifyLive({
    url: args.url || 'https://cityrt.com/en/',
    profileDir: args.profileDir || 'cityrt-audit/.profile',
    harPath: args.harPath || 'cityrt-audit/evidence/reachability/session.har',
    outDir: args.outDir || 'cityrt-audit/evidence/reachability',
  });
  console.log('browser held open for REA/CDP use; close the window to exit.');
  process.on('SIGINT', async () => {
    await result.context.close().catch(() => {});
    process.exit(0);
  });
}

module.exports = { classifyPage, openSession, classifyLive, CHROME };

if (require.main === module) {
  main().catch((error) => {
    console.error(error);
    process.exit(1);
  });
}
