#!/usr/bin/env python3
"""Check a Blender art run's deliverable files without importing bpy."""

import argparse
import json
import struct
import sys
import zlib
from pathlib import Path

COASTS = ("kodingareng", "tunda", "amur")
COAST_FILES = (
    "scene.blend", "coast.glb", "godview.png", "mapview.png", "section.png",
    "travel.mp4", "review.md",
)
UHD = (3840, 2160)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
GLB_JSON = 0x4E4F534A
GLB_BIN = 0x004E4942
IO_BLOCK_SIZE = 1024 * 1024


def expected_artifacts():
    """Return relative paths and any exact pixel-size requirement."""
    rules = {
        "globe/globe.blend": None,
        "globe/globe-overview.png": UHD,
        "globe/globe.glb": None,
        "coast-reel.mp4": None,
        "kit/common-kit.blend": None,
        "kit/common-kit.glb": None,
        "kit/asset-sheet.png": None,
        "review/parity-sheet.png": None,
        "review/audit-intake.md": None,
        "review/handoff.md": None,
        "review/export-check.md": None,
        "review/deviations.md": None,
    }
    for coast in COASTS:
        for filename in COAST_FILES:
            path = f"coasts/{coast}/{filename}"
            rules[path] = UHD if filename.endswith(".png") else None
    return rules


def read_exact(handle, size):
    value = handle.read(size)
    if len(value) != size:
        raise ValueError("truncated file")
    return value


def png_details(path, expected):
    """Check PNG block structure and CRCs without decoding pixel data."""
    width = height = None
    image_data_seen = False
    with path.open("rb") as handle:
        if read_exact(handle, len(PNG_SIGNATURE)) != PNG_SIGNATURE:
            raise ValueError("invalid PNG signature")
        while True:
            length, kind = struct.unpack(">I4s", read_exact(handle, 8))
            if width is None and kind != b"IHDR":
                raise ValueError("IHDR is not the first PNG chunk")
            if kind == b"IHDR" and (width is not None or length != 13):
                raise ValueError("invalid PNG IHDR")
            crc = zlib.crc32(kind)
            remaining = length
            while remaining:
                block = read_exact(handle, min(IO_BLOCK_SIZE, remaining))
                crc = zlib.crc32(block, crc)
                if kind == b"IHDR":
                    width, height = struct.unpack_from(">II", block)
                remaining -= len(block)
            if crc != struct.unpack(">I", read_exact(handle, 4))[0]:
                raise ValueError(f"PNG chunk CRC mismatch ({kind!r})")
            if kind == b"IDAT" and length:
                image_data_seen = True
            if kind == b"IEND":
                if length or handle.read(1):
                    raise ValueError("invalid PNG ending")
                break
    if not width or not height or not image_data_seen:
        raise ValueError("missing PNG dimensions or image data")
    if expected and (width, height) != expected:
        raise ValueError(f"PNG is {width}×{height}; expected {expected[0]}×{expected[1]}")
    return {"width": width, "height": height}


def glb_payload(path):
    """Read JSON and verify the binary container boundaries."""
    size = path.stat().st_size
    with path.open("rb") as handle:
        magic, version, declared_size = struct.unpack("<4sII", read_exact(handle, 12))
        if magic != b"glTF" or version != 2:
            raise ValueError("expected binary glTF 2.0")
        if declared_size != size:
            raise ValueError("GLB header length differs from the file size")
        json_size, chunk_type = struct.unpack("<II", read_exact(handle, 8))
        if chunk_type != GLB_JSON or json_size < 4 or json_size % 4:
            raise ValueError("first GLB chunk must be aligned JSON")
        if json_size > size - handle.tell():
            raise ValueError("GLB JSON extends beyond the file")
        document = json.loads(read_exact(handle, json_size).decode("utf-8"))
        binary_size = None
        first_remaining_chunk = True
        while handle.tell() < size:
            chunk_size, chunk_type = struct.unpack("<II", read_exact(handle, 8))
            if chunk_size % 4 or chunk_size > size - handle.tell():
                raise ValueError("GLB chunk is misaligned or extends beyond the file")
            if chunk_type == GLB_BIN:
                if not first_remaining_chunk:
                    raise ValueError("GLB BIN must follow JSON immediately and occur once")
                binary_size = chunk_size
            elif chunk_type == GLB_JSON:
                raise ValueError("duplicate GLB JSON chunk")
            first_remaining_chunk = False
            handle.seek(chunk_size, 1)
    return document, binary_size


def json_array(document, key):
    value = document.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ValueError(f"{key} must be an array of JSON objects")
    return value


def natural_number(value, field):
    if type(value) is not int or value < 0:
        raise ValueError(f"{field} must be a non-negative integer")
    return value


def require_embedded_uris(value, location="GLB"):
    """Reject external URIs in asset entries and extensions, ignoring custom extras."""
    if isinstance(value, dict):
        for key, entry in value.items():
            pointer = f"{location}.{key}"
            if key == "uri" and (not isinstance(entry, str) or not entry.startswith("data:")):
                raise ValueError(f"external or invalid URI at {pointer}")
            if key != "extras":
                require_embedded_uris(entry, pointer)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            require_embedded_uris(item, f"{location}[{index}]")


def glb_details(path):
    document, binary_size = glb_payload(path)
    if not isinstance(document, dict) or not isinstance(document.get("asset"), dict):
        raise ValueError("GLB JSON lacks a glTF asset object")
    if document["asset"].get("version") != "2.0":
        raise ValueError("GLB JSON asset version must be 2.0")
    require_embedded_uris(document)
    buffers = json_array(document, "buffers")
    sizes = []
    for index, buffer in enumerate(buffers):
        length = natural_number(buffer.get("byteLength"), f"buffers[{index}].byteLength")
        if "uri" not in buffer:
            if index != 0 or binary_size is None:
                raise ValueError("only buffers[0] may consume the GLB BIN chunk")
            if not 0 <= binary_size - length <= 3:
                raise ValueError("GLB BIN length does not match buffers[0].byteLength and padding")
        sizes.append(length)
    if binary_size is not None and (not buffers or "uri" in buffers[0]):
        raise ValueError("GLB BIN chunk has no matching buffer")
    views = json_array(document, "bufferViews")
    for index, view in enumerate(views):
        buffer_number = natural_number(view.get("buffer"), f"bufferViews[{index}].buffer")
        offset = natural_number(view.get("byteOffset", 0), f"bufferViews[{index}].byteOffset")
        length = natural_number(view.get("byteLength"), f"bufferViews[{index}].byteLength")
        if buffer_number >= len(sizes) or offset + length > sizes[buffer_number]:
            raise ValueError(f"bufferViews[{index}] is outside its declared buffer")
    images = json_array(document, "images")
    for index, image in enumerate(images):
        if ("uri" in image) == ("bufferView" in image):
            raise ValueError(f"images[{index}] must use one embedded source")
        if "bufferView" in image:
            slot = natural_number(image["bufferView"], f"images[{index}].bufferView")
            if slot >= len(views):
                raise ValueError(f"images[{index}].bufferView is out of range")
    meshes = json_array(document, "meshes")
    if not meshes or not any(mesh.get("primitives") for mesh in meshes):
        raise ValueError("GLB has no mesh primitives")
    extensions = document.get("extensions") or {}
    lights = (extensions.get("KHR_lights_punctual") or {}).get("lights", [])
    return {
        "meshes": len(meshes),
        "cameras": len(json_array(document, "cameras")),
        "punctual_lights": len(lights),
        "embedded_images": len(images),
    }


def mp4_details(path):
    """Check the ISO BMFF box envelope without claiming any codec or playback check."""
    file_size = path.stat().st_size
    found = set()
    with path.open("rb") as handle:
        while handle.tell() < file_size:
            start = handle.tell()
            length, kind = struct.unpack(">I4s", read_exact(handle, 8))
            if length == 1:
                length = struct.unpack(">Q", read_exact(handle, 8))[0]
            elif length == 0:
                length = file_size - start
            if length < handle.tell() - start or start + length > file_size:
                raise ValueError(f"MP4 box {kind!r} has invalid bounds")
            if length > handle.tell() - start:
                found.add(kind)
            handle.seek(start + length)
    if not {b"ftyp", b"moov", b"mdat"}.issubset(found):
        raise ValueError("expected nonempty MP4 ftyp, moov and mdat boxes")
    return {"container": "ISO BMFF"}


def check_artifact(root, relative, exact_dimensions):
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("artifact resolves outside the output folder")
    if not path.is_file() or not path.stat().st_size:
        raise ValueError("missing or empty regular file")
    details = {"bytes": path.stat().st_size}
    if path.suffix == ".png":
        details.update(png_details(path, exact_dimensions))
    elif path.suffix == ".glb":
        details.update(glb_details(path))
    elif path.suffix == ".mp4":
        details.update(mp4_details(path))
    elif path.suffix == ".md" and not path.read_text(encoding="utf-8").strip():
        raise ValueError("review document has no text")
    return details


def check_delivery(root):
    root = root.resolve()
    results = {}
    for relative, exact_dimensions in expected_artifacts().items():
        try:
            details = check_artifact(root, relative, exact_dimensions)
        except (OSError, ValueError, TypeError, AttributeError, RuntimeError) as error:
            results[relative] = {"pass": False, "issue": str(error)}
        else:
            results[relative] = {"pass": True, **details}
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parent.parent / "output"
    parser.add_argument("output", type=Path, nargs="?", default=default_root)
    parser.add_argument("--json", action="store_true", help="write the per-file report as JSON")
    args = parser.parse_args(argv)
    results = check_delivery(args.output)
    passed = sum(result["pass"] for result in results.values())
    if args.json:
        print(json.dumps({"passed": passed, "total": len(results), "files": results}, indent=2))
    else:
        for relative, result in results.items():
            if not result["pass"]:
                print(f"FAIL {relative}  {result['issue']}")
            elif "width" in result:
                print(f"PASS {relative}  {result['width']}×{result['height']}")
            elif "meshes" in result:
                print(
                    f"PASS {relative}  {result['meshes']} meshes, "
                    f"{result['cameras']} cameras, {result['punctual_lights']} punctual lights"
                )
            else:
                print(f"PASS {relative}  {result['bytes']:,} bytes")
        print(f"{passed}/{len(results)} required artifacts passed file checks.")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
