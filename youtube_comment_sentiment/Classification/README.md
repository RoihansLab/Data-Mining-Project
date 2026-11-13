# 🤖 Klasifikasi Sikap Publik terhadap AI yang Menggantikan Pekerjaan

> Folder ini berisi notebook untuk **membandingkan, melatih, dan menguji model** yang menebak sikap sebuah komentar YouTube: **positif**, **negatif**, atau **perlu ditinjau**.

📓 Notebook utama: [`classification_modeling.ipynb`](classification_modeling.ipynb)
📦 Data yang dipakai: [`datasets/youtube_comments_label_final.csv`](../../datasets/youtube_comments_label_final.csv) (3.935 komentar berlabel, hasil notebook [Data Preparation](../Data_Preparation/))

---

## 💡 Ringkasan Singkat

- **Pertanyaan:** model mana yang paling bisa diandalkan untuk menebak sikap komentar YouTube secara otomatis?
- **Yang dibandingkan:** 9 model, yaitu 4 algoritma (SVM, Naive Bayes, Logistic Regression, KNN) × 2 cara mengubah teks jadi angka (e5-large dan TF-IDF), ditambah 1 model *deep learning* (XLM-RoBERTa).
- **Jawaban:** **SVM linear + e5-large**. Model ini unggul dalam performa, paling sedikit menghafal, dan paling stabil di video baru.
- **Nilai akhir di data uji:** macro-F1 **0,640** dan akurasi **0,716**.

---

## 🗺️ Alur Notebook

```
📄 Data berlabel → 🧹 Text preprocessing → ✂️ Pembagian data → 🔢 e5-large & TF-IDF
→ 🤖 9 model (5-fold CV) → 🎯 Bayesian Search → ⚖️ Perbandingan → 📊 Evaluasi di data uji
```

| Bab | Tahap | Isi |
|---|---|---|
| 1 | Import Library | library dikelompokkan per bab, semua sumber acak dikunci dengan angka 42 |
| 6 | Text Preprocessing | case folding, removing, stopword (kata negasi tetap disimpan), tokenizing, dan stemming (Sastrawi & Porter), khusus untuk TF-IDF |
| 7 | Pembagian Data | 80% data latih (3.141) dan 20% data uji (786), *stratified* |
| 8 | Ekstraksi Fitur | embedding **e5-large** (1.024 angka per komentar) dan **TF-IDF** (bobot kata) |
| 9 | Klasifikasi | 4 algoritma × 2 fitur dengan pengaturan standar, dinilai dengan 5-fold CV. Model TF-IDF memakai *pipeline*, dan Naive Bayes serta KNN diseimbangkan dengan SMOTE |
| 10 | Optimasi | Bayesian Search (Optuna, 50 percobaan per model) untuk kedelapan model |
| 11 | Deep Learning | *fine-tuning* **XLM-RoBERTa-large** dengan 5-fold CV yang sama |
| 12 | Perbandingan Model | performa, good fit, robustness (uji lintas video), grafik, uji McNemar, dan model terpilih |
| 13 | Evaluasi di Data Uji | laporan model akhir, confusion matrix, rentang bootstrap, skor per bahasa, skor pada label manusia, contoh kesalahan, dan menyimpan model |
| 14 | Kesimpulan | jawaban rumusan masalah, makna untuk otomatisasi, keterbatasan, dan saran |

---

## 📚 Istilah Penting (Versi Sederhana)

| Istilah | Artinya |
|---|---|
| **e5-large** | model yang sudah dilatih dari jutaan kalimat, untuk mengubah komentar menjadi 1.024 angka sesuai **maknanya**. Komentar yang maknanya mirip punya angka yang mirip |
| **TF-IDF** | cara mengubah komentar menjadi angka berdasarkan **kata-katanya**. Kata yang jarang muncul diberi nilai lebih tinggi |
| **Data latih / data uji** | data latih untuk belajar; data uji disimpan sampai akhir untuk menilai model secara jujur |
| **5-fold cross-validation (CV)** | data latih dibagi 5 bagian. Model belajar dari 4 bagian lalu menebak 1 bagian sisanya, bergiliran 5 kali. Seperti 5 kali *try out* sebelum ujian akhir |
| **Macro-F1** | ukuran utama: rata-rata F1 dari ketiga label, setiap label dianggap sama penting |
| **Class weight** | label yang jumlahnya sedikit diberi bobot kesalahan lebih besar saat model belajar |
| **SMOTE** | membuat data sintetis untuk label yang jumlahnya sedikit, sampai jumlah ketiga label sama |
| **Pipeline** | rangkaian langkah (misalnya TF-IDF → SMOTE → model) yang selalu dijalankan bersama, supaya TF-IDF dan SMOTE hanya belajar dari data latih di setiap fold |
| **Bayesian Search** | cara mencari pengaturan terbaik model. Setiap percobaan berikutnya dipilih berdasarkan hasil percobaan sebelumnya |
| **Uji McNemar** | uji statistik untuk mengecek apakah perbedaan dua model nyata atau hanya kebetulan |

---

## ⚖️ Supaya Perbandingannya Adil

1. **Data uji hanya dipakai sekali**, di Bab 13, untuk model yang sudah terpilih. Pemilihan model di Bab 9–12 hanya memakai data latih.
2. **Semua model memakai 5 fold CV yang sama persis**, termasuk XLM-RoBERTa.
3. **Semua model diseimbangkan**, karena labelnya tidak seimbang (perlu ditinjau 59,5%, negatif 23,8%, positif 16,6%):

| Model | Cara menyeimbangkan |
|---|---|
| SVM linear, Logistic Regression | `class_weight="balanced"` |
| Naive Bayes, KNN | SMOTE (karena tidak punya `class_weight`) |
| XLM-RoBERTa | bobot label `balanced` di *loss* |

4. **Tidak ada kebocoran data (*data leakage*).** TF-IDF dan SMOTE dimasukkan ke dalam *pipeline*, sehingga keduanya hanya belajar dari data latih di setiap fold.

---

## 🏆 Cara Memilih Model

Model dipilih berdasarkan tiga kriteria dari rumusan masalah:

| Kriteria | Ukuran | Artinya |
|---|---|---|
| **Performa** | macro-F1 5-fold CV | seberapa bagus model menebak komentar yang belum pernah dilihat |
| **Good fit** | selisih macro-F1 latih dan CV | makin kecil, makin sedikit model menghafal data latih |
| **Robustness** | macro-F1 lintas video | model dilatih dengan 5 video lalu diuji di 1 video yang belum pernah dilihat, bergiliran untuk keenam video |

**Hasil perbandingan (setelah Bayesian Search):**

| Model | Penyeimbangan | Macro-F1 CV | Selisih latih–CV | Lintas video |
|---|---|---|---|---|
| **SVM linear + e5** | class weight | **0,648** | **0,102** | **0,586** |
| Logistic Regression + e5 | class weight | 0,645 | 0,120 | 0,583 |
| XLM-RoBERTa-large | bobot di *loss* | 0,632 | 0,127 | 0,558 |
| Naive Bayes + e5 | SMOTE | 0,592 | 0,039 | 0,510 |
| Logistic Regression + TF-IDF | class weight | 0,579 | 0,380 | 0,472 |
| SVM linear + TF-IDF | class weight | 0,570 | 0,422 | 0,452 |
| Naive Bayes + TF-IDF | SMOTE | 0,524 | 0,444 | 0,338 |
| KNN + TF-IDF | SMOTE | 0,476 | 0,522 | 0,361 |
| KNN + e5 | SMOTE | 0,470 | 0,530 | 0,353 |

**Yang bisa dibaca dari tabel:**
- **SVM + e5 unggul di ketiga kriteria sekaligus.**
- **e5-large lebih baik daripada TF-IDF** pada SVM, Logistic Regression, dan Naive Bayes. Model TF-IDF lebih banyak menghafal dan lemah di video baru.
- **Model yang lebih rumit tidak selalu lebih baik.** XLM-RoBERTa butuh GPU dan waktu latih jauh lebih lama, tetapi tidak melampaui SVM + e5.
- **SMOTE tidak membantu.** Naive Bayes dan KNN dengan SMOTE tetap paling rendah, karena data sintetis di ruang berdimensi tinggi tidak mirip komentar asli.
- **Uji McNemar:** SVM + e5 lebih sering benar secara signifikan daripada semua model lain (p < 0,001), termasuk Logistic Regression + e5 (166 vs 94 komentar), dan tetap signifikan setelah koreksi Bonferroni.

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

**Artinya:**
- Skor data uji (0,640) **hampir sama dengan skor CV** (0,648), jadi pemilihan model bisa dipercaya dan bukan kebetulan.
- Untuk komentar dari **video baru**, gambaran realistisnya sekitar **0,59** (uji lintas video).
- **Label "perlu ditinjau" paling mudah dikenali** (F1 0,828), sedangkan **positif paling sulit** (F1 0,485).
- Kesalahan terbanyak terjadi pada **sindiran dan sikap yang tersirat**, terutama di batas antara "perlu ditinjau" dan sikap yang jelas.

---

## 📊 Visualisasi di Notebook

| Bab | Grafik | Yang terlihat |
|---|---|---|
| 6.1 | diagram lingkaran sebaran label, 10 komentar dengan *likes* terbanyak per label | perlu ditinjau 59,5%; komentar terpopuler kebanyakan sindiran |
| 12.3 | performa dan robustness setiap model (batang) | SVM + e5 tertinggi; model TF-IDF dan KNN paling rendah di video baru |
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

## 🧪 Cara Memakai Model Akhir

`model_svm_e5_large.pkl` hanya berisi model SVM. Komentar baru harus diubah dulu menjadi angka dengan **e5-large**, dengan cara yang sama seperti saat pelatihan: diberi awalan `"query: "` dan `normalize_embeddings=True`.

```python
import joblib
from sentence_transformers import SentenceTransformer

e5 = SentenceTransformer("intfloat/multilingual-e5-large")
svm = joblib.load("model_svm_e5_large.pkl")

komentar = ["Takut banget kerjaan gue diambil AI", "AI cuma alat, yang penting kita terus belajar"]
angka = e5.encode(["query: " + k for k in komentar], normalize_embeddings=True)
print(svm.predict(angka))
```

Hasilnya berupa label untuk setiap komentar: `positif`, `negatif`, atau `perlu ditinjau`.

Model disimpan dengan scikit-learn di Google Colab. Jika muncul peringatan versi saat `joblib.load`, gunakan versi scikit-learn yang sama dengan Colab.

---

## ▶️ Cara Menjalankan

1. Buka notebook di **Google Colab** dengan runtime **GPU**, lalu pilih *Runtime → Run all*. Dataset diambil langsung dari GitHub, jadi tidak perlu upload file (butuh koneksi internet).
2. Saat diminta, izinkan akses **Google Drive**. Drive dipakai untuk menyimpan hasil XLM-RoBERTa.
3. Bagian yang paling lama:
   - stemming: sekitar 2–3 menit
   - embedding e5-large: sekitar 1–2 menit (saat pertama kali, model sekitar 2 GB diunduh dulu)
   - Bayesian Search: sekitar 15–40 menit, karena TF-IDF dan SMOTE dijalankan ulang di setiap fold
   - XLM-RoBERTa: sekitar 5 menit per pelatihan, atau sekitar 1 jam untuk 5-fold CV dan uji lintas video jika belum ada hasil tersimpan di Drive

---

## ⚠️ Keterbatasan

- Sekitar 89% label dibuat oleh AI (Claude Opus 5.5), dengan kecocokan sedang terhadap manusia (kappa 0,506). Pada 90 komentar uji berlabel manusia, model mencapai macro-F1 0,612.
- Setiap komentar berlabel manual hanya dilabeli satu orang, sehingga kesepakatan antarpelabel manusia belum diukur.
- Data hanya dari 6 video, dengan dua video berbahasa Indonesia.
- XLM-RoBERTa tidak dioptimasi dengan Bayesian Search karena keterbatasan komputasi.
- Uji McNemar dihitung dari tebakan cross-validation, sehingga sedikit kurang ketat daripada uji pada satu data uji yang sama.
