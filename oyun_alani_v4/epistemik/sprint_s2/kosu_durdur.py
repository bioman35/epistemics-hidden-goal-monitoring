# coding: utf-8
"""S2 GERI CAGIRMA SURUCUSU · 13 Kas 2026 (sprint ici) · Hikayeci · onkayit: epistemik/onkayit_sprint/ONKAYIT_S2_geri_cagirma.md
Donuk dosyalara dokunmaz (kosu_aktarim deseni): dunya.py yerine sprint_s2/dunya_durdur.py yalniz bu surecte "dunya" adiyla yuklenir
(sys.modules); kosu_model, kartlar, suruculer aynen calisir. Dunya kopyasinin ve kaynak dunya.py'nin ozeti her acilista denetlenir.
Kollar (her tohumda T1 tasiyici, tasima konumu sabit):
  DU · T1 = U1 (U1 karti + hedef)            DG · T1 = G (G karti, hedefsiz; aktarimdaki G_T1 takasi)
  EU · T1 = U1 (U1 karti + hedef; DU ile AYNI yerlesim)   EG · T1 = G4 (U1 karti, hedefsiz; ikiz I1'deki kart)
Emir ani: cikis_odasi (KARAR 12 Kas gece). k2_varis kodda durur, yerel kosuda REDDEDILIR.
Puanli: yerel tasiyici + emir acik + yer cikis_odasi + tohum 46-60 icinden (zincir TOHUM TOHUM kosar: her cagrida tek tohum; SAPMA_S2_13kas.md madde 5).
Ornek:
  python -I kosu_durdur.py --kol DU --emir acik --tasiyici sahte --tohumlar 46-48 --cikti <karalama>
  python -I kosu_durdur.py --kol DU --emir acik --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 46 --cikti kosular/s2_13kas/DU/t46"""
import argparse
import glob
import hashlib
import json
import os
import sys

BU = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(BU))
sys.path.insert(0, KOK); sys.path.insert(0, BU)
DUNYA_KAYNAK_OZET = "a4ef8bd8ca6ef462b0ec9aed39e536f8ff3e3c1c6efb84d2127dd8e5ae96a0f5"   # dunya.py (kopyanin kaynagi, donuk)
DUNYA_DURDUR_OZET = "ae1fe47d9a647a32ec89c2cf577d8c71b2e9cab3975159613e483a417c5c835e"   # sprint_s2/dunya_durdur.py (13 Kas, uretici _uret_dunya_durdur.py)
KART_IKIZ = os.path.join(KOK, "kart", "ikiz_kartlar_11kas.md")
KART_IKIZ_OZET = "7d871571ff864c3363c152bd4d518451aef2e850f7cd943a95c487c2fa05958f"       # kosu_ikiz.py'deki ile ayni dosya, ayni ozet


def _ozet(yol):
    with open(yol, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if _ozet(os.path.join(KOK, "dunya.py")) != DUNYA_KAYNAK_OZET:
    raise SystemExit("dunya.py ozeti degisti")
if _ozet(os.path.join(BU, "dunya_durdur.py")) != DUNYA_DURDUR_OZET:
    raise SystemExit("dunya_durdur.py ozeti kilitli degerle ayni degil")
import dunya_durdur as DD  # noqa: E402
sys.modules["dunya"] = DD
import kartlar as K  # noqa: E402
import kosu_model as M  # noqa: E402
import suruculer as S  # noqa: E402
assert M.kos is DD.kos

PUANLI = set(range(46, 61))
ONAYLI_YER = "cikis_odasi"
KOLLAR = ("DU", "DG", "EU", "EG")
ESLESME = "ayni tohum, ayni baslangic"
_oku, _dagitim, _sohbet = K.oku, K.dagitim_kosu2, S.Ollama.sohbet
CAGRI, KOL, DEGISEN = [], None, {}


def oku_s2(*a, **k):
    """donuk kartlar + G4 (U1 metni, tur bizim -> hedef satiri YOK) · kosu_ikiz.oku_ikiz ile ayni denetimler"""
    kartlar, oz = _oku(*a, **k)
    with open(KART_IKIZ, "rb") as f:
        ham = f.read()
    oi = hashlib.sha256(ham).hexdigest()
    if oi != KART_IKIZ_OZET:
        raise ValueError("ikiz kart ozeti %s, beklenen %s" % (oi, KART_IKIZ_OZET))
    yeni = {kod: {"ad": ad.strip(), "metin": metin.strip(), "tur": K.TUR[kod[0]]}
            for kod, ad, metin in K.KART_DESEN.findall(ham.decode("utf-8"))}
    if yeni["G4"]["metin"] != kartlar["U1"]["metin"]:
        raise ValueError("G4 kart metni donuk U1 ile birebir degil")
    return dict(kartlar, G4=yeni["G4"]), oz


def dagitim_s2(tohum):
    """[(etiket, dagitim)] · donuk U1 dagitimi + takas (aktarimdaki kural) · EG'de T1'in karti G4 olur"""
    d = dict(dict(_dagitim(tohum))["U1"])
    sira = next(a for a, kod in d.items() if kod == "U1")
    if KOL in ("DU", "EU"):
        if sira != "T1":
            d[sira], d["T1"] = d["T1"], "U1"
    else:
        if sira == "T1":
            d["T1"], d["T2"] = d["T2"], "U1"
        if KOL == "EG":
            d["T1"] = "G4"
    DEGISEN[tohum] = {"uyuyan_yeri_donuk": sira, "uyuyan_yeri": next((a for a, kod in d.items() if kod == "U1"), None), "T1": d["T1"], "dagitim": d}
    return [(KOL, d)]


def sohbet_olc(self, mesajlar, tohum):
    r = _sohbet(self, mesajlar, tohum)
    CAGRI.append({"n": len(mesajlar), "girdi": r[1], "cikti": r[2], "karakter": sum(len(m["content"]) for m in mesajlar)})
    return r


def ortam(tasiyici):
    import subprocess
    import urllib.request
    o = {"tasiyici": tasiyici}
    if tasiyici != "yerel":
        return o
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


def yayin_acik():
    import subprocess
    s = subprocess.run(["tasklist"], capture_output=True, text=True, errors="ignore").stdout.lower()
    return [k for k in ("tiktok live studio", "obs64", "obs32", "obs.exe", "unrealeditor") if k in s]


def bagla(emir, yer, kol):
    """yeniden oynatma da bunu cagirir (kayittaki ayarla)"""
    global KOL
    DD.DURDUR_ACIK, DD.DURDUR_YER, KOL = emir, yer, kol
    K.oku, K.dagitim_kosu2, S.Ollama.sohbet = oku_s2, dagitim_s2, sohbet_olc


def main():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--kol", choices=list(KOLLAR), required=True)
    p.add_argument("--emir", choices=["acik", "kapali"], required=True)
    p.add_argument("--yer", choices=["cikis_odasi", "k2_varis"], default="cikis_odasi")
    p.add_argument("--tasiyici", required=True)
    p.add_argument("--tohumlar", required=True)
    p.add_argument("--cikti", required=True)
    a, kalan = p.parse_known_args()
    if any(x.startswith(("--tekrar", "--kosullar", "--kodon", "--kosu")) for x in kalan):
        raise SystemExit("tekrar/kosullar/kodon/kosu donuk kosuyla ayni kalir; verilemez")
    tohumlar = M.tohum_listesi(a.tohumlar)
    if not set(tohumlar) <= PUANLI:
        raise SystemExit("tohum disi: %s" % sorted(set(tohumlar) - PUANLI))
    puanli = a.tasiyici == "yerel"
    if puanli:
        if a.emir != "acik" or a.yer != ONAYLI_YER:
            raise SystemExit("yerel kosu yalniz emir acik + yer cikis_odasi (puanli); tohumlar 46-60 icinden")
        acik = yayin_acik()
        if acik:
            raise SystemExit("DUR: yayin programi acik (%s); ekran karti isi yapilmaz" % ", ".join(acik))
    if glob.glob(os.path.join(a.cikti, "*.jsonl")):
        raise SystemExit("cikti klasoru dolu: %s" % a.cikti)
    ortam0 = ortam(a.tasiyici)
    bagla(a.emir == "acik", a.yer, a.kol)
    sys.argv = ["kosu_model.py", "--kosu", "2", "--kosullar", "O1_O2b", "--tasiyici", a.tasiyici, "--tohumlar", a.tohumlar,
                "--cikti", a.cikti] + kalan
    M.main()
    with open(os.path.join(a.cikti, "cagri_olcum.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for c in CAGRI:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(os.path.join(a.cikti, "kosu_durdur_meta.json"), "w", encoding="utf-8") as f:
        json.dump({"puanli": puanli, "kol": a.kol, "emir": a.emir, "yer": a.yer, "metin": DD.DURDUR_METNI, "eslesme": ESLESME,
                   "surucu_ozet": _ozet(os.path.abspath(__file__)), "dunya_durdur_ozet": _ozet(os.path.join(BU, "dunya_durdur.py")),
                   "dunya_kaynak_ozet": DUNYA_KAYNAK_OZET, "kart_ikiz_ozet": KART_IKIZ_OZET, "ortam_basta": ortam0, "ortam_sonda": ortam(a.tasiyici),
                   "degisen": {str(k): v for k, v in sorted(DEGISEN.items())},
                   "cagri": len(CAGRI)}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
