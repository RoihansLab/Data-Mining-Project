# 💬 Sikap Publik terhadap AI yang Menggantikan Pekerjaan (Komentar YouTube)

Proyek Data Mining (Kelompok 9, TI-3C, Politeknik Negeri Semarang) untuk menjawab dua pertanyaan:
1. Bagaimana sebaran sikap publik (positif, negatif, perlu ditinjau) terhadap isu AI yang menggantikan pekerjaan berdasarkan komentar YouTube?
2. Model klasifikasi mana yang paling seimbang antara performa, *good fit*, dan *robustness* untuk mengotomatisasi deteksi sikap publik?

| Tahap | Folder | Notebook |
|---|---|---|
| 1. Persiapan data dan pelabelan (Bab 1–5) | [`Data_Preparation/`](Data_Preparation/) | `data_preparation_labeling.ipynb` |
| 2. Klasifikasi dan evaluasi (Bab 6–10) | [`Classification/`](Classification/) | `classification_modeling.ipynb` |
| Pembanding *fine-tuning* Transformer | [`Classification/`](Classification/) | `finetune_transformer_colab.ipynb` |

**Hasil singkat:**
- Dari 1.593 komentar yang bersikap jelas, **58,9% khawatir atau menolak** dan 41,1% optimis.
- Model akhir **e5-large + SVM linear**: macro-F1 **0,639**, akurasi **0,715**, good fit, dan robust di video baru (macro-F1 0,590).

Semua notebook bisa dijalankan di **Google Colab** maupun **Antigravity**. Dataset diambil langsung dari folder [`datasets/`](../datasets/) di GitHub.
