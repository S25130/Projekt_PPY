from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError
from databaseModels import User
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