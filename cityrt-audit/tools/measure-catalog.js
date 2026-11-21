// Measure every published building thumbnail without letting the cream vignette
// dominate: model the radial background, mask it out, then measure the building
// pixels only (palette, tonal stats, silhouette box).
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(
  process.env.PLAYWRIGHT_CORE ||
    'C:\\Users\\fauzi\\AppData\\Roaming\\npm\\node_modules\\rea-agents\\node_modules\\playwright-core',
);
const { extractPalette } = require('./analysis/palette.js');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ROOT = process.argv[2] || 'cityrt-audit';
const BATCH = 24;
const TARGET_WIDTH = 300;
const BG_TOLERANCE = 14;

const catalog = JSON.parse(
  fs.readFileSync(path.join(ROOT, 'evidence', 'catalog', 'catalog.json'), 'utf8').replace(/^\uFEFF/, ''),
);
const imgDir = path.join(ROOT, 'evidence', 'catalog', 'img');
const outDir = path.join(ROOT, 'analysis', 'catalog');
fs.mkdirSync(outDir, { recursive: true });

const present = new Set(fs.readdirSync(imgDir).filter((f) => f.endsWith('.webp')).map((f) => f.replace(/\.webp$/, '')));
const entries = catalog.filter((b) => present.has(b.name));

// Background is a smooth cream vignette. Flood fill from every border pixel,
// accepting a neighbour within a small local colour step, so the fill follows the
// vignette but stops at building silhouettes. Building pixels are the remainder.
function buildingMask(width, height, rgba) {
  const visited = new Uint8Array(width * height);
  const queue = [];
  const index = (x, y) => y * width + x;
  const push = (x, y) => {
    if (x < 0 || y < 0 || x >= width || y >= height) return;
    const i = index(x, y);
    if (visited[i]) return;
    visited[i] = 1;
    queue.push(i);
  };
  for (let x = 0; x < width; x += 1) { push(x, 0); push(x, height - 1); }
  for (let y = 0; y < height; y += 1) { push(0, y); push(width - 1, y); }

  const STEP = 9;
  let head = 0;
  while (head < queue.length) {
    const current = queue[head];
    head += 1;
    const x = current % width;
    const y = (current - x) / width;
    const base = current * 4;
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = x + dx;
      const ny = y + dy;
      if (nx < 0 || ny < 0 || nx >= width || ny >= height) continue;
      const next = index(nx, ny);
      if (visited[next]) continue;
      const candidate = next * 4;
      const delta = Math.abs(rgba[base] - rgba[candidate]) + Math.abs(rgba[base + 1] - rgba[candidate + 1]) + Math.abs(rgba[base + 2] - rgba[candidate + 2]);
      if (delta <= STEP) {
        visited[next] = 1;
        queue.push(next);
      }
    }
  }

  let minX = width, minY = height, maxX = -1, maxY = -1, kept = 0;
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      if (visited[index(x, y)]) continue;
      kept += 1;
      if (x < minX) minX = x;
      if (x > maxX) maxX = x;
      if (y < minY) minY = y;
      if (y > maxY) maxY = y;
    }
  }
  return { mask: visited, kept, bbox: maxX >= 0 ? { minX, minY, maxX, maxY } : null };
}
async function main() {
  console.log('thumbnails present:', entries.length);
  const browser = await chromium.launch({ executablePath: CHROME });
  const page = await browser.newPage();
  await page.goto('about:blank');
  const results = [];
  try {
    for (let start = 0; start < entries.length; start += BATCH) {
      const batch = entries.slice(start, start + BATCH);
      const payload = batch.map((entry) => ({
        name: entry.name,
        dataUrl: 'data:image/webp;base64,' + fs.readFileSync(path.join(imgDir, entry.name + '.webp')).toString('base64'),
      }));
      const decoded = await page.evaluate(async (items) => {
        const out = [];
        for (const item of items) {
          try {
            const image = new Image();
            await new Promise((resolve, reject) => {
              image.onload = resolve;
              image.onerror = () => reject(new Error('decode failed'));
              image.src = item.dataUrl;
            });
            const scale = Math.min(1, 300 / image.naturalWidth);
            const canvas = document.createElement('canvas');
            canvas.width = Math.max(1, Math.round(image.naturalWidth * scale));
            canvas.height = Math.max(1, Math.round(image.naturalHeight * scale));
            const ctx = canvas.getContext('2d');
            ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
            const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
            let binary = '';
            for (let i = 0; i < data.length; i += 1) binary += String.fromCharCode(data[i]);
            out.push({ name: item.name, width: canvas.width, height: canvas.height, rgba: btoa(binary) });
          } catch (error) {
            out.push({ name: item.name, error: error.message });
          }
        }
        return out;
      }, payload);

      for (const item of decoded) {
        if (item.error) { results.push({ name: item.name, error: item.error }); continue; }
        const rgba = new Uint8Array(Buffer.from(item.rgba, 'base64'));
        const { mask, kept, bbox } = buildingMask(item.width, item.height, rgba);
        if (!kept || !bbox) { results.push({ name: item.name, error: 'no building pixels' }); continue; }

        // Palette over building pixels only.
        const pixels = new Uint8Array(kept * 4);
        let cursor = 0;
        for (let index = 0; index < mask.length; index += 1) {
          if (mask[index]) continue;
          pixels[cursor] = rgba[index * 4];
          pixels[cursor + 1] = rgba[index * 4 + 1];
          pixels[cursor + 2] = rgba[index * 4 + 2];
          pixels[cursor + 3] = 255;
          cursor += 4;
        }
        const palette = extractPalette({ width: kept, height: 1, rgba: pixels }, { k: 5, iterations: 12, step: 1 });
        const meta = catalog.find((b) => b.name === item.name) || {};
        const boxWidth = bbox.maxX - bbox.minX + 1;
        const boxHeight = bbox.maxY - bbox.minY + 1;
        results.push({
          name: item.name,
          style: meta.style,
          cat: meta.cat,
          title: meta.title,
          coverage: Number((kept / mask.length).toFixed(3)),
          silhouetteAspect: Number((boxWidth / boxHeight).toFixed(3)),
          footprintInFrame: Number((boxWidth / item.width).toFixed(3)),
          palette: palette.colors.map((c) => c.hex),
          stats: palette.stats,
        });
      }
      if (start % 240 === 0) console.log('processed', start + batch.length);
    }
  } finally {
    await browser.close();
  }

  fs.writeFileSync(path.join(outDir, 'building-palettes.json'), JSON.stringify(results, null, 1) + '\n');

  const ok = results.filter((r) => !r.error);
  const aggregate = (key) => {
    const buckets = {};
    for (const item of ok) {
      const value = item[key];
      if (!value) continue;
      buckets[value] = buckets[value] || { count: 0, luma: 0, saturation: 0, coverage: 0, aspect: 0, colors: new Map() };
      const bucket = buckets[value];
      bucket.count += 1;
      bucket.luma += item.stats.meanLuma;
      bucket.saturation += item.stats.meanSaturation;
      bucket.coverage += item.coverage;
      bucket.aspect += item.silhouetteAspect;
      for (const hex of item.palette) bucket.colors.set(hex, (bucket.colors.get(hex) || 0) + 1);
    }
    return Object.fromEntries(
      Object.entries(buckets).map(([value, bucket]) => [
        value,
        {
          count: bucket.count,
          meanLuma: Number((bucket.luma / bucket.count).toFixed(1)),
          meanSaturation: Number((bucket.saturation / bucket.count).toFixed(2)),
          meanCoverage: Number((bucket.coverage / bucket.count).toFixed(3)),
          meanSilhouetteAspect: Number((bucket.aspect / bucket.count).toFixed(2)),
          topColors: [...bucket.colors.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10).map(([hex, count]) => ({ hex, count })),
        },
      ]),
    );
  };

  const summary = {
    generatedAt: new Date().toISOString(),
    method:
      'WebP decoded in Chrome at 300px wide; radially symmetric background modelled from outer 38% of pixels and masked at RGB distance >14; 5-colour k-means over building pixels only',
    counts: { catalog: catalog.length, measured: ok.length, failed: results.length - ok.length },
    byStyle: aggregate('style'),
    byCategory: aggregate('cat'),
  };
  fs.writeFileSync(path.join(outDir, 'catalog-summary.json'), JSON.stringify(summary, null, 2) + '\n');
  console.log('measured', ok.length, 'buildings; failed', results.length - ok.length);
  for (const [styleKey, value] of Object.entries(summary.byStyle)) {
    console.log(
      `  ${styleKey.padEnd(13)} n=${String(value.count).padStart(3)} luma=${String(value.meanLuma).padStart(5)} sat=${value.meanSaturation} aspect=${value.meanSilhouetteAspect} top=${value.topColors.slice(0, 4).map((c) => c.hex).join(' ')}`,
    );
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});

