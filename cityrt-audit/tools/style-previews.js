// Measure the published style preview art without logging in.
// Downloads the style WebPs the site registers, decodes them in Chrome
// (Node has no WebP decoder here), then measures palettes and tonal stats.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(
  process.env.PLAYWRIGHT_CORE ||
    'C:\\Users\\fauzi\\AppData\\Roaming\\npm\\node_modules\\rea-agents\\node_modules\\playwright-core',
);
const { extractPalette } = require('./analysis/palette.js');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ROOT = process.argv[2] || 'cityrt-audit';
const PUBLIC_DIR = path.join(ROOT, 'evidence', 'scripts', 'public');
const PREVIEW_DIR = path.join(ROOT, 'evidence', 'style-previews');
const PALETTE_DIR = path.join(ROOT, 'analysis', 'palette');

function styleMap() {
  const source = fs.readFileSync(path.join(PUBLIC_DIR, 'styles-DATr6XE2.js'), 'utf8');
  const map = new Map();
  for (const match of source.matchAll(/"\.\/(styles\/[a-z-]+\.webp)":`(\/assets\/[^`]+\.webp)`/g)) {
    map.set(match[1].replace(/^styles\//, '').replace(/\.webp$/, ''), match[2]);
  }
  return map;
}

async function main() {
  fs.mkdirSync(PREVIEW_DIR, { recursive: true });
  fs.mkdirSync(PALETTE_DIR, { recursive: true });
  const styles = styleMap();
  console.log('style previews registered:', styles.size);

  for (const [name, assetPath] of styles) {
    const file = path.join(PREVIEW_DIR, `${name}.webp`);
    if (!fs.existsSync(file)) {
      const res = await fetch('https://cityrt.com' + assetPath);
      if (!res.ok) {
        console.log(`${name}: HTTP ${res.status}`);
        continue;
      }
      fs.writeFileSync(file, Buffer.from(await res.arrayBuffer()));
    }
  }

  const browser = await chromium.launch({ executablePath: CHROME });
  const page = await browser.newPage();
  await page.goto('about:blank');
  const results = {};
  try {
    for (const [name] of styles) {
      const file = path.join(PREVIEW_DIR, `${name}.webp`);
      if (!fs.existsSync(file)) continue;
      const base64 = fs.readFileSync(file).toString('base64');
      const decoded = await page.evaluate(async (dataUrl) => {
        const image = new Image();
        await new Promise((resolve, reject) => {
          image.onload = resolve;
          image.onerror = () => reject(new Error('decode failed'));
          image.src = dataUrl;
        });
        const maxWidth = 320;
        const scale = Math.min(1, maxWidth / image.naturalWidth);
        const canvas = document.createElement('canvas');
        canvas.width = Math.max(1, Math.round(image.naturalWidth * scale));
        canvas.height = Math.max(1, Math.round(image.naturalHeight * scale));
        const ctx = canvas.getContext('2d');
        ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
        const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
        let binary = '';
        for (let i = 0; i < data.length; i += 1) binary += String.fromCharCode(data[i]);
        return {
          width: canvas.width,
          height: canvas.height,
          sourceWidth: image.naturalWidth,
          sourceHeight: image.naturalHeight,
          rgbaBase64: btoa(binary),
        };
      }, `data:image/webp;base64,${base64}`);

      const rgba = Buffer.from(decoded.rgbaBase64, 'base64');
      const image = { width: decoded.width, height: decoded.height, rgba: new Uint8Array(rgba) };
      const palette = extractPalette(image, { k: 6, iterations: 16 });
      results[name] = {
        style: name,
        previewBytes: fs.statSync(file).size,
        source: { width: decoded.sourceWidth, height: decoded.sourceHeight },
        sampled: { width: decoded.width, height: decoded.height },
        palette,
      };
      fs.writeFileSync(path.join(PALETTE_DIR, `${name}.json`), JSON.stringify(results[name], null, 2) + '\n');
      const top = palette.colors.slice(0, 3).map((c) => c.hex).join(' ');
      console.log(
        `${name.padEnd(14)} ${String(decoded.sourceWidth).padStart(5)}x${String(decoded.sourceHeight).padEnd(5)} luma=${palette.stats.meanLuma.toFixed(1).padStart(5)} sat=${palette.stats.meanSaturation.toFixed(2)} ${top}`,
      );
    }
  } finally {
    await browser.close();
  }
  fs.writeFileSync(
    path.join(PALETTE_DIR, 'previews-summary.json'),
    JSON.stringify({ generatedAt: new Date().toISOString(), styles: results }, null, 2) + '\n',
  );
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
