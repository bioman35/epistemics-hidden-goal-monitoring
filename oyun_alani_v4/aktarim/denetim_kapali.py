# coding: utf-8
"""AKTARIM DENETIMI (koşudan ÖNCE, CPU, model yok) · duyuru KAPALI dunya_aktarim.py donuk koşuları birebir yeniden oynatmalı
(kopya başka şey değiştirmedi). Ayrıca birim sınaması: duyuru AÇIK iken K2 parolayı ve levha kodunu kabul eder, başka kapı parolayı kabul etmez.
Çıktı: aktarim/denetim/ (istem + sinama) ve aktarim/denetim_kapali_11kas.json"""
import importlib.util, json, os, sys

AK = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(AK)
sys.path.insert(0, AK)
import kosu_aktarim as KA  # noqa: E402  (dunya -> dunya_aktarim)
DA = KA.DA
DA.DUYURU_ACIK = False
s = importlib.util.spec_from_file_location("yo", os.path.join(KOK, "epistemik", "yeniden_oynat.py")); Y = importlib.util.module_from_spec(s); s.loader.exec_module(Y)
assert Y.D is DA and Y.M.kos is DA.kos, "yeniden_oynat dunya kopyasini kullanmiyor"
sys.stdout.reconfigure(encoding="utf-8")
R = {"PUANSIZ": "koşu öncesi denetim", "dunya_aktarim_ozet": KA._ozet(os.path.join(AK, "dunya_aktarim.py")), "oynat": [], "birim": {}}
for klasor, kid in (("v4_g1_kosu2_t26_35_30eki", "v4_kosu2_O1_O2b_t31_U1"), ("v4_kosu2_28eki", "v4_kosu2_O1_O2b_t16_U1")):
    r = Y.oynat(os.path.join(KOK, "kosular", klasor, kid + ".jsonl"), os.path.join(AK, "denetim"))
    R["oynat"].append({"kosu": kid, "klasor": klasor, "birebir": r["birebir"], "satir": [r["satir_yeniden"], r["satir_kayit"]]})
    print("%s birebir %s satir %d/%d" % (kid, r["birebir"], r["satir_yeniden"], r["satir_kayit"]))
# birim: kapi karari
d = DA.Dunya.__new__(DA.Dunya)
d.kod = {"K0": "K0-AAAA", "K1": "K1-BBBB", "K2": "K2-CCCC"}; d.parola = DA.parola_uret(31); d.antikodon = {}; d.muhur = {}
d.gecen = {k: set() for k in d.kod}; d.bagli = {}; d.jeton_sahibi = {"J": "T1"}
g = lambda kapi, levha: {"zarf": None, "jeton": "J", "kimlik": "T1", "levha": levha, "durdurma": 0, "isaret": None, "suphe": (), "rolsuz": False}
for ac in (False, True):
    DA.DUYURU_ACIK = ac
    R["birim"]["duyuru_%s" % ("acik" if ac else "kapali")] = {
        "K2_kod": d.kapi_karari("K2", g("K2", "K2-CCCC"))[0], "K2_parola": d.kapi_karari("K2", g("K2", d.parola))[0],
        "K2_yanlis": d.kapi_karari("K2", g("K2", "XXXX"))[0], "K1_parola": d.kapi_karari("K1", g("K1", d.parola))[0]}
DA.DUYURU_ACIK = False
print(json.dumps(R["birim"], ensure_ascii=False))
json.dump(R, open(os.path.join(AK, "denetim_kapali_11kas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
