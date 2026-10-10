import os
import tempfile
import unittest
from perpustakaan import fileio, processing, validasi

class TestPerpustakaan(unittest.TestCase):  #untuk menguji fungsi-fungsi perpustakaan

    def setUp(self):   #untuk menyiapkan data awal sebelum setiap pengujian
        self.perpus = processing.Perpustakaan([
            processing.buat_buku("B01", "Python", penulis="Budi", tahun=2020, stok=2),
            processing.buat_buku("B02", "Basis Data", penulis="Sari", tahun=2018, stok=1),
        ])

    def test_cek_angka_benar(self):  #untuk menguji fungsi cek_angka dengan input yang benar
        self.assertEqual(validasi.cek_angka("10", "Stok"), 10)

    def test_cek_angka_negatif(self):  #untuk menguji fungsi cek_angka dengan input negatif
        with self.assertRaises(validasi.DataError):
            validasi.cek_angka("-1", "Stok")

    def test_cek_angka_huruf(self):   #untuk menguji fungsi cek_angka dengan input huruf
        with self.assertRaises(validasi.DataError):
            validasi.cek_angka("abc", "Stok")

    def test_hitung_total(self):   #untuk menguji fungsi hitung_total dengan beberapa angka
        self.assertEqual(processing.hitung_total(1, 2, 3), 6)

    def test_pinjam_stok_berkurang(self):   #untuk menguji fungsi pinjam mengurangi stok buku
        buku = self.perpus.cari_kode("B01")
        buku.pinjam()
        self.assertEqual(buku.stok, 1)

    def test_pinjam_stok_habis(self):   #untuk menguji fungsi pinjam ketika stok buku habis
        buku = self.perpus.cari_kode("B02")
        buku.pinjam()
        with self.assertRaises(ValueError):
            buku.pinjam()

    def test_urutkan_tahun(self):   #untuk menguji fungsi urutkan berdasarkan tahun
        hasil = [b.tahun for b in self.perpus.urutkan(berdasarkan="tahun")]
        self.assertEqual(hasil, [2018, 2020])

    def test_file_tidak_ada(self):  #untuk menguji fungsi baca_buku ketika file tidak ada
        self.assertEqual(fileio.baca_buku("file_tidak_ada.txt"), [])

    def test_buat_buku_stok_negatif(self):   #untuk menguji fungsi buat_buku dengan stok negatif
        with self.assertRaises(validasi.DataError):
            processing.buat_buku("B03", "Tes", stok=-3)

    def test_buat_buku_atribut_salah_ketik(self):   #untuk menguji fungsi buat_buku dengan atribut salah ketik
        with self.assertRaises(validasi.DataError):
            processing.buat_buku("B03", "Tes", pengarang="X")

    def test_judul_mengandung_koma(self):  #untuk menguji fungsi buat_buku dengan judul yang mengandung koma
        with self.assertRaises(validasi.DataError):
            processing.buat_buku("B03", "Struktur Data, Edisi 2")

    def test_simpan_tidak_menghapus_baris_rusak(self):  #untuk menguji fungsi simpan_buku agar tidak menghapus baris yang rusak
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

if __name__ == "__main__":  #untuk menjalankan pengujian jika file ini dijalankan langsung
    unittest.main()