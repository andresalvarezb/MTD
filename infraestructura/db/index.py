from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


load_dotenv()

DATABASE_URL = "mysql+pymysql://root:Abecerra321$@localhost:3306/cuentasmedicas"


print("🔗 DATABASE_URL:", DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
