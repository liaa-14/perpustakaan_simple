import os
import tempfile
import unittest
from perpustakaan import fileio, processing, validasi

class TestPerpustakaan(unittest.TestCase):

    def setUp(self):
        self.perpus = processing.Perpustakaan([
            processing.buat_buku("B01", "Python", penulis="Budi", tahun=2020, stok=2),
            processing.buat_buku("B02", "Basis Data", penulis="Sari", tahun=2018, stok=1),
        ])

    def test_cek_angka_benar(self):
        self.assertEqual(validasi.cek_angka("10", "Stok"), 10)

    def test_cek_angka_negatif(self):
        with self.assertRaises(validasi.DataError):
            validasi.cek_angka("-1", "Stok")

    def test_cek_angka_huruf(self):
        with self.assertRaises(validasi.DataError):
            validasi.cek_angka("abc", "Stok")

    def test_hitung_total(self):
        self.assertEqual(processing.hitung_total(1, 2, 3), 6)

    def test_pinjam_stok_berkurang(self):
        buku = self.perpus.cari_kode("B01")
        buku.pinjam()
        self.assertEqual(buku.stok, 1)

    def test_pinjam_stok_habis(self):
        buku = self.perpus.cari_kode("B02")
        buku.pinjam()
        with self.assertRaises(ValueError):
            buku.pinjam()

    def test_urutkan_tahun(self):
        hasil = [b.tahun for b in self.perpus.urutkan(berdasarkan="tahun")]
        self.assertEqual(hasil, [2018, 2020])

    def test_file_tidak_ada(self):
        self.assertEqual(fileio.baca_buku("file_tidak_ada.txt"), [])

    def test_buat_buku_stok_negatif(self):
        with self.assertRaises(validasi.DataError):
            processing.buat_buku("B03", "Tes", stok=-3)

    def test_buat_buku_atribut_salah_ketik(self):
        with self.assertRaises(validasi.DataError):
            processing.buat_buku("B03", "Tes", pengarang="X")

    def test_judul_mengandung_koma(self):
        with self.assertRaises(validasi.DataError):
            processing.buat_buku("B03", "Struktur Data, Edisi 2")

    def test_simpan_tidak_menghapus_baris_rusak(self):
        folder = tempfile.mkdtemp()
        nama_file = os.path.join(folder, "uji.txt")
        with open(nama_file, "w", encoding="utf-8") as file:
            file.write("B01,Python,Budi,2020,2\n")
            file.write("\n")
            file.write("B02,Rusak,Sari,abc,1\n")
        daftar = fileio.baca_buku(nama_file)
        self.assertEqual(len(daftar), 1)         
        fileio.simpan_buku(nama_file, daftar)
        with open(nama_file, "r", encoding="utf-8") as file:
            isi = file.read()
        self.assertIn("B02,Rusak,Sari,abc,1", isi)
        os.remove(nama_file)
        os.rmdir(folder)

if __name__ == "__main__":
    unittest.main()