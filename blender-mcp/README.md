# blender-mcp

DeepSeek Harness bundle that connects an already-running Blender to the agent.

Blender 5.1+ ships an official `MCP` add-on that listens on `127.0.0.1:9876` and speaks NUL-framed JSON (`{"type":"execute","code":...,"strict_json":...}`), not MCP. `server.js` is a dependency-free stdio MCP server that bridges the two, so the harness can drive the open session.

Tools (as `mcp__blender__*`):

- `execute_blender_code` — run Python inside Blender
- `get_scene_info` — objects, transforms, collections, engine, frame
- `get_object_info` — one object's geometry, modifiers and materials
- `get_viewport_screenshot` — PNG preview render from the active camera

Requirements: Blender running, the MCP add-on enabled, online access enabled in Blender's system preferences, and port 9876 free. This is the same machine-local integration Blender's add-on is designed for — it is not a remote service.

See `docs/DETAIL.md` for configuration, usage and limitations.
