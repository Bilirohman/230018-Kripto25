# 🔐 Program Hill Cipher

Program ini adalah implementasi algoritma kriptografi **Hill Cipher** menggunakan **Python**.  
Dengan program ini, Anda dapat melakukan tiga operasi utama:

1. **Enkripsi** – Mengubah _plaintext_ menjadi _ciphertext_ menggunakan matriks kunci.
2. **Dekripsi** – Mengembalikan _ciphertext_ menjadi _plaintext_ dengan menggunakan invers dari matriks kunci.
3. **Mencari Kunci** – Menemukan matriks kunci jika diberikan pasangan _plaintext_ dan _ciphertext_.

---

### 1. Enkripsi

- Masukkan _plaintext_ dan matriks kunci.
- **Alur proses:**
  1. Konversi huruf ke angka (`A=0, B=1, ..., Z=25`).
  2. Jika panjang _plaintext_ ganjil, tambahkan huruf `X` di akhir.
  3. Bagi teks ke dalam blok 2×1.
  4. Setiap blok dikalikan dengan matriks kunci 2×2.
  5. Hasilnya dimodulo 26 lalu dikonversi kembali ke huruf → menghasilkan _ciphertext_.

### 2. Dekripsi

- Masukkan _ciphertext_ dan matriks kunci.
- **Alur proses:**
  1. Hitung invers matriks kunci.
  2. Kalikan setiap blok _ciphertext_ dengan invers matriks kunci.
  3. Lakukan operasi modulo 26.
  4. Konversi hasil ke huruf → diperoleh _plaintext_.

### 3. Mencari Kunci

- Masukkan pasangan _plaintext_ dan _ciphertext_.
- **Alur proses:**

  1. Ambil dua blok pertama dari _plaintext_ dan _ciphertext_.
  2. Bentuk matriks **P** (plaintext) dan **C** (ciphertext).
  3. Hitung invers dari matriks **P**.
  4. Gunakan rumus:

     \[
     K = C \times P^{-1} \pmod{26}
     \]

  5. Hasilnya adalah matriks kunci **K**.

---

## Catatan Penting

- Program menggunakan **NumPy** untuk operasi matriks.  
  Pastikan sudah menginstal:
  ```bash
  pip install numpy
  ```

## HASIL RUNNING PROGRAM

![RUNNING](https://media.discordapp.net/attachments/1376564660773326941/1414810857975582800/image.png?ex=68c0ecca&is=68bf9b4a&hm=87e7dd31a10a30697dc88f5e840bc5c78995e9454f08e69d2538b0b28afa7734&=&format=webp&quality=lossless&width=538&height=989)
![RUNNING](https://media.discordapp.net/attachments/1376564660773326941/1414811054541770763/image.png?ex=68c0ecf9&is=68bf9b79&hm=0ecd5028c481563b2c9d4550a10f9bdfd2a3b9ad1e944412c23c0eb970d88a87&=&format=webp&quality=lossless&width=548&height=989)
