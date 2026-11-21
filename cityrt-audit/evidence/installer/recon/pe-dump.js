// Read-only PE32 structure dump: sections, overlay position, and printable
// strings around given offsets. Nothing is extracted or executed.
const fs = require('node:fs');

const file = process.argv[2];
const anchors = process.argv.slice(3).map((v) => Number(v));

const fd = fs.openSync(file, 'r');
const size = fs.fstatSync(fd).size;

function readAt(offset, length) {
  const buffer = Buffer.alloc(Math.min(length, size - offset));
  fs.readSync(fd, buffer, 0, buffer.length, offset);
  return buffer;
}

const dos = readAt(0, 0x40);
const peOffset = dos.readUInt32LE(0x3c);
const pe = readAt(peOffset, 24);
const machine = pe.readUInt16LE(4);
const sectionCount = pe.readUInt16LE(6);
const optionalSize = pe.readUInt16LE(20);
const optional = readAt(peOffset + 24, optionalSize);
const magic = optional.readUInt16LE(0);
const imageBase = optional.readUInt32LE(28);
const sectionTableOffset = peOffset + 24 + optionalSize;

console.log('file size      :', size);
console.log('e_lfanew       :', peOffset, `(0x${peOffset.toString(16)})`);
console.log('machine        :', `0x${machine.toString(16)}`, machine === 0x14c ? '(i386)' : machine === 0x8664 ? '(x64)' : '');
console.log('optional magic :', `0x${magic.toString(16)}`, magic === 0x10b ? '(PE32)' : magic === 0x20b ? '(PE32+)' : '');
console.log('image base     :', `0x${imageBase.toString(16)}`);
console.log('sections       :', sectionCount);

let endOfImage = 0;
for (let i = 0; i < sectionCount; i += 1) {
  const entry = readAt(sectionTableOffset + i * 40, 40);
  const name = entry.subarray(0, 8).toString('latin1').replace(/\0+$/, '');
  const virtualSize = entry.readUInt32LE(8);
  const virtualAddress = entry.readUInt32LE(12);
  const rawSize = entry.readUInt32LE(16);
  const rawPointer = entry.readUInt32LE(20);
  const characteristics = entry.readUInt32LE(36);
  const sectionEnd = rawPointer + rawSize;
  if (rawSize > 0) endOfImage = Math.max(endOfImage, sectionEnd);
  console.log(
    `  ${name.padEnd(9)} vaddr=0x${virtualAddress.toString(16).padStart(8, '0')} vsize=${String(virtualSize).padStart(10)} raw=0x${rawPointer.toString(16).padStart(8, '0')} rawsize=${String(rawSize).padStart(10)} flags=0x${characteristics.toString(16)}`,
  );
}

console.log('end of last raw section:', endOfImage, `(0x${endOfImage.toString(16)})`);
console.log('overlay bytes          :', size - endOfImage, `(0x${(size - endOfImage).toString(16)})`);

if (size > endOfImage) {
  const head = readAt(endOfImage, 64);
  console.log('overlay first 64 bytes hex :', head.toString('hex'));
  console.log('overlay first 64 bytes text:', JSON.stringify(head.toString('latin1')));
}

for (const anchor of anchors) {
  const start = Math.max(0, anchor - 120);
  const window = readAt(start, 320);
  const text = window.toString('latin1').replace(/[^\x20-\x7e]/g, '.');
  console.log(`\n--- around ${anchor} (0x${anchor.toString(16)}) ---`);
  console.log(text);
}

fs.closeSync(fd);
