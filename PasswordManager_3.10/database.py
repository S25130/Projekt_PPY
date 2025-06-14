from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseModels import Base

DATABASE_URL = "sqlite:///password_manager.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
