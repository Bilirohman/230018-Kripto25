import argparse
import hashlib
import random
from PIL import Image


def xor_encrypt_decrypt(data, key):
    key_bytes = key.encode("utf-8")
    data_bytes = data.encode("utf-8") if isinstance(data, str) else data

    encrypted_data = bytearray()
    for i in range(len(data_bytes)):
        encrypted_data.append(data_bytes[i] ^ key_bytes[i % len(key_bytes)])

    return encrypted_data


def to_binary(data):
    if isinstance(data, str):
        return "".join(format(ord(i), "08b") for i in data)
    elif isinstance(data, bytes) or isinstance(data, bytearray):
        return "".join(format(i, "08b") for i in data)
    else:
        raise TypeError("Tipe data tidak didukung.")


def generate_pixel_map(width, height, seed):
    random.seed(seed)
    pixel_indices = list(range(width * height))
    random.shuffle(pixel_indices)

    pixel_map = []
    for index in pixel_indices:
        x = index % width
        y = index // width
        pixel_map.append((x, y))
    return pixel_map


def hide_data(image_path, secret_message, output_path, key):
    print("[INFO] Memulai proses encoding...")
    try:
        img = Image.open(image_path, "r")
    except FileNotFoundError:
        print(f"[ERROR] File gambar tidak ditemukan di: {image_path}")
        return

    width, height = img.size

    message_with_delimiter = secret_message + "--END--"
    encrypted_message = xor_encrypt_decrypt(message_with_delimiter, key)
    binary_secret_message = to_binary(encrypted_message)
    data_len = len(binary_secret_message)

    max_capacity = width * height * 3
    if data_len > max_capacity:
        print("[ERROR] Pesan terlalu besar untuk disembunyikan di gambar ini.")
        print(
            f"Kapasitas Maksimum: {max_capacity} bits. Ukuran Pesan: {data_len} bits."
        )
        return

    seed = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    pixel_map = generate_pixel_map(width, height, seed)

    data_index = 0
    img_data = img.getdata()
    new_img_data = []

    pixels_used = set()

    for pixel in img_data:
        if data_index < data_len:
            try:
                while True:
                    x, y = pixel_map.pop(0)
                    if (x, y) not in pixels_used:
                        pixels_used.add((x, y))
                        break

                target_pixel = list(img.getpixel((x, y)))

                for i in range(3):
                    if data_index < data_len:
                        target_pixel[i] = target_pixel[i] & ~1 | int(
                            binary_secret_message[data_index]
                        )
                        data_index += 1

                img.putpixel((x, y), tuple(target_pixel))
            except IndexError:
                print("[ERROR] Kehabisan piksel unik.")
                break

    img.save(output_path, "PNG")
    print(f"[SUCCESS] Pesan berhasil disembunyikan di: {output_path}")


def find_data(image_path, key):
    print("[INFO] Memulai proses decoding...")
    try:
        img = Image.open(image_path, "r")
    except FileNotFoundError:
        print(f"[ERROR] File gambar tidak ditemukan di: {image_path}")
        return

    width, height = img.size

    seed = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    pixel_map = generate_pixel_map(width, height, seed)

    binary_data = ""
    byte_buffer = bytearray()

    for x, y in pixel_map:
        pixel = img.getpixel((x, y))
        for i in range(3):
            binary_data += str(pixel[i] & 1)

            if len(binary_data) == 8:
                byte_data = int(binary_data, 2)
                byte_buffer.append(byte_data)

                decrypted_so_far = xor_encrypt_decrypt(byte_buffer, key).decode(
                    "utf-8", errors="ignore"
                )

                if decrypted_so_far.endswith("--END--"):
                    final_message = decrypted_so_far[:-7]
                    print(f"[SUCCESS] Pesan ditemukan: {final_message}")
                    return final_message

                binary_data = ""

    print("[ERROR] Tidak ada pesan rahasia yang ditemukan atau kunci salah.")
    return None


def main():
    """Fungsi utama untuk menjalankan program dari terminal."""
    parser = argparse.ArgumentParser(
        description="KryptonPixel - Alat Steganografi Hibrida"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    encode_parser = subparsers.add_parser(
        "encode", help="Sembunyikan pesan dalam gambar"
    )
    encode_parser.add_argument(
        "-i", "--image", required=True, help="Path ke gambar sampul (cover image)"
    )
    encode_parser.add_argument(
        "-m", "--message", required=True, help="Pesan rahasia yang akan disembunyikan"
    )
    encode_parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Path untuk menyimpan gambar hasil (stego-image)",
    )
    encode_parser.add_argument(
        "-k", "--key", required=True, help="Kunci rahasia untuk enkripsi"
    )

    decode_parser = subparsers.add_parser("decode", help="Ekstrak pesan dari gambar")
    decode_parser.add_argument(
        "-i",
        "--image",
        required=True,
        help="Path ke gambar yang berisi pesan (stego-image)",
    )
    decode_parser.add_argument(
        "-k", "--key", required=True, help="Kunci rahasia untuk dekripsi"
    )

    args = parser.parse_args()

    if args.command == "encode":
        hide_data(args.image, args.message, args.output, args.key)
    elif args.command == "decode":
        find_data(args.image, args.key)


if __name__ == "__main__":
    main()
