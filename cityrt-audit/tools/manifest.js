// Evidence manifest: every audit claim points at a file recorded here by SHA-256.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const stores = new Map();

function storeFor(root) {
  const key = path.resolve(root);
  if (!stores.has(key)) stores.set(key, new Map());
  return stores.get(key);
}

function addEvidence({ root, path: filePath, kind, producedBy, proves }) {
  const abs = path.resolve(filePath);
  const bytes = fs.readFileSync(abs);
  const sha256 = crypto.createHash('sha256').update(bytes).digest('hex');
  const store = storeFor(root);
  store.set(abs, { path: path.relative(path.resolve(root), abs).replace(/\\/g, '/'), sha256, bytes: bytes.length, kind, producedBy, proves });
  return { path: abs, sha256, bytes: bytes.length };
}

function writeManifest(root) {
  const dir = path.join(root, 'evidence');
  fs.mkdirSync(dir, { recursive: true });
  const entries = [...storeFor(root).values()].sort((a, b) => a.path.localeCompare(b.path));
  const out = path.join(dir, 'manifest.json');
  fs.writeFileSync(out, JSON.stringify({ generatedAt: new Date().toISOString(), entries }, null, 2) + '\n');
  return out;
}

function readManifest(root) {
  const out = path.join(root, 'evidence', 'manifest.json');
  if (!fs.existsSync(out)) return { generatedAt: null, entries: [] };
  return JSON.parse(fs.readFileSync(out, 'utf8'));
}

module.exports = { addEvidence, writeManifest, readManifest };
