from database import SessionLocal
from databaseModels import User
from passlib.hash import bcrypt

def create_user(username, password):
    session = SessionLocal()
    master_password = bcrypt.hash(password)
    user = User(username=username, master_password=master_password)

    try:
        session.add(user)
        session.commit()
        print(f"Użytkownik '{username}' został dodany.")
    except Exception as e:
        session.rollback()
        print("Błąd podczas dodawania użytkownika:", e)
    finally:
        session.close()

