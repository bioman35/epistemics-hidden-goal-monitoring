# coding: utf-8
"""S3 KOSU SURUCUSU (tek koşu) · 14 Kas 2026 · Hikayeci · onkayit ONKAYIT_S3_397b_ajan.md + SAPMA_S3_14kas.md
Donuk dosyalara dokunmaz. sprint_s2/kosu_durdur.py ICE AKTARILIR (degistirilmez): dunya_durdur.py (ozet denetimli) "dunya" adiyla yuklenir,
kartlar ve takas (dagitim) S2 ile ayni. Fark yalniz: emir KAPALI (DD.DURDUR_ACIK = False, olagan kol) ve tasiyici 397B (s3_ortak.Adaption397).
Kollar: SU = T1 U1 (S2'deki DU dagitimi) · SG = T1 G (S2'deki DG dagitimi). Tohum 46-60. Seed YOK (Adaption'da yok; ajan tohumlari hesaplanir ama gonderilmez).
Kosu 150 cagrida KESILIR (kayit klasoru "kesildi" isaretiyle kalir; dunya kaydi yazilamaz, cagri kaydi tam).
python -I kosu_s3.py --kol SU --tohum 46 --cikti kosular/s3_14kas/SU/t46 [--sahte] [--sinir 150]"""
import argparse, hashlib, json, os, sys, time

BU = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(BU); KOK = os.path.dirname(EP)
sys.path.insert(0, os.path.join(EP, "sprint_s2")); sys.path.insert(0, BU)
import kosu_durdur as KD   # noqa: E402  (ozet denetimleri ice aktarmada calisir)
import s3_ortak as O       # noqa: E402
M, K, S, DD = KD.M, KD.K, KD.S, KD.DD
KOL = {"SU": "DU", "SG": "DG"}


def ozet(y):
    return hashlib.sha256(open(y, "rb").read()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(); p.add_argument("--kol", choices=list(KOL), required=True); p.add_argument("--tohum", type=int, required=True)
    p.add_argument("--cikti", required=True); p.add_argument("--sahte", action="store_true"); p.add_argument("--sinir", type=int, default=O.KOSU_CAGRI_SINIRI)
    p.add_argument("--sahte-gecersiz", type=float, default=0.0)
    a = p.parse_args()
    if a.tohum not in range(46, 61): raise SystemExit("tohum 46-60 disi")
    os.makedirs(a.cikti, exist_ok=True)
    if os.path.exists(os.path.join(a.cikti, "kosu_meta.json")): raise SystemExit("cikti klasoru dolu: %s" % a.cikti)
    KD.bagla(False, "cikis_odasi", KOL[a.kol])                  # emir KAPALI: olagan kol
    assert DD.DURDUR_ACIK is False
    kartlar, kart_oz = K.oku()
    kural_oz = M.ozet_dosya(os.path.join(KOK, K.KURAL_DOSYA))
    if kural_oz != K.KURAL_OZET: raise SystemExit("kural ozeti degisti")
    cp = os.path.join(a.cikti, "cagri_s3.jsonl"); t = O.Adaption397(cp, "kosu", sahte=a.sahte, sinir=a.sinir, sahte_gecersiz=a.sahte_gecersiz)
    _karar = S.ModelAjan.karar
    def karar(self, g):                                          # hangi ajanin cagirdigi cagri kaydina yazilsin diye (davranis degismez)
        t.ajan, t.adim = self.id, g.get("adim", g.get("tur")); return _karar(self, g)
    S.ModelAjan.karar = karar
    meta = {"s3": True, "kol": a.kol, "dagitim_kolu_s2": KOL[a.kol], "tohum": a.tohum, "emir": "kapali (DURDUR_ACIK = False, olagan kol)", "model": t.model,
            "tasiyici": "adaption responses, akisli" if not a.sahte else "SAHTE: dil modeli yok, yalniz boru hatti sinamasi; sonuc model sonucu DEGILDIR",
            "sicaklik": O.SICAKLIK, "cikti_payi": O.CIKTI_PAYI, "seed": "YOK (Adaption seed kabul etmiyor; ajan tohumlari hesaplanir, gonderilmez)",
            "kosu_cagri_siniri": a.sinir, "fiyat_1M": O.FIYAT, "kart_ozet": kart_oz, "kural_ozet": kural_oz,
            "ozet": {"kosu_s3.py": ozet(__file__), "s3_ortak.py": ozet(O.__file__), "kosu_durdur.py": ozet(KD.__file__), "dunya_durdur.py": ozet(DD.__file__)},
            "baslangic": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "eslesme_7b": "ayni tohum = ayni baslangic dunyasi; model farkli"}
    json.dump(meta, open(os.path.join(a.cikti, "kosu_meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    isler = list(M.isler(2, [a.tohum], ["O1_O2b"])); assert len(isler) == 1
    kosu_id, tohum, kosul, dag = isler[0]; kosu_id = kosu_id.replace("_DU", "_" + a.kol).replace("_DG", "_" + a.kol)
    ajanlar = M.ekip_kur(dag, kartlar, t, kosul, tohum, S.Butce()); bas = time.time(); durum = "tamam"; ayr = None
    try:
        d = M.kos(ajanlar, tohum, kosu_id)
        d.kayit.kaydet(os.path.join(a.cikti, kosu_id + ".jsonl")); d.kayit.kafa_bas(os.path.join(a.cikti, kosu_id + ".kafa"))
        tamam, _ = M.dogrula(d.kayit.metin()); o = M.olcum.olc([json.loads(x) for x in d.kayit.satirlar])
        o.update(kosul=kosul, dagitim=dag, sure_duvar_sn=round(time.time() - bas, 1), zincir=tamam, cagri={x.id: x.sayac for x in ajanlar})
        json.dump(o, open(os.path.join(a.cikti, kosu_id + ".olcum.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    except O.KosuKesildi as h:
        durum, ayr = "kesildi", str(h)
    except O.S3Dur as h:
        durum, ayr = "fren", str(h)
    C = [json.loads(x) for x in open(cp, encoding="utf-8")] if os.path.exists(cp) else []
    meta.update(bitis=time.strftime("%Y-%m-%dT%H:%M:%S%z"), durum=durum, ayrinti=ayr, kosu_id=kosu_id, T1=KD.DEGISEN.get(tohum, {}).get("T1"), degisen=KD.DEGISEN.get(tohum),
                cagri=len(C), girdi=sum(c["girdi"] for c in C), cikti=sum(c["cikti"] for c in C), gecersiz=sum(1 for c in C if c["gecersiz"]),
                kesik=sum(1 for c in C if c["kesik"]), hata=sum(1 for c in C if c["hata"]), maliyet=round(sum(c["maliyet"] for c in C), 6), sure_sn=round(time.time() - bas))
    json.dump(meta, open(os.path.join(a.cikti, "kosu_meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("S3 %s t%d %s · T1 %s · cagri %d · gecersiz %d · kesik %d · %.4f $ · %d sn%s" % (a.kol, a.tohum, durum, meta["T1"], meta["cagri"], meta["gecersiz"], meta["kesik"], meta["maliyet"], meta["sure_sn"], (" · " + ayr) if ayr else ""), flush=True)
    sys.exit(0 if durum in ("tamam", "kesildi") else 4)


if __name__ == "__main__":
    main()
