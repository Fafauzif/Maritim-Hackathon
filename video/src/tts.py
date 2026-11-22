import sys, numpy as np, soundfile as sf
sys.path.insert(0, 'src')
from script import SEGMENTS, VOICE, SPEED
from kokoro import KPipeline
only = sys.argv[1].split(',') if len(sys.argv) > 1 else None
pipe = KPipeline(lang_code='b' if VOICE.startswith('b') else 'a', repo_id='hexgrad/Kokoro-82M')
FIX = {'Ferdiansyah': '[Ferdiansyah](/fɜːdiˈɑːnʃə/)', 'Pulau': '[Pulau](/pˈuːlaʊ/)', 'Angger': '[Angger](/ˈɑːŋɡə/)',
       'Kodingareng': '[Kodingareng](/kˌəʊdɪŋɡɑːɹˈɛŋ/)', 'Razdolnaya': '[Razdolnaya](/ɹɑːzdˈɒlnəjə/)',
       'Fadhlurohman': '[Fadhlurohman](/fˌɑːdluːɹˈəʊmɑːn/)', 'Makassar': '[Makassar](/məkˈæsə/)',
       'Vladivostok': '[Vladivostok](/vlˌædɪvˈɒstɒk/)', 'Tunda': '[Tunda](/tˈʊndə/)', 'Alifia': '[Alifia](/ɐlˈiːfiə/)'}
for scene, sid, text, pause in SEGMENTS:
    if only and sid not in only: continue
    for k, v in FIX.items(): text = text.replace(k, v)
    audio = np.concatenate([a.numpy() if hasattr(a, 'numpy') else a for _, _, a in pipe(text, voice=VOICE, speed=SPEED)])
    sf.write(f'audio/seg/{sid}.wav', audio, 24000)
    print(sid, round(len(audio) / 24000, 2), flush=True)
