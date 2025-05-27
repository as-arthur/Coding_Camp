# CNN Image Classification - Weather Classification

Proyek ini membangun model klasifikasi gambar cuaca ke dalam 11 kategori menggunakan arsitektur **CNN + MobileNetV2** dalam framework **TensorFlow/Keras**.

---

# Struktur Folder

submissions/
│ 
├── sample_data/ 
│	├── glaze.jpg
│	├── lightning.jpg
│	└── rainbow.jpg
├─── tflite
│	├── model.tflite
│	└──label.txt
├── Submission_Akhir_Klasifikasi_Gambar_Fathur.ipynb
├── requirements.txt 
└── README.md 

# Setup 

pip install -r requirements.txt


# Arsitektur Model

Link Dataset : https://www.kaggle.com/datasets/jehanbhathena/weather-dataset

Model dibangun menggunakan `Sequential` dengan backbone **MobileNetV2**

# Hasil Evaluasi

- **Val Accuracy**: 85%
- **Test Accuracy**: 85%


# Dataset

Dataset berisi 11 kelas cuaca (dew, fogsmog, frost, dll) yang sudah dipisah ke dalam folder:

- `train/`
- `val/`
- `test/`



#Ekspor Model

Model telah diekspor ke format berikut:

- `.keras`
- `.tflite`

Model ini kompatibel untuk digunakan pada aplikasi Android menggunakan **TensorFlow Lite**.


# Label

File `label.txt` berisi urutan label sesuai dengan urutan pada saat training, contoh:

- `dew`
- `fogsmog`
- `frost`
...




