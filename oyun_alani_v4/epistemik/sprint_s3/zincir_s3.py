# coding: utf-8
"""S3 ZINCIRI · 14 Kas 2026 · Hikayeci · UCRETLI (Adaption 397B) · yalniz Turan'in Hikayeci penceresindeki soziyle.
  python -I zincir_s3.py pilot            1 koşu: SU t46 (onkayit: olagan, tohum 46). Bitince DURUR; devam icin Turan'in sozu.
  python -I zincir_s3.py asil [--paralel 4] kalan 29 koşu (tohum tohum SU, SG), en cok P surec ayni anda
  ... --sahte --kosular karalama/z   modelsiz sinama
Tamamlanan (durum tamam / kesildi) koşu yeniden kosulmaz. Coken koşu (cikis 0 ya da 4 disi): klasor "<ad>_yarim_<saat>" adini alir (SILINMEZ),
en cok 2 kez yeniden kosulur (seed yok: yeniden koşu YENI bir ornektir; sayisi olcume ayri satir). Fren (cikis 4 ya da S3_DUR.txt) zinciri durdurur.
Gunluk: zincir_s3_<etiket>.log"""
import argparse, json, os, subprocess, sys, time

BU = os.path.dirname(os.path.abspath(__file__)); ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
sys.path.insert(0, BU); import s3_ortak as O  # noqa: E402


def main():
    p = argparse.ArgumentParser(); p.add_argument("adim", choices=["pilot", "asil"]); p.add_argument("--paralel", type=int, default=4)
    p.add_argument("--kosular", default="kosular/s3_14kas"); p.add_argument("--sahte", action="store_true"); p.add_argument("--etiket", default="14kas")
    a = p.parse_args(); sys.stdout.reconfigure(encoding="utf-8")
    gun = open(os.path.join(BU, "zincir_s3_%s%s.log" % (a.etiket, "_sahte" if a.sahte else "")), "a", encoding="utf-8")
    def yaz(*m):
        s = time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in m); print(s, flush=True); gun.write(s + "\n"); gun.flush()
    IS = [("SU", 46)] if a.adim == "pilot" else [(k, t) for t in range(46, 61) for k in ("SU", "SG") if (k, t) != ("SU", 46)]
    def kl(k, t): return os.path.join(BU, a.kosular, k, "t%d" % t)
    def bitti(k, t):
        m = os.path.join(kl(k, t), "kosu_meta.json")
        return os.path.exists(m) and json.load(open(m, encoding="utf-8")).get("durum") in ("tamam", "kesildi")
    kalan = [(k, t) for k, t in IS if not bitti(k, t)]; deneme = {}; calisan = {}; dur = None
    if a.adim == "asil" and not a.sahte:                       # 14 Kas danisman: pilottan tahmini toplam; > 50 $ ise asil BASLAMAZ (genel fren)
        P = [json.loads(x) for x in open(os.path.join(kl("SU", 46), "cagri_s3.jsonl"), encoding="utf-8") if x.strip()]
        c = sum(d["maliyet"] for d in P) / len(P); tah = 30 * len(P) * c + 30 * 3 * 10 * c
        yaz("TAHMIN (pilottan): pilot cagri %d, cagri basi %.4f $, koşular 30 x %d x c = %.2f $, catal 900 x c = %.2f $, toplam %.2f $ (sinir %.0f $)" % (len(P), c, len(P), 30 * len(P) * c, 900 * c, tah, O.TAHMIN_SINIRI))
        if tah > O.TAHMIN_SINIRI:
            open(O.DUR, "w", encoding="utf-8").write(time.strftime("%Y-%m-%d %H:%M:%S ") + "tahmini toplam %.2f $ > %.0f $; asil baslatilmadi" % (tah, O.TAHMIN_SINIRI) + chr(10)); yaz("ASIL BASLATILMADI: tahmin sinirin ustunde"); sys.exit(4)
    yaz("ZINCIR S3", a.adim, "· is", len(IS), "· kalan", len(kalan), "· paralel", a.paralel, "· sahte" if a.sahte else "· UCRETLI")
    while (kalan or calisan) and not dur:
        while kalan and len(calisan) < a.paralel and not os.path.exists(O.DUR) and not os.path.exists(O.DUR_KOSU):
            k, t = kalan.pop(0); c = kl(k, t)
            if os.path.exists(c):
                y = c + "_yarim_" + time.strftime("%H%M%S"); os.rename(c, y); yaz("YARIM klasor kenara alindi (silinmedi):", os.path.relpath(y, BU))
            deneme[(k, t)] = deneme.get((k, t), 0) + 1
            komut = [sys.executable, "-I", os.path.join(BU, "kosu_s3.py"), "--kol", k, "--tohum", str(t), "--cikti", c] + (["--sahte"] if a.sahte else [])
            calisan[(k, t)] = (subprocess.Popen(komut, env=ENV, cwd=BU, stdout=gun, stderr=subprocess.STDOUT), time.time()); yaz("BASLADI", k, t, "deneme", deneme[(k, t)])
        time.sleep(2 if a.sahte else 15)
        for (k, t), (ps, t0) in list(calisan.items()):
            if ps.poll() is None: continue
            del calisan[(k, t)]; r = ps.returncode; yaz("BITTI", k, t, "cikis", r, "sure sn", round(time.time() - t0))
            if r == 4 or os.path.exists(O.DUR) or os.path.exists(O.DUR_KOSU):
                f_ = O.DUR if os.path.exists(O.DUR) else O.DUR_KOSU; dur = open(f_, encoding="utf-8").read().strip() if os.path.exists(f_) else "fren (cikis 4)"; yaz("FREN: zincir durdu ·", dur)
            elif r != 0:
                if deneme[(k, t)] < 3: kalan.insert(0, (k, t)); yaz("COKTU, yeniden kosulacak:", k, t)
                else: yaz("COKTU 3 kez, atlandi:", k, t)
        for f_ in (O.DUR, O.DUR_KOSU):
            if os.path.exists(f_) and not dur: dur = open(f_, encoding="utf-8").read().strip(); yaz("FREN dosyasi:", os.path.basename(f_), dur)
    for (k, t), (ps, _) in calisan.items(): ps.wait(); yaz("BITTI (fren sonrasi bekleme)", k, t, "cikis", ps.returncode)
    import glob
    D = [json.loads(x) for p in glob.glob(os.path.join(BU, a.kosular, "*", "t*", "cagri_s3.jsonl")) for x in open(p, encoding="utf-8") if x.strip()]
    yaz("ZINCIR S3 SONU", a.adim, "· durum", "fren: " + dur if dur else "tamam", "· cagri", len(D), "· harcama %.4f $" % sum(d.get("maliyet") or 0 for d in D))
    sys.exit(0 if not dur else 4)


if __name__ == "__main__":
    main()
