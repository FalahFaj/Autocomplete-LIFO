import os
import sys
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import font as tkfont

# -- Setup Path (Agar module 'mesin' terbaca) --
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from mesin.penggabung import MesinKetik

# --- FUNGSI PENTING UNTUK EXE ---
def resource_path(relative_path):
    """Mendapatkan path file absolut, baik untuk mode dev maupun EXE"""
    try:
        # PyInstaller membuat folder temp di _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Skema Warna Modern (Dark Theme) ---
COLOR_BG_MAIN = "#2E3440"
COLOR_BG_SIDE = "#3B4252"
COLOR_TEXT = "#ECEFF4"
COLOR_ACCENT = "#88C0D0"
COLOR_ACCENT_HOVER = "#81A1C1"  
COLOR_BUTTON = "#4C566A"
COLOR_SUCCESS = "#A3BE8C"

class ModernApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Smart Editor Pro - Autocomplete & Undo/Redo")
        self.geometry("1000x650")
        self.configure(bg=COLOR_BG_MAIN)
        
        # --- Inisialisasi Logic (UPDATED PATH) ---
        # Menggunakan resource_path agar kompatibel dengan EXE
        # Kita asumsikan file ada di folder 'data' relatif terhadap root aplikasi
        file_kamus = resource_path(os.path.join('data', 'kumpulan_kata.txt'))
        
        # Fallback: Jika tidak ketemu di root (mode dev script), cari manual
        if not os.path.exists(file_kamus):
             file_kamus = os.path.join(parent_dir, 'data', 'kumpulan_kata.txt')
             
        self.mesin = MesinKetik(file_kamus)
        
        # Variabel Statistik
        self.start_time = None
        self.word_count = 0
        self.char_count = 0

        self._setup_styles()
        self._create_menu()
        self._create_layout()
        self._bind_events()
        
        self.text_area.focus_set()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Main.TFrame", background=COLOR_BG_MAIN)
        style.configure("Side.TFrame", background=COLOR_BG_SIDE)
        style.configure("Header.TLabel", background=COLOR_BG_SIDE, foreground=COLOR_ACCENT, font=("Segoe UI", 12, "bold"))
        style.configure("Status.TLabel", background=COLOR_BG_MAIN, foreground="#D8DEE9", font=("Segoe UI", 9))
        style.configure("Stats.TLabel", background=COLOR_BG_MAIN, foreground=COLOR_SUCCESS, font=("Consolas", 10))
        style.configure("Action.TButton", background=COLOR_BUTTON, foreground="white", font=("Segoe UI", 10), borderwidth=0)
        style.map("Action.TButton", background=[('active', COLOR_ACCENT_HOVER)])

    def _create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Buka File (Open)", command=self.open_file)
        file_menu.add_command(label="Simpan (Save)", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo (Ctrl+Z)", command=self.handle_undo)
        edit_menu.add_command(label="Redo (Ctrl+Y)", command=self.handle_redo)
        menubar.add_cascade(label="Edit", menu=edit_menu)

    def _create_layout(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        editor_frame = ttk.Frame(self, style="Main.TFrame", padding=15)
        editor_frame.grid(row=0, column=0, sticky="nsew")

        lbl_editor = tk.Label(editor_frame, text="📝 Editor Teks", bg=COLOR_BG_MAIN, fg=COLOR_TEXT, font=("Segoe UI", 14, "bold"))
        lbl_editor.pack(anchor="w", pady=(0, 10))

        txt_container = tk.Frame(editor_frame, bg=COLOR_BG_MAIN)
        txt_container.pack(fill=tk.BOTH, expand=True)

        self.text_font = tkfont.Font(family="Consolas", size=12)
        self.text_area = tk.Text(txt_container, wrap="word", font=self.text_font, bg="#3B4252", fg=COLOR_TEXT, insertbackground="white", selectbackground=COLOR_ACCENT, undo=False, bd=0, padx=10, pady=10)
        
        scroll_y = ttk.Scrollbar(txt_container, orient="vertical", command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scroll_y.set)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        side_frame = ttk.Frame(self, style="Side.TFrame", padding=15)
        side_frame.grid(row=0, column=1, sticky="nsew")

        lbl_control = ttk.Label(side_frame, text="Kontrol", style="Header.TLabel")
        lbl_control.pack(anchor="w", pady=(0, 10))
        
        btn_frame = ttk.Frame(side_frame, style="Side.TFrame")
        btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(btn_frame, text="⟲ Undo", style="Action.TButton", command=self.handle_undo).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="⟳ Redo", style="Action.TButton", command=self.handle_redo).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="💾 Simpan", style="Action.TButton", command=self.save_file).pack(fill=tk.X, pady=2)

        lbl_saran = ttk.Label(side_frame, text="Saran Kata (Tab)", style="Header.TLabel")
        lbl_saran.pack(anchor="w", pady=(0, 10))

        list_container = tk.Frame(side_frame, bg=COLOR_BG_SIDE)
        list_container.pack(fill=tk.BOTH, expand=True)

        self.suggestion_box = tk.Listbox(list_container, font=("Segoe UI", 11), bg=COLOR_BG_MAIN, fg=COLOR_TEXT, selectbackground=COLOR_ACCENT, selectforeground=COLOR_BG_MAIN, bd=0, highlightthickness=0)
        
        scroll_saran = ttk.Scrollbar(list_container, orient="vertical", command=self.suggestion_box.yview)
        self.suggestion_box.configure(yscrollcommand=scroll_saran.set)
        scroll_saran.pack(side=tk.RIGHT, fill=tk.Y)
        self.suggestion_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(side_frame, text="*Klik ganda untuk pilih", style="Status.TLabel", background=COLOR_BG_SIDE).pack(anchor="w", pady=(5,0))

        status_frame = ttk.Frame(self, style="Main.TFrame")
        status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        self.status_var = tk.StringVar(value="Siap mengetik...")
        self.stats_var = tk.StringVar(value="Kata: 0 | Karakter: 0 | WPM: 0")

        ttk.Label(status_frame, textvariable=self.status_var, style="Status.TLabel").pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.stats_var, style="Stats.TLabel").pack(side=tk.RIGHT)

    def _bind_events(self):
        self.text_area.bind("<KeyRelease>", self.handle_key_release)
        self.text_area.bind("<Tab>", self.handle_tab_complete)
        self.suggestion_box.bind("<Double-Button-1>", self.handle_suggestion_select)
        self.bind_all("<Control-z>", lambda e: self.handle_undo())
        self.bind_all("<Control-y>", lambda e: self.handle_redo())
        self.bind_all("<Control-s>", lambda e: self.save_file())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                content = self.text_area.get("1.0", tk.END)
                with open(file_path, "w", encoding="utf-8") as f: f.write(content)
                self.update_status(f"File disimpan: {os.path.basename(file_path)}")
            except Exception as e: messagebox.showerror("Error", f"Gagal menyimpan file: {e}")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f: content = f.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)
                self.mesin.ketik(content)
                self.update_status(f"File dibuka: {os.path.basename(file_path)}")
                self.calculate_stats()
            except Exception as e: messagebox.showerror("Error", f"Gagal membuka file: {e}")

    def handle_key_release(self, event):
        if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Tab"): return
        if self.start_time is None: self.start_time = time.time()
        full_text = self.text_area.get("1.0", "end-1c")
        if event.keysym in ("space", "Return"):
            self.mesin.ketik(full_text)
            self.update_status("State tersimpan.")
        self.update_suggestions(self._get_current_prefix())
        self.calculate_stats()

    def calculate_stats(self):
        text = self.text_area.get("1.0", "end-1c")
        words = text.split()
        self.word_count = len(words)
        self.char_count = len(text)
        wpm = 0
        if self.start_time:
            elapsed_minutes = (time.time() - self.start_time) / 60
            if elapsed_minutes > 0: wpm = int(self.word_count / elapsed_minutes)
        self.stats_var.set(f"Kata: {self.word_count} | Karakter: {self.char_count} | WPM: {wpm}")

    def _get_current_prefix(self):
        try:
            cursor_idx = self.text_area.index(tk.INSERT)
            line_start = cursor_idx.split('.')[0] + ".0"
            text_upto_cursor = self.text_area.get(line_start, cursor_idx)
            words = text_upto_cursor.split(' ')
            if words: return words[-1]
            return ""
        except: return ""

    def update_suggestions(self, prefix):
        self.suggestion_box.delete(0, tk.END)
        if prefix.strip():
            saran = self.mesin.dapatkan_saran(prefix)
            for kata, freq in saran: self.suggestion_box.insert(tk.END, f"{kata} ({freq})")
            if not saran: self.update_status("Tidak ada saran.")
        else: self.update_status("Mengetik...")

    def handle_tab_complete(self, event):
        if self.suggestion_box.size() > 0:
            first_item = self.suggestion_box.get(0)
            selected_word = first_item.split(' ')[0]
            self._complete_word(selected_word)
            return "break"

    def handle_suggestion_select(self, event):
        selection = self.suggestion_box.curselection()
        if selection:
            item = self.suggestion_box.get(selection[0])
            selected_word = item.split(' ')[0]
            self._complete_word(selected_word)
            self.text_area.focus_set()

    def _complete_word(self, word):
        cursor_pos = self.text_area.index(tk.INSERT)
        start_pos = cursor_pos
        while True:
            prev_idx = self.text_area.index(f"{start_pos}-1c")
            char = self.text_area.get(prev_idx)
            if char in (' ', '\n') or start_pos == "1.0" or start_pos == prev_idx: break
            start_pos = prev_idx
        self.text_area.delete(start_pos, cursor_pos)
        self.text_area.insert(start_pos, word + " ")
        self.mesin.ketik(self.text_area.get("1.0", "end-1c"))
        self.suggestion_box.delete(0, tk.END)
        self.calculate_stats()

    def handle_undo(self):
        new_text = self.mesin.undo()
        self._refresh_editor(new_text)
        self.update_status("Undo berhasil.")

    def handle_redo(self):
        new_text = self.mesin.redo()
        self._refresh_editor(new_text)
        self.update_status("Redo berhasil.")

    def _refresh_editor(self, text):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", text)
        self.calculate_stats()

    def update_status(self, msg): self.status_var.set(msg)

if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()