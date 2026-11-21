// Mine the shipped building catalog: style/category composition, architectural
// vocabulary, and the explicit growth rules the descriptions encode.
const fs = require('node:fs');
const path = require('node:path');

const ROOT = process.argv[2] || 'cityrt-audit';
const catalog = JSON.parse(
  fs.readFileSync(path.join(ROOT, 'evidence', 'catalog', 'catalog.json'), 'utf8').replace(/^\uFEFF/, ''),
);
const outDir = path.join(ROOT, 'analysis', 'catalog');
fs.mkdirSync(outDir, { recursive: true });

const MATERIAL_TOKENS = [
  'фахверк', 'черепиц', 'кирпич', 'мансард', 'мрамор', 'гранит', 'бетон', 'стекл', 'медь', 'дерев',
  'камен', 'штукатур', 'металл', 'неон', 'панел', 'сваи', 'аркад', 'портик', 'щипец', 'башн', 'купол',
  'шпил', 'слухов', 'эркер', 'балкон', 'лоджи', 'навес', 'козыр', 'оград', 'чугун', 'кован', 'изразц',
  'азулежу', 'пилотис', 'кобого', 'жалюзи', 'ставн', 'витраж', 'фонар', 'вывеск',
];

const byStyle = new Map();
const byCategory = new Map();
const growthRules = [];
const footprints = [];

for (const building of catalog) {
  if (!byStyle.has(building.style)) byStyle.set(building.style, { count: 0, categories: {}, titles: [] });
  if (!byCategory.has(building.cat)) byCategory.set(building.cat, 0);
  const style = byStyle.get(building.style);
  style.count += 1;
  style.categories[building.cat] = (style.categories[building.cat] || 0) + 1;
  style.titles.push(building.title);
  byCategory.set(building.cat, byCategory.get(building.cat) + 1);

  const texts = [building.desc || '', ...(building.descKeys || [])].filter(Boolean);
  for (const text of texts) {
    const growth = text.match(/Тянется[^.]*\./);
    if (growth) growthRules.push({ name: building.name, style: building.style, cat: building.cat, rule: growth[0] });
    for (const match of text.matchAll(/(\d+)\s*[×x]\s*(\d+)/g)) {
      footprints.push({ name: building.name, style: building.style, cat: building.cat, width: Number(match[1]), depth: Number(match[2]) });
    }
  }
}

const vocabulary = [...byStyle.entries()].map(([styleKey, value]) => {
  const corpus = catalog
    .filter((b) => b.style === styleKey)
    .map((b) => [b.title, b.desc || '', ...(b.descKeys || [])].join(' '))
    .join(' ')
    .toLowerCase();
  const counts = {};
  for (const token of MATERIAL_TOKENS) {
    const matches = corpus.match(new RegExp(token, 'g'));
    if (matches) counts[token] = matches.length;
  }
  return { style: styleKey, buildings: value.count, categories: value.categories, topTerms: Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 12) };
});

const footprintsByStyle = {};
for (const footprint of footprints) {
  const key = footprint.style;
  footprintsByStyle[key] = footprintsByStyle[key] || [];
  footprintsByStyle[key].push(`${footprint.width}x${footprint.depth}`);
}

const summary = {
  generatedAt: new Date().toISOString(),
  source: 'evidence/catalog/catalog.json (public, unauthenticated)',
  totals: {
    buildings: catalog.length,
    withDescription: catalog.filter((b) => b.desc).length,
    withGrowthRules: growthRules.length,
    footprintMentions: footprints.length,
    styles: byStyle.size,
    categories: byCategory.size,
  },
  byCategory: Object.fromEntries([...byCategory.entries()].sort((a, b) => b[1] - a[1])),
  byStyle: Object.fromEntries([...byStyle.entries()].map(([k, v]) => [k, { count: v.count, categories: v.categories }]).sort((a, b) => b[1].count - a[1].count)),
  vocabulary,
  growthRules,
  footprintsByStyle,
};

fs.writeFileSync(path.join(outDir, 'catalog-analysis.json'), JSON.stringify(summary, null, 2) + '\n');

console.log('buildings:', summary.totals.buildings, '| with desc:', summary.totals.withDescription, '| growth rules:', summary.totals.withGrowthRules);
console.log('by category:', JSON.stringify(summary.byCategory));
console.log('by style:', JSON.stringify(summary.byStyle));
console.log('\nvocabulary (top terms per style):');
for (const entry of vocabulary) {
  console.log(`  ${entry.style.padEnd(13)} ${entry.buildings.toString().padStart(3)}  ${entry.topTerms.slice(0, 6).map(([t, c]) => `${t}:${c}`).join(' ')}`);
}
console.log('\nfootprint mentions:', summary.totals.footprintMentions);
for (const [styleKey, list] of Object.entries(footprintsByStyle)) console.log(`  ${styleKey}: ${list.join(' ')}`);
console.log('\nsample growth rules:');
for (const rule of growthRules.slice(0, 8)) console.log(`  ${rule.name}: ${rule.rule}`);
