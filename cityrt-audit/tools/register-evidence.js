// Register every audit artefact in evidence/manifest.json by SHA-256.
const fs = require('node:fs');
const path = require('node:path');
const { addEvidence, writeManifest } = require('./manifest.js');

const root = process.argv[2] || 'cityrt-audit';
const dirs = [
  'evidence/installer',
  'evidence/pages',
  'evidence/catalog',
  'evidence/reachability',
  'evidence/scripts',
  'evidence/style-previews',
  'analysis',
  'docs',
];

function walk(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out;
}

let count = 0;
for (const dir of dirs) {
  const target = path.join(root, dir);
  if (!fs.existsSync(target)) continue;
  const files = fs.statSync(target).isDirectory() ? walk(target) : [target];
  for (const file of files) {
    if (file.endsWith('manifest.json')) continue;
    addEvidence({
      root,
      path: file,
      kind: 'derived-evidence',
      producedBy: 'cityrt-audit',
      proves: 'CityRT audit artefact',
    });
    count += 1;
  }
}
const written = writeManifest(root);
const manifest = JSON.parse(fs.readFileSync(written, 'utf8'));
console.log('registered', count, 'files; manifest entries', manifest.entries.length);
