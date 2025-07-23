from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:123@localhost:5432/math_db')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class RequestsLog(Base):
    __tablename__ = 'requests_log'
    
    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(255), nullable=False)
    parameters = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

    def init_db():
        """Initialize the database."""
        Base.metadata.create_all(bind=engine)

    def __repr__(self):
        return f"<RequestsLog(id={self.id}, endpoint={self.endpoint}, parameters={self.parameters}, result={self.result}, timestamp={self.timestamp})>"
