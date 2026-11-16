"""
Modul penyimpanan: mengatur baca/tulis file JSON, backup, dan persiapan folder data.
"""

import json
import os
import shutil
from datetime import datetime


def siapkan_folder():
    """
    Membuat folder data/ dan data/backup/ jika belum ada.
    Dipanggil saat program mulai.
    Input: tidak ada
    Output: tidak ada (side effect: folder dibuat)
    """
    folder_data = "data"
    folder_backup = os.path.join(folder_data, "backup")

    if not os.path.exists(folder_data):
        os.makedirs(folder_data)
    if not os.path.exists(folder_backup):
        os.makedirs(folder_backup)


def _buat_backup(path_file):
    """
    Menyalin file lama ke folder backup dengan nama file + tanggal.
    Dipanggil sebelum menimpa file.
    Input: path_file (string) - path file yang akan di-backup
    Output: True jika berhasil, False jika file tidak ada atau gagal
    """
    if not os.path.exists(path_file):
        return False

    try:
        nama_file = os.path.basename(path_file)
        nama_tanpa_ext, ext = os.path.splitext(nama_file)
        tanggal_sekarang = datetime.now().strftime("%Y-%m-%d")
        nama_backup = f"{nama_tanpa_ext}_{tanggal_sekarang}{ext}"
        path_backup = os.path.join("data", "backup", nama_backup)

        shutil.copy2(path_file, path_backup)
        return True
    except Exception:
        return False


def muat(path_file):
    """
    Memuat data dari file JSON. Jika file tidak ada, buat file baru berisi [].
    Jika file rusak (JSON invalid), coba pakai backup terakhir.
    Input: path_file (string) - path file JSON
    Output: list - data yang dimuat (list of dict)
    """
    siapkan_folder()

    # Jika file tidak ada, buat file kosong
    if not os.path.exists(path_file):
        with open(path_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []

    # Coba baca file
    try:
        with open(path_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            # Bukan list, anggap rusak
            raise ValueError("Data bukan list")
    except (json.JSONDecodeError, ValueError) as e:
        # File rusak, coba backup
        print(f"PERINGATAN: File {path_file} rusak ({type(e).__name__}), mencoba pulihkan dari backup...")
        data_backup = _coba_backup_terakhir(path_file)
        if data_backup is not None:
            print("BERHASIL: Data dipulihkan dari backup terakhir.")
            return data_backup
        else:
            print("GAGAL: Tidak ada backup valid, memulai dari data kosong [].")
            return []


def _coba_backup_terakhir(path_file):
    """
    Mencari backup terbaru untuk file yang rusak.
    Input: path_file (string)
    Output: list data dari backup, atau None jika tidak ada backup
    """
    nama_file = os.path.basename(path_file)
    nama_tanpa_ext, ext = os.path.splitext(nama_file)
    folder_backup = os.path.join("data", "backup")

    if not os.path.exists(folder_backup):
        return None

    # Cari file backup yang cocok
    daftar_backup = []
    for file_backup in os.listdir(folder_backup):
        if file_backup.startswith(nama_tanpa_ext + "_") and file_backup.endswith(ext):
            path_backup = os.path.join(folder_backup, file_backup)
            daftar_backup.append((path_backup, os.path.getmtime(path_backup)))

    if not daftar_backup:
        return None

    # Ambil yang paling baru (modified time terbesar)
    daftar_backup.sort(key=lambda x: x[1], reverse=True)
    path_terbaru = daftar_backup[0][0]

    try:
        with open(path_terbaru, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        pass

    return None


def _file_valid_json_list(path_file):
    """
    Cek apakah file berisi JSON valid dan bertipe list.
    Input: path_file (string)
    Output: True jika valid list, False jika tidak
    """
    try:
        with open(path_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return isinstance(data, list)
    except Exception:
        return False


def simpan(path_file, data):
    """
    Menyimpan data ke file JSON. Backup file lama dulu sebelum menimpa.
    Hanya backup jika file lama valid (JSON list), agar file rusak tidak menimpa backup baik.
    Input: path_file (string), data (list of dict)
    Output: True jika berhasil, False jika gagal
    """
    siapkan_folder()

    # Backup file lama hanya jika file lama valid
    if os.path.exists(path_file) and _file_valid_json_list(path_file):
        _buat_backup(path_file)
    elif os.path.exists(path_file):
        print(f"Peringatan: File {path_file} rusak/tidak valid, backup dilewati.")

    try:
        # Tulis ke file sementara dulu, lalu rename (atomic write)
        path_sementara = path_file + ".tmp"
        with open(path_sementara, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Rename menggantikan file lama
        os.replace(path_sementara, path_file)
        return True
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan: {e}")
        # Hapus file sementara jika ada
        if os.path.exists(path_sementara):
            try:
                os.remove(path_sementara)
            except Exception:
                pass
        return False