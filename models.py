"""
Modul models: definisi kelas Mahasiswa dan MataKuliah dengan serialisasi.
"""


class Mahasiswa:
    """
    Kelas representasi data Mahasiswa.
    Atribut: nim (str), nama (str), prodi (str), semester (int)
    """

    def __init__(self, nim, nama, prodi, semester):
        """
        Inisialisasi objek Mahasiswa.
        Input: nim (string), nama (string), prodi (string), semester (int)
        Output: tidak ada (objek dibuat)
        """
        self.nim = str(nim).strip()
        self.nama = str(nama).strip()
        self.prodi = str(prodi).strip()
        self.semester = int(semester)

    def to_dict(self):
        """
        Mengubah objek Mahasiswa menjadi dictionary untuk disimpan ke JSON.
        Input: tidak ada
        Output: dict dengan keys nim, nama, prodi, semester
        """
        return {
            "nim": self.nim,
            "nama": self.nama,
            "prodi": self.prodi,
            "semester": self.semester
        }

    @classmethod
    def dari_dict(cls, data):
        """
        Membuat objek Mahasiswa dari dictionary (misal hasil load JSON).
        Input: data (dict) dengan keys nim, nama, prodi, semester
        Output: instance Mahasiswa
        """
        return cls(
            nim=data.get("nim", ""),
            nama=data.get("nama", ""),
            prodi=data.get("prodi", ""),
            semester=data.get("semester", 1)
        )

    def __repr__(self):
        """Representasi string untuk debugging."""
        return f"Mahasiswa(nim={self.nim}, nama={self.nama}, prodi={self.prodi}, semester={self.semester})"


class MataKuliah:
    """
    Kelas representasi data Mata Kuliah.
    Atribut: kode (str), nama (str), sks (int), dosen (str)
    """

    def __init__(self, kode, nama, sks, dosen):
        """
        Inisialisasi objek MataKuliah.
        Input: kode (string), nama (string), sks (int), dosen (string)
        Output: tidak ada (objek dibuat)
        """
        self.kode = str(kode).strip().upper()
        self.nama = str(nama).strip()
        self.sks = int(sks)
        self.dosen = str(dosen).strip()

    def to_dict(self):
        """
        Mengubah objek MataKuliah menjadi dictionary untuk disimpan ke JSON.
        Input: tidak ada
        Output: dict dengan keys kode, nama, sks, dosen
        """
        return {
            "kode": self.kode,
            "nama": self.nama,
            "sks": self.sks,
            "dosen": self.dosen
        }

    @classmethod
    def dari_dict(cls, data):
        """
        Membuat objek MataKuliah dari dictionary (misal hasil load JSON).
        Input: data (dict) dengan keys kode, nama, sks, dosen
        Output: instance MataKuliah
        """
        return cls(
            kode=data.get("kode", ""),
            nama=data.get("nama", ""),
            sks=data.get("sks", 0),
            dosen=data.get("dosen", "")
        )

    def __repr__(self):
        """Representasi string untuk debugging."""
        return f"MataKuliah(kode={self.kode}, nama={self.nama}, sks={self.sks}, dosen={self.dosen})"