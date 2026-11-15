# coding: utf-8
"""KOD / VERI PAKETI (15 Kas 2026, Hikayeci; danisman IS EMRI 7 madde 5). YAYINLAMAZ: push, yukleme yok; yalniz yerel zip.
Iki arsiv (D diskine; C dolu): ana paket (kod, onkayit, sapma, olcum, sekil, README, ekler, sprint oncesi dunya ve kosucu) ve ham kayit paketi.
Her arsivde SHA256SUMS.txt. Pakete giren her dosyada (anlik goruntu zip'inin ici dahil) gizli anahtar ve kisisel veri taramasi; bulunan DEGERLER yazilmaz.
Calistir: python -I epistemics/rapor_ekleri/paket.py   -> D:/calisma_cikti/epistemics_paket/*.zip ve epistemics/rapor_ekleri/PAKET.md"""
import fnmatch
import hashlib
import io
import os
import re
import sys
import time
import zipfile

KOK = os.path.dirname(os.path.abspath(__file__))
SP = os.path.normpath(os.path.join(KOK, "..", ".."))
CIK = r"D:\calisma_cikti\epistemics_paket"
EP = "oyun_alani_v4/epistemik"
DISLA = ["*/__pycache__/*", "*.pyc", "*/karalama/*", "*/karalama2/*", "*/karalama2_oynat/*", "*/_etek_tmp/*"]
HAM_KALIP = [EP + "/sprint_s1/kosu_397b_s1_13kas/*", EP + "/sprint_s2/kosular/*", EP + "/sprint_s2/kosular_oynat/*", EP + "/sprint_s3/kosular/*",
             EP + "/sprint_s3/catal_s3_14kas.jsonl", EP + "/sprint_s2/celiski_s2_13kas.jsonl", EP + "/sprint_s4/cagri_s4_*.jsonl", EP + "/sprint_s5/cagri_s5_*.jsonl"]
ANA_KOK = [  # (klasor ya da dosya, ozyineli)
    ("epistemics/README.md", 0), ("epistemics/DONDURMA_12KAS.sha256", 0), ("epistemics/DONDURMA_12KAS.tsv", 0), ("epistemics/DONDURMA_12KAS_kod_sonuc.zip", 0),
    ("epistemics/rapor_ekleri", 1), ("epistemics/sekil_sprint", 1),
    ("oyun_alani_v4", "py"), ("oyun_alani_v4", "sha256"), ("oyun_alani_v4/aktarim", 1),
    (EP + "/onkayit_sprint", 1), (EP + "/sprint_s1", 1), (EP + "/sprint_s2", 1), (EP + "/sprint_s3", 1), (EP + "/sprint_s4", 1), (EP + "/sprint_s5", 1),
    ("film_epistemics", "film")]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def esle(y, kal):
    return any(fnmatch.fnmatch(y, k) for k in kal)


def topla():
    ana, ham, dis = [], [], []
    for yol, tip in ANA_KOK:
        p = os.path.join(SP, yol)
        if tip == 0:
            ana.append(yol); continue
        if tip in ("py", "sha256"):
            ana += sorted("%s/%s" % (yol, f) for f in os.listdir(p) if f.endswith("." + tip) and os.path.isfile(os.path.join(p, f))); continue
        for kok, dl, fl in os.walk(p):
            for f in fl:
                y = os.path.relpath(os.path.join(kok, f), SP).replace(os.sep, "/")
                if tip == "film":   # video: metin, kaynak ve kod; mp4 ve kareler yok
                    if f.endswith(".mp4") or "/arac/veri/filmler.js" in y:
                        dis.append((y, "video / large generated data (delivered separately)")); continue
                if esle(y, DISLA):
                    dis.append((y, "scratch / cache")); continue
                if y == "epistemics/rapor_ekleri/PAKET.md":   # paketi anlatan dosya pakete girmez (dongu)
                    continue
                (ham if esle(y, HAM_KALIP) else ana).append(y)
    return sorted(set(ana)), sorted(set(ham)), dis


# ---- tarama: deger yazilmaz
GIZLI = [("openai/adaption style key sk-", r"sk-[A-Za-z0-9_\-]{16,}"), ("bearer token", r"Bearer\s+[A-Za-z0-9._\-]{16,}"), ("github token", r"gh[pousr]_[A-Za-z0-9]{20,}"),
         ("huggingface token", r"hf_[A-Za-z0-9]{25,}"), ("google api key", r"AIza[0-9A-Za-z_\-]{30,}"), ("aws key", r"AKIA[0-9A-Z]{16}"), ("slack token", r"xox[baprs]-[A-Za-z0-9-]{10,}"),
         ("private key block", r"-----BEGIN [A-Z ]*PRIVATE KEY"), ("key / password assignment", r"(?i)\b(api[_-]?key|secret|password|passwd|parola|token)\b\s*[:=]\s*['\"][^'\"\s]{8,}['\"]")]
KISISEL = [("e-mail address", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), ("TR mobile phone", r"(?<!\d)(?:\+90|0)\s?5\d{2}\s?\d{3}\s?\d{2}\s?\d{2}(?!\d)"),
           ("IPv4 address", r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"), ("Windows user path", r"(?i)users[\\/]+monster"), ("key file path", r"(?i)desktop[\\/]+api[\\/]"),
           ]
# kisi adlari (yazar ve sirket sahibi; kucuk harf): liste pakete girmesin diye yalniz sha256 ilk 16
AD_OZET = {"28949ea86dcc7636": "author first name", "e1cd7a44c70c07d7": "author surname", "b869d7293dabd05f": "author surname",
           "6e7b21d1178f415c": "third party (company owner)", "a0f2800481af8a56": "third party (company owner)", "4556368b1aade1c5": "third party (company owner)"}
KELIME = re.compile(r"[^\W\d_]{4,}")
METIN = (".py", ".md", ".json", ".jsonl", ".txt", ".log", ".csv", ".tsv", ".sha256", ".js", ".html", ".svg", ".sh", ".mjs", ".kafa", ".b64")


def tara(ad, b, sonuc):
    if not ad.lower().endswith(METIN):
        return
    t = b.decode("utf-8", errors="replace")
    for tur, kal in GIZLI + KISISEL:
        for m in re.finditer(kal, t):
            v = m.group(0); bag = t[max(0, m.start() - 24):m.end() + 24]
            if tur.startswith("openai"):
                sinif = "fake test value (contains SAHTE)" if "SAHTE" in v.upper() else "POSSIBLE REAL KEY"
            elif tur == "TR mobile phone":
                sinif = "digits inside a sha256 / hex string" if re.search(r"[0-9a-f]{24,}", bag) else "POSSIBLE PHONE NUMBER"
            elif tur == "IPv4 address":
                sinif = "loopback 127.0.0.1" if v == "127.0.0.1" else ("not an address (part > 255)" if any(int(x) > 255 for x in v.split(".")) else "IP ADDRESS")
            elif tur == "Windows user path":
                sinif = "local machine user folder in a hard-coded path"
            else:
                sinif = "CHECK"
            sonuc.setdefault(tur, []).append((ad, sinif))
    for w in set(KELIME.findall(t.lower())):
        o = hashlib.sha256(w.encode()).hexdigest()[:16]
        if o in AD_OZET:
            sonuc.setdefault("person name (author / company owner)", []).append((ad, AD_OZET[o] + " (name list kept as sha256 only)"))
    if os.path.basename(ad).startswith(".env") or ad.endswith((".pem", ".key")):
        sonuc.setdefault(".env / key file", []).append((ad, 1))


def yaz(ad, dosyalar, sonuc):
    os.makedirs(CIK, exist_ok=True)
    z = os.path.join(CIK, ad); sat = []; ham_bayt = 0
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as Z:
        for y in dosyalar:
            b = open(os.path.join(SP, y), "rb").read(); ham_bayt += len(b)
            Z.writestr(zipfile.ZipInfo(y, time.localtime(os.stat(os.path.join(SP, y)).st_mtime)[:6]), b, zipfile.ZIP_DEFLATED)
            sat.append("%s  %s" % (sha(b), y)); tara(y, b, sonuc)
            if y.endswith(".zip"):   # ic arsiv de taranir
                with zipfile.ZipFile(io.BytesIO(b)) as I:
                    for n in I.namelist():
                        if not n.endswith("/"):
                            tara(y + "!" + n, I.read(n), sonuc)
        Z.writestr("SHA256SUMS.txt", "\n".join(sat) + "\n")
    return z, len(dosyalar), ham_bayt, os.path.getsize(z)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ana, ham, dis = topla()
    S1, S2 = {}, {}
    za = yaz("epistemics_kod_veri_15kas.zip", ana, S1)
    zh = yaz("epistemics_ham_kayit_15kas.zip", ham, S2)
    R = ["# Code / data package · 15 Nov 2026", "", "Built by `epistemics/rapor_ekleri/paket.py`. The first build was published by the author on 15 Nov 2026 (GitHub, first commit and release `sprint-15nov2026`); this rebuild adds S5 and is local until the author's word (no push, no upload). Each archive contains `SHA256SUMS.txt` (sha256 of every file, path relative to the `sprint/` folder).", "",
         "| archive | files | uncompressed | archive size | sha256 of the archive |", "|---|---|---|---|---|"]
    for z, n, hb, zb in (za, zh):
        R.append("| `%s` | %d | %.1f MB | %.1f MB | `%s` |" % (os.path.basename(z), n, hb / 1e6, zb / 1e6, sha(open(z, "rb").read())))
    R += ["", "Location (local only): `%s`." % CIK, "",
          "Main archive: pre-sprint world and runner (`oyun_alani_v4/*.py`, `aktarim/`, freeze manifests and the 12 Nov snapshot zip), sprint preregistrations, deviation files, sprint scripts, measurement files and run logs (S1-S5), the bridge check, figures and tables, README, report appendices, and the video's text, sources and code (no video file).",
          "Raw-record archive: the run records and replays (`sprint_s2/kosular`, `kosular_oynat`, `sprint_s3/kosular`), the model call logs (`sprint_s1/kosu_397b_s1_13kas`, `sprint_s4/cagri_s4_*.jsonl`, `sprint_s5/cagri_s5_*.jsonl`; files named `sahte` are fake-data pipeline tests) and the contradiction-fork answers (`celiski_s2_13kas.jsonl`, `catal_s3_14kas.jsonl`).",
          "Left out: %d scratch / cache files (`karalama*`, `__pycache__`) and %d video / generated files (mp4 files and the generated `filmler.js`; the video is delivered separately)." % (sum(1 for d in dis if d[1].startswith("scratch")), sum(1 for d in dis if d[1].startswith("video"))), "",
          "## Secret and personal-data scan", "",
          "Every text file put into the archives was scanned, including the files inside the 12 Nov snapshot zip. Values are never printed; only file and count.", ""]
    for ad, S in (("main", S1), ("raw", S2)):
        R += ["### %s archive" % ad, ""]
        for tur in [g[0] for g in GIZLI] + [".env / key file"] + [k[0] for k in KISISEL] + ["person name (author / company owner)"]:
            v = S.get(tur, [])
            if not v:
                R.append("- %s: none" % tur); continue
            sinif = {}
            for f, c in v:
                sinif.setdefault(c, set()).add(f)
            R.append("- %s: %d hit(s) in %d file(s). " % (tur, len(v), len({f for f, _ in v})) + "; ".join("%s: %d hit(s), e.g. %s" % (c, sum(1 for _, cc in v if cc == c), ", ".join("`%s`" % f for f in sorted(fs)[:3])) for c, fs in sinif.items()))
        R.append("")
    open(os.path.join(KOK, "PAKET.md"), "w", encoding="utf-8", newline="\n").write("\n".join(R) + "\n")
    print("\n".join(R))


if __name__ == "__main__":
    main()
