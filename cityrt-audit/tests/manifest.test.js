const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { addEvidence, writeManifest } = require('../tools/manifest.js');

test('manifest records sha256, dedupes identical paths, and sorts by path', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'cityrt-'));
  const bFile = path.join(root, 'b.txt');
  const aFile = path.join(root, 'a.txt');
  fs.writeFileSync(bFile, 'beta');
  fs.writeFileSync(aFile, 'alpha');
  addEvidence({ root, path: bFile, kind: 'text', producedBy: 'test', proves: 'b' });
  addEvidence({ root, path: aFile, kind: 'text', producedBy: 'test', proves: 'a' });
  addEvidence({ root, path: bFile, kind: 'text', producedBy: 'test', proves: 'b again' });
  const written = writeManifest(root);
  const manifest = JSON.parse(fs.readFileSync(written, 'utf8'));
  assert.strictEqual(manifest.entries.length, 2);
  assert.deepStrictEqual(manifest.entries.map((e) => path.basename(e.path)), ['a.txt', 'b.txt']);
  assert.strictEqual(manifest.entries[2 - 2].proves, 'a');
  assert.strictEqual(manifest.entries[1].proves, 'b again');
  assert.match(manifest.entries[0].sha256, /^[0-9a-f]{64}$/);
});
