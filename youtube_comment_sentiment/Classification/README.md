# 🤖 Klasifikasi Sikap Publik terhadap AI yang Menggantikan Pekerjaan

> Folder ini berisi notebook untuk **melatih dan menguji model** yang menebak sikap sebuah komentar YouTube: **positif**, **negatif**, atau **perlu ditinjau**.

📓 Notebook utama: [`classification_modeling.ipynb`](classification_modeling.ipynb)
📦 Data yang dipakai: [`datasets/youtube_comments_label_final.csv`](../../datasets/youtube_comments_label_final.csv) (3.935 komentar berlabel, hasil notebook [Data Preparation](../Data_Preparation/))

---

## 🗺️ Alur Notebook

```
📄 Data berlabel → 🧹 Text preprocessing → 🔢 Embedding e5-large → 🤖 SVM linear → 🎯 Bayesian Search → 📊 Evaluasi
```

| Bab | Tahap | Isi |
|---|---|---|
| 6 | Text Preprocessing | case folding, removing, stopword (kata negasi tetap disimpan), tokenizing, stemming (Sastrawi & Porter) |
| 7 | Ekstraksi Fitur | embedding **e5-large** (1.024 angka per komentar), lalu pembagian data 80:20 (stratified) |
| 8 | Klasifikasi | **SVM linear** dengan pengaturan awal |
| 9 | Optimasi & Evaluasi | Bayesian Search (Optuna), metrik, cek overfitting/underfitting, robustness, perbandingan model, uji McNemar, analisis per bahasa dan kesalahan, simpan model, ringkasan good fit & robust |
| 10 | Kesimpulan | hasil akhir, keterbatasan, dan rekomendasi |

Semua sumber acak dikunci dengan **`random_state=42`**, jadi hasilnya selalu sama setiap kali dijalankan.

---

## 🎯 Hasil Model Akhir

**Model akhir: e5-large + SVM linear** (`C = 0,58`, `class_weight="balanced"`, dipilih dengan Bayesian Search)

| Metrik | Nilai |
|---|---|
| Macro-F1 data uji | **0,640** |
| Akurasi data uji | **0,716** |
| Macro-F1 CV (5-fold) | 0,648 ± 0,021 |
| Macro-F1 di video yang belum pernah dilihat | 0,590 ± 0,042 |
| Selisih skor latih-uji | 0,105 (good fit) |

**Good fit dan robust?** Ya (ringkasan lengkap di Bab 9.9):
- **Good fit:** selisih latih-uji kecil (0,105), `C = 0,58` berada di puncak kurva validasi, dan garis latih dan uji pada kurva belajar makin rapat.
- **Robust:** stabil antar-fold (± 0,021), skor uji berada di tengah rentang bootstrap (0,603–0,676), tetap bekerja di video baru (0,590, terendah 0,536), dan keunggulannya signifikan menurut uji McNemar.
- **Catatan:** skor turun ke 0,59 di video baru, dan batas skornya ada pada kualitas label (kappa 0,506), bukan pada modelnya.

**Perbandingan dengan model lain:**

| Model | Macro-F1 CV | Macro-F1 uji | Lintas video | Selisih latih-uji |
|---|---|---|---|---|
| TF-IDF + SVM linear (baseline klasik) | 0,566 | 0,569 | 0,469 | 0,409 |
| Naive Bayes, hitungan kata (baseline klasik) | 0,525 | 0,531 | 0,343 | 0,411 |
| e5-large + Naive Bayes | *lihat notebook* | *lihat notebook* | *lihat notebook* | *lihat notebook* |
| e5-large + LR | 0,641 | 0,642 | 0,585 | 0,087 |
| e5-large + KNN (k=15) | 0,619 | 0,659 | 0,506 | 0,037 |
| e5-large + TF-IDF + LR | 0,664 | 0,661 | 0,587 | 0,242 |
| XLM-RoBERTa-large (*fine-tuning*) | - | 0,623 | - | - |
| **e5-large + SVM linear** | 0,648 | 0,640 | **0,590** | 0,105 |

SVM linear dipilih karena **paling seimbang untuk otomasi**: skornya di video baru paling tinggi, tidak overfitting, stabil, dan paling sederhana. Uji McNemar menunjukkan SVM **setara** dengan e5-large + TF-IDF + LR, dan **lebih baik secara signifikan** daripada kedua baseline klasik (TF-IDF + SVM dan Naive Bayes dengan hitungan kata), e5-large + LR, dan KNN pada video baru (p < 0,001). Kedua baseline klasik paling rendah dan paling overfitting, jadi embedding e5-large terbukti penting.

---

## 📊 Visualisasi di Notebook

Setiap grafik diberi penjelasan cara membacanya dan bagian **Hasil**.

| Bab | Grafik | Yang terlihat |
|---|---|---|
| 6.1 | diagram lingkaran sebaran label, 10 komentar dengan *likes* terbanyak per label | perlu ditinjau 59,5%; komentar terpopuler kebanyakan sindiran yang layak ditinjau ulang |
| 9.2 | bukti hitung precision, recall, F1, macro-F1 dari confusion matrix + grafik garisnya | rumus terbukti sama dengan scikit-learn; precision dan recall seimbang |
| 9.2 | confusion matrix (jumlah dan persen), garis kenyataan vs tebakan | positif paling sulit (hanya 49% ditebak benar) |
| 9.2 | kurva logistik dari skor SVM | skor SVM membentuk kurva S, tetapi banyak komentar tumpang-tindih di dekat garis batas |
| 9.2 | ilustrasi SVM: daerah 3 label dan *support vector* | perlu ditinjau berada di daerah "skor negatif dan positif sama-sama rendah" |
| 9.3 | kurva validasi `C`, kurva belajar | `C = 0,58` berada di puncak validasi (good fit) |
| 9.4 | sebaran bootstrap, skor per video baru | skor uji bukan kebetulan; skor turun di video baru |
| 9.5 | ilustrasi KNN (15 tetangga terdekat), skor vs good fit, *heatmap* skor per video | label bercampur sehingga KNN gagal di video baru |
| Colab | hasil validasi XLM-R per epoch, confusion matrix | puncak di epoch 4, lalu mulai overfitting |

---

## 📁 Isi Folder

| Berkas | Isi |
|---|---|
| `classification_modeling.ipynb` | notebook utama: Bab 6–10 |
| `finetune_transformer_colab.ipynb` | percobaan pembanding: *fine-tuning* XLM-RoBERTa-large. Dipisah karena dilatih dan diuji di **Google Colab** untuk meminjam GPU yang lebih kuat (T4, 16 GB), sedangkan GPU laptop hanya 6 GB |
| `model_svm_e5_large.pkl` | model SVM akhir, **dibuat oleh notebook** (Bab 9.8) |
| `hasil_perbandingan_model.csv` | tabel perbandingan model, **dibuat oleh notebook** (Bab 9.8) |

---

## ▶️ Cara Menjalankan

1. Buka notebook di **Google Colab** atau **Antigravity**, lalu jalankan sel dari atas ke bawah. Dataset diambil langsung dari GitHub, jadi tidak perlu upload file (butuh koneksi internet).
2. Bagian yang paling lama: stemming (sekitar 2–3 menit), embedding e5-large (sekitar 2–3 menit di GPU, lebih lama di CPU; saat pertama kali, model sekitar 2 GB diunduh dulu), dan Bayesian Search (sekitar 5 menit).
3. `finetune_transformer_colab.ipynb` sebaiknya dijalankan di Google Colab dengan **T4 GPU** (sekitar 20–30 menit).

---

## ⚠️ Keterbatasan

- Sebagian besar label dibuat oleh AI (Claude Opus 5.5), dengan kecocokan sedang terhadap manusia (kappa 0,506). Pada 90 komentar uji berlabel manusia, model mencapai macro-F1 0,612.
- Data hanya dari 6 video. Pada video baru, skor turun ke sekitar 0,59.
- Label positif paling sulit ditebak (F1 0,485), terutama pada komentar berbahasa Inggris.
