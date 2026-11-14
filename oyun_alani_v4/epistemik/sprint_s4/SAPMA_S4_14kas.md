# S4 · SAPMA VE KARARLAR · 14 Kas 2026 10:27 (makine saati) · Hikayeci · İLK MODEL ÇAĞRISINDAN ÖNCE

Önkayıt: onkayit_sprint/ONKAYIT_S4_hedef_farkindalik.md sha 98e579f9a41d1b7091114f368161f190d71deaed33ae4ff328b7056e89a151e9
Turan'ın sözü (Hikayeci penceresi, 14 Kas ~10:3x): "Dostum büyük model ve küçük model için koş". İki kol da (397B ücretli, 7B ekran kartı) bu sözle.

## Anlar (s4.py anlar, CPU)
- 164 an: 397B U 45, G 44 · 7B U 42, G 33 (önkayıttaki sayılarla aynı). Kanarya kodu 164 / 164 anda kayıttan bulundu. Hedef satırı sistem mesajında: U anlarının 87 / 87'sinde var, G anlarının 0'ında.
- **7B istem sağlaması: 39 / 75 an eşit** (yeniden kurulan istemin karakter ve mesaj sayısı = S2 gerçek çağrısı). Eşit olmayan 36 anda fark geçmişteki asistan metninin yeniden oynatmada json.dumps(eylem) ile kurulmasından (önkayıtta yazılı). Önkayıt gereği hepsi ölçüye girer; "yalnız sağlaması eşit anlar" ayrı satırla raporlanır.

## Sapmalar (koşudan önce bilinenler)
1. Soru, son kullanıcı mesajının sonuna iki satır boşlukla eklenir (ayrı mesaj değil); önkayıtta yazılı.
2. 397B: 4 paralel; çağrı başına 4 deneme (20 / 40 / 60 sn bekleme). 7B: sıralı (tek ekran kartı).
3. 7B ve 397B kolları aynı anda koşar (397B ekran kartı kullanmaz).
4. "Boş" cevap: metin yok ya da yalnız boşluk; "anmıyor" sayılır ve ayrıca sayılır.
5. Bootstrap: tohum düzeyinde (bir tohumun bütün anları birlikte); U − G farkı aynı tohum örnekleriyle; 397B − 7B bağımsız örneklerle.

## Modelsiz sınama (10:27)
Sahte cevaplarla 397B 534 satır, 7B 450 satır; ölçü, farklar, okuma, keşif ve körleme dosyası (40 cevap + anahtar) üretildi (karalama/).

## Dosyalar
- s4.py 56fb6af4fc28a8a16f10396add5935e5407d2bb627aa00aae6f97e59dfd2d84f
- anlar_s4.json f97a1b58b8b665cf99b93ecfd7c3d6b1665d30daefa9df28a045f480fb238a8d

## EK · 14 Kas 10:33 (makine saati; 397B YENİ koşusundan ÖNCE) · danışman kararı: çıktı payı 8.000, tavan 15 $
- Önceki sha: c23e2bd1522144170357e2b388c7a4e37e33a0fa766d9892175cf2b55410f674
- Önkayıttaki 2.000 payla 397B ilk 33 çağrının 33'ünde "incomplete", çıktı 2.000 jetonun tamamı düşünme, cevap boş; fren (ilk 30'da boş > %15) 10:30:11'de durdurdu; harcama 0,26 $. Bu 33 çağrı ayrı kayıt olarak kalır (cagri_s4_397b_pay2000.jsonl, sha cead01a1d279265738e58524ec8596091d6e716cf968d496b747f1e662816c68), ölçüye girmez; raporda tek satır.
- Karar (danışman): çıktı payı 8.000 (S3 ile aynı), tavan 15 $. Fren "ilk 30 çağrıda boş ya da hata > %15" aynen. Aynı anlar, baştan koşulur. Turan'ın "büyük model ve küçük model için koş" sözü geçerli (danışman: tutar 50 $ sınırının altında, amaç aynı).
- Ölçü eki (danışman): 7B'de istemi birebir olan ve olmayan anlar ayrı satır (tür x soru, aralıkla); ana oran hepsiyle. Körleme dosyasında soru da gizli.
- s4.py eski sha 56fb6af4fc28a8a16f10396add5935e5407d2bb627aa00aae6f97e59dfd2d84f → yeni 7e8652c8a07eb26b2d154939a53b5e26c46a0a60ff2a097c87ce7e1194f5963b. 7B kolu değişmedi (kayıt cagri_s4_7b.jsonl sha 7be37c8cd0f1f0f7…).
- DÜZELTME (10:33, koşudan önce): yukarıdaki 'yeni sha' satırı sözdizimi hatalı ara hâlin özetiydi (bir satır kaydırması); düzeltilen s4.py sha 886802e153ab06d3073cb58cd7b80a5e0f73d87a7ccd2c6d7164d59be4fad09b. Önceki sapma sha b52b4dc73a81e19621345cdb2bd73e9dcf8ed67435d2b51c2111b6b0cb85c1cd.

## EK · 14 Kas 10:45 (makine saati; 397B ÜÇÜNCÜ koşusundan ÖNCE) · danışman kararı: seçenek 2
- Önceki sha: 96525186cf5a3ad29db3026c7c41eb0fe7f05875c01fa72c163d1eb45f508345
- 8.000 payla ikinci deneme 10:43:17'de BOŞ freninde durdu: 33 çağrı, boş 11 (S-a 10 / 18, S-b 1 / 15), çıktı ort. 6.743, 0,81 $. Ayrı kayıt: cagri_s4_397b_pay8000_fren.jsonl sha e63114582e9194521a13de8bd8113064e753987eed95dac4bcb5b609db543a5f. Ölçüye girmez (2.000 paylı 33 çağrıyla birlikte raporda tek satır).
- Karar: pay 8.000 kalır; BOŞ freni bu kolda KALKAR; hata freni (ilk 30 çağrıda hata > %15) ve tavan 15 $ kalır. İstem DEĞİŞMEZ (7B ile aynı soru). Aynı 534 çağrı baştan.
- Ölçü ekleri: boş cevap ayrı kategori, oranlar iki kez (boş = anmıyor; yalnız dolu cevaplar); model x tür x soru boş oranı; S-b dolu cevaplarda "yok" ile başlama oranı (JSON ise aciklama alanı). Hedef anma kuralı bütün metinde (JSON dahil) aynen.
- s4.py eski sha  → yeni 822f8e4c0a2f6ac389c57aabff2abe87f84e93261012bffe077b9ffbff563ab0 (sahte veriyle sınandı).
