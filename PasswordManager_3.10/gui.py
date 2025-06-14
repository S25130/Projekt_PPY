import tkinter as tk
from tkinter import messagebox
from auth import register_user
from auth import login_user, is_strong_password


def start_gui():
    root = tk.Tk()
    root.title("PasswordManager")
    root.geometry("1200x675")

    try:
        icon = tk.PhotoImage(file="locker.png")
        root.iconphoto(True, icon)
    except tk.TclError:
        print("Błąd: Nieprawidłowy plik PNG lub plik nie istnieje.")

    label = tk.Label(root, text="Welcome in your Password Manager!", font=("Arial", 18))
    label.pack(pady=40)

    login_button = tk.Button(root, text="Sign in", width=20, height=2, command=handle_login)
    login_button.pack(pady=10)

    register_button = tk.Button(root, text="Sign up", width=20, height=2, command=handle_register)
    register_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", width=20, height=2, command=root.destroy)
    exit_button.pack(pady=40)

    root.mainloop()

def handle_login():
    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry("400x250")

    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def submit_login():
        username = username_entry.get()
        password = password_entry.get()
        user = login_user(username, password)
        if user:
            messagebox.showinfo("Success", f"Logged in as: {user.username}")
            login_window.destroy()
            # TODO: open user dashboard here
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    tk.Button(login_window, text="Log In", command=submit_login).pack(pady=20)


def handle_register():
    register_window = tk.Toplevel()
    register_window.title("Register")
    register_window.geometry("400x250")

    tk.Label(register_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(register_window)
    username_entry.pack()

    tk.Label(register_window, text="Master password:").pack(pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack()

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
    tk.Button(register_window, text="Sign Up", command=submit_registration).pack(pady=20)

