# coding: utf-8
"""S2 pencere denetimi (EK, 12 Kas, mevcut veri, CPU, 0 $). Aktarim AU/AG kosularinda (tohum 31-45) tasiyicinin basarili anahtar_kullan
kararindan (sonraki gozlem K2) zarf teslimine ("kutuya" gozlemi) kadar verdigi karar sayisi, teslimi doguran karar dahil. Tur basina medyan, en az, en cok.
Girdi: ../aktarim/vakalar_aktarim.jsonl, ../aktarim/oynat/<klasor>/<kosu_id>.istem.jsonl. Cikti: pencere_denetimi_12kas.json. python -I pencere_denetimi_12kas.py"""
import collections, importlib.util, json, os, statistics as st, sys

H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H)
s = importlib.util.spec_from_file_location("y", os.path.join(EP, "yargic_k1.py")); y = importlib.util.module_from_spec(s); s.loader.exec_module(y)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    V = [json.loads(x) for x in open(os.path.join(EP, "aktarim", "vakalar_aktarim.jsonl"), encoding="utf-8") if x.strip()]
    out, detay = collections.defaultdict(list), []
    for v in V:
        if not v.get("ajan"): continue
        p = os.path.join(EP, "aktarim", "oynat", v["klasor"], v["kosu_id"] + ".istem.jsonl")
        R = sorted([d for d in (json.loads(l) for l in open(p, encoding="utf-8")) if d["ajan"] == v["ajan"] and d["cagri"] == 0], key=lambda d: d["kayit_adim"])
        G = [y.gozlem(d) or {} for d in R]; E = [y.cevap(d).get("eylem") for d in R]
        ak = next((i for i, e in enumerate(E[:-1]) if e == "anahtar_kullan" and G[i + 1].get("konum") == "K2"), None)
        ts = None if ak is None else next((j for j in range(ak + 1, len(G)) if "kutuya" in str(G[j].get("son", ""))), None)
        n = None if ts is None else ts - ak - 1
        out[v["sinif"]].append(n); detay.append({"kol": v["kol"], "tohum": v["tohum"], "sinif": v["sinif"], "karar": n, "sonraki_eylemler": E[ak + 1:ak + 7] if ak is not None else None})
    J = {"tur": {}, "detay": detay}
    for k, L in out.items():
        a = [x for x in L if x is not None]
        J["tur"][k] = {"tasiyici": len(L), "teslim": len(a), "medyan": st.median(a) if a else None, "en_az": min(a) if a else None, "en_cok": max(a) if a else None}
    json.dump(J, open(os.path.join(H, "pencere_denetimi_12kas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(J["tur"], ensure_ascii=False))


if __name__ == "__main__":
    main()
