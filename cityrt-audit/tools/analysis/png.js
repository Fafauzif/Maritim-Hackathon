// Minimal PNG decoder for measured colour work: 8-bit RGB/RGBA, all filters.
const zlib = require('node:zlib');

const SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

class UnsupportedPngError extends Error {
  constructor(reason) {
    super(`Unsupported PNG: ${reason}`);
    this.name = 'UnsupportedPngError';
  }
}

function paeth(a, b, c) {
  const p = a + b - c;
  const pa = Math.abs(p - a);
  const pb = Math.abs(p - b);
  const pc = Math.abs(p - c);
  if (pa <= pb && pa <= pc) return a;
  if (pb <= pc) return b;
  return c;
}

function decodePng(buffer) {
  if (!Buffer.isBuffer(buffer) || buffer.length < 8 || !buffer.subarray(0, 8).equals(SIGNATURE)) {
    throw new UnsupportedPngError('not a PNG signature');
  }
  let offset = 8;
  let width = 0;
  let height = 0;
  let bitDepth = 0;
  let colorType = 0;
  let interlace = 0;
  const idat = [];

  while (offset + 8 <= buffer.length) {
    const length = buffer.readUInt32BE(offset);
    const type = buffer.toString('ascii', offset + 4, offset + 8);
    const dataStart = offset + 8;
    const data = buffer.subarray(dataStart, dataStart + length);
    if (data.length !== length) throw new UnsupportedPngError('truncated chunk');
    if (type === 'IHDR') {
      width = data.readUInt32BE(0);
      height = data.readUInt32BE(4);
      bitDepth = data[8];
      colorType = data[9];
      interlace = data[12];
    } else if (type === 'IDAT') {
      idat.push(Buffer.from(data));
    } else if (type === 'IEND') {
      break;
    }
    offset = dataStart + length + 4;
  }

  if (!width || !height) throw new UnsupportedPngError('missing IHDR');
  if (interlace !== 0) throw new UnsupportedPngError('interlaced images are not supported');
  if (bitDepth !== 8) throw new UnsupportedPngError(`bit depth ${bitDepth} is not supported`);
  if (colorType !== 2 && colorType !== 6) {
    throw new UnsupportedPngError(`colour type ${colorType} is not supported`);
  }

  const channels = colorType === 6 ? 4 : 3;
  const rowBytes = width * channels;
  const stride = rowBytes + 1;
  const inflated = zlib.inflateSync(Buffer.concat(idat));
  if (inflated.length < stride * height) throw new UnsupportedPngError('short image data');

  const pixels = Buffer.alloc(rowBytes * height);
  for (let y = 0; y < height; y += 1) {
    const filter = inflated[y * stride];
    const source = inflated.subarray(y * stride + 1, y * stride + 1 + rowBytes);
    const target = pixels.subarray(y * rowBytes, (y + 1) * rowBytes);
    const prior = y > 0 ? pixels.subarray((y - 1) * rowBytes, y * rowBytes) : null;
    for (let x = 0; x < rowBytes; x += 1) {
      const raw = source[x];
      const left = x >= channels ? target[x - channels] : 0;
      const up = prior ? prior[x] : 0;
      const upLeft = prior && x >= channels ? prior[x - channels] : 0;
      let value;
      switch (filter) {
        case 0: value = raw; break;
        case 1: value = raw + left; break;
        case 2: value = raw + up; break;
        case 3: value = raw + ((left + up) >> 1); break;
        case 4: value = raw + paeth(left, up, upLeft); break;
        default: throw new UnsupportedPngError(`unknown filter type ${filter}`);
      }
      target[x] = value & 0xff;
    }
  }

  if (channels === 3) {
    const rgba = new Uint8Array(width * height * 4);
    for (let i = 0; i < width * height; i += 1) {
      rgba[i * 4] = pixels[i * 3];
      rgba[i * 4 + 1] = pixels[i * 3 + 1];
      rgba[i * 4 + 2] = pixels[i * 3 + 2];
      rgba[i * 4 + 3] = 255;
    }
    return { width, height, rgba };
  }
  return { width, height, rgba: new Uint8Array(pixels.buffer, pixels.byteOffset, pixels.length) };
}

module.exports = { decodePng, UnsupportedPngError };
