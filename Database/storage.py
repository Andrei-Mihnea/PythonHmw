from datetime import datetime
from Database.log_db import SessionLocal, RequestsLog

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
    session = SessionLocal()
    try:
        logs = session.query(RequestsLog).all()
        return logs
    finally:
        session.close()

def get_log(operation, parameters,result):
    """Retrieve respective log request"""
    session = SessionLocal()
    try:
        result = (
            session.query(RequestsLog)
            .filter_by(endpoint=operation, parameters = str(parameters), result = str(result))
            .order_by(RequestsLog.timestamp.desc())
            .first()
        )

        if result:
            return result
        else:
            print("Log not found")
            return None
        
    except Exception as e:
        print("Error when fetching log")
        return None
    finally:
        session.close()