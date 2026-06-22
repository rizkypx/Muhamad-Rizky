import csv
import os
from datetime import datetime

CSV_FILE = 'data_parkir.csv'

HEADERS = [
    'plat_nomor',
    'jenis_kendaraan',
    'waktu_masuk',
    'waktu_keluar',
    'durasi',
    'total_bayar',
    'status'
]

TARIF_MOBIL_PER_JAM = 5000
TARIF_MOTOR_PER_JAM = 2000


# =========================
# INIT CSV
# =========================
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)


# =========================
# LOAD DATA
# =========================
def load_data():
    init_csv()
    data = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


# =========================
# SAVE DATA
# =========================
def save_data(data):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(data)


# =========================
# 1. MASUK PARKIR
# =========================
def masuk_parkir():
    print("\n--- MASUK PARKIR ---")
    plat = input("Plat Nomor: ").upper()
    jenis = input("Jenis (Mobil/Motor): ").capitalize()

    if jenis not in ["Mobil", "Motor"]:
        print("❌ Jenis salah!")
        return

    data = load_data()

    for d in data:
        if d['plat_nomor'] == plat and d['status'] == 'PARKIR':
            print("❌ Kendaraan masih di parkir!")
            return

    waktu = datetime.now().strftime("%Y-%m-%d %H:%M")

    data.append({
        'plat_nomor': plat,
        'jenis_kendaraan': jenis,
        'waktu_masuk': waktu,
        'waktu_keluar': '-',
        'durasi': '-',
        'total_bayar': '0',
        'status': 'PARKIR'
    })

    save_data(data)
    print("✅ Kendaraan masuk parkir")


# =========================
# 2. LIHAT PARKIR
# =========================
def lihat_parkir():
    print("\n--- KENDARAAN PARKIR ---")
    data = load_data()

    for d in data:
        if d['status'] == 'PARKIR':
            print(d['plat_nomor'], "|", d['jenis_kendaraan'], "|", d['waktu_masuk'])


# =========================
# 3. KELUAR & BAYAR
# =========================
def keluar_parkir():
    print("\n--- KELUAR PARKIR ---")
    plat = input("Plat Nomor: ").upper()

    data = load_data()
    found = False

    for d in data:
        if d['plat_nomor'] == plat and d['status'] == 'PARKIR':
            found = True

            masuk = datetime.strptime(d['waktu_masuk'], "%Y-%m-%d %H:%M")
            keluar = datetime.now()

            lama = keluar - masuk
            jam = int(lama.total_seconds() // 3600)
            if lama.total_seconds() % 3600 > 0:
                jam += 1

            tarif = TARIF_MOBIL_PER_JAM if d['jenis_kendaraan'] == 'Mobil' else TARIF_MOTOR_PER_JAM
            total = jam * tarif

            d['waktu_keluar'] = keluar.strftime("%Y-%m-%d %H:%M")
            d['durasi'] = f"{jam} jam"
            d['total_bayar'] = str(total)
            d['status'] = 'KELUAR'

            print(f"TOTAL BAYAR: Rp {total}")
            break

    if not found:
        print("❌ Kendaraan tidak ditemukan")

    save_data(data)


# =========================
# 4. HISTORI
# =========================
def histori():
    print("\n--- HISTORI ---")
    data = load_data()

    for d in data:
        print(d)


# =========================
# MENU
# =========================
def menu():
    init_csv()

    while True:
        print("\n===== SMART PARKING =====")
        print("1. Masuk Parkir")
        print("2. Lihat Parkir")
        print("3. Keluar Parkir")
        print("4. Histori")
        print("5. Keluar")

        pilih = input("Pilih: ")

        if pilih == '1':
            masuk_parkir()
        elif pilih == '2':
            lihat_parkir()
        elif pilih == '3':
            keluar_parkir()
        elif pilih == '4':
            histori()
        elif pilih == '5':
            break
        else:
            print("❌ Salah menu")


if __name__ == "__main__":
    menu()