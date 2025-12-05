from .struktur.trie import Trie
from .struktur.stack import Stack

class MesinKetik:
    def __init__(self, file_kamus: str):
        self.trie = Trie()
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self.teks_sekarang = ""
        self.jumlah_kata_dimuat = self._muat_kamus(file_kamus)

    def _muat_kamus(self, file_path: str) -> int:
        # ... (Kod sama seperti sebelumnya) ...
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
        Mencatat state teks baru.
        """
        if simpan_riwayat and teks != self.teks_sekarang:
            self.undo_stack.push(self.teks_sekarang)
            # Aksi baru akan menghapus riwayat redo
            if not self.redo_stack.is_empty():
                self.redo_stack = Stack() # Reset stack baru (Pythonic way)
        
        self.teks_sekarang = teks
        
        # [PENAMBAHBAIKAN LOGIC]
        # Jika pengguna mengetik spasi atau enter, pelajari kata terakhir
        if teks.endswith(' ') or teks.endswith('\n'):
            kata_terakhir = teks.strip().split()[-1] if teks.strip() else ""
            if kata_terakhir:
                # Masukkan ke Trie agar sistem 'belajar' kata baru/menambah frekuensi
                self.trie.insert(kata_terakhir.lower())

    # ... (Method undo, redo, dapatkan_saran sama seperti sebelumnya) ...
    def undo(self) -> str:
        if not self.undo_stack.is_empty():
            self.redo_stack.push(self.teks_sekarang)
            self.teks_sekarang = self.undo_stack.pop()
        return self.teks_sekarang

    def redo(self) -> str:
        if not self.redo_stack.is_empty():
            self.undo_stack.push(self.teks_sekarang)
            self.teks_sekarang = self.redo_stack.pop()
        return self.teks_sekarang

    def dapatkan_saran(self, prefix: str):
        if not prefix:
            return []
        return self.trie.suggest(prefix.lower())