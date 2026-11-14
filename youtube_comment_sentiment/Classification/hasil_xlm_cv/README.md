# 🧠 Hasil Prediksi XLM-RoBERTa

Folder ini berisi **tebakan XLM-RoBERTa-large** dari run terakhir notebook [`classification_modeling.ipynb`](../classification_modeling.ipynb), yaitu hasil **5-fold CV** (Bab 11) dan **uji lintas video** (Bab 12.2). File-file ini disalin dari Google Drive (`MyDrive/hasil_xlm_cv`), tempat notebook menyimpannya saat dijalankan.

---

## 💡 Kenapa Disimpan?

- **Bukti hasil.** Melatih XLM-RoBERTa butuh GPU dan waktu sekitar 1 jam, jadi tebakannya disimpan supaya angka di notebook dan README bisa diperiksa ulang.
- **Supaya bisa diulang persis.** *Fine-tuning* XLM-RoBERTa memberi hasil yang sedikit berbeda setiap kali dilatih ulang, meskipun *seed* sudah dikunci (42), karena perhitungan GPU tidak sepenuhnya deterministik. Dengan file ini, notebook memakai tebakan yang sama sehingga angkanya sama persis.

---

## 📁 Isi Folder

### Hasil 5-fold CV (Bab 11)

| File | Jumlah baris | Macro-F1 latih fold ini |
|---|---|---|
| `fold_0.csv` | 629 | 0,801 |
| `fold_1.csv` | 628 | 0,761 |
| `fold_2.csv` | 628 | 0,786 |
| `fold_3.csv` | 628 | 0,779 |
| `fold_4.csv` | 628 | 0,752 |
| **Total** | **3.141** (seluruh data latih) | rata-rata **0,776** |

| Kolom | Isi |
|---|---|
| `fold` | nomor fold (0–4) |
| `baris` | posisi komentar di **data latih** (0–3.140), sesuai urutan `df_train` setelah pembagian data di Bab 7. Bukan nomor baris di dataset asli |
| `tebakan` | label tebakan XLM-RoBERTa: `positif`, `negatif`, atau `perlu ditinjau` |
| `f1_latih` | macro-F1 model fold itu pada data latihnya sendiri (nilainya sama untuk semua baris dalam satu fold), dipakai untuk cek good fit di Bab 12.1 |

Setiap komentar di data latih muncul tepat satu kali di salah satu fold, karena setiap fold menebak bagian data yang **tidak** dipakai untuk melatihnya.

### Hasil uji lintas video (Bab 12.2)

Model dilatih dengan komentar dari 5 video, lalu menebak komentar dari 1 video sisanya. Nomor video mengikuti **urutan abjad judul**.

| File | Video yang ditebak | Jumlah baris | Macro-F1 |
|---|---|---|---|
| `video_0.csv` | *AI is taking their jobs. But they're fighting back.* | 106 | 0,593 |
| `video_1.csv` | *Humans Need Not Apply - CGP Grey* | 1.011 | 0,456 |
| `video_2.csv` | *Manusia Belum Tergantikan AI Karena Satu Hambatan Ini* | 635 | 0,595 |
| `video_3.csv` | *Pekerja Latih Robot Untuk Gantikan Mereka! KIAMAT KERJA AI DIMULAI!* | 552 | 0,610 |
| `video_4.csv` | *The EXACT moment AI took my job...* | 159 | 0,588 |
| `video_5.csv` | *UK unemployment soars: is AI already taking our jobs?* | 678 | 0,529 |
| **Total** | | **3.141** | rata-rata **0,562** |

| Kolom | Isi |
|---|---|
| `tebakan` | label tebakan XLM-RoBERTa untuk setiap komentar data latih dari video itu, **berurutan sesuai urutan baris di `df_train`** |

---

## 🎯 Ringkasan Hasil

| Ukuran | XLM-RoBERTa | SVM + e5 (model akhir) |
|---|---|---|
| Macro-F1 CV | 0,635 | **0,648** |
| Akurasi CV | 0,682 | **0,720** |
| Selisih latih–CV (good fit) | 0,141 | **0,102** |
| Macro-F1 lintas video (robustness) | 0,562 | **0,586** |

XLM-RoBERTa lebih sering menemukan komentar yang bersikap (recall negatif 0,691 dan positif 0,597), tetapi lebih sering salah menebak komentar "perlu ditinjau". Hasilnya tetap di bawah SVM + e5 di ketiga kriteria, dan uji McNemar menunjukkan SVM + e5 lebih sering benar secara signifikan (367 vs 248 komentar, p < 0,001).

Run sebelumnya memberi macro-F1 CV 0,632 dan lintas video 0,558. Perbedaan kecil ini berasal dari variasi pelatihan di GPU dan tidak mengubah kesimpulan.

---

## ▶️ Cara Memakai

**Agar notebook memakai hasil ini (tanpa melatih ulang):**
1. Buat folder `hasil_xlm_cv` langsung di **My Drive** Google Drive.
2. Salin kesebelas file `.csv` dari folder ini ke folder tersebut.
3. Jalankan notebook di Google Colab dan izinkan akses Google Drive saat diminta. Bab 11 akan menampilkan "Fold … sudah ada, dilewati", dan Bab 12.2 langsung membaca file video tanpa melatih ulang. Keduanya memakai tebakan dari file ini.

Jika folder di Drive kosong, notebook akan melatih ulang XLM-RoBERTa (sekitar 1 jam di GPU T4), dan angkanya bisa sedikit berbeda dari tabel di atas.

**Untuk memeriksa skor sendiri** (di dalam notebook, setelah Bab 7 dan sel Google Drive di Bab 11 dijalankan, sehingga `df_train`, `y_train`, dan `FOLDER_XLM` sudah ada):

```python
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

# 5-fold CV: gabungkan kelima fold, lalu kembalikan ke urutan data latih
semua = pd.concat([pd.read_csv(f"{FOLDER_XLM}/fold_{i}.csv") for i in range(5)])
pred = np.empty(len(y_train), dtype=object)
pred[semua["baris"]] = semua["tebakan"]
print("Macro-F1 CV:", round(f1_score(y_train, pred, average="macro"), 3))   # 0.635

# Lintas video: nomor file mengikuti urutan abjad judul video
video = df_train["video_title"].to_numpy()
for nomor, judul in enumerate(np.unique(video)):
    tebakan = pd.read_csv(f"{FOLDER_XLM}/video_{nomor}.csv")["tebakan"]
    print(judul[:30], round(f1_score(y_train[video == judul], tebakan, average="macro"), 3))
```
