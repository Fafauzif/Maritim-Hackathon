const test = require('node:test');
const assert = require('node:assert');
const zlib = require('node:zlib');
const { decodePng } = require('../tools/analysis/png.js');

const CRC_TABLE = (() => {
  const table = new Int32Array(256);
  for (let n = 0; n < 256; n += 1) {
    let c = n;
    for (let k = 0; k < 8; k += 1) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c;
  }
  return table;
})();

function crc32(buffer) {
  let c = 0xffffffff;
  for (const byte of buffer) c = CRC_TABLE[(c ^ byte) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function chunk(type, data) {
  const length = Buffer.alloc(4);
  length.writeUInt32BE(data.length, 0);
  const typeAndData = Buffer.concat([Buffer.from(type, 'ascii'), data]);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(typeAndData), 0);
  return Buffer.concat([length, typeAndData, crc]);
}

function encodePng(width, height, pixels) {
  const raw = Buffer.alloc(height * (1 + width * 3));
  for (let y = 0; y < height; y += 1) {
    raw[y * (1 + width * 3)] = 0;
    for (let x = 0; x < width; x += 1) {
      const [r, g, b] = pixels[y * width + x];
      const o = y * (1 + width * 3) + 1 + x * 3;
      raw[o] = r;
      raw[o + 1] = g;
      raw[o + 2] = b;
    }
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 2; // colour type: truecolour
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk('IHDR', ihdr),
    chunk('IDAT', zlib.deflateSync(raw)),
    chunk('IEND', Buffer.alloc(0)),
  ]);
}

test('decodes a 2x2 RGB PNG into RGBA', () => {
  const png = encodePng(2, 2, [
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
    [255, 255, 255],
  ]);
  const image = decodePng(png);
  assert.strictEqual(image.width, 2);
  assert.strictEqual(image.height, 2);
  assert.deepStrictEqual([...image.rgba.subarray(0, 4)], [255, 0, 0, 255]);
  assert.deepStrictEqual([...image.rgba.subarray(8, 12)], [0, 0, 255, 255]);
});

test('rejects interlaced PNG with a typed error', () => {
  const png = encodePng(1, 1, [[0, 0, 0]]);
  png[28] = 1; // IHDR interlace byte
  assert.throws(() => decodePng(png), /interlace/i);
});

test('rejects a non-PNG buffer', () => {
  assert.throws(() => decodePng(Buffer.from('nope')), /PNG/);
});
