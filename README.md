# Data-Mining-Project

Proyek mata kuliah **Data Mining**, Program Studi D4 Teknologi Rekayasa Komputer, **Politeknik Negeri Semarang** (Kelompok 9, TI-3C).

Setiap kelompok mengerjakan **satu proyek penelitian** dari data yang dikumpulkan sendiri secara legal, lalu menuliskannya menjadi **artikel jurnal untuk dipublikasikan**. Repositori ini berisi seluruh proses penelitian kami, mulai dari pengumpulan data sampai evaluasi model, supaya hasilnya bisa diperiksa dan diulang.

## Proyek

| Proyek | Deskripsi |
|---|---|
| [`youtube_comment_sentiment/`](youtube_comment_sentiment/) | Analisis sikap publik terhadap AI yang menggantikan pekerjaan berdasarkan komentar YouTube: persiapan data, pelabelan (manusia dan Claude Opus 5.5), perbandingan 9 kombinasi fitur dan algoritma, serta evaluasi model akhir (**e5-large + SVM linear**) |

## Data

- Data berupa **komentar publik YouTube** dari 6 video, diambil dengan skrip [`datasets/scrape_youtube_comments.py`](datasets/scrape_youtube_comments.py).
- Nama akun penulis komentar sudah **diganti kode** untuk menjaga privasi. Data hanya dipakai untuk keperluan penelitian.
- Semua dataset ada di folder [`datasets/`](datasets/).

## Anggota Kelompok

1. Muhammad Rafa Enrico (4.33.24.2.15)
2. Roihan Saputra (4.33.24.2.20)

**Dosen pembimbing:** Dr. Sukamto, S.Kom., M.T.
