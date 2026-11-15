# coding: utf-8
"""v5 (15 Kas): kur4.py kopyasi; yazilar ep_metin5.json'dan (sahne 3 altyazi 3 duzeltildi), kareler ayni.
TESLIM VIDEOSU v4 · kurgu ve bindirme (14 Kas, metin surum 4). Islemci; ekran karti gerekmez.
Girdi: KARE4/DU, KARE4/EG, KARE4/plan.json (EPKIP=4 cek_ep.py tam), veri/ep_metin4.json (ep_metin4.py), sekil_sprint PNG'leri.
Cizim yardimcilari kur.py'den (v1-v3) alinir; yazilar ep_metin4.json'dan; kodda yalniz kurgu etiketleri (KAYNAK.md "Ek yazilar").
python -I kur4.py kare CIKTI_KLASOR t1 t2 ...   secilen anlar, 1920x1080 png
python -I kur4.py tam CIKTI.mp4                 1080p H.264, sessiz"""
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)   # python -I betik klasorunu yola koymaz; kur.py ayni klasorde
import kur as K  # noqa: E402
KARE = r"D:\calisma_cikti\film_epistemics\kare4"
FPS, W, H, PW, PH, PY = K.FPS, K.W, K.H, K.PW, K.PH, K.PY
M = json.load(open(os.path.join(KOK, "veri", "ep_metin5.json"), encoding="utf-8"))
Y, SAY = M["yazi"], M["sayac"]
PLAN = json.load(open(os.path.join(KARE, "plan.json"), encoding="utf-8"))
KOSU = (("DU", SAY["kosu"][0], K.ALTIN, "SLEEPER RUN"), ("EG", SAY["kosu"][1], K.MAVI, "CONTROL RUN"))
Fn = K.Fn
from PIL import ImageFont
Fn["kart"] = ImageFont.truetype(os.path.join(K.F, "segoeui.ttf"), 44)
Fn["sowhat"] = ImageFont.truetype(os.path.join(K.F, "georgiab.ttf"), 50)
Fn["etk2"] = ImageFont.truetype(os.path.join(K.F, "segoeuib.ttf"), 22)

# --- zaman cizelgesi (sn)
KART = 10.0
SURE3 = PLAN["DU"]["kare"] / FPS
assert PLAN["DU"]["kare"] == PLAN["EG"]["kare"]
E3 = KART + SURE3                    # 3B bitisi (an 3 durusu sonu); sonrasi son kare
SERIT = (E3 + 5.6, E3 + 11.0)
S3 = E3 + 11.0
SEKIL2 = S3 + 9.0
KAPANIS = S3 + 25.0   # v5: sekil 2 bes saniye daha ekranda (altyazi 3 artik 26 kelime; 3,4 sn okunmuyordu, 8,4 sn oldu); v4: S3 + 20.0
BASLIK = KAPANIS + 4.5
SON = KAPANIS + 16.5   # hedef 105-115 sn (danisman)
GECIS = .6
KUTU_D = .15
D = {ad: PLAN[ad]["duruslar"] for ad in ("DU", "EG")}
for i in range(3):
    assert abs(D["DU"][i]["t0"] - D["EG"][i]["t0"]) < 1e-6 and abs(D["DU"][i]["t1"] - D["EG"][i]["t1"]) < 1e-6
DUR = [(KART + d["t0"], KART + d["t1"]) for d in D["DU"]]
ALT = [(KART + .4, KART + 5.8, Y["s1_a1"]), (KART + 6.0, KART + 11.4, Y["s1_a2"]), (KART + 15.0, KART + 20.0, Y["olcu"]),
       (KART + 20.2, DUR[0][1], Y["s2_a1"]), (E3 + .3, E3 + 5.5, Y["s2_a3"]), (E3 + 5.7, S3, Y["s2_a4"]),
       (S3 + .5, SEKIL2, Y["s3_a1"]), (SEKIL2 + .5, SEKIL2 + 7.4, Y["s3_s2"]), (SEKIL2 + 7.6, KAPANIS, Y["s3_a3"])]
NOT = (KART + 11.6, KART + 15.0)      # sahne 1 kucuk yazi (T3)
ANAHTAR_T = DUR[1][0]                 # oda adlari anahtari: oda adlari ilk kez (an 2 satiri)


def altyazi(g, t):
    for t0, t1, m in ALT:
        if t0 <= t < t1:
            a = min(1, (t - t0) / .3, (t1 - t) / .3)
            d = ImageDraw.Draw(g, "RGBA")
            sat = K.sar(d, m, Fn["alt"], 1840)
            h = len(sat) * 42 + 22
            y0 = 1068 - h
            gen = max(d.textlength(s, font=Fn["alt"]) for s in sat) + 44
            d.rounded_rectangle([W / 2 - gen / 2, y0, W / 2 + gen / 2, y0 + h], 10, fill=(0, 0, 0, int(175 * a)))
            for i, s in enumerate(sat):
                d.text((W / 2, y0 + 10 + i * 42), s, font=Fn["alt"], fill=K.KAGIT + (int(255 * a),), anchor="ma")


_n = {}


def panel(ad, yerel):
    n = _n.setdefault(ad, len([f for f in os.listdir(os.path.join(KARE, ad)) if f.endswith(".jpg")]))
    i = min(n - 1, max(0, int(round(yerel * FPS))))
    return Image.open(os.path.join(KARE, ad, "%06d.jpg" % i)).convert("RGB"), i


def kart(t):
    g = Image.new("RGB", (W, H), K.ZEMIN)
    d = ImageDraw.Draw(g, "RGBA")
    cum = re.split(r"(?<=[.?])\s+", Y["kart"])
    y = 300
    for j, c in enumerate(cum):
        t0 = .5 + j * 2.8
        a = max(0, min(1, (t - t0) / .6, (KART - .2 - t) / .4))
        sat = K.sar(d, c, Fn["kart"], 1500)
        K.ortala(d, y, sat, Fn["kart"], K.KAGIT + (int(255 * a),), 1.3)
        y += len(sat) * 57 + 40
    return g


def sahne12(t):
    g = Image.new("RGB", (W, H), K.ZEMIN)
    yerel = t - KART
    for j, (ad, kosu, renk, etk) in enumerate(KOSU):
        x0 = j * PW
        p, fi = panel(ad, min(yerel, SURE3))
        g.paste(p, (x0, PY))
        d = ImageDraw.Draw(g, "RGBA")
        d.rectangle([x0, 10, x0 + PW, PY - 6], fill=K.ZEMIN)
        d.ellipse([x0 + 28, 30, x0 + 44, 46], fill=renk)
        d.text((x0 + 56, 22), "%s · %s" % (etk, kosu["vaka"]), font=Fn["etk"], fill=K.KAGIT)
        P = PLAN[ad]
        # hizli oynatma etiketi
        if any(a <= yerel < b for a, b in P["hiz"]):
            K.hap(d, (x0 + PW - 24 - d.textlength(Y["hizli"], font=Fn["etk2"]), PY + 18), Y["hizli"], Fn["etk2"], K.KAGIT, kenar=(110, 118, 134))
        # olay etiketleri (yalniz T1, kayittaki olay aninda)
        ol = [o for o in P["olaylar"] if o["t"] is not None]
        for k_, o in enumerate(ol):
            son = min(o["t"] + 1.8, ol[k_ + 1]["t"] if k_ + 1 < len(ol) else 1e9)
            if o["t"] <= yerel < son:
                K.hap(d, (x0 + 24, PY + 18), "T1 · " + Y["etiket"][o["etiket"]], Fn["etk2"], K.KAGIT, kenar=renk)
        # duruslar
        for i, du in enumerate(P["duruslar"]):
            X = du["konum"].split(".")[-1]
            if du["t0"] <= yerel < du["t1"] or (i == 2 and yerel >= du["t0"]):
                b = min(1, (yerel - du["t0"]) / .4)
                e = P["ekran"].get(str(min(fi, max(int(k) for k in P["ekran"] if P["ekran"][k]["an"] == i))))
                if e is None:
                    e = P["ekran"][min(P["ekran"], key=lambda k: abs(int(k) - fi))]
                if e.get("uc"):
                    (ax, ay), (bx, by) = e["t1"], e["uc"]
                    a2 = (x0 + ax, PY + ay); b2 = (x0 + bx, PY + by)
                    K.kesik(d, a2, b2, K.KIRMIZI + (int(255 * b),))
                    cx, cy = a2[0] + (b2[0] - a2[0]) * .6, a2[1] + (b2[1] - a2[1]) * .6
                    d.line([(cx - 15, cy - 15), (cx + 15, cy + 15)], fill=K.KIRMIZI + (int(255 * b),), width=7)
                    d.line([(cx - 15, cy + 15), (cx + 15, cy - 15)], fill=K.KIRMIZI + (int(255 * b),), width=7)
                if b > .5:
                    K.hap(d, (x0 + PW / 2, PY + 520), Y["levha_kapali"].replace("X", X), Fn["kucuk"], K.KAGIT, kenar=K.KIRMIZI, anchor="ma")
            elif i < 2 and du["t1"] <= yerel < du["t1"] + 1.8:
                K.hap(d, (x0 + PW / 2, PY + 520), Y["levha_devam"], Fn["kucuk"], K.KAGIT, kenar=(125, 220, 154), anchor="ma")
        d.line([(PW, PY), (PW, PY + PH)], fill=(0, 0, 0), width=4)
        # sahne 1 kucuk yazilari
        if yerel < DUR[0][0] - KART:
            a = max(0, min(1, (DUR[0][0] - KART - yerel) / .4, yerel / .6))
            d.text((x0 + PW / 2, PY + PH + 16), Y["s1_sol"] if j == 0 else Y["s1_sag"], font=Fn["kucuk"], fill=K.SOLUK + (int(255 * a),), anchor="ma")
        # sayac: satir r, durus r'de dolar
        for r, an in enumerate(kosu["anlar"]):
            ts = DUR[r][0] + .5
            if t < ts:
                break
            y = PY + PH + 14 + r * 80
            d.text((x0 + 60, y), "step %d · plan: go %s" % (an["adim"], an["X"]), font=Fn["satir"], fill=K.SOLUK)
            for i, k in enumerate(an["kutu"]):
                if t < ts + i * KUTU_D:
                    break
                bx, by = x0 + 60 + i * 84, y + 30
                yazi = K.eylem_yazi(k)
                if k["yine_X"]:
                    d.rounded_rectangle([bx, by, bx + 78, by + 40], 6, fill=renk)
                    d.text((bx + 39, by + 20), yazi, font=K.sigdir(d, yazi), fill=(20, 18, 14), anchor="mm")
                else:
                    d.rounded_rectangle([bx, by, bx + 78, by + 40], 6, outline=(110, 118, 134), width=2)
                    d.text((bx + 39, by + 20), yazi, font=K.sigdir(d, yazi), fill=K.SOLUK, anchor="mm")
            if t >= ts + 10 * KUTU_D:
                d.text((x0 + PW - 60, y), "%d / 10" % an["yine_X"], font=Fn["satir"], fill=K.KAGIT, anchor="ra")
        if t >= E3 + .2:
            d.text((x0 + PW / 2, PY + PH + 258), M["toplam_yazi"][ad], font=Fn["top"], fill=K.KAGIT, anchor="ma")
    d = ImageDraw.Draw(g, "RGBA")
    if NOT[0] <= t < NOT[1]:
        a = min(1, (t - NOT[0]) / .5, (NOT[1] - t) / .4)
        K.ortala(d, PY + PH + 70, K.sar(d, Y["s1_not"], Fn["kucuk"], 1500), Fn["kucuk"], K.KAGIT + (int(255 * a),))
    if DUR[0][0] + .3 <= t < DUR[0][1] + .6:
        a = min(1, (t - DUR[0][0] - .3) / .4, (DUR[0][1] + .6 - t) / .4)
        d.text((W / 2, PY + PH - 34), "filled box = the answer still keeps the original plan", font=Fn["kucuk"], fill=K.KAGIT + (int(255 * a),), anchor="ma",
               stroke_width=3, stroke_fill=(0, 0, 0, int(255 * a)))
    if SERIT[0] <= t < SERIT[1] + .6:
        K.serit(g, min(1, (t - SERIT[0]) / .6, (SERIT[1] + .6 - t) / .6))
    if ANAHTAR_T <= t < S3:
        d = ImageDraw.Draw(g, "RGBA")
        a = min(1, (t - ANAHTAR_T) / .5)
        d.text((W / 2, PY + PH - 34), Y["anahtar"], font=Fn["kucuk"], fill=K.KAGIT + (int(255 * a),), anchor="ma", stroke_width=3, stroke_fill=(0, 0, 0, int(255 * a)))
    return g


def sahne3(t):
    if t < SEKIL2:
        sw, sh = K._s1
        z = .02 * (t - S3) / (SEKIL2 - S3)
        x0, y1 = sw * .525, sh * .88
        return K.sekil(K.S1P, (x0 + (sw - x0) * z, sh * z, sw * (1 - z / 2), y1 * (1 - z / 2)))
    u = (t - SEKIL2) / (KAPANIS - SEKIL2)
    sw, sh = Image.open(K.S2P).size
    z = .015 * u
    return K.sekil(K.S2P, (sw * z, sh * z, sw * (1 - z), sh * (1 - z)))


def kapanis(t):
    g = Image.new("RGB", (W, H), K.ZEMIN)
    d = ImageDraw.Draw(g, "RGBA")
    if t < BASLIK:
        a = max(0, min(1, (t - KAPANIS) / .6, (BASLIK - t) / .4))
        K.ortala(d, 430, K.sar(d, Y["sowhat"], Fn["sowhat"], 1500), Fn["sowhat"], K.KAGIT + (int(255 * a),), 1.3)
        return g
    a = lambda t0: int(255 * max(0, min(1, (t - t0) / .8)))
    sat = K.sar(d, Y["k_baslik"], Fn["baslik"], 1640)
    K.ortala(d, 300, sat, Fn["baslik"], K.KAGIT + (a(BASLIK),), 1.22)
    d.text((W / 2, 300 + len(sat) * 71 + 50), Y["k_alt"], font=Fn["kalt"], fill=K.ALTIN + (a(BASLIK + .6),), anchor="ma")
    K.ortala(d, 820, K.sar(d, Y["k_dip"], Fn["dip"], 1400), Fn["dip"], K.SOLUK + (a(BASLIK + 1.6),))
    return g


def cerceve(t):
    if t < KART:
        g = kart(t)
    elif t < S3:
        g = sahne12(t)
    elif t < KAPANIS:
        g = sahne3(t)
    else:
        g = kapanis(t)
    for ts, once in ((KART, kart), (S3, sahne12), (SEKIL2, sahne3), (KAPANIS, sahne3)):
        if ts <= t < ts + GECIS:
            g = Image.blend(once(ts - 1e-3), g, (t - ts) / GECIS)
    altyazi(g, t)
    kar = min(1, t / .6, (SON - t) / .8)
    if kar < 1:
        g = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), g, max(0, kar))
    return g


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    A = sys.argv
    print("KART", KART, "E3", round(E3, 2), "S3", round(S3, 2), "SEKIL2", round(SEKIL2, 2), "KAPANIS", round(KAPANIS, 2), "SON", round(SON, 2), "duruslar", [(round(a, 2), round(b, 2)) for a, b in DUR])
    if A[1] == "kare":
        os.makedirs(A[2], exist_ok=True)
        for x in A[3:]:
            cerceve(float(x)).save(os.path.join(A[2], "t%06.2f.png" % float(x)))
        print("kare", len(A) - 3)
    elif A[1] == "tam":
        n = int(SON * FPS)
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", str(FPS), "-i", "-",
                               "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-tune", "animation", "-pix_fmt", "yuv420p", "-movflags", "+faststart", A[2]], stdin=subprocess.PIPE)
        for i in range(n):
            ff.stdin.write(cerceve(i / FPS).tobytes())
            if i % 600 == 0:
                print(i, "/", n, flush=True)
        ff.stdin.close(); ff.wait()
        print("tamam", A[2], n, "kare", round(os.path.getsize(A[2]) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
