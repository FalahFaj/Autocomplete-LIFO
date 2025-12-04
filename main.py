import os

def main():
    print("Selamat Datang di Project Autocomplete & Undo-Redo")
    print("Silakan pilih mode demo:")
    print("1. Demo CLI (Command Line)")
    print("2. Demo GUI (Window)")
    print("3. Jalankan Tests")
    
    pilihan = input("Masukkan pilihan (1/2/3): ")
    
    if pilihan == "1":
        print("\nMenjalankan Demo CLI...")
        os.system("python examples/demo_cli.py")
    elif pilihan == "2":
        print("\nMenjalankan Demo GUI...")
        os.system("python examples/demo_gui.py")
    elif pilihan == "3":
        print("\nMenjalankan Unit Tests...")
        os.system("python -m unittest discover tests")
    else:
        print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()