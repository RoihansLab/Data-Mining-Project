# 💬 Sikap Publik terhadap AI yang Menggantikan Pekerjaan (Komentar YouTube)

Proyek Data Mining (Kelompok 9, TI-3C, Politeknik Negeri Semarang) untuk menjawab dua pertanyaan:
1. Bagaimana sebaran sikap publik (positif, negatif, perlu ditinjau) terhadap isu AI yang menggantikan pekerjaan berdasarkan komentar YouTube?
2. Kombinasi fitur (e5-large dan TF-IDF) dan algoritma klasifikasi (SVM linear, Naive Bayes, Logistic Regression, KNN, serta *fine-tuning* XLM-RoBERTa) mana yang paling seimbang antara performa, *good fit*, dan *robustness* untuk mengotomatisasi deteksi sikap publik?

---

## 🗺️ Alur Proyek

```
📥 Scraping 6 video → 🧹 Pembersihan → 🏷️ Pelabelan (manusia + Claude) → 🤖 9 model → ⚖️ Perbandingan → 📊 Evaluasi
   4.458 komentar      3.935 komentar      3 label                        5-fold CV    3 kriteria     data uji
```

| Tahap | Folder | Notebook | Isi |
|---|---|---|---|
| 1. Persiapan data dan pelabelan (Bab 1–5) | [`Data_Preparation/`](Data_Preparation/) | `data_preparation_labeling.ipynb` | memahami data, membersihkan komentar, EDA, dan memberi label sikap |
| 2. Klasifikasi, perbandingan model, dan evaluasi (Bab 6–14) | [`Classification/`](Classification/) | `classification_modeling.ipynb` | mengubah teks jadi angka, melatih dan membandingkan 9 model, lalu menguji model terbaik |

Setiap folder punya README sendiri yang menjelaskan langkahnya secara lebih detail.

---

## 🎯 Hasil Singkat

**Jawaban rumusan masalah 1 (sebaran sikap publik):**
- 4.458 komentar dari 6 video YouTube dibersihkan menjadi **3.935 komentar**, lalu diberi label oleh manusia (449) dan Claude Opus 5.5 (3.486). Kecocokan label Claude dengan manusia: **kappa 0,506** (sedang).
- Sebaran label: perlu ditinjau 59,5%, negatif 23,8%, dan positif 16,6%.
- Dari 1.593 komentar yang bersikap jelas, **58,9% khawatir atau menolak** dan 41,1% optimis.

**Jawaban rumusan masalah 2 (model paling seimbang):**
- 9 kombinasi dibandingkan secara adil: semua model memakai **5-fold CV yang sama**, **semua diseimbangkan** (class weight, SMOTE, atau bobot di *loss*), dan **tanpa kebocoran data** (TF-IDF dan SMOTE ada di dalam *pipeline*).
- Fitur **e5-large lebih baik daripada TF-IDF** pada SVM, Logistic Regression, dan Naive Bayes.
- **Model akhir: SVM linear + e5-large**, unggul di ketiga kriteria (macro-F1 CV 0,648, selisih latih–CV 0,102, lintas video 0,586) dan lebih sering benar secara signifikan daripada semua model lain menurut uji McNemar (p < 0,001).
- **Di data uji:** macro-F1 **0,640** dan akurasi **0,716**. Untuk komentar dari video baru, gambaran realistisnya sekitar 0,59.

---

## ▶️ Cara Menjalankan

- `data_preparation_labeling.ipynb` bisa dijalankan di **Google Colab** maupun **Antigravity**.
- `classification_modeling.ipynb` dijalankan di **Google Colab dengan GPU**, karena melatih XLM-RoBERTa dan menyimpan hasilnya ke Google Drive.
- Dataset diambil langsung dari folder [`datasets/`](../datasets/) di GitHub, jadi tidak perlu upload file. Nama akun pada data mentah sudah diganti kode untuk menjaga privasi.
