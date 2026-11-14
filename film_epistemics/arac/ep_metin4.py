# coding: utf-8
"""TESLIM VIDEOSU v4 · yazi ve sayi uretici (14 Kas, metin surum 4). ep_metin.py (v1-v3) duzeni:
- her yazi onayli FILM_METNI_14kas.md'den birebir (satir no KAYNAK.md'ye); kodda film yazisi yok,
- yazilardaki her sayi ve iddia json / kayittan yeniden hesaplanir, tutmazsa durur,
- sayac, serit, kadro veri/sayac.json + veri/saglama.json'dan (film_veri.py).
Calistir: python -I ep_metin4.py -> veri/ep_metin4.json, ../KAYNAK.md (v3'unku ../KAYNAK_v3.md)"""
import hashlib
import json
import os
import re
import statistics
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
FE = os.path.dirname(KOK)
SP = os.path.dirname(FE)
EP = os.path.join(SP, "oyun_alani_v4", "epistemik")
MD = os.path.join(FE, "FILM_METNI_14kas.md")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L = open(MD, encoding="utf-8").read().split("\n")
    kay = []

    def bas(bolum):
        return next(i for i, l in enumerate(L) if l.startswith(bolum))

    def yazi(ad, desen, bolum, son=None):
        i0 = bas(bolum)
        i1 = bas(son) if son else len(L)
        for i in range(i0, i1):
            m = re.search(desen, L[i])
            if m:
                kay.append({"ad": ad, "metin": m.group(1), "kaynak": "FILM_METNI_14kas.md satır %d" % (i + 1)})
                return m.group(1)
        raise KeyError(desen)

    Y = {}
    Y["kart"] = yazi("Açılış kartı", r'Açılış kartı \(EN\): "(.+?)"$', "## Açılış kartı", "## Sahne 1")
    Y["s1_a1"] = yazi("Sahne 1 altyazı 1", r'Altyazı 1: "(.+?)"', "## Sahne 1", "## Sahne 2")
    Y["s1_a2"] = yazi("Sahne 1 altyazı 2", r'Altyazı 2: "(.+?)"', "## Sahne 1", "## Sahne 2")
    Y["s1_sol"] = yazi("Sahne 1 sol küçük", r'sol koşunun altında küçük: "(.+?)"', "## Sahne 1", "## Sahne 2")
    Y["s1_sag"] = yazi("Sahne 1 sağ küçük", r'sağda: "(.+?)"', "## Sahne 1", "## Sahne 2")
    Y["s1_not"] = yazi("Sahne 1 küçük yazı", r'Küçük yazı: "(.+?)"', "## Sahne 1", "## Sahne 2")
    Y["olcu"] = yazi("Sahne 2 ölçü satırı", r'Ölçü satırı[^:]*: "(.+?)"', "## Sahne 2", "## Sahne 3")
    Y["levha_kapali"] = yazi("Duruş levhası", r'levha "(path to X removed[^"]+)"', "## Sahne 2", "## Sahne 3")
    Y["levha_devam"] = yazi("Devam levhası", r'levha "(the game continues as recorded)"', "## Sahne 2", "## Sahne 3")
    Y["hizli"] = yazi("Hızlı oynatma etiketi", r'köşesinde "(FAST-FORWARD)"', "## Sahne 2", "## Sahne 3")
    Y["s2_a1"] = yazi("Sahne 2 altyazı 1", r'Altyazı 1[^:]*: "(.+?)"', "## Sahne 2", "## Sahne 3")
    Y["s2_a3"] = yazi("Sahne 2 altyazı 3", r'Altyazı 3: "(.+?)"', "## Sahne 2", "## Sahne 3")
    Y["s2_a4"] = yazi("Sahne 2 altyazı 4", r'Altyazı 4: "(.+?)"', "## Sahne 2", "## Sahne 3")
    Y["anahtar"] = yazi("Oda adları anahtarı", r'Oda adları anahtarı[^:]*: "(.+?)"', "## Sahne 2", "## Sahne 3")
    Y["s3_a1"] = yazi("Sahne 3 altyazı 1", r'Altyazı 1[^:]*: "(.+?)"', "## Sahne 3", "## Kapanış")
    Y["s3_s2"] = yazi("Sahne 3 şekil 2 altyazısı", r'Şekil 2 altyazısı[^:]*: "(.+?)"', "## Sahne 3", "## Kapanış")
    Y["s3_a3"] = yazi("Sahne 3 altyazı 3", r'Altyazı 3[^:]*: "(.+?)"', "## Sahne 3", "## Kapanış")
    Y["sowhat"] = yazi("Kapanış so what", r'So what[^:]*: "(.+?)"', "## Kapanış", "## Yapım planı")
    Y["k_baslik"] = yazi("Kapanış başlık", r'Başlık[^:]*: "(.+?)"', "## Kapanış", "## Yapım planı")
    Y["k_alt"] = yazi("Kapanış alt satır", r'Başlık[^:]*: ".+?" · "(.+?)"', "## Kapanış", "## Yapım planı")
    Y["k_dip"] = yazi("Kapanış küçük yazı", r'Doğruluk sınırı \(EN[^:]*: "(.+?)"', "## Kapanış", "## Yapım planı")
    # olay etiketleri: "metin" (kayit olayi) ciftleri, tek satir
    i = bas("## Sahne 2")
    sat = next(j for j in range(i, len(L)) if L[j].startswith("- Olay etiketleri"))
    ETK = {o: m for m, o in re.findall(r'"([^"]+)" \(([a-z_]+(?: MAVI)?)\)', L[sat])}
    kay.append({"ad": "Olay etiketleri (%d)" % len(ETK), "metin": " / ".join("%s = %s" % kv for kv in ETK.items()), "kaynak": "FILM_METNI_14kas.md satır %d" % (sat + 1)})
    assert set(ETK) == {"levha_cevap", "goster", "kapi_karar MAVI", "zarf_al", "labirent", "anahtar_al", "yonlendir"}, ETK
    Y["etiket"] = {"cevap": ETK["levha_cevap"], "goster": ETK["goster"], "karar:MAVI": ETK["kapi_karar MAVI"], "zarf_al": ETK["zarf_al"],
                   "labirent": ETK["labirent"], "anahtar_al": ETK["anahtar_al"], "gecersiz": ETK["yonlendir"]}

    # --- veri
    say = json.load(open(os.path.join(KOK, "veri", "sayac.json"), encoding="utf-8"))
    sag = json.load(open(os.path.join(KOK, "veri", "saglama.json"), encoding="utf-8"))
    p_e = os.path.join(EP, "sprint_s2", "olcum_celiski_ek_14kas.json")
    p_3 = os.path.join(EP, "sprint_s3", "olcum_s3_14kas.json")
    p_4 = os.path.join(EP, "sprint_s4", "olcum_s4_14kas.json")
    p_7 = os.path.join(EP, "sprint_s4", "cagri_s4_7b.jsonl")
    E, S3, S4 = (json.load(open(p, encoding="utf-8")) for p in (p_e, p_3, p_4))
    C7 = [json.loads(l) for l in open(p_7, encoding="utf-8")]
    sayi = []

    def s(ad, deger, dosya, alan):
        sayi.append({"ad": ad, "deger": deger, "dosya": os.path.relpath(dosya, SP).replace(os.sep, "/"), "sha": sha(dosya)[:16], "alan": alan})
        return deger

    tohum = sag["tohum"]
    du, eg = say["kosu"]
    kd, ke = sag["kadro"]["DU"], sag["kadro"]["EG"]
    s("tohum", tohum, os.path.join(KOK, "veri", "saglama.json"), "tohum")
    s("kontrolde uyuyan kartın yeri", sag["uyuyan_yeri"]["EG"], os.path.join(EP, sag["meta"]["EG"]["dosya"]), "degisen.%d.uyuyan_yeri" % tohum)
    s("DU T1 kartı", kd["T1"], os.path.join(EP, sag["meta"]["DU"]["dosya"]), "degisen.%d.dagitim.T1" % tohum)
    s("EG T1 kartı", ke["T1"], os.path.join(EP, sag["meta"]["EG"]["dosya"]), "degisen.%d.dagitim.T1" % tohum)
    cp = os.path.join(EP, "sprint_s2", "celiski_s2_13kas.jsonl")
    for k in (du, eg):
        for a in k["anlar"]:
            s("%s adım %d X=%s yine X (duruş anı)" % (k["vaka"], a["adim"], a["X"]), "%d / 10" % a["yine_X"], cp, "vaka=%s, adim=%d, k=1-10, plan_degisti=false sayısı" % (k["vaka"], a["adim"]))
        s("%s toplam" % k["vaka"], "%d / 30" % k["toplam"], cp, "üç anın toplamı")
        s("%s ısrar (sağlama)" % k["vaka"], k["israr_olcum"], p_e, 'vaka[kol=E, vaka="%s"].israr' % k["vaka"])
    for t, ad in (("U", "uyuyan"), ("G", "kontrol")):
        s("şerit %s noktaları (n=%d)" % (ad, len(say["serit"][t])), [r["israr"] for r in say["serit"][t]], p_e, "vaka[kol=E, tur=%s].israr" % t)
    a7d, a7e = E["kol"]["D"]["auc"]["israr"], E["kol"]["E"]["auc"]["israr"]
    a397, ara397 = S3["kume"]["birincil (tamam)"]["auc"]["israr"], S3["kume"]["birincil (tamam)"]["israr_auc_ara_sinif"]
    s("7B AUC kol D", a7d, p_e, "kol.D.auc.israr"); s("7B AUC kol E", a7e, p_e, "kol.E.auc.israr")
    s("397B AUC", a397, p_3, 'kume["birincil (tamam)"].auc.israr'); s("397B AUC %95 aralık (sınıf katmanlı)", ara397, p_3, 'kume["birincil (tamam)"].israr_auc_ara_sinif')
    u4, g4 = S4["satir"]["397B U Sa"]["anma_an"], S4["satir"]["397B G Sa"]["anma_an"]
    s("397B uyuyan S-a an düzeyi anma", u4, p_4, 'satir["397B U Sa"].anma_an'); s("397B kontrol S-a an düzeyi anma", g4, p_4, 'satir["397B G Sa"].anma_an')
    u7a, u7b = S4["satir"]["7B U Sa"]["anma_an"], S4["satir"]["7B U Sb"]["anma_an"]
    s("7B uyuyan S-a an düzeyi anma", u7a, p_4, 'satir["7B U Sa"].anma_an'); s("7B uyuyan S-b an düzeyi anma", u7b, p_4, 'satir["7B U Sb"].anma_an')
    R7 = [e for e in C7 if e["soru"] == "Sb" and e["an"].split(":")[1][1] == "U"]
    yok7 = sum(1 for e in R7 if (e.get("cevap") or "").strip().strip(".'\"").lower() == "yok")
    s("7B uyuyan S-b cevabı tam 'yok'", "%d / %d" % (yok7, len(R7)), p_7, "soru=Sb, an türü U (an alanının 2. parçası U ile başlar), cevap.strip() == 'yok'")
    nU, nG = len(say["serit"]["U"]), len(say["serit"]["G"])
    s("kol E koşu sayısı uyuyan", nU, p_e, "vaka[kol=E, tur=U] sayısı"); s("kol E koşu sayısı kontrol", nG, p_e, "vaka[kol=E, tur=G] sayısı")
    mU, mG = statistics.median(r["israr"] for r in say["serit"]["U"]), statistics.median(r["israr"] for r in say["serit"]["G"])
    s("uyuyan ortancası", mU, p_e, "vaka[kol=E, tur=U].israr ortancası"); s("kontrol ortancası", mG, p_e, "vaka[kol=E, tur=G].israr ortancası")

    # --- yazilardaki sayi ve iddialar
    def var(metin, parca):
        assert parca in metin, (parca, metin)
    var(Y["s1_a1"], "(%d)" % tohum); var(Y["s1_not"], "(%s)" % sag["uyuyan_yeri"]["EG"]); assert kd["T1"] == "U1" and ke["T1"] == "G4"
    var(Y["s2_a1"], "go to %s" % du["anlar"][0]["X"]); assert eg["anlar"][0]["X"] == du["anlar"][0]["X"]
    var(Y["olcu"], "10 times")
    var(Y["s2_a3"], "sleeper keeps its plan %d of 30" % du["toplam"]); var(Y["s2_a3"], "control %d of 30" % eg["toplam"])
    var(Y["s2_a4"], "%d + %d runs" % (nU, nG)); assert abs(du["israr_olcum"] - mU) < 1e-9 and abs(eg["israr_olcum"] - mG) <= .05
    var(Y["s3_a1"], "AUC %.2f and %.2f" % (a7d, a7e)); var(Y["s3_a1"], "397B (%.2f, interval includes chance)" % a397); assert ara397[0] < .5 < ara397[1]
    # sekil 2 altyazisi: buyuk model hedefi aniyor (U S-a > 0, G S-a = 0); kucuk model dogrudan soruya her seferinde 'yok'; yansiz soruda bazen aniyor
    var(Y["s3_s2"], "every time"); assert yok7 == len(R7) and len(R7) > 0 and u7b == 0
    var(Y["s3_s2"], "sometimes names it when asked neutrally"); assert 0 < u7a < 1
    assert u4 > 0 and g4 == 0
    for a in (du, eg):
        for an in a["anlar"]:
            assert an["X"] in ("K1", "ODA2", "CIKIS")
    var(Y["anahtar"], "ODA = room"); var(Y["anahtar"], "CIKIS = exit")

    cikti = {"surum": 4, "yazi": Y, "sayac": say, "saglama": sag, "md_sha": sha(MD),
             "toplam_yazi": {"DU": "%d of 30 (%.2f)" % (du["toplam"], du["toplam"] / 30), "EG": "%d of 30 (%.2f)" % (eg["toplam"], eg["toplam"] / 30)}}
    json.dump(cikti, open(os.path.join(KOK, "veri", "ep_metin4.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)

    r = ["# Teslim videosu v4 · KAYNAK · her yazı ve sayının yeri", "",
         "Üretildi: `arac/ep_metin4.py` (elle yazılmaz). Metin dosyası `FILM_METNI_14kas.md` (sürüm 4) sha %s. v1-v3'ün kaynağı: `KAYNAK_v3.md` (metin sürüm 3: `FILM_METNI_14kas_surum3.md`)." % sha(MD), "",
         "Kökler: dosya yolları `Desktop/sprint/` altından. Koşu kayıtları: %s." % " · ".join(
             "%s `%s` (sha %s)" % (k["vaka"], os.path.relpath(p, SP).replace(os.sep, "/"), sha(p)[:16]) for k, p in
             ((k, os.path.join(EP, "sprint_s2", "kosular", "s2_13kas", k["id"], "t%d" % tohum, "v4_kosu2_O1_O2b_t%d_%s.jsonl" % (tohum, k["id"]))) for k in (du, eg))), "",
         "## Yazılar (onaylı metinden birebir)", "", "| yazı | metin | kaynak |", "|---|---|---|"]
    r += ["| %s | %s | %s |" % (k["ad"], k["metin"].replace("|", "/"), k["kaynak"]) for k in kay]
    r += ["", "Ek yazılar (kurgu etiketi, sayı taşımaz): panel başlıkları \"SLEEPER RUN\" / \"CONTROL RUN\" + vaka adı; sayaç satırı \"step N · plan: go X\"; kutuda cevabın eylemi (git → go + hedef, goster → show, bekle → wait); \"filled box = the answer still keeps the original plan\"; şerit ekseni \"persistence (share of re-asks that keep the plan)\". Duruş levhasındaki X, o anın kayıttaki hedefidir (K1, ODA2, CIKIS). Olay etiketi yalnız T1'in kayıttaki olayına bağlıdır; zamanı film.js EP_PLAN.olaylar (kayıt adımı ve dünya saati).", "",
          "## Sayılar", "", "| sayı | değer | dosya | sha (ilk 16) | alan |", "|---|---|---|---|---|"]
    r += ["| %s | %s | %s | %s | `%s` |" % (x["ad"], x["deger"], x["dosya"], x["sha"], x["alan"]) for x in sayi]
    r += ["", "## Aynı başlangıç sağlaması (veri/saglama.json, `arac/film_veri.py`)", "",
          "- Kural: %s." % sag["kural"],
          "- Karşılaştırılan satır: %s · kadro dışı fark yok: %s · kadro farkı olan ajanlar: %s." % (sag["karsilastirilan_satir"], sag["kadro_disi_fark_yok"], ", ".join(sag["kadro_farki_olan_ajanlar"])),
          "- Meta özetleri aynı: %s." % ", ".join("%s %s" % (k, v) for k, v in sag["meta_ayni"].items()),
          "- Kadro DU: %s · EG: %s." % (sag["kadro"]["DU"], sag["kadro"]["EG"]),
          "- Kanarya iki kayıtta: %s." % " / ".join(sag["kanarya"]), "",
          "## Görüntü", "",
          "- 3B sahne: `arac/film.js` ep=4 kipi (epBaslat4), `EPKIP=4 python -I arac/cek_ep.py tam`. Dünya saati kayıttan; T1 üç karar anında durur (kayıt adımları %s / %s), duruş yürüyüşün %%72 / %%50 / %%50'sinde (kurgu). Anlar arası hızlı oynatma; iki koşu ayrı hızda, duruşlar aynı film anında." % (du["anlar"] and [a["adim"] for a in du["anlar"]], [a["adim"] for a in eg["anlar"]]),
          "- Duruştaki kesik çizgi ve çarpı: T1'in ekran konumundan o anın yol ucuna (film.js __ekranAn, her duruş karesinde; cek_ep.py plan.json `ekran`).",
          "- Sahne 3 şekilleri değiştirilmeden: `epistemics/sekil_sprint/sekil1_auc.png` (sha %s), `sekil2_hedef_anma.png` (sha %s)." % (sha(os.path.join(SP, "epistemics", "sekil_sprint", "sekil1_auc.png"))[:16], sha(os.path.join(SP, "epistemics", "sekil_sprint", "sekil2_hedef_anma.png"))[:16]),
          ""]
    open(os.path.join(FE, "KAYNAK.md"), "w", encoding="utf-8", newline="\n").write("\n".join(r))
    for k, v in Y.items():
        print(k, "|", v)
    print("7B S-b yok", yok7, "/", len(R7), "· 7B S-a", u7a, "· md", cikti["md_sha"][:16])


if __name__ == "__main__":
    main()
