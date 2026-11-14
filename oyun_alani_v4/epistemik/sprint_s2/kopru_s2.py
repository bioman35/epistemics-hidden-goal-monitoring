# coding: utf-8
"""KOPRU SINAMASI · 14 Kas 2026 · Hikayeci · danismanin sarti: Ollama yeniden kurulduktan sonra, S2 baslamadan ONCE.
Soru: yeniden kurulan Ollama (0.40.15, ekran karti) kilitteki 11 Kas kosularini BIREBIR yeniden uretiyor mu?
Yontem (belirlenim_kaynak.py ile ayni komut, ayni tohum, ayni model; dondurulmus dosyalara yazmaz):
  model bosaltilir (soguk) -> kosu_ikiz.py --kol K0 --tohumlar <T> -> cikti YENI klasore (sprint_s2/kopru_14kas/<ad>/)
  -> satir satir karsilastirma: eylem alanlari (ALAN) + ajan_aciklamasi, kilitteki SOGUK kayitla.
  Uc adim: t16 soguk (kayit v4_ikiz_bk_t16_soguk_11kas) · t26 soguk (v4_ikiz_bk_t26_soguk_11kas) · "16,26" soguk (v4_ikiz_bk_1626_soguk_11kas).
Her adimda Ollama surumu, /api/ps islemci bilgisi (size_vram / size) ve model ozeti yazilir.
Cikti: sprint_s2/kopru_s2_14kas.json ve .md · cikis kodu 0 = ucu de birebir, 1 = en az biri tutmadi.
python -I kopru_s2.py"""
import glob, json, os, subprocess, sys, time, urllib.request

BU = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(BU)); M = "qwen2.5:7b-instruct-q4_K_M"
ALAN = ("zaman", "ajan_id", "olay", "konum", "metin", "kapi_id", "karar", "renk", "zarf", "isaret")
ADIM = [("t16_soguk", "16", "v4_ikiz_bk_t16_soguk_11kas"), ("t26_soguk", "26", "v4_ikiz_bk_t26_soguk_11kas"), ("1626_soguk", "16,26", "v4_ikiz_bk_1626_soguk_11kas")]


def api(yol, veri=None):
    r = urllib.request.Request("http://127.0.0.1:11434" + yol, data=None if veri is None else json.dumps(veri).encode(), headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(r, timeout=180).read() or b"{}")


def bosalt():
    try: api("/api/generate", {"model": M, "keep_alive": 0})
    except Exception: pass
    for _ in range(30):
        if not api("/api/ps").get("models"): return True
        time.sleep(2)
    raise SystemExit("model bosalmadi")


def durum():
    ps = api("/api/ps").get("models") or []; t = api("/api/tags").get("models") or []
    return {"ollama": api("/api/version").get("version"), "ps": [{"ad": m.get("name"), "boyut": m.get("size"), "ekran_bellegi": m.get("size_vram"), "ozet": (m.get("digest") or "")[:12]} for m in ps],
            "model_ozet": next(((m.get("digest") or "")[:12] for m in t if m.get("name") == M), None)}


def satirlar(klasor, tohum):
    p = glob.glob(os.path.join(klasor, "*_t%s_K0.jsonl" % tohum))
    if len(p) != 1: return None
    return [json.loads(x) for x in open(p[0], encoding="utf-8") if x.strip()]


def karsilastir(yeni, eski):
    if yeni is None or eski is None: return {"birebir": False, "neden": "dosya yok"}
    n = min(len(yeni), len(eski)); ilk = None; ef = 0; af = 0
    for i in range(n):
        e = any(yeni[i].get(a) != eski[i].get(a) for a in ALAN); c = yeni[i].get("ajan_aciklamasi") != eski[i].get("ajan_aciklamasi")
        if e: ef += 1; ilk = i if ilk is None else ilk
        if c: af += 1
    return {"birebir": len(yeni) == len(eski) and ef == 0 and af == 0, "satir": [len(yeni), len(eski)], "eylem_farkli_satir": ef, "ilk_eylem_farki": ilk, "aciklama_farkli_satir": af}


def main():
    sys.stdout.reconfigure(encoding="utf-8"); S = []
    for ad, toh, kayit in ADIM:
        ck = os.path.join(BU, "kopru_14kas", ad)
        if os.path.exists(ck): raise SystemExit("cikti klasoru zaten var, ustune yazilmaz: %s" % ck)
        bosalt(); t0 = time.time()
        r = subprocess.run([sys.executable, "-I", "kosu_ikiz.py", "--kol", "K0", "--tasiyici", "yerel", "--model", M, "--tohumlar", toh, "--cikti", ck], cwd=KOK, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        d = durum(); k = {"ad": ad, "tohumlar": toh, "kayit": kayit, "cikis": r.returncode, "sure_sn": round(time.time() - t0), "saat": time.strftime("%Y-%m-%d %H:%M:%S"), "durum": d, "tohum": {}}
        for t in toh.split(","): k["tohum"][t] = karsilastir(satirlar(ck, t), satirlar(os.path.join(KOK, "kosular", kayit), t))
        S.append(k); print("KOPRU %s cikis %d %d sn · %s · %s" % (ad, r.returncode, k["sure_sn"], {t: v.get("birebir") for t, v in k["tohum"].items()}, d["ps"]), flush=True)
    tamam = all(v.get("birebir") for k in S for v in k["tohum"].values()) and all(k["cikis"] == 0 for k in S)
    json.dump({"tamam": tamam, "adim": S, "betik": os.path.basename(__file__)}, open(os.path.join(BU, "kopru_s2_14kas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Köprü sınaması · 14 Kas 2026 · Hikayeci", "", "Yeniden kurulan Ollama ile kilitteki 11 Kas soğuk koşularının yeniden üretimi (aynı komut, aynı tohum). Ölçü: eylem alanları + açıklama, satır satır.", "",
          "| adım | tohum | kilitteki kayıt | süre sn | satır (yeni, eski) | eylem farklı satır | açıklama farklı satır | birebir | Ollama | ekran belleği / boyut | model özeti |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in S:
        for t, v in k["tohum"].items():
            p = (k["durum"]["ps"] or [{}])[0]
            md.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s / %s | %s |" % (k["ad"], t, k["kayit"], k["sure_sn"], v.get("satir"), v.get("eylem_farkli_satir"), v.get("aciklama_farkli_satir"), v.get("birebir"), k["durum"]["ollama"], p.get("ekran_bellegi"), p.get("boyut"), k["durum"]["model_ozet"]))
    md += ["", "Sonuç: %s" % ("üç adım da birebir" if tamam else "EN AZ BİR ADIM TUTMADI; S2 başlatılmaz")]
    open(os.path.join(BU, "kopru_s2_14kas.md"), "w", encoding="utf-8").write("\n".join(md)); print("\n".join(md[4:])); sys.exit(0 if tamam else 1)


main()
