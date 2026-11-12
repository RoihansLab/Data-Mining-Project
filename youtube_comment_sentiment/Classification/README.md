# 🤖 Klasifikasi Sikap Publik terhadap AI yang Menggantikan Pekerjaan

> Folder ini berisi notebook untuk **membandingkan, melatih, dan menguji model** yang menebak sikap sebuah komentar YouTube: **positif**, **negatif**, atau **perlu ditinjau**.

📓 Notebook utama: [`classification_modeling.ipynb`](classification_modeling.ipynb)
📦 Data yang dipakai: [`datasets/youtube_comments_label_final.csv`](../../datasets/youtube_comments_label_final.csv) (3.935 komentar berlabel, hasil notebook [Data Preparation](../Data_Preparation/))

---

## 🗺️ Alur Notebook

```
📄 Data berlabel → 🧹 Text preprocessing → ✂️ Pembagian data → 🔢 e5-large & TF-IDF
→ 🤖 9 model (5-fold CV) → 🎯 Bayesian Search → ⚖️ Perbandingan → 📊 Evaluasi di data uji
```

| Bab | Tahap | Isi |
|---|---|---|
| 1 | Import Library | library dikelompokkan per bab, semua sumber acak dikunci dengan angka 42 |
| 6 | Text Preprocessing | case folding, removing, stopword (kata negasi tetap disimpan), tokenizing, stemming (Sastrawi & Porter), khusus untuk TF-IDF |
| 7 | Pembagian Data | 80% data latih (3.141) dan 20% data uji (786), *stratified* |
| 8 | Ekstraksi Fitur | embedding **e5-large** (1.024 angka per komentar) dan **TF-IDF** (belajar dari data latih saja) |
| 9 | Klasifikasi | SVM linear, Naive Bayes, Logistic Regression, dan KNN, masing-masing dengan e5 dan TF-IDF, dinilai dengan 5-fold CV |
| 10 | Optimasi | Bayesian Search (Optuna, 50 percobaan) untuk kedelapan model |
| 11 | Deep Learning | *fine-tuning* **XLM-RoBERTa-large** dengan 5-fold CV yang sama |
| 12 | Perbandingan Model | performa, good fit, robustness (uji lintas video), visualisasi, uji McNemar, dan model terpilih |
| 13 | Evaluasi di Data Uji | laporan model akhir, confusion matrix, rentang bootstrap, skor per bahasa, skor pada label manusia, contoh kesalahan, dan menyimpan model |
| 14 | Kesimpulan | jawaban rumusan masalah, makna untuk otomatisasi, keterbatasan, dan saran |

Data uji **hanya dipakai sekali** di Bab 13. Pemilihan model di Bab 9–12 hanya memakai data latih (CV dan uji lintas video), supaya skor akhirnya jujur.

---

## ⚖️ Cara Memilih Model

Model dipilih berdasarkan tiga kriteria dari rumusan masalah:

| Kriteria | Ukuran | Artinya |
|---|---|---|
| **Performa** | macro-F1 5-fold CV | seberapa bagus model menebak komentar yang belum pernah dilihat |
| **Good fit** | selisih macro-F1 latih dan CV | makin kecil, makin sedikit model menghafal data latih |
| **Robustness** | macro-F1 lintas video | model dilatih dengan 5 video lalu diuji di 1 video yang belum pernah dilihat, bergiliran untuk keenam video |

**Hasil perbandingan (setelah Bayesian Search):**

| Model | Macro-F1 CV | Selisih latih–CV | Lintas video |
|---|---|---|---|
| **SVM linear + e5** | **0,648** | **0,102** | **0,586** |
| Logistic Regression + e5 | 0,645 | 0,120 | 0,583 |
| XLM-RoBERTa-large | 0,632 | 0,127 | 0,558 |
| KNN + e5 | 0,629 | 0,371 | 0,496 |
| Naive Bayes + e5 | 0,592 | 0,042 | 0,514 |
| Logistic Regression + TF-IDF | 0,571 | 0,322 | 0,440 |
| Naive Bayes + TF-IDF | 0,548 | 0,440 | 0,376 |
| SVM linear + TF-IDF | 0,543 | 0,449 | 0,411 |
| KNN + TF-IDF | 0,483 | 0,517 | 0,338 |

- **e5-large lebih baik daripada TF-IDF untuk semua algoritma.** Model TF-IDF lebih banyak menghafal dan lemah di video baru.
- **SVM + e5 unggul di ketiga kriteria sekaligus.**
- **Uji McNemar:** SVM + e5 lebih sering benar secara signifikan daripada semua model lain, termasuk Logistic Regression + e5 (166 vs 94 komentar, p < 0,001). Dengan koreksi Bonferroni, hanya keunggulan atas KNN + e5 yang tidak lagi signifikan (p = 0,024).

---

## 🎯 Hasil Model Akhir

**Model akhir: SVM linear + e5-large** (`C = 0,584`, `class_weight="balanced"`)

| Metrik di data uji (786 komentar) | Nilai |
|---|---|
| Macro-F1 | **0,640** |
| Akurasi | **0,716** |
| Rentang bootstrap 95% (macro-F1) | 0,603–0,676 |
| F1 negatif / perlu ditinjau / positif | 0,608 / 0,828 / 0,485 |

| Analisis tambahan | Macro-F1 |
|---|---|
| Komentar berbahasa Indonesia (276) | 0,659 |
| Komentar berbahasa Inggris (510) | 0,618 |
| Komentar berlabel manusia (90) | 0,612 |
| Komentar berlabel Claude (696) | 0,644 |

- Skor data uji (0,640) **hampir sama dengan skor CV** (0,648), jadi pemilihan model bisa dipercaya.
- Untuk komentar dari **video baru**, gambaran realistisnya sekitar **0,59** (uji lintas video).
- Kesalahan terbanyak terjadi pada **sindiran dan sikap yang tersirat**, terutama di batas antara "perlu ditinjau" dan sikap yang jelas.

---

## 📊 Visualisasi di Notebook

| Bab | Grafik | Yang terlihat |
|---|---|---|
| 6.1 | diagram lingkaran sebaran label, 10 komentar dengan *likes* terbanyak per label | perlu ditinjau 59,5%; komentar terpopuler kebanyakan sindiran |
| 12.3 | performa dan robustness setiap model (batang) | semua model e5 di atas model TF-IDF; SVM + e5 tertinggi |
| 12.3 | good fit setiap model (batang) | model TF-IDF dan KNN paling banyak menghafal |
| 13.1 | confusion matrix model akhir | label positif paling sulit; kesalahan terbanyak di sekitar "perlu ditinjau" |
| 13.2 | sebaran macro-F1 dari 1.000 kali bootstrap | skor uji berada di tengah sebaran, bukan kebetulan |

---

## 📁 Isi Folder

| Berkas | Isi |
|---|---|
| `classification_modeling.ipynb` | notebook utama: Bab 1 dan 6–14 |
| `model_svm_e5_large.pkl` | model SVM akhir, **dibuat oleh notebook** (Bab 13.6) |

Tebakan XLM-RoBERTa untuk setiap fold dan setiap video disimpan di Google Drive (`MyDrive/hasil_xlm_cv`), sehingga notebook bisa dijalankan ulang tanpa melatih XLM-RoBERTa dari awal.

---

## ▶️ Cara Menjalankan

1. Buka notebook di **Google Colab** dengan runtime **GPU**, lalu pilih *Runtime → Run all*. Dataset diambil langsung dari GitHub, jadi tidak perlu upload file (butuh koneksi internet).
2. Saat diminta, izinkan akses **Google Drive**. Drive dipakai untuk menyimpan hasil XLM-RoBERTa.
3. Bagian yang paling lama:
   - stemming: sekitar 2–3 menit
   - embedding e5-large: sekitar 1–2 menit (saat pertama kali, model sekitar 2 GB diunduh dulu)
   - Bayesian Search: sekitar 10–30 menit
   - XLM-RoBERTa: sekitar 5 menit per pelatihan, atau sekitar 1 jam untuk 5-fold CV dan uji lintas video jika belum ada hasil tersimpan di Drive

---

## ⚠️ Keterbatasan

- Sekitar 89% label dibuat oleh AI (Claude Opus 5.5), dengan kecocokan sedang terhadap manusia (kappa 0,506). Pada 90 komentar uji berlabel manusia, model mencapai macro-F1 0,612.
- Setiap komentar berlabel manual hanya dilabeli satu orang, sehingga kesepakatan antarpelabel manusia belum diukur.
- Data hanya dari 6 video, dengan dua video berbahasa Indonesia.
- XLM-RoBERTa tidak dioptimasi dengan Bayesian Search karena keterbatasan komputasi.
- Uji McNemar dihitung dari tebakan cross-validation, sehingga sedikit kurang ketat daripada uji pada satu data uji yang sama.
