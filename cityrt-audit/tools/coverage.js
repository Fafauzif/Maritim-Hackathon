// Verify that repository paths cited in the deliverables exist and are registered
// in the evidence manifest with the same SHA-256.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const PATH_PATTERN = /(?:^|[\s(`'"])((?:analysis|evidence|docs)\/[A-Za-z0-9_.\/-]+)/g;
const SKIP_EXTENSIONS = new Set(['.md', '.js', '.html', '.webp', '.png', '.css']);

function walk(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out;
}

function hashFile(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function checkCoverage(repoRoot) {
  const docsDir = path.join(repoRoot, 'docs');
  const manifestPath = path.join(repoRoot, 'evidence', 'manifest.json');
  let manifest = { entries: [] };
  if (fs.existsSync(manifestPath)) manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const manifestByPath = new Map(manifest.entries.map((entry) => [entry.path, entry]));

  const checked = [];
  const missingEvidence = [];
  const unregistered = [];
  const hashMismatches = [];
  let claims = 0;

  const files = fs.existsSync(docsDir) ? walk(docsDir).filter((f) => f.endsWith('.md')) : [];
  for (const file of files) {
    const text = fs.readFileSync(file, 'utf8');
    const seen = new Set();
    for (const match of text.matchAll(PATH_PATTERN)) {
      const cited = match[1].replace(/[.,;:)]+$/, '');
      if (seen.has(cited)) continue;
      seen.add(cited);
      claims += 1;
      const absolute = path.join(repoRoot, cited);
      const extension = path.extname(cited);
      // Directory-shaped or wildcard citations are references, not files.
      if (cited.includes('<') || cited.endsWith('/')) {
        const base = path.join(repoRoot, cited.replace(/\/$/, ''));
        if (!fs.existsSync(base)) missingEvidence.push({ file: path.relative(repoRoot, file), path: cited, reason: 'missing directory' });
        continue;
      }
      if (!fs.existsSync(absolute)) {
        if (!SKIP_EXTENSIONS.has(extension)) missingEvidence.push({ file: path.relative(repoRoot, file), path: cited, reason: 'missing file' });
        continue;
      }
      checked.push(cited);
      // The manifest is the index itself, not an entry inside it.
      if (cited === 'evidence/manifest.json') continue;
      const registered = manifestByPath.get(cited);
      if (!registered) unregistered.push({ file: path.relative(repoRoot, file), path: cited });
      else if (hashFile(absolute) !== registered.sha256) hashMismatches.push({ file: path.relative(repoRoot, file), path: cited });
    }
  }

  return { claims, checked, missingEvidence, unregistered, hashMismatches };
}

module.exports = { checkCoverage };

if (require.main === module) {
  const result = checkCoverage(process.argv[2] || 'cityrt-audit');
  console.log(JSON.stringify({
    claims: result.claims,
    checked: result.checked.length,
    missingEvidence: result.missingEvidence,
    unregistered: result.unregistered.length,
    hashMismatches: result.hashMismatches,
  }, null, 2));
  process.exit(result.missingEvidence.length === 0 && result.hashMismatches.length === 0 ? 0 : 1);
}
