"""Create an editable Blender globe starting scene from the adjacent flat color art."""
import argparse
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector


def surface_xyz(radius, longitude, latitude):
    """Return XYZ, where +Z is north and east rotates from +X toward +Y."""
    lon, lat = math.radians(longitude), math.radians(latitude)
    return radius * Vector(
        (math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat))
    )


def make_mesh(radius, longitude_steps=192, latitude_steps=96):
    vertices, faces, face_uvs = [(0.0, 0.0, -radius)], [], []
    for ring in range(1, latitude_steps):
        latitude = 180.0 * ring / latitude_steps - 90.0
        for column in range(longitude_steps):
            longitude = 360.0 * column / longitude_steps - 180.0
            vertices.append(tuple(surface_xyz(radius, longitude, latitude)))
    north_pole = len(vertices)
    vertices.append((0.0, 0.0, radius))

    def point(ring, column):
        return 1 + (ring - 1) * longitude_steps + column % longitude_steps

    for ring_from in range(latitude_steps):
        ring_to = ring_from + 1
        v0, v1 = ring_from / latitude_steps, ring_to / latitude_steps
        for column in range(longitude_steps):
            following = column + 1
            u0, u1 = column / longitude_steps, following / longitude_steps
            if ring_from == 0:
                faces.append((0, point(ring_to, following), point(ring_to, column)))
                face_uvs.append((((u0 + u1) / 2, v0), (u1, v1), (u0, v1)))
            elif ring_to == latitude_steps:
                faces.append((point(ring_from, column), point(ring_from, following), north_pole))
                face_uvs.append(((u0, v0), (u1, v0), ((u0 + u1) / 2, v1)))
            else:
                faces.append(
                    (point(ring_from, column), point(ring_from, following),
                     point(ring_to, following), point(ring_to, column))
                )
                face_uvs.append(((u0, v0), (u1, v0), (u1, v1), (u0, v1)))

    mesh = bpy.data.meshes.new("Earth_Surface_192x96")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    uv_layer = mesh.uv_layers.new(name="Earth_Longitude_Latitude")
    for polygon, coordinates in zip(mesh.polygons, face_uvs):
        polygon.use_smooth = True
        for loop_index, uv in zip(polygon.loop_indices, coordinates):
            uv_layer.data[loop_index].uv = uv
    return mesh


def make_material(texture_path):
    material = bpy.data.materials.new("Earth_Teal_Sand_Color")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    shader = nodes.get("Principled BSDF")
    shader.inputs["Roughness"].default_value = 0.62
    color = nodes.new("ShaderNodeTexImage")
    color.label = "Original Natural Earth-based color art"
    color.image = bpy.data.images.load(str(texture_path), check_existing=True)
    color.image.pack()
    material.node_tree.links.new(color.outputs["Color"], shader.inputs["Base Color"])
    return material


def aim_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def link_camera(scene, radius):
    camera = bpy.data.objects.new("Camera_Earth_AsiaPacific", bpy.data.cameras.new("Earth_Ortho"))
    scene.collection.objects.link(camera)
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 4.3 * radius
    camera.data.clip_end = 20.0 * radius
    camera.location = surface_xyz(4.2 * radius, 112.0, 19.0)
    aim_at(camera, (0, 0, 0))
    scene.camera = camera


def link_sun(scene, name, direction, energy, color):
    light = bpy.data.lights.new(name, type="SUN")
    light.energy, light.color = energy, color
    light.angle = math.radians(23.0)
    obj = bpy.data.objects.new(name, light)
    scene.collection.objects.link(obj)
    obj.location = direction
    aim_at(obj, (0, 0, 0))


def build_globe(radius, texture_path, output):
    scene = bpy.data.scenes.new("Earth_Art_Seed")
    bpy.context.window.scene = scene
    for other in list(bpy.data.scenes):
        if other != scene:
            bpy.data.scenes.remove(other)

    globe = bpy.data.objects.new("Earth_Surface", make_mesh(radius))
    scene.collection.objects.link(globe)
    globe.data.materials.append(make_material(texture_path))
    globe["earth_art_radius"] = radius
    globe["longitude_origin"] = "+X at 0 degrees, +Y at 90 degrees east"
    globe["design_grain"] = "Decorative land and ocean color. Not geography layers."
    link_camera(scene, radius)
    world = bpy.data.worlds.new("Earth_World_Night_Teal")
    world.use_nodes = True
    world.node_tree.nodes.get("Background").inputs["Color"].default_value = (0.013, 0.041, 0.048, 1.0)
    world.node_tree.nodes.get("Background").inputs["Strength"].default_value = 0.7
    scene.world = world
    link_sun(scene, "Earth_Key", surface_xyz(1.0, 82.0, 57.0), 2.4, (1.0, 0.94, 0.83))
    link_sun(scene, "Earth_Fill", surface_xyz(1.0, 212.0, -13.0), 0.30, (0.62, 0.83, 1.0))

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "AgX"
    scene.render.filepath = "//earth-seed-preview.png"
    bpy.context.view_layer.objects.active = globe
    globe.select_set(True)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                area.spaces.active.region_3d.view_perspective = "CAMERA"

    output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output))
    print("Globe seed created:", output)


def main():
    if not bpy.app.background or bpy.data.filepath:
        raise SystemExit("Use a fresh Blender --background --factory-startup process.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Path to a new .blend file")
    parser.add_argument("--radius", type=float, default=10.0, help="Art scene radius in Blender units")
    cli_args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    args = parser.parse_args(cli_args)
    output = args.output.resolve()
    if output.suffix.lower() != ".blend" or output.exists():
        parser.error("--output must be a new .blend file")
    if not math.isfinite(args.radius) or args.radius < 0.1:
        parser.error("--radius must be finite and at least 0.1")
    texture = Path(__file__).resolve().with_name("earth-base-color.jpg")
    if not texture.is_file():
        parser.error(f"Missing texture: {texture}")
    build_globe(args.radius, texture, output)


if __name__ == "__main__":
    main()
