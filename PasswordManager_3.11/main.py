import tkinter as tk
import os

def main():
    root = tk.Tk()
    root.title("PasswordManager")
    root.geometry("1200x675")

    try:
        icon = tk.PhotoImage(file="locker.png")
        root.iconphoto(True, icon)
    except tk.TclError:
        print("Błąd: Nieprawidłowy plik PNG lub plik nie istnieje.")

    label = tk.Label(root, text="Welcome in your Password Manager!", font=("Arial", 14))
    label.pack(pady=20)

    button = tk.Button(root, text="Close", command=root.destroy)
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
