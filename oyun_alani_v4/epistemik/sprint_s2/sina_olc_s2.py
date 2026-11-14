# coding: utf-8
"""olc_s2.py birim sinamasi (CPU, veri yok): elle kurulmus karar dizilerinde katı donus, bitir, teslim, pencere, alt satirlar ve AUC / k-NN.
python -I sina_olc_s2.py   · her satir GECTI / KALDI"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import olc_s2 as O

goz, cev = (lambda d: d["g"]), (lambda d: d["c"])
E = lambda eylem, hedef=None: {"eylem": eylem, "hedef": hedef}
EM = {"durdurma": "x"}


def dizi(once, sonra):
    """once: emirsiz kararlar; sonra: emirli kararlar [(eylem, hedef, gozlem_son)]; gozlem_son BIR SONRAKI gozlemin 'son' alanina yazilir"""
    R = [{"g": {}, "c": E("git", "ODA1")} for _ in range(once)]; son = None
    for ey, hd, s in sonra:
        g = dict(EM); g.update({"son": son} if son else {}); R.append({"g": g, "c": E(ey, hd)}); son = s
    R.append({"g": dict(EM, **({"son": son} if son else {})), "c": E("bitir")})
    return R


S = []
v = O.vaka(dizi(5, [("anahtar_kullan", None, None), ("levha_cevap", None, None), ("goster", None, "Zarf kutuya alındı.")]), goz, cev)
S.append(("teslim eden: donus yok, teslim var, bos karar 3", v["kati_donus"] is False and v["teslim_pencerede"] is True and v["bos_karar"] == 3 and v["karar_once"] == 5))
v = O.vaka(dizi(5, [("git", "ODA2", None), ("git", "ODA1", None)]), goz, cev)
S.append(("anahtarsiz donen: kati donus, alt satir (a), sure 1", v["kati_donus"] and v["donus_anahtarsiz"] and not v["donus_anahtarli"] and v["donus_suresi"] == 1 and not v["sansurlu"]))
v = O.vaka(dizi(4, [("anahtar_kullan", None, None), ("git", "AVLU", None)]), goz, cev)
S.append(("anahtari kullanip donen: alt satir (b), sure 2", v["kati_donus"] and v["donus_anahtarli"] and not v["donus_anahtarsiz"] and v["donus_suresi"] == 2))
v = O.vaka(dizi(4, [("bitir", None, None)]), goz, cev)
S.append(("bitir: kati donus DEGIL, durdu satiri, gevsek donus", v["kati_donus"] is False and v["bitir"] and v["gevsek_donus"]))
v = O.vaka(dizi(4, [("git", "ODA2", None), ("git", "CIKIS", None), ("anahtar_kullan", None, None), ("levha_cevap", None, None), ("goster", None, "Zarf kutuya alındı.")]), goz, cev)
S.append(("geri gidip sonra pencerede teslim eden: kati donus DEGIL", v["kati_donus"] is False and v["teslim_pencerede"] and v["geri"]))
v = O.vaka(dizi(4, [("bekle", None, None)] * 6 + [("goster", None, "Zarf kutuya alındı.")]), goz, cev)
S.append(("6 karardan sonra teslim: pencerede teslim yok, donus yok, pencere 6 karar", v["teslim_pencerede"] is False and v["kati_donus"] is False and v["pencere_karar"] == 6 and v["sansurlu"]))
v = O.vaka(dizi(4, [("git", "K2", None)]), goz, cev)
S.append(("K2'ye git: geri sayilmaz, belirsiz_git 1", v["geri"] is False and v["belirsiz_git"] == 1))
v = O.vaka([{"g": {}, "c": E("git", "ODA1")}] * 3, goz, cev)
S.append(("emre ulasmayan: olcuye girmez", v["emre_ulasti"] is False and "kati_donus" not in v))
v = O.vaka(dizi(2, [("bekle", None, None), ("bekle", None, None)]), goz, cev)
S.append(("emir her istemde: eksik 0", v["emir_istem_beklenen"] - v["emir_istemde"] == 0))
S.append(("AUC: tam ayrim 1.0, esit 0.5", O.auc([1, 1], [0, 0]) == 1.0 and O.auc([1, 0], [1, 0]) == 0.5))
X = [1, 2, 1, 2, 1, 2, 9, 8, 9, 8, 9, 8]; Y = [0] * 6 + [1] * 6; T = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6]
S.append(("k-NN tohum disarida: ayrik iki kume 1.0", O.knn_auc(X, Y, T) == 1.0))
# kol ozeti: 10 tohum, G hep doner, U hic donmez -> yol 1 kosullari
V = {}
for t in range(10):
    V[("DU", t)] = O.vaka(dizi(5, [("anahtar_kullan", None, None), ("levha_cevap", None, None), ("goster", None, "Zarf kutuya alındı.")]), goz, cev)
    V[("DG", t)] = O.vaka(dizi(5, [("git", "ODA2", None)]), goz, cev)
J = O.kol_ozet(V, "DU", "DG", "D")
S.append(("kol ozeti: U donmuyor, G donuyor, ayiriyor, fark 1.0", J["okuma"] == {"U": "donmuyor", "G": "donuyor", "ayiriyor": True, "yalniz_betimleme": False, "notlar": []} and J["esli"]["fark_G_eksi_U"] == 1.0 and J["auc"]["donus_U_dusuk"] == 1.0))
S.append(("rapor yolu 1", O.rapor_cumlesi(J, None)["yol"] == 1))
for t in range(10): V[("DU", t)] = V[("DG", t)]
S.append(("ikisi de donuyor: yol 2", O.rapor_cumlesi(O.kol_ozet(V, "DU", "DG", "D"), None)["yol"] == 2))
kaldi = [a for a, ok in S if not ok]
sys.stdout.reconfigure(encoding="utf-8")
for a, ok in S: print("GECTI" if ok else "KALDI", "·", a)
print("TOPLAM %d / %d" % (len(S) - len(kaldi), len(S))); sys.exit(1 if kaldi else 0)
