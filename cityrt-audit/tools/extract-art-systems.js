// Extract the game's art systems: palette tables, the sketch shader, the wash
// material injection, camera parameters and geometry-building hints.
const fs = require('node:fs');
const path = require('node:path');

const ROOT = process.argv[2] || 'cityrt-audit';
const DIR = path.join(ROOT, 'evidence', 'game-bundles');
const OUT = path.join(ROOT, 'analysis', 'game');
const SHADER_DIR = path.join(OUT, 'shaders');
fs.mkdirSync(SHADER_DIR, { recursive: true });

const read = (name) => {
  try { return fs.readFileSync(path.join(DIR, name), 'utf8'); } catch { return ''; }
};

// ---- 1. Palette families ----
function paletteFrom(name) {
  const text = read(name);
  if (!text) return null;
  const families = {};
  for (const match of text.matchAll(/([A-Za-z][A-Za-z0-9]*):\[((?:`#[0-9A-Fa-f]{6}`,?){2,})\]/g)) {
    families[match[1]] = [...match[2].matchAll(/#[0-9A-Fa-f]{6}/g)].map((m) => m[0]);
  }
  for (const match of text.matchAll(/([A-Za-z][A-Za-z0-9]*):`(#[0-9A-Fa-f]{6})`/g)) {
    families[match[1]] = [match[2]];
  }
  for (const match of text.matchAll(/([A-Za-z][A-Za-z0-9]*):\{([^}]+)\}/g)) {
    const entries = {};
    for (const pair of match[2].matchAll(/([A-Za-z][A-Za-z0-9]*):`(#[0-9A-Fa-f]{6})`/g)) entries[pair[1]] = pair[2];
    if (Object.keys(entries).length) families[match[1]] = entries;
  }
  return { file: name, families };
}

const palettes = ['pal-T-INdQBs.js', 'pal-Doxq3a-X.js'].map(paletteFrom).filter(Boolean);

// ---- 2. Sketch shader & wash material GLSL ----
function glslFrom(name) {
  const text = read(name);
  const chunks = [];
  for (const match of text.matchAll(/`([^`]{120,20000}?)`/g)) {
    const body = match[1];
    if (/(void\s+main|gl_FragColor|gl_Position|ik_noise|outgoingLight|#include)/.test(body)) {
      chunks.push(body);
    }
  }
  return chunks;
}

const sketchChunks = [...glslFrom('sketch-C5kxZCCL.js'), ...glslFrom('washmat-Bp0o3aa1.js'), ...glslFrom('post-BtPl7EWO.js')];
sketchChunks.slice(0, 20).forEach((body, index) => {
  fs.writeFileSync(path.join(SHADER_DIR, `sketch-${String(index).padStart(2, '0')}.glsl`), body);
});

// Uniform / parameter names used by the sketch system
const sketchText = read('sketch-C5kxZCCL.js') + read('washmat-Bp0o3aa1.js') + read('post-BtPl7EWO.js');
const uniforms = [...new Set([...sketchText.matchAll(/\b(u[A-Z][A-Za-z0-9]{2,24})\b/g)].map((match) => match[1]))].sort();
const shaderFunctions = [...new Set([...sketchText.matchAll(/\b(ik_[a-zA-Z0-9_]+)\b/g)].map((match) => match[1]))].sort();

// ---- 3. Camera search ----
const candidateFiles = fs.readdirSync(DIR).filter((name) => name.endsWith('.js'));
const cameraHits = [];
for (const name of candidateFiles) {
  const text = read(name);
  for (const match of text.matchAll(/.{70}(?:new [A-Za-z_$]{1,4}\((?:3[0-9]|4[0-9]|5[0-9]|6[0-9])(?:\.\d+)?,|camSlow|minZoom|maxZoom|zoomTo|camDist|distanceMin|distanceMax|pitch|azimuth)/g)) {
    if (cameraHits.length < 30) cameraHits.push({ bundle: name, snippet: match[0].replace(/\s+/g, ' ').slice(0, 220) });
  }
}

// ---- 4. Geometry hints ----
const geoFiles = ['geo-CPar3Mvm.js', 'geo-CjVqi9gp.js', 'geom-DoZGdBci.js', 'shapes-BncVtTXM.js', 'shared_kit-CduiyIzJ.js', 'geopack-HDAxjwGV.js', 'atlas-ptNQDssk.js'];
const geometry = geoFiles.map((name) => {
  const text = read(name);
  return {
    file: name,
    bytes: text.length,
    head: text.slice(0, 420).replace(/\s+/g, ' '),
    exports: [...new Set([...text.matchAll(/export\s*\{([^}]*)\}/g)].flatMap((match) => match[1].split(',').map((entry) => entry.trim())))].slice(0, 20),
    numbers: [...new Set([...text.matchAll(/[=(:,]\s*(\d+(?:\.\d+)?)\s*[),;]/g)].map((match) => match[1]))].slice(0, 25),
  };
});

const report = {
  generatedAt: new Date().toISOString(),
  source: 'authenticated client bundles (evidence/game-bundles)',
  palettes,
  sketch: {
    glslChunkCount: sketchChunks.length,
    uniforms,
    functions: shaderFunctions,
    washInjection: (read('washmat-Bp0o3aa1.js').match(/`([^`]{40,400})`/g) || []).slice(0, 4),
  },
  cameraHits,
  geometry,
};
fs.writeFileSync(path.join(OUT, 'art-systems.json'), JSON.stringify(report, null, 2) + '\n');

console.log('palette families:', palettes.map((entry) => `${entry.file}:${Object.keys(entry.families).length}`).join(' '));
for (const entry of palettes) {
  console.log(`\n[${entry.file}]`);
  for (const [family, value] of Object.entries(entry.families).slice(0, 18)) console.log(`  ${family}: ${Array.isArray(value) ? value.join(' ') : JSON.stringify(value)}`);
}
console.log('\nsketch GLSL chunks:', sketchChunks.length, 'uniforms:', uniforms.length);
console.log('uniforms:', uniforms.join(' '));
console.log('shader fns:', shaderFunctions.join(' '));
console.log('\ncamera hits:');
for (const hit of cameraHits.slice(0, 10)) console.log(`  [${hit.bundle}] ${hit.snippet.slice(0, 170)}`);
console.log('\ngeometry modules:');
for (const entry of geometry) console.log(`  ${entry.file.padEnd(26)} ${(entry.bytes / 1024).toFixed(1)} KB exports=${entry.exports.slice(0, 6).join(',')}`);
