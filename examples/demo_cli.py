# Contoh implementasi dan demo interaktif menggunakan MesinKetik di lingkungan CLI.
# Versi ini menggunakan msvcrt untuk input per-karakter (Windows-only).
# "
import os
import sys

# -- Menambahkan parent directory ke sys.path untuk impor --
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# ---------------------------------------------------------

from mesin.penggabung import MesinKetik

def clear_screen():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_prefix(text: str):
    """Mendapatkan kata terakhir dari teks sebagai prefix."""
    if not text or text.endswith(' '):
        return ""
    return text.split(' ')[-1]

def run_interactive_demo():
    """
    Menjalankan demo interaktif utama menggunakan msvcrt.
    """
    import msvcrt

    # --- Setup ---
    file_kamus = os.path.join(parent_dir, 'data', 'kumpulan_kata.txt')
    mesin = MesinKetik(file_kamus)
    # Simpan state awal yang kosong
    mesin.ketik("", simpan_riwayat=False) 
    
    current_text = ""
    
    # --- Main Loop ---
    while True:
        # 1. Gambar Ulang Tampilan
        clear_screen()
        print("Selamat Datang di Demo Interaktif (Windows-only)!")
        print("Ctrl+Z: Undo | Ctrl+Y: Redo | Tab: Autocomplete | Ctrl+C: Keluar")
        print("-" * 60)
        
        print(f"> {current_text}", end='', flush=True)

        prefix = get_prefix(current_text)
        saran = mesin.dapatkan_saran(prefix)
        
        if saran:
            saran_kata = [s[0] for s in saran[:5]]
            print("\n\n" + " | ".join(saran_kata), end='')
            sys.stdout.write('\r\033[A\033[A') 
            print(f"> {current_text}", end='', flush=True)

        # 2. Tunggu Input Karakter
        try:
            char = msvcrt.getch()
        except KeyboardInterrupt:
            break

        # 3. Proses Input Karakter
        # Tombol Spesial
        if char == b'\x03': # Ctrl+C
            print("\nKeluar dari program...")
            break
        elif char == b'\x1a': # Ctrl+Z (Undo)
            current_text = mesin.undo()
        elif char == b'\x19': # Ctrl+Y (Redo)
            current_text = mesin.redo()
        elif char == b' ': # Spasi
            # Simpan state sebelum menambahkan spasi
            mesin.ketik(current_text)
            current_text += " "
        elif char == b'\r': # Enter
            # Simpan state saat ini, lalu mulai baris baru (opsional)
            mesin.ketik(current_text)
            current_text += "\n> " # Pindah ke baris baru
        elif char == b'\t': # Tab
            if saran:
                top_suggestion = saran[0][0]
                last_space = current_text.rfind(' ')
                if last_space == -1:
                    current_text = top_suggestion
                else:
                    current_text = current_text[:last_space+1] + top_suggestion
                # Simpan state setelah autocomplete
                mesin.ketik(current_text)
        elif char == b'\x08': # Backspace
            current_text = current_text[:-1]
        
        # Karakter Biasa
        else:
            try:
                char_decoded = char.decode('utf-8')
                if char_decoded.isprintable():
                    current_text += char_decoded
            except UnicodeDecodeError:
                # Abaikan karakter yang tidak bisa di-decode
                pass

def main():
    if os.name != 'nt':
        print("Error: Demo interaktif ini hanya dapat berjalan di Windows.")
        print("Silakan jalankan versi non-interaktif jika ada.")
        sys.exit(1)
    
    run_interactive_demo()

if __name__ == '__main__':
    main()
