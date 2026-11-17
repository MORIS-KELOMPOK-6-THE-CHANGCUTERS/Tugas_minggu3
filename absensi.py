"""
Modul absensi: input absensi dan rekap kehadiran (Menu 5).
"""

import penyimpanan
import validasi
from nilai import cari_mahasiswa, cari_matakuliah
import ui


def absensi_sudah_ada(data_absensi, kode, tanggal):
    """Cek apakah absensi untuk kode MK dan tanggal sudah ada."""
    for a in data_absensi:
        if a.get("kode") == kode and a.get("tanggal") == tanggal:
            return True
    return False


def hitung_kehadiran(kode):
    """Hitung kehadiran per mhs. Return [{"nim","nama","hadir","total","persen"},...]."""
    data_absensi = penyimpanan.muat("data/absensi.json")
    data_mhs = penyimpanan.muat("data/mahasiswa.json")
    pertemuan = [a for a in data_absensi if a.get("kode") == kode]
    if not pertemuan:
        return []
    rincian = []
    for mhs in data_mhs:
        nim, hadir, total = mhs.get("nim"), 0, 0
        for p in pertemuan:
            status = p.get("status", {}).get(nim)
            if status is not None:
                total += 1
                if status == "H":
                    hadir += 1
        persen = round(hadir / total * 100, 1) if total > 0 else 0.0
        rincian.append({"nim": nim, "nama": mhs.get("nama", ""), "hadir": hadir,
                       "total": total, "persen": persen})
    return rincian


def input_absensi():
    """Input absensi. Kode MK (3x), tanggal (3x), tolak ganda, status per mhs (3x)."""
    data_mk = penyimpanan.muat("data/matakuliah.json")
    data_mhs = penyimpanan.muat("data/mahasiswa.json")
    if not data_mk or not data_mhs:
        print(ui.error("Belum ada data MK/mahasiswa."))
        return
    print(ui.sub_header("INPUT ABSENSI"))
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
    tanggal = None
    for _ in range(3):
        tanggal = input(ui.input_prompt("Masukkan Tanggal (YYYY-MM-DD)")).strip()
        ok, msg = validasi.validasi_tanggal(tanggal)
        if not ok:
            print(ui.warning(msg))
            continue
        break
    else:
        print(ui.error("Batal: Tanggal salah 3 kali."))
        return
    data_absensi = penyimpanan.muat("data/absensi.json")
    if absensi_sudah_ada(data_absensi, kode_up, tanggal):
        print(ui.warning("Absensi ganda ditolak."))
        return
    status_dict = {}
    for mhs in data_mhs:
        nim, nama = mhs.get("nim"), mhs.get("nama", "")
        status = None
        for _ in range(3):
            s = input(ui.input_prompt(f"Status {nim} - {nama} (H/I/S/A)")).strip()
            ok, msg, s_up = validasi.validasi_status_absensi(s)
            if not ok:
                print(ui.warning(msg))
                continue
            status = s_up
            break
        else:
            print(ui.error(f"Batal: Status {nim} salah 3x. Input dibatalkan."))
            return
        status_dict[nim] = status
    data_absensi.append({"kode": kode_up, "tanggal": tanggal, "status": status_dict})
    penyimpanan.simpan("data/absensi.json", data_absensi)
    print(ui.success("Absensi tersimpan."))


def rekap_absensi():
    """Rekap kehadiran. Tabel + PERINGATAN < 75%."""
    data_mk = penyimpanan.muat("data/matakuliah.json")
    if not data_mk:
        print(ui.error("Belum ada data MK."))
        return
    print(ui.sub_header("REKAP KEHADIRAN"))
    kode = input(ui.input_prompt("Masukkan Kode MK")).strip()
    ok, msg, kode_up = validasi.validasi_kode_mk(kode)
    if not ok:
        print(ui.warning(msg))
        return
    if not cari_matakuliah(data_mk, kode_up):
        print(ui.warning("Kode MK tidak ditemukan."))
        return
    rincian = hitung_kehadiran(kode_up)
    if not rincian:
        print(ui.info("Belum ada absensi."))
        return
    rows = []
    for r in rincian:
        if r["total"] == 0:
            persen_str = "-"
        else:
            persen_str = f"{r['persen']:.1f}%"
        rows.append([r["nim"], r["nama"], str(r["hadir"]), str(r["total"]), persen_str])
    
    def row_color(idx):
        r = rincian[idx]
        return ui.RED if r["total"] > 0 and r["persen"] < 75 else ""
    
    print(ui.draw_table(["NIM", "Nama", "Hadir", "Total", "%"], rows, row_color))
    
    # Print warnings after table
    for r in rincian:
        if r["total"] > 0 and r["persen"] < 75:
            print(f"{ui.RED}  ⚠ {r['nim']} - {r['nama']}: {r['persen']:.1f}% (Di bawah 75%){ui.RESET}")