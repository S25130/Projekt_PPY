import tkinter as tk
from tkinter import messagebox, Canvas, PhotoImage, Button
from pathlib import Path
from auth import register_user, login_user, is_strong_password, get_user_passwords
#from auth import login_user, get_user_passwords

from passwordTable import PasswordTableApp

# Ścieżka główna
OUTPUT_PATH = Path(__file__).parent

# Pomocnicza funkcja do zasobów
def relative_to_assets(path: str, base_folder: str) -> Path:
    return OUTPUT_PATH / Path(base_folder) / "build/assets/frame0" / Path(path)

# -------------------------
#      LOGOWANIE
# -------------------------
def handle_login(root):
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("400x250")
    login_window.configure(bg="#FFFFFF")

    canvas = Canvas(
        login_window,
        bg="#FFFFFF",
        height=250,
        width=400,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    try:
        login_window.bg_image = PhotoImage(file=relative_to_assets("image_1.png", "Login"))
        canvas.create_image(200.0, 125.0, image=login_window.bg_image)
    except Exception as e:
        print("Błąd ładowania tła:", e)
        canvas.create_rectangle(0, 0, 400, 250, fill="#f0f0f0", outline="")

    canvas.create_text(152.0, 25.0, anchor="nw", text="Username:", fill="#FFFFFF", font=("Inter Bold", 16))
    canvas.create_text(152.0, 86.0, anchor="nw", text="Password:", fill="#FFFFFF", font=("Inter Bold", 16))

    username_entry = tk.Entry(login_window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    username_entry.place(x=110.0, y=48.0, width=180.0, height=28.0)

    password_entry = tk.Entry(login_window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
    password_entry.place(x=110.0, y=109.0, width=180.0, height=28.0)

    def submit_login():
        username = username_entry.get()
        password = password_entry.get()
        user = login_user(username, password)
        if user:
            dane_uzytkownika = get_user_passwords(user.id)
            login_window.destroy()
            for widget in root.winfo_children():
                widget.destroy()
            PasswordTableApp(root, dane_uzytkownika, user.id)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    try:
        login_window.login_button_image = PhotoImage(file=relative_to_assets("button_1.png", "Login"))
        login_button = Button(
            login_window,
            image=login_window.login_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=submit_login,
            relief="flat"
        )
        login_button.place(x=110.0, y=185.0, width=180.0, height=30.0)
    except Exception as e:
        print("Błąd ładowania przycisku:", e)
        tk.Button(login_window, text="Login", command=submit_login).place(x=160, y=185)

    login_window.resizable(False, False)

# -------------------------
#     REJESTRACJA
# -------------------------
def handle_register():
    register_window = tk.Toplevel()
    register_window.title("Register")
    register_window.geometry("400x250")
    register_window.configure(bg="#FFFFFF")

    canvas = Canvas(
        register_window,
        bg="#FFFFFF",
        height=250,
        width=400,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    try:
        register_window.bg_image = PhotoImage(file=relative_to_assets("image_1.png", "Register"))
        canvas.create_image(200.0, 125.0, image=register_window.bg_image)
    except Exception as e:
        print("Błąd ładowania tła (Register):", e)
        canvas.create_rectangle(0, 0, 400, 250, fill="#f0f0f0", outline="")

    canvas.create_text(152.0, 25.0, anchor="nw", text="Username:", fill="#FFFFFF", font=("Inter Bold", 16))
    canvas.create_text(115, 86.0, anchor="nw", text="Master Password:", fill="#FFFFFF", font=("Inter Bold", 16))

    username_entry = tk.Entry(register_window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    username_entry.place(x=110.0, y=48.0, width=180.0, height=28.0)

    password_entry = tk.Entry(register_window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
    password_entry.place(x=110.0, y=109.0, width=180.0, height=28.0)

    def submit_registration():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        if not is_strong_password(password):
            messagebox.showwarning(
                "Weak Password",
                "Password must be at least 8 characters,\ncontain one uppercase letter,\nand one special character."
            )
            return

        success = register_user(username, password)
        if success:
            messagebox.showinfo("Success", "Account created successfully!")
            register_window.destroy()
        else:
            messagebox.showerror("Error", "Username already exists.")

    try:
        register_window.register_button_image = PhotoImage(file=relative_to_assets("button_1.png", "Register"))
        register_button = Button(
            register_window,
            image=register_window.register_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=submit_registration,
            relief="flat"
        )
        register_button.place(x=110.0, y=185.0, width=180.0, height=30.0)
    except Exception as e:
        print("Błąd ładowania przycisku (Register):", e)
        tk.Button(register_window, text="Sign Up", command=submit_registration).place(x=160, y=185)

    register_window.resizable(False, False)

# -------------------------
#     OKNO STARTOWE
# -------------------------
def start_gui():
    root = tk.Tk()
    root.title("PasswordManager")
    root.geometry("1280x720")
    root.configure(bg="#FFFFFF")

    try:
        icon = PhotoImage(file="locker.png")
        root.iconphoto(True, icon)
    except tk.TclError:
        print("Błąd: Ikona nie została załadowana.")

    canvas = Canvas(
        root,
        bg="#FFFFFF",
        height=720,
        width=1280,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png", "Start"))
    canvas.create_image(640.0, 360.0, image=image_image_1)

    canvas.create_text(
        105.0,
        83.0,
        anchor="nw",
        text="PASSWORD MANAGER",
        fill="#FFFFFF",
        font=("Inter Bold", 96 * -1)
    )

    # Exit
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png", "Start"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=root.destroy,
        relief="flat"
    )
    button_1.place(x=434.0, y=478.0, width=412.0, height=94.0)

    # Sign Up
    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png", "Start"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=handle_register,
        relief="flat"
    )
    button_2.place(x=434.0, y=360.0, width=412.0, height=94.0)

    # Sign In
    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png", "Start"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: handle_login(root),  # ← przekazujemy root
        relief="flat"
    )
    button_3.place(x=434.0, y=242.0, width=412.0, height=94.0)

    root.resizable(False, False)
    root.mainloop()
