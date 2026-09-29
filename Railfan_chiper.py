import tkinter as tk
from tkinter import messagebox

# ====== TEMA: BIRU LANGIT ======
WARNA, GELAP, MUDA, BG, BORDER = "#0284C7", "#0369A1", "#E0F2FE", "#F0F9FF", "#BAE6FD"
FONT = "Segoe UI"


def pola_baris(panjang, rails):
    """Nomor baris untuk tiap posisi karakter (zig-zag)."""
    pola = []
    baris, arah = 0, 1
    for _ in range(panjang):
        pola.append(baris)
        if rails > 1:
            if baris == 0:
                arah = 1
            elif baris == rails - 1:
                arah = -1
            baris += arah
    return pola


def enkripsi(text, rails):
    pola = pola_baris(len(text), rails)
    urutan = sorted(range(len(text)), key=lambda i: pola[i])
    return "".join(text[i] for i in urutan)


def dekripsi(text, rails):
    pola = pola_baris(len(text), rails)
    urutan = sorted(range(len(text)), key=lambda i: pola[i])
    hasil = [""] * len(text)
    for posisi, idx in enumerate(urutan):
        hasil[idx] = text[posisi]
    return "".join(hasil)


def gambar_zigzag(teks, rails):
    teks = teks.replace("\n", " ")[:30]
    pola = pola_baris(len(teks), rails)
    baris = []
    for r in range(rails):
        baris.append(" ".join(teks[i] if pola[i] == r else "." for i in range(len(teks))))
    return "\n".join(baris)


def tombol(parent, teks, cmd, bg, fg, hover):
    b = tk.Label(parent, text=teks, bg=bg, fg=fg, font=(FONT, 10, "bold"),
                 padx=20, pady=8, cursor="hand2")
    b.bind("<Button-1>", lambda e: cmd())
    b.bind("<Enter>", lambda e: b.config(bg=hover))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def kotak_teks(parent, tinggi):
    return tk.Text(parent, height=tinggi, width=54, font=("Consolas", 11), wrap="word",
                   relief="flat", bg="#F7FCFF", padx=8, pady=8,
                   highlightthickness=2, highlightbackground=BORDER, highlightcolor=WARNA)


def label(parent, teks):
    return tk.Label(parent, text=teks, bg="white", fg=GELAP, font=(FONT, 10, "bold"))


def proses(decrypt):
    try:
        rails = int(entry_key.get())
        if rails < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Jumlah rail harus angka >= 1!")
        return
    teks = input_text.get("1.0", tk.END).strip()
    if not teks:
        messagebox.showwarning("Peringatan", "Teks masih kosong!")
        return
    hasil = (dekripsi if decrypt else enkripsi)(teks, rails)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, hasil)

    # Panel visual khas Rail Fence: pola zig-zag dari teks asli
    zigzag.config(text=gambar_zigzag(hasil if decrypt else teks, rails))
    status.config(text="Dekripsi berhasil" if decrypt else "Enkripsi berhasil")


def salin():
    hasil = output_text.get("1.0", tk.END).strip()
    if hasil:
        root.clipboard_clear()
        root.clipboard_append(hasil)
        status.config(text="Hasil disalin ke clipboard")


root = tk.Tk()
root.title("Rail Fence Cipher")
root.configure(bg=BG)
root.resizable(False, False)

# Header
header = tk.Frame(root, bg=WARNA)
header.pack(fill="x")
tk.Label(header, text="RAIL FENCE CIPHER", font=(FONT, 22, "bold"), bg=WARNA, fg="white").pack(pady=(18, 0))
tk.Label(header, text="Cipher transposisi  |  huruf ditulis zig-zag pada beberapa rail",
         font=(FONT, 10), bg=WARNA, fg=MUDA).pack(pady=(2, 18))

# Kartu utama
card = tk.Frame(root, bg="white", padx=22, pady=16)
card.pack(padx=18, pady=18)

label(card, "Teks").pack(anchor="w")
input_text = kotak_teks(card, 5)
input_text.pack(pady=(4, 10))

label(card, "Jumlah rail (angka)").pack(anchor="w")
entry_key = tk.Entry(card, font=(FONT, 12), width=8, relief="flat", bg="#F7FCFF",
                     highlightthickness=2, highlightbackground=BORDER, highlightcolor=WARNA)
entry_key.insert(0, "3")
entry_key.pack(anchor="w", pady=(4, 10), ipady=4)

frame = tk.Frame(card, bg="white")
frame.pack(pady=(0, 10))
tombol(frame, "Enkripsi", lambda: proses(False), WARNA, "white", GELAP).pack(side="left", padx=5)
tombol(frame, "Dekripsi", lambda: proses(True), MUDA, GELAP, "#BAE6FD").pack(side="left", padx=5)

zigzag = tk.Label(card, text="Pola zig-zag akan tampil di sini setelah proses",
                  bg=MUDA, fg=GELAP, font=("Consolas", 9), justify="left",
                  anchor="w", padx=8, pady=6)
zigzag.pack(fill="x", pady=(0, 10))

label(card, "Hasil").pack(anchor="w")
output_text = kotak_teks(card, 5)
output_text.pack(pady=(4, 8))

bawah = tk.Frame(card, bg="white")
bawah.pack(fill="x")
status = tk.Label(bawah, text="", bg="white", fg="#64748B", font=(FONT, 9))
status.pack(side="left")
tombol(bawah, "Salin Hasil", salin, "white", WARNA, MUDA).pack(side="right")

root.mainloop()