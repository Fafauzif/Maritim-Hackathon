const test = require('node:test');
const assert = require('node:assert');
const { extractPalette } = require('../tools/analysis/palette.js');

function bands(colors, pixelsPerBand) {
  const rgba = new Uint8Array(colors.length * pixelsPerBand * 4);
  colors.forEach((color, band) => {
    for (let i = 0; i < pixelsPerBand; i += 1) {
      const offset = (band * pixelsPerBand + i) * 4;
      rgba.set([...color, 255], offset);
    }
  });
  return { width: colors.length * pixelsPerBand, height: 1, rgba };
}

test('recovers three solid bands with equal weights', () => {
  const image = bands([[255, 0, 0], [0, 128, 255], [16, 16, 16]], 100);
  const { colors } = extractPalette(image, { k: 3, iterations: 12 });
  assert.strictEqual(colors.length, 3);
  assert.deepStrictEqual(colors.map((c) => c.hex).sort(), ['#0080ff', '#101010', '#ff0000']);
  for (const color of colors) assert.ok(Math.abs(color.weight - 1 / 3) < 0.02);
});

test('flags a uniform image as blank', () => {
  const image = bands([[40, 40, 40]], 250);
  assert.strictEqual(extractPalette(image, { k: 2 }).stats.isBlank, true);
});

test('is deterministic for the same input', () => {
  const image = bands([[10, 20, 30], [200, 190, 180], [90, 140, 60], [250, 250, 245]], 64);
  const first = JSON.stringify(extractPalette(image, { k: 4 }));
  const second = JSON.stringify(extractPalette(image, { k: 4 }));
  assert.strictEqual(first, second);
});
