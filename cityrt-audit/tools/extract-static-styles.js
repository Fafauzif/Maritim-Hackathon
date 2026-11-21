// Extract style and map-skin records from the public client chunks.
// These are shipped, unauthenticated data; every record cites its chunk.
const fs = require('node:fs');
const path = require('node:path');

const ROOT = process.argv[2] || 'cityrt-audit';
const PUBLIC_DIR = path.join(ROOT, 'evidence', 'scripts', 'public');
const OUT_DIR = path.join(ROOT, 'analysis', 'styles');
const ANALYSIS_DIR = path.join(ROOT, 'analysis');
fs.mkdirSync(OUT_DIR, { recursive: true });

function read(name) {
  return fs.readFileSync(path.join(PUBLIC_DIR, name), 'utf8');
}

function unescapeJs(raw) {
  return raw.replace(/\\`/g, '`').replace(/\\'/g, "'").replace(/\\\\/g, '\\');
}

// Style records: {id:N,key:`x`,name:e(`...`),short:e(`...`),color:`#..`,accent:`#..`,desc:e(`...`),...}
function extractStyles(source) {
  const records = [];
  const pattern =
    /\{id:(\d+),key:`([^`]+)`,name:e\(`([^`]*)`\),short:e\(`([^`]*)`\),color:`(#[0-9A-Fa-f]{6})`,accent:`(#[0-9A-Fa-f]{6})`,desc:e\(`([^`]*)`\)/g;
  for (const match of source.matchAll(pattern)) {
    records.push({
      id: Number(match[1]),
      key: match[2],
      name: unescapeJs(match[3]),
      short: unescapeJs(match[4]),
      color: match[5],
      accent: match[6],
      description: unescapeJs(match[7]),
      evidence: 'evidence/scripts/public/styles-EE7sSX4o.js',
    });
  }
  return records;
}

// Map skins: {id:`meadow`,name:e(`...`),desc:e(`...`),grass:[`#..`,`#..`],...}
function extractSkins(source) {
  const records = [];
  const blocks = source.split(/\},\{id:`/).map((block, index) => (index === 0 ? block : '{id:`' + block));
  for (const block of blocks) {
    const id = block.match(/id:`([^`]+)`/);
    if (!id) continue;
    const hexes = [...block.matchAll(/`(#[0-9A-Fa-f]{6})`/g)].map((m) => m[1]);
    const named = {};
    for (const field of ['grass', 'leaf', 'soil', 'tint', 'water', 'sky']) {
      const list = block.match(new RegExp(field + ':\\[([^\\]]+)\\]'));
      if (list) named[field] = [...list[1].matchAll(/#[0-9A-Fa-f]{6}/g)].map((m) => m[0]);
      const scalar = block.match(new RegExp(field + ':`(#[0-9A-Fa-f]{6})`'));
      if (scalar) named[field] = [scalar[1]];
    }
    const desat = block.match(/desat:([0-9.]+)/);
    records.push({
      id: id[1],
      colors: named,
      hexCount: hexes.length,
      desat: desat ? Number(desat[1]) : null,
      evidence: 'evidence/scripts/public/_skins-DJrChhsr.js',
    });
  }
  return records;
}

function extractPreviewMap(source) {
  const map = {};
  for (const match of source.matchAll(/"\.\/(styles\/([a-z-]+)\.webp)":`(\/assets\/[^`]+\.webp)`/g)) {
    map[match[2]] = match[3];
  }
  return map;
}

const styleChunk = read('styles-EE7sSX4o.js');
const skinChunk = read('_skins-DJrChhsr.js');
const previewChunk = read('styles-DATr6XE2.js');

const styles = extractStyles(styleChunk);
const skins = extractSkins(skinChunk);
const previews = extractPreviewMap(previewChunk);

const styleDoc = {
  generatedAt: new Date().toISOString(),
  source: 'public client chunks (no authentication required)',
  counts: {
    styleRecords: styles.length,
    previewImages: Object.keys(previews).length,
    mapSkins: skins.length,
  },
  contradiction:
    'Marketing copy says "nine personalities"; the client registers 14 style previews and N style records. Unresolved until the in-game style picker is observable.',
  styles,
  previews,
};
fs.writeFileSync(path.join(OUT_DIR, 'styles-static.json'), JSON.stringify(styleDoc, null, 2) + '\n');
fs.writeFileSync(path.join(ANALYSIS_DIR, 'skins-static.json'), JSON.stringify({ generatedAt: styleDoc.generatedAt, skins }, null, 2) + '\n');

console.log('style records:', styles.length);
for (const style of styles) console.log(`  ${style.id}. ${style.key.padEnd(14)} ${style.color} / ${style.accent}  ${style.short}`);
console.log('preview images:', Object.keys(previews).length, Object.keys(previews).join(', '));
console.log('map skins:', skins.length);
for (const skin of skins) console.log(`  ${skin.id.padEnd(12)} desat=${skin.desat} fields=${Object.keys(skin.colors).join(',')}`);
