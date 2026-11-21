"""Shared scene library for The Ocean Has Floors coastal dioramas.

Coordinate convention (from brief/CAMERAS_AND_TRAVEL.md):
    +X east, +Y north, +Z up, 1 Blender unit = 1 metre, water surface at Z = 0.

Everything is authored with the data API plus numpy so it also runs headless.
"""
import math

import bpy
import numpy as np
from mathutils import Vector

# ----------------------------------------------------------------------------
# small math helpers
# ----------------------------------------------------------------------------


def smoothstep(edge0, edge1, x):
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def lerp(a, b, t):
    return a + (b - a) * t


# ----------------------------------------------------------------------------
# materials
# ----------------------------------------------------------------------------

def make_material(name, base, rough=0.9, metallic=0.0, alpha=1.0,
                  emission=None, emission_strength=0.0, backface_cull=False):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    use_nodes = True
    try:
        mat.use_nodes = use_nodes
    except Exception:
        pass
    nodes = mat.node_tree.nodes
    bsdf = None
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            bsdf = node
            break
    if bsdf is None:
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        out = nodes.get('Material Output') or nodes.new('ShaderNodeOutputMaterial')
        mat.node_tree.links.new(bsdf.outputs[0], out.inputs[0])
    bsdf.inputs['Base Color'].default_value = (base[0], base[1], base[2], 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metallic
    if 'Alpha' in bsdf.inputs:
        bsdf.inputs['Alpha'].default_value = alpha
    if emission is not None:
        if 'Emission Color' in bsdf.inputs:
            bsdf.inputs['Emission Color'].default_value = (*emission, 1.0)
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = emission_strength
    if alpha < 1.0:
        try:
            mat.surface_render_method = 'BLENDED'
        except Exception:
            try:
                mat.blend_method = 'BLEND'
            except Exception:
                pass
    mat.use_backface_culling = backface_cull
    mat.diffuse_color = (base[0], base[1], base[2], alpha)
    return mat


INK = None


def ink_material():
    """Ink line material used by the inverted-hull outline.

    The cache is validated on every call: opening another .blend (or resetting
    the scene) invalidates datablock references, and a stale StructRNA here
    aborts a whole build halfway through.
    """
    global INK
    if INK is not None:
        try:
            if INK.name:
                return INK
        except ReferenceError:
            INK = None
    INK = bpy.data.materials.get('MAT_Ink_Line')
    if INK is None:
        INK = make_material('MAT_Ink_Line', (0.045, 0.040, 0.040), rough=1.0,
                            backface_cull=True)
    return INK


def add_outline(obj, thickness=0.05):
    """Classic inverted-hull toon outline: solidify outward, flip normals, cull front."""
    ink = ink_material()
    if ink.name not in [m.name for m in obj.data.materials if m]:
        obj.data.materials.append(ink)
    ink_index = list(obj.data.materials).index(ink)
    mod = obj.modifiers.new('InkOutline', 'SOLIDIFY')
    mod.thickness = thickness
    mod.offset = 1.0
    mod.use_flip_normals = True
    mod.use_rim = False
    mod.material_offset = ink_index
    mod.material_offset_rim = ink_index
    return mod


# ----------------------------------------------------------------------------
# meshes
# ----------------------------------------------------------------------------

def mesh_from(name, verts, faces, materials=None, collection=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.update()
    ob = bpy.data.objects.new(name, me)
    for mat in (materials or []):
        me.materials.append(mat)
    (collection or bpy.context.scene.collection).objects.link(ob)
    return ob


def grid_mesh(name, xs, ys, heights, face_materials, collection=None,
              material_by_face=None):
    """Build a quad grid mesh fast via foreach_set.

    xs, ys: 1-D coordinate arrays. heights: 2-D (ny, nx). face_materials:
    list of materials; material_by_face: 2-D int array (ny-1, nx-1).
    """
    nx, ny = len(xs), len(ys)
    verts = np.empty((ny, nx, 3), dtype=np.float32)
    verts[:, :, 0] = xs[None, :]
    verts[:, :, 1] = ys[:, None]
    verts[:, :, 2] = heights

    n_quads = (ny - 1) * (nx - 1)
    quads = np.empty((n_quads, 4), dtype=np.int64)
    idx = np.arange(ny * nx).reshape(ny, nx)
    quads[:, 0] = idx[:-1, :-1].ravel()
    quads[:, 1] = idx[:-1, 1:].ravel()
    quads[:, 2] = idx[1:, 1:].ravel()
    quads[:, 3] = idx[1:, :-1].ravel()

    me = bpy.data.meshes.new(name)
    me.vertices.add(ny * nx)
    me.vertices.foreach_set('co', verts.ravel())
    me.loops.add(n_quads * 4)
    me.loops.foreach_set('vertex_index', quads.ravel())
    me.polygons.add(n_quads)
    me.polygons.foreach_set('loop_start', np.arange(0, n_quads * 4, 4, dtype=np.int32))
    for mat in face_materials:
        me.materials.append(mat)
    if material_by_face is not None:
        me.polygons.foreach_set('material_index', material_by_face.ravel().astype(np.int32))
    me.update()
    me.validate()
    ob = bpy.data.objects.new(name, me)
    (collection or bpy.context.scene.collection).objects.link(ob)
    return ob


def box_mesh(name, size, location, materials, collection, rotation=(0, 0, 0),
             material_index=0):
    hx, hy, hz = size[0] / 2, size[1] / 2, size[2] / 2
    verts = [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
             (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    ob = mesh_from(name, verts, faces, materials, collection)
    ob.location = location
    ob.rotation_euler = rotation
    me = ob.data
    if len(materials) > 1:
        me.polygons.foreach_set('material_index', [material_index] * len(me.polygons))
    return ob


def cylinder_mesh(name, radius, depth, location, material, collection,
                  segments=10, cap=True):
    verts = []
    faces = []
    for s in range(segments):
        a = 2 * math.pi * s / segments
        verts.append((math.cos(a) * radius, math.sin(a) * radius, -depth / 2))
    for s in range(segments):
        a = 2 * math.pi * s / segments
        verts.append((math.cos(a) * radius, math.sin(a) * radius, depth / 2))
    for s in range(segments):
        n = (s + 1) % segments
        faces.append((s, n, n + segments, s + segments))
    if cap:
        faces.append(tuple(range(segments - 1, -1, -1)))
        faces.append(tuple(range(segments, segments * 2)))
    ob = mesh_from(name, verts, faces, [material], collection)
    ob.location = location
    return ob


def join_objects(objects, name, collection):
    """Join a list of objects into one using bmesh (no operator context needed)."""
    import bmesh
    target_mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    material_slots = []
    for ob in objects:
        me = ob.data.copy()
        me.transform(ob.matrix_world)
        tmp = bpy.data.objects.new('_tmp', me)
        collection.objects.link(tmp)
        # remap materials into a shared slot list
        remap = []
        for mat in me.materials:
            if mat not in material_slots:
                material_slots.append(mat)
            remap.append(material_slots.index(mat))
        for poly in me.polygons:
            poly.material_index = remap[min(poly.material_index, len(remap) - 1)]
        bm.from_mesh(me)
        bpy.data.objects.remove(tmp, do_unlink=True)
        bpy.data.meshes.remove(me)
        bpy.data.objects.remove(ob, do_unlink=True)
    bm.to_mesh(target_mesh)
    bm.free()
    for mat in material_slots:
        target_mesh.materials.append(mat)
    joined = bpy.data.objects.new(name, target_mesh)
    collection.objects.link(joined)
    return joined
