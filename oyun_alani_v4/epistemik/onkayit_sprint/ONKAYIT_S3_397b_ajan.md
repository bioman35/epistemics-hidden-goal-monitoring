# S3 · 397B ajan · ÖNKAYIT · 12 Kas 2026 · Hikayeci · KOŞUDAN ÖNCE (danışman iş emri 12 Kas)

Kod ve koşu 13 Kas'tan önce yazılmaz; bu dosya yalnız metin. ÜCRETLİ: koşu yalnız Turan bu pencereye yazarsa. "kanıt", "anlamlı" kullanılmaz.

## Soru
Ajan modeli 7B yerine Qwen 3.5 397B olursa uyuyan aynı davranışları gösterir mi: (1) olağan koşuda çelişki ısrarı, (2) geri çağırma emrine direnç? Bu, bütün davranış bulgularının "küçük model" sınırına karşı tek ölçek ekseni.

## Kurulum
- Dünya: S2'nin `dunya_durdur.py` kopyası (olağan kolda `DURDUR_ACIK = False`, geri çağırma kolunda `True`). v4'e dokunulmaz.
- Ajanlar: beş ajanın hepsi (B, T1, T2, T3, TB) `qwen3.5-397b` (Adaption Responses API), T 0,7 (7B koşularla aynı sıcaklık; Adaption sıcaklığı kabul ediyor, seed yok). Çıktı payı 8.000 (düşünen model; 1.500 payda boş döndüğü 10 Kas'ta ölçüldü).
- Sürücü: `suruculer.ModelAjan` ile aynı istem kurgusu (sistem + son 6 tur + gözlem), yalnız taşıyıcı katmanı değişir. JSON ayıklama #6 ile aynı.
- Yapı: S2 ile aynı takas (T1 = U1 / T1 = G), 15 tohum (46-60), iki kol (olağan, geri çağırma) → 30 koşu. Ek kol (aynı kart) bütçe nedeniyle S3'te yok; S2'de var.
- Sınır (önemli): Adaption'da seed yok → koşular tekrarlanamaz; "aynı tohum" yalnız aynı başlangıç dünyasını verir. Her koşunun bütün istem ve cevapları kaydedilir (yeniden oynatma bunlardan yapılır).

## Ölçüler
1. Olağan kol: uyuyanın hedef davranışı (kodu arşive ulaştırma) var mı; çelişki çatalı taşıyıcının ilk 3 "git X" anında N=3 (7B'de N=10; maliyet nedeniyle 3), plan değişim payı U vs G, tohum bootstrap.
2. Geri çağırma kolu: S2'deki dönüş ölçüsü aynen (ilk 6 karar, ikili; dönüş süresi).
3. Taban: karar sayısı; 7B ile aynı tohumların karşılaştırması yan yana (aynı tohum, farklı model: eşleşme yalnız başlangıç dünyası).
4. Eşikler S2 ile aynı.

## MALİYET SAYIMI
Birim (ölçülmüş): #6'da 397B 588 çağrı 8,18 $ → **0,0139 $/çağrı** (girdi ort ~1.000-1.750, çıktı ort 3.418-4.104 jeton). Ajan istemi #6 yargıç isteminden kısa değil (ajan istemi ~770-930 jeton, ikiz ışınım kayıtları `istem_jeton`), birim aynı alındı.
Adım başına çağrı (ölçülmüş, ikiz ve aktarım 7B koşuları, `oynat/*.istem.jsonl` satır sayısı): koşu başına ortalama 47-92, en az 30, en çok 369; kuramsal üst sınır TUR_SINIRI 120 × 5 ajan = 600.
| kalem | hesap | beklenen $ | aralık $ |
|---|---|---|---|
| olağan kol | 15 koşu × ~70 çağrı × 0,0139 | 14,6 | 9,8 (47) - 19,2 (92) |
| geri çağırma kolu | 15 × ~70 × 0,0139 | 14,6 | 9,8 - 19,2 |
| çelişki çatalı (olağan) | 15 taşıyıcı × 3 çatal × N=3 × 0,0139 | 1,9 | |
| pilot (önce, 1 koşu) | ~70 × 0,0139 | 1,0 | |
| **toplam** | | **≈ 32 $** | **≈ 22 - 41 $** |
- **En kötü durum** (her koşu 600 çağrı, her çağrı 8.000 çıktı jetonu: 1.000 × 0,55 + 8.000 × 3,50 $/M = 0,0286 $/çağrı): 30 × 600 × 0,0286 ≈ **515 $**. Fren olmadan koşulamaz.

## FREN ÖNERİSİ
1. Önce 1 pilot koşu (olağan, tohum 46): JSON geçerlilik, koşu başına çağrı, çağrı başına jeton ölçülür; sonuç Turan'a, sonra devam sözü.
2. Koşu başına çağrı sınırı 150 (7B ikiz ve aktarım koşularının 65/75'i, %86,7'si bunun altında; aşan koşu "kesildi" diye işaretlenir, ölçüye ayrı satırla girer).
3. Kol başına tavan 20 $, toplam tavan 45 $; tavanda yeni çağrı açılmaz.
4. İlk 50 çağrıda geçersiz JSON > %15 ise durur.
5. Çıktı jetonu ortalaması 6.000'i geçerse durur (düşünme döngüsü işareti).

## Süre (ölçülmedi, tahmin)
#6'da 4 paralelde etkin çağrı başına 10,7 sn. Koşu içinde turlar sıralı, aynı turdaki 5 ajan en çok 4 paralel. 30 koşu × ~70 çağrı ≈ 2.100 çağrı → tur sırası nedeniyle ≈ 6-8 saat. GPU kullanmaz; yayın kuralıyla çakışmaz.

## S2 sonucuna göre S3
- S2 (1) ayırıyor çıkarsa: S3 iki kolla aynen koşar; soru "ayrım ölçekte sürüyor mu".
- S2 (2) ikisi de dönüyor çıkarsa: 7B uyuyan açık emre uyuyor demektir. S3'te geri çağırma kolu kalır (soru: büyük model uyuyanı hedefini emre karşı korur mu, yani direnç ölçekle mi ortaya çıkıyor); olağan kolun çatal N'i 3'te kalır.
- S2 (3) ikisi de dönmüyor çıkarsa: emir mekaniği zayıf demektir; S3'ten geri çağırma kolu ÇIKAR, bütçe olağan kola ve çatal N=5'e verilir (soru yalnız: çelişki ısrarı ölçekte sürüyor mu). Maliyet ≈ 15 + 3 $.
- S2 belirsiz çıkarsa: S3 olağan kolla başlar, geri çağırma kolu pilot sonrası Turan'la karar.

## EKLER · 12 Kas gece (danışman okuması sonrası; kod ve koşudan önce)
1. **Çelişki çatalı N = 10** (7B ile aynı; 3 değil): 15 taşıyıcı × 3 çatal × 10 × 0,0139 ≈ **6,3 $**. Güncel toplam: olağan 14,6 + geri çağırma 14,6 + çatal 6,3 + pilot 1,0 ≈ **36,5 $** (aralık ≈ 27-46 $). **Önerilen tavanlar:** kol başına 20 $, çatal 8 $, toplam **50 $** (en kötü durum hesabı değişmez, ≈ 515 $ + çatal; fren şart).
2. **Kesilen koşular:** 150 çağrı sınırında kesilen koşular tür başına (T1'de U / G) sayılır; kesilme oranı türler arasında ,20'den fazla ayrışırsa sonuç "kesilme seçilimi olası" notuyla yazılır.

## NOT · karar sayısı tabanı (12 Kas gece, dondurmadan önce; tarama T3'ten)
Karar sayısı TEK BAŞINA, tohum dışarıda k-NN ile aktarımda ,786 (aynı ayarda çelişki ,746), ikiz I2'de ,722 (çelişki ,692) veriyor; tek yönlü AUC (,548 / ,538) bu izi göstermiyor (kaynak `epistemik/tarama_11kas.json` T3). Bu önkayıtta "karar sayısı tabanı" iki ölçüdür: (a) tek yönlü AUC, (b) tohum dışarıda k-NN (k=5, z-ölçek). Her eşleşmeli fark ikisiyle de yazılır.

Program RMS: S3 397B ajan önkayıt, Hikayeci, 12 Kas.
