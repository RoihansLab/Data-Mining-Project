# 🧹 Data Preparation & Pelabelan Komentar YouTube

> **Apa kata warganet soal AI yang menggantikan pekerjaan manusia?**
> Folder ini berisi langkah-langkah mengubah ribuan komentar YouTube yang berantakan menjadi **data bersih yang sudah diberi label sikap**, siap dipakai untuk melatih model klasifikasi.

📓 Notebook utama: [`data_preparation_labeling.ipynb`](data_preparation_labeling.ipynb)
📦 Hasil akhir: [`datasets/youtube_comments_label_final.csv`](../../datasets/youtube_comments_label_final.csv) (3.935 komentar berlabel)

---

## 🗺️ Gambaran Besar

Bayangkan kita punya **4.458 komentar** dari 6 video YouTube. Isinya campur aduk: ada spam judi online, komentar dobel, emoji doang, link, sampai bahasa yang tidak jelas. Komentar-komentar itu juga **belum punya label**, jadi kita belum tahu mana yang khawatir soal AI dan mana yang optimis.

Notebook ini mengerjakan semuanya dalam 5 tahap:

```
📥 Kumpulkan data  →  🔍 Kenali data  →  🧹 Bersihkan  →  📊 Eksplorasi  →  🏷️ Beri label
   4.458 komentar                         3.935 komentar                    3.935 berlabel
```

---

## 🪜 Langkah demi Langkah

### Langkah 1 · Siapkan alat (Bab 1)
Memasang dan memanggil semua *library* yang dibutuhkan, misalnya `pandas` untuk mengolah tabel, `matplotlib` untuk grafik, dan `lingua` untuk mendeteksi bahasa.
Di sini juga dipasang **`SEED = 42`**, semacam "kunci" supaya hasil yang acak selalu sama setiap kali notebook dijalankan ulang.

### Langkah 2 · Kenali datanya (Bab 2)
Data mentah diambil dengan skrip [`datasets/scrape_youtube_comments.py`](../../datasets/scrape_youtube_comments.py) dari **6 video** (2 berbahasa Indonesia, 4 berbahasa Inggris), maksimal 1.500 komentar per video.
Video dipilih secara **purposif**: bertema sama (AI menggantikan pekerjaan), mencakup dua bahasa, dan punya cukup banyak komentar. Jadi hasilnya adalah **studi kasus** pada 6 video ini.
Setiap komentar punya 5 informasi: video asal, nama akun, isi komentar, jumlah *like*, dan waktu.

### Langkah 3 · Bersihkan datanya (Bab 3)
Ibarat mencuci sayur sebelum dimasak. Setiap masalah dicek dulu jumlahnya, baru dibersihkan:

| Masalah yang ditemukan | Jumlah | Yang dilakukan |
|---|---|---|
| Baris yang dobel persis | 11 | dihapus |
| Karakter tak terlihat | 273 | dibuang dari teks |
| Spasi khusus (NBSP) | 896 | diganti spasi biasa |
| Mention `@nama` | 923 | dibuang dari teks |
| Link (URL) | 11 | dibuang dari teks |
| Spasi berlebih / baris baru | 1.611 | dirapikan |
| Spam judi online | 36 | dihapus |
| Isi komentar kembar | 56 | dihapus |
| Komentar kurang dari 3 kata ("Up", "Gass") | 299 | dihapus |
| Bahasa tidak jelas | 121 | dihapus |
| *Likes* berupa teks (`4,4K`) | 42 | diubah jadi angka (4.400) |

Nama akun juga **diganti nomor** supaya identitas penulis terlindungi.
Hasilnya: dari **4.458** tersisa **3.935 komentar bersih** (11,7% dibuang).

### Langkah 4 · Lihat polanya (Bab 4 · EDA)
Sebelum memberi label, kita intip dulu isi datanya lewat grafik:
- jumlah komentar per video dan per bahasa (Inggris 2.494, Indonesia 1.441),
- panjang komentar, pemakaian emoji dan tanda tanya/seru,
- sebaran *likes*: **52% komentar tidak mendapat like sama sekali**, dan hanya 41 komentar yang tembus lebih dari 1.000 like.

### Langkah 5 · Beri label (Bab 5)
Setiap komentar diberi salah satu dari **3 label** berdasarkan **sikap penulis terhadap AI dan pekerjaan**:

| Label | Artinya | Contoh (ilustrasi) |
|---|---|---|
| 🟢 **positif** | tidak takut, optimis, atau mendukung | "AI cuma alat, yang penting kita mau belajar" |
| 🔴 **negatif** | takut, khawatir, menolak, atau menyalahkan AI | "Takut banget kerjaan gue diambil AI" |
| ⚪ **perlu ditinjau** | benar-benar ambigu: *off-topic*, pertanyaan netral, ucapan terima kasih, sindiran yang arahnya tidak jelas | "Bang bahas demo dong" |

Aturan pentingnya: kalau komentar membahas pekerjaan atau dampak AI, label dipilih **positif atau negatif sesuai arah condongnya**. "Perlu ditinjau" hanya untuk yang benar-benar tidak bisa ditentukan.

**Kenapa "perlu ditinjau", bukan "netral"?** Banyak komentar berupa sindiran yang sikapnya tersirat: punya sikap, tetapi arahnya sulit dipastikan, jadi tidak tepat disebut netral. Label ini menandai komentar yang **layak ditinjau ulang oleh manusia**. "Positif" sendiri berarti **tidak memandang AI sebagai ancaman bagi pekerjaan**, bukan berarti senang.

Pelabelan dikerjakan **gabungan manusia dan AI**:

| Tahap | Pelabel | Jumlah |
|---|---|---|
| Gold set | manual (manusia) | 150 |
| Sampel acak | manual: pelabel 1 (200) dan pelabel 2 (99) | 299 |
| Sisa komentar | **Claude Opus 5.5**, dengan 200 label pelabel 1 sebagai contoh patokan | 3.486 |

Untuk 449 komentar berlabel manual, **label manusia yang dipakai**. Asal setiap label dicatat di kolom `sumber_label` (`manual` atau `claude`). Pelabelan oleh Claude dilakukan lewat sesi chat, bukan lewat kode. Kode di Bab 5 hanya dipakai untuk menguji kualitas label (5.3) dan mencari pola sikap (5.5).

**Kenapa dibantu LLM?** Untuk efisiensi: melabeli 3.935 komentar secara manual oleh tim kecil butuh waktu lama, jadi sebagian kecil dilabeli manual dan sisanya oleh LLM, lalu kualitasnya diuji terhadap label manusia. Uji coba awal memakai Qwen lewat API, tetapi dihentikan karena batasan akses API, lalu dilanjutkan dengan Claude Opus 5.5 lewat chat.

**Uji kualitas label.** 99 label pelabel 2 tidak pernah dijadikan contoh untuk Claude, jadi dipakai sebagai uji buta:

| Dibandingkan dengan 99 label manusia | Macro-F1 | Akurasi | Kappa |
|---|---|---|---|
| Label Claude Opus 5.5 | 0,676 | 0,707 | 0,506 (kesepakatan sedang) |

Angka ini dihitung ulang dengan kode di Bab 5.3. Panduan diperbaiki beberapa kali: kecocokan dengan manusia naik dari kappa sekitar 0,39 (versi awal, 4 label) menjadi sekitar 0,51 (v7–v8, 3 label). Versi akhir (v8) dipilih karena paling cocok dengan label manusia, bukan berdasarkan skor model.

---

## 🎯 Hasil Akhir

| Label | Jumlah | Persen |
|---|---|---|
| ⚪ perlu ditinjau | 2.342 | 59,5% |
| 🔴 negatif | 938 | 23,8% |
| 🟢 positif | 655 | 16,6% |

Kalau hanya menghitung komentar yang punya sikap jelas (1.593 komentar):

> **58,9% khawatir atau menolak · 41,1% optimis**

Artinya, warganet yang bersikap terhadap isu ini **lebih banyak yang khawatir** dibanding yang optimis terhadap AI yang menggantikan pekerjaan.

**Pola tersembunyi (Bab 5.5):**
- 🎬 **Judul video memengaruhi sikap.** Video berjudul menakutkan ("KIAMAT KERJA", "unemployment soars") punya komentar negatif terbanyak (35–37%), sedangkan video CGP Grey hampir seluruhnya candaan atau *off-topic* (84,5% perlu ditinjau).
- 📏 **Makin panjang komentar, makin jelas sikapnya.** Komentar 1–5 kata 87% "perlu ditinjau", sedangkan komentar lebih dari 50 kata 64% punya sikap jelas.
- 👍 **Penonton lebih suka candaan.** Dari 50 komentar dengan *likes* terbanyak, 38 berlabel "perlu ditinjau", hanya 8 negatif dan 4 positif.

---

## 📏 Cara Membaca Skor (Versi Santai)

Bayangkan memetik **durian matang** di kebun. Di kebun ada 10 yang matang, kamu memetik 8, dan 6 di antaranya benar-benar matang.

- **Precision**: dari yang kamu petik, berapa yang benar? → 6 dari 8 = **75%**
- **Recall**: dari yang matang di kebun, berapa yang berhasil kamu petik? → 6 dari 10 = **60%**
- **F1-score**: nilai gabungan keduanya, tidak bisa curang dengan bagus di satu sisi saja.
- **Macro-F1**: rata-rata F1 dari ketiga label, dengan setiap label dianggap sama penting. Ini ukuran utama di proyek ini.
- **Kappa**: seberapa sering dua pelabel sepakat setelah dikurangi kesepakatan yang terjadi karena kebetulan (0 = asal tebak, 1 = sempurna).

---

## 📁 Isi Folder & Berkas Terkait

| Berkas | Isi |
|---|---|
| `data_preparation_labeling.ipynb` | notebook persiapan data dan pelabelan (Bab 1–5) |
| `../../datasets/youtube_comments.csv` | data mentah hasil *scraping* (4.458 komentar) |
| `../../datasets/youtube_comments_clean_EDA.csv` | data bersih (dibuat oleh notebook, tidak ikut di GitHub) |
| `../../datasets/youtube_comments_label_final.csv` | **hasil akhir**: data bersih + label final, dengan kolom `sumber_label` (`manual` atau `claude`) |
| `../../datasets/label_manual_299.csv` | 299 label manual (pelabel 1 dan pelabel 2), dipakai untuk uji kualitas label (Bab 5.3) |
| `../../datasets/label_manual_300.xlsx` | lembar pelabelan manual beserta sheet **Panduan** pelabelan |
| `../../datasets/youtube_comments_label_claude*.csv` | label Claude per versi panduan (v1, v2, v3, v6, v7, v8); v8 adalah versi akhir (Bab 5.3) |

---

## ▶️ Cara Menjalankan

1. **Buka notebook** di **Google Colab** atau **Antigravity**, lalu jalankan sel dari atas ke bawah. Data mentah diambil langsung dari GitHub, jadi tidak perlu upload file (butuh koneksi internet). Tidak perlu API key, karena label sudah tersedia di `youtube_comments_label_final.csv`.
2. **Bab 1–4** selesai dalam hitungan detik sampai beberapa menit. **Bab 5** sebagian besar berisi penjelasan; kodenya (5.3 dan 5.5) hanya membaca label dari GitHub, jadi cepat.

---

## ⚠️ Keterbatasan (Jujur Saja)

- Sebagian besar label (sekitar 89%) dibuat oleh AI, dengan kecocokan **sedang** terhadap manusia (kappa 0,506). Persentase di atas adalah **perkiraan**, bukan angka pasti.
- Label manual dibuat sebelum panduan final dipertegas, dan setiap komentar manual hanya dilabeli satu orang, jadi kesepakatan antar-manusia belum diukur.
- Komentar yang sangat panjang hanya dibaca sekitar 400–450 karakter pertamanya oleh Claude, dan pelabelan lewat chat tidak bisa diulang persis.
- Komentar diambil dengan urutan "paling populer", sehingga komentar yang banyak di-*like* lebih terwakili.
- Data hanya dari 6 video yang dipilih secara purposif (studi kasus), jadi hasilnya belum tentu mewakili seluruh pengguna internet.
- Pada pohon keputusan, negatif dicek lebih dulu daripada positif, sehingga komentar yang condong ke dua arah cenderung berlabel negatif. Porsi negatif (58,9%) mungkin sedikit lebih tinggi dari kenyataannya.
- Panduan belum punya aturan khusus untuk komentar campuran (khawatir sekaligus optimis) dan keluhan soal pekerjaan yang tidak menyebut AI.

---

➡️ **Tahap berikutnya:** data berlabel ini dipakai di notebook [`classification_modeling.ipynb`](../Classification/classification_modeling.ipynb), mulai **Bab 6 (Text Preprocessing)** sampai **Bab 10 (Kesimpulan)**, untuk melatih dan menguji model klasifikasi (model akhir: **e5-large + SVM linear**).
