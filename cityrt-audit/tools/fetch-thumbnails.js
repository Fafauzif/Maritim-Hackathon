const fs = require('node:fs');
const path = require('node:path');
const catalog = JSON.parse(fs.readFileSync('cityrt-audit/evidence/catalog/catalog.json', 'utf8').replace(/^\uFEFF/, ''));
const outDir = 'cityrt-audit/evidence/catalog/img';
fs.mkdirSync(outDir, { recursive: true });
const queue = catalog.map((b) => b.name);
let ok = 0, skipped = 0, failed = [];
async function worker() {
  while (queue.length) {
    const name = queue.shift();
    const file = path.join(outDir, name + '.webp');
    if (fs.existsSync(file) && fs.statSync(file).size > 500) { skipped += 1; continue; }
    try {
      const res = await fetch('https://cityrt.com/cat/img/' + encodeURIComponent(name) + '.webp');
      if (!res.ok) { failed.push([name, res.status]); continue; }
      fs.writeFileSync(file, Buffer.from(await res.arrayBuffer()));
      ok += 1;
    } catch (e) { failed.push([name, e.message]); }
    await new Promise((r) => setTimeout(r, 60));
  }
}
(async () => {
  const workers = Array.from({ length: 6 }, () => worker());
  const started = Date.now();
  await Promise.all(workers);
  fs.writeFileSync('cityrt-audit/evidence/catalog/download-report.json', JSON.stringify({ total: catalog.length, ok, skipped, failed }, null, 1));
  console.log(`total=${catalog.length} downloaded=${ok} skipped=${skipped} failed=${failed.length} in ${Math.round((Date.now() - started) / 1000)}s`);
  if (failed.length) console.log('first failures', JSON.stringify(failed.slice(0, 5)));
})();

