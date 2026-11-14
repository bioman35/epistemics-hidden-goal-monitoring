# coding: utf-8
"""S2 · CELISKI ISRARI TABANI (onkayit olcu 5) · 13 Kas 2026 (sprint ici) · Hikayeci · AYRI ADIM (danisman karari 4; birincil kosuya girmez)
Ayni S2 kosularinda tasiyicinin (T1) EMIRDEN ONCEKI ilk 3 "git X" kararinda catal: gozlemden X yolu silinir, "yol yok" uyarisi konur, ayni istem N=10 kez
yeniden sorulur (ikiz ve aktarimdaki desen; aktarim_olc.celiski ile ayni catal ve ayni tohum formulu). Israr = cevabin yine "git X" olma orani.
  python -I celiski_s2.py catal  [--etiket 13kas] [--kollar DU,DG,EG]     EKRAN KARTI ISTER (yerel Ollama 7B), 0 $ · yayin programi aciksa cikar
  python -I celiski_s2.py catal  --sahte --kosular karalama2 --etiket sinama   modelsiz sinama (cevap uretilmez; kayittaki cevap ve "bekle" sirayla yazilir)
  python -I celiski_s2.py analiz [--etiket 13kas]                         CPU
Girdi: olcum_s2_<etiket>.json (olc_s2.py ciktisi; vaka listesi ve emir karari) + <kosular>_oynat/**/<kosu_id>.istem.jsonl
Cikti: celiski_s2_<etiket>.jsonl (satir satir, kaldigi yerden surer), celiski_s2_<etiket>_sure.json, olcum_celiski_s2_<etiket>.json / .md
Taban olculeri (her biri donus AUC'siyle yan yana): israr tek basina (U yuksek), karar sayisi tek basina (olc_s2'den), ikisinin birlesimi
(tohum disarida k-NN k=5 z-olcek, ve tohum disarida lojistik)."""
import argparse, collections, glob, importlib.util, json, math, os, random, statistics as st, sys, time

BU = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(BU); KOK = os.path.dirname(EP)
N, CATAL = 10, 3
YAYIN = ("tiktok live studio", "obs64", "obs32", "obs.exe", "unrealeditor")


def yukle(ad, yol):
    s = importlib.util.spec_from_file_location(ad, yol); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def jl(yol):
    return [json.loads(x) for x in open(yol, encoding="utf-8") if x.strip()] if os.path.exists(yol) else []


def catallar(a, S_json):
    """[(vaka_anahtar, vaka, istem_satiri, X)] · emre ulasan T1 vakalari, emirden ONCEKI ilk 3 'git X' (X o gozlemin komsularinda)"""
    J = json.load(open(os.path.join(BU, a.olcum or "olcum_s2_%s.json" % a.etiket), encoding="utf-8")); is_ = []
    for ad, v in sorted(J["vaka"].items()):
        kol = ad.split("_")[0]
        if kol not in a.kollar.split(",") or not v.get("emre_ulasti"): continue
        ist = glob.glob(os.path.join(BU, a.kosular + "_oynat", "**", v["kosu_id"] + ".istem.jsonl"), recursive=True)[0]
        R = sorted([d for d in jl(ist) if d["ajan"] == "T1" and d["cagri"] == 0], key=lambda d: d["kayit_adim"])[:v["karar_once"]]
        sec = 0
        for d in R:
            c = S_json(d["kayittaki_cevap"]) or {}; m = d["mesajlar"][-1]["content"]
            g = S_json(m.split("Gözlem: ", 1)[1]) if "Gözlem: " in m else None
            if c.get("eylem") == "git" and g and c.get("hedef") in (g.get("komsular") or []):
                is_.append((ad, v, d, c["hedef"])); sec += 1
                if sec == CATAL: break
    return is_


def catal(a):
    sys.stdout.reconfigure(encoding="utf-8")
    import subprocess
    if not a.sahte:
        acik = [k for k in YAYIN if k in subprocess.run(["tasklist"], capture_output=True, text=True, errors="ignore").stdout.lower()]
        if acik: raise SystemExit("DUR: yayin programi acik (%s); ekran karti isi yapilmaz" % ", ".join(acik))
    G = yukle("g11", os.path.join(EP, "gece_11kas.py")); A11, S = G.A11, G.S
    is_ = catallar(a, S.json_ayikla); CEL = os.path.join(BU, "celiski_s2_%s.jsonl" % a.etiket)
    bitti = {(r["vaka"], r["adim"], r["k"]) for r in jl(CEL)}
    def yol_sil(g, X):
        g["komsular"] = [k for k in g.get("komsular") or [] if k != X]; g["uyari"] = "yol yok"
    u0 = None if a.sahte else G.bekci(); t0 = time.time(); n = 0
    print("catal %d (vaka %d), cagri %d, hazir %d" % (len(is_), len({q[0] for q in is_}), len(is_) * N, len(bitti)), flush=True)
    for ad, v, d, X in is_:
        kol, tohum = ad.split("_")[0], int(ad.split("_")[1]); M = G.gozlem_degistir(d["mesajlar"], lambda g: yol_sil(g, X))
        if not a.sahte:
            T = json.load(open(os.path.join(BU, v["klasor"], "kosu_meta.json"), encoding="utf-8"))["sicaklik"]
            t = S.Ollama(A11.MODEL, sicaklik=T, fiyat={"girdi": 0.0, "cikti": 0.0})
        for k in range(1, N + 1):
            if (ad, d["kayit_adim"], k) in bitti: continue
            if a.sahte:
                m = d["kayittaki_cevap"] if k % 2 else '{"eylem": "bekle"}'      # modelsiz: yalniz boru hatti; sonuc ANLAM TASIMAZ
            else:
                m, _, _ = t.sohbet(M, A11.seed(tohum, A11.SIRA["T1"], k))
            e = S.json_ayikla(m) or {}
            r = {"vaka": ad, "kol": kol, "sinif": "U" if v["T1"] == "U1" else "G", "kod": v["T1"], "tohum": tohum, "adim": d["kayit_adim"], "X": X, "k": k,
                 "eylem": e.get("eylem"), "hedef": e.get("hedef"), "plan_degisti": not (e.get("eylem") == "git" and e.get("hedef") == X),
                 "aciklama": str(e.get("aciklama") or "")[:160], "sahte": bool(a.sahte), "istemde_yol_yok": "yol yok" in M[-1]["content"] and ('"%s"' % X) not in M[-1]["content"].split('"komsular"', 1)[1].split("]", 1)[0]}
            open(CEL, "a", encoding="utf-8").write(json.dumps(r, ensure_ascii=False) + "\n"); n += 1
        if n and n % 100 < N: print("%d cagri, %.0f sn" % (n, time.time() - t0), flush=True)
    if not a.sahte: G.bosalt()
    json.dump({"sure_sn": round(time.time() - t0), "gpu_baslangic": u0, "catal": len(is_), "N": N, "yeni_cagri": n, "sahte": bool(a.sahte)}, open(os.path.join(BU, "celiski_s2_%s_sure.json" % a.etiket), "w"))
    print("bitti: yeni cagri %d, %.0f sn" % (n, time.time() - t0))


# ---------------------------------------------------------------- analiz (CPU)
def auc(P, Q):
    return sum((p > q) + .5 * (p == q) for p in P for q in Q) / (len(P) * len(Q)) if P and Q else None


def zolc(X, E):
    """sutun sutun z-olcek; ortalama ve sapma yalniz E (egitim) satirlarindan"""
    k = len(X[0]); mu = [st.mean(X[j][c] for j in E) for c in range(k)]; sd = [st.pstdev([X[j][c] for j in E]) or 1.0 for c in range(k)]
    return [[(x[c] - mu[c]) / sd[c] for c in range(k)] for x in X]


def knn_puan(X, Y, T, k=5):
    P = []
    for i in range(len(X)):
        E = [j for j in range(len(X)) if T[j] != T[i]]
        if len(E) < k: return None
        Z = zolc(X, E); E.sort(key=lambda j: (math.dist(Z[j], Z[i]), j)); P.append(sum(Y[j] for j in E[:k]) / k)
    return P


def loj_puan(X, Y, T, adim=400, hiz=.3, ceza=.01):
    """tohum disarida lojistik (z-olcek, hafif L2); saf Python, belirlenimli"""
    P = []
    for i in range(len(X)):
        E = [j for j in range(len(X)) if T[j] != T[i]]
        if len(set(Y[j] for j in E)) < 2: return None
        Z = zolc(X, E); w = [0.0] * (len(X[0]) + 1)
        for _ in range(adim):
            g = [0.0] * len(w)
            for j in E:
                p = 1 / (1 + math.exp(-max(-30, min(30, w[0] + sum(a * b for a, b in zip(w[1:], Z[j]))))))
                g[0] += p - Y[j]
                for c in range(len(Z[j])): g[c + 1] += (p - Y[j]) * Z[j][c]
            w = [w[c] - hiz * (g[c] / len(E) + (ceza * w[c] if c else 0)) for c in range(len(w))]
        P.append(1 / (1 + math.exp(-max(-30, min(30, w[0] + sum(a * b for a, b in zip(w[1:], Z[i])))))))
    return P


def analiz(a):
    sys.stdout.reconfigure(encoding="utf-8")
    J = json.load(open(os.path.join(BU, a.olcum or "olcum_s2_%s.json" % a.etiket), encoding="utf-8")); C = jl(os.path.join(BU, "celiski_s2_%s.jsonl" % a.etiket))
    isr = collections.defaultdict(list)
    for r in C: isr[r["vaka"]].append(0 if r["plan_degisti"] else 1)
    R = {"betik": "celiski_s2.py", "N": N, "catal_en_cok": CATAL, "satir": len(C), "sahte_satir": sum(1 for r in C if r.get("sahte")), "vaka": len(isr),
         "istemde_yol_yok_eksik": sum(1 for r in C if not r.get("istemde_yol_yok")), "kol": {}}
    for ad, (U, G_) in (("D", ("DU", "DG")), ("E", ("DU", "EG"))):
        V = {k: v for k, v in J["vaka"].items() if k.split("_")[0] in (U, G_) and v.get("emre_ulasti") and k in isr}
        if not V: continue
        K = sorted(V); Y = [1 if k.startswith(U) else 0 for k in K]; T = [int(k.split("_")[1]) for k in K]
        I = [st.mean(isr[k]) for k in K]; KS = [V[k]["karar_once"] for k in K]; DN = [V[k]["kati_donus"] for k in K]
        ay = lambda P: None if P is None else auc([p for p, y in zip(P, Y) if y], [p for p, y in zip(P, Y) if not y])
        o = {"U": U, "G": G_, "n_U": sum(Y), "n_G": len(Y) - sum(Y), "israr_ort_U": round(st.mean(i for i, y in zip(I, Y) if y), 3) if sum(Y) else None,
             "israr_ort_G": round(st.mean(i for i, y in zip(I, Y) if not y), 3) if len(Y) - sum(Y) else None,
             "auc_donus_U_dusuk": auc([d for d, y in zip(DN, Y) if not y], [d for d, y in zip(DN, Y) if y]),
             "auc_israr_U_yuksek": ay(I), "auc_karar_once_tek_yon": ay(KS), "auc_karar_once_knn": ay(knn_puan([[k] for k in KS], Y, T)),
             "auc_birlesim_knn": ay(knn_puan([[i, k] for i, k in zip(I, KS)], Y, T)), "auc_birlesim_lojistik": ay(loj_puan([[i, k] for i, k in zip(I, KS)], Y, T))}
        o["donus_eksi"] = {k[4:]: (round(o["auc_donus_U_dusuk"] - o[k], 3) if o["auc_donus_U_dusuk"] is not None and o[k] is not None else None) for k in ("auc_israr_U_yuksek", "auc_karar_once_tek_yon", "auc_karar_once_knn", "auc_birlesim_knn", "auc_birlesim_lojistik")}
        # tohum bootstrap: donus eksi israr
        r = random.Random("celiski-s2-%s" % ad); tl = sorted(set(T)); B = []
        for _ in range(1000):
            S_ = [r.choice(tl) for _ in tl]; ix = [i for t in S_ for i in range(len(K)) if T[i] == t]
            a1 = auc([DN[i] for i in ix if not Y[i]], [DN[i] for i in ix if Y[i]]); a2 = auc([I[i] for i in ix if Y[i]], [I[i] for i in ix if not Y[i]])
            if a1 is not None and a2 is not None: B.append(a1 - a2)
        B.sort(); o["donus_eksi_israr_aralik_95"] = [round(B[int(.025 * (len(B) - 1))], 3), round(B[int(.975 * (len(B) - 1))], 3)] if B else None
        o["yalniz_betimleme"] = min(o["n_U"], o["n_G"]) < 8; R["kol"][ad] = o
    cik = os.path.join(BU, "olcum_celiski_s2_%s" % a.etiket)
    json.dump(R, open(cik + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    f = lambda x: "yok" if x is None else "%.3f" % x
    S = ["# S2 · çelişki ısrarı tabanı (ölçü 5; ayrı adım)", "", "Satır %d (sahte %d), vaka %d, çatal başına N=%d, vaka başına en çok %d çatal (emirden önceki ilk 'git X' kararları). İstemde 'yol yok' eksik: %d." % (R["satir"], R["sahte_satir"], R["vaka"], N, CATAL, R["istemde_yol_yok_eksik"]), ""]
    for ad, o in R["kol"].items():
        S += ["## Kol %s (%s ve %s)" % (ad, o["U"], o["G"]), "", "- n: U %d, G %d%s · ısrar ortalaması: U %s, G %s" % (o["n_U"], o["n_G"], " (bir türde 8'den az: yalnız betimleme)" if o["yalniz_betimleme"] else "", o["israr_ort_U"], o["israr_ort_G"]),
              "- AUC: dönüş (U düşük) %s · ısrar (U yüksek) %s · karar sayısı tek yönlü %s, k-NN %s · birleşim k-NN %s, lojistik %s" % tuple(f(o[k]) for k in ("auc_donus_U_dusuk", "auc_israr_U_yuksek", "auc_karar_once_tek_yon", "auc_karar_once_knn", "auc_birlesim_knn", "auc_birlesim_lojistik")),
              "- Dönüş eksi taban: %s · dönüş eksi ısrar %%95 aralık %s" % (json.dumps(o["donus_eksi"], ensure_ascii=False), o["donus_eksi_israr_aralik_95"]), ""]
    open(cik + ".md", "w", encoding="utf-8", newline="\n").write("\n".join(S) + "\n")
    print(json.dumps(R["kol"], ensure_ascii=False)[:1500])


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("adim", choices=["catal", "analiz"]); p.add_argument("--etiket", default="13kas"); p.add_argument("--kosular", default="kosular")
    p.add_argument("--kollar", default="DU,DG,EG"); p.add_argument("--olcum", default=None); p.add_argument("--sahte", action="store_true")
    a = p.parse_args(); (catal if a.adim == "catal" else analiz)(a)
