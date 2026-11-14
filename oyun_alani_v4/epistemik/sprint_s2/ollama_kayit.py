# coding: utf-8
"""S2 OLLAMA KAYDI · 14 Kas 2026 · Hikayeci · danismanin istegi: kosu_meta'da Ollama surumu ve donanim alani yoktu; S2'de bu eksik tekrarlanmasin.
Dunya ve zincir kodu DEGISMEZ. Bu betik yanda calisir: dakikada bir Ollama surumunu, yuklu modelin ozetini, boyutunu ve ekran bellegindeki payini
(size_vram / size) saatle birlikte ollama_kayit_<etiket>.jsonl dosyasina yazar. Kosu - kayit eslesmesi saatten yapilir (kosu_meta baslangic / bitis).
python -I ollama_kayit.py [--etiket 13kas] [--aralik 60]"""
import argparse, json, os, time, urllib.request
BU = os.path.dirname(os.path.abspath(__file__))
def api(y):
    return json.loads(urllib.request.urlopen("http://127.0.0.1:11434" + y, timeout=20).read() or b"{}")
p = argparse.ArgumentParser(); p.add_argument("--etiket", default="13kas"); p.add_argument("--aralik", type=int, default=60); a = p.parse_args()
yol = os.path.join(BU, "ollama_kayit_%s.jsonl" % a.etiket)
while True:
    k = {"saat": time.strftime("%Y-%m-%d %H:%M:%S")}
    try:
        k["ollama"] = api("/api/version").get("version")
        k["ps"] = [{"ad": m.get("name"), "ozet": (m.get("digest") or "")[:12], "boyut": m.get("size"), "ekran_bellegi": m.get("size_vram"),
                    "ekran_payi": round((m.get("size_vram") or 0) / (m.get("size") or 1), 3)} for m in api("/api/ps").get("models") or []]
    except Exception as e:
        k["hata"] = type(e).__name__
    open(yol, "a", encoding="utf-8").write(json.dumps(k, ensure_ascii=False) + "\n"); time.sleep(a.aralik)
