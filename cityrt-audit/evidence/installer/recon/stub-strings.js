// Read-only: extract UTF-16LE and ASCII strings from the NSIS stub region
// (first N bytes), where installer metadata and UI text live.
const fs = require('node:fs');

const file = process.argv[2];
const bytesToScan = Number(process.argv[3] || 400000);
const fd = fs.openSync(file, 'r');
const buffer = Buffer.alloc(bytesToScan);
const read = fs.readSync(fd, buffer, 0, bytesToScan, 0);
fs.closeSync(fd);
const slice = buffer.subarray(0, read);

function utf16Strings(buf, minimum) {
  const out = [];
  let start = -1;
  for (let i = 0; i + 1 < buf.length; i += 2) {
    const code = buf.readUInt16LE(i);
    const printable = code >= 0x20 && code <= 0x7e;
    if (printable) {
      if (start < 0) start = i;
    } else if (start >= 0) {
      const text = buf.subarray(start, i).toString('utf16le');
      if (text.length >= minimum) out.push({ offset: start, text });
      start = -1;
    }
  }
  return out;
}

function asciiStrings(buf, minimum) {
  const out = [];
  let start = -1;
  for (let i = 0; i < buf.length; i += 1) {
    const byte = buf[i];
    const printable = byte >= 0x20 && byte <= 0x7e;
    if (printable) {
      if (start < 0) start = i;
    } else if (start >= 0) {
      const text = buf.subarray(start, i).toString('latin1');
      if (text.length >= minimum) out.push({ offset: start, text });
      start = -1;
    }
  }
  return out;
}

const utf16 = utf16Strings(slice, 4);
console.log(`UTF-16 strings (>=4 chars): ${utf16.length}`);
const interesting = utf16.filter((s) =>
  /city|rt\b|studio|games?|entertainment|version|publisher|company|product|unity|unreal|godot|copyright|install|setup/i.test(s.text),
);
for (const item of interesting.slice(0, 80)) {
  console.log(`  ${String(item.offset).padStart(7)}  ${JSON.stringify(item.text)}`);
}

console.log('\nASCII strings (>=6 chars) containing keywords:');
const ascii = asciiStrings(slice, 6);
const asciiInteresting = ascii.filter((s) =>
  /cityrt|\.dll|\.exe|unity|unreal|godot|mono|il2cpp|\.pak|\.pck|steam/i.test(s.text),
);
for (const item of asciiInteresting.slice(0, 60)) {
  console.log(`  ${String(item.offset).padStart(7)}  ${JSON.stringify(item.text)}`);
}
