from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError
from databaseModels import User
from databaseModels import PasswordEntry
from database import SessionLocal


def register_user(username, password):
    session = SessionLocal()
    hashed_pw = bcrypt.hash(password)
    user = User(username=username, master_password=hashed_pw)

    try:
        session.add(user)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    finally:
        session.close()


def login_user(username, password):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if user and bcrypt.verify(password, user.master_password):
        return user
    return None

import re

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def get_user_passwords(user_id):
    session = SessionLocal()
    passwords = session.query(PasswordEntry).filter_by(user_id=user_id).all()
    session.close()
    return [
        {
            "id": entry.id,  # dodaj to
            "aplikacja": entry.service_name,
            "login": entry.service_username,
            "haslo": entry.encrypted_password
        }
        for entry in passwords
    ]

