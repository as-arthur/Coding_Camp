# Laporan Proyek Machine Learning - Muhammad Fathurrahman

## Project Overview

Industri penerbitan buku yang berkembang pesat menyebabkan information overload bagi pembaca, menyulitkan mereka menemukan buku yang relevan dan sesuai minat. Tantangan ini juga berdampak pada visibilitas buku bagi penerbit dan penulis. Sistem rekomendasi buku menjadi solusi krusial untuk mengatasi masalah ini, membantu pembaca menemukan buku yang tepat dengan efisien serta meningkatkan penjualan dan loyalitas pembaca bagi industri.

Proyek ini akan mengembangkan sistem rekomendasi buku menggunakan dua pendekatan terpisah: Content-Based Filtering dan Collaborative Filtering.

Content-Based Filtering (CBF): Merekomendasikan buku berdasarkan kesamaan atribut (genre, penulis, deskripsi) dengan preferensi pengguna sebelumnya. Pendekatan ini efektif untuk buku baru dan memberikan transparansi dalam rekomendasi.

Collaborative Filtering (CF): Merekomendasikan buku berdasarkan perilaku dan rating pengguna lain yang memiliki preferensi serupa. Metode ini berguna untuk menemukan pola tersembunyi dan dapat menghasilkan rekomendasi yang tidak terduga namun relevan (serendipitous).

Dengan mengeksplorasi kedua metode ini secara independen, proyek ini bertujuan memberikan wawasan komprehensif mengenai efektivitas masing-masing dalam memenuhi kebutuhan personalisasi rekomendasi buku.

**Referensi:**
- Rokhim, A., & Saikhu, A. (2017). Sistem rekomendasi buku pada aplikasi perpustakaan menggunakan metode collaborative filtering pada smkn 1 bangil. SPIRIT, 8(2).
- Maulidah, M., Gata, W., Aulianita, R., & Agustyaningrum, C. I. (2020). Algoritma Klasifikasi Decision Tree Untuk Rekomendasi Buku Berdasarkan Kategori Buku. E-Bisnis: Jurnal Ilmiah Ekonomi dan Bisnis , 13 (2), 89-96.
- Dharmawan, H., Hilabi, S. S., & Karniawulan, I. (2023). Sistem Rekomendasi Buku dengan Metode K-Nearest Neighbor (K-NN) pada Gramedia. ZONAsi: Jurnal Sistem Informasi, 5(1), 16-25.
- Zayyad, M. R. A. (2021). Sistem Rekomendasi Buku Menggunakan Metode Content Based Filtering.
        
## Business Understanding

### Problem Statements

1. Bagaimana membuat sistem yang dapat memberikan rekomendasi buku yang sesuai dengan preferensi pembaca?
2. Bagaimana memanfaatkan data rating dan informasi buku untuk menghasilkan rekomendasi yang personal?

### Goals

1. Membuat sistem rekomendasi yang dapat memprediksi rating buku yang mungkin diberikan user
2. Menghasilkan daftar rekomendasi buku yang sesuai dengan preferensi pembaca

### Solution Statements

1. Mengembangkan model collaborative filtering untuk memprediksi rating
2. Menggunakan teknik content-based filtering berdasarkan fitur buku
3. Menggunakan metrik RMSE dan MAE untuk melakukan evaluasi pada collaborative filtering

## Data Understanding
Dataset yang digunakan berasal dari Kaggle dan terdiri dari tiga file utama: **Books.csv**, **Ratings.csv**, dan **Users.csv**. Ketiga dataset ini merepresentasikan sistem rekomendasi buku berdasarkan informasi buku, pengguna, dan penilaian mereka terhadap buku.
Sumber Data : https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset   
### 1. Books.csv 
Dataset ini memuat informasi tentang buku yang tersedia dalam sistem. Dataset ini terdiri dari 8 kolom dan 271.360 baris data. Terdapat 6 baris data kosong, namun tidak ditemukan data duplikat.

**Fitur-fitur:**
- `ISBN`: Nomor identifikasi unik untuk setiap buku (International Standard Book Number).
- `Book-Title`: Judul buku.
- `Book-Author`: Nama penulis buku.
- `Year-Of-Publication`: Tahun terbit buku.
- `Publisher`: Nama penerbit buku.
- `Image-URL-S`: URL gambar sampul buku ukuran kecil.
- `Image-URL-M`: URL gambar sampul buku ukuran sedang.
- `Image-URL-L`: URL gambar sampul buku ukuran besar.

---

### 2. Ratings.csv 
Dataset ini mencatat penilaian (rating) yang diberikan oleh pengguna terhadap buku. Dataset ini terdiri dari 3 kolom dan 1.149.780 baris data. Tidak terdapat nilai kosong maupun data duplikat.

**Fitur-fitur:**
- `User-ID`: Identitas unik pengguna.
- `ISBN`: Identitas unik buku yang dinilai.
- `Book-Rating`: Nilai rating yang diberikan oleh pengguna terhadap buku.

---

### 3. Users.csv 
Dataset ini menyimpan informasi tentang pengguna. Terdiri dari 3 kolom dan 278.858 baris data. Terdapat 110.762 nilai kosong, khususnya pada kolom 'Age', namun tidak ditemukan data duplikat.

**Fitur-fitur:**
- `User-ID`: Identitas unik pengguna.
- `Location`: Lokasi geografis pengguna dalam format “Kota, Negara Bagian, Negara”.
- `Age`: Usia pengguna.

## Exploratory Data Analysis (Univariate)

Analisis univariat dilakukan untuk memahami distribusi dari masing-masing variabel:

#### Books.csv
- Sebagian besar buku diterbitkan antara tahun **1980–2005**
- Ditemukan nilai tahun tidak valid seperti `0`, `1376`, `2038`, dan `2050`
- Sebaran penulis dan penerbit sangat luas dan tidak terstandarisasi

#### Ratings.csv
- Mayoritas entri merupakan rating **0** (interaksi pasif)
- Rating eksplisit paling banyak adalah **8**, **10**, dan **7**

#### Users.csv
- Banyak pengguna berasal dari negara berbahasa Inggris (UK, Canada, USA, Australia)
- Lokasi sangat bervariasi dan tidak distandarisasi
- Perlu filtering usia karena terdapat nilai ekstrem

## Data Preparation

Tahapan _data preparation_ dilakukan untuk memastikan data yang digunakan dalam proses pemodelan sistem rekomendasi memiliki kualitas yang baik. Langkah-langkah yang dilakukan meliputi penggabungan dataset, pembersihan data, transformasi data, serta seleksi fitur untuk pendekatan content-based filtering dan collaborative filtering.

### 1. Penggabungan Dataset

Dataset awal terdiri dari tiga file utama, yaitu `Books.csv`, `Ratings.csv`, dan `Users.csv`. Ketiga file ini digabungkan berdasarkan kolom `ISBN` dan `User-ID`, menghasilkan satu dataset terintegrasi dengan total sebanyak **1.031.132 baris data** dan **12 kolom**. Hasil penggabungan mencakup informasi lengkap terkait buku (judul, penulis, tahun terbit), pengguna (lokasi dan usia), serta nilai rating buku.

### 2. Pembersihan Data Kosong

Setelah penggabungan, dilakukan penghapusan terhadap baris-baris data yang mengandung nilai kosong, khususnya pada kolom `Book-Author`, `Publisher`, dan `Age`. Dari total data gabungan, sebanyak **277.837 baris** dihapus karena tidak memenuhi kelengkapan data, sehingga tersisa **753.295 baris data lengkap** untuk dianalisis lebih lanjut.

### 3. Penghapusan Fitur yang Tidak Relevan

Kolom-kolom seperti `Image-URL-S`, `Image-URL-M`, `Image-URL-L`, dan `Publisher` dihapus dari dataset karena tidak memberikan kontribusi signifikan dalam sistem rekomendasi berbasis konten atau kolaboratif. Tujuan dari penghapusan ini adalah untuk menyederhanakan dataset dan mengurangi kompleksitas proses analisis.

### 4. Validasi dan Normalisasi ISBN

Kolom `ISBN` diperiksa untuk memastikan hanya berisi angka. ISBN yang mengandung karakter selain digit atau yang panjangnya kurang dari **10 digit** dihapus dari dataset. Hal ini penting agar setiap buku memiliki identifikasi unik yang valid dan seragam.

### 5. Konversi Tipe Data

Beberapa kolom seperti `Year-Of-Publication`, `Age`, dan `ISBN` dikonversi ke dalam format bilangan bulat (_integer_) agar dapat diproses lebih optimal dalam analisis statistik dan algoritma rekomendasi.

### 6. Filter Berdasarkan Rating

Dalam sistem rekomendasi, rating dengan nilai nol biasanya merepresentasikan bahwa pengguna tidak benar-benar memberikan penilaian terhadap buku tersebut. Oleh karena itu, data dengan nilai rating **0** dihapus, dan hanya rating dengan nilai **1 hingga 10** yang digunakan untuk melatih model.

### 7. Filter Berdasarkan Usia Pengguna

Untuk menjaga validitas data demografis pengguna, hanya usia antara **6 hingga 75 tahun** yang disertakan dalam dataset. Rentang ini dipilih berdasarkan pertimbangan usia minimum anak mulai membaca (sekitar 6 tahun menurut American Academy of Pediatrics) dan usia harapan hidup global pada tahun 2024 yang berkisar **73,33 tahun**, dengan maksimum didefinisikan di **75 tahun**.

Referensi:
- Umur harapan hidup global: [Kompas.id](https://www.kompas.id/artikel/sampai-usia-berapa-manusia-bisa-hidup)
- Usia anak mulai membaca: [Tempo.co](https://www.tempo.co/gaya-hidup/umur-berapa-sebaiknya-anak-dibimbing-belajar-membaca--224080)

### 8. Filter Tahun Terbit Buku

Tahun terbit buku juga difilter agar hanya mencakup data dari tahun **1 hingga 2025**. Buku yang memiliki tahun terbit **0** atau lebih dari **2025** dianggap tidak valid dan dihapus dari dataset.

### 9. Ekstraksi Lokasi Pengguna

Kolom `Location` yang berisi informasi dalam format "Kota, Provinsi/Negara Bagian, Negara" dipisah menjadi tiga kolom terpisah yaitu `City`, `State`, dan `Country`. Pemisahan ini memungkinkan analisis lokasi geografis dilakukan secara lebih terperinci. Setiap elemen lokasi juga dibersihkan dari spasi yang tidak perlu.

### 10. Filter Berdasarkan Nama Penulis

Data penulis yang bernama tidak valid seperti `'x x'` dihapus. Selain itu, hanya penulis yang memiliki **lebih dari satu** buku di dalam dataset yang dipertahankan. Hal ini dilakukan untuk memastikan bahwa model tidak dipengaruhi oleh outlier dari penulis dengan hanya satu karya yang mungkin tidak representatif.

### 11. Pembersihan dan Pra-pemrosesan Teks

Seluruh data pada kolom `Book-Title` dan `Book-Author` dibersihkan melalui beberapa tahapan sebagai berikut:

- Pembersihan karakter khusus atau tanda baca
- Konversi huruf menjadi huruf kecil (_case folding_)
- Tokenisasi teks menjadi kata-kata
- Penghapusan kata-kata umum (_stop words_)
- Penggabungan kembali kata-kata bersih menjadi kalimat

Langkah-langkah ini penting agar data teks lebih terstruktur dan konsisten sebelum digunakan dalam representasi fitur berbasis teks.

### 12. Seleksi Fitur untuk Content-Based Filtering

Untuk pendekatan content-based, dipilih beberapa fitur utama, yaitu:

- `Book-Title` (dalam bentuk kalimat bersih)
- `Book-Author` (dalam bentuk kalimat bersih)
- `Year-Of-Publication`

Setelah dilakukan seleksi, ditemukan bahwa terdapat **12.792** duplikasi data yang kemudian dihapus untuk memastikan keunikan representasi setiap buku.

Fitur `Book-Title` kemudian diproses menggunakan teknik TF-IDF (Term Frequency–Inverse Document Frequency), sementara `Book-Author` direpresentasikan dengan metode one-hot encoding. Kolom `Year-Of-Publication` dinormalisasi menggunakan teknik Min-Max Scaling, agar berada dalam rentang nilai antara 0 dan 1.

Ketiga jenis fitur tersebut (judul, penulis, dan tahun) kemudian dikombinasikan ke dalam satu matriks fitur gabungan (_combined features_) yang akan digunakan untuk menghitung kemiripan antar buku.

### 13. Penghapusan Duplikat Data

Sebelum membangun model content-based, dilakukan pengecekan terhadap data duplikat pada `content_df`. Ditemukan sebanyak **12.792** baris duplikat yang kemudian dihapus untuk memastikan setiap buku memiliki representasi unik. Setelah penghapusan, jumlah duplikasi menjadi **0**.

Langkah ini penting untuk menjaga akurasi dalam perhitungan kemiripan antar buku dan menghindari bias akibat data yang berulang.


### 14. Representasi Fitur Judul Buku (TF-IDF)

Fitur `Book-Title` yang telah dibersihkan direpresentasikan menggunakan teknik **TF-IDF (Term Frequency–Inverse Document Frequency)**. Pendekatan ini digunakan untuk mengekstrak bobot penting dari kata-kata dalam judul buku, sehingga memungkinkan sistem mengenali kesamaan konten antar buku berdasarkan representasi vektor.

### 15. Representasi Fitur Penulis (One-Hot Encoding)

Fitur `Book-Author` direpresentasikan menggunakan metode **One-Hot Encoding**, di mana setiap nama penulis diubah menjadi vektor biner. Representasi ini memungkinkan algoritma mengenali keberadaan penulis sebagai atribut penting dalam pencocokan konten.

### 16. Normalisasi Tahun Terbit (Min-Max Scaling)

Fitur `Year-Of-Publication` dinormalisasi menggunakan teknik **Min-Max Scaling** ke dalam rentang 0 hingga 1. Tujuannya adalah untuk menyamakan skala fitur numerik dengan fitur lain dalam proses pembobotan kemiripan antar buku.

Ketiga fitur (judul, penulis, dan tahun) kemudian dikombinasikan ke dalam satu **matriks fitur gabungan** yang digunakan sebagai dasar penghitungan kemiripan dalam sistem *content-based filtering*.

### 17. Seleksi Fitur untuk Collaborative Filtering

Untuk pendekatan **collaborative filtering**, fitur yang digunakan terbatas pada:

- `User-ID`
- `ISBN`
- `Book-Rating`

Setelah melalui proses filter, diperoleh **28.011 interaksi eksplisit** antara pengguna dan buku. Selanjutnya, identitas pengguna dan ISBN dienkode menjadi nilai numerik untuk keperluan pemetaan. Nilai rating dikonversi ke tipe `float32` dan dinormalisasi dalam rentang 0–1 untuk kesiapan dalam pelatihan model berbasis *neural collaborative filtering*.

---

### 18. Pembagian Dataset

Dataset hasil filtering untuk collaborative filtering diacak dan dibagi menjadi dua bagian:

- **80%** sebagai *training set*
- **20%** sebagai *validation set*

Pembagian ini bertujuan untuk mengukur performa model dalam memprediksi interaksi baru secara adil dan representatif.

## Modeling and Result

Dalam proyek ini, dikembangkan dua pendekatan sistem rekomendasi buku yang berbeda untuk menyelesaikan permasalahan: **Content-Based Filtering** dan **Collaborative Filtering**. Setiap pendekatan dirancang untuk memberikan **Top-N Recommendation** yang sesuai dengan preferensi pengguna berdasarkan data yang tersedia.

### 1. Content-Based Filtering

Pendekatan pertama dalam sistem rekomendasi ini menggunakan teknik **Content-Based Filtering**, yaitu metode yang merekomendasikan buku berdasarkan kemiripan fitur antar item. Sistem ini tidak bergantung pada data historis pengguna, melainkan memanfaatkan atribut yang dimiliki oleh setiap buku.

#### Fitur yang Digunakan

Untuk menentukan kemiripan antar buku, digunakan tiga fitur utama:

- **Judul buku** (`Book-Title`)  
  → Diolah menggunakan teknik **TF-IDF (Term Frequency-Inverse Document Frequency)** untuk menangkap representasi teks dari judul buku dalam bentuk vektor.

- **Penulis buku** (`Book-Author`)  
  → Diubah ke dalam bentuk numerik menggunakan **One-Hot Encoding** untuk membedakan setiap penulis secara unik.

- **Tahun terbit** (`Year-Of-Publication`)  
  → Dinormalisasi menggunakan teknik **Min-Max Normalization** agar berada dalam rentang yang seragam dan tidak mendominasi fitur lain.

Seluruh fitur tersebut digabungkan untuk merepresentasikan setiap buku dalam ruang vektor multidimensi. Kemudian, kemiripan antar buku dihitung menggunakan **Cosine Similarity**, menghasilkan matriks kesamaan yang menjadi dasar rekomendasi.

#### Hasil Rekomendasi

Untuk ISBN `2290306126`, sistem memberikan rekomendasi **Top-5 buku paling mirip** sebagai berikut:

1. *viou jai lu* (henri troyat, 1994)  
2. *terrible tsarinas five russian women in power* (henri troyat, 2001)  
3. *la troisiãâme fille* (agatha christie, 1998)  
4. *le bonheur un jour ã la fois* (collectif, 1999)  
5. *la poursuite du bonheur* (michel houellebecq, 2002)

Buku-buku di atas dipilih karena memiliki kemiripan tinggi dengan buku input berdasarkan fitur kontennya, khususnya pada pola kata dalam judul dan penulis yang sering muncul bersama tema "dreams".

#### Evaluasi Rekomendasi

Hasil evaluasi menunjukkan bahwa sistem menghasilkan **Precision@5 sebesar 1.00**, artinya semua buku dalam Top-5 rekomendasi termasuk dalam daftar buku relevan yang ditentukan. Hal ini menunjukkan performa sistem yang sangat baik dalam skenario pengujian ini.

#### Kelebihan

- Tidak memerlukan data perilaku pengguna, sehingga cocok untuk sistem dengan data pengguna terbatas atau baru.
- Rekomendasi dapat dijelaskan secara transparan karena berbasis pada fitur yang dapat diidentifikasi secara langsung.
- Dapat bekerja dengan baik meskipun hanya tersedia metadata dari item (judul, penulis, tahun terbit).

#### Kekurangan

- Rekomendasi hanya terbatas pada item yang memiliki fitur serupa dengan input, sehingga kurang menangkap preferensi pengguna yang lebih kompleks.
- Kurang efektif untuk buku-buku baru yang tidak memiliki fitur mirip dengan buku lain, dikenal sebagai masalah *cold start* pada item.

---

## 2. Collaborative Filtering (Neural Collaborative Filtering)

Pendekatan kedua yang digunakan adalah **Neural Collaborative Filtering (NCF)**, yaitu teknik *Collaborative Filtering* berbasis deep learning. Model ini mempelajari representasi (*embedding*) pengguna dan buku, kemudian memprediksi skor preferensi melalui interaksi antar keduanya.

Model dilatih dengan data interaksi eksplisit antara pengguna dan buku, yang mencakup:

- **User-ID**: Identitas unik pengguna  
- **ISBN**: Identitas unik buku  
- **Book-Rating**: Nilai rating yang diberikan pengguna pada buku tertentu  

### Arsitektur Model

1. **Embedding Layer**  
   - *User Embedding*: Setiap pengguna direpresentasikan oleh vektor embedding berdimensi tetap (`embedding_size`).
   - *Book Embedding*: Setiap buku juga direpresentasikan oleh vektor embedding serupa.

2. **Dot Product**  
   - Perhitungan interaksi dilakukan dengan mengambil dot product antara vektor pengguna dan buku.

3. **Bias Tambahan**  
   - Ditambahkan bias pengguna dan bias buku untuk mengakomodasi preferensi umum atau popularitas.

4. **Aktivasi Sigmoid**  
   - Output akhir dikonversi menjadi skor antara 0 dan 1 melalui fungsi sigmoid.

---

### Output Top-10 Rekomendasi Buku

Sebagai contoh penerapan, model diuji pada **User-ID: 212002**. Berikut adalah daftar buku yang disukai pengguna tersebut:

#### Buku-buku yang Disukai oleh User 212002:

| Judul Buku                           | Penulis             | Rating | ISBN        |
|--------------------------------------|---------------------|--------|-------------|
| *Geschehnisse am Wasser*             | Kerstin Ekman       | 9.0    | 3442720621  |
| *At E.R.O.S.*                        | Greg Iles           | 9.0    | 3404142357  |
| *Tote lügen nicht*                   | Kathy Reichs        | 8.0    | 3442352266  |
| *Der zweite Mord*                    | Helene Tursten      | 8.0    | 3442726247  |
| *Nachtblende*                        | Douglas Kennedy     | 7.0    | 3404142780  |

#### Top-10 Rekomendasi Buku untuk User 212002:

| No. | Judul Buku                                                                    | Penulis                                    | Predicted Rating | ISBN         |
|-----|-------------------------------------------------------------------------------|--------------------------------------------|------------------|--------------|
| 1   | *Halloween: Romantic Art and Customs Of Yesteryear Postcard Book*             | Diane C. Arkins                            | 0.90             | 1565548353   |
| 2   | *Uncle John's Bathroom Reader Plunges into the Universe*                      | Bathroom Readers Hysterical Society        | 0.90             | 1571458506   |
| 3   | *Your Pregnancy: Week by Week (Your Pregnancy Series)*                        | Glade B. Curtis M.D. OB/GYN                | 0.90             | 1555611435   |
| 4   | *Le Cycle d'Ender, tome 2 : La Voix des morts*                                | Scott Card Orson                           | 0.90             | 2290312924   |
| 5   | *Uncle John's Supremely Satisfying Bathroom Reader*                           | Bathroom Readers Institute                 | 0.89             | 1571456988   |
| 6   | *The Little Zen Companion*                                                    | David Schiller                             | 0.89             | 1563054671   |
| 7   | *Maus 1. Mein Vater kotzt Geschichte aus. Die Geschichte eines Überlebenden.* | Art Spiegelman                             | 0.89             | 3499224615   |
| 8   | *New Vegetarian: Bold and Beautiful Recipes for Every Occasion*               | Celia Brooks Brown                         | 0.89             | 1841721522   |
| 9   | *Death: The Time of Your Life (Death)*                                        | Neil Gaiman                                | 0.89             | 1563893339   |
| 10  | *Cunt: A Declaration of Independence (Live Girls)*                            | Inga Muscio                                | 0.89             | 1580050158   |

> **Catatan**: Rekomendasi diberikan untuk buku-buku yang belum pernah diberi rating oleh pengguna, dan disusun berdasarkan skor prediksi tertinggi.

---

### Kelebihan

- Dapat menangkap preferensi pengguna secara lebih kompleks melalui representasi embedding.
- Mampu memberikan rekomendasi yang personal meskipun tidak ada informasi eksplisit tentang buku.

### Kekurangan

- Kinerja dapat menurun jika data interaksi pengguna sedikit.
- Tidak efektif untuk *cold-start problem* (pengguna atau buku baru yang belum punya interaksi).

---

### Parameter Pelatihan Model

- **Embedding Size**: 50  
- **Optimizer**: Adam (`learning rate = 0.001`)  
- **Loss Function**: Mean Squared Error (MSE)  
- **Epochs**: 100  
- **Batch Size**: 16  
- **Metrik Evaluasi**: Root Mean Squared Error (RMSE)

#### Callbacks

- `EarlyStopping`: Menghentikan pelatihan jika tidak ada peningkatan performa pada data validasi.
- `ModelCheckpoint`: Menyimpan model terbaik.
- `ReduceLROnPlateau`: Mengurangi `learning rate` saat pelatihan stagnan.

---

## Evaluation

Evaluasi dilakukan untuk menilai performa kedua pendekatan sistem rekomendasi yang dikembangkan: **Content-Based Filtering** dan **Collaborative Filtering**. Setiap pendekatan menggunakan metrik evaluasi yang sesuai dengan karakteristiknya.

---

### 1. Evaluasi Content-Based Filtering

Untuk mengukur kualitas hasil rekomendasi berbasis konten, digunakan metrik **Precision@5**, yang menunjukkan proporsi item relevan dalam 5 rekomendasi teratas.

- **Precision@5** = **1.00**  
  → Artinya, semua buku dalam daftar Top-5 yang direkomendasikan merupakan buku relevan yang telah ditentukan sebelumnya.

Nilai ini menunjukkan performa yang sangat baik pada skenario pengujian, meskipun perlu diuji lebih lanjut dengan data uji yang lebih besar untuk validasi menyeluruh.

---

### 2. Evaluasi Collaborative Filtering

Model **Neural Collaborative Filtering** dievaluasi menggunakan dua metrik regresi: **Mean Squared Error (MSE)** dan **Root Mean Squared Error (RMSE)**.

#### a. Mean Squared Error (MSE)

MSE mengukur rata-rata dari kuadrat selisih antara rating aktual dan prediksi.

$$
\mathrm{MSE} = \frac{1}{n} \sum_{i=1}^{n} \left( y_i - \hat{y}_i \right)^2
$$

- **Nilai MSE pada data validasi**: **0.0458**

#### b. Root Mean Squared Error (RMSE)

RMSE memberikan penalti lebih besar terhadap kesalahan prediksi yang besar.

$$
\mathrm{RMSE} = \sqrt{ \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 }
$$

- **Nilai RMSE pada data validasi**: **0.2090**

Selama pelatihan, model menunjukkan stabilitas dengan nilai `val_loss` (MSE) konstan di **0.0459** dan `val_root_mean_squared_error` di **0.2091** pada epoch-akhir. Model terbaik disimpan sebagai `best_recommender_model.h5` menggunakan `ModelCheckpoint`, dengan `EarlyStopping` aktif menghentikan pelatihan saat tidak ada perbaikan lebih lanjut.

---

### Kesimpulan Evaluasi

| Pendekatan              | Metrik       | Nilai   |
|-------------------------|--------------|---------|
| Content-Based Filtering | Precision@5  | 1.00    |
| Collaborative Filtering | MSE          | 0.0459  |
| Collaborative Filtering | RMSE         | 0.2091  |

Evaluasi menunjukkan bahwa sistem rekomendasi memiliki performa yang memadai untuk konteks data yang digunakan, dengan Content-Based memberikan rekomendasi yang sangat relevan, dan Collaborative Filtering cukup akurat dalam memprediksi rating pengguna.


## Kesimpulan

Dari dua pendekatan yang dikembangkan:

- **Content-Based Filtering** cocok digunakan sebagai rekomendasi awal, khususnya saat data pengguna terbatas.
- **Collaborative Filtering** unggul dalam memberikan rekomendasi yang bersifat personal berdasarkan histori interaksi.

> **Rekomendasi**: Gabungan kedua pendekatan ini dapat membentuk sistem rekomendasi **hybrid**, yang mampu mengatasi kelemahan masing-masing dan memberikan hasil yang lebih optimal.
