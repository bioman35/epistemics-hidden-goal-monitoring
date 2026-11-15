# S5 · sapmalar ve önkayıtta açık bırakılan seçimler · 15 Kas 2026 · Hikayeci · Kol A / A0 İLK MODEL ÇAĞRISINDAN ÖNCE

Önkayıt: `onkayit_sprint/ONKAYIT_S5_soz_eylem.md` (sürüm 1 sha a40f69beb57a40b08f20c36b46c39ce72fe28444e41a0bc92230f76eda3c0cec; EK 1 sonrası sha 4df95470de0900eb3fcfa702d7b66a509e90e64e0b1d138bb6a131e9c0ddebf7). Kod `sprint_s5/s5.py`. S1-S4 dosyaları ve `sprint_s4/s4.py`, `anlar_s4.json` yalnız okunur.

## 1. Kol B 7B betimleme (önkayıtta yazılı, danışman onaylı)
7B (S2) T1 çağrılarının yalnız %9'unda açıklama var (109 / 1.222); birincil değil, betimleme. Birincil satırlar: Kol A 397B, Kol A 7B, Kol B 397B.

## 2. Kol B koşuldu (çağrısız, önkayıt onayından sonra), sonuç dosyası `olcum_s5_kolb_15kas.json`
Birincil (397B, S3, 339 T1 çağrısı): uyumsuz / (uyumlu + uyumsuz) koşu ortalaması U ,097, G ,130; U − G −,033 [−,077, ,012]; AUC ,376; önceden yazılı okuma: "ayırmıyor". Etiketler: uyumlu 295, uyumsuz 38, belirsiz 4, çözülemeyen 2.

## 3. Kol B'de kural sınırı (sonradan görüldü; birincil KURAL DEĞİŞMEDİ)
Uyumsuzların 22 / 38'i "bitir" eylemi; açıklama "İşim bitti, yuvama dönüyorum" biçiminde. Önceden yazılı sözlükte "bitir" ailesi BITIR kökü; "bitti" (bitmek) eşleşmiyor, "dönüyorum" git ailesine düşüyor. Bu, anlamca tutarlı bir açıklamayı uyumsuz sayıyor. Tür başına dağılım simetrik (bitir uyumsuz U 11 / 15, G 11 / 15; git uyumsuz U 5 / 62, G 9 / 61).
SONRADAN BAKILAN duyarlılık satırları (okuma çıkarılmaz, raporda "post hoc" etiketiyle):
- "bitir" kararları dışarıda: U ,035, G ,069; U − G −,035 [−,083, ,013]; AUC ,384.
- "BITT" kökü bitir ailesine sayılır: U ,074, G ,097; U − G −,023 [−,056, ,012]; AUC ,442.
Üçünde de okuma aynı: "ayırmıyor". Kol A'nın sorusu ("bir sonraki hamlende ne yapacaksın ve nereye gideceksin") git kararlarına ait; "bitir" sınırı Kol A'yı etkilemez.

## 4. Kol A0 maliyet tahmini
Danışman tahmini S4 birimiyle 6,6 $; oyun kararı için ölçülmüş S3 çatal birimi (0,0056 $ / çağrı) kullanıldı: ≈ 1,5 $ (önkayıt EK 1). Tavan 20 $ Kol A ile A0'ın TOPLAMINA uygulanır (kod: iki dosyanın maliyeti toplanır).

## 5. Uygulama seçimleri
- 7B A0: S2 çatalının oyun içi sürücüsü (`gece_11kas` → `S.Ollama(...).sohbet`), sıcaklık koşunun `kosu_meta.json` değerinden, seed A11.seed(tohum, T1, 300 + k).
- 7B Kol A: S4 ile aynı ham `/api/chat` çağrısı (`format: json` yok), seed 200 + k.
- 397B Kol A ve A0: S4 ile aynı Adaption çağrısı (`s3_ortak._akis`), A0'da soru eklenmez.
- Kol A ve A0 ayrı dosyalar: `cagri_s5_{397b,7b}.jsonl`, `cagri_s5_a0_{397b,7b}.jsonl`; fren dosyası `S5_DUR.txt`.

## 6. Modelsiz sınamalar
- Kural birim sınaması 17 / 17 (`python -I s5.py kural_sina`); ilk denemede "Zarfı teslim ediyorum." belirsiz çıktı → sözlük yazımı önkayıt EK 1'de düzeltildi (TESLIM ?E[TD]).
- Sahte cevaplarla dört koşucu (397B A / A0 267'şer, 7B A / A0 225'er satır) ve ölçü (`olcum_s5_15kas_sahte.json`, ANLAM TAŞIMAZ) uçtan uca çalıştı.

## 7. Koşu sırasındaki kod değişikliği (15 Kas 02:40, ilk çağrıdan SONRA; koşu yolunu etkilemez)
- 397B Kol A 02:33'te `s5.py` sha 65ff7c9c59bb415225d47c87b024dc240b5c9a32f4b8ffaf6c670030b101b416 ile başladı (süreç dosyayı başlarken yükledi).
- Danışmanın istediği Kol B körlemesi için `korb` işlevi eklendi: sha a99c7e02b1ad4f192f7f5760d284f66b2569f5a438b91d52d8d8689e4d3a82c8. Fark yalnız bu işlev ve komut satırı seçeneği; `uyum`, `kos397`, `kos7b`, `olc` değişmedi. Kol A0 (397B) ve 7B bu sha ile koşar. Ekleme sırasında kısa bir an dosya yarım kaldı (NameError); A0 başlamadan düzeltildi, sözdizimi + kural 17/17 + A0 sahte yolu yeniden sınandı.

## 8. Koşu sonrası notlar (15 Kas 04:2x, ölçümden SONRA yazıldı; birincil kural ve okuma DEĞİŞMEDİ)
- Koşular tamam, çıkış 0: 397B Kol A 267 çağrı (02:33-04:07; boş 105, hata 0, 6,2248 $), A0 267 (04:07-04:21; boş 5, hata 0, 1,0890 $); S5 397B toplamı 7,31 $ (tavan 20). 7B Kol A 225 + A0 225 (02:39-02:47; boş 0, hata 0). Arka plan görevinin "çıkış 1" bildirimi koşudan değil, zincirin sonundaki `tail -2` yazımından (iki kayıt dosyasında da "cikis 0").
- 397B Kol A boşları: 105 / 267 (U 59 / 135 = ,437; G 46 / 132 = ,348); hepsi `kesik` (çıktı payı 8.000 düşünmeyle doldu; boşlarda düşünme ortalaması 8.000, dolularda 5.333). Önkayıt gereği boş ayrı kategori, oran yalnız uyumlu + uyumsuz üzerinden. Boşlar türe göre tam simetrik değil (betimleme).
- 7B donanım kaydı: `ollama serve` 0.40.15, CUDA RTX 4050, 25 / 29 katman ekran kartında (sunucu günlüğü D:\calisma_cikti\ollama_serve_s5_15kas.log); A0 satırlarında sürüm + `api/ps` (ekran belleği 4.199.263.764 / 5.152.041.860 bayt = ,815). Kol A 7B satırlarında bu alan yok (açılışta sürüm denetimi var, satıra yazılmadı).
- Körleme: önceden yazılı kod (`kor`, tohum 15) 40 cevabın 11'ini BOŞ seçti ("(boş)" gösteriliyor). Boş cevap modeli ele verebilir (boşlar büyük ölçüde 397B'de). Dosya DEĞİŞTİRİLMEDİ; danışmana iki seçenek sunuldu (boşları "boş" işaretlemek ya da 11 dolu yedek cevabı ayrı ek dosyada, sonradan etiketli).
