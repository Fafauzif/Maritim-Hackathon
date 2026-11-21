const fs = require('node:fs');
const path = require('node:path');
const outDir = process.argv[2];
const loader = fs.readFileSync(path.join(outDir, 'index-BOyK8tfh.js'), 'utf8');
const names = [...new Set([...loader.matchAll(/assets\/[A-Za-z0-9_\-.]+\.(?:js|css)/g)].map((m) => m[0]))];
console.log('assets referenced:', names.length);
(async () => {
  const results = [];
  for (const name of names) {
    const url = 'https://cityrt.com/' + name;
    const file = path.join(outDir, path.basename(name));
    if (fs.existsSync(file) && fs.statSync(file).size > 0) { results.push([name, fs.statSync(file).size, 'cached']); continue; }
    try {
      const res = await fetch(url);
      if (!res.ok) { results.push([name, 0, 'HTTP ' + res.status]); continue; }
      const buf = Buffer.from(await res.arrayBuffer());
      fs.writeFileSync(file, buf);
      results.push([name, buf.length, 'ok']);
    } catch (e) { results.push([name, 0, 'ERR ' + e.message]); }
  }
  for (const [name, size, status] of results) console.log(String(size).padStart(9), status.padEnd(10), name);
  fs.writeFileSync(path.join(outDir, 'download-report.json'), JSON.stringify(results, null, 1));
})();
