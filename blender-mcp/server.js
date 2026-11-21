#!/usr/bin/env node
/**
 * MCP stdio bridge for Blender's official "MCP" extension (Blender 5.1+).
 *
 * Blender's extension (extensions/user_default/mcp/mcp_to_blender_server.py)
 * exposes a TCP socket on 127.0.0.1:9876 that accepts ONE request per
 * connection: NUL-terminated JSON of the shape
 *   {"type": "execute", "code": "<python>", "strict_json": <bool>}
 * The executed Python must assign a dict to `result`; captured stdout is
 * returned as well. Response shape:
 *   {"status": "ok"|"error", "result": {...}, "stdout": "...", "stderr": "..."}
 *
 * This process translates MCP (JSON-RPC 2.0 over stdio) into that protocol.
 */

import net from 'node:net';

const HOST = process.env.BLENDER_HOST || '127.0.0.1';
const PORT = Number(process.env.BLENDER_PORT || 9876);
const CONNECT_TIMEOUT_MS = Number(process.env.BLENDER_CONNECT_TIMEOUT_MS || 5000);
const EXEC_TIMEOUT_MS = Number(process.env.BLENDER_EXEC_TIMEOUT_MS || 180000);
const MAX_RESPONSE_BYTES = 64 * 1024 * 1024;

const SERVER_INFO = { name: 'blender-mcp-bridge', version: '1.0.0' };
const SUPPORTED_PROTOCOLS = ['2025-06-18', '2025-03-26', '2024-11-05'];

/** Send one execute request to the Blender addon and resolve its JSON response. */
function blenderExecute(code, strictJson = false) {
  return new Promise((resolve, reject) => {
    const payload = Buffer.concat([
      Buffer.from(JSON.stringify({ type: 'execute', code, strict_json: strictJson }), 'utf8'),
      Buffer.from([0]),
    ]);

    const socket = new net.Socket();
    const chunks = [];
    let total = 0;
    let settled = false;

    const done = (fn, value) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      socket.destroy();
      fn(value);
    };

    const timer = setTimeout(() => {
      done(reject, new Error(`Blender did not answer within ${EXEC_TIMEOUT_MS} ms`));
    }, EXEC_TIMEOUT_MS);

    socket.setTimeout(CONNECT_TIMEOUT_MS, () => {
      done(reject, new Error(
        `Timed out connecting to Blender at ${HOST}:${PORT}. ` +
        'Is Blender running with the MCP extension enabled (Preferences > Add-ons > MCP)?',
      ));
    });

    socket.on('error', (err) => {
      done(reject, new Error(`Could not reach Blender at ${HOST}:${PORT}: ${err.message}`));
    });

    socket.on('data', (chunk) => {
      total += chunk.length;
      if (total > MAX_RESPONSE_BYTES) {
        done(reject, new Error('Blender response exceeded the 64 MiB bridge limit'));
        return;
      }
      chunks.push(chunk);
      const buf = Buffer.concat(chunks);
      const nul = buf.indexOf(0);
      if (nul !== -1) {
        finish(buf.subarray(0, nul).toString('utf8'));
      }
    });

    socket.on('end', () => {
      const buf = Buffer.concat(chunks);
      const nul = buf.indexOf(0);
      finish((nul !== -1 ? buf.subarray(0, nul) : buf).toString('utf8'));
    });

    function finish(text) {
      if (settled) return;
      if (!text.trim()) {
        done(reject, new Error('Blender closed the connection without sending a response'));
        return;
      }
      let parsed;
      try {
        parsed = JSON.parse(text);
      } catch (err) {
        done(reject, new Error(`Unreadable response from Blender: ${text.slice(0, 400)}`));
        return;
      }
      done(resolve, parsed);
    }

    socket.connect(PORT, HOST, () => {
      socket.setNoDelay(true);
      socket.setTimeout(0);
      socket.write(payload);
    });
  });
}

/** Normalise an addon response into { text, image }. */
function interpret(response) {
  const parts = [];
  let image = null;

  if (response.status !== 'ok') {
    parts.push(`Blender error:\n${response.message || '(no message)'}`);
  } else {
    const result = response.result ?? {};
    if (result && typeof result === 'object' && typeof result.image_base64 === 'string') {
      image = result.image_base64;
      const meta = { ...result };
      delete meta.image_base64;
      if (Object.keys(meta).length) parts.push(JSON.stringify(meta, null, 2));
    } else {
      parts.push(JSON.stringify(result, null, 2));
    }
  }

  if (response.stdout) parts.push(`stdout:\n${response.stdout}`);
  if (response.stderr) parts.push(`stderr:\n${response.stderr}`);

  return { text: parts.filter(Boolean).join('\n\n') || '(no output)', image };
}

const TOOLS = [
  {
    name: 'execute_blender_code',
    description:
      "Run Python inside the user's open Blender session (bpy, bmesh, mathutils are available). " +
      'Assign a JSON-serialisable dict to `result` to return data; printed output is captured ' +
      'as stdout. Blender blocks while the script runs, so keep it fast and avoid infinite loops.',
    inputSchema: {
      type: 'object',
      properties: {
        code: { type: 'string', description: 'Python source to execute in Blender.' },
        strict_json: {
          type: 'boolean',
          description:
            'When true, fail instead of repr()-ing non-serialisable values in `result`. Default false.',
        },
      },
      required: ['code'],
      additionalProperties: false,
    },
  },
  {
    name: 'get_scene_info',
    description:
      'Return the current .blend scene as structured JSON: Blender version, render engine, ' +
      'frame, objects with transforms/parents/collections, and the collections, materials, ' +
      'cameras and lights in the file. Use this before changing anything.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  },
  {
    name: 'get_object_info',
    description:
      'Return detailed JSON for one object: transform, dimensions, world-space bounding box, ' +
      'modifiers, vertex/edge/polygon counts, material slots and custom properties.',
    inputSchema: {
      type: 'object',
      properties: { name: { type: 'string', description: 'Exact object name.' } },
      required: ['name'],
      additionalProperties: false,
    },
  },
  {
    name: 'get_viewport_screenshot',
    description:
      'Render the current scene from its active camera and return the PNG as an image. ' +
      'Use it to check silhouette, framing, materials and lighting.',
    inputSchema: {
      type: 'object',
      properties: {
        max_size: {
          type: 'integer',
          minimum: 64,
          maximum: 4096,
          description: 'Longest edge of the returned image in pixels. Default 1024.',
        },
      },
      additionalProperties: false,
    },
  },
];

const SCENE_INFO_CODE = `
import bpy
scene = bpy.context.scene
objects = []
for obj in bpy.data.objects:
    objects.append({
        "name": obj.name,
        "type": obj.type,
        "location": [round(v, 4) for v in obj.location],
        "rotation_euler": [round(v, 4) for v in obj.rotation_euler],
        "scale": [round(v, 4) for v in obj.scale],
        "dimensions": [round(v, 4) for v in obj.dimensions],
        "parent": obj.parent.name if obj.parent else None,
        "collections": [c.name for c in obj.users_collection],
        "hidden": obj.hide_viewport,
    })
result = {
    "blender_version": bpy.app.version_string,
    "file": bpy.data.filepath,
    "engine": scene.render.engine,
    "frame": scene.frame_current,
    "camera": scene.camera.name if scene.camera else None,
    "object_count": len(objects),
    "objects": objects,
    "collections": [c.name for c in bpy.data.collections],
    "materials": [m.name for m in bpy.data.materials],
    "cameras": [o.name for o in bpy.data.objects if o.type == "CAMERA"],
    "lights": [o.name for o in bpy.data.objects if o.type == "LIGHT"],
}
`;

function objectInfoCode(name) {
  return `
import bpy
obj = bpy.data.objects.get(${JSON.stringify(name)})
if obj is None:
    result = {"error": "No object named ${name.replace(/["\\]/g, '')}"}
else:
    mesh = obj.data if obj.type == "MESH" else None
    corners = [obj.matrix_world @ v.co for v in mesh.vertices] if mesh else []
    bbox = {
        "min": [round(min(c[i] for c in corners), 4) for i in range(3)],
        "max": [round(max(c[i] for c in corners), 4) for i in range(3)],
    } if corners else None
    result = {
        "name": obj.name,
        "type": obj.type,
        "location": [round(v, 4) for v in obj.location],
        "rotation_euler": [round(v, 4) for v in obj.rotation_euler],
        "scale": [round(v, 4) for v in obj.scale],
        "dimensions": [round(v, 4) for v in obj.dimensions],
        "world_bounding_box": bbox,
        "parent": obj.parent.name if obj.parent else None,
        "collections": [c.name for c in obj.users_collection],
        "modifiers": [{"name": m.name, "type": m.type} for m in obj.modifiers],
        "vertex_count": len(mesh.vertices) if mesh else None,
        "edge_count": len(mesh.edges) if mesh else None,
        "polygon_count": len(mesh.polygons) if mesh else None,
        "materials": [s.material.name if s.material else None for s in obj.material_slots],
        "custom_properties": {k: repr(obj[k]) for k in obj.keys() if k != "_RNA_UI"},
    }
`;
}

function screenshotCode(maxSize) {
  return `
import bpy, base64, os, tempfile

scene = bpy.context.scene
if scene.camera is None:
    result = {"error": "Scene has no active camera; add one or run execute_blender_code to create it."}
else:
    max_size = int(${maxSize})
    res = scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage
    old_path = scene.render.filepath
    old_format = scene.render.image_settings.file_format
    tmpdir = tempfile.mkdtemp(prefix="blender_mcp_")
    try:
        scene.render.resolution_percentage = 100
        longest = max(scene.render.resolution_x, scene.render.resolution_y)
        if longest > max_size and longest > 0:
            pct = max(1, int(round(max_size * 100.0 / longest)))
            scene.render.resolution_percentage = pct
        scene.render.image_settings.file_format = "PNG"
        scene.render.filepath = os.path.join(tmpdir, "shot_")
        bpy.ops.render.opengl(write_still=True, view_context=False)
        source = scene.render.frame_path(frame=scene.frame_current)
        if not os.path.exists(source):
            candidates = [
                os.path.join(tmpdir, name)
                for name in sorted(os.listdir(tmpdir))
                if name.lower().endswith(".png")
            ]
            source = candidates[0] if candidates else ""
        if not source:
            result = {
                "error": "Blender did not write an OpenGL preview file.",
                "written_to": scene.render.filepath,
            }
        else:
            with open(source, "rb") as handle:
                encoded = base64.b64encode(handle.read()).decode("ascii")
            result = {
                "image_base64": encoded,
                "width": int(scene.render.resolution_x * scene.render.resolution_percentage / 100),
                "height": int(scene.render.resolution_y * scene.render.resolution_percentage / 100),
                "camera": scene.camera.name,
                "frame": scene.frame_current,
                "engine": scene.render.engine,
            }
    finally:
        scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = res
        scene.render.filepath = old_path
        scene.render.image_settings.file_format = old_format
`;
}

async function callTool(name, args) {
  switch (name) {
    case 'execute_blender_code': {
      if (typeof args.code !== 'string' || !args.code.trim()) {
        return { content: [{ type: 'text', text: 'The `code` argument is required.' }], isError: true };
      }
      const response = await blenderExecute(args.code, args.strict_json === true);
      const { text, image } = interpret(response);
      const content = [];
      if (image) content.push({ type: 'image', data: image, mimeType: 'image/png' });
      content.push({ type: 'text', text });
      return { content, isError: response.status !== 'ok' };
    }
    case 'get_scene_info': {
      const response = await blenderExecute(SCENE_INFO_CODE);
      const { text } = interpret(response);
      return { content: [{ type: 'text', text }], isError: response.status !== 'ok' };
    }
    case 'get_object_info': {
      if (typeof args.name !== 'string' || !args.name) {
        return { content: [{ type: 'text', text: 'The `name` argument is required.' }], isError: true };
      }
      const response = await blenderExecute(objectInfoCode(args.name));
      const { text } = interpret(response);
      return { content: [{ type: 'text', text }], isError: response.status !== 'ok' };
    }
    case 'get_viewport_screenshot': {
      const maxSize = Number.isFinite(args.max_size) ? args.max_size : 1024;
      const response = await blenderExecute(screenshotCode(maxSize));
      const { text, image } = interpret(response);
      const content = [];
      if (image) content.push({ type: 'image', data: image, mimeType: 'image/png' });
      content.push({ type: 'text', text });
      return { content, isError: response.status !== 'ok' };
    }
    default:
      return { content: [{ type: 'text', text: `Unknown tool: ${name}` }], isError: true };
  }
}

function send(message) {
  process.stdout.write(`${JSON.stringify(message)}\n`);
}

function reply(id, result) {
  send({ jsonrpc: '2.0', id, result });
}

function fail(id, code, message) {
  send({ jsonrpc: '2.0', id, error: { code, message } });
}

async function handle(message) {
  const { id, method, params } = message;
  const isNotification = id === undefined || id === null;

  switch (method) {
    case 'initialize': {
      const requested = params?.protocolVersion;
      const protocolVersion = SUPPORTED_PROTOCOLS.includes(requested)
        ? requested
        : SUPPORTED_PROTOCOLS[0];
      reply(id, {
        protocolVersion,
        capabilities: { tools: { listChanged: false } },
        serverInfo: SERVER_INFO,
        instructions:
          'Drives the Blender session that is already open. Prefer get_scene_info first, ' +
          'execute_blender_code to build and edit, and get_viewport_screenshot to verify visually.',
      });
      return;
    }
    case 'notifications/initialized':
    case 'initialized':
      return;
    case 'ping':
      if (!isNotification) reply(id, {});
      return;
    case 'tools/list':
      reply(id, { tools: TOOLS });
      return;
    case 'tools/call': {
      const name = params?.name;
      const args = params?.arguments ?? {};
      try {
        const result = await callTool(name, args);
        reply(id, result);
      } catch (err) {
        reply(id, {
          content: [{ type: 'text', text: `Blender bridge error: ${err.message}` }],
          isError: true,
        });
      }
      return;
    }
    case 'resources/list':
      if (!isNotification) reply(id, { resources: [] });
      return;
    case 'prompts/list':
      if (!isNotification) reply(id, { prompts: [] });
      return;
    default:
      if (!isNotification) fail(id, -32601, `Method not found: ${method}`);
  }
}

let buffer = '';
let pending = 0;
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => {
  buffer += chunk;
  let newline;
  while ((newline = buffer.indexOf('\n')) !== -1) {
    const line = buffer.slice(0, newline).trim();
    buffer = buffer.slice(newline + 1);
    if (!line) continue;
    let message;
    try {
      message = JSON.parse(line);
    } catch {
      continue;
    }
    pending += 1;
    handle(message)
      .catch((err) => {
        if (message?.id !== undefined && message?.id !== null) {
          fail(message.id, -32603, `Internal error: ${err.message}`);
        }
      })
      .finally(() => {
        pending -= 1;
      });
  }
});

// Let in-flight tool calls (which may be a long render) finish before leaving.
process.stdin.on('end', () => {
  const waitForIdle = () => {
    if (pending === 0) {
      process.exit(0);
      return;
    }
    setTimeout(waitForIdle, 50);
  };
  waitForIdle();
});
process.on('unhandledRejection', (err) => {
  process.stderr.write(`blender-mcp-bridge unhandled rejection: ${err}\n`);
});
