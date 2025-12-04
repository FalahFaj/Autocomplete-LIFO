Berikut adalah isi file `README.md` yang telah diperbarui dengan penjelasan alur kerja (algoritma) yang mendetail. Penjelasan ini mencakup logika di balik Trie untuk Autocomplete dan Double Stack untuk Undo-Redo, cocok untuk laporan tugas akhir atau dokumentasi GitHub.

Silakan salin konten di bawah ini ke dalam file `README.md` Anda:

````markdown
# Pengembangan Modul Autocomplete dan Undo–Redo Terintegrasi

Proyek ini adalah implementasi struktur data **Trie (Prefix Tree)** dan **Double Stack** untuk membangun simulasi *Text Editor* sederhana. Proyek ini dibangun sepenuhnya dari nol (*scratch*) menggunakan Python tanpa bantuan library struktur data eksternal.

## 📂 Struktur Folder
```text
C:.
│   main.py               # Entry point aplikasi
│   README.md             # Dokumentasi alur sistem
│
├───examples
│       demo_cli.py       # Contoh antarmuka Command Line
│       demo_gui.py       # Contoh antarmuka GUI (Tkinter)
│
├───mesin
│   │   penggabung.py     # Engine utama (Integrasi Stack & Trie)
│   │
│   └───struktur
│           stack.py      # Implementasi Class Stack (LIFO)
│           trie.py       # Implementasi Class Trie (Prefix Tree)
│
└───tests
        test_stack.py     # Unit test untuk Stack
        test_trie.py      # Unit test untuk Trie
````

-----

## ⚙️ Alur Kerja Sistem (System Workflow)

Sistem ini menggabungkan dua mekanisme utama yang bekerja secara paralel ketika pengguna mengetik:

### 1\. Alur Autocomplete (Struktur Data Trie)

Fitur ini bertugas memberikan saran kata berdasarkan awalan (prefix) yang sedang diketik.

**Mekanisme:**

1.  **Input Prefix:** Pengguna mengetik karakter, misalnya `"str"`.
2.  **Navigasi Node:** Sistem menelusuri `Trie` dimulai dari *root*.
      * Cek apakah `root` punya anak `'s'`. Jika ya, pindah ke node `'s'`.
      * Dari node `'s'`, cek anak `'t'`. Jika ya, pindah ke node `'t'`.
      * Dari node `'t'`, cek anak `'r'`. Jika ya, pindah ke node `'r'`.
3.  **Pencarian (DFS):** Setelah sampai di node terakhir dari prefix (`'r'`), sistem melakukan *Depth First Search* (DFS) untuk menemukan semua node di bawahnya yang ditandai sebagai `is_end_of_word`.
4.  **Output:** Sistem mengembalikan daftar kata yang ditemukan (contoh: `"struktur"`, `"string"`, `"strategi"`).

**Ilustrasi Trie:**

```text
(root)
  |
  s -> t -> r -> i -> n -> g [end]
  |         |
  |         u -> k -> t -> u -> r [end]
  |
  a -> p -> e -> l [end]
```

### 2\. Alur Undo-Redo (Struktur Data Double Stack)

Fitur ini menangani riwayat perubahan teks menggunakan dua tumpukan: `Undo Stack` dan `Redo Stack`.

#### A. Saat Mengetik (Write Operation)

Setiap kali pengguna menambahkan teks baru:

1.  **Push ke Undo Stack:** Isi teks *sebelum* perubahan disimpan ke dalam `undo_stack`.
2.  **Reset Redo Stack:** `redo_stack` **dikosongkan** (`clear()`).
      * *Alasan:* Logika "Redo" adalah mengulang masa depan yang dibatalkan. Jika kita membuat cabang masa depan baru (mengetik baru), maka riwayat masa depan yang lama menjadi tidak valid.
3.  **Update Konten:** Konten teks diperbarui dengan input baru.
4.  **Update Trie:** Kata baru diproses dan dimasukkan ke dalam Trie agar bisa muncul di autocomplete berikutnya.

#### B. Saat Undo (Mundur)

1.  **Validasi:** Cek apakah `undo_stack` kosong. Jika ya, batalkan operasi.
2.  **Push ke Redo Stack:** Isi teks *saat ini* disimpan ke `redo_stack` (agar bisa di-redo nanti).
3.  **Pop dari Undo Stack:** Ambil state terakhir dari `undo_stack` dan jadikan sebagai konten aktif.

#### C. Saat Redo (Maju)

1.  **Validasi:** Cek apakah `redo_stack` kosong. Jika ya, batalkan operasi.
2.  **Push ke Undo Stack:** Isi teks *saat ini* disimpan kembali ke `undo_stack`.
3.  **Pop dari Redo Stack:** Ambil state masa depan dari `redo_stack` dan jadikan sebagai konten aktif.

**Ilustrasi Stack:**

```text
Kondisi Awal: Teks = "Halo"
[Undo Stack]: Kosong
[Redo Stack]: Kosong

Aksi 1: Ketik " Dunia" -> Teks = "Halo Dunia"
[Undo Stack]: ["Halo"]
[Redo Stack]: Kosong  <-- Dibersihkan

Aksi 2: Undo
[Undo Stack]: Kosong
[Redo Stack]: ["Halo Dunia"]
Teks Aktif  : "Halo"

Aksi 3: Redo
[Undo Stack]: ["Halo"]
[Redo Stack]: Kosong
Teks Aktif  : "Halo Dunia"
```

-----

## 🚀 Cara Menjalankan

### Persyaratan

  * Python 3.x terinstall.

### Langkah-langkah

1.  Buka terminal/cmd di folder root proyek.
2.  Jalankan perintah berikut:
    ```bash
    python main.py
    ```
3.  Pilih mode yang diinginkan:
      * **Mode 1 (CLI):** Interaksi berbasis teks di terminal.
      * **Mode 2 (GUI):** Interaksi visual menggunakan window.
      * **Mode 3 (Test):** Menjalankan pengujian otomatis untuk memastikan struktur data valid.

<!-- end list -->

```

### Apa yang saya tambahkan?
1.  **Visualisasi Teks (ASCII Art):** Membantu pembaca membayangkan bentuk pohon Trie dan tumpukan Stack.
2.  **Logika "Reset Redo Stack":** Menjelaskan poin krusial dalam algoritma undo-redo (mengapa redo hilang saat kita mengetik baru).
3.  **Penjelasan DFS:** Menyebutkan algoritma pencarian yang digunakan dalam Trie.

Ini akan membuat README Anda terlihat sangat profesional dan menunjukkan pemahaman mendalam tentang struktur data yang Anda buat.
```