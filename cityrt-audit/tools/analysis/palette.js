// Deterministic k-means palette and tonal statistics over decoded RGBA pixels.
const DEFAULT_STEP = 4;

function luma(r, g, b) {
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function toHex(r, g, b) {
  const part = (value) => Math.max(0, Math.min(255, Math.round(value))).toString(16).padStart(2, '0');
  return `#${part(r)}${part(g)}${part(b)}`;
}

function saturation(r, g, b) {
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  if (max === 0) return 0;
  return (max - min) / max;
}

function samplePixels(image, step) {
  const { rgba } = image;
  const pixels = [];
  for (let i = 0; i < rgba.length; i += 4 * step) {
    pixels.push([rgba[i], rgba[i + 1], rgba[i + 2]]);
  }
  return pixels;
}

function distance(a, b) {
  const dr = a[0] - b[0];
  const dg = a[1] - b[1];
  const db = a[2] - b[2];
  return dr * dr + dg * dg + db * db;
}

function seedCentroids(pixels, k) {
  const centroids = [pixels[0].slice()];
  while (centroids.length < k) {
    let best = null;
    let bestDistance = -1;
    for (const pixel of pixels) {
      let nearest = Infinity;
      for (const centroid of centroids) nearest = Math.min(nearest, distance(pixel, centroid));
      if (nearest > bestDistance) {
        bestDistance = nearest;
        best = pixel;
      }
    }
    if (!best) break;
    centroids.push(best.slice());
  }
  return centroids;
}

function extractPalette(image, options = {}) {
  const k = Math.max(1, options.k || 6);
  const iterations = Math.max(1, options.iterations || 12);
  const step = Math.max(1, options.step || DEFAULT_STEP);
  const pixels = samplePixels(image, step);

  const stats = (() => {
    let sumLuma = 0;
    let sumSaturation = 0;
    for (const [r, g, b] of pixels) {
      sumLuma += luma(r, g, b);
      sumSaturation += saturation(r, g, b);
    }
    const meanLuma = sumLuma / pixels.length;
    let variance = 0;
    let withinTwo = 0;
    for (const [r, g, b] of pixels) {
      const value = luma(r, g, b);
      variance += (value - meanLuma) ** 2;
      if (Math.abs(value - meanLuma) <= 2) withinTwo += 1;
    }
    return {
      meanLuma,
      meanSaturation: sumSaturation / pixels.length,
      lumaStdDev: Math.sqrt(variance / pixels.length),
      isBlank: withinTwo / pixels.length >= 0.95,
    };
  })();

  let centroids = seedCentroids(pixels, k);
  let assignments = new Array(pixels.length).fill(0);

  for (let iteration = 0; iteration < iterations; iteration += 1) {
    for (let i = 0; i < pixels.length; i += 1) {
      let nearest = 0;
      let bestDistance = Infinity;
      for (let c = 0; c < centroids.length; c += 1) {
        const d = distance(pixels[i], centroids[c]);
        if (d < bestDistance) {
          bestDistance = d;
          nearest = c;
        }
      }
      assignments[i] = nearest;
    }

    const sums = centroids.map(() => [0, 0, 0, 0]);
    for (let i = 0; i < pixels.length; i += 1) {
      const bucket = sums[assignments[i]];
      bucket[0] += pixels[i][0];
      bucket[1] += pixels[i][1];
      bucket[2] += pixels[i][2];
      bucket[3] += 1;
    }
    centroids = centroids.map((centroid, index) => {
      const [r, g, b, count] = sums[index];
      return count === 0 ? centroid : [r / count, g / count, b / count];
    });
  }

  const counts = centroids.map(() => 0);
  for (const assignment of assignments) counts[assignment] += 1;

  const colors = centroids
    .map((centroid, index) => ({
      hex: toHex(centroid[0], centroid[1], centroid[2]),
      rgb: [
        Math.round(centroid[0]),
        Math.round(centroid[1]),
        Math.round(centroid[2]),
      ],
      weight: counts[index] / pixels.length,
    }))
    .sort((a, b) => b.weight - a.weight);

  return { colors, stats };
}

module.exports = { extractPalette };
