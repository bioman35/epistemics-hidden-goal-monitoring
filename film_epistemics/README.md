# Teslim videosu · Apart AI x Epistemics Sprint (14 Kas 2026)

İstek: Turan ("labirent oyun videosu olmaz mı"), danışman İŞ EMRİ 6. Sessiz, İngilizce altyazılı, 1080p. Model çağrısı yok, para yok. Kayıtlara ve dondurulmuş dosyalara dokunulmaz (yalnız okunur).

- `FILM_METNI_14kas.md`: onaylı metin (sürüm 3, danışman). Filmdeki her yazı buradan birebir gelir.
- `KAYNAK.md`: her yazının metindeki satırı, her sayının dosya + alan + sha'sı, aynı başlangıç sağlaması. `arac/ep_metin.py` üretir; elle yazılmaz.
- `arac/`: preexisting (film tooling). `D:\masaustu_tasinan_14kas\sprint\film_sprint\` (8 Kas; 14 Kas'ta C diski dolu olduğu için oraya taşındı) kopyası. Kaynağa yazılmadı. Kopyada değişenler:
  - `film_veri.py`: S2 kol E tohum 58 (DU_58, EG_58); aynı başlangıç sağlaması → `veri/saglama.json`; sayaç ve şerit → `veri/sayac.json`.
  - `film.js`: `?ep=1&f=N` kipi (tek koşu, yalnız sahne ve ajan etiketleri; çekim listesi `window.EP_PLAN`). `index.html`: ep kipi biçemi; `veri/sprint.js` satırı kaldırıldı.
  - Yeni: `ep_metin.py` (yazılar ve sayı sağlaması), `cek_ep.py` (3B çekim, ekran kartı), `kur.py` (bindirme ve kurgu, işlemci).
  - Kopyada duran ama bu filmde kullanılmayanlar: `cik.py`, `metin.py`, `karis.py`, `dogrula.py`, `plan.json`, `IZLE.bat`, eski README.

Yapım sırası v1-v3 (metin sürüm 3, `FILM_METNI_14kas_surum3.md`, `KAYNAK_v3.md`): `python -I film_veri.py` → `python -I ep_metin.py` → `python -I cek_ep.py tam D:\calisma_cikti\film_epistemics\kare` (ekran kartı; yayın programı ve başka başlıksız tarayıcı kapalıyken, yazılımcıyla sırayla) → `python -I kur.py tam <çıktı.mp4>`.

Yapım sırası v4 (metin sürüm 4, `FILM_METNI_14kas.md`, `KAYNAK.md`; Turan'ın iki notu: açıklama eksik, çok bekleme): `python -I film_veri.py` → `python -I ep_metin4.py` → `EPKIP=4 python -I cek_ep.py tam D:\calisma_cikti\film_epistemics\kare4` (film.js `?ep=4`: tek akış, T1'in üç karar anında duruş; ekran kartı, aynı kurallar) → `python -I kur4.py tam <çıktı.mp4>`. Durgunluk ölçüsü: `python -I durgun.py <video> <bölüm sınırları>`.

Videolar: `teslim_videosu_v1.mp4` … `teslim_videosu_v4.mp4` (hiçbiri silinmez).

Çıktı ve ara kareler `D:\calisma_cikti\film_epistemics\` altında (C diski dolu).
