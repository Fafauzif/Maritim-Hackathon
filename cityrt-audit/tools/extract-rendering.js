// Extract concrete rendering configuration from the authenticated game bundles:
// renderer settings, post-processing, lights, fog, camera and simulation timing.
const fs = require('node:fs');
const path = require('node:path');

const ROOT = process.argv[2] || 'cityrt-audit';
const DIR = path.join(ROOT, 'evidence', 'game-bundles');
const OUT = path.join(ROOT, 'analysis', 'game');
fs.mkdirSync(OUT, { recursive: true });

const files = fs.readdirSync(DIR).filter((name) => name.endsWith('.js'));
const texts = new Map(files.map((name) => [name, fs.readFileSync(path.join(DIR, name), 'utf8')]));

function snippets(text, pattern, radius, limit = 6) {
  const out = [];
  const regex = new RegExp(pattern, 'g');
  let match;
  while ((match = regex.exec(text)) && out.length < limit) {
    const start = Math.max(0, match.index - radius);
    const end = Math.min(text.length, match.index + match[0].length + radius);
    out.push(text.slice(start, end).replace(/\s+/g, ' '));
  }
  return out;
}

function collect(pattern, radius, limit) {
  const found = [];
  for (const [name, text] of texts) {
    for (const snippet of snippets(text, pattern, radius, limit)) {
      found.push({ bundle: name, snippet: snippet.slice(0, 700) });
      if (found.length >= limit) return found;
    }
  }
  return found;
}

const extract = {
  generatedAt: new Date().toISOString(),
  source: 'authenticated client bundles in evidence/game-bundles',
  renderer: collect('new [A-Za-z_$][A-Za-z0-9_$]*\\.WebGLRenderer|new WebGLRenderer', 260, 5),
  toneMapping: collect('toneMapping\\s*[:=]', 200, 8),
  exposure: collect('toneMappingExposure', 160, 6),
  outputColorSpace: collect('outputColorSpace', 140, 4),
  shadowMap: collect('shadowMap\\s*[\\.=]', 180, 6),
  pixelRatio: collect('setPixelRatio', 160, 6),
  clearColor: collect('setClearColor', 160, 4),
  fog: collect('FogExp2|new Fog\\(', 200, 5),
  lights: collect('new [A-Za-z_$]*(Directional|Hemisphere|Ambient|Point|Spot)Light', 240, 8),
  camera: collect('PerspectiveCamera\\(|OrthographicCamera\\(', 240, 6),
  postProcessing: collect('EffectComposer|UnrealBloomPass|RenderPass|ShaderPass|SMAA|Vignette', 220, 8),
  instancing: collect('InstancedMesh', 180, 4),
  materials: collect('new [A-Za-z_$]*\\.(MeshStandardMaterial|MeshLambertMaterial|MeshPhongMaterial|ShaderMaterial|RawShaderMaterial)\\(', 260, 10),
  simulation: collect('(?:dayLength|dayNight|timeOfDay|tickMs|tickRate|simSpeed|constructionTime|growInterval)', 200, 10),
  styles: collect('(?:cityrt\\.|styleKey|skinKey|palette)', 140, 6),
};

fs.writeFileSync(path.join(OUT, 'rendering-extract.json'), JSON.stringify(extract, null, 2) + '\n');

function printSection(title, rows) {
  console.log(`\n=== ${title} (${rows.length}) ===`);
  for (const row of rows.slice(0, 5)) console.log(`[${row.bundle}] ${row.snippet.slice(0, 420)}`);
}

printSection('WebGLRenderer', extract.renderer);
printSection('toneMapping', extract.toneMapping);
printSection('exposure', extract.exposure);
printSection('shadowMap', extract.shadowMap);
printSection('fog', extract.fog);
printSection('lights', extract.lights);
printSection('camera', extract.camera);
printSection('postProcessing', extract.postProcessing);
printSection('materials', extract.materials);
printSection('simulation', extract.simulation);
