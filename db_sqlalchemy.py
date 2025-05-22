from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base

DATABASE_URL = 'postgresql+psycopg2://postgres:password123@localhost:5432/bank'
engine = create_engine(DATABASE_URL)
SessionLocal = Session(bind=engine)

def init_db():
    Base.metadata.create_all(engine)