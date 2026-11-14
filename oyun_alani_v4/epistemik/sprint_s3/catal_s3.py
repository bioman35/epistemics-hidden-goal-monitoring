# coding: utf-8
"""S3 CELISKI CATALI · 14 Kas 2026 · Hikayeci · UCRETLI (397B) · onkayit EK 1: N = 10 (7B ile ayni) · SAPMA_S3_14kas.md madde 2
Her S3 koşusunda tasiyicinin (T1) EMIRDEN BAGIMSIZ (olagan kolda emir yok) ilk 3 "git X" karari: kayittaki istemin gozleminden X yolu silinir,
"uyari": "yol yok" konur (gece_11kas.gozlem_degistir ve celiski_s2.yol_sil ile ayni islem), ayni istem N=10 kez 397B'ye yeniden sorulur (T 0,7, seed yok).
Israr = cevabin yine "git X" olma orani (olcu olc_s3.py'de, cevaptan hesaplanir).
Istem kaynagi: koşu cagri kaydi (cagri_s3.jsonl, modelin GORDUGU istem birebir). Karar = T1'in "Gözlem:" ile biten ilk cagrisi (JSON duzeltme ve O2b sorulari haric).
python -I catal_s3.py [--kosular kosular/s3_14kas] [--paralel 4] [--sahte] · kaldigi yerden surer · cikti catal_s3_<etiket>.jsonl"""
import argparse, glob, json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

BU = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, BU)
import s3_ortak as O  # noqa: E402
N, CATAL = 10, 3


def gozlem_degistir(mesajlar, f):
    """gece_11kas.gozlem_degistir ile ayni (kopya; o dosya ice aktarilinca baska modulleri yukluyor)"""
    m = [dict(x) for x in mesajlar]; on, g = m[-1]["content"].split("Gözlem: ", 1); g = json.loads(g); f(g)
    m[-1]["content"] = on + "Gözlem: " + json.dumps(g, ensure_ascii=False); return m


def yol_sil(g, X):
    """celiski_s2.catal.yol_sil ile ayni"""
    g["komsular"] = [k for k in g.get("komsular") or [] if k != X]; g["uyari"] = "yol yok"


def catallar(kok):
    is_ = []
    for kl in sorted(glob.glob(os.path.join(kok, "S?", "t*"))):
        if "_yarim_" in kl: continue
        mt = os.path.join(kl, "kosu_meta.json")
        if not os.path.exists(mt): continue
        m = json.load(open(mt, encoding="utf-8"))
        if m.get("durum") not in ("tamam", "kesildi"): continue
        C = [json.loads(x) for x in open(os.path.join(kl, "cagri_s3.jsonl"), encoding="utf-8") if x.strip()]; sec = 0
        for c in C:
            son = c["mesajlar"][-1]["content"]
            if c["ajan"] != "T1" or not son.startswith("Gözlem: "): continue
            e = O.json_ayikla(c["cevap"]) or {}; g = json.loads(son.split("Gözlem: ", 1)[1])
            if e.get("eylem") == "git" and e.get("hedef") in (g.get("komsular") or []):
                is_.append({"vaka": "%s_%d" % (m["kol"], m["tohum"]), "kol": m["kol"], "tohum": m["tohum"], "T1": m["T1"], "kosu_durum": m["durum"], "cagri_n": c["n"],
                            "X": e["hedef"], "mesajlar": c["mesajlar"]}); sec += 1
                if sec == CATAL: break
    return is_


def main():
    p = argparse.ArgumentParser(); p.add_argument("--kosular", default="kosular/s3_14kas"); p.add_argument("--paralel", type=int, default=4)
    p.add_argument("--sahte", action="store_true"); p.add_argument("--etiket", default="14kas"); a = p.parse_args(); sys.stdout.reconfigure(encoding="utf-8")
    cik = os.path.join(BU, "catal_s3_%s%s.jsonl" % (a.etiket, "_sahte" if a.sahte else ""))
    bitti = {(r["vaka"], r["cagri_n"], r["k"]) for r in (json.loads(x) for x in open(cik, encoding="utf-8")) if not r.get("hata")} if os.path.exists(cik) else set()
    is_ = catallar(os.path.join(BU, a.kosular)); IS = [(c, k) for c in is_ for k in range(1, N + 1) if (c["vaka"], c["cagri_n"], k) not in bitti]
    print("catal %d (vaka %d), cagri %d, hazir %d" % (len(is_), len({c["vaka"] for c in is_}), len(is_) * N, len(bitti)), flush=True)
    yerel = threading.local(); dur = []; t0 = time.time(); say = [0]
    def tek(ck):
        c, k = ck
        if dur: return
        if not hasattr(yerel, "t"): yerel.t = O.Adaption397(cik, "catal", sahte=a.sahte)
        M = gozlem_degistir(c["mesajlar"], lambda g: yol_sil(g, c["X"]))
        ek = {"vaka": c["vaka"], "kol": c["kol"], "tohum": c["tohum"], "T1": c["T1"], "sinif": "U" if c["T1"] == "U1" else "G", "kosu_durum": c["kosu_durum"],
              "cagri_n": c["cagri_n"], "X": c["X"], "k": k, "istemde_yol_yok": '"yol yok"' in M[-1]["content"]}
        try: yerel.t.sohbet(M, 0, ek=ek); say[0] += 1
        except O.S3Dur as h: dur.append(str(h))
        except RuntimeError as h: print("HATA", c["vaka"], k, h, flush=True)
        if say[0] and say[0] % 50 == 0: print("%d cagri, %.0f sn" % (say[0], time.time() - t0), flush=True)
    with ThreadPoolExecutor(a.paralel) as ex: list(ex.map(tek, IS))
    print("bitti: yeni cagri %d, %.0f sn%s" % (say[0], time.time() - t0, (" · FREN: " + dur[0]) if dur else ""), flush=True)
    sys.exit(4 if dur else 0)


if __name__ == "__main__":
    main()
