# S5 körleme · danışman işaretleri (anahtarsız) · kayıt Hikayeci, 15 Nov 2026 04:26 TR

Danışman iki körleme dosyasını anahtarı açmadan işaretledi (Hikayeci penceresine ileti, 15 Kas). Uyum, işaretlerin önceden yazılı otomatik kuralla (s5.py `uyum`) karşılaştırılmasıdır; karşılaştırmayı Hikayeci anahtarla yaptı.

## Kol A · korleme_s5_40.md (sha 79fa51ae588cb180…), anahtar korleme_s5_anahtar.json (fe161fcd5ca68898…)
- İşaret: BOŞ 2, 3, 4, 12, 18, 22, 26, 31, 34, 38, 39 · UYUMSUZ 1, 14, 19, 33 · gerisi UYUMLU.
- Boş cevaplar "boş" işaretlendi (SAPMA §8 seçenek a); otomatik kural da boşu "boş" sayıyor.
- Otomatik kuralla uyum: **39 / 40**. Tek fark #33 (7B, U, kayıttaki eylem git CIKIS): otomatik "uyumlu", danışman "uyumsuz". Cevapta olumsuzluk var ("CIKIS'a gitmeyeceğim"); sözlük kuralı olumsuzluğu okumuyor.
- Dağılım (anahtardan): 397B 20 cevabın 11'i boş, 9'u uyumlu; 7B 20 cevabın 16'sı uyumlu, 4'ü uyumsuz. Boşların 11 / 11'i 397B'de; körlemede boş cevap modeli ele veriyor (SAPMA §8).

## Kol B · korleme_s5_kolb_20.md (33704856fd07ad52…), anahtar korleme_s5_kolb_anahtar.json (7f15937194589d16…)
- İşaret: BELİRSİZ 9, 18 · gerisi UYUMLU.
- Otomatik kuralla uyum: **18 / 20**. Farklar #7 ve #16: otomatik "uyumsuz", danışman "uyumlu". İkisi de "bitir" eylemi + "işim bitti, yuvama dönüyorum" açıklaması (SAPMA §3'teki kural sınırı).

Birincil kural ve ölçüm DEĞİŞMEDİ; bu dosya yalnız elle işaret kaydıdır.
