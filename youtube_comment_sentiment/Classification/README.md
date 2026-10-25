# Classification & Modeling

Folder ini berisi notebook dan artefak pemodelan Machine Learning untuk klasifikasi sentimen/sikap publik terhadap isu AI yang menggantikan pekerjaan manusia.

---

## Isi Berkas
1. **[`classification_modeling.ipynb`](classification_modeling.ipynb)**:
   - **Text Preprocessing:** Case folding, cleaning, stopword removal (Sastrawi & NLTK), tokenizing, dan stemming.
   - **Ekstraksi Fitur:** TF-IDF, FastText word embedding, dan e5 sentence embedding.
   - **Pemodelan:** Decision Tree, Naïve Bayes, Random Forest, Logistic Regression, Extra Trees, Linear SVM, serta perbandingan fine-tuning transformer.
   - **Optimasi:** Bayesian Search dengan Optuna untuk pencarian hyperparameter terbaik.
2. **`model_sikap_ai_terbaik.pkl`**:
   - Bobot model klasifikasi terbaik yang telah dilatih dan siap diimplementasikan untuk inferensi data baru.

---

## Dataset yang Digunakan
Notebook ini secara otomatis membaca dataset final yang sudah berlabel dari folder `datasets/`:
- `datasets/youtube_comments_label_claude_v2.csv` (3.929 komentar berlabel).
