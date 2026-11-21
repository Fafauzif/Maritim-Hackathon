// Focused extraction: renderer settings, the paper "look" shader system,
// day/night timing and camera parameters from the authenticated bundles.
const fs = require('node:fs');
const path = require('node:path');

const ROOT = process.argv[2] || 'cityrt-audit';
const DIR = path.join(ROOT, 'evidence', 'game-bundles');
const OUT = path.join(ROOT, 'analysis', 'game');
fs.mkdirSync(OUT, { recursive: true });

const names = fs.readdirSync(DIR).filter((name) => name.endsWith('.js'));
const byName = new Map();
for (const name of names) byName.set(name, fs.readFileSync(path.join(DIR, name), 'utf8'));

function findFiles(pattern) {
  const hits = [];
  const regex = new RegExp(pattern, 'i');
  for (const [name, text] of byName) {
    if (regex.test(text)) hits.push(name);
  }
  return hits;
}

function grab(name, pattern, radius = 260, limit = 4) {
  const text = byName.get(name);
  if (!text) return [];
  const out = [];
  const regex = new RegExp(pattern, 'g');
  let match;
  while ((match = regex.exec(text)) && out.length < limit) {
    const start = Math.max(0, match.index - radius);
    out.push(text.slice(start, Math.min(text.length, match.index + match[0].length + radius)).replace(/\s+/g, ' '));
  }
  return out;
}

const report = {
  generatedAt: new Date().toISOString(),
  rendererFiles: findFiles('WebGLRenderer|setPixelRatio'),
  lookFiles: findFiles('uVignette|uPaper|uHatch'),
  daylightFiles: findFiles('dayMinutes|dayNight'),
  styleFiles: findFiles('european|cyberpunk'),
  findings: {},
};

// Renderer construction settings
const rendererFiles = report.rendererFiles;
report.findings.renderer = [];
for (const name of rendererFiles.slice(0, 6)) {
  for (const snippet of grab(name, 'antialias\\s*:', 220, 3)) report.findings.renderer.push({ bundle: name, snippet });
  for (const snippet of grab(name, 'toneMapping\\s*:', 160, 2)) report.findings.renderer.push({ bundle: name, snippet });
  for (const snippet of grab(name, 'shadowMap\\s*:', 200, 2)) report.findings.renderer.push({ bundle: name, snippet });
}

// Camera parameters
report.findings.camera = [];
for (const name of names) {
  for (const snippet of grab(name, 'fov\\s*:\\s*[0-9]+', 200, 2)) report.findings.camera.push({ bundle: name, snippet });
  for (const snippet of grab(name, 'OrthographicCamera|perspective', 160, 1)) report.findings.camera.push({ bundle: name, snippet });
}

// Look shader system defaults
report.findings.look = [];
for (const name of report.lookFiles.slice(0, 4)) {
  for (const snippet of grab(name, 'uPaper\\s*:', 300, 2)) report.findings.look.push({ bundle: name, snippet });
  for (const snippet of grab(name, 'uVignette\\s*:', 300, 2)) report.findings.look.push({ bundle: name, snippet });
  for (const snippet of grab(name, 'paper\\s*:\\s*-?[0-9.]', 260, 3)) report.findings.look.push({ bundle: name, snippet });
}

// Day/night + prefs
report.findings.daylight = [];
for (const name of report.daylightFiles.slice(0, 4)) {
  for (const snippet of grab(name, 'dayMinutes', 240, 3)) report.findings.daylight.push({ bundle: name, snippet });
  for (const snippet of grab(name, 'speed', 120, 2)) report.findings.daylight.push({ bundle: name, snippet });
}

// Style keys in game code
report.findings.styles = [];
for (const name of report.styleFiles.slice(0, 6)) {
  for (const snippet of grab(name, 'european', 200, 2)) report.findings.styles.push({ bundle: name, snippet });
}

fs.writeFileSync(path.join(OUT, 'focused-extract.json'), JSON.stringify(report, null, 2) + '\n');

console.log('renderer files:', rendererFiles.join(', '));
console.log('look files:', report.lookFiles.join(', '));
console.log('daylight files:', report.daylightFiles.join(', '));
console.log('style files:', report.styleFiles.slice(0, 12).join(', '));
for (const section of ['renderer', 'camera', 'look', 'daylight', 'styles']) {
  console.log(`\n=== ${section} ===`);
  for (const row of report.findings[section].slice(0, 6)) console.log(`[${row.bundle}] ${row.snippet.slice(0, 380)}`);
}
