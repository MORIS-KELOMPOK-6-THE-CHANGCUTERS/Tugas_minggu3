"""
Modul nilai: konversi nilai, perhitungan IPK, menu Input & Lihat IPK.
Maks 130 baris. Menggunakan penyimpanan, validasi.
"""

import penyimpanan
import validasi
import ui


def nilai_ke_huruf(nilai):
    """Konversi angka 0-100 ke huruf A/B/C/D/E (>=85 A, >=70 B, >=55 C, >=40 D)."""
    if nilai >= 85:
        return "A"
    if nilai >= 70:
        return "B"
    if nilai >= 55:
        return "C"
    if nilai >= 40:
        return "D"
    return "E"


def huruf_ke_bobot(huruf):
    """Konversi huruf ke bobot IPK (A=4.0, B=3.0, C=2.0, D=1.0, E=0.0)."""
    return {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "E": 0.0}.get(huruf.upper(), 0.0)


def cari_mahasiswa(data, nim):
    """Cari mahasiswa di list berdasarkan NIM. Return dict atau None."""
    for m in data:
        if m.get("nim") == nim:
            return m
    return None


def cari_matakuliah(data, kode):
    """Cari mata kuliah di list berdasarkan kode. Return dict atau None."""
    for m in data:
        if m.get("kode") == kode:
            return m
    return None


def hitung_ipk(nim):
    """Hitung IPK mahasiswa. Return (ipk, total_sks, rincian_list)."""
    data_nilai = penyimpanan.muat("data/nilai.json")
    data_mk = penyimpanan.muat("data/matakuliah.json")
    rincian, total_bobot_sks, total_sks = [], 0.0, 0
    for n in data_nilai:
        if n.get("nim") != nim:
            continue
        mk = cari_matakuliah(data_mk, n.get("kode"))
        if not mk:
            continue
        sks = mk.get("sks", 0)
        if sks <= 0:
            continue
        huruf = nilai_ke_huruf(n.get("nilai"))
        bobot = huruf_ke_bobot(huruf)
        rincian.append({"kode": n["kode"], "nama": mk["nama"], "sks": sks,
                       "nilai": n["nilai"], "huruf": huruf, "bobot": bobot})
        total_bobot_sks += bobot * sks
        total_sks += sks
    if total_sks == 0:
        return 0.0, 0, rincian
    return round(total_bobot_sks / total_sks, 2), total_sks, rincian


def menu_input_nilai():
    """Menu 3: Input nilai. Tanpa PIN (diurus main.py). Ulang sampai user pilih n."""
    data_mhs = penyimpanan.muat("data/mahasiswa.json")
    data_mk = penyimpanan.muat("data/matakuliah.json")
    if not data_mhs or not data_mk:
        print(ui.error("Belum ada data mahasiswa/mata kuliah."))
        return
    while True:
        print(ui.sub_header("INPUT NILAI"))
        print(ui.info("Daftar Mata Kuliah:"))
        for mk in data_mk:
            print(f"  {ui.CYAN}{mk['kode']}{ui.RESET} - {mk['nama']} ({mk['sks']} SKS)")
        nim = None
        for _ in range(3):
            nim = input(ui.input_prompt("Masukkan NIM")).strip()
            ok, msg = validasi.validasi_nim(nim)
            if not ok:
                print(ui.warning(msg))
                continue
            if not cari_mahasiswa(data_mhs, nim):
                print(ui.warning("NIM tidak ditemukan."))
                continue
            break
        else:
            print(ui.error("Batal: NIM salah 3 kali."))
            return
        kode = None
        for _ in range(3):
            kode = input(ui.input_prompt("Masukkan Kode MK")).strip()
            ok, msg, kode_up = validasi.validasi_kode_mk(kode)
            if not ok:
                print(ui.warning(msg))
                continue
            if not cari_matakuliah(data_mk, kode_up):
                print(ui.warning("Kode MK tidak ditemukan."))
                continue
            break
        else:
            print(ui.error("Batal: Kode MK salah 3 kali."))
            return
        nilai = validasi.input_angka_aman("Masukkan Nilai (0-100)", float, 0, 100)
        if nilai is None:
            return
        data_nilai = penyimpanan.muat("data/nilai.json")
        ditemukan = False
        for n in data_nilai:
            if n.get("nim") == nim and n.get("kode") == kode_up:
                n["nilai"] = nilai
                ditemukan = True
                break
        if not ditemukan:
            data_nilai.append({"nim": nim, "kode": kode_up, "nilai": nilai})
        penyimpanan.simpan("data/nilai.json", data_nilai)
        huruf = nilai_ke_huruf(nilai)
        print(ui.success(f"Nilai tersimpan: {nilai} ({huruf})"))
        if input(ui.confirm_prompt("Input nilai lagi?")).strip().lower() != "y":
            break


def menu_lihat_ipk():
    """Menu 4: Lihat IPK. Bebas PIN."""
    data_mhs = penyimpanan.muat("data/mahasiswa.json")
    if not data_mhs:
        print(ui.error("Belum ada data mahasiswa."))
        return
    print(ui.sub_header("LIHAT IPK"))
    nim = input(ui.input_prompt("Masukkan NIM")).strip()
    mhs = cari_mahasiswa(data_mhs, nim)
    if not mhs:
        print(ui.warning("NIM tidak ditemukan."))
        return
    ipk, total_sks, rincian = hitung_ipk(nim)
    if not rincian:
        print(ui.info("Belum ada nilai."))
        return
    print(ui.info(f"Mahasiswa: {mhs['nama']} ({nim})"))
    print(ui.info(f"Prodi: {mhs['prodi']} | Semester: {mhs['semester']}"))
    rows = [[r["kode"], r["nama"], str(r["sks"]), f"{r['nilai']:.1f}", r["huruf"], f"{r['bobot']:.1f}"] for r in rincian]
    print(ui.draw_table(["Kode", "Mata Kuliah", "SKS", "Nilai", "Huruf", "Bobot"], rows))
    print(ui.success(f"Total SKS: {total_sks} | IPK: {ipk:.2f}"))