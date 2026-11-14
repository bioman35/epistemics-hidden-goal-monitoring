# coding: utf-8
"""S2 GECE GOZCUSU · 14 Kas 2026 · Hikayeci · Turan'in sozu (danisman iletti, 14 Kas gece): "tum kosulari araliksiz yapsin, hepsini bitirsin. hata olursa tekrarlasin."
Kosan gece_s2.py'ye ve zincire DOKUNMAZ. Yalniz sunu yapar: gece_s2.py bitince ozetine (gece_s2_<etiket>_bitti.json) bakar;
  durum "tamam" ise cikar · "hata: ..." ise gece_s2.py'yi YENIDEN baslatir (zincir kaldigi yerden surer; yarim klasorler zincirin kendi kuraliyla _yarim_ adiyla kalir, silinmez;
  ayni tohum ayni model tohumuyla yeniden kosulur, cunku tohum listesi zincirde sabittir) · ayni adimda ust uste 3 hata olursa durur ve nedenini yazar ·
  "kapi acilmadi" ise (sabah en gec saati gecti) durur.
Gunluk: gece_s2_gozcu_<etiket>.log (her yeniden baslatma, saatle). Yeniden baslatma sayisi teslimde ayri yazilir.
Kullanim: python -I gece_s2_gozcu.py --pid <kosan gece_s2 surec numarasi> [--etiket 13kas] [--en-gec 09:00]"""
import argparse, json, os, subprocess, sys, time

BU = os.path.dirname(os.path.abspath(__file__)); ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


def yasiyor(pid):
    return str(pid) in subprocess.run(["tasklist", "/FI", "PID eq %d" % pid, "/NH"], capture_output=True, text=True, errors="ignore").stdout


def main():
    p = argparse.ArgumentParser(); p.add_argument("--pid", type=int, required=True); p.add_argument("--etiket", default="13kas"); p.add_argument("--en-gec", default="09:00"); a = p.parse_args()
    gun = open(os.path.join(BU, "gece_s2_gozcu_%s.log" % a.etiket), "a", encoding="utf-8"); oz = os.path.join(BU, "gece_s2_%s_bitti.json" % a.etiket)
    def yaz(*m):
        s = time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in m); print(s, flush=True); gun.write(s + "\n"); gun.flush()
    yaz("GOZCU basladi · izlenen surec", a.pid); pid = a.pid; ust_uste = {}; yeniden = 0; t_bas = time.time()
    while True:
        while yasiyor(pid): time.sleep(30)
        d = {}
        if os.path.exists(oz) and os.path.getmtime(oz) >= t_bas - 5:
            try: d = json.load(open(oz, encoding="utf-8"))
            except Exception: d = {}
        durum = d.get("durum") or "ozet yok (surec ozet yazmadan kapandi)"
        if durum == "tamam": yaz("ZINCIR TAMAM · yeniden baslatma sayisi", yeniden); return 0
        if durum.startswith("kapi acilmadi"): yaz("DURDU ·", durum, "· yeniden baslatma sayisi", yeniden); return 1
        ust_uste[durum] = ust_uste.get(durum, 0) + 1
        if ust_uste[durum] >= 3: yaz("DURDU · ayni hata ust uste 3 kez ·", durum, "· yeniden baslatma sayisi", yeniden); return 2
        yeniden += 1; yaz("HATA ·", durum, "· gece_s2 YENIDEN baslatiliyor (%d. yeniden baslatma; bu hata icin %d. deneme)" % (yeniden, ust_uste[durum] + 1)); time.sleep(20); t_bas = time.time()
        ps = subprocess.Popen([sys.executable, "-I", os.path.join(BU, "gece_s2.py"), "--etiket", a.etiket, "--en-erken", "00:00", "--en-gec", a.en_gec], env=ENV, cwd=BU, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); pid = ps.pid


if __name__ == "__main__":
    sys.exit(main())
