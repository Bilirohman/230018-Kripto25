# 🔐 KryptonPixel — Hybrid Steganography System

**Tugas 5 Kriptografi**  
**Dibuat oleh:** Gunawan Sabili Rohman \
**NPM:** 140810230018

## ⚙️ Konsep Dasar Metode KryptonPixel

KryptonPixel bekerja berdasarkan tiga pilar utama:

1. **Enkripsi XOR dengan Kunci Rahasia**  
   Sebelum pesan disisipkan, setiap karakter pesan dienkripsi menggunakan operasi XOR dengan kunci yang diberikan.  
   ➤ Hasilnya, pesan tidak dapat dibaca meski berhasil diekstrak tanpa kunci.

2. **Pola Acak Berbasis Kunci (PRNG Seed)**  
   Urutan piksel tempat bit pesan disisipkan **tidak berurutan**, melainkan ditentukan oleh **Pseudo-Random Number Generator (PRNG)** dengan seed yang berasal dari hash kunci rahasia.

3. **Delimiter Unik (`--END--`)**  
   Ditambahkan di akhir pesan untuk memberi tahu program kapan proses pembacaan pesan harus berhenti saat decoding.


## Cara Kerja Program

### 🔸 Proses Encoding (Menyembunyikan Pesan)

1. **Input:**  
   - Gambar sampul (cover image)  
   - Pesan rahasia  
   - Nama file output (stego-image)  
   - Kunci rahasia  

2. **Langkah-langkah:**  
   - Memeriksa kapasitas gambar.  
   - Menambahkan delimiter `--END--`.  
   - Mengenkripsi pesan menggunakan XOR.  
   - Mengubah pesan menjadi bit biner.  
   - Menentukan urutan acak piksel berdasarkan hash kunci.  
   - Menyisipkan bit pesan ke LSB pada tiap channel (R, G, B).  
   - Menyimpan gambar hasil ke dalam format **PNG (lossless)**.

### 🔸 Proses Decoding (Mengekstrak Pesan)

1. **Input:**  
   - Stego-image  
   - Kunci rahasia  

2. **Langkah-langkah:**  
   - Menentukan kembali urutan piksel berdasarkan hash kunci.  
   - Mengekstrak bit dari LSB pada piksel target.  
   - Menggabungkan bit menjadi byte, kemudian mendekripsi dengan XOR.  
   - Menghentikan proses setelah menemukan delimiter `--END--`.  
   - Menampilkan pesan rahasia di terminal.

---

## 🖥️ Instruksi Menjalankan Program

### 1️⃣ Prasyarat Sistem

Pastikan sistem Anda memiliki:

- **Python 3.x**
- **Library Pillow**

Untuk memasang Pillow:
```bash
pip install Pillow
```

### 2️⃣ Persiapan File

**Simpan file** program KryptonPixel.py di satu folder. \
**Siapkan gambar** cover (misal cover.png).\
Pastikan **format gambar PNG** (lossless) agar bit LSB tidak rusak.

### 3️⃣ Menjalankan Program
#### **Encoding (Menyembunyikan Pesan)**
```bash
python KryptonPixel.py encode -i [nama_gambar_input] -m "[pesan_rahasia]" -o [nama_gambar_output] -k [kunci_rahasia]
```

Contoh:
```bash
python KryptonPixel.py encode -i cover.png -m "Orang yang cuman mental bilang bubarin DPR, itu adalah orang tolol sedunia ~ masroni 2k25" -o stego_result.png -k assetindonesia
```

Output: file bernama stego_result.png akan berisi pesan tersembunyi.

#### **Decoding (Mengekstrak Pesan)**
```bash
python KryptonPixel.py decode -i [nama_gambar_stego] -k [kunci_rahasia]
```

Contoh:
```bash
python KryptonPixel.py decode -i stego_result.png -k assetindonesia
```

Jika kunci benar, pesan rahasia akan muncul di terminal.

### 📂 Struktur folder
```bash
Tugas5/
├── KryptonPixel.py        # File utama program
├── cover.png              # Contoh cover image
├── stego_result.png       # Contoh hasil encoding
└── README.md              # Dokumentasi proyek
```

### 🧾 Contoh Hasil & Bukti Implementasi
Gambar 1 – Proses Encoding
![Proses encoding](https://media.discordapp.net/attachments/870493631360942092/1428277428773453905/image.png?ex=68f1ea83&is=68f09903&hm=508be1752745aa177f34d648887bc1fc9850c1cfac1368abc3d9ccece1075a2e&=&format=webp&quality=lossless)

Gambar 2 – Proses Decoding
![Proses Decoding](https://media.discordapp.net/attachments/870493631360942092/1428277508029153352/image.png?ex=68f1ea96&is=68f09916&hm=fced679d7cc6f137305b20f3f6022893b8c2f3d8327e00652f110bf712c6513c&=&format=webp&quality=lossless)

**Sekian terimagaji**