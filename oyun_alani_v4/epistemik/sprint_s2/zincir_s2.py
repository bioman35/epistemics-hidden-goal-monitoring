# coding: utf-8
"""S2 ASIL KOSU ZINCIRI · 13 Kas 2026 (sprint ici) · Hikayeci · EKRAN KARTI ISTER (yerel Ollama 7B) · 0 $
YALNIZ Turan'in yayinsiz pencere sozuyle baslatilir.
SIRA (danisman karari 13 Kas, SAPMA_S2_13kas.md madde 5): TOHUM TOHUM. Her tohumda DU, DG, EG (birincil kume, 45 kosu); tohum 46'dan 60'a.
  Hepsi bitince EU blogu (46-60): "tekrar gurultusu" (DU ile ayni kurulumun ikinci kosusu; birincil olcuye girmez). --eu-yok ile atlanir.
Klasor: kosular/s2_<etiket>/<KOL>/t<NN>/ (her klasorde tek kosu). Tamam = klasorde kosu_durdur_meta.json var.
Yarim kalan kosu SILINMEZ: klasor "t<NN>_yarim_<saat>" adini alir, tohum yeni (bos) "t<NN>" klasorunde yeniden kosulur; gunluge yazilir.
Bekci: her 20 saniyede surec listesi; TikTok LIVE Studio / OBS / Unreal acilirsa kosan kosu surec agaciyla durdurulur ve zincir cikar.
Yeniden baslatinca kaldigi yerden surer (tamam olanlar atlanir).
Kullanim: python -I zincir_s2.py [--etiket 13kas] [--tohumlar 46-60] [--eu-yok] [--kuru]      (--kuru: yalniz sirayi yazar, hicbir sey kosmaz)"""
import argparse, json, os, subprocess, sys, time

BU = os.path.dirname(os.path.abspath(__file__))
YAYIN = ("tiktok live studio", "obs64", "obs32", "obs.exe", "unrealeditor")
MODEL = "qwen2.5:7b-instruct-q4_K_M"
BIRINCIL = ("DU", "DG", "EG")


def yayin():
    s = subprocess.run(["tasklist"], capture_output=True, text=True, errors="ignore").stdout.lower()
    return [k for k in YAYIN if k in s]


def sira(tohumlar, eu=True):
    return [(t, k) for t in tohumlar for k in BIRINCIL] + ([(t, "EU") for t in tohumlar] if eu else [])


def main():
    p = argparse.ArgumentParser(); p.add_argument("--etiket", default="13kas"); p.add_argument("--tohumlar", default="46-60")
    p.add_argument("--eu-yok", action="store_true"); p.add_argument("--kuru", action="store_true")
    a = p.parse_args(); sys.stdout.reconfigure(encoding="utf-8")
    a0, a1 = (int(x) for x in a.tohumlar.split("-")) if "-" in a.tohumlar else (int(a.tohumlar), int(a.tohumlar))
    tohumlar = list(range(a0, a1 + 1)); assert set(tohumlar) <= set(range(46, 61)), "tohum disi"
    S = sira(tohumlar, not a.eu_yok); kok = os.path.join(BU, "kosular", "s2_%s" % a.etiket)
    if a.kuru:
        print("sira (%d kosu):" % len(S), " ".join("%d%s" % q for q in S)); return
    gunluk = open(os.path.join(BU, "zincir_s2_%s.log" % a.etiket), "a", encoding="utf-8")
    def yaz(*m):
        s = time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in m); print(s, flush=True); gunluk.write(s + "\n"); gunluk.flush()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1"); t0 = time.time(); sure, kosulan = {}, 0
    yaz("ZINCIR BASLADI", len(S), "kosu, sira tohum tohum:", " ".join(BIRINCIL), "sonra EU" if not a.eu_yok else "(EU yok)")
    for t, kol in S:
        cik = os.path.join(kok, kol, "t%d" % t)
        if os.path.exists(os.path.join(cik, "kosu_durdur_meta.json")):
            continue
        if os.path.isdir(cik) and os.listdir(cik):
            yeni = cik + "_yarim_" + time.strftime("%H%M%S"); os.rename(cik, yeni); yaz("YARIM kosu kenara alindi (silinmedi):", os.path.relpath(yeni, BU), "· tohum yeniden kosulacak")
        acik = yayin()
        if acik:
            yaz("DUR: yayin programi acik:", acik, "· kalinan yer", t, kol); sys.exit(3)
        t1 = time.time()
        ps = subprocess.Popen([sys.executable, "-I", os.path.join(BU, "kosu_durdur.py"), "--kol", kol, "--emir", "acik", "--yer", "cikis_odasi", "--tasiyici", "yerel",
                               "--model", MODEL, "--tohumlar", str(t), "--cikti", cik], env=env, stdout=gunluk, stderr=subprocess.STDOUT)
        while ps.poll() is None:
            time.sleep(20); acik = yayin()
            if acik:
                subprocess.run(["taskkill", "/PID", str(ps.pid), "/T", "/F"], capture_output=True)
                yaz("BEKCI DURDURDU:", t, kol, "yayin programi acildi:", acik, "· yarim klasor yerinde, yeniden baslatinca kenara alinir"); sys.exit(3)
        sure["%d_%s" % (t, kol)] = round(time.time() - t1); kosulan += 1
        yaz("BITTI t%d %s cikis %d sure %d sn (toplam %d sn, %d kosu)" % (t, kol, ps.returncode, sure["%d_%s" % (t, kol)], time.time() - t0, kosulan))
        if ps.returncode != 0:
            yaz("HATA: kosu bitmedi, zincir durdu"); sys.exit(1)
    yaz("OLCU")
    r = subprocess.run([sys.executable, "-I", os.path.join(BU, "olc_s2.py"), "--kosular", "kosular", "--etiket", a.etiket], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    yaz(r.stdout[-3000:], r.stderr[-1500:])
    json.dump({"sure_sn": sure, "toplam_sn": round(time.time() - t0)}, open(os.path.join(BU, "zincir_s2_%s_sure_%s.json" % (a.etiket, time.strftime("%H%M%S"))), "w"), indent=1)
    yaz("ZINCIR BITTI toplam sn", round(time.time() - t0))


if __name__ == "__main__":
    main()
