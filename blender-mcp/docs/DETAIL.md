# Blender

This bundle connects the Blender session that is already open to DeepSeek Harness. It adds one `@deepseek-ai/dsh-mcp-client` row, `id: blender-mcp`, with `serverName: blender`, plus a small local stdio server that translates MCP into the socket protocol Blender's own extension speaks.

## What it connects to

Blender 5.1+ ships an official MCP add-on, `MCP` (`extensions/user_default/mcp/`, maintained by Blender Lab, version 1.0.3 on this machine). It is not the third-party `blender-mcp` add-on, and it does not accept MCP itself. When enabled it opens a TCP listener on `127.0.0.1:9876` and accepts **one request per connection**: NUL-terminated JSON of the form `{"type": "execute", "code": "<python>", "strict_json": <bool>}`. The Python runs on Blender's main thread, and must assign a dict to `result`; captured `stdout` comes back alongside it.

DeepSeek Harness speaks MCP over stdio, so `server.js` in this folder sits in between: it accepts MCP JSON-RPC on stdin and turns each tool call into that socket request. This is why the bundle contains code rather than being configuration only.

## Tools

Available as `mcp__blender__<tool>` once the server connects.

| Tool | Purpose |
| --- | --- |
| `execute_blender_code` | Run Python in the open session (`bpy`, `bmesh`, `mathutils`). Assign a dict to `result` to return data; prints become `stdout`. |
| `get_scene_info` | Blender version, file, engine, frame, active camera, objects with transforms and collections, plus collections/materials/cameras/lights. |
| `get_object_info` | One object: transform, dimensions, world bounding box, modifiers, vertex/edge/polygon counts, material slots, custom properties. |
| `get_viewport_screenshot` | OpenGL preview render from the active camera, returned as a PNG image. |

## How it is configured

- `command` is the same portable Node.js 24.22.3 runtime the REA bundle uses, so no system Node dependency and no package install.
- `args` run `blender-mcp/server.js`; `cwd` is the bundle folder.
- `BLENDER_HOST` / `BLENDER_PORT` (defaults `127.0.0.1` / `9876`) select the add-on's listener. Change them if you moved the port in Blender's MCP preferences.
- `toolCallTimeoutMs` is 600000 because a Cycles render or a heavy mesh operation easily outlives the 60-second default.
- `startupTimeoutMs` is on the generous side; it only bounds starting the local bridge, not Blender.

## Prerequisites

1. Blender is running with **Preferences > Add-ons > MCP** enabled.
2. Online access is enabled in Blender's system preferences, which the add-on requires even for localhost.
3. Nothing else holds port 9876. The add-on allows one listener, so a second MCP-capable Blender instance cannot share it.

The bridge reports a plain-language error when the port refuses or times out, rather than failing silently.

## Usage

Ask in plain language: "what's in my Blender scene", "add a bevel and check it", "render the camera so I can see the silhouette". The agent calls `get_scene_info` first, edits with `execute_blender_code`, then verifies with `get_viewport_screenshot`.

Good practice when generating code for it: keep scripts short and deterministic, assign `result` with plain data types, avoid modal operators and infinite loops. Blender's UI is blocked for the duration of each script, and Deferred responses (`check_is_finished`) are not supported by this bridge, so long jobs should be chunked or driven by a Blender timer.

## Limitations

- `get_viewport_screenshot` uses `bpy.ops.render.opengl`, so it shows the active camera's view with material colours, not the exact interactive viewport shading or overlays. It needs an active camera; without one it returns an error instead of an image.
- The screenshot's longest edge is scaled down in whole percentage steps, so the returned width can overshoot the requested `max_size` by a few pixels.
- Scripts run with Blender's own privileges and full `bpy` access. There is no sandbox beyond the add-on's own weak sandbox; treat `execute_blender_code` as write access to the open file.
- The bundle links this directory; moving or deleting it breaks the registration.
