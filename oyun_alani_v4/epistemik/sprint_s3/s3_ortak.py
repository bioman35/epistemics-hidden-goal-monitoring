# coding: utf-8
"""S3 ORTAK · 14 Kas 2026 · Hikayeci · onkayit epistemik/onkayit_sprint/ONKAYIT_S3_397b_ajan.md + SAPMA_S3_14kas.md
397B tasiyicisi (Adaption Responses API, akisli), cagri kaydi, defter (butun koşu ve catal cagrilari) ve FRENLER.
Anahtar yalniz surec ortaminda: ADAPTION_API_KEY (basilmaz, yazilmaz).
FRENLER (danisman is emri 3, tek kola uyarlanmis):
  koşu basina 150 cagri (asan koşu KESILIR, ayri satir) · ilk 50 cagrida gecersiz JSON > %15 DUR · cikti jetonu ortalamasi > 6.000 DUR
  tavan: koşular 20 $, catal 8 $, toplam 30 $ · DUR olursa S3_DUR.txt yazilir, butun surecler yeni cagri acmaz."""
import json, os, random, re, sys, threading, time, urllib.error, urllib.request

BU = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(BU))
ADAPTION = "https://api.prod.adaptionlabs.ai/api/v1"
MODEL, SICAKLIK, CIKTI_PAYI = "qwen3.5-397b", 0.7, 8000
FIYAT = {"girdi": 0.55, "cikti": 3.50}                      # $ / 1M jeton (hafiza: reference_adaption_model_fiyatlari, 13 Kas)
KOSU_CAGRI_SINIRI, ILK_N, GECERSIZ_ESIK, CIKTI_ORT_ESIK = 150, 50, 0.15, 6000
TAVAN = {"kosu": 40.0, "catal": 12.0, "toplam": 50.0}          # 14 Kas 08:1x danisman: onkayit Yol 3 + EK 1 (toplam 50 $); ilk hali 20 / 8 / 30
TAHMIN_SINIRI = 50.0
DUR = os.path.join(BU, "S3_DUR.txt")                              # genel fren: her sey durur
DUR_KOSU = os.path.join(BU, "S3_DUR_kosu.txt")                     # yalniz koşu tavani: yeni koşu cagrisi durur, catal kendi tavaniyla surer
_kilit = threading.Lock()


class KosuKesildi(Exception):
    pass


class S3Dur(Exception):
    pass


def json_ayikla(metin):
    sys.path.insert(0, KOK)
    import suruculer as S
    return S.json_ayikla(metin)


def defter(kok=None):
    """butun cagri kayitlari: sprint_s3/kosular/**/cagri_s3.jsonl + sprint_s3/catal_s3*.jsonl"""
    import glob
    L = []
    for p in glob.glob(os.path.join(kok or BU, "kosular", "**", "cagri_s3.jsonl"), recursive=True):
        L += [dict(json.loads(x), _tur="kosu") for x in open(p, encoding="utf-8") if x.strip()]
    for p in glob.glob(os.path.join(kok or BU, "catal_s3*.jsonl")):
        L += [dict(json.loads(x), _tur="catal") for x in open(p, encoding="utf-8") if x.strip()]
    return L


def fren(tur, kok=None):
    """yeni cagri acmadan once · DUR dosyasi ya da kural ihlali varsa S3Dur · kok: yalniz sinama icin baska klasor"""
    dur = os.path.join(kok, "S3_DUR.txt") if kok else DUR; dur_k = os.path.join(kok, "S3_DUR_kosu.txt") if kok else DUR_KOSU
    if os.path.exists(dur):
        raise S3Dur(open(dur, encoding="utf-8").read().strip())
    if tur == "kosu" and os.path.exists(dur_k):
        raise S3Dur(open(dur_k, encoding="utf-8").read().strip())
    D = [d for d in defter(kok) if not d.get("sahte")]
    h = {"kosu": sum(d.get("maliyet") or 0 for d in D if d["_tur"] == "kosu"), "catal": sum(d.get("maliyet") or 0 for d in D if d["_tur"] == "catal")}
    h["toplam"] = h["kosu"] + h["catal"]; neden = None
    yalniz_kosu = False
    if h[tur] >= TAVAN[tur]: neden = "tavan %s %.2f $ >= %.0f $" % (tur, h[tur], TAVAN[tur]); yalniz_kosu = tur == "kosu"
    elif h["toplam"] >= TAVAN["toplam"]: neden = "toplam tavan %.2f $ >= %.0f $" % (h["toplam"], TAVAN["toplam"])
    K = sorted([d for d in D if d["_tur"] == "kosu" and not d.get("hata")], key=lambda d: d.get("saat", ""))
    if len(K) >= ILK_N and neden is None:
        ilk = K[:ILK_N]; g = sum(1 for d in ilk if d.get("gecersiz")) / ILK_N
        if g > GECERSIZ_ESIK: neden = "ilk %d kosu cagrisinda gecersiz JSON %.3f > %.2f" % (ILK_N, g, GECERSIZ_ESIK)
    C = [d.get("cikti") for d in D if d.get("cikti") is not None and not d.get("hata")]
    if len(C) >= 20 and neden is None and sum(C) / len(C) > CIKTI_ORT_ESIK:
        neden = "cikti jetonu ortalamasi %.0f > %d (%d cagri)" % (sum(C) / len(C), CIKTI_ORT_ESIK, len(C))
    if neden:
        dur = dur_k if yalniz_kosu else dur
        with _kilit:
            if not os.path.exists(dur):
                open(dur, "w", encoding="utf-8").write(time.strftime("%Y-%m-%d %H:%M:%S ") + neden + "\n")
        raise S3Dur(neden)
    return h


def _akis(govde):
    k = os.environ.get("ADAPTION_API_KEY")
    if not k: raise SystemExit("ortam degiskeni yok: ADAPTION_API_KEY")
    q = urllib.request.Request(ADAPTION + "/responses", data=json.dumps(dict(govde, stream=True)).encode("utf-8"),
                               headers={"Content-Type": "application/json", "Accept": "text/event-stream", "Authorization": "Bearer " + k})
    son = None; ilk = None; t0 = time.time()
    with urllib.request.urlopen(q, timeout=900) as y:
        for ln in y:
            ln = ln.decode("utf-8", "replace").strip()
            if not ln.startswith("data:"): continue
            try: o = json.loads(ln[5:].strip())
            except Exception: continue
            if o.get("type") == "response.output_text.delta" and ilk is None: ilk = time.time() - t0
            if o.get("type") in ("response.completed", "response.incomplete", "response.failed") and isinstance(o.get("response"), dict): son = o["response"]
    if son is None: raise RuntimeError("akis bitti, son yanit yok")
    return son, ilk


class Adaption397:
    """suruculer.Tasiyici arayuzu: sohbet(mesajlar, tohum) -> (metin, girdi, cikti) · seed GONDERILMEZ (Adaption'da yok) ·
    her cagri kayit_yolu'na bir satir (istem dahil) · sahte=True: dil modeli YOK, suruculer.Sahte cevabi + uydurma jeton (yalniz boru hatti sinamasi)"""
    ad = "api"

    def __init__(self, kayit_yolu, tur="kosu", sahte=False, sinir=None, sahte_gecersiz=0.0):
        self.model, self.fiyat, self.kayit_yolu, self.tur, self.sahte = (MODEL if not sahte else "sahte"), FIYAT, kayit_yolu, tur, sahte
        self.n, self.sinir, self.ajan, self.adim = 0, sinir, None, None
        self.rr = random.Random(7); self.sahte_gecersiz = sahte_gecersiz
        if sahte:
            sys.path.insert(0, KOK); import suruculer as S; self._s = S.Sahte()

    def dolar(self, g, c):
        return round(g * FIYAT["girdi"] / 1e6 + c * FIYAT["cikti"] / 1e6, 8) if not self.sahte else 0.0

    def sohbet(self, mesajlar, tohum, ek=None):
        if self.sinir is not None and self.n >= self.sinir:
            raise KosuKesildi("kosu cagri siniri %d" % self.sinir)
        if not self.sahte: fren(self.tur)
        self.n += 1; t0 = time.time(); hata = None; durum = None; ilk = None; dus = None
        if self.sahte:
            metin, g, c = self._s.sohbet(mesajlar, tohum)
            if self.sahte_gecersiz and self.rr.random() < self.sahte_gecersiz: metin = "bozuk cevap"
            g, c, durum = 900 + self.rr.randint(0, 300), 3000 + self.rr.randint(0, 1500), "completed"
        else:
            govde = {"model": MODEL, "instructions": mesajlar[0]["content"], "temperature": SICAKLIK, "max_output_tokens": CIKTI_PAYI, "store": False,
                     "input": [{"role": m["role"], "content": m["content"]} for m in mesajlar[1:]]}
            metin, g, c = "", 0, 0
            for deneme in range(4):
                try:
                    son, ilk = _akis(govde); u = son.get("usage") or {}; g, c = u.get("input_tokens") or 0, u.get("output_tokens") or 0
                    dus = (u.get("output_tokens_details") or {}).get("reasoning_tokens"); durum = son.get("status")
                    metin = son.get("output_text") or "".join(x.get("text", "") for o in son.get("output") or [] if o.get("type") == "message" for x in o.get("content") or [] if x.get("type") == "output_text")
                    hata = None; break
                except urllib.error.HTTPError as e:
                    hata = "HTTP %d" % e.code
                    if e.code in (429, 500, 502, 503, 504) and deneme < 3: time.sleep(20 * (deneme + 1)); continue
                    break
                except Exception as e:
                    hata = type(e).__name__
                    if deneme < 3: time.sleep(20 * (deneme + 1)); continue
                    break
        e = json_ayikla(metin); gecersiz = not (e and isinstance(e.get("eylem"), str))
        r = {"saat": time.strftime("%Y-%m-%d %H:%M:%S"), "n": self.n, "ajan": self.ajan, "adim": self.adim, "girdi": g, "cikti": c, "dusunme": dus, "durum": durum,
             "kesik": durum == "incomplete", "gecersiz": gecersiz, "hata": hata, "sure_sn": round(time.time() - t0, 2), "ilk_jeton_sn": None if ilk is None else round(ilk, 2),
             "maliyet": self.dolar(g, c), "sahte": self.sahte, "tohum_gonderildi": False, "mesajlar": mesajlar, "cevap": metin}
        if ek: r.update(ek)
        with _kilit:
            open(self.kayit_yolu, "a", encoding="utf-8").write(json.dumps(r, ensure_ascii=False) + "\n")
        if hata and not metin:
            raise RuntimeError("cagri basarisiz (%s), 4 deneme" % hata)
        return metin, g, c
