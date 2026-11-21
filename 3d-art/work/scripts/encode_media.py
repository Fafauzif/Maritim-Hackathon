"""Phase 06 · encode the films and prove them with ffprobe.

    python encode_media.py

* one H.264 1080p24 travel film per coast from its rendered frame sequence,
* `coast-reel.mp4`: Earth intro -> the three coasts -> Earth outro,
* `work/reports/media.json` with measured width/height/fps/duration/codec for
  every encoded file (a container that merely exists is not a delivered film).
"""
import json
import os
import subprocess
import sys

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
RENDERS = os.path.join(ART, 'work', 'renders')
OUTPUT = os.path.join(ART, 'output')
REPORTS = os.path.join(ART, 'work', 'reports')

FFMPEG = r"C:\Users\fauzi\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\fauzi\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

SITES = ('kodingareng', 'tunda', 'amur')
COAST_FRAMES = 132
GLOBE_INTRO_FRAMES = 72
GLOBE_OUTRO_START = 49
GLOBE_OUTRO_FRAMES = 24


def run(cmd, label):
    print('RUN', label)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print('FAILED', label, proc.returncode)
        print((proc.stderr or '')[-2000:])
        raise SystemExit(1)
    return proc


def encode_frames(frames_dir, out_path, start=1, count=None):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cmd = [FFMPEG, '-y', '-framerate', '24', '-start_number', str(start),
           '-i', os.path.join(frames_dir, 'frame_%04d.png')]
    if count:
        cmd += ['-frames:v', str(count)]
    cmd += ['-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
            '-pix_fmt', 'yuv420p', '-r', '24', '-movflags', '+faststart', out_path]
    run(cmd, 'encode ' + os.path.basename(out_path))
    return out_path


def probe(path):
    cmd = [FFPROBE, '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=width,height,r_frame_rate,codec_name,nb_frames',
           '-show_entries', 'format=duration,size',
           '-of', 'json', path]
    proc = run(cmd, 'probe ' + os.path.basename(path))
    data = json.loads(proc.stdout)
    stream = (data.get('streams') or [{}])[0]
    fmt = data.get('format') or {}
    num, _, den = (stream.get('r_frame_rate') or '0/1').partition('/')
    fps = round(float(num) / float(den or 1), 3) if float(den or 1) else 0.0
    return {
        'path': path.replace('\\', '/'),
        'width': stream.get('width'), 'height': stream.get('height'),
        'fps': fps, 'codec': stream.get('codec_name'),
        'frames': int(stream.get('nb_frames') or 0),
        'duration_s': round(float(fmt.get('duration') or 0), 2),
        'bytes': int(fmt.get('size') or os.path.getsize(path)),
    }


def main():
    media = {'clips': [], 'failures': []}

    globe_dir = os.path.join(RENDERS, 'globe-reel')
    for site in SITES:
        frames_dir = os.path.join(RENDERS, 'travel-frames', site)
        if not os.path.isdir(frames_dir):
            media['failures'].append('no frames for ' + site)
            continue
        have = [n for n in os.listdir(frames_dir) if n.endswith('.png')]
        if len(have) < COAST_FRAMES:
            media['failures'].append('%s frames %d/%d' % (site, len(have), COAST_FRAMES))
            continue
        out = os.path.join(OUTPUT, 'coasts', site, 'travel.mp4')
        encode_frames(frames_dir, out, count=COAST_FRAMES)
        media['clips'].append(probe(out))

    if not os.path.isdir(globe_dir):
        media['failures'].append('no globe reel frames')
        return finish(media)

    intro = os.path.join(RENDERS, 'globe-reel', 'globe_intro.mp4')
    encode_frames(globe_dir, intro, start=1, count=GLOBE_INTRO_FRAMES)
    outro = os.path.join(RENDERS, 'globe-reel', 'globe_outro.mp4')
    encode_frames(globe_dir, outro, start=GLOBE_OUTRO_START, count=GLOBE_OUTRO_FRAMES)

    playable = [os.path.join(OUTPUT, 'coasts', site, 'travel.mp4') for site in SITES]
    if all(os.path.exists(p) for p in playable):
        concat_list = os.path.join(RENDERS, 'globe-reel', 'concat.txt')
        with open(concat_list, 'w', encoding='utf-8') as fh:
            for clip in [intro] + playable + [outro]:
                fh.write("file '%s'\n" % clip.replace('\\', '/'))
        reel = os.path.join(OUTPUT, 'coast-reel.mp4')
        run([FFMPEG, '-y', '-f', 'concat', '-safe', '0', '-i', concat_list,
             '-c', 'copy', '-movflags', '+faststart', reel], 'concat reel')
        media['reel'] = probe(reel)

    return finish(media)


def finish(media):
    os.makedirs(REPORTS, exist_ok=True)
    target = os.path.join(REPORTS, 'media.json')
    tmp = target + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(media, fh, indent=2)
    os.replace(tmp, target)
    print('MEDIA report', target, 'failures:', media['failures'])
    for clip in media['clips']:
        print(' CLIP', os.path.basename(clip['path']), clip['width'], 'x', clip['height'],
              clip['fps'], 'fps', clip['duration_s'], 's')
    if 'reel' in media:
        r = media['reel']
        print(' REEL', r['width'], 'x', r['height'], r['fps'], 'fps', r['duration_s'], 's')
    return 0 if not media['failures'] else 1


if __name__ == '__main__':
    sys.exit(main())
