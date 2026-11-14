# S2 · çelişki ısrarı tabanı (ölçü 5; ayrı adım)

Satır 1140 (sahte 0), vaka 38, çatal başına N=10, vaka başına en çok 3 çatal (emirden önceki ilk 'git X' kararları). İstemde 'yol yok' eksik: 0.

## Kol D (DU ve DG)

- n: U 14, G 11 · ısrar ortalaması: U 0.44, G 0.224
- AUC: dönüş (U düşük) 0.500 · ısrar (U yüksek) 0.838 · karar sayısı tek yönlü 0.594, k-NN 0.403 · birleşim k-NN 0.838, lojistik 0.818
- Dönüş eksi taban: {"israr_U_yuksek": -0.338, "karar_once_tek_yon": -0.094, "karar_once_knn": 0.097, "birlesim_knn": -0.338, "birlesim_lojistik": -0.318} · dönüş eksi ısrar %95 aralık [-0.488, -0.114]

## Kol E (DU ve EG)

- n: U 14, G 13 · ısrar ortalaması: U 0.44, G 0.215
- AUC: dönüş (U düşük) 0.500 · ısrar (U yüksek) 0.860 · karar sayısı tek yönlü 0.343, k-NN 0.591 · birleşim k-NN 0.841, lojistik 0.808
- Dönüş eksi taban: {"israr_U_yuksek": -0.36, "karar_once_tek_yon": 0.157, "karar_once_knn": -0.091, "birlesim_knn": -0.341, "birlesim_lojistik": -0.308} · dönüş eksi ısrar %95 aralık [-0.49, -0.154]

