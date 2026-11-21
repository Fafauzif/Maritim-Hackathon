const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_CORE);
const { classifyPage } = require('../tools/browser/session.js');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

test('classifies anti-bot text without a canvas as challenge', async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  try {
    const page = await browser.newPage();
    await page.goto('file://' + path.join(__dirname, 'fixtures', 'challenge.html').replace(/\\/g, '/'));
    assert.strictEqual(await classifyPage(page), 'challenge');
  } finally {
    await browser.close();
  }
});

test('classifies a page with no canvas and no challenge text as landing', async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  try {
    const page = await browser.newPage();
    await page.goto('file://' + path.join(__dirname, 'fixtures', 'landing.html').replace(/\\/g, '/'));
    assert.strictEqual(await classifyPage(page), 'landing');
  } finally {
    await browser.close();
  }
});

test('classifies a pass URL as challenge even without challenge text', async () => {
  // A file:// document cannot rewrite its own path, so the URL rule is exercised
  // with the minimal page surface classifyPage reads.
  const stub = {
    url: () => 'https://cityrt.com/en/pass',
    evaluate: async () => ({ bodyText: 'Loading...', canvas: null, drawCalls: 0 }),
  };
  assert.strictEqual(await classifyPage(stub), 'challenge');
});

test('a live 3D canvas outranks challenge text', async () => {
  const stub = {
    url: () => 'https://cityrt.com/en/play',
    evaluate: async () => ({ bodyText: 'verify you are human', canvas: { width: 1440, height: 900 }, drawCalls: 1200 }),
  };
  assert.strictEqual(await classifyPage(stub), 'game');
});
