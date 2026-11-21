const endpoint = 'http://127.0.0.1:9222/json';
const deadline = Date.now() + 900000;
let last = '';
(async () => {
  while (Date.now() < deadline) {
    try {
      const res = await fetch(endpoint);
      const targets = await res.json();
      const pages = targets.filter((t) => t.type === 'page');
      const cityrt = /^https?:\/\/cityrt\.com\//i;
      const summary = pages.map((p) => `${p.title} :: ${p.url.split('?')[0]}`).join(' | ');
      if (summary !== last) {
        console.log(new Date().toISOString(), summary);
        last = summary;
      }
      const playing = pages.find((p) => cityrt.test(p.url) && !/\/login(\/|$|\?)/i.test(p.url));
      if (playing) {
        console.log('LOGIN_COMPLETE', playing.title, playing.url);
        process.exit(0);
      }
    } catch (e) {
      console.log('poll error', e.message);
    }
    await new Promise((r) => setTimeout(r, 3000));
  }
  console.log('TIMEOUT waiting for login');
  process.exit(1);
})();
