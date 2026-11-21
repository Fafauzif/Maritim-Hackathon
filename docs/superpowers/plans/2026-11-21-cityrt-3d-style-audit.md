# CityRT 3D Style Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a complete, evidence-cited audit of CityRT's 3D style — all nine style personalities, their art direction, rendering technique, building language and simulation feel — plus a normative art bible and a Blender 5.2 kit specification, without running Blender.

**Architecture:** A Playwright harness drives the live cityrt.com client with Chrome, injecting WebGL hooks before any page script runs and exposing a CDP port so REA can inspect the same authenticated session. Per-style captures (screenshots, HAR with embedded bodies, shader sources, scene probes) feed dependency-free Node analysis modules — PNG decode, k-means palette, GLB parse — whose outputs are synthesized into the three deliverables. Every claim cites an evidence file by SHA-256.

**Tech Stack:** Node.js 24 (`node:test`, `node:zlib`, `node:crypto`), `playwright-core@1.64.1` (already present in the REA install), installed Google Chrome, REA MCP tools for JS/HAR/DOM inspection, Markdown deliverables.

**Spec:** `docs/superpowers/specs/2026-11-21-cityrt-style-audit-brief.md`

## Global Constraints

- Audit only: no Blender execution, no Blender MCP calls, no 3D asset authoring in this run.
- Never bypass the anti-bot pass or any challenge; a human may clear it in a visible window, and the harness must reuse that profile afterwards.
- Read-only on CityRT: no writes to other players' cities, no account creation, no purchases. If sign-in is required, stop and ask the requester.
- Extracted models, textures and shaders remain local under `cityrt-audit/evidence/` and are never redistributed; the future kit must be original geometry.
- Sequential capture only: one page at a time, ≥2000 ms between style loads.
- Tooling runs on system Node v24.19.0. REA CLI is `C:\Users\fauzi\AppData\Local\Programs\rea-node\rea.cmd`.
- Chrome is `C:\Program Files\Google\Chrome\Application\chrome.exe`. Playwright is `C:\Users\fauzi\AppData\Roaming\npm\node_modules\rea-agents\node_modules\playwright-core`.
- Evidence files above 50 MiB stay out of commits: record SHA-256, size and a locator instead.
- Every deliverable claim carries `evidence_id` = repo-relative path + SHA-256 from `cityrt-audit/evidence/manifest.json`.

## Review Focus

These are the failure modes most likely to produce a confident, wrong art bible. Each has an owning task and an explicit test.

1. **A challenge page is captured as if it were the game.** Anti-bot screens can contain a canvas or marketing art; treating them as style evidence poisons every downstream measurement. Owned by Task 7 (`classifyPage` unit test).
2. **The marketing hero page is captured instead of the 3D client.** Many browser games ship a landing page whose imagery is 2D concept art. Owned by Task 11 (canvas + draw-call gate).
3. **Software or blocked WebGL yields black or flat frames.** Headless Chromium without GPU flags renders empty scenes that still screenshot "successfully". Owned by Task 5 (renderer assertion) and Task 11 (blank gate).
4. **Capture happens before the scene populates.** First paint has terrain but no buildings, so palette and geometry are measured from an empty world. Owned by Task 11 (scene-ready predicate on draw calls and model load).
5. **Style never changes because of persisted state.** If the style lives in `localStorage` or a URL param and is not reset, all nine captures silently show one style. Owned by Task 11 (fresh storage state plus distinct style-token assertion).

---

## File Structure

```
cityrt-audit/
  README.md                      # how to run the harness and reproduce the audit
  evidence/
    manifest.json                # index: path, sha256, bytes, kind, producedBy, proves
    reachability/                # Task 7 output: classification, screenshot, HAR
    scripts/                     # Task 8: exported JS bundles
    styles/<style-id>/           # Task 11: screenshots, HAR, probe.json, notes.md
    models/                      # Task 12: extracted GLB samples (bounded)
    installer/                   # Task 6: NSIS listing and shell inventory
  analysis/
    renderer/                    # Task 8-9: bundle graph, renderer verdict
    styles/styles.json           # Task 9: the nine style definitions
    constants.json               # Task 10: extracted numeric constants + citations
    palette/<style-id>.json      # Task 13
    asset-inventory.json         # Task 12
    rendering/pipeline.md        # Task 14
    geometry/building-language.md, metrics.json   # Task 15
    simulation/simulation.md, timeseries.json     # Task 16
  tools/
    manifest.js                  # Task 1
    styles.js                    # Task 9: style definition validator
    inventory.js                 # Task 12: asset classification and HAR summary
    coverage.js                  # Task 20: evidence-reference checker
    analysis/png.js              # Task 2
    analysis/palette.js          # Task 3
    analysis/glb.js              # Task 4
    browser/probe.js             # Task 5
    browser/session.js           # Task 7
    browser/styles.js            # Task 11
    browser/timeseries.js        # Task 16
    report/matrix.js             # Task 17
    report/palette-report.js     # Task 13
    report/shaders.js            # Task 14
    report/geometry.js           # Task 15
  tests/                         # node:test suites, one file per module
    fixtures/                    # probe.html, challenge.html, landing.html, coverage-bad/
  docs/
    STYLE-MATRIX.md              # Task 17
    ART-BIBLE.md                 # Task 18
    KIT-SPEC.md                  # Task 19
    UNKNOWNS.md                  # Task 20
    COVERAGE.md                  # Task 20
```

Deliverables are `docs/STYLE-MATRIX.md`, `docs/ART-BIBLE.md`, `docs/KIT-SPEC.md`; `UNKNOWNS.md` and `COVERAGE.md` are the audit's honesty controls.

## Phase gates

- **Gate A (after Task 7):** if the page classifies as `challenge`, stop and ask the requester to clear it in the visible browser; do not continue measuring.
- **Gate B (after Task 11):** if fewer than nine styles can be captured, stop and report which are gated; never fabricate a style from one screenshot.
- **Gate C (after Task 15):** if no served 3D models are recoverable, geometry claims must come from screenshot measurement only and must be labelled `inferred`.

---

## Phase 0 — Groundwork

### Task 1: Audit scaffold, git baseline, evidence manifest

**Files:**
- Create: `cityrt-audit/README.md`, `cityrt-audit/evidence/manifest.json`, `cityrt-audit/tools/manifest.js`, `cityrt-audit/tests/manifest.test.js`
- Create: `cityrt-audit/.gitignore` with `.profile/`, `evidence/**/*.har`, `evidence/models/` — large captures stay out of git and are referenced by SHA-256 instead

**Interfaces:**
- Produces: `addEvidence(entry: {path: string, kind: string, producedBy: string, proves: string}) -> {path, sha256, bytes}`, `writeManifest(rootDir: string) -> string`, `readManifest(rootDir: string) -> {entries: EvidenceEntry[]}`

- [ ] **Step 1: Initialise the repository**

The 111 MB installer stays untracked: it is an input, not a deliverable, and git must not carry it.

```powershell
cd 'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon'
git init
git add docs
git commit -m "docs: add CityRT audit brief"
```

- [ ] **Step 2: Write the failing test for the manifest module**

```javascript
// cityrt-audit/tests/manifest.test.js
const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { addEvidence, writeManifest, readManifest } = require('../tools/manifest.js');

test('manifest records sha256, dedupes identical paths, and sorts by path', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'cityrt-'));
  fs.writeFileSync(path.join(root, 'b.txt'), 'beta');
  fs.writeFileSync(path.join(root, 'a.txt'), 'alpha');
  addEvidence({ path: path.join(root, 'b.txt'), kind: 'text', producedBy: 'test', proves: 'b' });
  addEvidence({ path: path.join(root, 'a.txt'), kind: 'text', producedBy: 'test', proves: 'a' });
  addEvidence({ path: path.join(root, 'b.txt'), kind: 'text', producedBy: 'test', proves: 'b again' });
  const written = writeManifest(root);
  const manifest = JSON.parse(fs.readFileSync(written, 'utf8'));
  assert.strictEqual(manifest.entries.length, 2);
  assert.deepStrictEqual(manifest.entries.map((e) => path.basename(e.path)), ['a.txt', 'b.txt']);
  assert.match(manifest.entries[0].sha256, /^[0-9a-f]{64}$/);
});
```

- [ ] **Step 3: Run the test and confirm it fails**

Run: `node --test cityrt-audit/tests/manifest.test.js`
Expected: FAIL — `Cannot find module '../tools/manifest.js'`.

- [ ] **Step 4: Implement `cityrt-audit/tools/manifest.js`**

Exports the three functions above using `node:crypto` `createHash('sha256')`, keyed by absolute path, replaced on re-add, sorted by repository-relative path, written as `{ generatedAt, entries }` with two-space JSON.

- [ ] **Step 5: Verify the test passes**

Run: `node --test cityrt-audit/tests/manifest.test.js`
Expected: PASS, 1 test.

- [ ] **Step 6: Commit**

```powershell
git add cityrt-audit
git commit -m "feat: audit scaffold with sha256 evidence manifest"
```

### Task 2: PNG decoder for measured colour work

**Files:**
- Create: `cityrt-audit/tools/analysis/png.js`, `cityrt-audit/tests/png.test.js`

**Interfaces:**
- Produces: `decodePng(buffer: Buffer) -> {width: number, height: number, rgba: Uint8Array}`
- Supports: bit depth 8, colour types 2 (RGB) and 6 (RGBA), all five filter types, no interlacing. Any other input throws `UnsupportedPngError` with the reason.

- [ ] **Step 1: Write the failing test, including a tiny PNG encoder helper**

```javascript
// cityrt-audit/tests/png.test.js
const test = require('node:test');
const assert = require('node:assert');
const zlib = require('node:zlib');
const { decodePng } = require('../tools/analysis/png.js');

// Helper: table-driven CRC-32 plus the four chunks (signature, IHDR, IDAT, IEND).
// Chunk payloads are fixed by the PNG spec; only the pixel data varies per call.
function crc32(buffer) { /* ... */ }

function encodePng(width, height, pixels /* [[r,g,b], ...] */) {
  const raw = Buffer.alloc(height * (1 + width * 3));
  for (let y = 0; y < height; y += 1) {
    raw[y * (1 + width * 3)] = 0; // filter: none
    for (let x = 0; x < width; x += 1) {
      const [r, g, b] = pixels[y * width + x];
      const o = y * (1 + width * 3) + 1 + x * 3;
      raw[o] = r; raw[o + 1] = g; raw[o + 2] = b;
    }
  }
  // IHDR (bit depth 8, colour type 2) + IDAT + IEND chunks with real CRC-32
  return Buffer.concat([signature, ihdrChunk, idatChunk, iendChunk]);
}

test('decodes a 2x2 RGB PNG into RGBA', () => {
  const png = encodePng(2, 2, [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 255]]);
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
```

- [ ] **Step 2: Run to confirm failure**

Run: `node --test cityrt-audit/tests/png.test.js`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `decodePng`**

Parse IHDR, concatenate IDAT, `zlib.inflateSync`, then unfilter rows (filters 0–4: None, Sub, Up, Average, Paeth) and expand RGB to RGBA with alpha 255.

- [ ] **Step 4: Verify both tests pass**

Run: `node --test cityrt-audit/tests/png.test.js`
Expected: PASS, 2 tests.

- [ ] **Step 5: Commit**

```powershell
git add cityrt-audit/tools/analysis/png.js cityrt-audit/tests/png.test.js
git commit -m "feat: dependency-free PNG decoder for colour measurement"
```

### Task 3: Palette and tonal analysis

**Files:**
- Create: `cityrt-audit/tools/analysis/palette.js`, `cityrt-audit/tests/palette.test.js`

**Interfaces:**
- Consumes: `decodePng` from Task 2.
- Produces: `extractPalette(image: {width, height, rgba}, options?: {k?: number, iterations?: number, step?: number}) -> {colors: {hex: string, rgb: [number, number, number], weight: number}[], stats: {meanLuma: number, meanSaturation: number, lumaStdDev: number, isBlank: boolean}}`
- Determinism: seeded initialisation (first pixel plus max-distance seeding), so identical input yields identical palette.
- `isBlank` is true when ≥95 % of sampled pixels lie within 2 luma units of the mean.

- [ ] **Step 1: Write the failing test**

```javascript
// cityrt-audit/tests/palette.test.js
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
```

- [ ] **Step 2: Run to confirm failure**

Run: `node --test cityrt-audit/tests/palette.test.js`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `extractPalette`**

k-means in RGB with deterministic seeding, `step` sampling (default 4 pixels), hex output lower-case, weight = cluster share, plus luma/saturation statistics using Rec. 709 weights.

- [ ] **Step 4: Verify tests pass and palette is deterministic**

Run: `node --test cityrt-audit/tests/palette.test.js`
Expected: PASS, 2 tests.

- [ ] **Step 5: Commit**

```powershell
git add cityrt-audit/tools/analysis/palette.js cityrt-audit/tests/palette.test.js
git commit -m "feat: deterministic k-means palette and blank-frame detection"
```

### Task 4: GLB parser for measured geometry

**Files:**
- Create: `cityrt-audit/tools/analysis/glb.js`, `cityrt-audit/tests/glb.test.js`

**Interfaces:**
- Produces: `parseGlb(buffer: Buffer) -> {version: number, generator: string|null, meshes: number, triangles: number, materials: number, textures: number, bounds: {min: [number,number,number], max: [number,number,number]}, extensionsUsed: string[]}`
- Throws `NotGlbError` when the magic is not `glTF`.

- [ ] **Step 1: Write the failing test with a handcrafted GLB**

```javascript
// cityrt-audit/tests/glb.test.js
const test = require('node:test');
const assert = require('node:assert');
const { parseGlb } = require('../tools/analysis/glb.js');

function buildGlb(json) {
  const jsonChunk = Buffer.from(JSON.stringify(json), 'utf8');
  const paddedJson = Buffer.concat([jsonChunk, Buffer.alloc((4 - (jsonChunk.length % 4)) % 4, 0x20)]);
  const header = Buffer.alloc(12);
  header.write('glTF', 0, 'ascii');
  header.writeUInt32LE(2, 4);
  header.writeUInt32LE(12 + 8 + paddedJson.length, 8);
  const chunk = Buffer.alloc(8);
  chunk.writeUInt32LE(paddedJson.length, 0);
  chunk.write('JSON', 4, 'ascii');
  return Buffer.concat([header, chunk, paddedJson]);
}

test('reads meshes, triangle count and union bounds', () => {
  const glb = buildGlb({
    asset: { version: '2.0', generator: 'CityRT-Test' },
    meshes: [{ primitives: [{ indices: { count: 36 }, attributes: { POSITION: 0 } }] }],
    accessors: [{ type: 'VEC3', min: [-2, 0, -2], max: [2, 6, 2] }],
    materials: [{}, {}],
  });
  const model = parseGlb(glb);
  assert.strictEqual(model.version, 2);
  assert.strictEqual(model.generator, 'CityRT-Test');
  assert.strictEqual(model.triangles, 12);
  assert.deepStrictEqual(model.bounds.min, [-2, 0, -2]);
  assert.deepStrictEqual(model.bounds.max, [2, 6, 2]);
});

test('rejects non-GLB input', () => {
  assert.throws(() => parseGlb(Buffer.from('not a model')), /glTF/i);
});
```

- [ ] **Step 2: Run to confirm failure**

Run: `node --test cityrt-audit/tests/glb.test.js`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `parseGlb`**

Validate magic/version, extract the JSON chunk, count primitives, derive triangles as `indices.count / 3` (or `POSITION.count / 3` when unindexed), union every POSITION accessor `min`/`max`, collect `extensionsUsed`.

- [ ] **Step 4: Verify tests pass**

Run: `node --test cityrt-audit/tests/glb.test.js`
Expected: PASS, 2 tests.

- [ ] **Step 5: Commit**

```powershell
git add cityrt-audit/tools/analysis/glb.js cityrt-audit/tests/glb.test.js
git commit -m "feat: GLB parser for measured building geometry"
```

### Task 5: WebGL probe — renderer identity, shader capture, draw-call counters

**Files:**
- Create: `cityrt-audit/tools/browser/probe.js`, `cityrt-audit/tests/fixtures/probe.html`, `cityrt-audit/tests/probe.test.js`

**Interfaces:**
- Produces: `installProbe(page) -> Promise<void>` (installs `page.addInitScript` hooks before navigation) and `dumpProbe(page) -> Promise<ProbeDump>`
- `ProbeDump = {renderer: string|null, vendor: string|null, contextAttributes: object|null, shaders: {hash: string, vertex: string, fragment: string}[], drawCalls: number, frames: number, canvas: {width: number, height: number}|null}`
- Hooks: `WebGLRenderingContext`/`WebGL2RenderingContext` `shaderSource`, `getParameter`, `drawElements`, `drawArrays`, plus `requestAnimationFrame` counting. No page behaviour is modified beyond counters.

- [ ] **Step 1: Write the failing test against a local fixture**

```javascript
// cityrt-audit/tests/probe.test.js
const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_CORE);
const { installProbe, dumpProbe } = require('../tools/browser/probe.js');

test('captures renderer string, one shader pair and draw calls', async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    args: ['--use-gl=angle', '--use-angle=swiftshader'],
  });
  const page = await browser.newPage();
  await installProbe(page);
  await page.goto('file://' + path.join(__dirname, 'fixtures', 'probe.html'));
  await page.waitForFunction(() => window.__probeReady === true, null, { timeout: 15000 });
  const dump = await dumpProbe(page);
  assert.match(String(dump.renderer), /swiftshader|angle|direct3d|opengl|vulkan/i);
  assert.strictEqual(dump.shaders.length, 1);
  assert.match(dump.shaders[0].fragment, /gl_FragColor|fragColor/);
  assert.ok(dump.drawCalls >= 1);
  await browser.close();
});
```

Fixture `probe.html` compiles one trivial GLSL program and issues one `drawArrays` inside `requestAnimationFrame`, then sets `window.__probeReady = true`.

- [ ] **Step 2: Run to confirm failure**

Run: `$env:PLAYWRIGHT_CORE='C:\Users\fauzi\AppData\Roaming\npm\node_modules\rea-agents\node_modules\playwright-core'; node --test cityrt-audit/tests/probe.test.js`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `probe.js`**

`addInitScript` defining `window.__cityrtProbe = {shaders: [], drawCalls: 0, frames: 0}` and wrapping the prototypes; `dumpProbe` reads the accumulated state and pairs vertex/fragment sources by program object identity using a `WeakMap`.

- [ ] **Step 4: Verify the test passes**

Run: same command as Step 2.
Expected: PASS, 1 test. Swiftshader is acceptable for the fixture; Task 11 asserts real GPU on the live site.

- [ ] **Step 5: Commit**

```powershell
git add cityrt-audit/tools/browser/probe.js cityrt-audit/tests
git commit -m "feat: WebGL probe for renderer identity, shaders and draw calls"
```

### Task 6: Installer forensics (shell only)

The live site is the target, so this task answers one question: what does the desktop shell add that the browser does not (user agent, flags, injected scripts, feature toggles)?

**Files:**
- Create: `cityrt-audit/evidence/installer/listing.txt`, `cityrt-audit/analysis/renderer/shell.md`

**Interfaces:**
- Consumes: `CityRT-Windows.exe`.
- Produces: a short `shell.md` stating shell type, version, payload start, and whether any 3D content or renderer configuration ships locally.

- [ ] **Step 1: Install 7-Zip (approved by the requester)**

```powershell
winget install --id 7zip.7zip -e --accept-package-agreements --accept-source-agreements
```

Expected: `Successfully installed`.

- [ ] **Step 2: List the installer payload without extraction**

```powershell
& 'C:\Program Files\7-Zip\7z.exe' l 'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\CityRT-Windows.exe' | Tee-Object cityrt-audit\evidence\installer\listing.txt
```

Expected: entries including `resources\app.asar` (Electron), or a payload whose top-level names identify another shell. Record the exact list.

- [ ] **Step 3: Classify the shell and note the version**

Write `analysis/renderer/shell.md` with shell type, version, main executable size, and whether `app.asar` exists. If it exists, extract only `package.json` and any preload/main script to `evidence/installer/` and record their hashes through the manifest.

- [ ] **Step 4: Register evidence and commit**

```powershell
node -e "const m=require('./cityrt-audit/tools/manifest.js'); m.addEvidence({path:'cityrt-audit/evidence/installer/listing.txt',kind:'text',producedBy:'7z',proves:'installer payload inventory'}); m.writeManifest('cityrt-audit')"
git add cityrt-audit
git commit -m "docs: classify desktop shell and record installer payload"
```

---

## Phase 1 — Access and static truth

### Task 7: Reachability, anti-bot policy, and CDP-attachable session

**Files:**
- Create: `cityrt-audit/tools/browser/session.js`, `cityrt-audit/tests/session.test.js`, `cityrt-audit/tests/fixtures/challenge.html`, `cityrt-audit/tests/fixtures/landing.html`
- Produces: `cityrt-audit/evidence/reachability/report.json`, `page.png`, `session.har`

**Interfaces:**
- Produces: `classifyPage(page) -> Promise<'game'|'landing'|'challenge'>`, `openSession(options: {profileDir: string, harPath: string, headless?: boolean, debugPort?: number}) -> Promise<{context, page}>`
- `openSession` must always launch with `--remote-debugging-port={debugPort}` (default 9222) so REA attaches to the same session, and `recordHar: {path: harPath, mode: 'full', content: 'embed'}`.

- [ ] **Step 1: Write the failing classifier test**

```javascript
// cityrt-audit/tests/session.test.js
const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_CORE);
const { classifyPage } = require('../tools/browser/session.js');

test('classifies anti-bot text without canvas as challenge', async () => {
  const browser = await chromium.launch({ executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' });
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'fixtures', 'challenge.html'));
  assert.strictEqual(await classifyPage(page), 'challenge');
  await browser.close();
});

test('classifies a page with no canvas and no challenge text as landing', async () => {
  const browser = await chromium.launch({ executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' });
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'fixtures', 'landing.html'));
  assert.strictEqual(await classifyPage(page), 'landing');
  await browser.close();
});
```

`challenge.html` contains "Anti-Bot Pass" plus "verify you are human"; `landing.html` contains marketing copy and no canvas.

- [ ] **Step 2: Run to confirm failure**

Run: `$env:PLAYWRIGHT_CORE='C:\Users\fauzi\AppData\Roaming\npm\node_modules\rea-agents\node_modules\playwright-core'; node --test cityrt-audit/tests/session.test.js`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `classifyPage` and `openSession`**

Classification order: (a) challenge if body text matches `/anti-bot|captcha|verify you are human|капча|подтвердите/i` **or** the URL matches `/pass/i`, unless a live WebGL canvas with draw calls ≥ 100 is present; (b) game if a canvas exists and the probe reports `canvas.width > 0` and `drawCalls > 100`; (c) otherwise landing. `openSession` uses `launchPersistentContext(profileDir, {channel: 'chrome', headless: false, recordHar, args})`.

- [ ] **Step 4: Verify tests pass**

Run: `$env:PLAYWRIGHT_CORE='C:\Users\fauzi\AppData\Roaming\npm\node_modules\rea-agents\node_modules\playwright-core'; node --test cityrt-audit/tests/session.test.js`
Expected: PASS, 2 tests.

- [ ] **Step 5: Open the live site and classify it**

```powershell
node cityrt-audit/tools/browser/session.js --open https://cityrt.com/en/ --profile cityrt-audit/.profile --har cityrt-audit/evidence/reachability/session.har
```

Expected for the `game` case: `report.json` records `classification: "game"`, `renderer` from the probe, screenshot saved. **Gate A:** on `challenge`, stop, ask the requester to complete the pass in the visible window, then re-run this step; on `landing`, record it and continue to Task 8 to find the client route, then return here.

- [ ] **Step 6: Confirm REA can attach to the same session**

Call `list_browser_targets` with `cdp_endpoint: http://127.0.0.1:9222` and expect the CityRT page target; then `inspect_web_page` for that target and record the DOM/script counts in `report.json`.

- [ ] **Step 7: Commit**

```powershell
git add cityrt-audit
git commit -m "feat: reachability harness with challenge classification and CDP sharing"
```

### Task 8: Static bundle truth — renderer and module map

**Files:**
- Create: `cityrt-audit/evidence/scripts/` (exported bundles), `cityrt-audit/evidence/reachability/page-capture.json`, `cityrt-audit/analysis/renderer/bundle.json`, `cityrt-audit/analysis/renderer/renderer-verdict.md`

**Interfaces:**
- Consumes: the CDP-attached page from Task 7.
- Produces: `renderer-verdict.md` answering — Three.js / Babylon.js / PlayCanvas / Unity wasm / custom WebGL, version where determinable, and the module that owns styles, with citations (`script URL` + byte offset or symbol path).

- [ ] **Step 1: Save a page capture, then export scripts with REA**

Call `inspect_web_page` with `include_script_sources: true` against the CDP target, write the returned result to `evidence/reachability/page-capture.json`, then call `export_web_scripts` with `capture_path` set to that file and `output_directory` `cityrt-audit/evidence/scripts`. Expected: a manifest listing every captured script URL and digest. If `export_web_scripts` cannot use that file shape, fall back to downloading each `Content-Type: javascript` response observed in the Task 11 HAR into `evidence/scripts/`.

- [ ] **Step 2: Build the static application graph**

Call `analyze_javascript_application` with `input_path` = the exported scripts directory and `detail: summary`. Expected: nodes and edges for modules, imports and routes; save the summary reference in `bundle.json`.

- [ ] **Step 3: Identify the renderer and the style registry**

Search the exported sources for `THREE`, `WebGLRenderer`, `MeshStandardMaterial`, `babylon`, `pc.Application`, `unityloader`, `wasm`. Record the winning family with file and offset. Locate the structure holding the nine styles (search for `styles`, `themes`, `styleId`, `setStyle`) and record how a style is selected.

- [ ] **Step 4: Write the verdict with citations**

`renderer-verdict.md` states the renderer family, version evidence, style-selection mechanism, and every unknown explicitly (for example "minified module names prevent mapping to original files; source maps absent").

- [ ] **Step 5: Commit**

```powershell
git add cityrt-audit
git commit -m "analysis: renderer verdict and style-selection mechanism from static bundles"
```

### Task 9: Enumerate the nine styles

**Files:**
- Create: `cityrt-audit/analysis/styles/styles.json`, `cityrt-audit/tools/styles.js`, `cityrt-audit/tests/styles.test.js`

**Interfaces:**
- Produces: `validateStyles(styles: StyleEntry[]) -> {ok: boolean, errors: string[]}` where `StyleEntry = {id: string, name: string, evidence: string[], select: {kind: 'url'|'storage'|'click', value: string}}`
- Constraint: exactly nine entries, unique `id`, every `select` recipe executable by Task 11.

- [ ] **Step 1: Write the failing validator test**

```javascript
// cityrt-audit/tests/styles.test.js
const test = require('node:test');
const assert = require('node:assert');
const { validateStyles } = require('../tools/styles.js');

const valid = Array.from({ length: 9 }, (_, i) => ({
  id: `style-${i}`, name: `Style ${i}`, evidence: ['analysis/renderer/renderer-verdict.md'],
  select: { kind: 'url', value: `?style=style-${i}` },
}));

test('accepts nine unique styles', () => {
  assert.deepStrictEqual(validateStyles(valid), { ok: true, errors: [] });
});

test('rejects eight styles and duplicate ids', () => {
  assert.strictEqual(validateStyles(valid.slice(0, 8)).ok, false);
  const duplicated = valid.map((s) => ({ ...s, id: 'same' }));
  const result = validateStyles(duplicated);
  assert.strictEqual(result.ok, false);
  assert.match(result.errors.join(' '), /duplicate/i);
});
```

- [ ] **Step 2: Run to confirm failure**

Run: `node --test cityrt-audit/tests/styles.test.js`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `validateStyles` and collect the real nine**

Implement the validator, then extract the actual style ids/names from the static graph (Task 8), the `/en/styles` page data, or the in-game picker DOM. Write `styles.json` with a `select` recipe per style; if a recipe cannot be executed programmatically, record `kind: 'click'` with a stable text selector.

- [ ] **Step 4: Verify the test passes and the file validates**

Run: `node --test cityrt-audit/tests/styles.test.js` then `node -e "console.log(require('./cityrt-audit/tools/styles.js').validateStyles(require('./cityrt-audit/analysis/styles/styles.json')).ok)"`
Expected: PASS, and `true`.

- [ ] **Step 5: Commit**

```powershell
git add cityrt-audit
git commit -m "analysis: enumerate the nine style personalities with selection recipes"
```

### Task 10: Harvest numeric constants with citations

**Files:**
- Create: `cityrt-audit/analysis/constants.json`

**Interfaces:**
- Produces: entries shaped `{key: string, value: number|string, unit: string, source: {script: string, offset: number}, note?: string}` covering renderer settings, lighting, fog, camera, materials, and simulation timing.

- [ ] **Step 1: Search the bundles for renderer and lighting configuration**

Look for `toneMapping`, `toneMappingExposure`, `outputColorSpace`, `shadowMap`, `antialias`, `pixelRatio`, `Fog`, `HemisphereLight`, `DirectionalLight`, `AmbientLight`, `camera = new`.

- [ ] **Step 2: Search for simulation constants**

Look for `tick`, `stepInterval`, `speed`, `setInterval(`, `requestAnimationFrame` throttles, growth/budget intervals, day-length or `timeOfDay` constants, camera `minZoom`/`maxZoom`/`damping`.

- [ ] **Step 3: Record every hit with file and offset, and mark absences**

Write `constants.json`; where a value is inferred from a call site rather than a literal, set `note: "inferred from call site"`. Absences stay in the file as `value: "not found"` so Task 20 can report them.

- [ ] **Step 4: Cross-check one value per category in the browser**

For tone mapping, exposure, fog and camera FOV, confirm by evaluating the live renderer if it is reachable on `window` (for example `window.__renderer` or a module registry); if unreachable, record `unverified`.

- [ ] **Step 5: Commit**

```powershell
git add cityrt-audit/analysis/constants.json
git commit -m "analysis: cited renderer, lighting, camera and simulation constants"
```

---

## Phase 2 — Per-style capture

### Task 11: Style capture runner

**Files:**
- Create: `cityrt-audit/tools/browser/styles.js`, `cityrt-audit/tests/styles-runner.test.js`
- Produces: `cityrt-audit/evidence/styles/<style-id>/{overview.png, mid.png, street.png, night.png, session.har, probe.json, notes.md}`

**Interfaces:**
- Produces: `captureStyle(browser, style: StyleEntry, outDir: string) -> Promise<{styleToken: string, screenshots: string[], har: string, probe: ProbeDump}>`, `styleToken(style: StyleEntry) -> string`, and `sceneReady(probe: ProbeDump, previous?: ProbeDump) -> boolean`
- Scene-ready predicate: `drawCalls >= 500` **and** at least one network response with `content-type` `model/gltf-binary` observed **and** two consecutive probe dumps 500 ms apart with draw calls within ±10 %.
- Blank gate: every screenshot must return `stats.isBlank === false` from Task 3.

- [ ] **Step 1: Write the failing test for the freshness gate**

```javascript
// cityrt-audit/tests/styles-runner.test.js
const test = require('node:test');
const assert = require('node:assert');
const { styleToken, sceneReady } = require('../tools/browser/styles.js');

test('different styles produce different tokens', () => {
  assert.notStrictEqual(
    styleToken({ id: 'a', name: 'Alpha', select: { kind: 'url', value: '?style=a' } }),
    styleToken({ id: 'b', name: 'Beta', select: { kind: 'url', value: '?style=b' } }),
  );
});

test('identical style definitions produce identical tokens', () => {
  const style = { id: 'a', name: 'Alpha', select: { kind: 'url', value: '?style=a' } };
  assert.strictEqual(styleToken(style), styleToken(style));
});

test('an unpopulated scene is not ready even when a canvas exists', () => {
  const empty = { renderer: 'ANGLE', drawCalls: 12, frames: 3, canvas: { width: 1280, height: 720 }, shaders: [] };
  assert.strictEqual(sceneReady(empty), false);
});

test('a populated, stable scene is ready', () => {
  const first = { renderer: 'ANGLE', drawCalls: 900, frames: 60, canvas: { width: 1280, height: 720 }, shaders: [] };
  const second = { renderer: 'ANGLE', drawCalls: 905, frames: 62, canvas: { width: 1280, height: 720 }, shaders: [] };
  assert.strictEqual(sceneReady(second, first), true);
});
```

- [ ] **Step 2: Run to confirm failure**

Run: `node --test cityrt-audit/tests/styles-runner.test.js`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement the runner**

`captureStyle` creates a **fresh context per style** (`browser.newContext({recordHar})`, no shared storage), installs the probe, applies the selection recipe, waits for the scene-ready predicate with a 120 s cap, then captures the four screenshots and probe dump. On timeout it throws `SceneNotReadyError` with the last draw-call count — it never saves a screenshot as if it were valid. The blank gate reuses `extractPalette(...).stats.isBlank` (proven by the Task 3 test) and throws `BlankFrameError` instead of writing a black image into the evidence set.

- [ ] **Step 4: Verify the unit tests pass**

Run: `node --test cityrt-audit/tests/styles-runner.test.js`
Expected: PASS, 4 tests.

- [ ] **Step 5: Capture all nine styles**

```powershell
node cityrt-audit/tools/browser/styles.js --styles cityrt-audit/analysis/styles/styles.json --out cityrt-audit/evidence/styles --profile cityrt-audit/.profile
```

Expected: nine directories, each with four PNGs plus HAR and probe. **Gate B:** if a style cannot reach the scene-ready predicate, write `notes.md` with the reason and continue; report the gap rather than substituting another style's images.

- [ ] **Step 6: Verify freshness and non-blankness mechanically**

For each style directory, assert `probe.styleToken` differs from every other style's token, and every screenshot passes the blank gate. Record the table in `evidence/styles/capture-report.json`.

- [ ] **Step 7: Commit**

```powershell
git add cityrt-audit
git commit -m "feat: per-style capture runner with scene-ready and freshness gates"
```

### Task 12: Asset inventory and bounded model extraction

**Files:**
- Create: `cityrt-audit/analysis/asset-inventory.json`, `cityrt-audit/tools/inventory.js`, `cityrt-audit/tests/inventory.test.js`
- Produces: `cityrt-audit/evidence/models/*.glb` (bounded sample) and per-kind counts.

**Interfaces:**
- Produces: `classifyAsset(url: string, contentType: string|null) -> 'model'|'texture'|'script'|'style'|'audio'|'data'|'other'`, `summarizeHars(paths: string[]) -> {kinds: Record<string, {count: number, bytes: number, uniqueHashes: number}>, models: {url: string, sha256: string, bytes: number}[]}`

- [ ] **Step 1: Write the failing classifier test**

```javascript
// cityrt-audit/tests/inventory.test.js
const test = require('node:test');
const assert = require('node:assert');
const { classifyAsset } = require('../tools/inventory.js');

test('classifies by extension and mime', () => {
  assert.strictEqual(classifyAsset('/a/b.glb', 'model/gltf-binary'), 'model');
  assert.strictEqual(classifyAsset('/a/b.ktx2', null), 'texture');
  assert.strictEqual(classifyAsset('/a/b.js', 'application/javascript'), 'script');
  assert.strictEqual(classifyAsset('/a/b.webp', 'image/webp'), 'texture');
  assert.strictEqual(classifyAsset('/a/b.bin', null), 'other');
});
```

- [ ] **Step 2: Run to confirm failure**

Run: `node --test cityrt-audit/tests/inventory.test.js`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement classification and HAR summarising**

Decode each per-style HAR, classify every response, dedupe by body SHA-256, and write `asset-inventory.json` with counts, bytes and unique hashes per kind plus a `models` list.

- [ ] **Step 4: Extract a bounded model sample**

Extract up to 200 GLB bodies (each ≤ 5 MiB) to `evidence/models/`, naming files by SHA-256, and register them through the manifest. Expected: at least one file if the game streams glTF; if zero, record `models: 0` and set the Gate C flag.

- [ ] **Step 5: Verify and commit**

Run: `node --test cityrt-audit/tests/inventory.test.js`
Expected: PASS, 1 test.

```powershell
git add cityrt-audit/analysis/asset-inventory.json cityrt-audit/tools/inventory.js cityrt-audit/tests/inventory.test.js
git commit -m "analysis: asset inventory and bounded model extraction"
```

---

## Phase 3 — Measurement

### Task 13: Palette, tonal range and lighting direction per style

**Files:**
- Create: `cityrt-audit/tools/report/palette-report.js`, `cityrt-audit/analysis/palette/<style-id>.json`, `cityrt-audit/analysis/palette/summary.md`

**Interfaces:**
- Consumes: `decodePng` (Task 2), `extractPalette` (Task 3), `evidence/styles/<id>/*.png` (Task 11).
- Produces: per style `{styleId, images: {name: PaletteResult}, combined: {colors: [...], stats: {...}}}` plus a Markdown summary table.

- [ ] **Step 1: Run the extraction over all captured images**

For each style and each screenshot, compute a 6-colour palette plus luma/saturation statistics; merge per style by weight.

- [ ] **Step 2: Derive lighting direction and contrast per style**

Using the `mid.png` frame, compare upper-quadrant versus lower-quadrant mean luma to infer sky-dominance and vertical gradient, and record shadow-side darkening as the ratio p5/p50 luma. Mark both as `derived`, not measured radiometry.

- [ ] **Step 3: Emit per-style JSON and a summary table**

Write `analysis/palette/<id>.json` and a summary table with columns style, top three hexes, mean luma, saturation, contrast ratio.

- [ ] **Step 4: Verify every style has an entry**

Run: `node -e "const fs=require('fs');const f=fs.readdirSync('cityrt-audit/analysis/palette').filter(x=>x.endsWith('.json'));console.log(f.length)"`
Expected: `9` (or the number of styles successfully captured, with the gap explained in `UNKNOWNS.md`).

- [ ] **Step 5: Commit**

```powershell
git add cityrt-audit/analysis/palette cityrt-audit/tools/report/palette-report.js
git commit -m "analysis: per-style palette and tonal measurements"
```

### Task 14: Shader pipeline reconstruction

**Files:**
- Create: `cityrt-audit/analysis/rendering/pipeline.md`, `cityrt-audit/tools/report/shaders.js`

**Interfaces:**
- Consumes: `probe.json` shader arrays (Task 5/11), exported scripts (Task 8).
- Produces: a documented pass chain and a technique verdict: NPR vs PBR, outline method, AO/shadow technique, tone mapping, fog model.

- [ ] **Step 1: Cluster captured shaders by hash**

Group identical shader pairs across styles; count how many are variants of one base material.

- [ ] **Step 2: Identify engine built-ins versus custom passes**

Match `#include <...>` guards and known chunk names to classify as engine built-in; any shader with no includes is a custom pass candidate.

- [ ] **Step 3: Detect post-processing and outlines**

Look for full-screen quad patterns (`vUv`, `gl_FragCoord`), named effects (bloom, vignette, SMAA, FXAA, SSAO, outline, sobel), and inverted-hull outline signatures (front-face culling with expanded normals).

- [ ] **Step 4: Write `pipeline.md` with a mermaid diagram and one citation per stage**

Each stage cites the shader hash and the style in which it was observed; stages never observed are listed as absent with the styles checked.

- [ ] **Step 5: Commit**

```powershell
git add cityrt-audit/analysis/rendering
git commit -m "analysis: shader pipeline and rendering technique verdict"
```

### Task 15: Building language metrics

**Files:**
- Create: `cityrt-audit/analysis/geometry/building-language.md`, `cityrt-audit/analysis/geometry/metrics.json`, `cityrt-audit/tools/report/geometry.js`

**Interfaces:**
- Consumes: `parseGlb` (Task 4), `evidence/models/*.glb` (Task 12), or screenshots when no models exist.
- Produces: `metrics.json` with `{count, bbox: {length: {p50,p90}, width: {...}, height: {...}}, triangles: {p50,p90,max}, materialsPerBuilding: {p50,max}, roofHeightRatio: {p50}, moduleGrid: number|null}`

- [ ] **Step 1: Parse every extracted model**

Collect bounding boxes, triangle counts, material counts and node-name patterns; normalise units by the modal footprint size and record the raw distribution too.

- [ ] **Step 2: Infer the module grid**

Find the greatest common divisor-like clustering of footprint dimensions (histogram peaks within 5 % tolerance) and record the candidate cell size in metres assuming a street module of 1 cell. Mark `inferred` unless a constant in Task 10 confirms it.

- [ ] **Step 3: Describe the vocabulary**

Document massing types (slab, tower, courtyard, park, road), roof treatments, façade rhythm, and where variation comes from (scale, palette, prop swaps).

- [ ] **Step 4: Handle the no-model case**

If Task 12 found zero models, compute apparent cell size from screenshots by detecting the isometric grid and report every geometry number as `inferred from imagery`, with the method stated.

- [ ] **Step 5: Verify and commit**

Run: `node -e "const m=require('./cityrt-audit/analysis/geometry/metrics.json'); if(!(m.count>0)) process.exit(1); console.log('models', m.count, 'p50 tris', m.triangles.p50)"`
Expected: exit 0 with plausible numbers.

```powershell
git add cityrt-audit/analysis/geometry cityrt-audit/tools/report/geometry.js
git commit -m "analysis: measured building language and module grid"
```

### Task 16: Simulation and feel

**Files:**
- Create: `cityrt-audit/analysis/simulation/simulation.md`, `cityrt-audit/analysis/simulation/timeseries.json`, `cityrt-audit/tools/browser/timeseries.js`

**Interfaces:**
- Consumes: `constants.json` (Task 10), a capture session (Task 11).
- Produces: `timeseries.json` = `{styleId, samples: {t: number, drawCalls: number, frames: number, screenshotSample: {meanLuma: number, hueHistogram: number[]}}[]}` over ≥60 s at 2 s intervals. Sky colour is sampled from a screenshot each tick, not from canvas readback, because a WebGL canvas without `preserveDrawingBuffer` reads back empty.

- [ ] **Step 1: Sample frame rate, draw calls and sky colour over time**

Run one style for 60 s, sampling every 2 s; record `frames` deltas (effective FPS) and a coarse screenshot sample per tick.

- [ ] **Step 2: Measure the day/night cycle**

Detect periodic luma/hue drift in the sky sample; report the period in seconds if at least two cycles are observed, otherwise mark `not established`.

- [ ] **Step 3: Correlate with source constants**

Match measured effective FPS and cycle length against `constants.json`; every mismatch above 20 % is recorded as a contradiction rather than smoothed over.

- [ ] **Step 4: Document the feel layer**

Write `simulation.md`: tick model, movement/pacing observations, construction cadence if observable, camera zoom/easing limits, and how each maps to a Blender-time recreation (for example "construction animates over N seconds; camera uses N-second ease").

- [ ] **Step 5: Commit**

```powershell
git add cityrt-audit/analysis/simulation cityrt-audit/tools/browser/timeseries.js
git commit -m "analysis: measured simulation timing and camera feel"
```

---

## Phase 4 — Synthesis

### Task 17: Nine-style matrix

**Files:**
- Create: `cityrt-audit/docs/STYLE-MATRIX.md`, `cityrt-audit/tools/report/matrix.js`, `cityrt-audit/tests/matrix.test.js`

**Interfaces:**
- Consumes: `analysis/styles/styles.json`, `analysis/palette/*.json`, `analysis/rendering/pipeline.md`, `analysis/geometry/metrics.json`, `analysis/simulation/simulation.md`.
- Produces: `renderMatrix(input) -> string` with one row per style and columns: palette, lighting, shader/NPR, geometry, simulation; each cell ends with an evidence reference.

- [ ] **Step 1: Write the failing test for empty-cell policy**

```javascript
// cityrt-audit/tests/matrix.test.js
const test = require('node:test');
const assert = require('node:assert');
const { renderMatrix } = require('../tools/report/matrix.js');

test('an unobserved cell is labelled, never blank', () => {
  const markdown = renderMatrix([{ id: 'x', name: 'X', cells: { palette: null, lighting: 'soft', shader: 'toon', geometry: null, simulation: 'calm' } }]);
  assert.match(markdown, /not observed/i);
  assert.doesNotMatch(markdown, /\|\s*\|/);
});
```

- [ ] **Step 2: Run to confirm failure**

Run: `node --test cityrt-audit/tests/matrix.test.js`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `renderMatrix` and generate the document**

Render the table; for every null cell write `not observed — <reason>`.

- [ ] **Step 4: Verify**

Run: `node --test cityrt-audit/tests/matrix.test.js`
Expected: PASS, 1 test.

- [ ] **Step 5: Commit**

```powershell
git add cityrt-audit/docs/STYLE-MATRIX.md cityrt-audit/tools/report/matrix.js cityrt-audit/tests/matrix.test.js
git commit -m "docs: nine-style matrix with explicit unobserved cells"
```

### Task 18: Art bible

**Files:**
- Create: `cityrt-audit/docs/ART-BIBLE.md`

**Interfaces:**
- Consumes: every analysis artefact.
- Produces: ten sections — design pillars; global rendering recipe; palette system; material rules; silhouette and detail budget; lighting and time of day; camera; motion and feel; do/don't checklist; verification procedure.

- [ ] **Step 1: Write pillars and the global recipe from measured values**

State tone mapping, exposure, fog model, shadow technique and anti-aliasing with the numbers from `constants.json` and `pipeline.md`.

- [ ] **Step 2: Write per-style palette and material rules**

For each style, give hex ramps (sky, ground, building base, accent, emissive) and material parameter guidance (roughness/metalness ranges, emissive window behaviour), each with an evidence reference.

- [ ] **Step 3: Write the silhouette and detail budget**

Convert measured triangle percentiles into authoring targets: hero building, standard building, prop; state where silhouette must read at the default camera distance.

- [ ] **Step 4: Write the do/don't checklist and verification procedure**

The checklist must be falsifiable ("no more than two base colours per façade", "shadow contact must be visible at 50 % zoom"), and the verification procedure must reference the same measurements used here so a later run can compare a Blender render against them.

- [ ] **Step 5: Self-check every claim for an evidence reference and commit**

Run: `Select-String -Path cityrt-audit/docs/ART-BIBLE.md -Pattern 'evidence:' | Measure-Object | Select-Object -ExpandProperty Count`
Expected: at least one `evidence:` marker per numbered section.

```powershell
git add cityrt-audit/docs/ART-BIBLE.md
git commit -m "docs: normative art bible derived from measured evidence"
```

### Task 19: Blender 5.2 kit specification

**Files:**
- Create: `cityrt-audit/docs/KIT-SPEC.md`

**Interfaces:**
- Consumes: `metrics.json`, `ART-BIBLE.md`, `constants.json`.
- Produces: a specification a later run can implement without re-reading this audit.

- [ ] **Step 1: Fix units, grid and module set**

State `1 Blender unit = 1 m`, the measured cell size, and the module list (road, lot, building, park, prop) with target dimensions from `metrics.json`.

- [ ] **Step 2: Fix the material recipes**

Give Principled BSDF values per style (base colour hex, roughness, metallic, emission colour/strength), the shading model choice (NPR vs PBR) justified by Task 14, and the outline or edge treatment if the audit found one.

- [ ] **Step 3: Fix budgets, LOD and naming**

Triangle budgets from measured percentiles, three LOD tiers with ratios, naming convention (`cityrt_<style>_<type>_<variant>`), and origin conventions (base-centre pivot, +Z up in Blender, +Y up on glTF export).

- [ ] **Step 4: Fix export and acceptance tests**

glTF export settings (metres, +Y up, no camera/lights, texture compression policy), plus acceptance tests: palette ΔE ≤ 6 against the style's measured palette, triangle budget within +10 %, silhouette ratio within 10 %, and a side-by-side render procedure against the captured reference frame.

- [ ] **Step 5: Mark every assumption and commit**

Any number not derived from analysis is labelled `assumption` with its rationale.

```powershell
git add cityrt-audit/docs/KIT-SPEC.md
git commit -m "docs: Blender 5.2 kit specification with acceptance tests"
```

### Task 20: Coverage and unknowns review

**Files:**
- Create: `cityrt-audit/docs/COVERAGE.md`, `cityrt-audit/docs/UNKNOWNS.md`, `cityrt-audit/tools/coverage.js`, `cityrt-audit/tests/coverage.test.js`, `cityrt-audit/tests/fixtures/coverage-bad/ART-BIBLE.md`

**Interfaces:**
- Produces: `checkCoverage(repoRoot: string) -> {claims: number, missingEvidence: {file: string, line: number}[], unknowns: number}`

- [ ] **Step 1: Write the failing test**

```javascript
// cityrt-audit/tests/coverage.test.js
const test = require('node:test');
const assert = require('node:assert');
const { checkCoverage } = require('../tools/coverage.js');

test('reports a claim whose evidence reference is missing', () => {
  const result = checkCoverage('cityrt-audit/tests/fixtures/coverage-bad');
  assert.ok(result.missingEvidence.length >= 1);
  assert.strictEqual(result.missingEvidence[0].file.includes('ART-BIBLE'), true);
});
```

The fixture directory contains one Markdown file with `evidence: missing/file.json`.

- [ ] **Step 2: Run to confirm failure**

Run: `node --test cityrt-audit/tests/coverage.test.js`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `checkCoverage`**

Scan deliverable Markdown for `evidence: <path>` markers, verify each path exists and its SHA-256 matches the manifest, and collect mismatches. Empty-`evidence` sections are reported too.

- [ ] **Step 4: Run it over the real deliverables and fix gaps**

Run: `node -e "const r=require('./cityrt-audit/tools/coverage.js').checkCoverage('cityrt-audit'); console.log(JSON.stringify(r,null,2))"`
Expected: `missingEvidence: []`. Fix any gap by adding the missing evidence file or removing the unsupported claim.

- [ ] **Step 5: Write `UNKNOWNS.md` and `COVERAGE.md`**

`UNKNOWNS.md` lists, per question from the brief: what was determined, what remains unknown, why (access, minification, absence), and the cheapest future probe. `COVERAGE.md` maps each brief success criterion to the section that satisfies it.

- [ ] **Step 6: Final verification and commit**

```powershell
node --test cityrt-audit/tests
```

Expected: all suites PASS.

```powershell
git add cityrt-audit
git commit -m "docs: coverage and unknowns review closing the audit"
```

---

## Definition of done

1. `node --test cityrt-audit/tests` passes with zero failures.
2. `analysis/styles/styles.json` validates with nine entries, each with an executable selection recipe.
3. Nine style directories exist with non-blank screenshots, or the shortfall is justified in `UNKNOWNS.md` with the exact gate that stopped it.
4. `STYLE-MATRIX.md` has no blank cells: every cell is measured or explicitly unobserved.
5. `checkCoverage` reports zero missing evidence references.
6. `KIT-SPEC.md` contains at least one acceptance test per dimension named in the brief, each numerically anchored to a measured value or labelled `assumption`.
7. No Blender execution occurred, and no extracted asset left `cityrt-audit/evidence/`.
