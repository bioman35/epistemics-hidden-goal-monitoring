# S2 · SAPMA EKİ · 14 Kas 2026 (saatler makine saatinden)

Bu dosya SAPMA_S2_13kas.md'ye (sha e9cb0b6b…) EKTİR; o dosya değişmedi.

1. BAŞLATMA: zincir 14 Kas 01:27'de başlatıldı (Turan'ın sözü Kaptan üzerinden: "bilgisayar ekran kartında koşuya geçiyor"). İlk deneme 01:28'de durdu: yerel model sunucusu (Ollama) kapalıydı, t46 DU koşusu model çağrısı yapamadan çıktı (çıkış 1, 20 sn). Klasör zincirin kuralıyla yarım adıyla kalır, silinmez. Ollama başlatıldı (sürüm 0.40.16), zincir 01:29'de yeniden başlatıldı. Aynı tohum, aynı model tohumu.
2. HATA OLURSA YİNELEME (Turan'ın sözü danışman üzerinden: "tüm koşuları aralıksız yapsın, hepsini bitirsin. hata olursa tekrarlasın"): koşan gece_s2.py ve zincir_s2.py DEĞİŞTİRİLMEDİ. Yeni dosya gece_s2_gozcu.py eklendi: gece_s2.py hata ile biterse onu yeniden başlatır (zincir kaldığı tohumdan sürer), aynı hata üst üste 3 kez olursa durur. Danışmanın istediği "3 denemeden sonra o tohumu atla, zincir sürsün" davranışı YOK: zincir atlamayı desteklemiyor ve koşarken değiştirilmedi; üçüncü hatada zincir durur. Yeniden başlatma sayısı gece_s2_gozcu_13kas.log'da.
3. ÇELİŞKİ ÇATALI KAPISI: gece_s2.py çatalı başlatmadan önce ekran kartı yüzde 25 altını üç okumada bekler (sabah 09:00'a kadar). Çatal kendi içinde beklemeyi bırakıp çıkarsa gözcü yeniden başlatır. Eşik değiştirilmedi.
4. Bu ek, ilk (başarısız) başlatmadan SONRA, ikinci başlatmayla aynı dakikalarda yazıldı; ilk model çağrısından önce yazıldığı söylenemez (ikinci başlatmanın ilk çağrısı bu dosyadan birkaç saniye önce ya da sonra olabilir).

## 14 Kas 01:41 · DURUM DÜZELTMESİ (yukarıdaki 1. madde eksikti)
- İkinci başlatma (01:31) da DURDURULDU (01:40, Hikayeci). Neden: Ollama modeli ekran kartına değil İŞLEMCİYE yükledi ("100% CPU"). Ollama günlüğü: 12 Kas 08:12'ye kadar "library=CUDA ... RTX 4050" (sürüm 0.40.15); 12 Kas 08:13'te Ollama kendi kendini 0.40.16'ya güncelledi ve güncelleme günlüğü ggml-cuda.dll dosyasını kurarken bitiyor (cuda_v12 klasöründe ggml-cuda.dll yok, yerinde is-GY23M9BWVM.tmp var); 12 Kas 17:39'dan beri her açılışta "library=cpu", toplam ekran belleği 0.
- İkinci başlatmada t46 DU koşusu 9 dakikada ilerleme yazmadı; tamamlanan koşu YOK, ölçüye girecek veri YOK. kosular/s2_13kas/DU/t46 klasöründe yalnız kosu_meta.json var; silinmedi.
- S2 için sonuç: bu makinede şu an (a) ekran kartı kullanılamıyor, (b) Ollama sürümü dondurulan koşulardaki 0.40.15 değil 0.40.16. İkisi de önkayıttan sapma olur. Koşu, Turan ve danışman karar verene kadar BAŞLATILMAYACAK.
- gece_s2_gozcu.py çalıştı ama hiçbir yeniden başlatma yapmadı (zincir hata vermeden önce elle durduruldu).

## 14 Kas 02:03 · KARAR VE ONARIM (koşudan ÖNCE yazıldı; tamamlanmış S2 koşusu yok)
- KARAR (danışman): S2 işlemcide koşmaz; Ollama 0.40.15 (kilitteki yerel ölçümlerin sürümü) + ekran kartı. İzin Turan'dan, Hikayeci penceresinde (14 Kas ~01:5x: "Ollama 0.40.15'i resmi sayfadan indirip kur, otomatik güncellemeyi kapat. Köprü sınaması tutarsa geri çağırma koşularının hepsini aralıksız koş. Tutmazsa başlatma, danışmana yaz.").
- ONARIM: kurulum dosyası github.com/ollama/ollama/releases/download/v0.40.15/OllamaSetup.exe, 1.689.667.936 bayt, sha256 106ef3d2a02437810fba6f574914b1413c512ea84ddd4f184c8e7f434b6f5564 (resmî sürüm sayfasındaki özetle aynı). Kurulum 01:53'te bitti; sunucu günlüğü "version 0.40.15", "library=CUDA ... RTX 4050".
- OTOMATİK GÜNCELLEME: Ollama uygulaması açılınca 0.40.16'yı yeniden indirdi (01:53:48). Uygulama kapatıldı, indirilen güncelleme silindi, açılış kısayolu D'ye taşındı. Koşular uygulama olmadan, doğrudan "ollama serve" ile çalışır (güncelleme denetimi yalnız uygulamada). Uygulama içinde güncellemeyi kapatan bir ayar BULUNMADI.
- DONANIM NOTU: yeni yüklemede model 25 / 29 katman ekran kartında (ollama ps: yüzde 18 işlemci, yüzde 82 ekran kartı). Kilit dönemindeki günlüklerde de yükleme kısmiydi: 23 / 29 (6 kez), 25 / 29 (6 kez), 21 / 29 (1 kez). Yani "tamamı ekran kartında" hiç olmamış; katman sayısı yüklemeden yüklemeye değişmiş.
- KÖPRÜ SINAMASI: kopru_s2.py (yeni dosya). Kilitteki üç soğuk koşu (t16, t26, "16,26") aynı komutla yeniden üretilir, satır satır karşılaştırılır. Tutmazsa S2 başlamaz.
- S2 OLLAMA KAYDI: ollama_kayit.py (yeni dosya) koşular boyunca dakikada bir Ollama sürümünü, model özetini ve ekran belleği payını ollama_kayit_13kas.jsonl dosyasına yazar. Dünya ve zincir kodu değişmedi.
- "3 denemeden sonra o tohumu atla" YOK (zincir desteklemiyor); gözcü aynı hata üst üste 3 kez olursa durur.
