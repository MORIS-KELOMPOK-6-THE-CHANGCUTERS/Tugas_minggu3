"""
Modul main: Menu utama dan alur program Sistem Data Mahasiswa.
Maks 280 baris.
"""

import penyimpanan
import validasi
from models import Mahasiswa, MataKuliah
import nilai
import absensi
import ui

SESI_ADMIN = False


def minta_pin():
    """Cek akses admin. Return True jika sudah/berhasil verifikasi."""
    global SESI_ADMIN
    if SESI_ADMIN:
        return True
    for _ in range(3):
        pin = input(ui.input_prompt("Masukkan PIN Admin"))
        if validasi.cek_pin(pin):
            SESI_ADMIN = True
            print(ui.success("Akses admin diterima."))
            return True
        print(ui.error("PIN Salah."))
    print(ui.error("Akses ditolak."))
    return False


def tampilkan_tabel_mhs(data):
    """Fungsi pembantu cetak tabel mahasiswa (responsive)."""
    if not data:
        print(ui.empty_state("Tidak ada data mahasiswa."))
        return
    rows = [[m['nim'], m['nama'], m['prodi'], str(m['semester'])] for m in data]
    print(ui.draw_table(["NIM", "Nama", "Prodi", "Sem"], rows))


def menu_mahasiswa():
    """Menu 1: Kelola Data Mahasiswa."""
    while True:
        print(ui.submenu_mahasiswa())
        pilih = input(ui.input_prompt("Pilih"))
        data = penyimpanan.muat("data/mahasiswa.json")

        if pilih == "1":
            tampilkan_tabel_mhs(data)
        elif pilih == "2":
            if not minta_pin():
                return
            # Input NIM
            nim = None
            for _ in range(3):
                inp = input(ui.input_prompt("NIM")).strip()
                ok, msg = validasi.validasi_nim(inp, data)
                if ok:
                    nim = inp
                    break
                print(ui.warning(msg))
            if not nim:
                continue
            # Input Nama
            nama = None
            for _ in range(3):
                inp = input(ui.input_prompt("Nama")).strip()
                ok, msg = validasi.validasi_nama(inp)
                if ok:
                    nama = inp
                    break
                print(ui.warning(msg))
            if not nama:
                continue
            # Input Prodi
            prodi = None
            for _ in range(3):
                inp = input(ui.input_prompt("Prodi")).strip()
                ok, msg = validasi.validasi_nama(inp)
                if ok:
                    prodi = inp
                    break
                print(ui.warning(msg))
            if not prodi:
                continue
            # Input Sem
            sem = validasi.input_angka_aman("Semester (1-14)", int, 1, 14)
            if sem is None:
                continue

            m_obj = Mahasiswa(nim, nama, prodi, sem)
            data.append(m_obj.to_dict())
            penyimpanan.simpan("data/mahasiswa.json", data)
            print(ui.success("Berhasil ditambah."))
        elif pilih == "3":
            if not minta_pin():
                return
            nim = input(ui.input_prompt("NIM yang akan diubah")).strip()
            m = nilai.cari_mahasiswa(data, nim)
            if not m:
                print(ui.error("NIM tidak ditemukan."))
                continue
            nama = input(ui.input_prompt(f"Nama baru [{m['nama']}]: ")).strip() or m['nama']
            prodi = input(ui.input_prompt(f"Prodi baru [{m['prodi']}]: ")).strip() or m['prodi']
            sem_baru = m['semester']
            for _ in range(3):
                inp = input(ui.input_prompt(f"Semester baru [{m['semester']}]: ")).strip()
                if not inp:
                    break
                ok, msg = validasi.validasi_semester(inp)
                if ok:
                    sem_baru = int(inp)
                    break
                print(ui.warning(msg))
            else:
                print(ui.error("Batal: Semester salah 3 kali. Perubahan dibatalkan."))
                continue
            m['nama'], m['prodi'], m['semester'] = nama, prodi, sem_baru
            penyimpanan.simpan("data/mahasiswa.json", data)
            print(ui.success("Berhasil diubah."))
        elif pilih == "4":
            if not minta_pin():
                return
            nim = input(ui.input_prompt("NIM yang akan dihapus")).strip()
            m = nilai.cari_mahasiswa(data, nim)
            if not m:
                print(ui.error("NIM tidak ditemukan."))
                continue
            if input(ui.confirm_prompt(f"Hapus {m['nama']}?")).lower() == 'y':
                data = [x for x in data if x['nim'] != nim]
                penyimpanan.simpan("data/mahasiswa.json", data)
                dn = [x for x in penyimpanan.muat("data/nilai.json") if x['nim'] != nim]
                penyimpanan.simpan("data/nilai.json", dn)
                da = penyimpanan.muat("data/absensi.json")
                for a in da:
                    if nim in a['status']:
                        del a['status'][nim]
                penyimpanan.simpan("data/absensi.json", da)
                print(ui.success("Berhasil dihapus."))
        elif pilih == "0":
            break
        else:
            print(ui.error("Pilihan salah."))


def menu_matakuliah():
    """Menu 2: Kelola Data Mata Kuliah."""
    while True:
        print(ui.submenu_matakuliah())
        pilih = input(ui.input_prompt("Pilih"))
        data = penyimpanan.muat("data/matakuliah.json")

        if pilih == "1":
            if not data:
                print(ui.empty_state("Tidak ada data mata kuliah."))
                continue
            rows = [[m['kode'], m['nama'], str(m['sks']), m['dosen']] for m in data]
            print(ui.draw_table(["Kode", "Nama", "SKS", "Dosen"], rows))
        elif pilih == "2":
            if not minta_pin():
                return
            kode = None
            for _ in range(3):
                inp = input(ui.input_prompt("Kode MK")).strip()
                ok, msg, up = validasi.validasi_kode_mk(inp, data)
                if ok:
                    kode = up
                    break
                print(ui.warning(msg))
            if not kode:
                return
            nama = None
            for _ in range(3):
                inp = input(ui.input_prompt("Nama MK")).strip()
                ok, msg = validasi.validasi_nama(inp)
                if ok:
                    nama = inp
                    break
                print(ui.warning(msg))
            if not nama:
                return
            sks = validasi.input_angka_aman("SKS (1-6)", int, 1, 6)
            if sks is None:
                return
            dosen = None
            for _ in range(3):
                inp = input(ui.input_prompt("Dosen")).strip()
                ok, msg = validasi.validasi_nama(inp)
                if ok:
                    dosen = inp
                    break
                print(ui.warning(msg))
            if not dosen:
                return
            mk_obj = MataKuliah(kode, nama, sks, dosen)
            data.append(mk_obj.to_dict())
            penyimpanan.simpan("data/matakuliah.json", data)
            print(ui.success("Berhasil ditambah."))
        elif pilih == "3":
            if not minta_pin():
                return
            kode = input(ui.input_prompt("Kode MK yang akan diubah")).strip().upper()
            m = nilai.cari_matakuliah(data, kode)
            if not m:
                print(ui.error("Kode tidak ditemukan."))
                continue
            m['nama'] = input(ui.input_prompt(f"Nama baru [{m['nama']}]: ")).strip() or m['nama']
            sks_baru = m['sks']
            for _ in range(3):
                inp = input(ui.input_prompt(f"SKS baru [{m['sks']}]: ")).strip()
                if not inp:
                    break
                ok, msg = validasi.validasi_sks(inp)
                if ok:
                    sks_baru = int(inp)
                    break
                print(ui.warning(msg))
            else:
                print(ui.error("Batal: SKS salah 3 kali. Perubahan dibatalkan."))
                continue
            m['sks'] = sks_baru
            m['dosen'] = input(ui.input_prompt(f"Dosen baru [{m['dosen']}]: ")).strip() or m['dosen']
            penyimpanan.simpan("data/matakuliah.json", data)
            print(ui.success("Berhasil diubah."))
        elif pilih == "4":
            if not minta_pin():
                return
            kode = input(ui.input_prompt("Kode MK yang akan dihapus")).strip().upper()
            m = nilai.cari_matakuliah(data, kode)
            if not m:
                print(ui.error("Kode tidak ditemukan."))
                continue
            if input(ui.confirm_prompt(f"Hapus {m['nama']}?")).lower() == 'y':
                data = [x for x in data if x['kode'] != kode]
                penyimpanan.simpan("data/matakuliah.json", data)
                dn = [x for x in penyimpanan.muat("data/nilai.json") if x['kode'] != kode]
                penyimpanan.simpan("data/nilai.json", dn)
                da = [x for x in penyimpanan.muat("data/absensi.json") if x['kode'] != kode]
                penyimpanan.simpan("data/absensi.json", da)
                print(ui.success("Berhasil dihapus."))
        elif pilih == "0":
            break
        else:
            print(ui.error("Pilihan salah."))


def key_nama(x):
    return x['nama']


def key_nim(x):
    return x['nim']


def key_ipk(x):
    return nilai.hitung_ipk(x['nim'])[0]


def menu_cari_urut():
    """Menu 6: Cari & Urutkan."""
    while True:
        print(ui.submenu_cari_urut())
        pilih = input(ui.input_prompt("Pilih"))
        if pilih not in ("1", "2", "0"):
            print(ui.error("Pilihan salah."))
            continue
        data = penyimpanan.muat("data/mahasiswa.json")
        if not data:
            print(ui.empty_state("Data mahasiswa kosong."))
            break

        if pilih == "1":
            key = None
            for _ in range(3):
                key = input(ui.input_prompt("Kata kunci (NIM/Nama)")).strip().lower()
                if key:
                    break
                print(ui.warning("Kata kunci tidak boleh kosong."))
            else:
                print(ui.error("Batal: Kata kunci kosong 3 kali."))
                continue
            if not key:
                continue
            hasil = []
            for m in data:
                if key in m['nim'].lower() or key in m['nama'].lower():
                    hasil.append(m)
            if not hasil:
                print(ui.warning("Tidak ditemukan."))
                continue
            tampilkan_tabel_mhs(hasil)
        elif pilih == "2":
            krit_baru = None
            for _ in range(3):
                print(ui.sort_kriteria_menu())
                krit = input(ui.input_prompt("Pilih"))
                if krit in ("1", "2", "3"):
                    krit_baru = krit
                    break
                print(ui.warning("Kriteria harus 1, 2, atau 3."))
            if krit_baru is None:
                print(ui.error("Batal: Kriteria salah 3 kali."))
                continue
            arah_baru = None
            for _ in range(3):
                print(ui.sort_arah_menu())
                arah = input(ui.input_prompt("Pilih"))
                if arah in ("1", "2"):
                    arah_baru = arah
                    break
                print(ui.warning("Arah harus 1 atau 2."))
            if arah_baru is None:
                print(ui.error("Batal: Arah salah 3 kali."))
                continue

            f_key = key_nama
            if krit_baru == "2":
                f_key = key_nim
            elif krit_baru == "3":
                f_key = key_ipk

            rev = (arah_baru == "2")
            data_sorted = sorted(data, key=f_key, reverse=rev)

            rows = [[m['nim'], m['nama'], f"{nilai.hitung_ipk(m['nim'])[0]:.2f}"] for m in data_sorted]
            print(ui.draw_table(["NIM", "Nama", "IPK"], rows))
        elif pilih == "0":
            break


def menu_absensi():
    """Submenu Absensi (Menu 5): Input, Rekap, Kembali."""
    while True:
        print(ui.submenu_absensi())
        p = input(ui.input_prompt("Pilih"))
        if p not in ("1", "2", "0"):
            print(ui.error("Pilihan salah."))
            continue
        if p == "1":
            if minta_pin():
                absensi.input_absensi()
        elif p == "2":
            absensi.rekap_absensi()
        elif p == "0":
            break


def main():
    penyimpanan.siapkan_folder()
    # Pemicu peringatan file rusak di awal
    for f in ["mahasiswa", "matakuliah", "nilai", "absensi"]:
        penyimpanan.muat(f"data/{f}.json")

    print(ui.header("SISTEM DATA MAHASISWA"))

    while True:
        try:
            print(ui.main_menu())
            pilih = input(ui.input_prompt("Pilih menu"))

            if pilih == "1":
                menu_mahasiswa()
            elif pilih == "2":
                menu_matakuliah()
            elif pilih == "3":
                if minta_pin():
                    nilai.menu_input_nilai()
            elif pilih == "4":
                nilai.menu_lihat_ipk()
            elif pilih == "5":
                menu_absensi()
            elif pilih == "6":
                menu_cari_urut()
            elif pilih == "0":
                print(ui.success("Data sudah tersimpan otomatis. Sampai jumpa."))
                break
            else:
                print(ui.error("Pilihan salah."))
        except (KeyboardInterrupt, EOFError):
            print(f"\n{ui.error('Program dihentikan paksa. Keluar.')}")
            break
        except Exception as e:
            print(ui.error(f"Terjadi kesalahan: {str(e)}"))


if __name__ == "__main__":
    main()