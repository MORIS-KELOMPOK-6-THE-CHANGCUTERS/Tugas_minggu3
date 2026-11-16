"""
Skrip seed data untuk Sistem Data Mahasiswa.
"""

import os
import penyimpanan
from models import Mahasiswa, MataKuliah


def main():
    # Cek apakah data sudah ada
    data_dir = "data"
    if os.path.exists(data_dir) and any(os.listdir(data_dir)):
        jawab = input("Data sudah ada. Timpa? (y/n): ").strip().lower()
        if jawab != "y":
            print("Batal.")
            return

    print("Membuat data seed...")

    # 10 Mahasiswa
    mhs_list = [
        Mahasiswa("2024001", "Ani Wijaya", "Informatika", 3),
        Mahasiswa("2024002", "Budi Santoso", "Informatika", 3),
        Mahasiswa("2024003", "Citra Dewi", "Sistem Informasi", 2),
        Mahasiswa("2024004", "Dedi Kurniawan", "Informatika", 1),
        Mahasiswa("2024005", "Eka Putri", "Sistem Informasi", 4),
        Mahasiswa("2024006", "Fajar Hidayat", "Informatika", 3),
        Mahasiswa("2024007", "Gina Sari", "Sistem Informasi", 2),
        Mahasiswa("2024008", "Hadi Pranoto", "Informatika", 5),
        Mahasiswa("2024009", "Indah Lestari", "Sistem Informasi", 1),
        Mahasiswa("2024010", "Joko Widodo", "Informatika", 7),
    ]
    penyimpanan.simpan("data/mahasiswa.json", [m.to_dict() for m in mhs_list])

    # 5 Mata Kuliah
    mk_list = [
        MataKuliah("IF101", "Algoritma dan Pemrograman", 3, "Dr. Budi Raharjo"),
        MataKuliah("IF102", "Basis Data", 3, "Dr. Siti Aminah"),
        MataKuliah("IF103", "Statistika", 2, "Dr. Joko Susilo"),
        MataKuliah("SI201", "Analisis Sistem", 3, "Dr. Rina Wati"),
        MataKuliah("IF301", "Pemrograman Web", 4, "Dr. Andi Setiawan"),
    ]
    penyimpanan.simpan("data/matakuliah.json", [m.to_dict() for m in mk_list])

    # Nilai: Ani (2024001) -> IPK 3.38 (Algoritma 88, Basis Data 76, Statistika 82)
    # Mahasiswa lain mendapat nilai acak demo
    nilai_list = [
        # Ani - target IPK 3.38
        {"nim": "2024001", "kode": "IF101", "nilai": 88},   # A, 4.0 * 3 = 12.0
        {"nim": "2024001", "kode": "IF102", "nilai": 76},   # B, 3.0 * 3 = 9.0
        {"nim": "2024001", "kode": "IF103", "nilai": 82},   # B, 3.0 * 2 = 6.0
        # Total bobot*sks = 27, total sks = 8, IPK = 3.375 -> 3.38
        
        # Budi
        {"nim": "2024002", "kode": "IF101", "nilai": 75},
        {"nim": "2024002", "kode": "IF102", "nilai": 80},
        {"nim": "2024002", "kode": "IF103", "nilai": 70},
        
        # Citra
        {"nim": "2024003", "kode": "SI201", "nilai": 85},
        {"nim": "2024003", "kode": "IF102", "nilai": 90},
        
        # Dedi
        {"nim": "2024004", "kode": "IF101", "nilai": 65},
        
        # Eka
        {"nim": "2024005", "kode": "SI201", "nilai": 92},
        {"nim": "2024005", "kode": "IF301", "nilai": 78},
        
        # Fajar
        {"nim": "2024006", "kode": "IF101", "nilai": 55},
        {"nim": "2024006", "kode": "IF102", "nilai": 60},
        
        # Gina
        {"nim": "2024007", "kode": "SI201", "nilai": 88},
        
        # Hadi
        {"nim": "2024008", "kode": "IF301", "nilai": 95},
        
        # Indah (tidak punya nilai sama sekali)
        
        # Joko
        {"nim": "2024010", "kode": "IF301", "nilai": 82},
    ]
    penyimpanan.simpan("data/nilai.json", nilai_list)

    # Absensi 4 pertemuan IF101:
    # - Ani (2024001): 3H, 1I -> 75.0% (tepat 75, tidak peringatan)
    # - Budi (2024002): 2H, 2A -> 50.0% (PERINGATAN)
    # - Citra (2024003): 1H, 3S -> 25.0% (PERINGATAN)
    # - Dedi (2024004): 4H -> 100%
    # - Eka (2024005): 3H, 1I -> 75.0%
    # - Fajar (2024006): 2H, 2I -> 50.0% (PERINGATAN)
    # - Gina (2024007): 3H, 1A -> 75.0%
    # - Hadi (2024008): 4H -> 100%
    # - Indah (2024009): 0H, 4A -> 0% (PERINGATAN)
    # - Joko (2024010): 2H, 2S -> 50.0% (PERINGATAN)
    absensi_list = [
        {
            "kode": "IF101",
            "tanggal": "2026-11-01",
            "status": {
                "2024001": "H", "2024002": "H", "2024003": "H", "2024004": "H",
                "2024005": "H", "2024006": "H", "2024007": "H", "2024008": "H",
                "2024009": "A", "2024010": "H"
            }
        },
        {
            "kode": "IF101",
            "tanggal": "2026-11-02",
            "status": {
                "2024001": "H", "2024002": "A", "2024003": "S", "2024004": "H",
                "2024005": "H", "2024006": "I", "2024007": "H", "2024008": "H",
                "2024009": "A", "2024010": "S"
            }
        },
        {
            "kode": "IF101",
            "tanggal": "2026-11-03",
            "status": {
                "2024001": "H", "2024002": "H", "2024003": "S", "2024004": "H",
                "2024005": "I", "2024006": "H", "2024007": "A", "2024008": "H",
                "2024009": "A", "2024010": "H"
            }
        },
        {
            "kode": "IF101",
            "tanggal": "2026-11-04",
            "status": {
                "2024001": "I", "2024002": "A", "2024003": "S", "2024004": "H",
                "2024005": "H", "2024006": "I", "2024007": "H", "2024008": "H",
                "2024009": "A", "2024010": "S"
            }
        },
    ]
    penyimpanan.simpan("data/absensi.json", absensi_list)

    print("Seed selesai!")
    print("- 10 mahasiswa (Informatika & Sistem Informasi)")
    print("- 5 mata kuliah (IF101, IF102, IF103, SI201, IF301)")
    print("- Nilai lengkap, Ani (2024001) IPK 3.38")
    print("- Indah (2024009) tidak punya nilai")
    print("- 4 pertemuan absensi IF101")
    print("- 4 mahasiswa di bawah 75%: Budi, Citra, Fajar, Indah, Joko (PERINGATAN)")
    print("- 3 mahasiswa tepat 75%: Ani, Eka, Gina")


if __name__ == "__main__":
    main()