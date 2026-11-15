# Sistem Data Mahasiswa

Proyek Tugas Akhir minggu ke 3 **MORRIS IF 2026** — Teknik Informatika Universitas Logistik dan Bisnis Internasional (ULBI).  
Aplikasi konsol interaktif berbasis **Python** untuk pengelolaan data mahasiswa, mata kuliah, perhitungan nilai & IPK otomatis, serta pemantauan rekap absensi dengan sistem keamanan PIN Admin.

---

## 👥 Identitas Kelompok
**Nama Kelompok:** Kelompok 6 The Changcuters  
**Tema Aplikasi:** Nilai Mahasiswa

| No | Nama Lengkap | NPM | Peran dalam Tim |
| :--- | :--- | :--- | :--- |
| 1 | **Rahmatan Gani** | **714260001** | **Programmer Utama** |
| 2 | **Zu Fauzan Yusuf** | **613260022** | **Programmer / Integrasi** |
| 3 | **Muhammad Fachry** | **613260017** | **Perancang Flowchart** |
| 4 | **Andika Dwi Permana** | **714260002** | **Penulis Dokumentasi (`README.md`)** |
| 5 | **Mutia Anggraini** | **714260007** | **Desainer Poster A3** |
| 6 | **Wijdan Athar Nurfaizi** | **714260009** | **Penguji / QA (*Quality Assurance*)** |
| 7 | **Muhammad Hilal Ahmar** | **613260016** | **Koordinator Video & Publikasi** |

---

## 📌 Deskripsi Aplikasi & Masalah yang Diselesaikan
### Permasalahan
Pengelolaan administrasi akademik secara manual—seperti mengolah nilai mata kuliah, mengonversi nilai ke bobot IPK sesuai SKS, hingga memantau persentase kehadiran mahasiswa—sering memakan waktu lama dan sangat rentan terhadap kesalahan hitung (*human error*).

### Solusi Aplikasi
**Sistem Data Mahasiswa** hadir sebagai aplikasi terminal terpadu dengan tampilan tabel berwarna yang rapi. Program ini mengotomatiskan perhitungan konversi nilai huruf, bobot, total SKS, dan IPK akhir, memantau status kehadiran (*Aman* atau *PERINGATAN*), serta membatasi akses modifikasi data penting menggunakan **PIN Admin**.

---

## ✨ Daftar Fitur Utama & Cara Penggunaan

Aplikasi memiliki **6 fitur utama** yang dapat diakses melalui menu interaktif berulang:

1. **Data Mahasiswa (`1`) — *Dilengkapi Keamanan PIN Admin***
   * **Sub-menu:** Lihat (`1`), Tambah (`2`), Ubah (`3`), Hapus (`4`), dan Kembali (`0`).
   * **Cara pakai:** Pilih menu `1`, lalu pilih aksi yang diinginkan. Untuk aksi penambahan/pengubahan/penghapusan data, pengguna wajib memasukkan **PIN Admin** (maksimal 3 kali percobaan salah sebelum akses ditolak otomatis).
2. **Data Mata Kuliah (`2`)**
   * **Cara pakai:** Pilih menu `2` untuk melihat dan mengelola daftar mata kuliah beserta Kode MK dan jumlah SKS.
3. **Input Nilai (`3`)**
   * **Cara pakai:** Pilih menu `3` untuk memasukkan nilai angka mahasiswa pada mata kuliah yang diambil.
4. **Lihat IPK (`4`)**
   * **Cara pakai:** Pilih menu `4`, lalu masukkan **NIM** mahasiswa (contoh: `2024001`). Sistem akan menampilkan identitas mahasiswa beserta tabel transkrip lengkap (`Kode`, `Mata Kuliah`, `SKS`, `Nilai`, `Huruf`, `Bobot`) serta hasil perhitungan **Total SKS** dan **IPK** akhir secara otomatis.
5. **Absensi (`5`)**
   * **Sub-menu:** Input absensi (`1`), Rekap kehadiran (`2`), dan Kembali (`0`).
   * **Cara pakai:** Pada menu Rekap Kehadiran, masukkan **Kode MK** (contoh: `IF101`). Program menampilkan tabel jumlah hadir, total pertemuan, persentase kehadiran, dan status otomatis (**Aman** berwarna hijau atau **PERINGATAN** berwarna merah).
6. **Cari & Urutkan (`6`)**
   * **Cara pakai:** Pilih menu `6` untuk mencari data mahasiswa tertentu atau mengurutkan daftar mahasiswa secara cepat.
7. **Keluar (`0`)**
   * **Cara pakai:** Pilih `0` pada menu utama untuk menghentikan program dengan rapi.

---

## 🛡️ Validasi & Keamanan Input
Program ini dirancang tahan terhadap kesalahan ketik (*error handling*), meliputi:
* **Validasi Pilihan Menu:** Menolak pilihan menu di luar daftar (contoh: mengetik `9` pada menu absensi akan memunculkan `Pilihan salah.` dan kembali ke menu).
* **Proteksi PIN Admin:** Membatasi kesalahan input PIN maksimal **3 kali** sebelum memunculkan peringatan `✖ Akses ditolak.`.
* **Validasi Tipe & Rentang Data:** Menolak input kosong, ketikan huruf saat diminta angka, serta angka di luar batas wajar.

---

## 📁 Struktur File & Alur Logika Program

Aplikasi dibangun secara modular menggunakan 9 file Python (`.py`) yang saling terhubung dengan perintah `import`:

* **`main.py`** — Titik masuk utama (*entry point*) yang mengatur perulangan menu utama (`while True`) dan navigasi seluruh fitur.
* **`ui.py`** — Mengatur tampilan antarmuka di terminal (cetakan kotak menu, tabel data rapi, dan pewarnaan teks).
* **`models.py`** — Mendefinisikan struktur/cetakan data untuk mahasiswa, mata kuliah, nilai, dan absensi.
* **`nilai.py`** — Berisi logika pengolahan nilai, konversi ke nilai huruf/bobot, serta perhitungan otomatis Total SKS dan IPK.
* **`absensi.py`** — Menangani fitur input kehadiran dan rekap persentase status kehadiran (*Aman* atau *PERINGATAN*).
* **`validasi.py`** — Menangani validasi keamanan input (menolak input kosong, salah tipe angka/huruf, menu tidak valid, serta verifikasi PIN Admin).
* **`penyimpanan.py`** — Mengatur proses simpan dan baca data aplikasi ke/dari folder `data/`.
* **`seed.py`** — Menyediakan skrip data contoh (*sample data*) untuk keperluan pengujian awal program.
* **`test_app.py`** — Skrip pengujian (*testing*) untuk memastikan seluruh fitur dan validasi berjalan normal tanpa *bug*.
* **`data/`** — Folder penyimpanan berkas data aplikasi.

### Alur Logika Singkat
1. Saat dijalankan melalui `main.py`, program memuat data melalui `penyimpanan.py` dan menampilkan antarmuka menu dari `ui.py`.
2. Pengguna memilih menu secara berulang (*looping*).
3. Setiap ketikan pengguna diperiksa terlebih dahulu oleh `validasi.py` sebelum diproses oleh `nilai.py` atau `absensi.py`.
4. Hasil pengolahan data dicetak ke layar dan disimpan kembali secara rapi hingga pengguna memilih `0` (Keluar).

---

## 💻 Cara Menjalankan Program di Komputer Lain

pastikan **Python 3** sudah terinstal di komputer, lalu jalankan perintah berikut di Terminal / CMD:

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/MORIS-KELOMPOK-6-THE-CHANGCUTERS/Tugas_minggu3.git
   ```
2. **Masuk ke folder proyek:**
   ```bash
   cd Tugas_minggu3
   ```
3. **Jalankan program utama:**
   ```bash
   python main.py
   ```