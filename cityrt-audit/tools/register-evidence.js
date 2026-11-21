const fs = require('node:fs');
const path = require('node:path');
const { addEvidence, writeManifest } = require('./manifest.js');
const root = 'cityrt-audit';
function walk(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out;
}
for (const dir of ['evidence/scripts/public', 'evidence/style-previews', 'analysis/palette', 'analysis/styles', 'analysis/skins-static.json']) {
  const target = path.join(root, dir);
  if (!fs.existsSync(target)) continue;
  const files = fs.statSync(target).isDirectory() ? walk(target) : [target];
  for (const file of files) {
    addEvidence({ root, path: file, kind: 'derived-evidence', producedBy: 'public-crawl', proves: 'CityRT public client data' });
  }
}
const written = writeManifest(root);
const manifest = JSON.parse(fs.readFileSync(written, 'utf8'));
console.log('manifest entries:', manifest.entries.length);

