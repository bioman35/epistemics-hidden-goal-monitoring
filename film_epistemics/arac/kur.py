# coding: utf-8
"""TESLIM VIDEOSU · kurgu ve bindirme (14 Kas). Islemci; ekran karti gerekmez.
Girdi: KARE/DU/*.jpg, KARE/EG/*.jpg (cek_ep.py tam), veri/ep_metin.json (ep_metin.py), sekil_sprint PNG'leri.
Yazilar ep_metin.json'dan; kodda yalniz kurgu etiketleri var (KAYNAK.md "Ek yazilar").
python -I kur.py kare CIKTI_KLASOR t1 t2 ...   secilen anlar, 1920x1080 png
python -I kur.py tam CIKTI.mp4                 1080p H.264, sessiz"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

KOK = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(os.path.dirname(KOK))
KARE = r"D:\calisma_cikti\film_epistemics\kare"
FPS, W, H = 30, 1920, 1080
PW, PH, PY = 960, 600, 70           # panel boyu ve ust kenari
F = r"C:\Windows\Fonts"
M = json.load(open(os.path.join(KOK, "veri", "ep_metin.json"), encoding="utf-8"))
Y, SAY = M["yazi"], M["sayac"]
DU, EG = SAY["kosu"]
ZEMIN, KAGIT, SOLUK, ALTIN, MAVI, KIRMIZI = (7, 11, 20), (243, 234, 215), (170, 178, 194), (232, 195, 122), (88, 180, 255), (255, 82, 64)


def yt(ad, boy):
    return ImageFont.truetype(os.path.join(F, ad), boy)


Fn = {"alt": yt("segoeui.ttf", 33), "kucuk": yt("segoeui.ttf", 24), "etk": yt("segoeuib.ttf", 26), "kutu": yt("segoeuib.ttf", 19), "satir": yt("segoeui.ttf", 21),
      "top": yt("segoeuib.ttf", 27), "baslik": yt("georgiab.ttf", 58), "kalt": yt("segoeuib.ttf", 28), "dip": yt("segoeui.ttf", 21), "eksen": yt("segoeui.ttf", 20)}

# --- zaman cizelgesi (sn); sahne 1-2 3B kareleri 0-27.5, sonra son kare
T_3B = 27.5
ALT = [(0.8, 8.4, Y["s1_a1"]), (8.8, 15.2, Y["s1_a2"]), (21.4, 27.4, Y["s2_a1"]), (28.2, 34.0, Y["s2_a2"]),
       (50.6, 57.0, Y["s2_a3"]), (57.4, 66.0, Y["s2_a4"]), (67.0, 82.0, Y["s3_a1"]), (82.8, 89.4, Y["s3_a2"]), (89.8, 96.0, Y["s3_a3"])]
SAYAC0, SATIR_D, KUTU_D = 34.4, 5.3, .38
TOPLAM_T = SAYAC0 + 3 * SATIR_D
SERIT = (57.4, 66.0)
ANAHTAR = "Room names from the game: ODA = room, CIKIS = exit, K1 = gate 1."   # ek yazi, kurgu (danisman 14 Kas, v3)
ANAHTAR_T = SAYAC0 + SATIR_D           # ikinci sayac satiri: oda adlari ilk kez gorunur
S3 = 66.0
SEKIL2 = 82.0
KAPANIS = 96.0
SON = 107.0
GECIS = .6


def sar(d, metin, font, gen):
    s, sat = "", []
    for k in metin.split():
        a = (s + " " + k).strip()
        if d.textlength(a, font=font) <= gen:
            s = a
        else:
            sat.append(s); s = k
    if s:
        sat.append(s)
    return sat


def ortala(d, y, satirlar, font, renk, ara=1.28):
    h = font.size * ara
    for i, s in enumerate(satirlar):
        d.text((W / 2, y + i * h), s, font=font, fill=renk, anchor="ma")


def altyazi(g, t):
    for t0, t1, m in ALT:
        if t0 <= t < t1:
            a = min(1, (t - t0) / .3, (t1 - t) / .3)
            d = ImageDraw.Draw(g, "RGBA")
            sat = sar(d, m, Fn["alt"], 1840)
            h = len(sat) * 42 + 22
            y0 = 1068 - h
            gen = max(d.textlength(s, font=Fn["alt"]) for s in sat) + 44
            d.rounded_rectangle([W / 2 - gen / 2, y0, W / 2 + gen / 2, y0 + h], 10, fill=(0, 0, 0, int(175 * a)))
            for i, s in enumerate(sat):
                d.text((W / 2, y0 + 10 + i * 42), s, font=Fn["alt"], fill=KAGIT + (int(255 * a),), anchor="ma")


_kare = {}


def panel(ad, t):
    n = len(os.listdir(os.path.join(KARE, ad))) if ad not in _kare else _kare[ad]
    _kare[ad] = n
    i = min(n - 1, int(round(t * FPS)))
    return Image.open(os.path.join(KARE, ad, "%06d.jpg" % i)).convert("RGB")


def hap(d, xy, metin, font, renk, kenar=None, dolgu=(7, 11, 20, 215), anchor="la"):
    x, y = xy
    w = d.textlength(metin, font=font)
    if anchor == "ma":
        x -= w / 2
    d.rounded_rectangle([x - 12, y - 6, x + w + 12, y + font.size + 10], 9, fill=dolgu, outline=kenar, width=2 if kenar else 0)
    d.text((x, y), metin, font=font, fill=renk)


def kesik(d, a, b, renk, gen=4, parca=14):
    import math
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0); n = int(L // parca)
    for i in range(0, n, 2):
        p, q = i / n, min(1, (i + 1) / n)
        d.line([(x0 + (x1 - x0) * p, y0 + (y1 - y0) * p), (x0 + (x1 - x0) * q, y0 + (y1 - y0) * q)], fill=renk, width=gen)


_kutuF = {b: yt("segoeuib.ttf", b) for b in (19, 17, 15, 14)}


def sigdir(d, m):
    """kutu yazisi 70 piksele sigsin (14 Kas denetim: "go ODA3", "go CIKIS" tasiyordu)"""
    for b in (19, 17, 15, 14):
        if d.textlength(m, font=_kutuF[b]) <= 70:
            return _kutuF[b]
    return _kutuF[14]


def eylem_yazi(k):
    e = k["eylem"]
    return ("go " + k["hedef"]) if e == "git" and k["hedef"] not in (None, "None") else {"goster": "show", "bekle": "wait"}.get(e, e)


def sahne12(t):
    g = Image.new("RGB", (W, H), ZEMIN)
    for j, (ad, kosu, renk, etk) in enumerate((("DU", DU, ALTIN, "SLEEPER RUN"), ("EG", EG, MAVI, "CONTROL RUN"))):
        x0 = j * PW
        p = panel(ad, min(t, T_3B))
        g.paste(p, (x0, PY))
        d = ImageDraw.Draw(g, "RGBA")
        d.rectangle([x0, 10, x0 + PW, PY - 6], fill=ZEMIN)
        d.ellipse([x0 + 28, 30, x0 + 44, 46], fill=renk)
        d.text((x0 + 56, 22), "%s · %s" % (etk, kosu["vaka"]), font=Fn["etk"], fill=KAGIT)
        if t >= T_3B:
            # cataldaki yol: K1 kapisi kararir, kesik cizgi, carpi, levha (oyun ici olay degil)
            a = min(1, (t - T_3B) / .6)
            d.text((x0 + 676, PY + 40), "K1", font=Fn["etk"], fill=KAGIT + (int(255 * a),))
            if t >= 28.0:
                b = min(1, (t - 28.0) / .6)
                d.polygon([(x0 + 596, PY + 20), (x0 + 800, PY + 20), (x0 + 800, PY + 245), (x0 + 596, PY + 245)], fill=(0, 0, 0, int(150 * b)))
                kesik(d, (x0 + 560, PY + 240), (x0 + 668, PY + 168), KIRMIZI + (int(255 * b),))
                cx, cy = x0 + 616, PY + 204
                d.line([(cx - 16, cy - 16), (cx + 16, cy + 16)], fill=KIRMIZI + (int(255 * b),), width=7)
                d.line([(cx - 16, cy + 16), (cx + 16, cy - 16)], fill=KIRMIZI + (int(255 * b),), width=7)
                if b > .5:
                    hap(d, (x0 + PW / 2, PY + 520), "path to K1 removed · re-ask only, not in the game", Fn["kucuk"], KAGIT, kenar=KIRMIZI, anchor="ma")
        d.line([(PW, PY), (PW, PY + PH)], fill=(0, 0, 0), width=4)
        # sahne 1 kucuk yazilari
        if t < SAYAC0 - .4:
            a = max(0, min(1, (SAYAC0 - .4 - t) / .4, t / .6))
            d.text((x0 + PW / 2, PY + PH + 16), Y["s1_sol"] if j == 0 else Y["s1_sag"], font=Fn["kucuk"], fill=SOLUK + (int(255 * a),), anchor="ma")
        # sayac
        if t >= SAYAC0:
            for r, an in enumerate(kosu["anlar"]):
                ts = SAYAC0 + r * SATIR_D
                if t < ts:
                    break
                y = PY + PH + 14 + r * 80
                d.text((x0 + 60, y), "step %d · plan: go %s" % (an["adim"], an["X"]), font=Fn["satir"], fill=SOLUK)
                for i, k in enumerate(an["kutu"]):
                    if t < ts + .3 + i * KUTU_D:
                        break
                    bx, by = x0 + 60 + i * 84, y + 30
                    if k["yine_X"]:
                        d.rounded_rectangle([bx, by, bx + 78, by + 40], 6, fill=renk)
                        d.text((bx + 39, by + 20), eylem_yazi(k), font=sigdir(d, eylem_yazi(k)), fill=(20, 18, 14), anchor="mm")
                    else:
                        d.rounded_rectangle([bx, by, bx + 78, by + 40], 6, outline=(110, 118, 134), width=2)
                        d.text((bx + 39, by + 20), eylem_yazi(k), font=sigdir(d, eylem_yazi(k)), fill=SOLUK, anchor="mm")
                if t >= ts + .3 + 10 * KUTU_D:
                    d.text((x0 + PW - 60, y), "%d / 10" % an["yine_X"], font=Fn["satir"], fill=KAGIT, anchor="ra")
            if t >= TOPLAM_T:
                d.text((x0 + PW / 2, PY + PH + 258), M["toplam_yazi"][ad], font=Fn["top"], fill=KAGIT, anchor="ma")
    d = ImageDraw.Draw(g, "RGBA")
    if SAYAC0 <= t < ANAHTAR_T - .2:   # v3: dolma aciklamasi oda adlari gorununce yerini anahtara birakir
        a = min(1, (t - SAYAC0) / .5, (ANAHTAR_T - .2 - t) / .4)
        d.text((W / 2, PY + PH - 34), "filled box = the answer still keeps the original plan", font=Fn["kucuk"], fill=KAGIT + (int(255 * a),), anchor="ma",
               stroke_width=3, stroke_fill=(0, 0, 0, int(255 * a)))
    if 15.0 <= t < SAYAC0 - .4:
        a = min(1, (t - 15) / .5, (SAYAC0 - .4 - t) / .4)
        ortala(d, PY + PH + 70, sar(d, Y["s1_not"], Fn["kucuk"], 1500), Fn["kucuk"], KAGIT + (int(255 * a),))
    if SERIT[0] <= t < SERIT[1] + .6:
        serit(g, min(1, (t - SERIT[0]) / .6, (SERIT[1] + .6 - t) / .6))
    if ANAHTAR_T <= t < S3:   # v3 (danisman 14 Kas, secenek 3): oda adlari anahtari, ek yazi (kurgu); seritten sonra cizilir, ustte kalir
        d = ImageDraw.Draw(g, "RGBA")
        a = min(1, (t - ANAHTAR_T) / .5)
        d.text((W / 2, PY + PH - 34), ANAHTAR, font=Fn["kucuk"], fill=KAGIT + (int(255 * a),), anchor="ma", stroke_width=3, stroke_fill=(0, 0, 0, int(255 * a)))
    return g


def serit(g, a):
    d = ImageDraw.Draw(g, "RGBA")
    d.rectangle([0, PY, W, PY + PH], fill=(7, 11, 20, int(232 * a)))
    x0, x1 = 300, 1620
    X = lambda v: x0 + (x1 - x0) * v
    yU, yG = PY + 210, PY + 360
    c = lambda r: tuple(r) + (int(255 * a),)
    for v in (0, .25, .5, .75, 1):
        d.line([(X(v), yU - 70), (X(v), yG + 60)], fill=(255, 255, 255, int(28 * a)), width=1)
        d.text((X(v), yG + 74), "%.2f" % v, font=Fn["eksen"], fill=c(SOLUK), anchor="ma")
    d.line([(x0, yG + 62), (x1, yG + 62)], fill=c((110, 118, 134)), width=2)
    d.text((W / 2, yG + 112), "persistence (share of re-asks that keep the plan)", font=Fn["eksen"], fill=c(SOLUK), anchor="ma")
    for yy, t_, renk, ad, sec in ((yU, "U", ALTIN, "sleeper (%d)", DU["vaka"]), (yG, "G", MAVI, "control (%d)", EG["vaka"])):
        noktalar = SAY["serit"][t_]
        d.text((x0 - 30, yy - 14), ad % len(noktalar), font=Fn["etk"], fill=c(KAGIT), anchor="ra")
        yigin = {}
        for r in noktalar:
            k = round(r["israr"], 3); n = yigin.get(k, 0); yigin[k] = n + 1
            cx, cy = X(r["israr"]), yy - n * 24 + (len([q for q in noktalar if round(q["israr"], 3) == k]) - 1) * 12
            d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=c(renk))
            if r["vaka"] == sec:
                d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], outline=c(KAGIT), width=3)
                d.text((cx, cy - 46), sec, font=Fn["eksen"], fill=c(KAGIT), anchor="ma")   # 14 Kas denetim: etiket noktalarin ustune biniyordu


def sekil(yol, kutu, olcek=1.0):
    """kutu: kaynak goruntuden kesilecek (x0, y0, x1, y1), ekrana sigdirilir"""
    im = Image.open(yol).convert("RGB")
    k = im.crop(tuple(int(v) for v in kutu))
    gx, gy = 1860, 900
    s = min(gx / k.width, gy / k.height) * olcek
    k = k.resize((int(k.width * s), int(k.height * s)), Image.LANCZOS)
    g = Image.new("RGB", (W, H), ZEMIN)
    g.paste(k, ((W - k.width) // 2, 30 + (gy - k.height) // 2))
    return g


S1P = os.path.join(SP, "epistemics", "sekil_sprint", "sekil1_auc.png")
S2P = os.path.join(SP, "epistemics", "sekil_sprint", "sekil2_hedef_anma.png")
_s1 = Image.open(S1P).size


def sahne3(t):
    if t < SEKIL2:
        sw, sh = _s1
        u = min(1, max(0, (t - 73.0) / 2.0)); u = u * u * (3 - 2 * u)
        sag = (sw * .525, 0, sw, sh * .88)   # 14 Kas denetim: .48 sol panelin sayilarini, tam boy alttaki kesik dipnotu aliyordu   # 14 Kas denetim: .48 sol panelin sayilarini aliyordu
        kutu = tuple(sag[i] + ((0, 0, sw, sh)[i] - sag[i]) * u for i in range(4))
        return sekil(S1P, kutu)
    u = (t - SEKIL2) / (KAPANIS - SEKIL2)
    sw, sh = Image.open(S2P).size
    z = .015 * u
    return sekil(S2P, (sw * z, sh * z, sw * (1 - z), sh * (1 - z)))


def kapanis(t):
    g = Image.new("RGB", (W, H), ZEMIN)
    d = ImageDraw.Draw(g, "RGBA")
    a = lambda t0: int(255 * max(0, min(1, (t - t0) / .8)))
    sat = sar(d, Y["k_baslik"], Fn["baslik"], 1640)
    ortala(d, 300, sat, Fn["baslik"], KAGIT + (a(KAPANIS),), 1.22)
    d.text((W / 2, 300 + len(sat) * 71 + 50), Y["k_alt"], font=Fn["kalt"], fill=ALTIN + (a(KAPANIS + .6),), anchor="ma")
    ortala(d, 820, sar(d, Y["k_dip"], Fn["dip"], 1400), Fn["dip"], SOLUK + (a(KAPANIS + 1.6),))
    return g


def cerceve(t):
    if t < S3:
        g = sahne12(t)
    elif t < KAPANIS:
        g = sahne3(t)
    else:
        g = kapanis(t)
    # gecisler: sahne 2 -> 3, sekil 1 -> 2, sekil -> kapanis
    for ts, once in ((S3, sahne12), (SEKIL2, sahne3), (KAPANIS, sahne3)):
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
