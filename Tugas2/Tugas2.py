import numpy as np


# Fungsi untuk mencari invers modular dari matriks
def modInverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1


# Fungsi untuk mengubah teks menjadi angka (A=0, B=1, ...)
def text_to_numbers(text):

    numbers = []
    for char in text.upper():
        if "A" <= char <= "Z":
            numbers.append(ord(char) - ord("A"))
    return numbers


# Fungsi untuk mengubah angka menjadi teks
def numbers_to_text(numbers):
    text = ""
    for num in numbers:
        text += chr(int(num) + ord("A"))
    return text


# Fungsi untuk enkripsi Hill Cipher
def encrypt(plaintext, key_matrix):
    print("\n" + "=" * 50)
    print("--- Proses Enkripsi ---".center(50))
    print("=" * 50)

    plaintext = plaintext.replace(" ", "").upper()
    n = len(key_matrix)

    # Menyesuaikan panjang plaintext agar habis dibagi n
    if len(plaintext) % n != 0:
        plaintext += "X" * (n - (len(plaintext) % n))

    p_numbers = text_to_numbers(plaintext)

    ciphertext_numbers = []

    print(f"1. Plaintext: {plaintext}")
    print(f"   Konversi ke angka: {p_numbers}")

    print(f"\n2. Matriks kunci:\n{key_matrix}")

    print("\n3. Membagi plaintext menjadi blok dan melakukan perkalian matriks:")
    for i in range(0, len(p_numbers), n):
        block_p = np.array(p_numbers[i : i + n]).reshape(n, 1)

        print(
            f"\n   - Blok Plaintext: {numbers_to_text(p_numbers[i:i+n])} ({p_numbers[i:i+n]})"
        )
        print(f"     Matriks Plaintext:\n{block_p.flatten()}")

        # Perkalian matriks
        block_c = np.dot(key_matrix, block_p) % 26

        print(f"     Hasil perkalian matriks:\n{block_c.flatten()}")

        ciphertext_numbers.extend(block_c.flatten())

    ciphertext = numbers_to_text(ciphertext_numbers)
    print("\n" + "-" * 50)
    print(f"Hasil Enkripsi: {ciphertext}".center(50))
    print("-" * 50 + "\n")

    return ciphertext


# Fungsi untuk dekripsi Hill Cipher
def decrypt(ciphertext, key_matrix):
    print("\n" + "=" * 50)
    print("--- Proses Dekripsi ---".center(50))
    print("=" * 50)

    n = len(key_matrix)
    c_numbers = text_to_numbers(ciphertext)

    print(f"1. Ciphertext: {ciphertext}")
    print(f"   Konversi ke angka: {c_numbers}")

    print(f"\n2. Matriks kunci:\n{key_matrix}")

    # Menghitung determinan
    det = int(np.round(np.linalg.det(key_matrix)))
    print(
        f"\n3. Menghitung determinan matriks kunci: det(K) = {det} mod 26 = {det % 26}"
    )

    # Menghitung invers modular dari determinan
    det_inv = modInverse(det, 26)
    if det_inv == -1:
        print(
            "   Determinan tidak memiliki invers modular. Dekripsi tidak dapat dilakukan."
        )
        return ""
    print(f"   Invers modular dari determinan: ({det})^-1 mod 26 = {det_inv}")

    # Menghitung matriks kofaktor/adjoin
    key_adj = np.round(np.linalg.det(key_matrix) * np.linalg.inv(key_matrix))
    key_adj = key_adj.astype(int)

    # Mengalikan dengan invers modular
    inv_key_matrix = (key_adj * det_inv) % 26

    print(f"\n4. Menghitung invers matriks kunci K^-1:\n{inv_key_matrix}")

    plaintext_numbers = []

    print("\n5. Membagi ciphertext menjadi blok dan melakukan perkalian matriks:")
    for i in range(0, len(c_numbers), n):
        block_c = np.array(c_numbers[i : i + n]).reshape(n, 1)

        print(
            f"\n   - Blok Ciphertext: {numbers_to_text(c_numbers[i:i+n])} ({c_numbers[i:i+n]})"
        )
        print(f"     Matriks Ciphertext:\n{block_c.flatten()}")

        block_p = np.dot(inv_key_matrix, block_c) % 26

        print(f"     Hasil perkalian matriks:\n{block_p.flatten()}")

        plaintext_numbers.extend(block_p.flatten())

    plaintext = numbers_to_text(plaintext_numbers)
    print("\n" + "-" * 50)
    print(f"Hasil Dekripsi: {plaintext}".center(50))
    print("-" * 50 + "\n")

    return plaintext


# Fungsi untuk mencari kunci
def find_key(plaintext, ciphertext):
    print("\n" + "=" * 50)
    print("--- Proses Mencari Kunci ---".center(50))
    print("=" * 50)

    plaintext = plaintext.replace(" ", "").upper()
    ciphertext = ciphertext.replace(" ", "").upper()

    # Asumsi ukuran matriks 2x2
    n = 2

    if len(plaintext) != len(ciphertext) or len(plaintext) < n * n:
        print(
            "Plaintext dan ciphertext harus memiliki panjang yang sama dan cukup untuk membentuk matriks kunci."
        )
        return None

    p_numbers = text_to_numbers(plaintext)
    c_numbers = text_to_numbers(ciphertext)

    # Menggunakan 2 blok pertama untuk mencari kunci
    p_matrix = np.array([p_numbers[0:n], p_numbers[n : n * 2]]).T
    c_matrix = np.array([c_numbers[0:n], c_numbers[n : n * 2]]).T

    print(
        f"1. Plaintext dan Ciphertext yang digunakan:\n   Plaintext: {plaintext[0:n*2]} ({p_numbers[0:n*2]})\n   Ciphertext: {ciphertext[0:n*2]} ({c_numbers[0:n*2]})"
    )

    print(
        f"\n2. Membuat matriks P dan C:\n   Matriks P:\n{p_matrix}\n   Matriks C:\n{c_matrix}"
    )

    # Mencari invers matriks P
    det_p = int(np.round(np.linalg.det(p_matrix)))
    print(
        f"\n3. Menghitung determinan matriks P: det(P) = {det_p} mod 26 = {det_p % 26}"
    )

    det_p_inv = modInverse(det_p, 26)
    if det_p_inv == -1:
        print(
            "   Determinan matriks P tidak memiliki invers modular. Tidak dapat mencari kunci."
        )
        return None
    print(f"   Invers modular dari det(P): ({det_p})^-1 mod 26 = {det_p_inv}")

    p_adj = np.round(np.linalg.det(p_matrix) * np.linalg.inv(p_matrix))
    p_adj = p_adj.astype(int)

    inv_p_matrix = (p_adj * det_p_inv) % 26

    print(f"\n4. Menghitung invers matriks P^-1:\n{inv_p_matrix}")

    # Mencari kunci K = C * P^-1
    key_matrix = np.dot(c_matrix, inv_p_matrix) % 26

    print("\n5. Menghitung matriks kunci K = C * P^-1:")
    print(f"   Matriks kunci ditemukan:\n{key_matrix}")

    print("\n" + "-" * 50)
    print("Kunci berhasil ditemukan!".center(50))
    print("-" * 50 + "\n")

    return key_matrix


# Menu utama
if __name__ == "__main__":
    while True:
        print("=" * 50)
        print("PROGRAM HILL CIPHER".center(50))
        print("=" * 50)
        print("Pilih opsi:")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Mencari Kunci")
        print("4. Keluar")

        choice = input("Masukkan pilihan Anda (1/2/3/4): ")

        if choice == "1":
            plaintext = input("Masukkan plaintext: ")
            print("Masukkan matriks kunci (misal: 3 2;2 7):")
            try:
                rows = []
                for _ in range(2):
                    row = list(map(int, input().split()))
                    rows.append(row)
                key_matrix = np.array(rows)
                encrypt(plaintext, key_matrix)
            except ValueError:
                print(
                    "Input matriks kunci tidak valid. Harap masukkan angka yang benar."
                )
            except np.linalg.LinAlgError:
                print("Matriks kunci tidak valid. Harap periksa kembali ukurannya.")

        elif choice == "2":
            ciphertext = input("Masukkan ciphertext: ")
            print("Masukkan matriks kunci (misal: 3 2;2 7):")
            try:
                rows = []
                for _ in range(2):
                    row = list(map(int, input().split()))
                    rows.append(row)
                key_matrix = np.array(rows)
                decrypt(ciphertext, key_matrix)
            except ValueError:
                print(
                    "Input matriks kunci tidak valid. Harap masukkan angka yang benar."
                )
            except np.linalg.LinAlgError:
                print("Matriks kunci tidak valid. Harap periksa kembali ukurannya.")

        elif choice == "3":
            plaintext = input("Masukkan plaintext (min. 4 huruf): ")
            ciphertext = input("Masukkan ciphertext (min. 4 huruf): ")
            found_key = find_key(plaintext, ciphertext)
            if found_key is not None:
                print("Matriks Kunci yang ditemukan:")
                print(found_key)

        elif choice == "4":
            print("Terima kasih telah menggunakan program Hill Cipher!")
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
