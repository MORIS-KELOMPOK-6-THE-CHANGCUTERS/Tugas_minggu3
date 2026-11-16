"""
Unit test untuk Sistem Data Mahasiswa.
"""

import unittest
import os
import sys
import tempfile
import shutil
import math

# Import modul yang diuji
sys.path.insert(0, os.path.dirname(__file__))
import nilai
import validasi
import absensi
import penyimpanan
from models import Mahasiswa, MataKuliah


class TestNilai(unittest.TestCase):
    """Test konversi nilai dan hitung IPK."""

    def test_nilai_ke_huruf_batas(self):
        self.assertEqual(nilai.nilai_ke_huruf(100), "A")
        self.assertEqual(nilai.nilai_ke_huruf(85), "A")
        self.assertEqual(nilai.nilai_ke_huruf(84.99), "B")
        self.assertEqual(nilai.nilai_ke_huruf(70), "B")
        self.assertEqual(nilai.nilai_ke_huruf(69.99), "C")
        self.assertEqual(nilai.nilai_ke_huruf(55), "C")
        self.assertEqual(nilai.nilai_ke_huruf(54.99), "D")
        self.assertEqual(nilai.nilai_ke_huruf(40), "D")
        self.assertEqual(nilai.nilai_ke_huruf(39.99), "E")
        self.assertEqual(nilai.nilai_ke_huruf(0), "E")

    def test_huruf_ke_bobot(self):
        self.assertEqual(nilai.huruf_ke_bobot("A"), 4.0)
        self.assertEqual(nilai.huruf_ke_bobot("B"), 3.0)
        self.assertEqual(nilai.huruf_ke_bobot("C"), 2.0)
        self.assertEqual(nilai.huruf_ke_bobot("D"), 1.0)
        self.assertEqual(nilai.huruf_ke_bobot("E"), 0.0)
        self.assertEqual(nilai.huruf_ke_bobot("a"), 4.0)

    def test_hitung_ipk_contoh_soal(self):
        """Algoritma 3 SKS 88, Basis Data 3 SKS 76, Statistika 2 SKS 82 -> IPK 3.38"""
        with tempfile.TemporaryDirectory() as tmpdir:
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                os.makedirs("data")
                # matakuliah.json
                mk = [
                    {"kode": "IF101", "nama": "Algoritma", "sks": 3, "dosen": "Pak Budi"},
                    {"kode": "IF102", "nama": "Basis Data", "sks": 3, "dosen": "Bu Sari"},
                    {"kode": "IF103", "nama": "Statistika", "sks": 2, "dosen": "Pak Joko"}
                ]
                penyimpanan.simpan("data/matakuliah.json", mk)
                # nilai.json
                n = [
                    {"nim": "2024001", "kode": "IF101", "nilai": 88},
                    {"nim": "2024001", "kode": "IF102", "nilai": 76},
                    {"nim": "2024001", "kode": "IF103", "nilai": 82}
                ]
                penyimpanan.simpan("data/nilai.json", n)
                ipk, total_sks, rincian = nilai.hitung_ipk("2024001")
                self.assertEqual(total_sks, 8)
                self.assertEqual(ipk, 3.38)
                self.assertEqual(len(rincian), 3)
            finally:
                os.chdir(old_cwd)

    def test_hitung_ipk_tanpa_nilai(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                os.makedirs("data")
                penyimpanan.simpan("data/matakuliah.json", [{"kode": "IF101", "nama": "Algoritma", "sks": 3, "dosen": "Pak Budi"}])
                penyimpanan.simpan("data/nilai.json", [])
                ipk, total_sks, rincian = nilai.hitung_ipk("2024001")
                self.assertEqual(total_sks, 0)
                self.assertEqual(ipk, 0.0)
                self.assertEqual(rincian, [])
            finally:
                os.chdir(old_cwd)

    def test_hitung_ipk_sks_nol(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                os.makedirs("data")
                penyimpanan.simpan("data/matakuliah.json", [{"kode": "IF101", "nama": "Algoritma", "sks": 0, "dosen": "Pak Budi"}])
                penyimpanan.simpan("data/nilai.json", [{"nim": "2024001", "kode": "IF101", "nilai": 80}])
                ipk, total_sks, rincian = nilai.hitung_ipk("2024001")
                self.assertEqual(total_sks, 0)
                self.assertEqual(ipk, 0.0)
            finally:
                os.chdir(old_cwd)


class TestValidasi(unittest.TestCase):
    """Test validasi input."""

    def test_validasi_nim(self):
        # NIM kosong
        ok, msg = validasi.validasi_nim("", [])
        self.assertFalse(ok)
        # NIM huruf
        ok, msg = validasi.validasi_nim("abc", [])
        self.assertFalse(ok)
        # NIM unik
        data = [{"nim": "123"}]
        ok, msg = validasi.validasi_nim("123", data)
        self.assertFalse(ok)
        # NIM valid
        ok, msg = validasi.validasi_nim("456", data)
        self.assertTrue(ok)

    def test_validasi_nilai(self):
        self.assertFalse(validasi.validasi_nilai(-1)[0])
        self.assertTrue(validasi.validasi_nilai(0)[0])
        self.assertTrue(validasi.validasi_nilai(100)[0])
        self.assertFalse(validasi.validasi_nilai(101)[0])
        # NaN
        self.assertFalse(validasi.validasi_nilai(float("nan"))[0])

    def test_validasi_tanggal(self):
        self.assertTrue(validasi.validasi_tanggal("2026-11-10")[0])
        self.assertFalse(validasi.validasi_tanggal("2026-1-5")[0])  # format salah
        self.assertFalse(validasi.validasi_tanggal("2026-02-30")[0])  # tanggal tidak valid

    def test_validasi_status_absensi(self):
        self.assertTrue(validasi.validasi_status_absensi("H")[0])
        self.assertTrue(validasi.validasi_status_absensi("i")[0])
        self.assertFalse(validasi.validasi_status_absensi("X")[0])

    def test_cek_pin(self):
        self.assertTrue(validasi.cek_pin("1234"))
        self.assertFalse(validasi.cek_pin("0000"))


class TestAbsensi(unittest.TestCase):
    """Test fungsi absensi."""

    def test_absensi_sudah_ada(self):
        data = [{"kode": "IF101", "tanggal": "2026-11-10", "status": {}}]
        self.assertTrue(absensi.absensi_sudah_ada(data, "IF101", "2026-11-10"))
        self.assertFalse(absensi.absensi_sudah_ada(data, "IF101", "2026-11-11"))
        self.assertFalse(absensi.absensi_sudah_ada(data, "IF102", "2026-11-10"))

    def test_hitung_kehadiran(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                os.makedirs("data")
                # 4 pertemuan, 3 H 1 I = 75%
                da = [
                    {"kode": "IF101", "tanggal": "2026-11-01", "status": {"2024001": "H"}},
                    {"kode": "IF101", "tanggal": "2026-11-02", "status": {"2024001": "H"}},
                    {"kode": "IF101", "tanggal": "2026-11-03", "status": {"2024001": "H"}},
                    {"kode": "IF101", "tanggal": "2026-11-04", "status": {"2024001": "I"}},
                ]
                mhs = [{"nim": "2024001", "nama": "Test", "prodi": "IF", "semester": 1}]
                penyimpanan.simpan("data/absensi.json", da)
                penyimpanan.simpan("data/mahasiswa.json", mhs)
                rincian = absensi.hitung_kehadiran("IF101")
                self.assertEqual(rincian[0]["hadir"], 3)
                self.assertEqual(rincian[0]["total"], 4)
                self.assertEqual(rincian[0]["persen"], 75.0)

                # 1 dari 4 = 25%
                da2 = [
                    {"kode": "IF102", "tanggal": "2026-11-01", "status": {"2024001": "H"}},
                    {"kode": "IF102", "tanggal": "2026-11-02", "status": {"2024001": "A"}},
                    {"kode": "IF102", "tanggal": "2026-11-03", "status": {"2024001": "S"}},
                    {"kode": "IF102", "tanggal": "2026-11-04", "status": {"2024001": "I"}},
                ]
                penyimpanan.simpan("data/absensi.json", da2)
                rincian = absensi.hitung_kehadiran("IF102")
                self.assertEqual(rincian[0]["hadir"], 1)
                self.assertEqual(rincian[0]["total"], 4)
                self.assertEqual(rincian[0]["persen"], 25.0)
            finally:
                os.chdir(old_cwd)


class TestPenyimpanan(unittest.TestCase):
    """Test penyimpanan file JSON."""

    def test_muat_file_belum_ada(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                data = penyimpanan.muat("data/tidakada.json")
                self.assertEqual(data, [])
                self.assertTrue(os.path.exists("data/tidakada.json"))
            finally:
                os.chdir(old_cwd)

    def test_muat_file_rusak_tanpa_backup(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                os.makedirs("data")
                with open("data/rusak.json", "w") as f:
                    f.write("{ ini json rusak }")
                data = penyimpanan.muat("data/rusak.json")
                self.assertEqual(data, [])
            finally:
                os.chdir(old_cwd)

    def test_simpan_membuat_backup(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                os.makedirs("data")
                os.makedirs("data/backup")
                data_awal = [{"nim": "1"}]
                penyimpanan.simpan("data/test.json", data_awal)
                data_baru = [{"nim": "2"}]
                penyimpanan.simpan("data/test.json", data_baru)
                # Cek backup ada
                backups = os.listdir("data/backup")
                self.assertTrue(len(backups) >= 1)
            finally:
                os.chdir(old_cwd)


class TestModels(unittest.TestCase):
    """Test model Mahasiswa dan MataKuliah."""

    def test_mahasiswa_to_dict_dari_dict(self):
        mhs = Mahasiswa("2024001", "Ani", "Informatika", 3)
        d = mhs.to_dict()
        mhs2 = Mahasiswa.dari_dict(d)
        self.assertEqual(mhs2.nim, "2024001")
        self.assertEqual(mhs2.nama, "Ani")
        self.assertEqual(mhs2.prodi, "Informatika")
        self.assertEqual(mhs2.semester, 3)

    def test_matakuliah_to_dict_dari_dict(self):
        mk = MataKuliah("IF101", "Algoritma", 3, "Pak Budi")
        d = mk.to_dict()
        mk2 = MataKuliah.dari_dict(d)
        self.assertEqual(mk2.kode, "IF101")
        self.assertEqual(mk2.nama, "Algoritma")
        self.assertEqual(mk2.sks, 3)
        self.assertEqual(mk2.dosen, "Pak Budi")


if __name__ == "__main__":
    unittest.main(verbosity=2)