# coding: utf-8
"""Durgun kare orani (14 Kas, danisman olcusu): 480x270 gri, ardisik kare mutlak farkinin ortalamasi < 0,5 olan karelerin orani.
v2 olcusu (son/v2_fark.json) ile ayni yontem. python -I durgun.py VIDEO.mp4 [bolum sinirlari sn: 10 57.8 ...]"""
import json
import subprocess
import sys

import numpy as np

W, H = 480, 270


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    v = sys.argv[1]
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", v, "-vf", "scale=%d:%d" % (W, H), "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
    onc, fark = None, []
    while True:
        b = p.stdout.read(W * H)
        if len(b) < W * H:
            break
        a = np.frombuffer(b, np.uint8).astype(np.int16)
        fark.append(0.0 if onc is None else float(np.abs(a - onc).mean()))
        onc = a
    p.wait()
    f = np.array(fark)
    s = [0.0] + [float(x) for x in sys.argv[2:]] + [len(f) / 30]
    print("kare", len(f), "sure", len(f) / 30, "durgun (fark<0,5) toplam %.1f%%" % (100 * (f < .5).mean()))
    for a, b in zip(s, s[1:]):
        k = f[int(a * 30):int(b * 30)]
        print("  %.1f-%.1f sn: %.1f%% (%d kare)" % (a, b, 100 * (k < .5).mean(), len(k)))
    json.dump({"fark": fark}, open(v + ".fark.json", "w"))


if __name__ == "__main__":
    main()
