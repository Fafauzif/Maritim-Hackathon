import sys, glob, cv2, numpy as np
fs = sorted(glob.glob(sys.argv[1] + '/*.jpg')); out = sys.argv[2]; per = 6
for s in range(0, len(fs), per):
    ims = []
    for f in fs[s:s+per]:
        im = cv2.resize(cv2.imread(f), (960, 540))
        cv2.putText(im, f.split('/')[-1][:-4], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
        ims.append(im)
    while len(ims) < per: ims.append(np.zeros_like(ims[0]))
    grid = np.vstack([np.hstack(ims[i:i+2]) for i in range(0, per, 2)])
    cv2.imwrite(f'{out}_{s//per}.jpg', grid, [cv2.IMWRITE_JPEG_QUALITY, 80])
