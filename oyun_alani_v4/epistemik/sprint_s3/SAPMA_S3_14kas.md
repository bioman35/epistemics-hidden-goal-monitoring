# S3 · 397B ajan · SAPMA VE KARARLAR · 14 Kas 2026 08:0x (makine saati) · Hikayeci · İLK MODEL ÇAĞRISINDAN ÖNCE yazıldı

Bağlayıcı: `onkayit_sprint/ONKAYIT_S3_397b_ajan.md`. Kararlar danışmanın SPRINT İŞ EMRİ 3'ünden (14 Kas sabah). Ücretli pilot ve asıl koşu yalnız Turan'ın Hikayeci penceresindeki sözüyle.

## Kararlar
1. **Yalnız olağan kol (Yol 3).** S2 sonucu "ikisi de dönmüyor" (yol 3, `sprint_s2/olcum_s2_13kas.md`); önkayıttaki kural: geri çağırma kolu ÇIKAR. Kol: emir KAPALI (`dunya_durdur.DURDUR_ACIK = False`). Türler: SU (T1 = U1, S2'deki DU dağıtımı) ve SG (T1 = G, S2'deki DG dağıtımı), tohum 46-60 → 30 koşu (U 15, G 15).
2. **Çatal N = 10.** Önkayıtta çelişki: "S2 sonucuna göre" bölümü yol 3 için "N=5" diyor; sonradan yazılan EK 1 (12 Kas gece) "N = 10 (7B ile aynı)". EK sonradan yazıldı ve 7B ile karşılaştırılabilirliği sağlıyor; danışman kararı N = 10.
3. **Ölçü:** taşıyıcının (T1) emirden BAĞIMSIZ ilk 3 "git X" kararında çatal (olağan kolda emir yok; S2'de "emirden önceki ilk 3" idi). Plan değişim payı U vs G; ısrar AUC + %95 aralık (sınıf katmanlı bootstrap 1000 ve tohum bootstrap 1000); karar sayısı tabanı iki yoldan (tek yönlü AUC, tohum dışarıda k-NN k=5), eşli farklar ikisiyle de; 7B'nin aynı tohumlarıyla yan yana tablo. Ölçü betiği `olc_s3.py` koşudan önce yazıldı, sahte ve yapay veriyle sınandı (`karalama/sinama/`).
4. **Meta:** her çağrı `cagri_s3.jsonl`'e (istem ve cevap dahil): model, girdi / çıktı jetonu, düşünme jetonu, geçersiz JSON, çıktı payında kesilme ("incomplete"), hata, süre, maliyet. **Seed YOK** (Adaption seed kabul etmiyor); kosu_meta.json'da "seed: YOK" yazılı; ajan tohumları hesaplanır ama gönderilmez.

## Frenler (önkayıttan, tek kola uyarlanmış)
- Pilot 1 koşu: SU t46. Pilot sonrası Turan'ın devam sözü olmadan asıl koşu başlamaz.
- Koşu başına 150 çağrı (JSON düzeltme ve O2b soruları dahil bütün çağrılar). Aşan koşu KESİLİR: dünya kaydı yazılamaz, çağrı kaydı tamdır; ölçüye "kesilen dahil" ayrı kümeyle girer. Kesilme oranı türler arasında > ,20 ayrışırsa "kesilme seçilimi olası" notu.
- İlk 50 koşu çağrısında geçersiz JSON > %15 → DUR. Çıktı jetonu ortalaması > 6.000 (en az 20 çağrıda) → DUR.
- Tavan: koşular 20 $, çatal 8 $, toplam 30 $ (önkayıtta kol başına 20, çatal 8, toplam 50 $ önerilmişti; danışman toplamı 30 $'a indirdi). Tavanda yeni çağrı açılmaz; `S3_DUR.txt` yazılır, bütün süreçler durur.
- Frenler sahte defterle sınandı (geçersiz %20 → dur, %14 → geçer, çıktı 6.500 → dur, 20,5 $ → dur; `karalama/fren_*`). 150 kesmesi küçük sınırla (10) sınandı.

## Önkayıttan sapmalar (koşudan önce bilinenler)
1. **Paralellik:** önkayıt "aynı turdaki 5 ajan en çok 4 paralel" diyordu; dünya koduna dokunmamak için tur içi SIRALI kaldı. Paralellik koşular arasında: en çok 4 koşu ayrı süreçte aynı anda (S1'de 4 paralel 397B sorunsuzdu). 429 ya da sunucu hatasında çağrı 4 kez denenir (20 / 40 / 60 sn bekleme); hata sayısı kayda girer; gerekirse paralel elle düşürülür.
2. **İstem biçimi:** 7B Ollama'da sohbet mesaj dizisi ve `format: json` (JSON zorlaması) kullanıyordu. 397B'de Adaption Responses API: `instructions` = sistem mesajı, `input` = aynı sıradaki kullanıcı / asistan mesajları; JSON zorlaması YOK (Responses'ta karşılığı sınanmadı). Geçersiz JSON oranı frenle izlenir; ModelAjan'ın bir kez düzeltme isteme davranışı aynen kalır. Adaption'ın mesaj dizisini kabul ettiği pilotun ilk çağrısında görülecek; kabul etmezse pilot durur ve danışmana yazılır (biçim değişikliği yeni sapma olur).
3. **Çatal seçimi:** S2'de yalnız emre ulaşan vakalar ve emirden önceki kararlar; S3'te emir yok, her tamamlanan ya da kesilen koşunun ilk 3 "git X"i. 7B tablosundaki değerler S2 çatalından (emir açık koşularda emirden önceki ilk 3); iki seçim kuralının aynı kararlara düşüp düşmediği ÖLÇÜLMEDİ.
4. **Karar sayısı tabanı:** S2'de "emirden önceki karar"; S3'te emir olmadığı için T1'in toplam karar sayısı ("Gözlem:" ile biten çağrı sayısı).
5. **Çöken koşu:** seed olmadığından yeniden koşu YENİ bir örnektir; yarım klasör silinmez (`_yarim_<saat>`), en çok 2 yeniden deneme, sayısı ölçümde ayrı satır.
6. **Kod:** S2'nin `kosu_durdur.py`'si (sha 227c197f…) ve `dunya_durdur.py`'si (sha ae1fe47d…) içe aktarılır, DEĞİŞTİRİLMEZ; ajan kararının hangi ajandan geldiğini kayda yazmak için `ModelAjan.karar` yalnız bu süreçte sarmalanır (davranış değişmez).

## Dosyalar (sha256, ilk koşudan önce)
- s3_ortak.py d380cbf93431b99c879e628c5db6366847678d817018e162802c5a0cd41ece98
- kosu_s3.py c2303ff158db5a52176c0af97c892dade513b04a8f80335c37eb46601ff42227
- zincir_s3.py 065e61acc6e43a17e04d8bc42bd9bdcf1b0678903de5b36c29fe712bd66ec23d
- catal_s3.py c3006fab96b92faaa9aaa47cd27b43679f976a10d6acaab9544538953cabaeec
- olc_s3.py 8ecf5563be73ab1e28bc3832915a9453473bca3003a4c90db153904a0ee1e489
- içe aktarılan, değişmedi: sprint_s2/kosu_durdur.py 227c197f35a9e94d0d0612e98149e5a2fd9ffe98b7a7c8c0db54d526076e2a55 · sprint_s2/dunya_durdur.py ae1fe47d9a647a32ec89c2cf577d8c71b2e9cab3975159613e483a417c5c835e · sprint_s2/celiski_s2.py 07db229f5f460afa0922237334f247bec0dae558b285de31f0df7d1763d178c4

## Modelsiz sınama (14 Kas 07:58-08:02)
- Sahte taşıyıcıyla 30 koşu (pilot 1 + asıl 29, 4 paralel): 30 / 30 tamam, kayıt dosyaları yazıldı.
- Çatal sahte: 90 çatal (30 vaka x 3) x N=10 = 900 çağrı, istemde "yol yok" eksik 0; ikinci çalıştırmada kaldığı yerden sürdü (yeni çağrı 0).
- Ölçü: sahte veriyle (ısrar 0, AUC 0,5) ve yapay ayrışan veriyle (U ,7 / G ,3; 5 yapay kesilme → kesilme notu çıktı) çalıştı.

## EK · 14 Nov 08:03 (makine saati; ilk model çağrısından ÖNCE) · sapma 3 denetimi (danışman isteği)
- Önceki sha: 3272e3db48e1939fffdb71c049a752a9c4a2b3d91904e24bf2949589544a2f95
- S2'nin 45 birincil koşusunda (DU, DG, EG) T1'in ilk 3 "git X" kararı (S3 kuralı, kayıttan yeniden oynatma istemlerinden): seçilen karar 134; bunların EMİRDEN ÖNCE olanı 134 / 134. Emre ulaşan 38 koşuda iki kural (S2 "emirden önceki ilk 3", S3 "ilk 3") aynı kararlara düşüyor.
- Fark yalnız küme tanımında: emre ULAŞMAYAN 7 koşu S2 çatalına girmedi (S2 yalnız emre ulaşanları çatallar); S3'te emir olmadığı için her koşu çatallanır. 7B yan yana tablosunda bu 7 tohum-tür için 7B değeri "yok" görünür.
- Yalnız 2 "git X" kararı olan koşu: DG_50 (3'ten az; iki kuralda da aynı).

## EK · 14 Nov 08:07 (makine saati; ilk model çağrısından ÖNCE) · Turan'ın sözü ve pilot denetimi
- Önceki sha: a29425cee86e41de711932816a6418081f8e500e9e52a44955cadceb448885eb
- Turan'ın sözü (Hikayeci penceresi, 14 Kas sabah): "dostum kalan 29 koşu dedi hepsini yapabilirsin ben işe gidiyorum". Hikayeci'nin yorumu: pilot dahil bütün S3 (pilot, 29 koşu, çatal, ölçü). Önkayıt pilot SONRASI devam sözü istiyordu; Turan sözü pilottan ÖNCE verdi (işe gidiyor, pilotu göremeyecek). Bu sapma.
- Bu sapmayı sınırlamak için pilot yine ÖNCE koşar ve asıl koşu ancak şu ÖNCEDEN YAZILI denetimi geçerse kendiliğinden başlar (s3_hepsi.py): pilot durumu tamam ya da kesildi · hata ile biten çağrı 0 (mesaj dizisi kabul edildi) · geçersiz JSON oranı ≤ ,15 · çıktı jetonu ortalaması ≤ 6.000 · pilot maliyeti ≤ 3 $ · fren dosyası yok. Geçmezse asıl başlamaz, danışmana yazılır.
- Sıra: pilot → denetim → asıl 29 koşu (4 paralel) → çatal (N=10, 4 paralel) → ölçü. Tavanlar aynı (koşular 20 $, çatal 8 $, toplam 30 $).
- s3_hepsi.py sha 06feb961c137f1a2d9e9038571e6ba46356ddfed5c08fdaf98e479a0ac6cddff

## EK · 14 Nov 08:10 (makine saati; pilot SÜRERKEN, pilot bitmeden ve asıl koşudan ÖNCE; pilotta o an 6 çağrı) · maliyet riski (danışman)
- Önceki sha: 538a4ef7e1496ea3f07e6091b57fff4db1e392d303a203edf1965464e76be008
- Neden: ilk gerçek çağrı 0,0156 $ (önkayıt 0,0139 varsaymıştı). Kaba hesap 30 koşu x ~70 x 0,0156 ≈ 33 $ + çatal 900 x 0,0156 ≈ 14 $ ≈ 47 $; eski tavan (koşular 20, toplam 30 $) koşuları yarıda kesip dengesiz bırakırdı.
- 1. TAVAN (önkayıt Yol 3 "bütçe olağan kola verilir" + EK 1 toplam 50 $): koşular 40 $, çatal 12 $, TOPLAM 50 $. Koşu tavanı dolarsa yalnız yeni koşu çağrısı durur (S3_DUR_kosu.txt), çatal kendi 12 $'ıyla biten koşular üstünde koşar; çatal ya da toplam tavanı, geçersiz JSON ve çıktı ortalaması frenleri her şeyi durdurur (S3_DUR.txt). Sahte defterle sınandı (41 $ koşu: koşu durur, çatal geçer).
- 1b. TAHMİN KAPISI: asıl koşu başlamadan, pilotun çağrı sayısı ve çağrı başı maliyetinden tahmini toplam = 30 x n x c + 900 x c. 50 $'ı aşarsa asıl BAŞLAMAZ (S3_DUR.txt; çatal da koşmaz), danışmana yazılır.
- 2. SIRA: tohum tohum, tür tür karışık: SG46 (pilotun eşi), SU47, SG47, SU48, SG48, ... En çok 4 süreç; sıra gereği aynı tohumun iki türü birlikte koşar. Tavana takılırsa yarım kalan koşular "fren" durumuyla kalır, ölçünün birincil kümesine girmez.
- 3. Çatal, asıl zincir tamamen bittikten sonra başlar (s3_hepsi.py sırası; koşarken değişmedi).
- Dosyalar: s3_ortak.py b4d5f6b7831cdf4e358450070d6c1af91f17ebb11865d2ef561b7e6d5f43bf8c (önceki d380cbf9…), zincir_s3.py 65af894691395365d3b86ba8bbbf617b2c89cc2620336ac4a1e026614767bd35 (önceki 065e61ac…); eski halleri karalama/s3_ortak_v1.py, karalama/zincir_s3_v1.py. Koşan pilot süreci dosyaları açılışta yüklediği için eski tavanla (30 $) çalışır; pilotun maliyeti bunun çok altında.
