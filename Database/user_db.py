import os
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:123@localhost:5432/user_db')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def init_db():
        """Initialize the database."""
        Base.metadata.create_all(bind=engine)
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
    
    def get_user_by_id(self, user_id):
        """Retrieve a user by their ID."""
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            return user
        finally:
            session.close()
    
    def get_user_by_username(self, username):
        """Retrieve a user by their username."""
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.username == username).first()
            return user
        finally:
            session.close()
    
    def get_user_by_email(self, email):
        """Retrieve a user by their email."""
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.email == email).first()
            return user
        finally:
            session.close()
