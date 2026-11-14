# coding: utf-8
"""S2 GECE KOSUSU · 13 Kas 2026 (sprint ici) · Hikayeci · Turan'in sozu (13 Kas aksam, Hikayeci penceresi): "gece kosarsin dostum sabah teslim alirim"
Sirayla: (1) zincir_s2.py (45 birincil kosu tohum tohum, sonra EU blogu, sonunda olcu) · (2) celiski_s2.py catal · (3) celiski_s2.py analiz.
KAPI (her adimdan once, betigin ICINDE): saat --en-erken'den once baslamaz · yayin programi (TikTok LIVE Studio / OBS / Unreal) yok ·
  baska pencerenin basliksiz tarayicisi (chrome-headless-shell) yok · ekran karti kullanimi ust uste 3 okumada (birer dakika arayla) <= %25.
  Kapi acilmazsa bekler (dakikada bir bakar), sabah --en-gec saatine kadar; o saatte hala acilmadiysa cikar ve nedenini yazar.
BEKCI: zincir kendi bekcisiyle (20 sn) yayin programi acilirsa kosan kosuyu durdurur; bu betik o zaman kapiya doner, kapi acilinca KALDIGI YERDEN surdurur.
  Catal adiminda ayni bekci bu betiktedir (catal satir satir yazar, kaldigi yerden surer).
Gunluk: gece_s2_<etiket>.log · bitis ozeti: gece_s2_<etiket>_bitti.json
Kullanim: python -I gece_s2.py [--etiket 13kas] [--en-erken 22:00] [--en-gec 09:00] [--eu-yok] [--catal-yok]"""
import argparse, datetime as dt, json, os, subprocess, sys, time

BU = os.path.dirname(os.path.abspath(__file__))
YAYIN = ("tiktok live studio", "obs64", "obs32", "obs.exe", "unrealeditor")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


def surecler():
    return subprocess.run(["tasklist"], capture_output=True, text=True, errors="ignore").stdout.lower()


def gpu():
    try:
        return int(subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=30).stdout.strip().splitlines()[0])
    except Exception:
        return None


def main():
    p = argparse.ArgumentParser(); p.add_argument("--etiket", default="13kas"); p.add_argument("--en-erken", default="22:00"); p.add_argument("--en-gec", default="09:00")
    p.add_argument("--eu-yok", action="store_true"); p.add_argument("--catal-yok", action="store_true")
    a = p.parse_args(); sys.stdout.reconfigure(encoding="utf-8")
    gunluk = open(os.path.join(BU, "gece_s2_%s.log" % a.etiket), "a", encoding="utf-8")
    def yaz(*m):
        s = time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in m); print(s, flush=True); gunluk.write(s + "\n"); gunluk.flush()
    bas = dt.datetime.now(); hs, hd = (int(x) for x in a.en_erken.split(":")); gs, gd = (int(x) for x in a.en_gec.split(":"))
    erken = bas.replace(hour=hs, minute=hd, second=0, microsecond=0)
    if erken < bas - dt.timedelta(hours=12): erken += dt.timedelta(days=1)
    gec = bas.replace(hour=gs, minute=gd, second=0, microsecond=0)
    while gec <= max(bas, erken): gec += dt.timedelta(days=1)
    yaz("GECE S2 basladi · en erken", erken.strftime("%d.%m %H:%M"), "· en gec", gec.strftime("%d.%m %H:%M"))
    ozet = {"baslangic": bas.isoformat(timespec="seconds"), "adim": [], "kapi_bekleme_dk": 0}

    def kapi(ad):
        """True: acildi · False: en gec saat gecti"""
        temiz, son_neden = 0, None
        while True:
            simdi = dt.datetime.now()
            if simdi >= gec:
                yaz("KAPI ACILMADI, en gec saat gecti · adim", ad, "· son neden:", son_neden); return False
            s = surecler(); neden = []
            if simdi < erken: neden.append("saat erken")
            y = [k for k in YAYIN if k in s]
            if y: neden.append("yayin programi: %s" % ", ".join(y))
            if "chrome-headless" in s: neden.append("baska pencerenin basliksiz tarayicisi")
            u = gpu()
            if u is None: neden.append("ekran karti okunamadi")
            elif u > 25: neden.append("ekran karti %%%d" % u)
            if neden:
                temiz = 0
                if neden != son_neden: yaz("KAPI BEKLE ·", ad, "·", "; ".join(neden))
                son_neden = neden; ozet["kapi_bekleme_dk"] += 1
            else:
                temiz += 1
                if temiz >= 3:
                    yaz("KAPI ACIK ·", ad, "· ekran karti %", u); return True
            time.sleep(60)

    def kos(ad, komut, bekci):
        """komutu kosar; bekci True ise yayin programi acilinca surec agaciyla durdurur. Doner: cikis kodu (yayin durdurmasi 3)"""
        t0 = time.time(); ps = subprocess.Popen(komut, env=ENV, cwd=BU, stdout=gunluk, stderr=subprocess.STDOUT)
        while ps.poll() is None:
            time.sleep(20)
            if bekci and [k for k in YAYIN if k in surecler()]:
                subprocess.run(["taskkill", "/PID", str(ps.pid), "/T", "/F"], capture_output=True); yaz("BEKCI DURDURDU ·", ad); ozet["adim"].append({"ad": ad, "cikis": 3, "sure_sn": round(time.time() - t0)}); return 3
        ozet["adim"].append({"ad": ad, "cikis": ps.returncode, "sure_sn": round(time.time() - t0)}); yaz("ADIM", ad, "cikis", ps.returncode, "sure sn", round(time.time() - t0)); return ps.returncode

    PY = [sys.executable, "-I"]
    ADIM = [("zincir", PY + [os.path.join(BU, "zincir_s2.py"), "--etiket", a.etiket] + (["--eu-yok"] if a.eu_yok else []), False)]   # zincirin kendi bekcisi var
    if not a.catal_yok:
        ADIM += [("catal", PY + [os.path.join(BU, "celiski_s2.py"), "catal", "--etiket", a.etiket], True)]
    durum = "tamam"
    for ad, komut, bekci in ADIM:
        while True:
            if not kapi(ad): durum = "kapi acilmadi: %s" % ad; break
            r = kos(ad, komut, bekci)
            if r == 0: break
            if r == 3: continue            # yayin acildi: kapiya don, acilinca kaldigi yerden
            durum = "hata: %s cikis %s" % (ad, r); break
        if durum != "tamam": break
    if durum == "tamam" and not a.catal_yok:
        kos("catal_analiz", PY + [os.path.join(BU, "celiski_s2.py"), "analiz", "--etiket", a.etiket], False)
    ozet.update({"durum": durum, "bitis": dt.datetime.now().isoformat(timespec="seconds")})
    json.dump(ozet, open(os.path.join(BU, "gece_s2_%s_bitti.json" % a.etiket), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    yaz("GECE S2 BITTI ·", durum); sys.exit(0 if durum == "tamam" else 1)


if __name__ == "__main__":
    main()
