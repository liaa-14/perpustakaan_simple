class DataError(Exception):
    pass
 
def cek_kosong(teks, nama):
    teks = teks.strip()
    if teks == "":
        raise DataError(nama + " tidak boleh kosong")
    return teks
 
def cek_angka(teks, nama):
    try:
        angka = int(teks)
    except ValueError:
        raise DataError(nama + " harus berupa angka")
    if angka < 0:
        raise DataError(nama + " tidak boleh negatif")
    return angka            
 
def cek_baris(baris):
    assert isinstance(baris, str), "baris harus berupa string"
    bagian = baris.strip().split(",")
    if len(bagian) != 5:
        raise DataError("jumlah kolom harus 5")
    return bagian
 
if __name__ == "__main__":
    print(cek_angka("10", "Stok"))
    try:
        cek_angka("abc", "Stok")
    except DataError as e:
        print("Error:", e)
    try:
        cek_angka("-5", "Stok")
    except DataError as e:
        print("Error:", e)
