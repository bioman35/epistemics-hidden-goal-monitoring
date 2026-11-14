# coding: utf-8
"""IKIZ KART SURUCUSU · 11 Kas · Turan "kos dostum. puanli sayilsin dostum." (danisman penceresi) · plan: epistemik/ikiz_kart_plan_11kas.md §8
Donuk dosyalara dokunmaz (kosu_5c deseni): kosu_model.py, kartlar.py, dunya.py aynen calisir; K.oku ve K.dagitim_kosu2 yalniz bu surecte sarilir.
Kollar (her tohumda tek kosu, donuk U1 dagitimindan):
  I1 · G, U kiliginda : U1 yerinde kalir; ilk G tasiyicinin (T1..T3, U1'in yeri disinda ilk) kodu G4 olur (U1 karakter metni, tur bizim -> hedef satiri YOK)
  I2 · U, G kiliginda : U1'in yeri U5 olur (G3 karakter metni, tur ic_uyuyan -> hedef satiri VAR)
  K0 · taze taban     : donuk U1 dagitimi aynen, kart degismez (11 Kas sabah t16/t26 kontrolu puansiz; 11 Kas oglen Turan "Kos dostum":
                        K0 16-30 PUANLI taze taban, I1/I2 ile ayni oturum, ayni Ollama · eslesme dili "ayni tohum, ayni baslangic")
Puanli: K0, I1, I2, tohum 16-30 tam, yerel tasiyici. K0 kismi tohum (or. t16 belirlenim tekrari) puansiz. Model tohumu donuk kosularla ayni (tekrar 0).
Onceki surucu ozeti (K0 yalniz 16,26): 6ad0d39ed302cff59cc0498e7ec308a77222381e5d814e89cdc3b44323d3f323
Ornek:
  python -I kosu_ikiz.py --kol I1 --tasiyici sahte --tohumlar 16 --cikti kosular/v4_ikiz_sahte_I1
  python -I kosu_ikiz.py --kol I1 --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 16-30 --cikti kosular/v4_ikiz_I1_11kas"""
import argparse
import glob
import hashlib
import json
import os
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import kartlar as K  # noqa: E402
import kosu_model as M  # noqa: E402
import suruculer as S  # noqa: E402

KART_IKIZ = os.path.join(KOK, "kart", "ikiz_kartlar_11kas.md")
KART_IKIZ_OZET = "7d871571ff864c3363c152bd4d518451aef2e850f7cd943a95c487c2fa05958f"   # Turan okudu 11 Kas (danisman penceresinde birebir basildi)
KODLAR_IKIZ = {"G4", "U5"}
PUANLI = set(range(16, 31))
KONTROL = set(PUANLI)
ESLESME = "ayni tohum, ayni baslangic"
_oku, _dagitim, _sohbet = K.oku, K.dagitim_kosu2, S.Ollama.sohbet
CAGRI = []
KOL = None
DEGISEN = {}


def oku_ikiz(*a, **k):
    """donuk kartlar (ozet denetimli) + G4, U5 (ozet denetimli) · metinler donuk U1/G3 ile birebir olmali"""
    kartlar, oz = _oku(*a, **k)
    with open(KART_IKIZ, "rb") as f:
        ham = f.read()
    oi = hashlib.sha256(ham).hexdigest()
    if oi != KART_IKIZ_OZET:
        raise ValueError("ikiz kart ozeti %s, beklenen %s" % (oi, KART_IKIZ_OZET))
    yeni = {kod: {"ad": ad.strip(), "metin": metin.strip(), "tur": K.TUR[kod[0]]}
            for kod, ad, metin in K.KART_DESEN.findall(ham.decode("utf-8"))}
    if set(yeni) != KODLAR_IKIZ:
        raise ValueError("ikiz kart kodlari %s" % sorted(yeni))
    if yeni["G4"]["metin"] != kartlar["U1"]["metin"] or yeni["U5"]["metin"] != kartlar["G3"]["metin"]:
        raise ValueError("ikiz kart metni donuk U1/G3 ile birebir degil")
    return dict(kartlar, **yeni), oz


def dagitim_ikiz(tohum):
    """[(etiket, dagitim)] · tek satir · donuk U1 dagitimindan yalniz bir kart degisir"""
    d = dict(_dagitim(tohum))["U1"]
    sira = next(a for a, kod in d.items() if kod == "U1")
    if KOL == "I1":
        hedef = next(t for t in ("T1", "T2", "T3") if t != sira)
        DEGISEN[tohum] = {"yer": hedef, "eski": d[hedef], "yeni": "G4", "uyuyan_yeri": sira}
        return [("I1", dict(d, **{hedef: "G4"}))]
    if KOL == "I2":
        DEGISEN[tohum] = {"yer": sira, "eski": "U1", "yeni": "U5", "uyuyan_yeri": sira}
        return [("I2", dict(d, **{sira: "U5"}))]
    DEGISEN[tohum] = {"yer": None, "eski": None, "yeni": None, "uyuyan_yeri": sira}
    return [("K0", d)]


def sohbet_olc(self, mesajlar, tohum):
    r = _sohbet(self, mesajlar, tohum)
    CAGRI.append({"n": len(mesajlar), "girdi": r[1], "cikti": r[2], "karakter": sum(len(m["content"]) for m in mesajlar)})
    return r


def ortam(tasiyici):
    """gunler arasi fark icin kaynak adaylari: Ollama surumu, GPU surucu surumu (danisman sart 3)"""
    import subprocess
    import urllib.request
    o = {"tasiyici": tasiyici}
    try:
        o["ollama"] = json.loads(urllib.request.urlopen("http://127.0.0.1:11434/api/version", timeout=10).read())["version"]
    except Exception as e:
        o["ollama"] = "okunamadi: %s" % type(e).__name__
    try:
        o["gpu"] = subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
                                  capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e:
        o["gpu"] = "okunamadi: %s" % type(e).__name__
    return o


def bagla():
    K.oku, K.dagitim_kosu2, S.Ollama.sohbet = oku_ikiz, dagitim_ikiz, sohbet_olc


def main():
    global KOL
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--kol", choices=["I1", "I2", "K0"], required=True)
    p.add_argument("--tasiyici", required=True)
    p.add_argument("--tohumlar", required=True)
    p.add_argument("--cikti", required=True)
    a, kalan = p.parse_known_args()
    if any(x.startswith("--tekrar") or x.startswith("--kosullar") or x.startswith("--kodon") for x in kalan):
        raise SystemExit("tekrar/kosullar/kodon donuk kosuyla ayni kalir; verilemez")
    KOL = a.kol
    tohumlar = M.tohum_listesi(a.tohumlar)
    izinli = KONTROL if a.kol == "K0" else PUANLI
    if not set(tohumlar) <= izinli:
        raise SystemExit("%s kolunda tohum disi: %s" % (a.kol, sorted(set(tohumlar) - izinli)))
    puanli = a.tasiyici == "yerel" and sorted(tohumlar) == sorted(PUANLI)
    if a.tasiyici == "yerel" and a.kol != "K0" and not puanli:
        raise SystemExit("yerel tasiyicida I1/I2 yalniz tohum 16-30 tam (puanli)")
    if glob.glob(os.path.join(a.cikti, "*.jsonl")):
        raise SystemExit("cikti klasoru dolu: %s" % a.cikti)
    ortam0 = ortam(a.tasiyici)
    bagla()
    sys.argv = ["kosu_model.py", "--kosu", "2", "--kosullar", "O1_O2b", "--tasiyici", a.tasiyici, "--tohumlar", a.tohumlar,
                "--cikti", a.cikti] + kalan
    M.main()
    with open(os.path.join(a.cikti, "cagri_olcum.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for c in CAGRI:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(os.path.abspath(__file__), "rb") as f:
        surucu = hashlib.sha256(f.read()).hexdigest()
    with open(os.path.join(a.cikti, "kosu_ikiz_meta.json"), "w", encoding="utf-8") as f:
        json.dump({"kol": a.kol, "puanli": puanli, "eslesme": ESLESME, "kart_ikiz_ozet": KART_IKIZ_OZET, "surucu_ozet": surucu,
                   "ortam_basta": ortam0, "ortam_sonda": ortam(a.tasiyici),
                   "degisen": {str(k): v for k, v in sorted(DEGISEN.items())},
                   "cagri": len(CAGRI), "en_cok_girdi": max([c["girdi"] for c in CAGRI] or [0]),
                   "en_cok_karakter": max([c["karakter"] for c in CAGRI] or [0])}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
