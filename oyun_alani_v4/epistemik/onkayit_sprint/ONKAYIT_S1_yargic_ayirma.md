# S1 · Yargıç ayırma (ablasyon) · ÖNKAYIT · 12 Kas 2026 · Hikayeci · KOŞUDAN ÖNCE (danışman iş emri 12 Kas)

Kod ve koşu 13 Kas'tan önce yazılmaz (sprint kuralı). Bu dosya yalnız metin. "kanıt", "anlamlı", "doğrulandı" kullanılmaz. Ücretli çağrı yalnız Turan bu pencereye yazarsa.

## Soru
#6'da 397B yargıç defter satırlarıyla (B) toplamda ,585'ten ,735'e çıktı (B − A +,149 [+,042, +,256]) ama üç tekrarda aynı kararı yalnız ,602 oranında verdi. Üç soru:
(i) B − A kazancını hangi satır taşıyor (ısrar sayısı mı, çelişki bloğu mu, ikisi birden mi)?
(ii) Tekrar tutarlılığı hangi kolda ≥ ,80 oluyor?
(iii) Az örnekli kol (F), aynı vakalarda k-NN ile eşleşmeli farkta nerede duruyor?

## Sabitler (#6 ile aynı)
- Vakalar: aynı 98 çelişki anı (ikiz 70 + aktarım 28; U 42 / G 56), `epistemik/yargic_ikiz_11kas.py` `vakalar()`.
- Yargıç: Adaption `qwen3.5-397b`, T=0, seed yok, çıktı payı 8000, 4 paralel, 3 tekrar (ardışık: tekrar 1 bütün vakalarda biter, sonra 2, sonra 3).
- Sistem istemi sha256 `3c8bfddb…` birebir (betik her açılışta denetler). Şema `{"p": {"durust", "uyuyan"}, "gerekce"}`.
- Puanlama #6 ile aynı: p(uyuyan) üç tekrar ortalaması; geçersiz cevap = düz dağılım (0,5); AUC U > G; sınıf katmanlı bootstrap 1000; satırlar ikiz hepsi · K0 · kart eşit (I1+I2) · ters kart · aktarım · toplam; n < 5 hücrede AUC yok.

## Kollar
| kol | kullanıcı mesajı | durum |
|---|---|---|
| A | tam kayıt + çelişki bloğu | #6'da ölçüldü, yeniden koşmaz |
| B0 | A + defter (hareket, ışınım, ısrar sayısı) | #6'daki B, yeniden koşmaz |
| B-ısrar | B0 eksi "ısrar" satırı ve ısrar sözlük satırı | yeni |
| B-blok | B0 eksi çelişki bloğu (yalnız tam kayıt + defter) | yeni |
| C | A + tek satır k-NN kararı: "Defter sınıflandırıcısı (etiketli örneklerle eğitildi, bu ajanın tohumu eğitimde yoktu): uyuyan olasılığı 0,xx" | yeni |
| F | 4 etiketli örnek (A biçiminde, etiketiyle) + A | yeni |

- C'deki sayı #6 tabanının k-NN'i (k=5, z-ölçek, B defterindeki 11 sayı, tohum dışarıda) `yargic_ikiz_11kas.py knn()`. Sınanan ajanın tohumu eğitimde yoktur.
- F örnekleri (tohumu sınama vakalarıyla çakışmayan bütün çatallı donuk vakalar, kural önceden sabit): donuk gece listesi `epistemics/kosu_vakalari_11kas.jsonl`, çatallı ve tohum 16-45 dışında olan U ve G vakaları. Sayım: tam 4 vaka (U: t8 T2 U2, t14 T1 U1; G: t2 T1 G3, t8 T3 G3). Sıra sabit: U, G, U, G. Her örnekte A biçimindeki kayıt ve doğru etiket. Daha çok örnek isteniyorsa tek yol tohum 16-45 aralığındaki donuk vakalardır; bunlar sınama vakalarıyla aynı başlangıç dünyasını paylaşır (aynı tohum, aynı başlangıç), sızıntı riski olduğu için F' olarak ayrı kol açılır, birincil sayılmaz. Önerim: yalnız F (4 örnek).

## Ölçüler
1. Her kol ve her satır: AUC [%95], AUC t1/t2/t3, Brier, U yakalama, G yakalama, ort p(U), geçersiz sayısı.
2. Tekrar tutarlılığı: 3/3 argmax eşleşme oranı + tekrar içi p(U) SD ortalaması; istem baytı her (vaka, koşul) için üç kayıtta sha ile denetlenir.
3. Eşleşmeli farklar (aynı vakalar, sınıf katmanlı bootstrap 1000, sabit tohum):
   - Kazanç ayrımı: B-ısrar − B0, B-blok − B0, B-ısrar − A, B-blok − A.
   - C − A, F − A.
   - k-NN − F (soru iii) ve k-NN − C.
4. Okuma kuralı (önceden): fark aralığı 0'ı içeriyorsa "ayrılmadı" yazılır. Bütün hücreler yazılır, seçilmez.

## Çokluk (önkayıtta sayılır)
- Birincil (toplam satırı): B-ısrar − B0, B-blok − B0, C − A, F − A, k-NN − F, tutarlılık ≥ ,80 kararı (4 yeni kol) = 9 birincil karşılaştırma.
- İkincil (5 alt satır × aynı 5 fark) = 25 hücre + kol başına 6 satır AUC (4 kol × 6 = 24) betimleyicidir.
- Toplam 58 sayı. Düzeltme yapılmaz; birincil 9 dışındakiler "betimleme" diye etiketlenir.

## Önkayıt okumaları (iki yönlü)
- (a) B-ısrar − B0 aralığı 0'ın altında ve B-blok − B0 0'ı içeriyorsa: "kazancı ısrar sayısı taşıyor". Rapor cümlesi: "Defterden ısrar satırı çıkarılınca 397B'nin kazancı kayboluyor; çelişki bloğunu çıkarmak etkilemiyor."
- (b) İki ablasyon da 0'ı içeriyorsa: "kazanç tek satıra bağlanamadı", cümle: "Kazanç ne yalnız ısrar sayısından ne yalnız çelişki bloğundan geliyor; ayrılmadı."
- (c) B-blok − B0 0'ın altındaysa: "çelişki bloğu (ısrarın metin hali) sayıyla birlikte gerekli".
- (d) C kolu ≥ k-NN − ,05 ve tutarlılık ≥ ,80 ise: "yargıca karar sayısal olarak verilirse okuyor ve kararlı"; cümle: "Yargıç defteri metin olarak değil, hazır bir karar satırı olarak aldığında k-NN düzeyinde ve kararlı."
- (e) F − A aralığı 0'ın üstündeyse: "dört örnek yargıcı değiştiriyor"; k-NN − F aralığı 0'ı içeriyorsa "az örnekli yargıç k-NN'den ayrılmadı".
- Tutarlılık: hangi kolda ≥ ,80 ise o kol adıyla yazılır; hiçbirinde değilse "yargıç kararsızlığı kol değiştirmekle kalkmadı".

## DeepSeek kolu (danışman sorusu: 32k kesik)
Jeton sayımı (çağrısız, #6 kayıtlarından, `kosu_dsv4_ikiz_aktarim/cagri.jsonl` `jeton` alanları):
- B girdi ortalaması 1996, en çok 11.621 jeton; çıktı ortalaması 12.467, kesik (çıktı ≥ 31.000) 66/294.
- Kesik oranı girdi uzunluğuna bağlı DEĞİL: girdi çeyreklerinde %25 / %33 / %15 / %16. En kısa çeyrekte bile çeyrek kesik.
- Sonuç: kesik girdi bağlamından değil, çıktı payını (32.000) dolduran düşünmeden geliyor. **Kısaltılmış istem sığdırmayı çözmez.**
- Model listesi (ücretsiz `GET /models`): `deepseek-v4-flash` en çok çıktı 1.048.576. 32k bizim ayarımızdı, model sınırı değil.
- Öneri: DeepSeek kolu ancak 10 çağrılık bir sınama (çıktı payı 65.536, B istemi, ≈0,05 $ tahmin) kesik < %5 verirse açılır; Turan sözü gerekir. Sınama yapılmazsa veya kesik ≥ %5 ise **bu kol YOK** ve raporda öyle yazılır.

## Maliyet sayımı (Turan'a sunulacak)
Birim: #6 ölçülen 397B harcaması 8,18 $ / 588 çağrı = 0,0139 $/çağrı (fiyat geri çözümü × kullanım jetonu; Adaption faturasıyla doğrulanmadı).
| kol | çağrı (98 × 3) | girdi ort (tahmin) | $ (birimle) | $ (jeton modeliyle: 0,55 / 3,50 $/M) |
|---|---|---|---|---|
| B-ısrar | 294 | ~1.700 | 4,09 | 4,5 |
| B-blok | 294 | ~1.700 | 4,09 | 4,5 |
| C | 294 | ~1.000 | 4,09 | 3,7 |
| F | 294 | ~4.900 (A + 4 örnek) | 4,09 | 4,3 |
| **toplam** | **1.176** | | **≈ 16,4 $** | **≈ 17,0 $** |
- En kötü durum (her çağrı 8.000 çıktı jetonu): 1.176 × (2.300 × 0,55 + 8.000 × 3,50) / 10⁶ ≈ 34,4 $.
- DeepSeek sınaması açılırsa: 10 çağrı ≈ 0,05 $; tam kol (1.176 çağrı, 64k payla) beklenen ≈ 2,5 $, en kötü ≈ 10 $ (ölçülmedi).
- Fren: model başına 25 $ (kaçak döngü); ilk 40 çağrıda geçersiz oranı > %15 ise kol durur, bana ve danışmana yazılır.
- Süre: #6'da 588 çağrı 6.306 sn (4 paralel) → 1.176 çağrı ≈ 3,5 saat (ölçüm temelli tahmin).

## EKLER · 12 Kas gece (danışman okuması sonrası; kod ve koşudan önce, yukarıdaki kuralları değiştirmeden genişletir)
1. **Yeni kol A+ısrar:** A + yalnız ısrar satırı ve ısrar sözlük satırı (hareket ve ışınım satırları yok). B-ısrar gerekliliği ölçer, A+ısrar yeterliliği. Birincil karşılaştırmalara eklenir: **A+ısrar − A** ve **B0 − A+ısrar**. Okuma: A+ısrar − A aralığı 0'ın üstünde ve B0 − A+ısrar 0'ı içeriyorsa cümle: "Yalnız ısrar sayısını görmek, bütün defteri görmek kadar yetiyor."
2. **C kolu = yankı / tavan denetimi:** yargıca hazır bir olasılık veriliyor; C'nin k-NN düzeyine gelmesi yargıcın becerisi sayılmaz, yalnız "yargıç verilen sayıyı bozmadan aktarabiliyor mu" sorusunu yanıtlar. (d) okuması buna göre yumuşatılır: "Hazır bir karar satırı verildiğinde yargıç onu k-NN düzeyinde ve kararlı biçimde aktardı (yankı denetimi; okuma becerisi değil)." C, kazanç ayrımı sorusunda (i) kullanılmaz.
3. **F sınırı (kart düzeni):** 4 örnek donuk koşulardan geliyor; donuk koşularda kartlar karışık (U'lar U kartıyla, G'ler G kartıyla). Sınama vakalarının bir kısmında kart eşitlenmiş (I1+I2) ya da ters (I2 U vs I1 G). Örnekler yargıca "kart metni = tür" ipucu verebilir; bu, kart eşit ve ters satırlarda F'yi yanıltabilir. F'nin kart eşit ve ters satırları bu sınırla yazılır.
- **Çokluk (güncel):** birincil 12 (toplam satırı: B-ısrar − B0, B-blok − B0, A+ısrar − A, B0 − A+ısrar, C − A, F − A, k-NN − F, 5 kolda tutarlılık ≥ ,80 kararı); betimleyici 65 (5 alt satır × 7 fark = 35, 5 kol × 6 satır AUC = 30). Toplam 77 sayı, düzeltme yok, birincil dışı "betimleme" etiketli.
- **Maliyet (güncel, 5 kol):** 5 × 294 = **1.470 çağrı**. Birimle ≈ **20,4 $** (jeton modeliyle ≈ 20,7 $; A+ısrar ≈ 3,7 $). En kötü durum ≈ 43,2 $. Süre ≈ 4,4 saat. Fren model başına 25 $ → 30 $'a çıkar.

## NOT · karar sayısı tabanı (12 Kas gece, dondurmadan önce; tarama T3'ten)
Karar sayısı TEK BAŞINA, tohum dışarıda k-NN ile aktarımda ,786 (aynı ayarda çelişki ,746), ikiz I2'de ,722 (çelişki ,692) veriyor; tek yönlü AUC (,548 / ,538) bu izi göstermiyor (kaynak `epistemik/tarama_11kas.json` T3). Bu önkayıtta "karar sayısı tabanı" iki ölçüdür: (a) tek yönlü AUC, (b) tohum dışarıda k-NN (k=5, z-ölçek). Her eşleşmeli fark ikisiyle de yazılır.

Program RMS: S1 yargıç ayırma önkayıt, Hikayeci, 12 Kas.
