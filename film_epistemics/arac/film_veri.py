# coding: utf-8
"""TESLIM VIDEOSU · VERI URETICISI (film_sprint/film_veri.py kopyasi, 14 Kas) · S2 kol E tohum 58: DU_58 ve EG_58.
Kayda dokunmaz, model cagrisi yok. Olaylar, sira, kapi kararlari ve ajan cumleleri kayittan birebir gelir.
Ayrica: ayni baslangic dunyasi saglamasi (veri/saglama.json) ve sahne 2 sayac + serit verisi (veri/sayac.json).
Calistir: python -I film_veri.py  -> veri/filmler.js, veri/saglama.json, veri/sayac.json"""
import hashlib
import json
import os
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
EP = os.path.normpath(os.path.join(KOK, "..", "..", "oyun_alani_v4", "epistemik"))
S2 = os.path.join(EP, "sprint_s2")
TOHUM = "58"
ALAN = ("adim", "zaman", "ajan_id", "ajan_turu", "rol", "karakter", "konum", "olay", "metin", "karar", "renk", "kapi_id", "isaret", "ajan_aciklamasi")
FILM = [{"id": "DU", "vaka": "DU_" + TOHUM, "yol": "kosular/s2_13kas/DU/t%s/v4_kosu2_O1_O2b_t%s_DU" % (TOHUM, TOHUM), "etiket": "sleeper"},
        {"id": "EG", "vaka": "EG_" + TOHUM, "yol": "kosular/s2_13kas/EG/t%s/v4_kosu2_O1_O2b_t%s_EG" % (TOHUM, TOHUM), "etiket": "control"}]
KADRO_ALAN = ("ajan_turu", "karakter")          # kadroyu tasiyan alanlar
ATLA = ("kosu_id", "onceki_ozet", "maliyet")    # kosu adi, zincir ozeti ve maliyet karsilastirilmaz


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cikti, ham_kayit, meta = [], {}, {}
    for f in FILM:
        p = os.path.join(S2, f["yol"].replace("/", os.sep))
        ham = open(p + ".jsonl", "rb").read()
        tam = [json.loads(l) for l in ham.decode("utf-8").splitlines()]
        ham_kayit[f["id"]] = tam
        kayit = [{k: e.get(k) for k in ALAN if e.get(k) not in (None, "")} for e in tam]
        o = json.load(open(p + ".olcum.json", encoding="utf-8"))
        mp = os.path.join(os.path.dirname(p), "kosu_durdur_meta.json")
        m = json.load(open(mp, encoding="utf-8"))
        meta[f["id"]] = {"dosya": os.path.relpath(mp, EP).replace(os.sep, "/"), "sha": sha(mp), "degisen": m["degisen"][TOHUM],
                         **{k: m.get(k) for k in ("eslesme", "dunya_kaynak_ozet", "dunya_durdur_ozet", "surucu_ozet", "kart_ikiz_ozet")}}
        cikti.append({"id": f["id"], "vaka": f["vaka"], "etiket": f["etiket"], "baslik": {"tr": f["vaka"], "en": f["vaka"]}, "ozet": {"tr": f["etiket"], "en": f["etiket"]}, "kosu": os.path.basename(f["yol"]), "dosya": os.path.relpath(p + ".jsonl", EP).replace(os.sep, "/"),
                      "sha": hashlib.sha256(ham).hexdigest(), "kayit": kayit,
                      "olcum": {k: o.get(k) for k in ("is_basarisi", "tur", "durdu", "takildi", "turler", "dagitim", "fark_edilmeme", "kanarya_arsivde", "kararlar")}})

    # --- ayni baslangic saglamasi: T1'in ilk model eylemine kadar olan satirlar (giris jetonu dahil)
    def bas(L):
        return L[:next(j for j, e in enumerate(L) if e["ajan_id"] == "T1" and not (e["olay"] == "gir" and (e.get("metin") or "").startswith("jeton verildi")))]
    a, b = bas(ham_kayit["DU"]), bas(ham_kayit["EG"])
    farklar = []
    for x, y in zip(a, b):
        fk = sorted(k for k in set(x) | set(y) if k not in KADRO_ALAN + ATLA and x.get(k) != y.get(k))
        kd = sorted(k for k in KADRO_ALAN if x.get(k) != y.get(k))
        if fk or kd:
            farklar.append({"adim": x["adim"], "ajan": x["ajan_id"], "kadro_farki": {k: [x.get(k), y.get(k)] for k in kd}, "baska_fark": fk})
    md, me = meta["DU"], meta["EG"]
    saglama = {"tohum": int(TOHUM), "kural": "T1'in ilk model eylemine kadar her satir; kosu_id, onceki_ozet, maliyet disinda butun alanlar; ajan_turu ve karakter kadro farki olarak ayri",
               "karsilastirilan_satir": [len(a), len(b)], "satir_farklari": farklar,
               "kadro_disi_fark_yok": all(not f["baska_fark"] for f in farklar) and len(a) == len(b),
               "kadro_farki_olan_ajanlar": sorted({f["ajan"] for f in farklar if f["kadro_farki"]}),
               "meta_ayni": {k: md[k] == me[k] for k in ("dunya_kaynak_ozet", "dunya_durdur_ozet", "surucu_ozet", "kart_ikiz_ozet")},
               "kadro": {"DU": md["degisen"]["dagitim"], "EG": me["degisen"]["dagitim"]},
               "uyuyan_yeri": {"DU": md["degisen"]["uyuyan_yeri"], "EG": me["degisen"]["uyuyan_yeri"]},
               "kanarya": [next(e["metin"] for e in ham_kayit[k] if (e.get("metin") or "").startswith("kanarya:")) for k in ("DU", "EG")],
               "meta": {k: {"dosya": meta[k]["dosya"], "sha": meta[k]["sha"]} for k in meta}}

    # --- sahne 2 sayaci: celiski_s2_13kas.jsonl; toplamlar olcum_celiski_ek_14kas.json kol E ile saglanir
    cp, op = os.path.join(S2, "celiski_s2_13kas.jsonl"), os.path.join(S2, "olcum_celiski_ek_14kas.json")
    C = [json.loads(l) for l in open(cp, encoding="utf-8")]
    oe = json.load(open(op, encoding="utf-8"))
    sayac = {"kaynak": {"celiski": {"dosya": "sprint_s2/celiski_s2_13kas.jsonl", "sha": sha(cp)}, "olcum": {"dosya": "sprint_s2/olcum_celiski_ek_14kas.json", "sha": sha(op), "alan": "vaka[kol=E].israr"}},
             "kosu": [], "serit": {t: sorted(({"vaka": v["vaka"], "israr": v["israr"]} for v in oe["vaka"] if v["kol"] == "E" and v["tur"] == t), key=lambda r: r["israr"]) for t in ("U", "G")}}
    for f in FILM:
        R = [e for e in C if e["vaka"] == f["vaka"]]
        anlar = []
        for ad in sorted({int(e["adim"]) for e in R}):
            r = sorted((e for e in R if int(e["adim"]) == ad), key=lambda e: int(e["k"]))
            assert [int(e["k"]) for e in r] == list(range(1, 11)), (f["vaka"], ad)
            anlar.append({"adim": ad, "X": r[0]["X"], "yine_X": sum(1 for e in r if not e["plan_degisti"]),
                          "kutu": [{"k": int(e["k"]), "eylem": e["eylem"], "hedef": e["hedef"], "yine_X": not e["plan_degisti"]} for e in r]})
        top = sum(x["yine_X"] for x in anlar)
        ov = next(v for v in oe["vaka"] if v["kol"] == "E" and v["vaka"] == f["vaka"])
        assert len(anlar) == 3 and abs(top / 30 - ov["israr"]) < 1e-3, (f["vaka"], top, ov["israr"])
        ke = next(e for e in ham_kayit[f["id"]] if e["adim"] == anlar[0]["adim"])   # karar ani kayitta T1'in "gir X" satiri
        assert ke["ajan_id"] == "T1" and ke["konum"] == anlar[0]["X"] and ke["olay"] == "gir", ke
        sayac["kosu"].append({"id": f["id"], "vaka": f["vaka"], "anlar": anlar, "toplam": top, "n": 30, "israr_olcum": ov["israr"], "karar_adim": ke["adim"], "karar_zaman": ke["zaman"]})
    assert len(sayac["serit"]["U"]) == 14 and len(sayac["serit"]["G"]) == 13
    for c, s in zip(cikti, sayac["kosu"]):   # v4 (14 Kas): uc karar aninin kayit adimi; film.js ep=4 bu adimlarda durur
        c["anlar"] = [a["adim"] for a in s["anlar"]]

    os.makedirs(os.path.join(KOK, "veri"), exist_ok=True)
    with open(os.path.join(KOK, "veri", "filmler.js"), "w", encoding="utf-8", newline="\n") as h:
        h.write("window.FILMLER=" + json.dumps(cikti, ensure_ascii=False, separators=(",", ":")) + ";\n")
    for ad, v in (("saglama.json", saglama), ("sayac.json", sayac)):
        with open(os.path.join(KOK, "veri", ad), "w", encoding="utf-8", newline="\n") as h:
            json.dump(v, h, ensure_ascii=False, indent=1)
    for c in cikti:
        print(c["vaka"], len(c["kayit"]), "olay", c["sha"][:16], c["olcum"]["turler"])
    print("saglama", json.dumps({k: saglama[k] for k in ("karsilastirilan_satir", "kadro_disi_fark_yok", "kadro_farki_olan_ajanlar", "meta_ayni", "uyuyan_yeri", "kanarya")}, ensure_ascii=False))
    for f in saglama["satir_farklari"]:
        print("  fark", f)
    for s in sayac["kosu"]:
        print(s["vaka"], [(a["adim"], a["X"], a["yine_X"]) for a in s["anlar"]], s["toplam"], "/ 30", s["israr_olcum"], "karar", s["karar_adim"], "zaman", s["karar_zaman"])


if __name__ == "__main__":
    main()
