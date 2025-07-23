from datetime import datetime
from Database.db import SessionLocal, RequestsLog

def log_request(operation, inputs, result):
    """Log the request details."""
    session = SessionLocal()
    
    try:
        log = RequestsLog(
            endpoint=operation,
            parameters=str(inputs),
            result=str(result),
            timestamp=datetime.utcnow()
        )

        session.add(log)
        session.commit()
    finally:
        session.close()

def get_logs():
    """Retrieve all logged requests."""
    return storage