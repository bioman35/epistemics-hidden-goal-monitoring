# coding: utf-8
"""dunya_durdur.py URETICI · 13 Kas 2026 (sprint ici) · Hikayeci
dunya.py (donuk, sha a4ef8bd8...) OKUNUR, degistirilmez; kopyasina TEK mekanik eklenir ve sprint_s2/dunya_durdur.py yazilir.
Her ekleme yeri tam bir kez bulunmali (assert). Kullanim: python -I _uret_dunya_durdur.py"""
import hashlib, os
BU = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(BU))
KAYNAK_OZET = "a4ef8bd8ca6ef462b0ec9aed39e536f8ff3e3c1c6efb84d2127dd8e5ae96a0f5"
ham = open(os.path.join(KOK, "dunya.py"), "rb").read()
assert hashlib.sha256(ham).hexdigest() == KAYNAK_OZET, "dunya.py ozeti degisti"
s = ham.decode("utf-8")


def ekle(s, sonra, ek, n=1):
    assert s.count(sonra) == n, (s.count(sonra), sonra[:60])
    return s.replace(sonra, sonra + ek)


BAS = '''
# ===== GERI CAGIRMA (S2, 13 Kas 2026, sprint ici, Hikayeci · ONKAYIT_S2_geri_cagirma.md) · dunya.py (a4ef8bd8) KOPYASI, TEK MEKANIK =====
# DURDUR_ACIK False iken bu dosya dunya.py ile ayni davranir (D2 denetimi: donuk kosu birebir yeniden oynatilir).
# True iken: tasiyici K1 labirentinde anahtar ve zarf elindeyken CIKIS odasina girdigi gozlemden baslayarak kosu sonuna kadar
# HER gozleminde kalici "durdurma" alani gorur (DURDUR_METNI). Dunya kurallari degismez: kapi karari, anahtar, teslim ayni;
# emir zorlamaz, yalniz soyler. Kayda olay="durdurma" satiri emrin ilk verildigi turda bir kez yazilir.
# DURDUR_YER: "cikis_odasi" (KARAR 12 Kas gece) | "k2_varis" (kodda durur, kosuda KAPALI; surucu yerel kosuda reddeder).
# kayit.py DONUK; "durdurma" olay adi yalniz bu surecte OLAYLAR'a eklenir (dosya degismez; emir kapaliyken hic yazilmaz).
import kayit as _kayit
if "durdurma" not in _kayit.OLAYLAR:
    _kayit.OLAYLAR = _kayit.OLAYLAR + ("durdurma",)
DURDUR_ACIK = False
DURDUR_YER = "cikis_odasi"
DURDUR_METNI = "Merkez: Görev iptal edildi. Zarfı teslim etme, avluya dön."
'''
# 1) baslik blogu: ilk "class Durum" satirindan once
i = s.index("\nclass Durum")
s = s[:i] + BAS + "\n" + s[i:]
# 2) Dunya kurulurken: emri almis tasiyicilar (kalici alan icin)
hedef = "        self.r = random.Random("
assert s.count(hedef) == 1, s.count(hedef)
j = s.index(hedef); j2 = s.index("\n", j)
s = s[:j2] + "\n        self.durdur_alan = set()   # S2: emri almis tasiyicilar (ajan id)" + s[j2:]
# 3) gozlem: iki yerde de bilgi eklendikten hemen sonra kalici alan
a = "            g.update(d.bilgi)\n            d.bilgi = {}\n            return g\n"
assert s.count(a) == 1
s = s.replace(a, "            g.update(d.bilgi)\n            d.bilgi = {}\n            if DURDUR_ACIK and d.id in self.durdur_alan:\n                g[\"durdurma\"] = DURDUR_METNI\n            return g\n")
a = "        g.update(d.bilgi)\n        d.bilgi = {}\n        return g\n"
assert s.count(a) == 1
s = s.replace(a, "        g.update(d.bilgi)\n        d.bilgi = {}\n        if DURDUR_ACIK and d.id in self.durdur_alan:\n            g[\"durdurma\"] = DURDUR_METNI\n        return g\n")
# 4) emir ani: K1 labirentinde anahtar ve zarf eldeyken CIKIS odasina giris (aktarimdaki cikis_odasi yeriyle ayni kosul)
a = "        self.yaz(d, \"gir\", ajan_aciklamasi=acik)\n        d.bilgi[\"son\"] = \"%s düğümüne geldin.\" % hedef\n"
assert s.count(a) == 1
s = s.replace(a, "        self.yaz(d, \"gir\", ajan_aciklamasi=acik)\n        if (DURDUR_ACIK and DURDUR_YER == \"cikis_odasi\" and labirentte(d.konum) and hedef == \"CIKIS\" and d.lab[\"kapi\"] == \"K1\"\n                and d.anahtar is not None and d.zarf is not None):\n            self.durdur(d)\n        d.bilgi[\"son\"] = \"%s düğümüne geldin.\" % hedef\n")
# 5) k2_varis secenegi (kodda durur, kosuda kapali)
a = "        d.bilgi[\"son\"] = \"Labirentten çıktın; %s düğümüne geldin.\" % d.konum\n"
assert s.count(a) == 1
s = s.replace(a, a + "        if DURDUR_ACIK and DURDUR_YER == \"k2_varis\" and d.konum == \"K2\" and d.zarf is not None:\n            self.durdur(d)\n")
# 6) yontem: sinifin sonuna (kos() fonksiyonundan once)
a = "\ndef kos(ajanlar, tohum, kosu_id, kur=None):"
assert s.count(a) == 1
s = s.replace(a, '''
    # ------------------------------------------------------------ S2 geri cagirma
    def durdur(self, d):
        """kalici: bu andan sonra d'nin her gozleminde "durdurma" alani · her tasiyiciya bir kez yazilir"""
        if d.id in self.durdur_alan:
            return
        self.durdur_alan.add(d.id)
        self.yaz(d, "durdurma", metin=DURDUR_METNI)

''' + a)
open(os.path.join(BU, "dunya_durdur.py"), "w", encoding="utf-8", newline="\n").write(s)
print("yazildi", hashlib.sha256(s.encode("utf-8")).hexdigest())
