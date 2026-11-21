// Static analysis of the authenticated game client bundles: identify the renderer,
// the shader pipeline, renderer settings and simulation constants.
const fs = require('node:fs');
const path = require('node:path');

const ROOT = process.argv[2] || 'cityrt-audit';
const DIR = path.join(ROOT, 'evidence', 'game-bundles');
const OUT = path.join(ROOT, 'analysis', 'game');
fs.mkdirSync(OUT, { recursive: true });

const files = fs.readdirSync(DIR).filter((name) => name.endsWith('.js'));

const MARKERS = [
  'WebGLRenderer', 'THREE', 'ShaderMaterial', 'RawShaderMaterial', 'MeshStandardMaterial',
  'MeshLambertMaterial', 'MeshPhongMaterial', 'MeshBasicMaterial', 'InstancedMesh', 'BufferGeometry',
  'EffectComposer', 'postprocessing', 'SMAA', 'FXAA', 'SSAO', 'bloom', 'toneMapping', 'ACESFilmicToneMapping',
  'shadowMap', 'PCFSoftShadowMap', 'DirectionalLight', 'HemisphereLight', 'AmbientLight', 'FogExp2', 'Fog(',
  'WebGL2RenderingContext', 'OffscreenCanvas', 'getContext(`webgl2`', 'getContext(`webgl`',
  'babylon', 'pc.Application', 'UnityLoader', 'WebGPU', 'requestAnimationFrame',
  'draco', 'ktx2', 'KTX2Loader', 'GLTFLoader', 'gltf', 'glb',
  'vertexShader', 'fragmentShader', 'gl_FragColor', 'gl_Position', '#include <',
  'setPixelRatio', 'perspectiveCamera', 'OrthographicCamera', 'fov', 'near', 'far',
];

const inventory = [];
const markerTotals = {};
const huge = [];

for (const name of files) {
  const file = path.join(DIR, name);
  const text = fs.readFileSync(file, 'utf8');
  const counts = {};
  for (const marker of MARKERS) {
    const matches = text.split(marker).length - 1;
    if (matches > 0) {
      counts[marker] = matches;
      markerTotals[marker] = (markerTotals[marker] || 0) + matches;
    }
  }
  inventory.push({ name, bytes: text.length, markers: counts });
  if (text.length > 150000) huge.push({ name, bytes: text.length });
}

inventory.sort((a, b) => b.bytes - a.bytes);
fs.writeFileSync(path.join(OUT, 'bundle-inventory.json'), JSON.stringify({ generatedAt: new Date().toISOString(), fileCount: files.length, totalBytes: inventory.reduce((sum, item) => sum + item.bytes, 0), markerTotals, inventory }, null, 2) + '\n');

console.log('bundles:', files.length, 'total MB:', (inventory.reduce((sum, item) => sum + item.bytes, 0) / 1048576).toFixed(2));
const top = Object.entries(markerTotals).sort((a, b) => b[1] - a[1]).slice(0, 40);
console.log('marker totals:');
for (const [marker, count] of top) console.log(`  ${marker.padEnd(26)} ${count}`);
console.log('\nlargest bundles:');
for (const item of inventory.slice(0, 8)) console.log(`  ${item.name.padEnd(34)} ${(item.bytes / 1024).toFixed(0)} KB  ${Object.keys(item.markers).slice(0, 6).join(',')}`);
console.log('\nfiles with shader markers:');
for (const item of inventory) {
  const shader = ['gl_FragColor', 'gl_Position', '#include <', 'ShaderMaterial', 'fragmentShader'].some((marker) => item.markers[marker]);
  if (shader) console.log(`  ${item.name.padEnd(34)} ${(item.bytes / 1024).toFixed(0)} KB  ${JSON.stringify(item.markers).slice(0, 200)}`);
}
