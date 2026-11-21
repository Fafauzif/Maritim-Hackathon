const fs = require('node:fs');
const { chromium } = require(process.env.PLAYWRIGHT_CORE);
(async () => {
  const browser = await chromium.launch({ executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' });
  const page = await browser.newPage();
  await page.goto('about:blank');
  const files = ['res_cottage', 'cyberpunk_house', 'medieval_house', 'fantasy_house'];
  for (const name of files) {
    const file = 'cityrt-audit/evidence/catalog/img/' + name + '.webp';
    if (!fs.existsSync(file)) { console.log(name, 'missing'); continue; }
    const b64 = fs.readFileSync(file).toString('base64');
    const info = await page.evaluate(async (dataUrl) => {
      const img = new Image();
      await new Promise((r, j) => { img.onload = r; img.onerror = () => j(new Error('decode')); img.src = dataUrl; });
      const c = document.createElement('canvas');
      c.width = img.naturalWidth; c.height = img.naturalHeight;
      const ctx = c.getContext('2d');
      ctx.drawImage(img, 0, 0);
      const d = ctx.getImageData(0, 0, c.width, c.height).data;
      let opaque = 0, transparent = 0;
      const border = [];
      for (let i = 0; i < d.length; i += 4) {
        if (d[i + 3] < 250) transparent++; else opaque++;
      }
      const px = (x, y) => { const i = (y * c.width + x) * 4; return [d[i], d[i+1], d[i+2], d[i+3]]; };
      border.push(px(0,0), px(c.width-1,0), px(0,c.height-1), px(c.width-1,c.height-1));
      return { w: c.width, h: c.height, opaque, transparent, border };
    }, 'data:image/webp;base64,' + b64);
    console.log(name, JSON.stringify(info));
  }
  await browser.close();
})();
