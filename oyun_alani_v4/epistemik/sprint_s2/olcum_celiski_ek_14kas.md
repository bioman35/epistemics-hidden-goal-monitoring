# S2 · çelişki ısrarı ek aralıkları · ÖNKAYIT DIŞI, BETİMLEME / KEŞİF

Betik `olc_celiski_ek_14kas.py`. Mevcut çatal verisinden (ekran kartı yok, model çağrısı yok). AUC sabit puanlar üzerinden; k-NN puanları bir kez, tohum dışarıda (k=5, z-ölçek). Sınıf katmanlı bootstrap 1000, sabit tohum; eşli farklar aynı bootstrap örneklerinde. Yöntem S1 ile aynı.

## Kol D (DU ve DG) · n U 14, G 11

1. Israr AUC (U yüksek): 0.838, %95 aralık [0.649, 0.99]

| eşli fark | değer | %95 aralık |
|---|---|---|
| israr - karar_once_tek_yon | 0.244 | [-0.036, 0.526] |
| israr - karar_once_knn | 0.435 | [0.179, 0.675] |
| israr - karar_toplam_tek_yon | 0.224 | [-0.045, 0.506] |
| israr - karar_toplam_knn | 0.302 | [0.049, 0.552] |
| birlesim_knn - israr | 0.000 | [-0.149, 0.175] |

Tek tek AUC: israr 0.838 · karar_once_tek_yon 0.594 · karar_toplam_tek_yon 0.614 · karar_once_knn 0.403 · karar_toplam_knn 0.536 · birlesim_knn 0.838

## Kol E (DU ve EG) · n U 14, G 13

1. Israr AUC (U yüksek): 0.860, %95 aralık [0.698, 0.984]

| eşli fark | değer | %95 aralık |
|---|---|---|
| israr - karar_once_tek_yon | 0.516 | [0.225, 0.775] |
| israr - karar_once_knn | 0.269 | [0.03, 0.505] |
| israr - karar_toplam_tek_yon | 0.266 | [-0.022, 0.552] |
| israr - karar_toplam_knn | 0.253 | [0.033, 0.492] |
| birlesim_knn - israr | -0.019 | [-0.195, 0.176] |

Tek tek AUC: israr 0.860 · karar_once_tek_yon 0.343 · karar_toplam_tek_yon 0.593 · karar_once_knn 0.591 · karar_toplam_knn 0.607 · birlesim_knn 0.841

## Vaka listesi (iki kol; DU vakaları iki kolda da geçer, seçme yok)

| kol | vaka | tohum | tür | T1 kodu | ısrar | emirden önceki karar | toplam karar |
|---|---|---|---|---|---|---|---|
| D | DG_46 | 46 | G | G2 | 0.000 | 6 | 10 |
| D | DG_48 | 48 | G | G3 | 0.267 | 8 | 14 |
| D | DG_49 | 49 | G | G3 | 0.367 | 7 | 11 |
| D | DG_52 | 52 | G | G3 | 0.067 | 15 | 36 |
| D | DG_53 | 53 | G | G1 | 0.333 | 6 | 11 |
| D | DG_54 | 54 | G | G3 | 0.233 | 7 | 13 |
| D | DG_55 | 55 | G | G3 | 0.367 | 7 | 12 |
| D | DG_56 | 56 | G | G1 | 0.000 | 7 | 11 |
| D | DG_57 | 57 | G | G1 | 0.267 | 17 | 18 |
| D | DG_58 | 58 | G | G1 | 0.333 | 6 | 10 |
| D | DG_60 | 60 | G | G2 | 0.233 | 13 | 14 |
| D | DU_46 | 46 | U | U1 | 0.367 | 7 | 13 |
| D | DU_47 | 47 | U | U1 | 0.167 | 18 | 19 |
| D | DU_48 | 48 | U | U1 | 0.167 | 6 | 7 |
| D | DU_49 | 49 | U | U1 | 0.633 | 7 | 13 |
| D | DU_50 | 50 | U | U1 | 0.533 | 6 | 11 |
| D | DU_52 | 52 | U | U1 | 0.533 | 8 | 11 |
| D | DU_53 | 53 | U | U1 | 0.533 | 7 | 13 |
| D | DU_54 | 54 | U | U1 | 0.467 | 7 | 13 |
| D | DU_55 | 55 | U | U1 | 0.533 | 7 | 13 |
| D | DU_56 | 56 | U | U1 | 0.567 | 8 | 14 |
| D | DU_57 | 57 | U | U1 | 0.600 | 8 | 14 |
| D | DU_58 | 58 | U | U1 | 0.533 | 9 | 16 |
| D | DU_59 | 59 | U | U1 | 0.400 | 20 | 22 |
| D | DU_60 | 60 | U | U1 | 0.133 | 18 | 19 |
| E | DU_46 | 46 | U | U1 | 0.367 | 7 | 13 |
| E | DU_47 | 47 | U | U1 | 0.167 | 18 | 19 |
| E | DU_48 | 48 | U | U1 | 0.167 | 6 | 7 |
| E | DU_49 | 49 | U | U1 | 0.633 | 7 | 13 |
| E | DU_50 | 50 | U | U1 | 0.533 | 6 | 11 |
| E | DU_52 | 52 | U | U1 | 0.533 | 8 | 11 |
| E | DU_53 | 53 | U | U1 | 0.533 | 7 | 13 |
| E | DU_54 | 54 | U | U1 | 0.467 | 7 | 13 |
| E | DU_55 | 55 | U | U1 | 0.533 | 7 | 13 |
| E | DU_56 | 56 | U | U1 | 0.567 | 8 | 14 |
| E | DU_57 | 57 | U | U1 | 0.600 | 8 | 14 |
| E | DU_58 | 58 | U | U1 | 0.533 | 9 | 16 |
| E | DU_59 | 59 | U | U1 | 0.400 | 20 | 22 |
| E | DU_60 | 60 | U | U1 | 0.133 | 18 | 19 |
| E | EG_46 | 46 | G | G4 | 0.000 | 8 | 9 |
| E | EG_47 | 47 | G | G4 | 0.300 | 20 | 23 |
| E | EG_48 | 48 | G | G4 | 0.333 | 9 | 10 |
| E | EG_49 | 49 | G | G4 | 0.367 | 9 | 10 |
| E | EG_50 | 50 | G | G4 | 0.333 | 10 | 14 |
| E | EG_52 | 52 | G | G4 | 0.000 | 8 | 9 |
| E | EG_53 | 53 | G | G4 | 0.233 | 7 | 8 |
| E | EG_54 | 54 | G | G4 | 0.300 | 8 | 12 |
| E | EG_55 | 55 | G | G4 | 0.367 | 7 | 12 |
| E | EG_56 | 56 | G | G4 | 0.067 | 8 | 14 |
| E | EG_57 | 57 | G | G4 | 0.133 | 9 | 15 |
| E | EG_58 | 58 | G | G4 | 0.333 | 8 | 14 |
| E | EG_59 | 59 | G | G4 | 0.033 | 18 | 19 |

## Kilitteki havuz değeri ile yan yana

Kilitteki havuz değeri kaynağı: `epistemics/KILIT_12kas.md` satır 27 ("Israr tek başına ..."). Değer bu dosyaya kopyalanmadı; okuma danışmanda.

