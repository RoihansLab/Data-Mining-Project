# 🧹 Data Preparation & Pelabelan Komentar YouTube

> **Apa kata warganet soal AI yang menggantikan pekerjaan manusia?**
> Folder ini berisi langkah-langkah mengubah ribuan komentar YouTube yang berantakan menjadi **data bersih yang sudah diberi label sikap**, siap dipakai untuk melatih model klasifikasi.

📓 Notebook utama: [`data_preparation_labeling.ipynb`](data_preparation_labeling.ipynb)
📦 Hasil akhir: [`datasets/youtube_comments_label_claude.csv`](../../datasets/) (3.929 komentar berlabel)

---

## 🗺️ Gambaran Besar

Bayangkan kita punya **4.458 komentar** dari 6 video YouTube. Isinya campur aduk: ada spam judi online, komentar dobel, emoji doang, link, sampai bahasa yang tidak jelas. Komentar-komentar itu juga **belum punya label**, jadi kita belum tahu mana yang khawatir soal AI dan mana yang optimis.

Notebook ini mengerjakan semuanya dalam 5 tahap:

```
📥 Kumpulkan data  →  🔍 Kenali data  →  🧹 Bersihkan  →  📊 Eksplorasi  →  🏷️ Beri label
   4.458 komentar                         3.929 komentar                    3.929 berlabel
```

---

## 🪜 Langkah demi Langkah

### Langkah 1 · Siapkan alat (Bab 1)
Memasang dan memanggil semua *library* yang dibutuhkan, misalnya `pandas` untuk mengolah tabel, `matplotlib` untuk grafik, dan `lingua` untuk mendeteksi bahasa.
Di sini juga dipasang **`SEED = 42`**, semacam "kunci" supaya hasil yang acak selalu sama setiap kali notebook dijalankan ulang.

### Langkah 2 · Kenali datanya (Bab 2)
Data mentah diambil dengan skrip [`datasets/scrape_youtube_comments.py`](../../datasets/scrape_youtube_comments.py) dari **6 video** (2 berbahasa Indonesia, 4 berbahasa Inggris), maksimal 1.500 komentar per video.
Setiap komentar punya 5 informasi: video asal, nama akun, isi komentar, jumlah *like*, dan waktu.

### Langkah 3 · Bersihkan datanya (Bab 3)
Ibarat mencuci sayur sebelum dimasak. Setiap masalah dicek dulu jumlahnya, baru dibersihkan:

| Masalah yang ditemukan | Jumlah | Yang dilakukan |
|---|---|---|
| Baris yang dobel persis | 11 | dihapus |
| Mention `@nama` | 923 | dibuang dari teks |
| Link (URL) | 11 | dibuang dari teks |
| Karakter tak terlihat | 273 | dibuang dari teks |
| Spasi berlebih / baris baru | 1.616 | dirapikan |
| Spam judi online | 33 | dihapus |
| Isi komentar kembar | 59 | dihapus |
| Komentar kurang dari 3 kata ("Up", "Gass") | 305 | dihapus |
| Bahasa tidak jelas | 121 | dihapus |
| *Likes* berupa teks (`4,4K`) | 42 | diubah jadi angka (4.400) |

Nama akun juga **diganti nomor** supaya identitas penulis terlindungi.
Hasilnya: dari **4.458** tersisa **3.929 komentar bersih** (11,9% dibuang).

### Langkah 4 · Lihat polanya (Bab 4 · EDA)
Sebelum memberi label, kita intip dulu isi datanya lewat grafik:
- jumlah komentar per video dan per bahasa (Inggris 2.492, Indonesia 1.437),
- panjang komentar, pemakaian emoji dan tanda tanya/seru,
- sebaran *likes*: **52% komentar tidak mendapat like sama sekali**, dan hanya 41 komentar yang tembus lebih dari 1.000 like.

### Langkah 5 · Beri label (Bab 5)
Setiap komentar diberi salah satu dari 4 label berdasarkan **sikap penulis terhadap AI yang menggantikan pekerjaan**:

| Label | Artinya | Contoh (ilustrasi) |
|---|---|---|
| 🟢 **positif** | tidak merasa terancam, optimis | "AI cuma alat, yang penting kita mau belajar" |
| 🔴 **negatif** | merasa terancam, khawatir | "Pull the plug. Nobody wants AI" |
| 🔵 **netral** | membahas AI tapi tidak memihak | "Kalau AI digabung quantum computing gimana?" |
| ⚪ **tidak relevan** | tidak membahas AI atau pekerjaan | "Bang bahas demo dong" |

Melabeli 3.929 komentar secara manual butuh waktu lama, jadi pelabelan dilakukan oleh **Claude Opus 5.5** (AI buatan Anthropic) lewat sesi chat, bukan lewat kode. Karena itu Bab 5 di notebook hanya berisi penjelasan. Tapi AI tidak langsung dipercaya: hasilnya diuji dulu.

**a. Kunci jawaban (gold set).** 150 komentar dilabeli manual: 50 untuk **dev** (dipakai sebagai contoh untuk Claude) dan 100 untuk **test** (ujian akhir).

**b. Ujian buta.** Claude melabeli 100 komentar test tanpa melihat jawabannya:

| Pelabel | Skor test (macro-F1) |
|---|---|
| **Claude Opus 5.5** | **0,595** 🏆 |
| Nemotron 3 Ultra (dicoba sebelumnya) | 0,522 |

**c. Labeli semuanya.** 3.929 komentar dibagi menjadi 20 kelompok berisi 200 komentar dan dilabeli satu per satu kelompok. Setelah itu hasilnya dicek: setiap komentar harus punya tepat satu label yang sah.

---

## 🎯 Hasil Akhir

| Label | Jumlah | Persen |
|---|---|---|
| ⚪ tidak relevan | 1.423 | 36,2% |
| 🔴 negatif | 988 | 25,1% |
| 🔵 netral | 868 | 22,1% |
| 🟢 positif | 650 | 16,5% |

Kalau hanya menghitung komentar yang benar-benar membahas AI atau pekerjaan (2.506 komentar):

> **39,4% khawatir · 34,6% netral · 25,9% optimis**

Artinya, warganet lebih banyak merasa **khawatir atau belum memihak** dibanding optimis terhadap AI yang menggantikan pekerjaan.

---

## 📏 Cara Membaca Skor (Versi Santai)

Bayangkan memetik **durian matang** di kebun. Di kebun ada 10 yang matang, kamu memetik 8, dan 6 di antaranya benar-benar matang.

- **Precision**: dari yang kamu petik, berapa yang benar? → 6 dari 8 = **75%**
- **Recall**: dari yang matang di kebun, berapa yang berhasil kamu petik? → 6 dari 10 = **60%**
- **F1-score**: nilai gabungan keduanya, tidak bisa curang dengan bagus di satu sisi saja.
- **Macro-F1**: rata-rata F1 dari keempat label, dengan setiap label dianggap sama penting. Ini ukuran utama di proyek ini.

Penjelasan lengkapnya ada di notebook, bagian **"Cara Membaca Hasil Evaluasi"**.

---

## 📁 Isi Folder & Berkas Terkait

| Berkas | Isi |
|---|---|
| `data_preparation_labeling.ipynb` | notebook utama: persiapan data dan pelabelan (Bab 1–5), lalu text preprocessing sampai klasifikasi (Bab 6–9) |
| `../../datasets/youtube_comments.csv` | data mentah hasil *scraping* (4.458 komentar) |
| `../../datasets/gold_set_final.csv` | 150 komentar berlabel manual (kunci jawaban) |
| `../../datasets/youtube_comments_clean_EDA.csv` | data bersih (dibuat oleh notebook, tidak ikut di GitHub) |
| `../../datasets/youtube_comments_label_claude.csv` | **hasil akhir**: data bersih + label dari Claude |
| `model_sikap_ai_terbaik.pkl` | model klasifikasi yang disimpan |

---

## ▶️ Cara Menjalankan

1. **Buka notebook** di VSCode atau Google Colab, lalu jalankan sel dari atas ke bawah. Tidak perlu API key, karena label sudah tersedia di `youtube_comments_label_claude.csv`.
2. **Bab 1–4** selesai dalam hitungan detik. **Bab 5** hanya berisi penjelasan, tidak ada kode yang dijalankan.
3. **Bab 6–9** butuh beberapa menit. Stemming sekitar 2–3 menit, dan deep learning (Bab 8.2) otomatis memakai GPU NVIDIA bila tersedia.

---

## ⚠️ Keterbatasan (Jujur Saja)

- Label dibuat oleh AI, bukan manusia. Dengan macro-F1 sekitar 0,6, persentase di atas adalah **perkiraan**, bukan angka pasti.
- Komentar yang lebih dari 600 karakter hanya dibaca 600 karakter pertamanya saat dilabeli, dan pelabelan lewat chat tidak bisa diulang persis.
- Kunci jawaban (150 komentar) dilabeli oleh **satu orang**, jadi kesepakatan antar-penilai belum diukur.
- Komentar diambil dengan urutan "paling populer", sehingga komentar yang banyak di-*like* lebih terwakili.
- Data hanya dari 6 video, jadi hasilnya belum tentu mewakili seluruh pengguna internet.

---

➡️ **Tahap berikutnya:** data berlabel ini langsung dipakai di notebook yang sama, mulai **Bab 6 (Text Preprocessing)** sampai **Bab 9 (Optimasi)**, untuk melatih dan membandingkan model klasifikasi (Decision Tree, Naïve Bayes, Random Forest, Logistic Regression, dan lainnya).
