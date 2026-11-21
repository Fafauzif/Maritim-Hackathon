"""Assemble delivery media: clean stills, pitch plates, review sheets and previews.

    python make_media.py --run-root <run> --staging-root <bundle>
"""
import argparse
import json
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

FONT_DIR = r"C:\Windows\Fonts"


def font(size, bold=False):
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    path = os.path.join(FONT_DIR, name)
    if not os.path.exists(path):
        path = os.path.join(FONT_DIR, "arialbd.ttf" if bold else "arial.ttf")
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def fit(path, size):
    im = Image.open(path).convert("RGB")
    return ImageOps.fit(im, size, method=Image.LANCZOS, centering=(0.5, 0.5))


def panel(img, box, caption=None, caption_h=34, fg=(245, 241, 230)):
    d = ImageDraw.Draw(img)
    x, y, w, h = box
    d.rectangle((x - 2, y - 2, x + w + 2, y + h + 2), fill=(30, 28, 25))
    img.paste(box_img(img, (w, h), None), (x, y)) if False else None
    if caption:
        d.rectangle((x, y + h, x + w, y + h + caption_h), fill=(24, 23, 21))
        d.text((x + 10, y + h + 7), caption, font=font(18), fill=fg)


def box_img(_img, _size, _unused):
    return Image.new("RGB", _size)


def make_pitch(run, stage):
    base_path = os.path.join(stage, "media", "coasts", "kodingareng", "approach.png")
    base = fit(base_path, (1920, 1080))
    sec_path = os.path.join(stage, "media", "coasts", "kodingareng", "section.png")
    W, H = 1920, 1080
    cream = (247, 243, 232)
    ink = (22, 21, 19)
    accent = (232, 132, 44)
    deep = (54, 144, 174)

    def base_plate(title, subtitle):
        im = base.copy()
        d = ImageDraw.Draw(im, "RGBA")
        d.rectangle((0, 0, W, 92), fill=(18, 22, 24, 214))
        d.text((44, 16), title, font=font(34, True), fill=cream)
        d.text((44, 56), subtitle, font=font(20), fill=(206, 214, 210))
        d.rectangle((0, H - 62, W, H), fill=(18, 22, 24, 214))
        d.text((44, H - 48),
               "GLORYS12 daily modeled mean · 16 Apr 2020 UTC · one ~9 km cell · "
               "regional estimate, not a local measurement · scene art is illustrative",
               font=font(17), fill=(206, 214, 210))
        return im

    def inset(im, depth_label, speed, bearing, arrow_deg, color, note):
        d = ImageDraw.Draw(im, "RGBA")
        x0, y0, x1, y1 = 48, 112, 640, 470
        d.rounded_rectangle((x0, y0, x1, y1), radius=16, fill=(17, 21, 23, 226),
                            outline=(*color, 230), width=2)
        d.text((x0 + 26, y0 + 20), "REGIONAL MODEL INSET", font=font(19, True),
               fill=(*color, 255))
        d.text((x0 + 26, y0 + 50), "GLORYS12 · 0.083° (~9 km) · cell centre −5.1667, 119.2500",
               font=font(15), fill=(205, 212, 208))
        d.line((x0 + 26, y0 + 78, x1 - 26, y0 + 78), fill=(90, 100, 102, 220), width=1)
        d.text((x0 + 26, y0 + 94), depth_label, font=font(38, True), fill=cream)
        # arrow dial
        cx, cy, r = x1 - 118, y0 + 178, 72
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(90, 100, 102, 220), width=2)
        d.text((cx - 7, cy - r - 26), "N", font=font(17, True), fill=cream)
        d.text((cx + r + 8, cy - 9), "E", font=font(15), fill=(170, 180, 178))
        d.text((cx - 7, cy + r + 4), "S", font=font(15), fill=(170, 180, 178))
        d.text((cx - r - 24, cy - 9), "W", font=font(15), fill=(170, 180, 178))
        ang = __import__("math").radians(arrow_deg)
        dx, dy = __import__("math").sin(ang), -__import__("math").cos(ang)
        d.line((cx, cy, cx + dx * (r - 16), cy + dy * (r - 16)), fill=(*color, 255), width=6)
        # arrow head
        import math
        for s in (-0.5, 0.5):
            a2 = ang + math.pi + s
            d.line((cx + dx * (r - 16), cy + dy * (r - 16),
                    cx + dx * (r - 16) + math.sin(a2) * 18,
                    cy + dy * (r - 16) - math.cos(a2) * 18), fill=(*color, 255), width=6)
        d.text((x0 + 26, y0 + 160), speed, font=font(27, True), fill=cream)
        d.text((x0 + 26, y0 + 196), bearing, font=font(23), fill=(*color, 255))
        import textwrap
        note_lines = textwrap.wrap(note, width=62)
        for k, line in enumerate(note_lines):
            d.text((x0 + 26, y0 + 246 + k * 21), line, font=font(15),
                   fill=(196, 204, 200))
        d.text((x0 + 26, y1 - 34), "Regional data, not drawn at local scale.",
               font=font(14), fill=(160, 168, 166))
        return im

    surface = base_plate("THE OCEAN HAS FLOORS · KODINGARENG LOMPO",
                         "Same place, same date, two modeled depths · fixed camera")
    surface = inset(surface, "0.494 m below surface", "0.093 m/s",
                    "bearing 264° toward (west)", 264, accent,
                    "Near-surface daily mean vector. Two officers can reproduce this "
                    "row from the verified fixture.")
    deeper = base_plate("THE OCEAN HAS FLOORS · KODINGARENG LOMPO",
                        "Same place, same date, two modeled depths · fixed camera")
    deeper = inset(deeper, "9.573 m below surface", "0.074 m/s",
                   "bearing 45° toward (northeast)", 45, deep,
                   "Deeper daily mean vector. Daily averages smooth within-day variation.")
    os.makedirs(os.path.join(stage, "media", "pitch"), exist_ok=True)
    surface.save(os.path.join(stage, "media", "pitch", "kodingareng-surface.png"))
    deeper.save(os.path.join(stage, "media", "pitch", "kodingareng-deeper.png"))

    # section explanation plate
    sec = fit(sec_path, (W, H))
    d = ImageDraw.Draw(sec, "RGBA")
    d.rectangle((0, 0, W, 92), fill=(18, 22, 24, 214))
    d.text((44, 16), "SECTION A–B · KODINGARENG LOMPO", font=font(34, True), fill=cream)
    d.text((44, 56), "Illustrated cut through the landing and survey boat · x3.2 vertical exaggeration",
           font=font(20), fill=(206, 214, 210))
    # waterline
    wy = 0.5801 * H
    for x in range(0, W, 26):
        d.line((x, wy, min(x + 14, W), wy), fill=(240, 235, 220, 210), width=2)
    d.text((880, wy - 30), "WATERLINE  Z = 0", font=font(17, True), fill=(240, 235, 220))
    d.text((W - 330, 112), "A  OFFSHORE  →", font=font(19, True), fill=(232, 132, 44))
    d.text((44, 112), "←  B  INLAND", font=font(19, True), fill=(232, 132, 44))
    d.text((int(0.79 * W), wy + 22), "survey boat", font=font(17), fill=cream)
    d.text((int(0.19 * W), wy - 58), "landing pavilion", font=font(17), fill=cream)
    d.text((44, H - 150), "Cut follows the authored A–B line through the landing and boat",
           font=font(19), fill=cream)
    d.text((44, H - 120), "Vertical exaggeration x3.2 · pivot at waterline Z=0",
           font=font(17), fill=(220, 212, 200))
    d.text((44, H - 94), "Seabed and strata are illustrative, not surveyed bathymetry",
           font=font(17), fill=(220, 212, 200))
    d.rectangle((0, H - 62, W, H), fill=(18, 22, 24, 214))
    d.text((44, H - 48),
           "Same boat and jetty anchors as the overhead art · animate coast and section as "
           "mutually exclusive views · values in runtime manifest",
           font=font(17), fill=(206, 214, 210))
    sec.save(os.path.join(stage, "media", "pitch", "kodingareng-section.png"))
    return {"surface": "media/pitch/kodingareng-surface.png",
            "deeper": "media/pitch/kodingareng-deeper.png",
            "section": "media/pitch/kodingareng-section.png"}


def tile_sheet(items, cols, rows, cell, out, title=None, bg=(20, 22, 24),
               caption_h=36, title_h=58, fg=(244, 240, 230)):
    W = cols * cell[0] + (cols + 1) * 12
    H = rows * (cell[1] + caption_h) + (rows + 1) * 12 + (title_h if title else 0)
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    y0 = 12
    if title:
        d.text((18, 16), title, font=font(27, True), fill=fg)
        y0 += title_h
    for idx, (path, caption) in enumerate(items):
        r, c = divmod(idx, cols)
        x = 12 + c * (cell[0] + 12)
        y = y0 + r * (cell[1] + caption_h + 12)
        if path and os.path.exists(path):
            im.paste(fit(path, cell), (x, y))
        else:
            d.rectangle((x, y, x + cell[0], y + cell[1]), fill=(42, 44, 46))
            d.text((x + 12, y + 12), "missing", font=font(18), fill=(220, 120, 110))
        d.rectangle((x, y + cell[1], x + cell[0], y + cell[1] + caption_h),
                    fill=(28, 30, 32))
        d.text((x + 10, y + cell[1] + 7), caption, font=font(17), fill=fg)
    im.save(out)
    return out


def make_review(run, stage):
    made = {}
    previews = os.path.join(run, "renders", "previews")
    sites = ("kodingareng", "tunda", "amur")
    # look contact sheet for the first gate
    items = []
    for slug, caption in (("godview", "OVERVIEW · 38 mm · high oblique"),
                          ("mapview", "PLAN · north-up orthographic"),
                          ("approach", "APPROACH · waterfront route"),
                          ("detail", "DETAIL · boat / jetty / architecture"),
                          ("section", "SECTION A–B · x3.2 illustrative cut")):
        items.append((os.path.join(previews, "kodingareng", slug + ".png"), caption))
    items.append((os.path.join(run, "proofs", "look", "kodingareng-coverage.png")
                  if False else os.path.join(run, "proofs", "coverage",
                                             "kodingareng_COAST_OVERVIEW.png"),
                  "COVERAGE PASS · QA only, not delivery art"))
    made["look_sheet"] = tile_sheet(items, 3, 2, (620, 349),
                                    os.path.join(run, "proofs", "look",
                                                 "kodingareng-look-contact-sheet.png"),
                                    title="KODINGARENG LOOK PROOF · 960 px review sheet")
    # v1/v2 before-after, three rows
    ba = []
    for site in sites:
        v1 = os.path.abspath(os.path.join(run, "..", "..", "..", "..", "output",
                                          "coasts", site, "godview.png"))
        ba.append((v1, "%s · V1 baseline overview" % site.upper()))
        ba.append((os.path.join(previews, site, "godview.png"),
                   "%s · V2 revised overview" % site.upper()))
    made["before_after"] = tile_sheet(ba, 2, 3, (620, 349),
                                      os.path.join(stage, "review", "before-after.png"),
                                      title="BEFORE / AFTER · left = v1, right = v2")
    # all-site equal-display parity
    par = []
    for site in sites:
        par.append((os.path.join(previews, site, "godview.png"),
                    "%s · overview" % site.upper()))
        par.append((os.path.join(previews, site, "section.png"),
                    "%s · section" % site.upper()))
    made["parity"] = tile_sheet(par, 3, 2, (620, 349),
                                os.path.join(stage, "review", "parity-sheet.png"),
                                title="ALL-SITE PARITY SHEET · equal display size")
    # 320 px legibility reductions
    small_dir = os.path.join(run, "proofs", "320")
    os.makedirs(small_dir, exist_ok=True)
    for site in sites:
        for slug in ("godview", "mapview", "approach", "detail", "section"):
            p = os.path.join(previews, site, slug + ".png")
            if os.path.exists(p):
                im = fit(p, (1280, 720))
                im.resize((320, 180), Image.LANCZOS).save(
                    os.path.join(small_dir, "%s_%s_320.png" % (site, slug)))
    return made


def make_runtime_sheet(run, stage):
    check = os.path.join(run, "renders", "import-check")
    items = []
    for aid, caption in (
            ("globe", "GLOBE · clean import"),
            ("kit", "COMMON KIT · clean import"),
            ("coast_kodingareng", "KODINGARENG · coast import"),
            ("section_kodingareng", "KODINGARENG · section import"),
            ("coast_tunda", "TUNDA · coast import"),
            ("section_tunda", "TUNDA · section import"),
            ("coast_amur", "AMUR · coast import"),
            ("section_amur", "AMUR · section import")):
        items.append((os.path.join(check, aid + ".png"), caption))
    if any(not os.path.exists(p) for p, _ in items):
        return None
    return tile_sheet(items, 4, 2, (455, 256),
                      os.path.join(stage, "review", "runtime-parity.png"),
                      title="RUNTIME PARITY · each GLB imported in a fresh Blender process")


def copy_clean(stage):
    import shutil
    src4k = os.path.join(stage, "..", "..", "work", "runs",
                         "20261121T1445-local", "renders", "final-4k")
    # paths are resolved by caller before this function in main
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--staging-root", required=True)
    a = ap.parse_args()
    run, stage = a.run_root, a.staging_root
    # clean stills
    for site in ("kodingareng", "tunda", "amur"):
        src = os.path.join(run, "renders", "final-4k", site)
        dst = os.path.join(stage, "media", "coasts", site)
        os.makedirs(dst, exist_ok=True)
        for slug in ("godview", "mapview", "approach", "detail", "section"):
            p = os.path.join(src, slug + ".png")
            if os.path.exists(p):
                Image.open(p).save(os.path.join(dst, slug + ".png"))
    globe_src = os.path.join(run, "renders", "final-4k", "globe", "globe-overview.png")
    if os.path.exists(globe_src):
        os.makedirs(os.path.join(stage, "media", "globe"), exist_ok=True)
        Image.open(globe_src).save(os.path.join(stage, "media", "globe",
                                                "globe-overview.png"))
    kit_src = os.path.join(run, "proofs", "look", "kit_asset-sheet.png")
    if os.path.exists(kit_src):
        os.makedirs(os.path.join(stage, "media", "kit"), exist_ok=True)
        Image.open(kit_src).save(os.path.join(stage, "media", "kit", "asset-sheet.png"))
    os.makedirs(os.path.join(stage, "review"), exist_ok=True)
    out = {}
    try:
        out["pitch"] = make_pitch(run, stage)
    except Exception as exc:
        out["pitch_error"] = str(exc)
    try:
        out["review"] = make_review(run, stage)
    except Exception as exc:
        out["review_error"] = str(exc)
    try:
        rp = make_runtime_sheet(run, stage)
        if rp:
            out["runtime_parity"] = rp
    except Exception as exc:
        out["runtime_error"] = str(exc)
    with open(os.path.join(run, "logs", "media-build.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("MEDIA " + json.dumps(out, default=str))


if __name__ == "__main__":
    main()
