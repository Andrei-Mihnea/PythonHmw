from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:123@localhost:5432/math_db')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

