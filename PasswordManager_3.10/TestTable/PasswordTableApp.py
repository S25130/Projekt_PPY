import tkinter as tk
from tkinter import ttk

# Dane testowe
dane = [
    {"aplikacja": "Gmail", "login": "jan.kowalski", "haslo": "admin123"},
    {"aplikacja": "Facebook", "login": "kowalski.jan", "haslo": "fbpass456"},
    {"aplikacja": "LinkedIn", "login": "jkowalski", "haslo": "linked789"},
]

ROW_HEIGHT = 30

class PasswordTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabela Haseł")
        self.checkbox_vars = []

        style = ttk.Style()
        style.configure("Treeview", rowheight=ROW_HEIGHT)

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.main_frame, width=40)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            self.left_frame,
            columns=("aplikacja", "login", "haslo"),
            show="headings",
            height=20
        )
        self.tree.heading("aplikacja", text="Aplikacja")
        self.tree.heading("login", text="Login")
        self.tree.heading("haslo", text="Hasło")

        self.tree.column("aplikacja", width=200)
        self.tree.column("login", width=200)
        self.tree.column("haslo", width=200)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.checkbox_widgets = []
        for idx, rekord in enumerate(dane):
            masked_pwd = "*" * len(rekord["haslo"])
            self.tree.insert("", "end", iid=idx, values=(rekord["aplikacja"], rekord["login"], masked_pwd))

            var = tk.IntVar()
            self.checkbox_vars.append(var)
            cb = tk.Checkbutton(self.right_frame, variable=var)
            self.checkbox_widgets.append(cb)

        self.root.after(100, self.place_checkboxes)

        # Przyciski: Pokaż i Ukryj
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)

        self.btn_show = tk.Button(self.btn_frame, text="Pokaż hasło", width=20, command=self.show_passwords)
        self.btn_show.pack(side=tk.LEFT, padx=10)

        self.btn_hide = tk.Button(self.btn_frame, text="Ukryj hasło", width=20, command=self.hide_passwords)
        self.btn_hide.pack(side=tk.LEFT, padx=10)

    def place_checkboxes(self):
        for idx, cb in enumerate(self.checkbox_widgets):
            bbox = self.tree.bbox(idx)
            if bbox:
                x, y, width, height = bbox
                cb.place(x=5, y=y + height // 2 - 10)

    def show_passwords(self):
        for idx, var in enumerate(self.checkbox_vars):
            if var.get() == 1:
                self.tree.set(idx, "haslo", dane[idx]["haslo"])

    def hide_passwords(self):
        for idx, var in enumerate(self.checkbox_vars):
            if var.get() == 1:
                masked = "*" * len(dane[idx]["haslo"])
                self.tree.set(idx, "haslo", masked)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    root.resizable(False, False)
    app = PasswordTableApp(root)
    root.mainloop()
