from perpustakaan import fileio, processing, validasi

FILE_DATA = "data_buku.txt"
FILE_LAPORAN = "laporan.txt"

def tampil_menu():
    print("\n===== PERPUSTAKAAN =====")
    print("1. Buat file data")
    print("2. Tambah buku")
    print("3. Lihat daftar buku")
    print("4. Cari buku")
    print("5. Pinjam buku")
    print("6. Kembalikan buku")
    print("7. Buat laporan")
    print("0. Keluar")

def jeda():
    input("\nTekan Enter untuk kembali ke menu...")

def menu_tambah():
    try:
        kode = validasi.cek_kosong(input("Kode    : "), "Kode")
        judul = validasi.cek_kosong(input("Judul   : "), "Judul")
        penulis = validasi.cek_kosong(input("Penulis : "), "Penulis")
        tahun = validasi.cek_angka(input("Tahun   : "), "Tahun")
        stok = validasi.cek_angka(input("Stok    : "), "Stok")
    except validasi.DataError as e:
        print("Input salah:", e)
        return

    perpus = processing.Perpustakaan(fileio.baca_buku(FILE_DATA))
    if perpus.cari_kode(kode) is not None:
        print("Kode sudah dipakai")
        return

    buku = processing.buat_buku(kode, judul, penulis=penulis, tahun=tahun, stok=stok)
    fileio.tambah_buku(FILE_DATA, buku)
    print("Buku berhasil ditambah")

def menu_lihat():
    perpus = processing.Perpustakaan(fileio.baca_buku(FILE_DATA))
    urutan = input("Urutkan berdasarkan (judul/tahun/stok): ")
    for buku in perpus.urutkan(berdasarkan=urutan):
        buku.tampil()

def menu_cari():
    perpus = processing.Perpustakaan(fileio.baca_buku(FILE_DATA))
    hasil = perpus.cari_judul(input("Kata kunci judul: "))
    if len(hasil) == 0:
        print("Buku tidak ditemukan")
    for buku in hasil:
        buku.tampil()


def menu_pinjam(pinjam=True):
    perpus = processing.Perpustakaan(fileio.baca_buku(FILE_DATA))
    buku = perpus.cari_kode(input("Kode buku: "))
    if buku is None:
        print("Kode buku tidak ditemukan")
        return
    try:
        if pinjam:
            buku.pinjam()
        else:
            buku.kembalikan()
        fileio.simpan_buku(FILE_DATA, perpus.daftar)
        print("Berhasil. Stok sekarang:", buku.stok)
    except ValueError as e:
        print("Gagal:", e)

def menu_laporan():
    perpus = processing.Perpustakaan(fileio.baca_buku(FILE_DATA))
    teks = perpus.buat_laporan()
    print(teks)
    fileio.tulis_laporan(FILE_LAPORAN, teks)
    print("Laporan disimpan di", FILE_LAPORAN)

def main():
    while True:
        tampil_menu()
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            fileio.buat_file(FILE_DATA)
        elif pilihan == "2":
            menu_tambah()
        elif pilihan == "3":
            menu_lihat()
        elif pilihan == "4":
            menu_cari()
        elif pilihan == "5":
            menu_pinjam(pinjam=True)
        elif pilihan == "6":
            menu_pinjam(pinjam=False)
        elif pilihan == "7":
            menu_laporan()
        elif pilihan == "0":
            print("Terima kasih")
            break
        else:
            print("Menu tidak ada")
        jeda()  
if __name__ == "__main__":
    main()
