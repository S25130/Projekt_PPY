from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    master_password = Column(String, nullable=False)

    passwords = relationship("PasswordEntry", back_populates="user")


class PasswordEntry(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True)
    service_name = Column(String, nullable=False)
    service_username = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="passwords")