// Extract the look presets, the sketch shader source, quality settings and any
// camera/simulation constants from the authenticated client bundles.
const fs = require('node:fs');
const path = require('node:path');

const ROOT = process.argv[2] || 'cityrt-audit';
const DIR = path.join(ROOT, 'evidence', 'game-bundles');
const OUT = path.join(ROOT, 'analysis', 'game');
const SHADER_DIR = path.join(OUT, 'shaders');
fs.mkdirSync(SHADER_DIR, { recursive: true });

const files = fs.readdirSync(DIR).filter((name) => name.endsWith('.js'));
const byName = new Map(files.map((name) => [name, fs.readFileSync(path.join(DIR, name), 'utf8')]));

// --- 1. Look presets: {key:{name:e(`..`),desc:e(`..`),v:{hatch:1,...}}} ---
const lookText = byName.get('look-DZfJ2UwR.js') || '';
const presets = {};
for (const match of lookText.matchAll(/([a-z][a-z0-9]*):\{name:e\(`([^`]*)`\),desc:e\(`([^`]*)`\),v:\{([^}]*)\}\}/g)) {
  const values = {};
  for (const pair of match[4].matchAll(/([a-z][A-Za-z0-9]*):(-?[0-9.]+)/g)) values[pair[1]] = Number(pair[2]);
  presets[match[1]] = { name: match[2], description: match[3], values };
}

// --- 2. Shader sources: template literals containing GLSL ---
const shaders = [];
for (const [name, text] of byName) {
  for (const match of text.matchAll(/`([^`]{200,20000}?)`/g)) {
    const body = match[1];
    if (!/(void\s+main|gl_FragColor|gl_Position|precision\s+(mediump|highp)\s+float)/.test(body)) continue;
    if (!/(uniform|attribute|varying|in\s+vec|out\s+vec)/.test(body)) continue;
    shaders.push({ bundle: name, length: body.length, body });
  }
}
shaders.sort((a, b) => b.length - a.length);
for (let index = 0; index < Math.min(shaders.length, 40); index += 1) {
  const shader = shaders[index];
  fs.writeFileSync(path.join(SHADER_DIR, `${String(index).padStart(2, '0')}-${shader.bundle.replace(/\.js$/, '')}.glsl`), shader.body);
}

// --- 3. Quality settings ---
const qualityText = byName.get('quality-BJbdVyLr.js') || '';
const quality = {
  mentions: {
    pixelRatio: (qualityText.match(/pixelRatio/g) || []).length,
    shadows: (qualityText.match(/shadow/gi) || []).length,
    antialias: (qualityText.match(/antialias/gi) || []).length,
    toneMapping: (qualityText.match(/toneMapping/g) || []).length,
    bloom: (qualityText.match(/bloom/gi) || []).length,
    presetNames: [...qualityText.matchAll(/name:e\(`([^`]*)`\)/g)].map((match) => match[1]).slice(0, 12),
  },
  snippet: qualityText.slice(0, 1600),
};

// --- 4. Camera and simulation probes ---
const cameraHits = [];
const simHits = [];
for (const [name, text] of byName) {
  for (const match of text.matchAll(/.{80}(?:fov|zoom|camSlow|minZoom|maxZoom|camera)[^]{0,120}/g)) {
    if (cameraHits.length < 25 && /\d/.test(match[0])) cameraHits.push({ bundle: name, snippet: match[0].replace(/\s+/g, ' ').slice(0, 220) });
  }
  for (const match of text.matchAll(/.{60}(?:tick|setInterval|dt\b|construction|growMs|growth|simSpeed)[^]{0,120}/g)) {
    if (simHits.length < 25 && /\d/.test(match[0])) simHits.push({ bundle: name, snippet: match[0].replace(/\s+/g, ' ').slice(0, 220) });
  }
}

const payload = {
  generatedAt: new Date().toISOString(),
  lookPresets: presets,
  shaderInventory: shaders.map((shader) => ({ bundle: shader.bundle, length: shader.length })),
  quality,
  cameraHits,
  simHits,
};
fs.writeFileSync(path.join(OUT, 'look-and-shaders.json'), JSON.stringify(payload, null, 2) + '\n');

console.log('look presets:', Object.keys(presets).join(', '));
for (const [key, preset] of Object.entries(presets)) {
  console.log(`  ${key.padEnd(8)} ${preset.name} — ${preset.description}`);
  console.log(`           ${JSON.stringify(preset.values)}`);
}
console.log('\nshaders captured:', shaders.length, 'largest:', shaders.slice(0, 5).map((shader) => `${shader.bundle}:${shader.length}`).join(' '));
console.log('quality presets:', quality.mentions.presetNames.join(', '));
console.log('quality snippet:', quality.snippet.slice(0, 500));
console.log('\ncamera hits:'); for (const hit of cameraHits.slice(0, 8)) console.log(`  [${hit.bundle}] ${hit.snippet.slice(0, 180)}`);
console.log('\nsim hits:'); for (const hit of simHits.slice(0, 8)) console.log(`  [${hit.bundle}] ${hit.snippet.slice(0, 180)}`);
