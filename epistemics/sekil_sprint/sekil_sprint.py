# coding: utf-8
"""SPRINT RAPOR SEKILLERI · 14 Kas 2026 · Hikayeci · danisman IS EMRI 5 · para ve ekran karti yok.
Butun sayilar json dosyalarindan OKUNUR (elle yazilmaz); her sayinin kaynagi KAYNAK.md'ye yazilir.
Cikti (bu klasor): sekil1_auc.svg/.png (300 dpi), sekil2_hedef_anma.svg/.png, tablo1_s1_birincil.md/.csv, KAYNAK.md
python -I sekil_sprint.py"""
import csv, json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

BU = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(os.path.dirname(BU)); EP = os.path.join(SP, "oyun_alani_v4", "epistemik")
MAVI, TURUNCU, GRI = "#0072B2", "#E69F00", "#8C8C8C"           # Okabe-Ito: renk koru dostu iki renk + gri
plt.rcParams.update({"font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9, "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9, "font.family": ["Arial", "DejaVu Sans"], "svg.fonttype": "none"})
KAY = []


def oku(yol):
    return json.load(open(os.path.join(EP, yol), encoding="utf-8"))


def k(etiket, deger, dosya, alan):
    KAY.append((etiket, deger, dosya, alan)); return deger


def f3(x):
    return ("%.3f" % x).replace("0.", ".", 1) if x is not None and x >= 0 else ("%.3f" % x).replace("-0.", "−.", 1)


def sekil1():
    S1 = oku("sprint_s1/olcum_s1_13kas.json"); T = oku("tarama_11kas.json"); EK = oku("sprint_s2/olcum_celiski_ek_14kas.json"); S3 = oku("sprint_s3/olcum_s3_14kas.json")
    f1 = "epistemik/sprint_s1/olcum_s1_13kas.json"
    sol = []
    for kod, ad in (("A", "A: record + contradiction text"), ("Ai", "A + persistence count"), ("B0", "B0: A + full ledger"), ("C", "C: A + classifier probability"), ("F", "F: A + four labelled examples")):
        t = S1["kol"][kod]["satir"]["toplam"]; c = S1["kol"][kod]["tutarlilik"]
        sol.append(dict(ad=ad, auc=k("Ş1 sol %s AUC" % ad, t["auc"], f1, "kol.%s.satir.toplam.auc" % kod), ara=k("Ş1 sol %s %%95" % ad, t["ara"], f1, "kol.%s.satir.toplam.ara" % kod),
                        tut=k("Ş1 sol %s tutarlılık" % ad, c, f1, "kol.%s.tutarlilik" % kod), renk=MAVI, isaret="o"))
    tb = S1["taban"]["toplam"]
    sol.append(dict(ad="k-NN on ledger numbers", auc=k("Ş1 sol k-NN defter AUC", tb["knn"], f1, "taban.toplam.knn"), ara=None, tut=None, renk=TURUNCU, isaret="D"))
    sol.append(dict(ad="decision-count k-NN", auc=k("Ş1 sol karar sayısı k-NN AUC", tb["karar_sayisi_knn"], f1, "taban.toplam.karar_sayisi_knn"), ara=None, tut=None, renk=GRI, isaret="o"))
    tk = next(x for x in T["T2"] if "donuk gece + ikiz K0 + aktar" in x)
    sag = [dict(ad="7B, pre-sprint pooled", auc=k("Ş1 sağ havuz 7B AUC", T["T2"][tk]["auc"], "epistemik/tarama_11kas.json", "T2[\"%s\"].auc" % tk), ara=k("Ş1 sağ havuz 7B %95", T["T2"][tk]["ara"], "epistemik/tarama_11kas.json", "T2[\"%s\"].ara (küme katmanlı)" % tk), ks=None),
           dict(ad="7B, fresh seeds (D)", auc=k("Ş1 sağ S2 D AUC", EK["kol"]["D"]["auc"]["israr"], "epistemik/sprint_s2/olcum_celiski_ek_14kas.json", "kol.D.auc.israr"),
                ara=k("Ş1 sağ S2 D %95", EK["kol"]["D"]["israr_auc_ara"], "epistemik/sprint_s2/olcum_celiski_ek_14kas.json", "kol.D.israr_auc_ara (sınıf katmanlı)"),
                ks=k("Ş1 sağ S2 D karar k-NN", EK["kol"]["D"]["auc"]["karar_once_knn"], "epistemik/sprint_s2/olcum_celiski_ek_14kas.json", "kol.D.auc.karar_once_knn")),
           dict(ad="7B, same card, goal only (E)", auc=k("Ş1 sağ S2 E AUC", EK["kol"]["E"]["auc"]["israr"], "epistemik/sprint_s2/olcum_celiski_ek_14kas.json", "kol.E.auc.israr"),
                ara=k("Ş1 sağ S2 E %95", EK["kol"]["E"]["israr_auc_ara"], "epistemik/sprint_s2/olcum_celiski_ek_14kas.json", "kol.E.israr_auc_ara (sınıf katmanlı)"),
                ks=k("Ş1 sağ S2 E karar k-NN", EK["kol"]["E"]["auc"]["karar_once_knn"], "epistemik/sprint_s2/olcum_celiski_ek_14kas.json", "kol.E.auc.karar_once_knn")),
           dict(ad="397B, fresh seeds", auc=k("Ş1 sağ S3 AUC", S3["kume"]["birincil (tamam)"]["auc"]["israr"], "epistemik/sprint_s3/olcum_s3_14kas.json", "kume[\"birincil (tamam)\"].auc.israr"),
                ara=k("Ş1 sağ S3 %95", S3["kume"]["birincil (tamam)"]["israr_auc_ara_sinif"], "epistemik/sprint_s3/olcum_s3_14kas.json", "kume[\"birincil (tamam)\"].israr_auc_ara_sinif (sınıf katmanlı)"),
                ks=k("Ş1 sağ S3 karar k-NN", S3["kume"]["birincil (tamam)"]["auc"]["karar_knn"], "epistemik/sprint_s3/olcum_s3_14kas.json", "kume[\"birincil (tamam)\"].auc.karar_knn"))]
    KAY.append(("Ş1 sağ havuz 7B karar k-NN", None, "epistemik/tarama_11kas.json", "YOK: T2 / T3'te havuz için karar sayısı k-NN değeri yok; gri nokta çizilmedi"))
    W, H = 6.3, 3.35; fig = plt.figure(figsize=(W, H)); ah, ab = 2.0 / H, .82 / H
    a1 = fig.add_axes([1.80 / W, ab, .82 / W, ah]); a2 = fig.add_axes([5.12 / W, ab, .82 / W, ah], sharex=a1)
    for ax, L in ((a1, sol), (a2, sag)):
        ax.axvline(.5, ls="--", lw=.8, color=GRI, zorder=0); ax.set_xlim(.3, 1.0); ax.set_ylim(len(L) - .5, -.5); ax.set_xticks([.3, .5, .7, .9]); ax.set_xticklabels([".3", ".5", ".7", ".9"])
        ax.set_yticks(range(len(L))); ax.set_yticklabels([r["ad"] for r in L]); ax.set_xlabel("AUC (sleeper vs honest)"); ax.tick_params(axis="y", length=2, pad=2)
        for sp in ("top", "right"): ax.spines[sp].set_visible(False)
        ax.text(1.05, 1.0, "AUC", fontsize=9, ha="left", va="bottom", color="#333333", transform=ax.transAxes)
    a1.text(1.40, 1.0, "cons.", fontsize=9, ha="left", va="bottom", color="#333333", transform=a1.transAxes)
    fig.text(.01, (ab + ah) + .09, "Judge (397B), 98 moments", fontsize=9, fontweight="bold", ha="left"); fig.text(3.45 / W, (ab + ah) + .09, "Persistence under contradiction", fontsize=9, fontweight="bold", ha="left")
    yx = a1.get_yaxis_transform()
    for i, r in enumerate(sol):
        if r["ara"]: a1.plot(r["ara"], [i, i], color=r["renk"], lw=1.4)
        a1.plot(r["auc"], i, marker=r["isaret"], color=r["renk"], ms=5.5 if r["isaret"] == "D" else 5, zorder=3)
        a1.text(1.04, i, f3(r["auc"]), fontsize=9, va="center", ha="left", color="#333333", transform=yx)
        if r["tut"] is not None: a1.text(1.40, i, f3(r["tut"]), fontsize=9, va="center", ha="left", color="#333333", transform=yx)
    yx2 = a2.get_yaxis_transform()
    for i, r in enumerate(sag):
        a2.plot(r["ara"], [i, i], color=MAVI, lw=1.4); a2.plot(r["auc"], i, "o", color=MAVI, ms=5, zorder=3)
        if r["ks"] is not None: a2.plot(r["ks"], i, "o", color=GRI, ms=4.5, zorder=3)
        a2.text(1.04, i, f3(r["auc"]), fontsize=9, va="center", ha="left", color="#333333", transform=yx2)
    fig.text(.01, .085, "Lines: 95% intervals. Orange diamond and grey dots: baselines without intervals; grey = decision-count k-NN.", fontsize=9, ha="left", color="#333333")
    fig.text(.01, .02, "Right: no decision-count value for the pre-sprint pooled row. D and E share sleeper runs.", fontsize=9, ha="left", color="#333333")
    for uz in ("svg", "png"): fig.savefig(os.path.join(BU, "sekil1_auc.%s" % uz), dpi=300)
    plt.close(fig)


def sekil2():
    S4 = oku("sprint_s4/olcum_s4_14kas.json"); f4 = "epistemik/sprint_s4/olcum_s4_14kas.json"
    fig, ax = plt.subplots(figsize=(6.3, 3.0)); g = .17; ad = [("U", "Sa", "Sleeper, neutral"), ("G", "Sa", "Honest, neutral"), ("U", "Sb", "Sleeper, direct"), ("G", "Sb", "Honest, direct")]
    XS = {"397B": [-1.5 * g, -.5 * g, .5 * g, 1.5 * g], "7B": [1 - 1.75 * g, 1 - .25 * g, 1 + .75 * g, 1 + 1.75 * g]}
    for gi, m in enumerate(("397B", "7B")):
        for bi, (t, s, et) in enumerate(ad):
            sat = S4["satir"]["%s %s %s" % (m, t, s)]; v = k("Ş2 %s %s %s oran" % (m, t, s), sat["anma_an"], f4, "satir[\"%s %s %s\"].anma_an" % (m, t, s)); r = k("Ş2 %s %s %s %%95" % (m, t, s), sat["ara"], f4, "satir[\"%s %s %s\"].ara" % (m, t, s))
            x = XS[m][bi]; renk = MAVI if t == "U" else TURUNCU
            ax.bar(x, v, g * .92, color=renk if s == "Sa" else "white", edgecolor=renk, hatch=None if s == "Sa" else "////", lw=1, label=et if gi == 0 else None)
            ax.errorbar(x, v, yerr=[[v - r[0]], [r[1] - v]], fmt="none", ecolor="#333333", lw=.9, capsize=2)
            ax.text(x, max(v, r[1]) + .02, f3(v) if v > 0 else "0", ha="center", va="bottom", fontsize=9, color="#333333")
    sat = S4["satir"]["7B U Sa (istemi birebir)"]; v = k("Ş2 7B U Sa birebir oran", sat["anma_an"], f4, "satir[\"7B U Sa (istemi birebir)\"].anma_an"); r = k("Ş2 7B U Sa birebir %95", sat["ara"], f4, "satir[\"7B U Sa (istemi birebir)\"].ara")
    n = k("Ş2 7B U Sa birebir an sayısı", sat["an"], f4, "satir[\"7B U Sa (istemi birebir)\"].an")
    x = 1 - 1.0 * g; ax.bar(x, v, g * .42, color=MAVI, alpha=.55, edgecolor=MAVI, lw=.8)
    ax.errorbar(x, v, yerr=[[v - r[0]], [r[1] - v]], fmt="none", ecolor="#333333", lw=.9, capsize=2)
    ax.text(x, r[1] + .02, f3(v), ha="center", va="bottom", fontsize=9, color="#333333")
    ax.text(x, -.03, "exact prompts" + chr(10) + "(n=%d)" % n, ha="center", va="top", fontsize=9, color="#333333", clip_on=False)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["397B", "7B"]); ax.tick_params(axis="x", pad=26, length=0); ax.set_ylim(0, 1.08); ax.set_ylabel("Goal mentioned (share of moments)")
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.legend(frameon=False, loc="upper right", fontsize=9); fig.subplots_adjust(left=.11, right=.99, top=.97, bottom=.2)
    for uz in ("svg", "png"): fig.savefig(os.path.join(BU, "sekil2_hedef_anma.%s" % uz), dpi=300)
    plt.close(fig)


def tablo1():
    S1 = oku("sprint_s1/olcum_s1_13kas.json"); f1 = "epistemik/sprint_s1/olcum_s1_13kas.json"; OKU = {"ayrılmadı": "interval includes 0", "0'ın üstünde": "above 0", "0'ın altında": "below 0"}; R = []
    for ad, v in S1["birincil"]["fark"].items():
        R.append(["difference", ad, "%.3f" % v["fark"], "[%.3f, %.3f]" % tuple(v["ara"]), OKU.get(v["okuma"], v["okuma"]), "birincil.fark.%s" % ad])
    for ad, v in S1["birincil"]["tutarlilik_080"].items():
        R.append(["consistency (3 repeats)", ad, "%.3f" % v["tutarlilik"], "", "≥ .80" if v["karar"] else "< .80", "birincil.tutarlilik_080.%s" % ad])
    assert len(R) == S1["sayim"]["birincil"], (len(R), S1["sayim"]["birincil"])
    with open(os.path.join(BU, "tablo1_s1_birincil.csv"), "w", encoding="utf-8", newline="") as fp:
        w = csv.writer(fp); w.writerow(["type", "comparison", "value", "95% interval", "reading", "source field (%s)" % f1]); w.writerows(R)
    md = ["| type | comparison | value | 95% interval | reading |", "|---|---|---|---|---|"] + ["| %s | %s | %s | %s | %s |" % tuple(r[:5]) for r in R]
    open(os.path.join(BU, "tablo1_s1_birincil.md"), "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n\nSource: `%s`, fields `birincil.fark.*` and `birincil.tutarlilik_080.*` (%d pre-registered primary comparisons, `sayim.birincil`).\n" % (f1, len(R)))
    for r in R: KAY.append(("Tablo 1 %s %s" % (r[0], r[1]), r[2], f1, r[5]))


def main():
    sys.stdout.reconfigure(encoding="utf-8"); sekil1(); sekil2(); tablo1()
    md = ["# KAYNAK · sprint şekilleri · 14 Kas 2026", "", "Betik `sekil_sprint.py`; bütün sayılar json'dan okundu, elle yazılmadı. Yollar `Desktop/sprint/oyun_alani_v4/` köküne göre.", "", "| şekildeki öğe | değer | dosya | json alanı |", "|---|---|---|---|"]
    for e, d, fl, al in KAY: md.append("| %s | %s | `%s` | `%s` |" % (e, ("[%.3f, %.3f]" % tuple(d)) if isinstance(d, list) else ("%.3f" % d if isinstance(d, float) else d), fl, al))
    open(os.path.join(BU, "KAYNAK.md"), "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n"); print("satir", len(KAY))


main()
