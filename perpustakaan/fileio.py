from perpustakaan.processing import Buku
from perpustakaan.validasi import DataError, cek_baris, cek_kosong, cek_angka

def baris_ke_buku(baris):   #untuk mengubah baris teks menjadi objek buku, memeriksa kesalahan data
    kode, judul, penulis, tahun, stok = cek_baris(baris)
    return Buku(cek_kosong(kode, "Kode"),
                cek_kosong(judul, "Judul"),
                cek_kosong(penulis, "Penulis"),
                cek_angka(tahun, "Tahun"),
                cek_angka(stok, "Stok"))
 
def buat_file(nama_file):   #untuk membuat file data awal jika belum ada
    try:
        with open(nama_file, "x", encoding="utf-8") as file:
            file.write("B01,Python Dasar,Budi,2020,3\n")
            file.write("B02,Basis Data,Sari,2018,2\n")
            file.write("B03,Algoritma,Andi,2022,1\n")
        print("File data berhasil dibuat")
    except FileExistsError:
        print("File data sudah ada, tidak dibuat ulang")

def tambah_buku(nama_file, buku):      #untuk menambahkan buku ke file data
    with open(nama_file, "a", encoding="utf-8") as file:
        file.write(buku.ke_baris() + "\n")

def baca_buku(nama_file):  #untuk membaca daftar buku dari file, mengabaikan baris yang rusak
    daftar = []
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            for baris in file:
                if baris.strip() == "": 
                    continue
                try:
                    daftar.append(baris_ke_buku(baris))
                except DataError as e:
                    print("Baris dilewati ->", baris.strip(), "|", e)
    except FileNotFoundError:
        print("File '" + nama_file + "' belum ada. Pilih menu 1 dulu untuk membuatnya.")
    return daftar


def simpan_buku(nama_file, daftar):   #untuk menyimpan daftar buku ke file, tanpa menghapus baris yang rusak
    baris_rusak = []
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            for baris in file:
                if baris.strip() == "":
                    continue
                try:
                    baris_ke_buku(baris)
                except DataError:
                    baris_rusak.append(baris.strip())
    except FileNotFoundError:
        pass   

    with open(nama_file, "w", encoding="utf-8") as file:
        for buku in daftar:
            file.write(buku.ke_baris() + "\n")
        for baris in baris_rusak:
            file.write(baris + "\n")

def tulis_laporan(nama_file, teks):    #untuk menulis laporan ke file
    with open(nama_file, "w", encoding="utf-8") as file:
        file.write(teks)