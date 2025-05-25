# main.py

import tkinter as tk

def main():
    root = tk.Tk()
    root.title("PasswordManager")
    root.geometry("600x300")  # szerokość x wysokość

    label = tk.Label(root, text="Welcome in your Password Manager!", font=("Arial", 14))
    label.pack(pady=20)

    button = tk.Button(root, text="Close", command=root.destroy)
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
