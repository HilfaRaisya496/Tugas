import tkinter as tk
from tkinter import ttk, messagebox
import csv
from collections import deque

# Struktur Data
antrian = deque()
pasien_map = {}  # HashMap: nama → data

CSV_FILE = "pasien.csv"
HEADER = ['id', 'nama', 'keluhan']

def baca_csv():
    antrian.clear()
    pasien_map.clear()
    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                antrian.append(row)
                pasien_map[row['nama'].lower()] = row
    except FileNotFoundError:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADER)
            writer.writeheader()

def simpan_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        for p in antrian:
            writer.writerow(p)

def tambah_pasien():
    id = entry_id.get()
    nama = entry_nama.get()
    keluhan = entry_keluhan.get()

    if not id or not nama:
        messagebox.showwarning("Wajib diisi", "ID dan Nama tidak boleh kosong!")
        return

    data = {'id': id, 'nama': nama, 'keluhan': keluhan}
    antrian.append(data)
    pasien_map[nama.lower()] = data
    update_tabel()
    simpan_csv()
    bersihkan_input()

def cari_pasien():
    nama = entry_cari.get().lower()
    if nama in pasien_map:
        p = pasien_map[nama]
        messagebox.showinfo("Pasien Ditemukan", f"{p['id']} - {p['nama']} - {p['keluhan']}")
    else:
        messagebox.showinfo("Tidak Ditemukan", "Pasien tidak ada dalam data.")

def panggil_pasien():
    if antrian:
        pasien = antrian.popleft()
        pasien_map.pop(pasien['nama'].lower(), None)
        messagebox.showinfo("Panggilan", f"Memanggil pasien: {pasien['nama']}")
        update_tabel()
        simpan_csv()
    else:
        messagebox.showinfo("Kosong", "Tidak ada pasien dalam antrian.")

def update_tabel():
    for item in tree.get_children():
        tree.delete(item)
    for p in antrian:
        tree.insert('', tk.END, values=[p['id'], p['nama'], p['keluhan']])

def bersihkan_input():
    entry_id.delete(0, tk.END)
    entry_nama.delete(0, tk.END)
    entry_keluhan.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Antrian Klinik - GUI + Queue + HashMap")

# Form
tk.Label(root, text="ID").grid(row=0, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

tk.Label(root, text="Nama").grid(row=1, column=0)
entry_nama = tk.Entry(root)
entry_nama.grid(row=1, column=1)

tk.Label(root, text="Keluhan").grid(row=2, column=0)
entry_keluhan = tk.Entry(root)
entry_keluhan.grid(row=2, column=1)

tk.Button(root, text="Tambah ke Antrian", command=tambah_pasien).grid(row=3, column=0, columnspan=2, pady=5)

tk.Label(root, text="Cari Pasien (Nama)").grid(row=4, column=0)
entry_cari = tk.Entry(root)
entry_cari.grid(row=4, column=1)
tk.Button(root, text="Cari", command=cari_pasien).grid(row=4, column=2)

tk.Button(root, text="Panggil Pasien Dari Antrian Pertama", command=panggil_pasien).grid(row=5, column=0, columnspan=3, pady=5)

# Tabel
tree = ttk.Treeview(root, columns=HEADER, show='headings')
for col in HEADER:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.grid(row=6, column=0, columnspan=3, pady=10)

baca_csv()
update_tabel()
root.mainloop()




