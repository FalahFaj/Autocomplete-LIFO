"""
File: penggabung.py

Kelas utama yang menggabungkan Trie untuk autocomplete dan Stack untuk undo/redo.
"""

from .struktur.trie import Trie
from .struktur.stack import Stack

class MesinKetik:
    """
    Kelas 'Mesin Ketik' yang mengelola state teks,
    riwayat perubahan (undo/redo), dan saran kata (autocomplete).
    """

    def __init__(self, file_kamus: str):
        """
        Inisialisasi MesinKetik.
        
        :param file_kamus: Path menuju file teks yang berisi daftar kata,
                           satu kata per baris.
        """
        self.trie = Trie()
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self.teks_sekarang = ""
        
        self.jumlah_kata_dimuat = self._muat_kamus(file_kamus)

    def _muat_kamus(self, file_path: str) -> int:
        """
        Memuat kata dari file dan memasukkannya ke dalam Trie.
        
        :param file_path: Path menuju file kamus.
        :return: Jumlah kata yang berhasil dimuat.
        """
        count = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    kata = line.strip().lower()
                    if kata:
                        self.trie.insert(kata)
                        count += 1
        except FileNotFoundError:
            print(f"Peringatan: File kamus tidak ditemukan di '{file_path}'")
        return count

    def ketik(self, teks: str, simpan_riwayat=True):
        """
        Mencatat state teks baru. Ini adalah aksi utama pengguna.
        
        :param teks: Teks lengkap yang baru dari input pengguna.
        :param simpan_riwayat: Jika True, state sebelumnya akan disimpan
                               ke undo stack.
        """
        if simpan_riwayat and teks != self.teks_sekarang:
            self.undo_stack.push(self.teks_sekarang)
            # Aksi baru akan menghapus riwayat redo
            if not self.redo_stack.is_empty():
                self.redo_stack = Stack()
        
        self.teks_sekarang = teks

    def undo(self) -> str:
        """
        Mengembalikan state teks ke kondisi sebelumnya.
        
        :return: State teks setelah undo.
        """
        if not self.undo_stack.is_empty():
            self.redo_stack.push(self.teks_sekarang)
            self.teks_sekarang = self.undo_stack.pop()
        return self.teks_sekarang

    def redo(self) -> str:
        """
        Mengembalikan state teks ke kondisi setelah di-undo.
        
        :return: State teks setelah redo.
        """
        if not self.redo_stack.is_empty():
            self.undo_stack.push(self.teks_sekarang)
            self.teks_sekarang = self.redo_stack.pop()
        return self.teks_sekarang

    def dapatkan_saran(self, prefix: str):
        """
        Mendapatkan saran kata berdasarkan prefix yang diberikan.
        
        :param prefix: Potongan kata untuk dijadikan dasar autocomplete.
        :return: List of tuples (kata, frekuensi)
        """
        if not prefix:
            return []
        return self.trie.suggest(prefix.lower())