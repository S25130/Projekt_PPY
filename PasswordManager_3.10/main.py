from database import init_db
from gui import start_gui
from auth import register_user, login_user
from create_test_user import create_user


if __name__ == "__main__":
    init_db()
    start_gui()
    if not login_user("admin", "admin123"):
        create_user("admin", "admin123")





