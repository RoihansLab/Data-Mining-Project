# 🧹 Data Preparation & Pelabelan Komentar YouTube

> **Apa kata warganet soal AI yang menggantikan pekerjaan manusia?**
> Folder ini berisi langkah-langkah mengubah ribuan komentar YouTube yang berantakan menjadi **data bersih yang sudah diberi label sikap**, siap dipakai untuk melatih model klasifikasi.

📓 Notebook utama: [`data_preparation_labeling.ipynb`](data_preparation_labeling.ipynb)
📦 Hasil akhir: [`datasets/youtube_comments_label_final.csv`](../../datasets/youtube_comments_label_final.csv) (3.935 komentar berlabel)

---

## 💡 Ringkasan Singkat

- **Data:** 4.458 komentar dari 6 video YouTube (2 berbahasa Indonesia, 4 berbahasa Inggris), dibersihkan menjadi **3.935 komentar**.
- **Label:** setiap komentar diberi satu dari 3 label, yaitu **positif**, **negatif**, atau **perlu ditinjau**.
- **Pelabel:** 449 komentar dilabeli **manusia**, sisanya (3.486) dilabeli **Claude Opus 5.5**. Kualitas label Claude diuji terhadap manusia: **kappa 0,506** (kesepakatan sedang).
- **Temuan utama:** dari komentar yang bersikap jelas, **58,9% khawatir atau menolak** dan 41,1% optimis.

---

## 🗺️ Gambaran Besar

Bayangkan kita punya **4.458 komentar** dari 6 video YouTube. Isinya campur aduk: ada spam judi online, komentar dobel, emoji doang, link, sampai bahasa yang tidak jelas. Komentar-komentar itu juga **belum punya label**, jadi kita belum tahu mana yang khawatir soal AI dan mana yang optimis.

Notebook ini mengerjakan semuanya dalam 5 tahap:

```
📥 Kumpulkan data  →  🔍 Kenali data  →  🧹 Bersihkan  →  📊 Eksplorasi  →  🏷️ Beri label
   4.458 komentar                         3.935 komentar                    3.935 berlabel
```

| Bab | Tahap | Isi |
|---|---|---|
| 1 | Import Library | memasang *library* dan mengunci hasil acak dengan `SEED = 42` |
| 2 | Data Understanding | sumber data, struktur kolom, statistik, jumlah komentar per video, contoh komentar mentah |
| 3 | Preprocessing Data | membersihkan duplikat, teks, spam, komentar pendek, bahasa, dan kolom *likes* |
| 4 | EDA | melihat komposisi data bersih: video, bahasa, emoji, tanda baca, dan *likes* |
| 5 | Pelabelan | panduan, cara pelabelan, uji kualitas label, sebaran label, dan pola sikap |

---

## 🪜 Langkah demi Langkah

### Langkah 1 · Siapkan alat (Bab 1)
Memasang dan memanggil semua *library* yang dibutuhkan, misalnya `pandas` untuk mengolah tabel, `matplotlib` untuk grafik, dan `lingua` untuk mendeteksi bahasa.
Di sini juga dipasang **`SEED = 42`**, semacam "kunci" supaya hasil yang acak selalu sama setiap kali notebook dijalankan ulang.

### Langkah 2 · Kenali datanya (Bab 2)
Data mentah diambil pada **17 Oktober 2026** dengan skrip [`datasets/scrape_youtube_comments.py`](../../datasets/scrape_youtube_comments.py) dari **6 video** (2 berbahasa Indonesia, 4 berbahasa Inggris).
- **Video dipilih secara purposif** (sengaja, bukan acak): bertema sama (AI menggantikan pekerjaan), mencakup dua bahasa, dan punya cukup banyak komentar. Jadi hasilnya adalah **studi kasus** pada 6 video ini.
- **Pengambilan dibatasi 1.500 komentar per video**, diurutkan dari yang terpopuler. Tanpa batas ini, video CGP Grey (sekitar 48 ribu komentar) akan menguasai sekitar 95% data.
- Setiap komentar punya 5 informasi: video asal, akun penulis, isi komentar, jumlah *like*, dan waktu.

🔒 **Privasi:** pada file `youtube_comments.csv` di GitHub, nama akun asli sudah **diganti kode** (`akun_0001`, `akun_0002`, dan seterusnya). Akun yang sama selalu mendapat kode yang sama, jadi semua langkah pembersihan tetap menghasilkan angka yang sama persis.

### Langkah 3 · Bersihkan datanya (Bab 3)
Ibarat mencuci sayur sebelum dimasak. Setiap masalah **dicek dulu jumlahnya, dibersihkan, lalu dicek ulang** sampai masalahnya hilang:

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
| Bahasa tidak jelas (keyakinan deteksi < 0,8) | 121 | dihapus |
| *Likes* berupa teks (`4,4K`) | 42 | diubah jadi angka (4.400) |

Kode akun juga **diganti nomor urut** (`author_id`), lalu kolom akunnya dibuang, supaya data yang disimpan tidak memuat identitas penulis.

**Jumlah komentar setelah setiap tahap:**

| Tahap | Sisa komentar |
|---|---|
| Data mentah | 4.458 |
| Setelah baris dobel dihapus | 4.447 |
| Setelah spam dihapus | 4.411 |
| Setelah isi kembar dihapus | 4.355 |
| Setelah komentar pendek dihapus | 4.056 |
| Setelah bahasa tidak jelas dihapus | **3.935** |

Hasilnya: **523 komentar (11,7%) dibuang**, dan **3.935 komentar bersih** (2.494 berbahasa Inggris dan 1.441 berbahasa Indonesia) siap dilabeli.

> Pembersihan di bab ini **tidak mengubah makna komentar**, karena pelabelan membutuhkan teks yang masih utuh. Pengolahan teks khusus untuk model (huruf kecil, stopword, stemming) dilakukan di notebook klasifikasi.

### Langkah 4 · Lihat polanya (Bab 4 · EDA)
Sebelum memberi label, kita intip dulu isi datanya lewat grafik:

| Bagian | Pertanyaan | Temuan |
|---|---|---|
| 4.1 | Video mana yang paling banyak menyumbang komentar? | tidak seimbang: 125 sampai 1.265 komentar per video |
| 4.2 | Berapa banyak komentar Indonesia dan Inggris? | Inggris 2.494 (63,4%), Indonesia 1.441 (36,6%) |
| 4.3 | Apakah bahasa komentar mengikuti bahasa video? | hampir selalu (96,5% sampai 100%) |
| 4.4 | Seberapa sering emoji dan tanda `?` / `!` dipakai? | emoji 10%, tanda tanya/seru 21%; keduanya dipertahankan karena membawa nada komentar |
| 4.5 | Bagaimana sebaran *likes*? | **52% komentar tidak mendapat like**, hanya 41 komentar yang lebih dari 1.000 like |
| 4.6–4.8 | Komentar mana yang paling sering mendapat *like*? | komentar video CGP Grey paling sering di-*like*; 10 komentar terpopuler semuanya dari video itu |

### Langkah 5 · Beri label (Bab 5)
Setiap komentar diberi salah satu dari **3 label** berdasarkan **sikap penulis terhadap AI dan pekerjaan** (bukan pendapat pelabel dan bukan gaya bahasanya):

| Label | Artinya | Contoh (ilustrasi) |
|---|---|---|
| 🟢 **positif** | tidak takut, optimis, atau mendukung | "AI cuma alat, yang penting kita mau belajar" |
| 🔴 **negatif** | takut, khawatir, menolak, atau menyalahkan AI | "Takut banget kerjaan gue diambil AI" |
| ⚪ **perlu ditinjau** | benar-benar ambigu: *off-topic*, pertanyaan netral, ucapan terima kasih, sindiran yang arahnya tidak jelas | "Bang bahas demo dong" |

**Pohon keputusan** yang dipakai, dijawab berurutan:
1. Apakah komentar membahas AI, pekerjaan, atau dampak AI? Tidak → **perlu ditinjau**.
2. Condong takut, khawatir, pesimis, menolak, atau menyalahkan AI? Ya → **negatif**.
3. Condong tidak takut, optimis, mendukung, atau menyalahkan faktor lain selain AI? Ya → **positif**.
4. Arahnya benar-benar tidak bisa ditentukan → **perlu ditinjau**.

**Kenapa "perlu ditinjau", bukan "netral"?** Banyak komentar berupa sindiran yang sikapnya tersirat: punya sikap, tetapi arahnya sulit dipastikan, jadi tidak tepat disebut netral. Label ini menandai komentar yang **layak ditinjau ulang oleh manusia**. "Positif" sendiri berarti **tidak memandang AI sebagai ancaman bagi pekerjaan**, bukan berarti senang.

**Pelabelan dikerjakan gabungan manusia dan AI:**

| Tahap | Pelabel | Jumlah |
|---|---|---|
| Gold set | manual (manusia) | 150 |
| Sampel acak | manual: pelabel 1 (200) dan pelabel 2 (99) | 299 |
| Sisa komentar | **Claude Opus 5.5**, dengan 200 label pelabel 1 sebagai contoh patokan | 3.486 |

- Untuk 449 komentar berlabel manual, **label manusia yang dipakai**. Asal setiap label dicatat di kolom `sumber_label` (`manual` atau `claude`).
- Pelabelan oleh Claude dilakukan **lewat sesi chat**, bukan lewat kode. Kode di Bab 5 hanya dipakai untuk menguji kualitas label (5.3) dan mencari pola sikap (5.5).

**Kenapa dibantu LLM?** Untuk efisiensi: melabeli 3.935 komentar secara manual oleh tim kecil butuh waktu lama, jadi sebagian kecil dilabeli manual dan sisanya oleh LLM, lalu kualitasnya diuji terhadap label manusia. Uji coba awal memakai Qwen lewat API, tetapi dihentikan karena batasan akses API, lalu dilanjutkan dengan Claude Opus 5.5 lewat chat.

**Uji kualitas label.** 99 label pelabel 2 **tidak pernah dijadikan contoh** untuk Claude, jadi dipakai sebagai uji buta:

| Dibandingkan dengan 99 label manusia | Macro-F1 | Akurasi | Kappa |
|---|---|---|---|
| Label Claude Opus 5.5 (v8) | 0,676 | 0,707 | 0,506 (kesepakatan sedang) |

**Panduan diperbaiki bertahap:**

| Versi | Jumlah label | Kappa |
|---|---|---|
| v1–v3 | 4 label (dengan netral dan tidak relevan) | sekitar 0,39 |
| v6 | 3 label | 0,356 |
| v7 | 3 label | 0,512 |
| **v8 (dipakai)** | 3 label | 0,506 (macro-F1 tertinggi, 0,676) |

Versi akhir (v8) dipilih karena paling cocok dengan label manusia, **bukan berdasarkan skor model**. Karena v8 dipilih dan diuji pada 99 komentar yang sama, kappa 0,506 kemungkinan sedikit lebih tinggi daripada kecocokan pada komentar baru.

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

**Pola sikap (Bab 5.5):**
- 🎬 **Sikap berbeda antarvideo.** Komentar pada video berjudul menakutkan ("KIAMAT KERJA", "unemployment soars", "took my job") paling banyak yang negatif (32–37%), sedangkan video CGP Grey hampir seluruhnya candaan atau *off-topic* (84,5% perlu ditinjau). Data ini hanya menunjukkan perbedaan antarvideo, belum membuktikan bahwa judul video yang menjadi penyebabnya.
- 🗣️ **Komentar berbahasa Indonesia lebih sering bersikap jelas** (negatif 29,6%, positif 21,0%) daripada komentar berbahasa Inggris (negatif 20,5%, positif 14,2%).

---

## 📏 Cara Membaca Skor (Versi Santai)

Bayangkan memetik **durian matang** di kebun. Di kebun ada 10 yang matang, kamu memetik 8, dan 6 di antaranya benar-benar matang.

- **Precision**: dari yang kamu petik, berapa yang benar? → 6 dari 8 = **75%**
- **Recall**: dari yang matang di kebun, berapa yang berhasil kamu petik? → 6 dari 10 = **60%**
- **F1-score**: nilai gabungan keduanya, tidak bisa curang dengan bagus di satu sisi saja.
- **Macro-F1**: rata-rata F1 dari ketiga label, dengan setiap label dianggap sama penting. Ini ukuran utama di proyek ini.
- **Kappa**: seberapa sering dua pelabel sepakat setelah dikurangi kesepakatan yang terjadi karena kebetulan (0 = asal tebak, 1 = sempurna; 0,41–0,60 = sedang).

---

## 📁 Isi Folder & Berkas Terkait

| Berkas | Isi |
|---|---|
| `data_preparation_labeling.ipynb` | notebook persiapan data dan pelabelan (Bab 1–5) |
| `../../datasets/scrape_youtube_comments.py` | skrip *scraping* komentar YouTube |
| `../../datasets/youtube_comments.csv` | data mentah hasil *scraping* (4.458 komentar), dengan nama akun sudah diganti kode |
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
- Versi panduan akhir (v8) dipilih dan diuji pada 99 label manusia yang sama, sehingga kappa 0,506 kemungkinan sedikit lebih tinggi daripada kecocokan pada data baru.
- Label manual dibuat sebelum panduan final dipertegas, dan setiap komentar manual hanya dilabeli satu orang, jadi kesepakatan antarmanusia belum diukur.
- Komentar yang sangat panjang hanya dibaca sekitar 400–450 karakter pertamanya oleh Claude, dan pelabelan lewat chat tidak bisa diulang persis.
- Komentar diambil dengan urutan "paling populer", sehingga komentar yang banyak di-*like* lebih terwakili.
- Data hanya dari 6 video yang dipilih secara purposif (studi kasus), jadi hasilnya belum tentu mewakili seluruh pengguna internet.
- Pada pohon keputusan, negatif dicek lebih dulu daripada positif, sehingga komentar yang condong ke dua arah cenderung berlabel negatif. Porsi negatif (58,9%) mungkin sedikit lebih tinggi dari kenyataannya.
- Sebaliknya, banyak komentar "perlu ditinjau" yang populer berupa sindiran yang diam-diam menyiratkan kekhawatiran. Jika sindiran seperti ini dihitung negatif, porsi kekhawatiran publik bisa lebih besar.
- Panduan belum punya aturan khusus untuk komentar campuran (khawatir sekaligus optimis) dan keluhan soal pekerjaan yang tidak menyebut AI.

---

➡️ **Tahap berikutnya:** data berlabel ini dipakai di notebook [`classification_modeling.ipynb`](../Classification/classification_modeling.ipynb), mulai **Bab 6 (Text Preprocessing)** sampai **Bab 14 (Kesimpulan)**. Di sana, 9 kombinasi fitur dan algoritma dibandingkan secara adil (semua model diseimbangkan, tanpa kebocoran data), dan model akhirnya adalah **SVM linear + e5-large** (macro-F1 data uji 0,640, akurasi 0,716).
