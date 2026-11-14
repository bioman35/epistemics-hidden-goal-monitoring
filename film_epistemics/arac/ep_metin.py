# coding: utf-8
"""TESLIM VIDEOSU · yazi ve sayi uretici (14 Kas). Kodda film yazisi yok:
- her altyazi ve kucuk yazi onayli FILM_METNI_14kas.md'den birebir alinir (satir numarasi KAYNAK.md'ye),
- yazilardaki her sayi json kaynagindan yeniden hesaplanir ve yazidakiyle karsilastirilir (tutmazsa durur),
- sayac, serit ve kadro veri/sayac.json + veri/saglama.json'dan (film_veri.py).
Calistir: python -I ep_metin.py -> veri/ep_metin.json, ../KAYNAK.md"""
import hashlib
import json
import os
import re
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
    kay = []   # (yazi, kaynak)

    def bul(desen, bolum=None):
        """md'de desene uyan ilk satir (bolum basligindan sonra); tirnak icindeki metni ve satir no'yu dondurur"""
        bas = 0
        if bolum:
            bas = next(i for i, l in enumerate(L) if l.startswith(bolum))
        for i in range(bas, len(L)):
            m = re.search(desen, L[i])
            if m:
                return m.group(1), i + 1
        raise KeyError(desen)

    def yazi(ad, desen, bolum):
        m, n = bul(desen, bolum)
        kay.append({"ad": ad, "metin": m, "kaynak": "FILM_METNI_14kas.md satır %d" % n})
        return m

    Y = {}
    Y["s1_a1"] = yazi("Sahne 1 altyazı 1", r'Altyazı 1: "(.+?)"', "## Sahne 1")
    Y["s1_a2"] = yazi("Sahne 1 altyazı 2", r'Altyazı 2: "(.+?)"', "## Sahne 1")
    Y["s1_sol"] = yazi("Sahne 1 sol küçük", r'sol koşunun altında küçük: "(.+?)"', "## Sahne 1")
    Y["s1_sag"] = yazi("Sahne 1 sağ küçük", r'sağda: "(.+?)"', "## Sahne 1")
    Y["s1_not"] = yazi("Sahne 1 küçük yazı", r'Küçük yazı: "(.+?)"', "## Sahne 1")
    for i in (1, 2, 3, 4):
        Y["s2_a%d" % i] = yazi("Sahne 2 altyazı %d" % i, r'Altyazı %d[^:]*: "(.+?)"' % i, "## Sahne 2")
    for i in (1, 2, 3):
        Y["s3_a%d" % i] = yazi("Sahne 3 altyazı %d" % i, r'Altyazı %d[^:]*: "(.+?)"' % i, "## Sahne 3")
    Y["k_baslik"] = yazi("Kapanış başlık", r'Başlık[^:]*: "(.+?)"', "## Kapanış")
    Y["k_alt"] = yazi("Kapanış alt satır", r'Başlık[^:]*: ".+?" · "(.+?)"', "## Kapanış")
    Y["k_dip"] = yazi("Kapanış küçük yazı", r'Doğruluk sınırı \(EN[^:]*: "(.+?)"', "## Kapanış")

    # --- veri
    say = json.load(open(os.path.join(KOK, "veri", "sayac.json"), encoding="utf-8"))
    sag = json.load(open(os.path.join(KOK, "veri", "saglama.json"), encoding="utf-8"))
    p_e = os.path.join(EP, "sprint_s2", "olcum_celiski_ek_14kas.json")
    p_3 = os.path.join(EP, "sprint_s3", "olcum_s3_14kas.json")
    p_4 = os.path.join(EP, "sprint_s4", "olcum_s4_14kas.json")
    E, S3, S4 = (json.load(open(p, encoding="utf-8")) for p in (p_e, p_3, p_4))
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
            s("%s adım %d X=%s yine X" % (k["vaka"], a["adim"], a["X"]), "%d / 10" % a["yine_X"], cp, "vaka=%s, adim=%d, k=1-10, plan_degisti=false sayısı" % (k["vaka"], a["adim"]))
        s("%s toplam" % k["vaka"], "%d / 30" % k["toplam"], cp, "üç anın toplamı")
        s("%s ısrar (sağlama)" % k["vaka"], k["israr_olcum"], p_e, 'vaka[kol=E, vaka="%s"].israr' % k["vaka"])
    for t, ad in (("U", "uyuyan"), ("G", "kontrol")):
        v = [r["israr"] for r in say["serit"][t]]
        s("şerit %s noktaları (n=%d)" % (ad, len(v)), v, p_e, "vaka[kol=E, tur=%s].israr" % t)
    a7d, a7e, a397 = E["kol"]["D"]["auc"]["israr"], E["kol"]["E"]["auc"]["israr"], S3["kume"]["birincil (tamam)"]["auc"]["israr"]
    ara397 = S3["kume"]["birincil (tamam)"]["israr_auc_ara_sinif"]
    s("7B AUC kol D", a7d, p_e, "kol.D.auc.israr"); s("7B AUC kol E", a7e, p_e, "kol.E.auc.israr")
    s("397B AUC", a397, p_3, 'kume["birincil (tamam)"].auc.israr'); s("397B AUC %95 aralık (sınıf katmanlı)", ara397, p_3, 'kume["birincil (tamam)"].israr_auc_ara_sinif')
    u4, g4 = S4["satir"]["397B U Sa"]["anma_an"], S4["satir"]["397B G Sa"]["anma_an"]
    s("397B uyuyan S-a an düzeyi anma", u4, p_4, 'satir["397B U Sa"].anma_an'); s("397B kontrol S-a an düzeyi anma", g4, p_4, 'satir["397B G Sa"].anma_an')
    nU, nG = len(say["serit"]["U"]), len(say["serit"]["G"])
    s("kol E koşu sayısı uyuyan", nU, p_e, "vaka[kol=E, tur=U] sayısı"); s("kol E koşu sayısı kontrol", nG, p_e, "vaka[kol=E, tur=G] sayısı")

    # --- yazilardaki sayilar json ile ayni mi
    def var(metin, parca):
        assert parca in metin, (parca, metin)
    var(Y["s1_a1"], "(%d)" % tohum)
    var(Y["s1_not"], "(%s)" % sag["uyuyan_yeri"]["EG"])
    assert kd["T1"] == "U1" and ke["T1"] == "G4"
    var(Y["s2_a1"], "go to %s" % du["anlar"][0]["X"]); assert eg["anlar"][0]["X"] == du["anlar"][0]["X"]
    var(Y["s2_a2"], "path to %s removed" % du["anlar"][0]["X"])
    var(Y["s2_a3"], "sleeper keeps its plan %d of 30" % du["toplam"]); var(Y["s2_a3"], "control %d of 30" % eg["toplam"])
    var(Y["s2_a4"], "%d + %d runs" % (nU, nG))
    var(Y["s3_a1"], "AUC %.2f and %.2f" % (a7d, a7e)); var(Y["s3_a1"], "397B (%.2f, interval includes chance)" % a397)
    assert ara397[0] < .5 < ara397[1]
    var(Y["s3_a2"], "%d%% of moments" % round(u4 * 100)); assert g4 == 0 and "never" in Y["s3_a2"]
    # medyan iddiasi (altyazi 4): gosterilen cift her grubun ortancasinda ya da yakininda
    import statistics
    mU, mG = statistics.median(r["israr"] for r in say["serit"]["U"]), statistics.median(r["israr"] for r in say["serit"]["G"])
    s("uyuyan ortancası", mU, p_e, "vaka[kol=E, tur=U].israr ortancası"); s("kontrol ortancası", mG, p_e, "vaka[kol=E, tur=G].israr ortancası")
    assert abs(du["israr_olcum"] - mU) < 1e-9 and abs(eg["israr_olcum"] - mG) <= .05, (mU, mG)

    cikti = {"yazi": Y, "sayac": say, "saglama": sag, "md_sha": sha(MD),
             "toplam_yazi": {"DU": "%d of 30 (%.2f)" % (du["toplam"], du["toplam"] / 30), "EG": "%d of 30 (%.2f)" % (eg["toplam"], eg["toplam"] / 30)}}
    json.dump(cikti, open(os.path.join(KOK, "veri", "ep_metin.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)

    # --- KAYNAK.md
    r = ["# Teslim videosu · KAYNAK · her yazı ve sayının yeri", "",
         "Üretildi: `arac/ep_metin.py` (elle yazılmaz). Metin dosyası `FILM_METNI_14kas.md` sha %s." % sha(MD), "",
         "Kökler: dosya yolları `Desktop/sprint/` altından. Koşu kayıtları: %s." % " · ".join(
             "%s `%s` (sha %s)" % (k["vaka"], os.path.relpath(p, SP).replace(os.sep, "/"), sha(p)[:16]) for k, p in
             ((k, os.path.join(EP, "sprint_s2", "kosular", "s2_13kas", k["id"], "t%d" % tohum, "v4_kosu2_O1_O2b_t%d_%s.jsonl" % (tohum, k["id"]))) for k in (du, eg))), "",
         "## Yazılar (onaylı metinden birebir)", "", "| yazı | metin | kaynak |", "|---|---|---|"]
    r += ["| %s | %s | %s |" % (k["ad"], k["metin"].replace("|", "/"), k["kaynak"]) for k in kay]
    r += ["", "Ek yazılar (kurgu etiketi, sayı taşımaz): panel başlıkları \"SLEEPER RUN\" / \"CONTROL RUN\" + vaka adı; sayaç satırı \"step N · plan: go X\"; kutuda cevabın eylemi (git → go + hedef, goster → show, bekle → wait); çatal levhası \"path to K1 removed · re-ask only, not in the game\"; şerit ekseni \"persistence (share of re-asks that keep the plan)\"; v3 (danışman 14 Kas, ek yazı, kurgu): oda adları anahtarı \"Room names from the game: ODA = room, CIKIS = exit, K1 = gate 1.\" (39,7-66 sn, sayaçların üstünde). Kutulardaki oda adları kayıttan aynen.", "",
          "## Sayılar", "", "| sayı | değer | dosya | sha (ilk 16) | alan |", "|---|---|---|---|---|"]
    r += ["| %s | %s | %s | %s | `%s` |" % (x["ad"], x["deger"], x["dosya"], x["sha"], x["alan"]) for x in sayi]
    r += ["", "## Aynı başlangıç sağlaması (veri/saglama.json, `arac/film_veri.py`)", "",
          "- Kural: %s." % sag["kural"],
          "- Karşılaştırılan satır: %s · kadro dışı fark yok: %s · kadro farkı olan ajanlar: %s." % (sag["karsilastirilan_satir"], sag["kadro_disi_fark_yok"], ", ".join(sag["kadro_farki_olan_ajanlar"])),
          "- Meta özetleri aynı: %s." % ", ".join("%s %s" % (k, v) for k, v in sag["meta_ayni"].items()),
          "- Kadro DU: %s · EG: %s." % (sag["kadro"]["DU"], sag["kadro"]["EG"]),
          "- Kanarya iki kayıtta: %s." % " / ".join(sag["kanarya"]), "",
          "## Görüntü", "",
          "- 3B sahne: `arac/film.js` ep kipi (film_sprint kopyası), `arac/cek_ep.py tam`; dünya saati kayıttan, T1'in yürüyüşü kayıttaki adım %d \"gir %s\" olayı; kare yürüyüşün %%72'sinde donar (kurgu)." % (du["karar_adim"], du["anlar"][0]["X"]),
          "- Sahne 3 şekilleri değiştirilmeden: `epistemics/sekil_sprint/sekil1_auc.png` (sha %s), `sekil2_hedef_anma.png` (sha %s)." % (sha(os.path.join(SP, "epistemics", "sekil_sprint", "sekil1_auc.png"))[:16], sha(os.path.join(SP, "epistemics", "sekil_sprint", "sekil2_hedef_anma.png"))[:16]),
          ""]
    open(os.path.join(FE, "KAYNAK.md"), "w", encoding="utf-8", newline="\n").write("\n".join(r))
    for k, v in Y.items():
        print(k, "|", v)
    print("toplam", cikti["toplam_yazi"], "ortanca U/G", mU, mG, "md", cikti["md_sha"][:16])


if __name__ == "__main__":
    main()
