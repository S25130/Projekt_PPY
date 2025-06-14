from database import init_db
from gui import start_gui
from auth import register_user, login_user
from create_test_user import create_user


def run_auth_test():

    print("=== SYMULACJA AUTORYZACJI ===")
    print("1. Rejestracja")
    print("2. Logowanie")
    print("0. Wyjście")

    choice = input("Wybierz opcję: ")

    if choice == "1":
        username = input("Podaj nazwę użytkownika: ")
        password = input("Podaj hasło: ")
        success = register_user(username, password)
        if success:
            print("Rejestracja zakończona sukcesem!")
        else:
            print("Taki użytkownik już istnieje.")

    elif choice == "2":
        username = input("Login: ")
        password = input("Hasło: ")
        user = login_user(username, password)
        if user:
            print(f"Zalogowano jako: {user.username}")
        else:
            print("Błędna nazwa użytkownika lub hasło.")

    elif choice == "0":
        print("Exit")
    else:
        print("Nieprawidłowa opcja.")



if __name__ == "__main__":
    init_db()
    start_gui()
    if not login_user("admin", "admin123"):
        create_user("admin", "admin123")
    run_auth_test()




