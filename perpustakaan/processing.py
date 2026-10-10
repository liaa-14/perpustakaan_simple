from perpustakaan.validasi import DataError, cek_kosong, cek_angka

#untuk menghitung total dari beberapa angka
def hitung_total(*angka):
    total = 0
    for a in angka:
        total += a
    return total

#untuk membuat objek buku dari data
def buat_buku(kode, judul, **info):
    for nama in info:
        if nama not in ("penulis", "tahun", "stok"):
            raise DataError("atribut '" + nama + "' tidak dikenal")

    penulis = info.get("penulis", "Anonim")
    tahun = info.get("tahun", 2000)
    stok = info.get("stok", 1)

    return Buku(cek_kosong(kode, "Kode"),
                cek_kosong(judul, "Judul"),
                cek_kosong(penulis, "Penulis"),
                cek_angka(tahun, "Tahun"),
                cek_angka(stok, "Stok"))

#untuk membuat objek perpustakaan dari daftar buku
class Buku:
    def __init__(self, kode, judul, penulis, tahun, stok):
        self.kode = kode
        self.judul = judul
        self.penulis = penulis
        self.tahun = tahun
        self.stok = stok

    def tampil(self):
        print(self.kode, "|", self.judul, "|", self.penulis, "|", self.tahun, "| stok:", self.stok)

    def pinjam(self):
        if self.stok <= 0:
            raise ValueError("Stok buku '" + self.judul + "' sudah habis")
        self.stok -= 1

    def kembalikan(self):
        self.stok += 1

    def ke_baris(self):
        return f"{self.kode},{self.judul},{self.penulis},{self.tahun},{self.stok}"

class Perpustakaan:
    def __init__(self, daftar):  #untuk membuat objek perpustakaan dari daftar buku
        self.daftar = daftar

    def cari_kode(self, kode):  #untuk mencari buku berdasarkan kode
        for buku in self.daftar:
            if buku.kode == kode:
                return buku
        return None

    def cari_judul(self, kata):   #untuk mencari buku berdasarkan kata kunci judul
        return list(filter(lambda b: kata.lower() in b.judul.lower(), self.daftar))

    def urutkan(self, berdasarkan="judul"):    #untuk mengurutkan daftar buku berdasarkan judul, tahun, atau stok
        if berdasarkan == "tahun":
            return sorted(self.daftar, key=lambda b: b.tahun)
        elif berdasarkan == "stok":
            return sorted(self.daftar, key=lambda b: b.stok)
        else:
            return sorted(self.daftar, key=lambda b: b.judul.lower())

    def total_stok(self):    #untuk menghitung total stok semua buku
        semua_stok = [b.stok for b in self.daftar]
        return hitung_total(*semua_stok)

    def buat_laporan(self):   #untu
        if len(self.daftar) == 0:
            return "Belum ada data buku."
        semua_tahun = [b.tahun for b in self.daftar]
        rata_tahun = hitung_total(*semua_tahun) / len(self.daftar)
        terbanyak = max(self.daftar, key=lambda b: b.stok)
        teks = "=== LAPORAN PERPUSTAKAAN ===\n"
        teks += f"Jumlah judul     : {len(self.daftar)}\n"
        teks += f"Total stok       : {self.total_stok()}\n"
        teks += f"Rata-rata tahun  : {round(rata_tahun)}\n"
        teks += f"Stok terbanyak   : {terbanyak.judul}\n"
        return teks
