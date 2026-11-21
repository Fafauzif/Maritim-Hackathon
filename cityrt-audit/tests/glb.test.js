const test = require('node:test');
const assert = require('node:assert');
const { parseGlb } = require('../tools/analysis/glb.js');

function buildGlb(json) {
  const jsonChunk = Buffer.from(JSON.stringify(json), 'utf8');
  const padded = Buffer.concat([jsonChunk, Buffer.alloc((4 - (jsonChunk.length % 4)) % 4, 0x20)]);
  const header = Buffer.alloc(12);
  header.write('glTF', 0, 'ascii');
  header.writeUInt32LE(2, 4);
  header.writeUInt32LE(12 + 8 + padded.length, 8);
  const chunk = Buffer.alloc(8);
  chunk.writeUInt32LE(padded.length, 0);
  chunk.write('JSON', 4, 'ascii');
  return Buffer.concat([header, chunk, padded]);
}

test('reads meshes, triangle count and union bounds', () => {
  const glb = buildGlb({
    asset: { version: '2.0', generator: 'CityRT-Test' },
    meshes: [{ primitives: [{ indices: 0, attributes: { POSITION: 1 } }] }],
    accessors: [
      { type: 'SCALAR', count: 36 },
      { type: 'VEC3', count: 24, min: [-2, 0, -2], max: [2, 6, 2] },
    ],
    materials: [{}, {}],
    textures: [{}],
  });
  const model = parseGlb(glb);
  assert.strictEqual(model.version, 2);
  assert.strictEqual(model.generator, 'CityRT-Test');
  assert.strictEqual(model.triangles, 12);
  assert.deepStrictEqual(model.bounds.min, [-2, 0, -2]);
  assert.deepStrictEqual(model.bounds.max, [2, 6, 2]);
  assert.strictEqual(model.materials, 2);
  assert.strictEqual(model.textures, 1);
});

test('uses POSITION count when geometry is unindexed', () => {
  const glb = buildGlb({
    asset: { version: '2.0' },
    meshes: [{ primitives: [{ attributes: { POSITION: 0 } }] }],
    accessors: [{ type: 'VEC3', count: 9, min: [0, 0, 0], max: [1, 1, 1] }],
  });
  assert.strictEqual(parseGlb(glb).triangles, 3);
});

test('rejects non-GLB input', () => {
  assert.throws(() => parseGlb(Buffer.from('not a model')), /glTF/i);
});
