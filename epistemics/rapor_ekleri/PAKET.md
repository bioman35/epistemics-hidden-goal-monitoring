# Code / data package · 15 Nov 2026

Built by `epistemics/rapor_ekleri/paket.py`. The first build was published by the author on 15 Nov 2026 (GitHub, first commit and release `sprint-15nov2026`); this rebuild adds S5 and is local until the author's word (no push, no upload). Each archive contains `SHA256SUMS.txt` (sha256 of every file, path relative to the `sprint/` folder).

| archive | files | uncompressed | archive size | sha256 of the archive |
|---|---|---|---|---|
| `epistemics_kod_veri_15kas.zip` | 228 | 15.8 MB | 9.5 MB | `bd65c6a28bfbc1c0fffefeb994db03ec1bf7e0722b6ddbeb678b79982cd57179` |
| `epistemics_ham_kayit_15kas.zip` | 709 | 46.5 MB | 2.5 MB | `ced66e2c2c75556895a34ed34fe55a084005ba9f7b23f1ff0039cd47d9f65104` |

Location (local only): `D:\calisma_cikti\epistemics_paket`.

Main archive: pre-sprint world and runner (`oyun_alani_v4/*.py`, `aktarim/`, freeze manifests and the 12 Nov snapshot zip), sprint preregistrations, deviation files, sprint scripts, measurement files and run logs (S1-S5), the bridge check, figures and tables, README, report appendices, and the video's text, sources and code (no video file).
Raw-record archive: the run records and replays (`sprint_s2/kosular`, `kosular_oynat`, `sprint_s3/kosular`), the model call logs (`sprint_s1/kosu_397b_s1_13kas`, `sprint_s4/cagri_s4_*.jsonl`, `sprint_s5/cagri_s5_*.jsonl`; files named `sahte` are fake-data pipeline tests) and the contradiction-fork answers (`celiski_s2_13kas.jsonl`, `catal_s3_14kas.jsonl`).
Left out: 443 scratch / cache files (`karalama*`, `__pycache__`) and 6 video / generated files (mp4 files and the generated `filmler.js`; the video is delivered separately).

## Secret and personal-data scan

Every text file put into the archives was scanned, including the files inside the 12 Nov snapshot zip. Values are never printed; only file and count.

### main archive

- openai/adaption style key sk-: 2 hit(s) in 2 file(s). fake test value (contains SAHTE): 2 hit(s), e.g. `epistemics/DONDURMA_12KAS_kod_sonuc.zip!oyun_alani_v4/luna_yargic.py`, `oyun_alani_v4/luna_yargic.py`
- bearer token: none
- github token: none
- huggingface token: none
- google api key: none
- aws key: none
- slack token: none
- private key block: none
- key / password assignment: none
- .env / key file: none
- e-mail address: none
- TR mobile phone: 10 hit(s) in 4 file(s). digits inside a sha256 / hex string: 10 hit(s), e.g. `epistemics/DONDURMA_12KAS.sha256`, `epistemics/DONDURMA_12KAS.tsv`, `epistemics/DONDURMA_12KAS_kod_sonuc.zip!oyun_alani_v4/DONDURMA_4KAS.sha256`
- IPv4 address: 46 hit(s) in 34 file(s). loopback 127.0.0.1: 43 hit(s), e.g. `epistemics/DONDURMA_12KAS_kod_sonuc.zip!oyun_alani_v4/KOSU_GUNLUGU_7KAS.md`, `epistemics/DONDURMA_12KAS_kod_sonuc.zip!oyun_alani_v4/aktarim/kosu_aktarim.py`, `epistemics/DONDURMA_12KAS_kod_sonuc.zip!oyun_alani_v4/epistemik/gece_11kas.py`; not an address (part > 255): 3 hit(s), e.g. `oyun_alani_v4/epistemik/sprint_s2/SAPMA_S2_ek_14kas.md`, `oyun_alani_v4/epistemik/sprint_s5/SAPMA_S5_15kas.md`
- Windows user path: 121 hit(s) in 32 file(s). local machine user folder in a hard-coded path: 121 hit(s), e.g. `epistemics/DONDURMA_12KAS_kod_sonuc.zip!epistemics/hareket/hareket_bilgi.py`, `epistemics/DONDURMA_12KAS_kod_sonuc.zip!epistemics/hareket/hareket_sayim.py`, `epistemics/DONDURMA_12KAS_kod_sonuc.zip!epistemics/hareket/kararsiz_an_sec.py`
- key file path: none
- person name (author / company owner): 121 hit(s) in 119 file(s). author first name (name list kept as sha256 only): 119 hit(s), e.g. `epistemics/DONDURMA_12KAS_kod_sonuc.zip!epistemics/GECE_PLANI_11kas.md`, `epistemics/DONDURMA_12KAS_kod_sonuc.zip!epistemics/GECE_RAPORU_11kas.md`, `epistemics/DONDURMA_12KAS_kod_sonuc.zip!epistemics/KILIT_12kas.md`; author surname (name list kept as sha256 only): 2 hit(s), e.g. `epistemics/RAPOR_TAM_15kas.md`, `epistemics/RAPOR_TAM_15kas_teslim1.md`

### raw archive

- openai/adaption style key sk-: none
- bearer token: none
- github token: none
- huggingface token: none
- google api key: none
- aws key: none
- slack token: none
- private key block: none
- key / password assignment: none
- .env / key file: none
- e-mail address: none
- TR mobile phone: 6 hit(s) in 6 file(s). digits inside a sha256 / hex string: 6 hit(s), e.g. `oyun_alani_v4/epistemik/sprint_s2/kosular/s2_13kas/DG/t52/v4_kosu2_O1_O2b_t52_DG.jsonl`, `oyun_alani_v4/epistemik/sprint_s2/kosular/s2_13kas/DU/t51/v4_kosu2_O1_O2b_t51_DU.jsonl`, `oyun_alani_v4/epistemik/sprint_s2/kosular/s2_13kas/DU/t55/v4_kosu2_O1_O2b_t55_DU.jsonl`
- IPv4 address: none
- Windows user path: none
- key file path: none
- person name (author / company owner): none

