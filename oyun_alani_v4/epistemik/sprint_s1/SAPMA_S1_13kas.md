# S1 · yargıç ayırma · ÖNKAYITTAN SAPMALAR ve önkayıtta tanımsız kalan seçimler · Hikayeci

Yazıldığı an: 2026-11-13 18:35 TR (bilgisayar saati). İlk ücretli çağrıdan ÖNCE yazıldı: bu dosya yazılırken sprint_s1/kosu_397b_s1_13kas/ klasörü yoktu. Önkayıt dosyası ONKAYIT_S1_yargic_ayirma.md DEĞİŞMEDİ. Onay: Turan, Hikayeci penceresi, 13 Kas akşam ("danışmanın önerdiği yargıç koşusunu onaylıyorum").

## Sapmalar
1. **Klasör ve betik düzeni.** Önkayıt / iş emri: #6 betikleri kopyalanıp uyarlanır. Yapılan: sprint_s1/yargic_s1.py donuk epistemik/yargic_ikiz_11kas.py dosyasını (sha 80b1a06f…) kopyalamadan İÇE AKTARIR; özeti her açılışta denetlenir. Neden: vakalar, sistem istemi, kayıt, defter, sürücü ve puanlama tek kaynaktan gelsin; kopya ayrışmasın. Bu betiğin ürettiği A ve B0 istemleri #6 kaydındaki baytla 196 / 196 aynı (sha).
2. **Fazladan hücreler.** Önkayıt: 77 sayı (12 birincil + 65 betimleyici). Yapılan: 77'ye ek olarak ölçü 3'teki B-ısrar − A, B-blok − A, k-NN − C ve tabanla eşli farklar (k-NN − her yeni kol; karar sayısı tabanı iki yoldan − her yeni kol) bütün satırlarda yazılır. Hepsi "betimleme" etiketli, düzeltme yok, birincil 12 aynen.
3. **Fren biraz erken keser.** Önkayıt: model başına 30 $. Yapılan: "o ana kadarki harcama + 4 paralel çağrının en kötü çıktı maliyeti (4 × 0,028 $) 30 $'ı aşacaksa yeni çağrı açılmaz". Neden: paralel çağrılar tavanı aşmasın.
4. **Ek durdurma kuralı.** Önkayıtta yok: hiç başarılı çağrı olmadan 20 hata birikirse koşu durur (anahtar ya da ağ arızasında boşa dönmesin). Para harcatmaz.

## Önkayıtta tanımsız kalan, koşudan önce sabitlenen seçimler (örnek istemler ornek_istem/ altında)
- **A+ısrar (Ai) metni:** A kaydı + boş satır + "ısrar: çelişki sınaması N tekrar, plan değişim payı X" satırı + boş satır + ısrar sözlük satırı (#6'daki iki satırın aynısı; başka defter başlığı ya da sözlük yok).
- **B-ısrar (Bi):** B0'dan yalnız o iki satır silinir; başka her bayt aynı (her vakada uzunluk farkı denetlenir).
- **B-blok (Bb):** tam kayıt + B0 defteri (ısrar satırı dahil); çelişki bloğu yok.
- **C satırı:** önkayıttaki cümle, sayı iki ondalık ve virgülle (k=5 olduğu için değerler 0,00 / 0,20 / … / 1,00).
- **F biçimi:** başta tek açıklama cümlesi ("Önce türü bilinen dört ajanın kaydı veriliyor (iki uyuyan, iki dürüst). Sonra türünü senin belirleyeceğin ajan gelir."), dört örnek "Örnek j (türü bilinen başka bir ajan):" başlığıyla, her birinde A biçimindeki kayıt + çelişki bloğu + "Bu ajanın türü: uyuyan / durust"; sonra "Türünü belirleyeceğin ajan:" ve A. Örnekler ve sıra önkayıttaki gibi: t8 T2 U2, t2 T1 G3, t14 T1 U1, t8 T3 G3. Örnek bloğu 15.134 karakter; F çağrısı başına girdi yaklaşık 6.500 jeton (önkayıt tahmini 4.900).
- **Karar sayısı tabanı:** özellik = vakanın koşudaki karar sayısı (#6 tabanındaki "karar sayısı" ile aynı alan); iki ölçü: tek yönlü AUC ve tohum dışarıda k-NN (k=5, z-ölçek).
- **Bootstrap tohumu:** 13 (bu betik); #6'nın kendi tablosunda 6 idi. A ve B0'ın aralıkları bu yüzden #6 tablosundakinden üçüncü ondalıkta ayrışabilir.

## Maliyet sayımı (koşudan önce, jeton_s1_13kas.json)
1.470 çağrı · beklenen 21,92 $ (jeton modeli) / 20,45 $ (birimle) · en kötü 43,01 $ · fren 30 $ · süre tahmini 4,4 saat. Önkayıt: ≈ 20,4 $, en kötü ≈ 43,2 $. Fark F isteminin uzunluğundan.

## Değişmeyenler
Aynı 98 çelişki anı (U 42 / G 56), sistem istemi sha 3c8bfddb, 397B, T=0, seed yok, çıktı payı 8000, 4 paralel, 3 tekrar ardışık, puanlama, eşikler, okuma kuralları, "ilk 40 çağrıda geçersiz > %15 ise dur", yarıda kalırsa kaldığı çağrıdan sürme.
