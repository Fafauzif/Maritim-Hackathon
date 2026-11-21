const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { checkCoverage } = require('../tools/coverage.js');

function makeRepo() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'cityrt-cov-'));
  fs.mkdirSync(path.join(root, 'docs'), { recursive: true });
  fs.mkdirSync(path.join(root, 'analysis', 'palette'), { recursive: true });
  fs.writeFileSync(path.join(root, 'analysis', 'palette', 'european.json'), '{"style":"european"}\n');
  fs.writeFileSync(
    path.join(root, 'docs', 'ART-BIBLE.md'),
    '# Art bible\n\nPalette lives in analysis/palette/european.json.\nMissing ref: analysis/palette/atlantis.json.\n',
  );
  return root;
}

test('reports a referenced path that does not exist', () => {
  const root = makeRepo();
  const result = checkCoverage(root);
  assert.strictEqual(result.missingEvidence.length, 1);
  assert.match(result.missingEvidence[0].path, /atlantis\.json$/);
  assert.strictEqual(result.claims >= 2, true);
});

test('counts only existing repository references and ignores prose URLs', () => {
  const root = makeRepo();
  const result = checkCoverage(root);
  assert.strictEqual(result.missingEvidence.every((item) => !item.path.startsWith('http')), true);
  assert.strictEqual(result.checked.includes('analysis/palette/european.json'), true);
});
