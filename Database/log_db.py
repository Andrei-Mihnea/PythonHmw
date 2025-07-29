from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP,and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class RequestsLog(Base):
    __tablename__ = 'requests_log'
    
    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(255), nullable=False)
    parameters = Column(Text, nullable=False)
    username = Column(String(50), nullable=True)
    result = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

    def init_db():
        """Initialize the database."""
        Base.metadata.create_all(bind=engine)

    def __repr__(self):
        return f"<RequestsLog(id={self.id}, endpoint={self.endpoint}, parameters={self.parameters}, result={self.result}, timestamp={self.timestamp})>"

    def get_log_by_id(self, log_id):
        """Retrieve a log entry by its ID."""
        session = SessionLocal()
        try:
            log = session.query(RequestsLog).filter(RequestsLog.id == log_id).first()
            return log
        finally:
            session.close()

    def get_logs_by_endpoint(self, endpoint):
        """Retrieve log entries by endpoint."""
        session = SessionLocal()
        try:
            logs = session.query(RequestsLog).filter(RequestsLog.endpoint == endpoint).all()
            return logs
        finally:
            session.close()
    
    def get_logs_by_timestamp(self, start_time, end_time):
        """Retrieve log entries within a specific time range."""
        session = SessionLocal()
        try:
            logs = session.query(RequestsLog).filter(RequestsLog.timestamp.between(start_time, end_time)).all()
            return logs
        finally:
            session.close()
    
    def get_logs_by_username_and_endpoint(self, username, endpoint):
        """Retrieve log entries by username."""
        session = SessionLocal()
        try:
            logs = session.query(RequestsLog).filter(
                and_(
                    RequestsLog.username == username,
                    RequestsLog.endpoint == endpoint
                    )
                ).order_by(RequestsLog.timestamp.desc()).limit(10).all()
            return logs or []
        finally:
            session.close()
    
    

