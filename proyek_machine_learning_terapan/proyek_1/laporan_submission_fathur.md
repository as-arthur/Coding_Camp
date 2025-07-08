# Laporan Proyek Machine Learning - Muhammad Fathurrahman

## Domain Proyek

Penyakit jantung koroner merupakan penyebab kematian utama di Indonesia, mengalahkan stroke dan diabetes. Menurut data Riskesdas 2018 dari Kementerian Kesehatan RI, prevalensi penyakit jantung koroner di Indonesia mencapai 1,5% dari total populasi. Gaya hidup tidak sehat, seperti pola makan tinggi lemak, kurang aktivitas fisik, merokok, dan stres, menjadi penyumbang utama risiko ini.

Sayangnya, akses terhadap fasilitas diagnostik seperti elektrokardiogram (EKG), echo jantung, atau treadmill test masih terbatas di daerah terpencil. Oleh karena itu, pengembangan sistem prediksi penyakit jantung berbasis data dapat menjadi solusi alternatif dalam skrining awal risiko penyakit ini.

Machine learning menawarkan kemampuan untuk membangun model prediksi risiko penyakit jantung dengan akurasi tinggi berdasarkan data klinis yang sederhana, seperti tekanan darah, kadar kolesterol, dan usia. Model ini dapat membantu petugas kesehatan di Puskesmas, klinik, atau layanan mobile screening untuk melakukan deteksi dini terhadap pasien berisiko tinggi.

Referensi:
- Badan Litbangkes Kemenkes RI. "Hasil Utama Riskesdas 2018."
- World Health Organization. "Cardiovascular diseases (CVDs)", 2023. [Online]. Tersedia: https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases-(cvds)
- Satoto, H. H. (2014). Patofisiologi Penyakit Jantung Koroner. JAI (Jurnal Anestesiologi Indonesia), 6(3), 209-224.
- Karyatin, K. (2019). Faktor-Faktor Yang Berhubungan Dengan Kejadian Penyakit Jantung Koroner. Jurnal Ilmiah Kesehatan, 11(1), 37-43.
- Santosa, W. N., & Baharuddin, B. (2020). Penyakit jantung koroner dan antioksidan. KELUWIH: Jurnal Kesehatan Dan Kedokteran, 1(2), 95-100.

## Business Understanding

### Problem Statements

- Bagaimana memprediksi risiko penyakit jantung seseorang berdasarkan data medis yang mudah diakses di internet?
- Fitur-fitur medis apa yang paling memengaruhi risiko penyakit jantung?
- Bagaimana cara mengoptimalkan sistem prediksi untuk meningkatkan akurasi?

### Goals

- Membangun model klasifikasi untuk memprediksi penyakit jantung menggunakan dataset medis sederhana.
- Mengidentifikasi fitur yang paling signifikan dalam memprediksi penyakit jantung (misalnya: kolesterol, tekanan darah, detak jantung).
- Menerapkan Data prepocessing yang tepat terhadap data penyakit jantung.


### Solution statements
- Membangun dua model: Xgboost dan Random Forest Classifier.
- Melakukan hyperparameter tuning pada model Random Forest menggunakan RandomSearch.
- Mengevaluasi model dengan metrik: akurasi, precision, recall, dan F1-score.

## Data Understanding

Dataset yang digunakan adalah heart.csv yang memiliki 14 kolom dan 1025 baris lalu, heart_statlog_cleveland_hungary_final.csv yang memiliki 12 kolom dan 1190 baris. Data ini diadaptasi dari dataset publik dari Kaggle. setelah melakukan drop terhadap data duplikat, heart.csv hanya memiliki 302 baris dan 14 kolom dan untuk heart_statlog_cleveland_hungary_final.csv tersisa 12  kolom dan 918 baris. Setelah digabungkan dan dibersihkan duplikat maka terdapat 1220 baris dan 11 kolom untuk dipakai dalam proyek ini. Data ini juga terdapat beberapa oulier di beberapa fitur seperti 'oldpeak', 'chol' dan 'tresbps'. Dan setelah data dibersihkan ternyata hanya terdapat 989 baris dan 11 kolom data.

link 1: [text](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset)
link 2: [text](https://www.kaggle.com/datasets/mexwell/heart-disease-dataset?select=heart_statlog_cleveland_hungary_final.csv)

### Variabel-variabel pada Restaurant UCI dataset adalah sebagai berikut:
- age: usia pasien

- sex: jenis kelamin (1 = laki-laki, 0 = perempuan)

- cp: jenis nyeri dada (0–3)

- trestbps: tekanan darah saat istirahat (mm Hg)

- chol: kadar kolesterol (mg/dl)

- fbs: gula darah puasa > 120 mg/dl (1 = ya, 0 = tidak)

- restecg: hasil EKG saat istirahat

- thalach: detak jantung maksimum

- exang: nyeri dada akibat latihan (1 = ya)

- oldpeak: depresi ST (numerik)

- slope: kemiringan segmen ST (0–2)

- ca: jumlah pembuluh darah besar yang diwarnai (0–4)

- thal: hasil tes thalassemia (1 = normal, 2 = cacat tetap, 3 = cacat reversibel)

- target: diagnosis akhir (0 = tidak sakit, 1 = ada penyakit jantung)


## Data Preparation
Beberapa tahapan data preparation yang dilakukan adalah sebagai berikut:

1. **Penggabungan Dataset:**

- Penggabungan dataset heart.csv dan heart_statlog_cleveland_hungary_final.csv dilakukan menggunakan pd.concat() untuk memperoleh jumlah data yang lebih banyak dan meningkatkan generalisasi model.

- Pemilihan hanya kolom-kolom yang sama (menggunakan common_columns) bertujuan menjaga konsistensi fitur yang digunakan dalam model.

- Penggantian nama kolom (.rename()) dilakukan agar kedua dataset memiliki struktur kolom yang seragam sehingga dapat digabung tanpa kesalahan struktur.

2. **Pembersihan Data:**   

- Penghapusan baris duplikat menggunakan .drop_duplicates() bertujuan menghindari bias dalam pelatihan model yang dapat terjadi jika ada data identik berulang.

- Pemeriksaan nilai null penting untuk memastikan tidak ada informasi yang hilang yang dapat mempengaruhi performa model atau menyebabkan error saat pelatihan.- 

- Pemeriksaan dan pembersihan outliers pada dataset agar model tidak terpengaruh oleh outlier.

3. **Pemilihan Fitur:**

- Dipilih 11 fitur numerik dan kategorikal yang relevan untuk klasifikasi penyakit jantung. Hal ini dilakukan karena dataset ke-2 hanya memikiki 11 kolom. jadi, supaya kolom sama maka dataset satu di buang 2 kolom.  

4. **Split Data:**
Pada tahap ini, saya melakukan pembagian dataset menjadi tiga bagian utama yaitu data latih (training), data validasi (validation), dan data uji (testing). Proses ini dilakukan untuk mempersiapkan data sebelum digunakan dalam pelatihan dan evaluasi model machine learning.

Hasil split data menunjukkan bahwa:

- Data latih (X_train) berjumlah 791 sampel dengan 11 fitur, digunakan untuk melatih model agar dapat mempelajari pola dari data.

- Data validasi (X_val) berjumlah 132 sampel, digunakan untuk menguji performa model selama pelatihan dan membantu melakukan tuning parameter agar model tidak overfitting.

- Data uji (X_test) berjumlah 66 sampel, berfungsi sebagai data baru yang tidak terlihat oleh model selama pelatihan, untuk mengevaluasi performa akhir model secara objektif.

- Target variabel (y) juga dibagi sesuai proporsi tersebut.

Tahapan pembagian dataset ini sangat penting untuk memastikan model yang dibangun dapat generalisasi dengan baik terhadap data yang belum pernah dilihat sebelumnya. Dengan adanya data validasi dan testing yang terpisah, proses pelatihan model menjadi lebih terkontrol dan hasil evaluasi model dapat dipercaya sebagai representasi performa nyata saat diaplikasikan ke data sesungguhnya.

5. **Penanganan Ketidakseimbangan Kelas:**

Ketidakseimbangan kelas pada target dapat menyebabkan model bias terhadap kelas mayoritas. Oleh karena itu, digunakan teknik oversampling SMOTE (Synthetic Minority Over-sampling Technique) untuk menyeimbangkan jumlah sampel antar kelas. SMOTE hanya diterapkan pada data latih agar tidak terjadi kebocoran informasi ke data validasi atau test.

6. **Feature Scaling:**

Normalisasi dengan StandardScaler() dilakukan agar semua fitur numerik berada dalam skala yang seragam, sehingga model seperti XGBoost dan Random Forest dapat bekerja optimal.Scaling dilakukan secara terpisah untuk train, val, dan test untuk menghindari data leakage, yaitu penggunaan informasi dari data uji dalam proses pelatihan.


## Modeling

### Algoritma yang Digunakan

1. **Random Forest Classifier**

- Random Forest merupakan algoritma ensemble berbasis decision tree yang bekerja dengan membangun banyak pohon keputusan secara paralel dan menggabungkan hasil prediksi masing-masing pohon menggunakan metode voting (klasifikasi) atau rata-rata (regresi).

- Setiap pohon dalam Random Forest dilatih menggunakan subset acak dari data (bagging) dan subset acak dari fitur, sehingga model lebih tahan terhadap overfitting dibanding decision tree tunggal.

2. **XGBoost Classifier**

- XGBoost adalah algoritma gradient boosting yang membangun model secara iteratif. Setiap pohon baru dibuat untuk meminimalkan kesalahan dari model sebelumnya dengan menyesuaikan bobot kesalahan.

- Keunggulan XGBoost terletak pada efisiensi, kemampuan menangani data tak seimbang, dan kontrol regulasi yang kuat untuk menghindari overfitting.

### Parameter Model
Setelah dilakukan hyperparameter tuning menggunakan RandomizedSearchCV, berikut parameter akhir yang digunakan:

#### Random Forest (tuned):

   - n_estimators = 300

   - min_samples_split = 2

   - min_samples_leaf = 1

   - max_depth = 20

#### XGBoost (tuned):

   - learning_rate = 0.01

   - max_depth = 15

   - subsample = 0.9

   - colsample_bytree = 0.9

   - n_estimators = 100

Model XGBoost awalnya diuji menggunakan parameter default sebagai baseline. Namun, model akhir yang digunakan adalah hasil tuning dengan performa terbaik pada data validasi.

### Model Terbaik
Model XGBoost Classifier dipilih sebagai model terbaik berdasarkan performa evaluasi pada data test, yang menunjukkan nilai akurasi, precision, recall, dan F1-score tertinggi dibanding model lainnya.

## Evaluation

### Metrik Evaluasi

Evaluasi performa model dilakukan dengan menggunakan empat metrik utama dalam klasifikasi biner, yaitu:

1. **Accuracy (Akurasi):**  
   Mengukur proporsi prediksi yang benar terhadap keseluruhan data.  
   **Rumus:**  
   $$
   \text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}
   $$

2. **Precision (Presisi):**  
   Mengukur ketepatan model dalam memprediksi kelas positif.  
   **Rumus:**  
   $$
   \text{Precision} = \frac{TP}{TP + FP}
   $$

3. **Recall (Sensitivitas):**  
   Mengukur sejauh mana model berhasil mendeteksi semua data positif.  
   **Rumus:**  
   $$
   \text{Recall} = \frac{TP}{TP + FN}
   $$

4. **F1-score:**  
   Rata-rata harmonik antara precision dan recall.  
   Cocok digunakan ketika distribusi kelas tidak seimbang.  
   **Rumus:**  
   $$
   \text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
   $$

### Data Evaluasi

Evaluasi dilakukan menggunakan **data test**, yaitu sebagian dari keseluruhan dataset yang **telah dipisahkan sejak awal dan tidak digunakan saat pelatihan maupun tuning model**. Langkah ini bertujuan untuk memastikan hasil evaluasi mencerminkan performa sebenarnya ketika model digunakan pada data baru (*unseen data*).

Sebaliknya, **data validasi** digunakan selama proses pelatihan untuk menyesuaikan parameter dan mencegah overfitting, bukan untuk evaluasi akhir. 

### Hasil Evaluasi pada Data Test

- **Random Forest (tuned):**
  - **Accuracy:** 83,3%  
  - **Precision:** 84%  
  - **Recall:** 83%  
  - **F1-Score:** 83%

**Classification Report:**

| Kelas              | Precision | Recall | F1-score | Support |
|--------------------|-----------|--------|----------|---------|
| Tidak Sakit Jantung| 0.87      | 0.79   | 0.83     | 33      |
| Sakit Jantung      | 0.81      | 0,88   | 0.84     | 33      |

- **XGBoost (tuned):**
  - **Accuracy:** 84,8% 
  - **Precision:** 85%  
  - **Recall:** 85%  
  - **F1-Score:** 85%

**Classification Report:**

| Kelas              | Precision | Recall | F1-score | Support |
|--------------------|-----------|--------|----------|---------|
| Tidak Sakit Jantung| 0.87      | 0.82   | 0.84     | 33      |
| Sakit Jantung      | 0.83      | 0.84   | 0.85     | 33      |

### Kesimpulan

Model XGBoost berhasil mencapai akurasi 84,8% pada data uji. Precision untuk kelas Tidak Sakit Jantung adalah 87%, dan untuk Sakit Jantung sebesar 83%, sementara recall masing-masing 82% dan 88%. F1-score untuk kedua kelas adalah 0,84–0,85, menunjukkan performa yang seimbang dan andal. Confusion matrix mencatat 6 kesalahan pada kelas negatif, dan 4 kesalahan pada kelas positif, dari total 66 sampel.

Dalam proyek ini, dua model dikembangkan: XGBoost dan Random Forest, dengan tuning khusus dilakukan pada keduanya. Meskipun keduanya menunjukkan performa baik, XGBoost dipilih sebagai model akhir karena memberikan akurasi sedikit lebih tinggi serta deteksi penyakit jantung yang lebih stabil, dengan kesalahan prediksi yang relatif rendah.

Visualisasi feature importance dari model XGBoost (gambar di bawah) menunjukkan bahwa slope (kemiringan segmen ST) merupakan faktor paling dominan, diikuti oleh cp (tipe nyeri dada) dan exang (angina akibat olahraga):

**---Ini adalah bagian akhir laporan---**