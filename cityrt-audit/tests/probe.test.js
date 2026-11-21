const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_CORE);
const { installProbe, dumpProbe } = require('../tools/browser/probe.js');

test('captures renderer identity, one shader pair and draw calls', async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    args: ['--use-gl=angle', '--use-angle=swiftshader'],
  });
  try {
    const page = await browser.newPage();
    await installProbe(page);
    await page.goto('file://' + path.join(__dirname, 'fixtures', 'probe.html').replace(/\\/g, '/'));
    await page.waitForFunction(() => window.__probeReady === true, null, { timeout: 15000 });
    const dump = await dumpProbe(page);
    // RENDERER alone returns "WebKit WebGL" in Chrome; the driver string is the
    // unmasked value from WEBGL_debug_renderer_info.
    assert.ok(dump.renderer, 'renderer string is present');
    assert.match(
      String(dump.unmaskedRenderer),
      /angle|swiftshader|direct3d|opengl|vulkan|mali|adreno|nvidia|amd|intel|apple/i,
    );
    assert.strictEqual(dump.shaders.length, 1);
    assert.match(dump.shaders[0].fragment, /gl_FragColor|fragColor/);
    assert.match(dump.shaders[0].hash, /^[0-9a-f]{16}$/);
    assert.ok(dump.drawCalls >= 1, 'draw calls are counted');
    assert.ok(dump.frames >= 1, 'frames are counted');
    assert.deepStrictEqual([dump.canvas.width, dump.canvas.height], [320, 240]);
  } finally {
    await browser.close();
  }
});
