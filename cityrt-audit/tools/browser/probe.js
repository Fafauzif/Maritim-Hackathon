// Pre-navigation WebGL probe: records renderer identity, every compiled shader
// pair, draw-call volume and frame cadence without altering page behaviour.
const crypto = require('node:crypto');

function installInPage() {
  const state = {
    shaders: [],
    drawCalls: 0,
    frames: 0,
    renderer: null,
    vendor: null,
    unmaskedRenderer: null,
    unmaskedVendor: null,
    contextAttributes: null,
    canvas: null,
  };
  window.__cityrtProbe = state;
  const shaderSources = new WeakMap();
  const programs = new WeakMap();

  function wrapContext(Ctor) {
    if (!Ctor || !Ctor.prototype) return;
    const proto = Ctor.prototype;
    const origShaderSource = proto.shaderSource;
    if (origShaderSource) {
      proto.shaderSource = function (shader, source) {
        try { shaderSources.set(shader, String(source)); } catch (e) { /* ignore */ }
        return origShaderSource.call(this, shader, source);
      };
    }
    const origAttach = proto.attachShader;
    if (origAttach) {
      proto.attachShader = function (program, shader) {
        try {
          const rec = programs.get(program) || { shaders: [] };
          rec.shaders.push(shader);
          programs.set(program, rec);
        } catch (e) { /* ignore */ }
        return origAttach.call(this, program, shader);
      };
    }
    const origLink = proto.linkProgram;
    if (origLink) {
      proto.linkProgram = function (program) {
        const result = origLink.call(this, program);
        try {
          const rec = programs.get(program);
          if (rec && rec.shaders.length) {
            let vertex = '';
            let fragment = '';
            for (const sh of rec.shaders) {
              const src = shaderSources.get(sh) || '';
              if (!vertex && /gl_Position/.test(src)) vertex = src;
              else if (!fragment && /gl_FragColor|gl_FragData|fragColor|out vec4/i.test(src)) fragment = src;
            }
            state.shaders.push({ vertex, fragment });
          }
        } catch (e) { /* ignore */ }
        return result;
      };
    }
    for (const name of ['drawElements', 'drawArrays', 'drawElementsInstanced', 'drawArraysInstanced']) {
      const orig = proto[name];
      if (!orig) continue;
      proto[name] = function () {
        state.drawCalls += 1;
        return orig.apply(this, arguments);
      };
    }
    const origGetParameter = proto.getParameter;
    if (origGetParameter) {
      proto.getParameter = function (pname) {
        const value = origGetParameter.call(this, pname);
        if (pname === 0x1f00) state.vendor = value;
        if (pname === 0x1f01) state.renderer = value;
        return value;
      };
    }
  }

  wrapContext(window.WebGLRenderingContext);
  wrapContext(window.WebGL2RenderingContext);

  const origGetContext = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (type) {
    const ctx = origGetContext.apply(this, arguments);
    if (ctx && /webgl/i.test(String(type)) && !state.contextAttributes) {
      try {
        state.contextAttributes = arguments[1] ? JSON.parse(JSON.stringify(arguments[1])) : {};
      } catch (e) { state.contextAttributes = {}; }
      state.canvas = { width: this.width, height: this.height };
      try {
        state.vendor = ctx.getParameter(0x1f00);
        state.renderer = ctx.getParameter(0x1f01);
      } catch (e) { /* ignore */ }
      try {
        const debugInfo = ctx.getExtension('WEBGL_debug_renderer_info');
        if (debugInfo) {
          state.unmaskedRenderer = ctx.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
          state.unmaskedVendor = ctx.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
        }
      } catch (e) { /* ignore */ }
    }
    return ctx;
  };

  const origRaf = window.requestAnimationFrame;
  window.requestAnimationFrame = function (cb) {
    state.frames += 1;
    return origRaf.call(window, cb);
  };
}

async function installProbe(page) {
  await page.addInitScript(installInPage);
}

async function dumpProbe(page) {
  const raw = await page.evaluate(() => {
    const probe = window.__cityrtProbe || {};
    return {
      renderer: probe.renderer === undefined ? null : probe.renderer,
      vendor: probe.vendor === undefined ? null : probe.vendor,
      unmaskedRenderer: probe.unmaskedRenderer === undefined ? null : probe.unmaskedRenderer,
      unmaskedVendor: probe.unmaskedVendor === undefined ? null : probe.unmaskedVendor,
      contextAttributes: probe.contextAttributes === undefined ? null : probe.contextAttributes,
      canvas: probe.canvas === undefined ? null : probe.canvas,
      drawCalls: probe.drawCalls || 0,
      frames: probe.frames || 0,
      shaders: (probe.shaders || []).map((s) => ({ vertex: s.vertex, fragment: s.fragment })),
    };
  });
  return {
    renderer: raw.renderer,
    vendor: raw.vendor,
    unmaskedRenderer: raw.unmaskedRenderer,
    unmaskedVendor: raw.unmaskedVendor,
    contextAttributes: raw.contextAttributes,
    canvas: raw.canvas,
    drawCalls: raw.drawCalls,
    frames: raw.frames,
    shaders: raw.shaders.map((s) => ({
      hash: crypto.createHash('sha256').update(s.vertex + '\u0000' + s.fragment).digest('hex').slice(0, 16),
      vertex: s.vertex,
      fragment: s.fragment,
    })),
  };
}

module.exports = { installProbe, dumpProbe };
