// Read-only marker scan of a packaged executable: identifies the runtime/engine
// without extracting anything. Prints first offsets for each marker found.
const fs = require('node:fs');

const file = process.argv[2];
const markers = [
  'Godot Engine', 'godot', 'GODOT',
  'UnityPlayer', 'Unity Technologies', 'UnityEngine', 'il2cpp', 'global-metadata',
  'PyInstaller', 'MEIPASS', 'pyi-', 'python3',
  'NODE_SEA_BLOB', 'node:sea', 'Bun', 'bun-', 'deno',
  'Electron', 'app.asar', 'chromium',
  'UnrealEngine', 'UE4', 'UnrealEd', '.ucas', '.utoc',
  'CityRT', 'City RT',
  'OpenGL', 'Direct3D', 'Vulkan', 'SDL2', 'GLFW', 'sfml',
];

const limit = 128 * 1024 * 1024;
const fd = fs.openSync(file, 'r');
const size = fs.fstatSync(fd).size;
const chunkSize = 8 * 1024 * 1024;
const overlap = 64;
const found = new Map();

let position = 0;
let carry = Buffer.alloc(0);
const scanEnd = Math.min(size, limit);

while (position < scanEnd) {
  const want = Math.min(chunkSize, scanEnd - position);
  const chunk = Buffer.alloc(want);
  const read = fs.readSync(fd, chunk, 0, want, position);
  if (read <= 0) break;
  const buffer = Buffer.concat([carry, chunk.subarray(0, read)]);
  const baseOffset = position - carry.length;

  for (const marker of markers) {
    if (found.has(marker)) continue;
    const haystack = buffer.toString('latin1');
    const needle = marker;
    const index = haystack.indexOf(needle);
    if (index >= 0) found.set(marker, baseOffset + index);
  }
  carry = buffer.subarray(Math.max(0, buffer.length - overlap));
  position += read;
}
fs.closeSync(fd);

console.log('file size:', size);
console.log('scanned to:', scanEnd);
const sorted = [...found.entries()].sort((a, b) => a[1] - b[1]);
if (sorted.length === 0) console.log('no markers found');
for (const [marker, offset] of sorted) {
  console.log(`${String(offset).padStart(10)}  0x${offset.toString(16).padStart(8, '0')}  ${marker}`);
}
