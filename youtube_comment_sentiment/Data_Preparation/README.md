# 🧹 Data Preparation & Pelabelan Komentar YouTube

> **Apa kata warganet soal AI yang menggantikan pekerjaan manusia?**
> Folder ini berisi langkah-langkah mengubah ribuan komentar YouTube yang berantakan menjadi **data bersih yang sudah diberi label sikap**, siap dipakai untuk melatih model klasifikasi.

📓 Notebook utama: [`data_preparation_labeling.ipynb`](data_preparation_labeling.ipynb)
📦 Hasil akhir: [`datasets/youtube_comments_gold.csv`](../../datasets/) (3.929 komentar berlabel)

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

Melabeli 3.929 komentar secara manual butuh waktu lama, jadi pelabelan dilakukan **otomatis oleh AI**. Tapi AI tidak langsung dipercaya: hasilnya diuji dulu.

**a. Buat kunci jawaban (gold set).** 150 komentar dilabeli manual: 50 untuk **dev** (latihan soal, dipakai untuk memilih model) dan 100 untuk **test** (ujian akhir, dipakai sekali untuk menilai).

**b. Adu dua model.**

| Model | Cara kerja | Berjalan di | Skor dev (macro-F1) |
|---|---|---|---|
| **Nemotron 3 Ultra** (550 miliar parameter) | diberi aturan + 10 contoh berlabel (*few-shot*) | server NVIDIA lewat API | **0,474** 🏆 |
| **mDeBERTa-v3** (±280 juta parameter) | mencocokkan komentar dengan kalimat hipotesis (*zero-shot*) | laptop sendiri (GPU) | 0,313 |

**c. Ujian akhir.** Nemotron diuji sekali pada 100 komentar test: **macro-F1 = 0,522** (akurasi 52%). Angka ini jauh di atas tebakan asal (34%), dan kesalahannya kebanyakan terjadi di antara label yang batasnya tipis (netral vs tidak relevan), bukan antara positif dan negatif.

**d. Labeli semuanya.** Nemotron melabeli seluruh 3.929 komentar. Karena server gratis NVIDIA membatasi jumlah permintaan, prosesnya sekitar **20 detik per komentar**. Kodenya dibuat tahan banting: kalau kena batas atau internet putus, ia menunggu lalu mencoba lagi, dan setiap hasil langsung disimpan sehingga bisa dilanjutkan kapan saja tanpa mengulang dari awal.

---

## 🎯 Hasil Akhir

| Label | Jumlah | Persen |
|---|---|---|
| ⚪ tidak relevan | 1.091 | 27,8% |
| 🔴 negatif | 1.039 | 26,4% |
| 🔵 netral | 1.005 | 25,6% |
| 🟢 positif | 794 | 20,2% |

Kalau hanya menghitung komentar yang benar-benar membahas AI atau pekerjaan (2.838 komentar):

> **36,6% khawatir · 35,4% netral · 28,0% optimis**

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
| `data_preparation_labeling.ipynb` | notebook utama (Bab 1–5) |
| `../../datasets/youtube_comments.csv` | data mentah hasil *scraping* (4.458 komentar) |
| `../../datasets/gold_set_final.csv` | 150 komentar berlabel manual (kunci jawaban) |
| `../../datasets/youtube_comments_clean_EDA.csv` | data bersih (dibuat oleh notebook, tidak ikut di GitHub) |
| `../../datasets/youtube_comments_gold.csv` | **hasil akhir**: data bersih + label |

---

## ▶️ Cara Menjalankan

1. **Siapkan API key NVIDIA** (gratis) dari [build.nvidia.com](https://build.nvidia.com), lalu simpan di file `.env` di folder utama proyek:
   ```
   NVIDIA_API_KEY_NEMOTRON_3_ULTRA=nvapi-xxxxxxxx
   ```
   File `.env` tidak ikut ter-*upload* ke GitHub, jadi API key tetap aman.
2. **Buka notebook** di VSCode atau Google Colab, lalu jalankan sel dari atas ke bawah.
3. **Bab 1–4** selesai dalam hitungan detik. **Bab 5.8** (pelabelan seluruh data) butuh waktu lama karena batas permintaan API; kalau terputus, cukup jalankan sel itu lagi dan ia akan melanjutkan dari komentar terakhir.
4. **mDeBERTa** (Bab 5.6) otomatis memakai GPU NVIDIA bila tersedia.

---

## ⚠️ Keterbatasan (Jujur Saja)

- Label dibuat oleh AI, bukan manusia. Dengan macro-F1 sekitar 0,52, persentase di atas adalah **perkiraan**, bukan angka pasti.
- Kunci jawaban (150 komentar) dilabeli oleh **satu orang**, jadi kesepakatan antar-penilai belum diukur.
- Komentar diambil dengan urutan "paling populer", sehingga komentar yang banyak di-*like* lebih terwakili.
- Data hanya dari 6 video, jadi hasilnya belum tentu mewakili seluruh pengguna internet.

---

➡️ **Tahap berikutnya:** data berlabel ini dipakai di folder [`../Classifcation`](../Classifcation) untuk melatih dan membandingkan model klasifikasi (Decision Tree, Naïve Bayes, Random Forest, dan Logistic Regression).
