// Minimal GLB (binary glTF 2.0) reader for measured geometry: counts, bounds.
class NotGlbError extends Error {
  constructor(reason) {
    super(`Not a glTF binary: ${reason}`);
    this.name = 'NotGlbError';
  }
}

function parseGlb(buffer) {
  if (!Buffer.isBuffer(buffer) || buffer.length < 12) throw new NotGlbError('too short');
  if (buffer.toString('ascii', 0, 4) !== 'glTF') throw new NotGlbError('missing glTF magic');
  const version = buffer.readUInt32LE(4);
  const totalLength = buffer.readUInt32LE(8);
  const end = Math.min(totalLength || buffer.length, buffer.length);

  let offset = 12;
  let json = null;
  while (offset + 8 <= end) {
    const chunkLength = buffer.readUInt32LE(offset);
    const chunkType = buffer.toString('ascii', offset + 4, offset + 8);
    const chunkStart = offset + 8;
    const chunkEnd = Math.min(chunkStart + chunkLength, end);
    if (chunkType === 'JSON') {
      json = JSON.parse(buffer.toString('utf8', chunkStart, chunkEnd).trim());
      break;
    }
    offset = chunkStart + chunkLength + ((4 - (chunkLength % 4)) % 4);
  }
  if (!json) throw new NotGlbError('no JSON chunk');

  let triangles = 0;
  let meshes = 0;
  const min = [Infinity, Infinity, Infinity];
  const max = [-Infinity, -Infinity, -Infinity];

  for (const mesh of json.meshes || []) {
    meshes += 1;
    for (const primitive of mesh.primitives || []) {
      const indices = primitive.indices !== undefined ? (json.accessors || [])[primitive.indices] : null;
      const position = (json.accessors || [])[(primitive.attributes || {}).POSITION];
      if (indices && indices.count) triangles += Math.floor(indices.count / 3);
      else if (position && position.count) triangles += Math.floor(position.count / 3);
      if (position && Array.isArray(position.min) && Array.isArray(position.max)) {
        for (let axis = 0; axis < 3; axis += 1) {
          min[axis] = Math.min(min[axis], position.min[axis]);
          max[axis] = Math.max(max[axis], position.max[axis]);
        }
      }
    }
  }

  const finite = min.every(Number.isFinite) && max.every(Number.isFinite);
  return {
    version,
    generator: (json.asset || {}).generator || null,
    meshes,
    triangles,
    materials: (json.materials || []).length,
    textures: (json.textures || []).length,
    nodes: (json.nodes || []).length,
    bounds: finite ? { min, max } : null,
    extensionsUsed: json.extensionsUsed || [],
  };
}

module.exports = { parseGlb, NotGlbError };
