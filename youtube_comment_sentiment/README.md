# 💬 Sikap Publik terhadap AI yang Menggantikan Pekerjaan (Komentar YouTube)

Proyek Data Mining (Kelompok 9, TI-3C, Politeknik Negeri Semarang) untuk menjawab dua pertanyaan:
1. Bagaimana sebaran sikap publik (positif, negatif, perlu ditinjau) terhadap isu AI yang menggantikan pekerjaan berdasarkan komentar YouTube?
2. Kombinasi fitur (e5-large dan TF-IDF) dan algoritma klasifikasi (SVM linear, Naive Bayes, Logistic Regression, KNN, serta *fine-tuning* XLM-RoBERTa) mana yang paling seimbang antara performa, *good fit*, dan *robustness* untuk mengotomatisasi deteksi sikap publik?

| Tahap | Folder | Notebook |
|---|---|---|
| 1. Persiapan data dan pelabelan (Bab 1–5) | [`Data_Preparation/`](Data_Preparation/) | `data_preparation_labeling.ipynb` |
| 2. Klasifikasi, perbandingan model, dan evaluasi (Bab 6–14) | [`Classification/`](Classification/) | `classification_modeling.ipynb` |

**Hasil singkat:**
- **Data:** 4.458 komentar dari 6 video YouTube dibersihkan menjadi **3.935 komentar**, lalu diberi label oleh manusia (449) dan Claude Opus 5.5 (3.486), dengan kecocokan terhadap manusia **kappa 0,506**.
- **Sikap publik:** dari 1.593 komentar yang bersikap jelas, **58,9% khawatir atau menolak** dan 41,1% optimis.
- **Perbandingan model:** 9 kombinasi dibandingkan dengan 5-fold CV, Bayesian Search, dan uji lintas video. Fitur **e5-large lebih baik daripada TF-IDF** untuk semua algoritma.
- **Model akhir: SVM linear + e5-large**, unggul di ketiga kriteria (macro-F1 CV 0,648, selisih latih–CV 0,102, lintas video 0,586) dan lebih baik secara signifikan menurut uji McNemar. Di data uji: macro-F1 **0,640**, akurasi **0,716**.

**Cara menjalankan:**
- `data_preparation_labeling.ipynb` bisa dijalankan di **Google Colab** maupun **Antigravity**.
- `classification_modeling.ipynb` dijalankan di **Google Colab dengan GPU**, karena melatih XLM-RoBERTa dan menyimpan hasilnya ke Google Drive.
- Dataset diambil langsung dari folder [`datasets/`](../datasets/) di GitHub. Nama akun pada data mentah sudah diganti kode untuk menjaga privasi.
