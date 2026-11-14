# coding: utf-8
"""S2 · CELISKI ISRARI EK ARALIKLARI · 14 Kas 2026 · Hikayeci · danismanin istegi · ONKAYIT DISI, BETIMLEME / KESIF.
Ekran karti ve para gerektirmez: mevcut cati verisi (celiski_s2_13kas.jsonl) ve olc_s2 olcumu (olcum_s2_13kas.json) okunur. Eski dosyalar degismez.
Yontem (S1 ile ayni): AUC'ler sabit puanlar uzerinden; k-NN puanlari BIR KEZ tum veride tohum disarida hesaplanir (celiski_s2.knn_puan, k=5, z-olcek),
sonra SINIF KATMANLI bootstrap 1000 (U ve G vakalari ayri ayri yerine koyarak), sabit tohum; esli farklar AYNI bootstrap orneklerinde.
Aralik: siralanmis 1000 degerin [int(.025*1000)] ve [int(.975*1000)-1] elemanlari (yargic_ikiz_11kas.bs_auc ile ayni).
Cikti: olcum_celiski_ek_14kas.json / .md · python -I olc_celiski_ek_14kas.py"""
import collections, importlib.util, json, os, random, statistics as st, sys

BU = os.path.dirname(os.path.abspath(__file__)); BOOT = 1000
s = importlib.util.spec_from_file_location("c2", os.path.join(BU, "celiski_s2.py")); C2 = importlib.util.module_from_spec(s); s.loader.exec_module(C2)
auc, knn = C2.auc, C2.knn_puan


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    J = json.load(open(os.path.join(BU, "olcum_s2_13kas.json"), encoding="utf-8")); CEL = C2.jl(os.path.join(BU, "celiski_s2_13kas.jsonl"))
    isr = collections.defaultdict(list)
    for r in CEL: isr[r["vaka"]].append(0 if r["plan_degisti"] else 1)
    R = {"betik": os.path.basename(__file__), "etiket": "ONKAYIT DISI, BETIMLEME / KESIF", "boot": BOOT, "kaynak": ["celiski_s2_13kas.jsonl", "olcum_s2_13kas.json"], "kol": {}, "vaka": []}
    md = ["# S2 · çelişki ısrarı ek aralıkları · ÖNKAYIT DIŞI, BETİMLEME / KEŞİF", "",
          "Betik `olc_celiski_ek_14kas.py`. Mevcut çatal verisinden (ekran kartı yok, model çağrısı yok). AUC sabit puanlar üzerinden; k-NN puanları bir kez, tohum dışarıda (k=5, z-ölçek). Sınıf katmanlı bootstrap 1000, sabit tohum; eşli farklar aynı bootstrap örneklerinde. Yöntem S1 ile aynı.", ""]
    for ad, (U, G) in (("D", ("DU", "DG")), ("E", ("DU", "EG"))):
        V = {k: v for k, v in J["vaka"].items() if k.split("_")[0] in (U, G) and v.get("emre_ulasti") and k in isr}
        K = sorted(V); Y = [1 if k.startswith(U) else 0 for k in K]; T = [int(k.split("_")[1]) for k in K]
        P = {"israr": [st.mean(isr[k]) for k in K], "karar_once_tek_yon": [V[k]["karar_once"] for k in K], "karar_toplam_tek_yon": [V[k]["karar_toplam"] for k in K]}
        P["karar_once_knn"] = knn([[x] for x in P["karar_once_tek_yon"]], Y, T); P["karar_toplam_knn"] = knn([[x] for x in P["karar_toplam_tek_yon"]], Y, T)
        P["birlesim_knn"] = knn([[i, x] for i, x in zip(P["israr"], P["karar_once_tek_yon"])], Y, T)
        iu = [i for i in range(len(K)) if Y[i]]; ig = [i for i in range(len(K)) if not Y[i]]
        A = lambda p, iu_, ig_: auc([p[i] for i in iu_], [p[i] for i in ig_])
        rr = random.Random("celiski-ek-14kas-%s" % ad); ORN = [([rr.choice(iu) for _ in iu], [rr.choice(ig) for _ in ig]) for _ in range(BOOT)]
        def ara(f):
            v = sorted(f(a, b) for a, b in ORN); return [round(v[int(.025 * BOOT)], 3), round(v[int(.975 * BOOT) - 1], 3)]
        o = {"U": U, "G": G, "n_U": len(iu), "n_G": len(ig), "auc": {n: round(A(p, iu, ig), 3) for n, p in P.items()}}
        o["israr_auc_ara"] = ara(lambda a, b: A(P["israr"], a, b))
        o["fark"] = {}
        for t in ("karar_once_tek_yon", "karar_once_knn", "karar_toplam_tek_yon", "karar_toplam_knn"):
            o["fark"]["israr - " + t] = {"deger": round(A(P["israr"], iu, ig) - A(P[t], iu, ig), 3), "ara": ara(lambda a, b, t=t: A(P["israr"], a, b) - A(P[t], a, b))}
        o["fark"]["birlesim_knn - israr"] = {"deger": round(A(P["birlesim_knn"], iu, ig) - A(P["israr"], iu, ig), 3), "ara": ara(lambda a, b: A(P["birlesim_knn"], a, b) - A(P["israr"], a, b))}
        R["kol"][ad] = o
        for i, k in enumerate(K):
            R["vaka"].append({"kol": ad, "vaka": k, "tohum": T[i], "tur": "U" if Y[i] else "G", "kod": V[k]["T1"], "israr": round(P["israr"][i], 3), "karar_once": P["karar_once_tek_yon"][i], "karar_toplam": P["karar_toplam_tek_yon"][i]})
        md += ["## Kol %s (%s ve %s) · n U %d, G %d" % (ad, U, G, len(iu), len(ig)), "",
               "1. Israr AUC (U yüksek): %.3f, %%95 aralık %s" % (o["auc"]["israr"], o["israr_auc_ara"]), "",
               "| eşli fark | değer | %95 aralık |", "|---|---|---|"]
        for n, v in o["fark"].items(): md.append("| %s | %.3f | %s |" % (n, v["deger"], v["ara"]))
        md += ["", "Tek tek AUC: " + " · ".join("%s %.3f" % (n, v) for n, v in o["auc"].items()), ""]
    md += ["## Vaka listesi (iki kol; DU vakaları iki kolda da geçer, seçme yok)", "", "| kol | vaka | tohum | tür | T1 kodu | ısrar | emirden önceki karar | toplam karar |", "|---|---|---|---|---|---|---|---|"]
    for v in R["vaka"]: md.append("| %s | %s | %d | %s | %s | %.3f | %d | %d |" % (v["kol"], v["vaka"], v["tohum"], v["tur"], v["kod"], v["israr"], v["karar_once"], v["karar_toplam"]))
    md += ["", "## Kilitteki havuz değeri ile yan yana", "", "Kilitteki havuz değeri kaynağı: `epistemics/KILIT_12kas.md` satır 27 (\"Israr tek başına ...\"). Değer bu dosyaya kopyalanmadı; okuma danışmanda.", ""]
    json.dump(R, open(os.path.join(BU, "olcum_celiski_ek_14kas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(BU, "olcum_celiski_ek_14kas.md"), "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")
    for ad, o in R["kol"].items(): print(ad, json.dumps({"n": [o["n_U"], o["n_G"]], "auc": o["auc"], "israr_ara": o["israr_auc_ara"], "fark": o["fark"]}, ensure_ascii=False))
    print("vaka satiri", len(R["vaka"]))


main()
