# coding: utf-8
"""AKTARIM ANI SURUCUSU · 11 Kas · Hikayeci · tasarim: Desktop/sprint/epistemics/KOSU_SIRASI_11kas.md "Aktarim ani testi" (danisman)
Donuk dosyalara dokunmaz (kosu_ikiz deseni): dunya.py yerine aktarim/dunya_aktarim.py yalniz bu surecte "dunya" adiyla yuklenir
(sys.modules), kosu_model/kartlar/suruculer aynen calisir. Dunya kopyasinin ve kaynak dunya.py'nin ozeti her acilista denetlenir.
Dagitim: donuk U1 dagitimi (K.dagitim_kosu2(t)["U1"]) + takas: --yerlesim U_T1 (AU) / G_T1 (AG) (danisman KARARI, bkz. ONKAYIT).
Puanli: yerel tasiyici + duyuru acik + tohum 31-45 tam + ONAYLI ayar. ONAYLI bos iken yerel kosu REDDEDILIR (karar danismanda).
Ornek:
  python -I aktarim/kosu_aktarim.py --duyuru acik --tasiyici sahte --tohumlar 31-33 --cikti <karalama>
  python -I aktarim/kosu_aktarim.py --duyuru acik --yer cikis_odasi --yerlesim U_T1 --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 31-45 --cikti kosular/v4_aktarim_AU_11kas
  python -I aktarim/kosu_aktarim.py --duyuru acik --yer cikis_odasi --yerlesim G_T1 --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 31-45 --cikti kosular/v4_aktarim_AG_11kas"""
import argparse
import glob
import hashlib
import json
import os
import sys

AK = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(AK)
sys.path.insert(0, KOK); sys.path.insert(0, AK)
DUNYA_KAYNAK_OZET = "a4ef8bd8ca6ef462b0ec9aed39e536f8ff3e3c1c6efb84d2127dd8e5ae96a0f5"   # dunya.py (kopyanin kaynagi, donuk)
DUNYA_AKTARIM_OZET = "b965ef2ec97b171fac273a654ad82013d3a9589799fe3433371e16285e232214"                                                                # aktarim/dunya_aktarim.py (onkayitla kilitlenir)


def _ozet(yol):
    with open(yol, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if _ozet(os.path.join(KOK, "dunya.py")) != DUNYA_KAYNAK_OZET:
    raise SystemExit("dunya.py ozeti degisti")
if DUNYA_AKTARIM_OZET != "DOLDUR" and _ozet(os.path.join(AK, "dunya_aktarim.py")) != DUNYA_AKTARIM_OZET:
    raise SystemExit("dunya_aktarim.py ozeti kilitli degerle ayni degil")
import dunya_aktarim as DA  # noqa: E402
sys.modules["dunya"] = DA
import kartlar as K  # noqa: E402
import kosu_model as M  # noqa: E402
import suruculer as S  # noqa: E402
assert M.kos is DA.kos

PUANLI = set(range(31, 46))
ONAYLI = {"yer": "cikis_odasi", "yerlesim": ("U_T1", "G_T1")}   # danisman KARARI 11 Kas 10:55 (S2 takas + cikis_odasi; ONKAYIT_aktarim_11kas.md)
ESLESME = "ayni tohum, ayni baslangic"
ETIKET = {"donuk": "A", "U_T1": "AU", "G_T1": "AG"}
_dagitim, _sohbet = K.dagitim_kosu2, S.Ollama.sohbet
CAGRI, YERLESIM, DEGISEN = [], None, {}


def dagitim_aktarim(tohum):
    d = dict(dict(_dagitim(tohum))["U1"])
    sira = next(a for a, kod in d.items() if kod == "U1")
    if YERLESIM == "U_T1" and sira != "T1":
        d[sira], d["T1"] = d["T1"], "U1"
    elif YERLESIM == "G_T1" and sira == "T1":
        d["T1"], d["T2"] = d["T2"], "U1"
    DEGISEN[tohum] = {"uyuyan_yeri_donuk": sira, "uyuyan_yeri": next(a for a, kod in d.items() if kod == "U1"), "dagitim": d}
    return [(ETIKET[YERLESIM], d)]


def sohbet_olc(self, mesajlar, tohum):
    r = _sohbet(self, mesajlar, tohum)
    CAGRI.append({"n": len(mesajlar), "girdi": r[1], "cikti": r[2], "karakter": sum(len(m["content"]) for m in mesajlar)})
    return r


def ortam(tasiyici):
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


def bagla(duyuru, yer, yerlesim):
    """yeniden oynatma da bunu cagirir (kayittaki ayarla)"""
    global YERLESIM
    DA.DUYURU_ACIK, DA.DUYURU_YER, YERLESIM = duyuru, yer, yerlesim
    K.dagitim_kosu2, S.Ollama.sohbet = dagitim_aktarim, sohbet_olc


def main():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--duyuru", choices=["acik", "kapali"], required=True)
    p.add_argument("--yer", choices=["zarf_al", "k2_varis", "cikis_odasi"], default="zarf_al")
    p.add_argument("--yerlesim", choices=list(ETIKET), default="donuk")
    p.add_argument("--tasiyici", required=True)
    p.add_argument("--tohumlar", required=True)
    p.add_argument("--cikti", required=True)
    a, kalan = p.parse_known_args()
    if any(x.startswith(("--tekrar", "--kosullar", "--kodon", "--kosu")) for x in kalan):
        raise SystemExit("tekrar/kosullar/kodon/kosu donuk kosuyla ayni kalir; verilemez")
    tohumlar = M.tohum_listesi(a.tohumlar)
    if not set(tohumlar) <= PUANLI:
        raise SystemExit("tohum disi: %s" % sorted(set(tohumlar) - PUANLI))
    if a.tasiyici == "yerel":
        if ONAYLI is None:
            raise SystemExit("KARAR BEKLIYOR: yer/yerlesim danismanda; yerel kosu yok")
        if a.duyuru != "acik" or sorted(tohumlar) != sorted(PUANLI) or a.yer != ONAYLI["yer"] or a.yerlesim not in ONAYLI["yerlesim"]:
            raise SystemExit("yerel kosu yalniz onayli ayar + tohum 31-45 tam (puanli)")
        if DUNYA_AKTARIM_OZET == "DOLDUR":
            raise SystemExit("dunya_aktarim ozeti kilitlenmedi")
    puanli = a.tasiyici == "yerel"
    if glob.glob(os.path.join(a.cikti, "*.jsonl")):
        raise SystemExit("cikti klasoru dolu: %s" % a.cikti)
    ortam0 = ortam(a.tasiyici)
    bagla(a.duyuru == "acik", a.yer, a.yerlesim)
    sys.argv = ["kosu_model.py", "--kosu", "2", "--kosullar", "O1_O2b", "--tasiyici", a.tasiyici, "--tohumlar", a.tohumlar,
                "--cikti", a.cikti] + kalan
    M.main()
    with open(os.path.join(a.cikti, "cagri_olcum.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for c in CAGRI:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(os.path.join(a.cikti, "kosu_aktarim_meta.json"), "w", encoding="utf-8") as f:
        json.dump({"puanli": puanli, "duyuru": a.duyuru, "yer": a.yer, "yerlesim": a.yerlesim, "eslesme": ESLESME,
                   "surucu_ozet": _ozet(os.path.abspath(__file__)), "dunya_aktarim_ozet": _ozet(os.path.join(AK, "dunya_aktarim.py")),
                   "dunya_kaynak_ozet": DUNYA_KAYNAK_OZET, "ortam_basta": ortam0, "ortam_sonda": ortam(a.tasiyici),
                   "parola": {str(t): DA.parola_uret(t) for t in tohumlar},
                   "degisen": {str(k): v for k, v in sorted(DEGISEN.items())},
                   "cagri": len(CAGRI)}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
