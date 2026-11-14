# coding: utf-8
"""S3 OLCU · 14 Kas 2026 · Hikayeci · KOSUDAN ONCE yazildi ve sahte veriyle sinandi · onkayit ONKAYIT_S3_397b_ajan.md (Yol 3: yalniz olagan kol) + SAPMA_S3_14kas.md
Model cagirmaz, para ve ekran karti yok. Girdi: koşu klasorleri (kosu_meta.json, cagri_s3.jsonl, *.olcum.json) + catal_s3_<etiket>.jsonl.
OLCULER (birincil kume: durumu "tamam" olan koşular; kesilen koşular ayri satir):
  1. Plan degisim payi U vs G (= 1 - israr) · israr AUC (U yuksek) + %95 aralik: sinif katmanli bootstrap 1000 (S1 / S2 ek ile ayni) ve tohum bootstrap 1000
  2. Karar sayisi tabani (T1'in toplam karar sayisi; olagan kolda emir yok): tek yonlu AUC (U cok) ve tohum disarida k-NN (k=5, z-olcek; celiski_s2.knn_puan)
     esli farklar israr - taban, ikisiyle de, ayni bootstrap orneklerinde, %95 aralik
  3. 7B ile yan yana: ayni tohumlarda S2 catali (DU = U1, DG = G; emirden onceki ilk 3 "git X") ve S2 kol D AUC'si (olcum_celiski_s2_13kas.json)
  4. Meta: koşu basina model, cagri, girdi / cikti jetonu, gecersiz JSON, cikti payinda kesilme, hata, maliyet, sure; seed yok
  5. Kesilme: tur basina; oran farki > ,20 ise "kesilme secilimi olasi" notu
python -I olc_s3.py [--kosular kosular/s3_14kas] [--catal catal_s3_14kas.jsonl] [--cikti olcum_s3_14kas]"""
import argparse, collections, glob, importlib.util, json, os, random, statistics as st, sys

BU = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(BU); S2 = os.path.join(EP, "sprint_s2"); BOOT = 1000
sys.path.insert(0, BU); import s3_ortak as O  # noqa: E402
_s = importlib.util.spec_from_file_location("c2", os.path.join(S2, "celiski_s2.py")); C2 = importlib.util.module_from_spec(_s); _s.loader.exec_module(C2)
auc, knn = C2.auc, C2.knn_puan


def ara(v):
    v = sorted(x for x in v if x is not None); return [round(v[int(.025 * len(v))], 3), round(v[int(.975 * len(v)) - 1], 3)] if len(v) >= 100 else None


def oku_kosular(kok):
    V = []
    for kl in sorted(glob.glob(os.path.join(kok, "S?", "t*"))):
        if "_yarim_" in kl or not os.path.exists(os.path.join(kl, "kosu_meta.json")): continue
        m = json.load(open(os.path.join(kl, "kosu_meta.json"), encoding="utf-8")); C = [json.loads(x) for x in open(os.path.join(kl, "cagri_s3.jsonl"), encoding="utf-8") if x.strip()] if os.path.exists(os.path.join(kl, "cagri_s3.jsonl")) else []
        oj = glob.glob(os.path.join(kl, "*.olcum.json")); o = json.load(open(oj[0], encoding="utf-8")) if oj else {}
        V.append({"vaka": "%s_%d" % (m["kol"], m["tohum"]), "kol": m["kol"], "tohum": m["tohum"], "T1": m.get("T1"), "sinif": "U" if m.get("T1") == "U1" else "G", "durum": m.get("durum"),
                  "sahte": "SAHTE" in str(m.get("tasiyici")), "model": m.get("model"), "seed": m.get("seed"), "cagri": len(C), "girdi": sum(c["girdi"] for c in C), "cikti": sum(c["cikti"] for c in C),
                  "cikti_ort": round(st.mean(c["cikti"] for c in C), 1) if C else None, "gecersiz": sum(1 for c in C if c["gecersiz"]), "kesik": sum(1 for c in C if c["kesik"]),
                  "hata": sum(1 for c in C if c["hata"]), "maliyet": round(sum(c["maliyet"] for c in C), 4), "sure_sn": m.get("sure_sn"),
                  "karar_toplam": sum(1 for c in C if c["ajan"] == "T1" and c["mesajlar"][-1]["content"].startswith("Gözlem: ")),
                  "betim": {k: o.get(k) for k in ("is_basarisi", "zarar", "fark_edilmeme", "yakalama", "durdu", "tur", "takildi") if k in o}})
    return V


def main():
    p = argparse.ArgumentParser(); p.add_argument("--kosular", default="kosular/s3_14kas"); p.add_argument("--catal", default="catal_s3_14kas.jsonl"); p.add_argument("--cikti", default="olcum_s3_14kas")
    a = p.parse_args(); sys.stdout.reconfigure(encoding="utf-8")
    V = oku_kosular(os.path.join(BU, a.kosular)); CT = [json.loads(x) for x in open(os.path.join(BU, a.catal), encoding="utf-8") if x.strip()] if os.path.exists(os.path.join(BU, a.catal)) else []
    isr = collections.defaultdict(list); cat = collections.defaultdict(set)
    for r in CT:
        if r.get("hata") and not r.get("cevap"): continue
        e = O.json_ayikla(r.get("cevap")) or {}; isr[r["vaka"]].append(1 if (e.get("eylem") == "git" and e.get("hedef") == r["X"]) else 0); cat[r["vaka"]].add(r["cagri_n"])
    for v in V: v["israr"] = round(st.mean(isr[v["vaka"]]), 3) if isr[v["vaka"]] else None; v["catal_sayisi"] = len(cat[v["vaka"]]); v["catal_cevap"] = len(isr[v["vaka"]])
    R = {"betik": os.path.basename(__file__), "sahte_veri": any(v["sahte"] for v in V), "kosu": len(V), "vaka": V, "kume": {}}
    # 7B (S2) ayni tohumlar
    C7 = [json.loads(x) for x in open(os.path.join(S2, "celiski_s2_13kas.jsonl"), encoding="utf-8") if x.strip()]; i7 = collections.defaultdict(list)
    for r in C7: i7[r["vaka"]].append(0 if r["plan_degisti"] else 1)
    J7 = json.load(open(os.path.join(S2, "olcum_celiski_s2_13kas.json"), encoding="utf-8"))["kol"]["D"]
    def kume(ad, sec):
        L = [v for v in V if sec(v) and v["israr"] is not None]; Y = [1 if v["sinif"] == "U" else 0 for v in L]; T = [v["tohum"] for v in L]
        iu = [i for i, y in enumerate(Y) if y]; ig = [i for i, y in enumerate(Y) if not y]
        o = {"n_U": len(iu), "n_G": len(ig), "dislanan_israrsiz": sum(1 for v in V if sec(v) and v["israr"] is None)}
        if not iu or not ig: R["kume"][ad] = o; return
        P = {"israr": [v["israr"] for v in L], "karar_tek_yon": [v["karar_toplam"] for v in L]}; P["karar_knn"] = knn([[x] for x in P["karar_tek_yon"]], Y, T)
        A = lambda pp, u, g: None if pp is None else auc([pp[i] for i in u], [pp[i] for i in g])
        o.update({"israr_ort_U": round(st.mean(P["israr"][i] for i in iu), 3), "israr_ort_G": round(st.mean(P["israr"][i] for i in ig), 3),
                  "plan_degisim_U": round(1 - st.mean(P["israr"][i] for i in iu), 3), "plan_degisim_G": round(1 - st.mean(P["israr"][i] for i in ig), 3),
                  "auc": {n: (None if A(pp, iu, ig) is None else round(A(pp, iu, ig), 3)) for n, pp in P.items()}})
        rr = random.Random("s3-%s" % ad); ORN = [([rr.choice(iu) for _ in iu], [rr.choice(ig) for _ in ig]) for _ in range(BOOT)]
        o["israr_auc_ara_sinif"] = ara([A(P["israr"], u, g) for u, g in ORN])
        tl = sorted(set(T)); rt = random.Random("s3-tohum-%s" % ad); BT = []
        for _ in range(BOOT):
            ix = [i for t in [rt.choice(tl) for _ in tl] for i in range(len(L)) if T[i] == t]; BT.append(A(P["israr"], [i for i in ix if Y[i]], [i for i in ix if not Y[i]]))
        o["israr_auc_ara_tohum"] = ara(BT)
        o["fark"] = {}
        for tb in ("karar_tek_yon", "karar_knn"):
            if P[tb] is None: o["fark"]["israr - " + tb] = None; continue
            o["fark"]["israr - " + tb] = {"deger": round(A(P["israr"], iu, ig) - A(P[tb], iu, ig), 3), "ara": ara([A(P["israr"], u, g) - A(P[tb], u, g) for u, g in ORN])}
        R["kume"][ad] = o
    kume("birincil (tamam)", lambda v: v["durum"] == "tamam"); kume("kesilen dahil", lambda v: v["durum"] in ("tamam", "kesildi"))
    kes = {s_: (sum(1 for v in V if v["sinif"] == s_ and v["durum"] == "kesildi"), sum(1 for v in V if v["sinif"] == s_)) for s_ in ("U", "G")}
    oran = {s_: (k / n if n else None) for s_, (k, n) in kes.items()}
    R["kesilme"] = {"U": kes["U"], "G": kes["G"], "not": "kesilme secilimi olasi (oran farki > ,20)" if None not in oran.values() and abs(oran["U"] - oran["G"]) > .20 else None}
    R["yan_yana_7b"] = [{"tohum": t, "7B_U(DU)": round(st.mean(i7["DU_%d" % t]), 3) if i7["DU_%d" % t] else None, "7B_G(DG)": round(st.mean(i7["DG_%d" % t]), 3) if i7["DG_%d" % t] else None,
                         "397B_U(SU)": next((v["israr"] for v in V if v["vaka"] == "SU_%d" % t), None), "397B_G(SG)": next((v["israr"] for v in V if v["vaka"] == "SG_%d" % t), None)} for t in range(46, 61)]
    R["7b_auc_israr_kol_D"] = J7["auc_israr_U_yuksek"]; R["7b_kaynak"] = "sprint_s2/olcum_celiski_s2_13kas.json kol D"
    R["catal_meta"] = {"cagri": len(CT), "gecersiz": sum(1 for r in CT if r.get("gecersiz")), "kesik": sum(1 for r in CT if r.get("kesik")), "hata": sum(1 for r in CT if r.get("hata")),
                       "maliyet": round(sum(r.get("maliyet") or 0 for r in CT), 4), "istemde_yol_yok_eksik": sum(1 for r in CT if not r.get("istemde_yol_yok"))}
    R["harcama"] = {"kosu": round(sum(v["maliyet"] for v in V), 4), "catal": R["catal_meta"]["maliyet"]}; R["harcama"]["toplam"] = round(R["harcama"]["kosu"] + R["harcama"]["catal"], 4)
    json.dump(R, open(os.path.join(BU, a.cikti + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    f = lambda x: "yok" if x is None else str(x)
    md = ["# S3 · 397B ajan · olağan kol · ölçüm", "", ("**SAHTE VERİ: dil modeli yok, yalnız betik sınaması; sonuç model sonucu DEĞİLDİR.**" if R["sahte_veri"] else "Model qwen3.5-397b (Adaption), T 0,7, çıktı payı 8.000, seed YOK (koşular tekrarlanamaz)."),
          "Önkayıt `onkayit_sprint/ONKAYIT_S3_397b_ajan.md` (Yol 3: yalnız olağan kol), sapmalar `SAPMA_S3_14kas.md`. Betik `olc_s3.py`.", ""]
    for ad, o in R["kume"].items():
        md += ["## Küme: %s · n U %d, G %d (ısrarı olmayan, dışlanan: %d)" % (ad, o["n_U"], o["n_G"], o["dislanan_israrsiz"]), ""]
        if "auc" not in o: md += ["Bir türde vaka yok; hesaplanmadı.", ""]; continue
        md += ["- Israr ortalaması U %s, G %s · plan değişim payı U %s, G %s" % (o["israr_ort_U"], o["israr_ort_G"], o["plan_degisim_U"], o["plan_degisim_G"]),
               "- Israr AUC (U yüksek) %s · %%95 aralık sınıf katmanlı %s · tohum bootstrap %s" % (f(o["auc"]["israr"]), f(o["israr_auc_ara_sinif"]), f(o["israr_auc_ara_tohum"])),
               "- Karar sayısı tabanı (T1 toplam karar): tek yönlü %s · tohum dışarıda k-NN %s" % (f(o["auc"]["karar_tek_yon"]), f(o["auc"]["karar_knn"]))]
        for n, x in o["fark"].items(): md.append("- %s: %s" % (n, "yok" if x is None else "%s, %%95 aralık %s" % (x["deger"], x["ara"])))
        md.append("")
    md += ["## Kesilme (150 çağrı sınırı)", "", "- U %d / %d · G %d / %d%s" % (kes["U"][0], kes["U"][1], kes["G"][0], kes["G"][1], (" · " + R["kesilme"]["not"]) if R["kesilme"]["not"] else ""), "",
           "## 7B ile yan yana (aynı tohum = aynı başlangıç dünyası; model farklı)", "", "7B ısrar AUC (S2 kol D): %s · kaynak %s" % (f(round(R["7b_auc_israr_kol_D"], 3)), R["7b_kaynak"]), "",
           "| tohum | 7B U (DU) | 7B G (DG) | 397B U (SU) | 397B G (SG) |", "|---|---|---|---|---|"]
    for y in R["yan_yana_7b"]: md.append("| %d | %s | %s | %s | %s |" % (y["tohum"], f(y["7B_U(DU)"]), f(y["7B_G(DG)"]), f(y["397B_U(SU)"]), f(y["397B_G(SG)"])))
    md += ["", "## Koşular (meta)", "", "| vaka | T1 | durum | çağrı | girdi | çıktı | çıktı ort | geçersiz | kesik | hata | $ | sn | T1 karar | çatal | ısrar | betim |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for v in V: md.append("| %s | %s | %s | %d | %d | %d | %s | %d | %d | %d | %.4f | %s | %d | %d | %s | %s |" % (v["vaka"], v["T1"], v["durum"], v["cagri"], v["girdi"], v["cikti"], f(v["cikti_ort"]), v["gecersiz"], v["kesik"], v["hata"], v["maliyet"], f(v["sure_sn"]), v["karar_toplam"], v["catal_sayisi"], f(v["israr"]), json.dumps(v["betim"], ensure_ascii=False)))
    cm = R["catal_meta"]
    md += ["", "## Çatal ve harcama", "", "- Çatal: çağrı %d · geçersiz %d · kesik %d · hata %d · istemde 'yol yok' eksik %d · %.4f $" % (cm["cagri"], cm["gecersiz"], cm["kesik"], cm["hata"], cm["istemde_yol_yok_eksik"], cm["maliyet"]),
           "- Harcama (hesap, jeton x fiyat): koşular %.4f $ · çatal %.4f $ · toplam %.4f $" % (R["harcama"]["kosu"], R["harcama"]["catal"], R["harcama"]["toplam"])]
    open(os.path.join(BU, a.cikti + ".md"), "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")
    print("\n".join(md[:30]))


if __name__ == "__main__":
    main()
