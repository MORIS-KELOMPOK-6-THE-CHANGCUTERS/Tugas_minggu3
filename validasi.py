"""
Modul validasi: menangani verifikasi input data dan authentikasi PIN Admin.
Hanya menggunakan library bawaan Python.
"""

from datetime import datetime
import math

PIN_ADMIN = "1234"


def cek_pin(input_pin):
    """
    Memeriksa apakah PIN yang dimasukkan sesuai dengan PIN_ADMIN.
    Input: input_pin (string)
    Output: bool - True jika benar, False jika salah
    """
    return str(input_pin).strip() == PIN_ADMIN


def validasi_nim(nim, daftar_mahasiswa=None, nim_lama=None):
    """
    Memvalidasi NIM: tidak boleh kosong, harus berupa angka saja, dan harus unik.
    Input:
        nim (string)
        daftar_mahasiswa (list of dict, opsional) - untuk cek keunikan
        nim_lama (string, opsional) - NIM saat ini jika dalam mode ubah data
    Output: tuple (bool, string) - (Status Valid, Pesan Error/Status)
    """
    nim_str = str(nim).strip()
    if not nim_str:
        return False, "NIM tidak boleh kosong."
    if not nim_str.isdigit():
        return False, "NIM hanya boleh berisi angka."
    if not nim_str.isascii():
        return False, "NIM harus berisi karakter ASCII."
    if daftar_mahasiswa is not None:
        for mhs in daftar_mahasiswa:
            # Jika sedang mode ubah, abaikan NIM lama sendiri
            if nim_lama and mhs.get("nim") == nim_lama:
                continue
            if mhs.get("nim") == nim_str:
                return False, "NIM sudah terdaftar (harus unik)."

    return True, "Valid"


def validasi_kode_mk(kode, daftar_mk=None, kode_lama=None):
    """
    Memvalidasi Kode Mata Kuliah: tidak kosong, otomatis huruf besar, dan unik.
    Input:
        kode (string)
        daftar_mk (list of dict, opsional)
        kode_lama (string, opsional)
    Output: tuple (bool, string, string) - (Status Valid, Pesan, Kode Uppercase)
    """
    kode_str = str(kode).strip().upper()
    if not kode_str:
        return False, "Kode mata kuliah tidak boleh kosong.", kode_str

    if daftar_mk is not None:
        for mk in daftar_mk:
            if kode_lama and mk.get("kode") == kode_lama:
                continue
            if mk.get("kode") == kode_str:
                return False, "Kode mata kuliah sudah terdaftar (harus unik).", kode_str

    return True, "Valid", kode_str


def validasi_nama(nama):
    """
    Memvalidasi nama/prodi: tidak boleh kosong.
    Input: nama (string)
    Output: tuple (bool, string)
    """
    if not str(nama).strip():
        return False, "Nama/Prodi tidak boleh kosong."
    return True, "Valid"


def validasi_semester(semester):
    """
    Memvalidasi semester: angka 1-14.
    Input: semester (int/string)
    Output: tuple (bool, string)
    """
    try:
        val = int(semester)
        if 1 <= val <= 14:
            return True, "Valid"
        return False, "Semester harus berupa angka antara 1 sampai 14."
    except (ValueError, TypeError):
        return False, "Semester harus berupa angka bulat."


def validasi_sks(sks):
    """
    Memvalidasi SKS: angka 1-6.
    Input: sks (int/string)
    Output: tuple (bool, string)
    """
    try:
        val = int(sks)
        if 1 <= val <= 6:
            return True, "Valid"
        return False, "SKS harus berupa angka antara 1 sampai 6."
    except (ValueError, TypeError):
        return False, "SKS harus berupa angka bulat."


def validasi_nilai(nilai):
    """
    Memvalidasi nilai angka: 0-100.
    Input: nilai (float/int/string)
    Output: tuple (bool, string)
    """
    try:
        val = float(nilai)
        if 0 <= val <= 100:
            return True, "Valid"
        return False, "Nilai harus rentang 0 sampai 100."
    except (ValueError, TypeError):
        return False, "Nilai harus berupa angka."


def validasi_tanggal(tanggal_str):
    """
    Memvalidasi format tanggal YYYY-MM-DD menggunakan modul datetime.
    Input: tanggal_str (string)
    Output: tuple (bool, string)
    """
    tanggal_str = str(tanggal_str).strip()
    if len(tanggal_str) != 10:
        return False, "Format tanggal harus 10 karakter (YYYY-MM-DD)."
    try:
        datetime.strptime(tanggal_str, "%Y-%m-%d")
        return True, "Valid"
    except ValueError:
        return False, "Format tanggal harus YYYY-MM-DD (contoh: 2026-11-10)."


def validasi_status_absensi(status):
    """
    Memvalidasi status absensi: H/I/S/A (case-insensitive).
    Input: status (string)
    Output: tuple (bool, string, string) - (Status Valid, Pesan, Status Uppercase)
    """
    st = str(status).strip().upper()
    if st in ["H", "I", "S", "A"]:
        return True, "Valid", st
    return False, "Status absensi harus H (Hadir), I (Izin), S (Sakit), atau A (Alpa).", st


def input_angka_aman(prompt, tipe=int, min_val=None, max_val=None, max_percobaan=3):
    """
    Menerima input angka dari pengguna secara aman dengan batas percobaan.
    Input:
        prompt (string) - Pesan input
        tipe (type) - int atau float
        min_val (number, opsional)
        max_val (number, opsional)
        max_percobaan (int) - Maksimal percobaan sebelum batal (default 3)
    Output: angka jika berhasil, None jika gagal/batal setelah 3x percobaan
    """
    percobaan = 0
    while percobaan < max_percobaan:
        try:
            inp = input(prompt)
            val = tipe(inp)
            # Tolak NaN untuk tipe float
            if tipe is float and math.isnan(val):
                print(f"Peringatan: Input tidak valid (NaN).")
                percobaan += 1
                continue
            if min_val is not None and val < min_val:
                print(f"Peringatan: Nilai minimal adalah {min_val}.")
                percobaan += 1
                continue
            if max_val is not None and val > max_val:
                print(f"Peringatan: Nilai maksimal adalah {max_val}.")
                percobaan += 1
                continue
            return val
        except (ValueError, TypeError):
            print(f"Peringatan: Input harus berupa angka ({tipe.__name__}).")
            percobaan += 1

    print("Batal: Memenuhi batas maksimal percobaan salah.")
    return None