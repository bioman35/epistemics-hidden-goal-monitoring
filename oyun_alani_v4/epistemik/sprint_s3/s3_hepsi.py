# coding: utf-8
"""S3 HEPSI · 14 Kas 2026 · Hikayeci · UCRETLI · Turan'in Hikayeci penceresindeki sozu (14 Kas ~08:2x): "kalan 29 koşu dedi hepsini yapabilirsin, ben işe gidiyorum"
Sira: pilot (SU t46) -> PILOT DENETIMI -> asil 29 koşu -> catal -> olcu. Pilot denetimi gecmezse DURUR (asil baslamaz), nedenini yazar.
PILOT DENETIMI (SAPMA_S3_14kas.md'de koşudan once yazildi): durum "tamam" ya da "kesildi" · hata ile biten cagri yok (mesaj dizisi kabul edildi) ·
  gecersiz JSON orani <= ,15 · cikti jetonu ortalamasi <= 6.000 · pilot maliyeti <= 3 $ · S3_DUR.txt yok.
Gunluk: s3_hepsi_14kas.log · ozet: s3_hepsi_14kas.json"""
import json, os, subprocess, sys, time

BU = os.path.dirname(os.path.abspath(__file__)); ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1"); PY = [sys.executable, "-I"]
sys.path.insert(0, BU); import s3_ortak as O  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding="utf-8"); gun = open(os.path.join(BU, "s3_hepsi_14kas.log"), "a", encoding="utf-8"); oz = {"baslangic": time.strftime("%Y-%m-%dT%H:%M:%S"), "adim": []}
    def yaz(*m):
        s = time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in m); print(s, flush=True); gun.write(s + "\n"); gun.flush()
    def kos(ad, komut):
        t0 = time.time(); r = subprocess.run(PY + komut, env=ENV, cwd=BU, stdout=gun, stderr=subprocess.STDOUT).returncode
        oz["adim"].append({"ad": ad, "cikis": r, "sure_sn": round(time.time() - t0)}); yaz("ADIM", ad, "cikis", r, "sure sn", round(time.time() - t0)); return r
    def bitir(durum):
        oz.update(durum=durum, bitis=time.strftime("%Y-%m-%dT%H:%M:%S")); json.dump(oz, open(os.path.join(BU, "s3_hepsi_14kas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1); yaz("S3 HEPSI BITTI ·", durum); sys.exit(0 if durum == "tamam" else 1)
    yaz("S3 HEPSI basladi")
    kos("pilot", ["zincir_s3.py", "pilot"])
    m = os.path.join(BU, "kosular", "s3_14kas", "SU", "t46", "kosu_meta.json"); C = os.path.join(BU, "kosular", "s3_14kas", "SU", "t46", "cagri_s3.jsonl")
    if not os.path.exists(m) or not os.path.exists(C): bitir("pilot klasoru eksik")
    M = json.load(open(m, encoding="utf-8")); L = [json.loads(x) for x in open(C, encoding="utf-8") if x.strip()]
    n = len(L); g = sum(1 for c in L if c["gecersiz"]) / n if n else 1; co = sum(c["cikti"] for c in L) / n if n else 0; h = sum(1 for c in L if c["hata"]); mal = sum(c["maliyet"] for c in L)
    pd = {"durum": M.get("durum"), "cagri": n, "gecersiz_oran": round(g, 3), "cikti_ort": round(co), "hata": h, "kesik": sum(1 for c in L if c["kesik"]), "maliyet": round(mal, 4),
          "sure_sn": M.get("sure_sn"), "ilk_cagri": {k: L[0].get(k) for k in ("durum", "hata", "girdi", "cikti", "gecersiz")} if L else None}
    oz["pilot"] = pd; yaz("PILOT", json.dumps(pd, ensure_ascii=False))
    neden = [x for x, kosul in (("durum %s" % pd["durum"], pd["durum"] not in ("tamam", "kesildi")), ("hatali cagri %d" % h, h > 0), ("gecersiz %.3f" % g, g > .15),
                                 ("cikti ort %.0f" % co, co > 6000), ("pilot maliyeti %.2f $" % mal, mal > 3), ("S3_DUR.txt var", os.path.exists(O.DUR))) if kosul]
    if neden: bitir("PILOT DENETIMI GECMEDI: " + "; ".join(neden))
    yaz("PILOT DENETIMI GECTI, asil kosu basliyor")
    r = kos("asil", ["zincir_s3.py", "asil", "--paralel", "4"])
    if r != 0: yaz("ASIL zincir fren / hata ile bitti; catal ve olcu yine de mevcut koşularla kosulacak (fren dosyasi varsa catal yeni cagri acmaz)")
    if not os.path.exists(O.DUR): kos("catal", ["catal_s3.py", "--paralel", "4"])
    kos("olcu", ["olc_s3.py"])
    bitir("tamam" if r == 0 and not os.path.exists(O.DUR) else ("fren: " + open(O.DUR, encoding="utf-8").read().strip() if os.path.exists(O.DUR) else "asil zincir cikis %d" % r))


if __name__ == "__main__":
    main()
