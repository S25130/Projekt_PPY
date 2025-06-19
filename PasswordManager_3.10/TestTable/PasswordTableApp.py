import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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

        # === Tło z grafiki ===
        bg_img = Image.open("tlo.png").resize((1280, 720))
        self.bg_photo = ImageTk.PhotoImage(bg_img)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # === Kontener (środek ekranu) ===
        self.center_frame = tk.Frame(root, width=960, height=540, bg="white")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.center_frame.pack_propagate(False)

        self.main_frame = tk.Frame(self.center_frame, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.main_frame, bg="white")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.main_frame, bg="white", width=40)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            self.left_frame,
            columns=("aplikacja", "login", "haslo"),
            show="headings",
            height=15
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
            cb = tk.Checkbutton(self.right_frame, variable=var, bg="white")
            self.checkbox_widgets.append(cb)

        self.retry_count = 0
        self.schedule_place_checkboxes()

        # Przyciski: Pokaż / Ukryj
        self.btn_frame = tk.Frame(self.center_frame, bg="white")
        self.btn_frame.pack(pady=5)

        self.btn_add = tk.Button(self.btn_frame, text="Dodaj hasło", width=20, command=self.open_add_password_window)
        self.btn_add.pack(side=tk.LEFT, padx=10)

        self.btn_show = tk.Button(self.btn_frame, text="Pokaż hasło", width=20, command=self.show_passwords)
        self.btn_show.pack(side=tk.LEFT, padx=10)

        self.btn_hide = tk.Button(self.btn_frame, text="Ukryj hasło", width=20, command=self.hide_passwords)
        self.btn_hide.pack(side=tk.LEFT, padx=10)

        self.btn_delete = tk.Button(self.btn_frame, text="Usuń hasło", width=20, command=self.delete_selected_passwords)
        self.btn_delete.pack(side=tk.LEFT, padx=10)

    def schedule_place_checkboxes(self):
        self.retry_count += 1
        success = False
        for idx, cb in enumerate(self.checkbox_widgets):
            bbox = self.tree.bbox(idx)
            if bbox:
                _, y, _, height = bbox
                cb.place(x=5, y=y + height // 2 - 10)
                success = True
        if not success and self.retry_count < 10:
            self.root.after(100, self.schedule_place_checkboxes)

    def place_checkboxes(self):
        for idx, cb in enumerate(self.checkbox_widgets):
            bbox = self.tree.bbox(idx)
            if bbox:
                x, y, width, height = bbox
                cb.place(in_=self.tree, x=5, y=y + height // 2 - 10)

    def show_passwords(self):
        for idx, var in enumerate(self.checkbox_vars):
            if var.get() == 1:
                self.tree.set(idx, "haslo", dane[idx]["haslo"])

    def hide_passwords(self):
        for idx, var in enumerate(self.checkbox_vars):
            if var.get() == 1:
                masked = "*" * len(dane[idx]["haslo"])
                self.tree.set(idx, "haslo", masked)

    def open_add_password_window(self):
        popup = tk.Toplevel(self.root)
        popup.title("Dodaj nowe hasło")
        popup.geometry("300x200")
        popup.resizable(False, False)

        tk.Label(popup, text="Aplikacja:").pack(pady=5)
        entry_app = tk.Entry(popup)
        entry_app.pack()

        tk.Label(popup, text="Login:").pack(pady=5)
        entry_login = tk.Entry(popup)
        entry_login.pack()

        tk.Label(popup, text="Hasło:").pack(pady=5)
        entry_pass = tk.Entry(popup, show="*")
        entry_pass.pack()

        def save():
            app_name = entry_app.get().strip()
            login = entry_login.get().strip()
            password = entry_pass.get().strip()

            if app_name and login and password:
                dane.append({"aplikacja": app_name, "login": login, "haslo": password})
                self.refresh_table()
                popup.destroy()

        tk.Button(popup, text="Zapisz", command=save).pack(pady=10)

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for cb in self.checkbox_widgets:
            cb.destroy()
        self.checkbox_vars.clear()
        self.checkbox_widgets.clear()

        for idx, rekord in enumerate(dane):
            masked = "*" * len(rekord["haslo"])
            self.tree.insert("", "end", iid=idx, values=(rekord["aplikacja"], rekord["login"], masked))
            var = tk.IntVar()
            self.checkbox_vars.append(var)
            cb = tk.Checkbutton(self.right_frame, variable=var, bg="white")
            self.checkbox_widgets.append(cb)

        self.retry_count = 0
        self.schedule_place_checkboxes()

    def delete_selected_passwords(self):
        to_delete = []

        for idx, var in enumerate(self.checkbox_vars):
            if var.get() == 1:
                to_delete.append(idx)

        # Usuń z końca, by nie zmieniać indeksów wcześniej
        for idx in sorted(to_delete, reverse=True):
            dane.pop(idx)

        self.refresh_table()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    root.resizable(False, False)
    app = PasswordTableApp(root)
    root.mainloop()
