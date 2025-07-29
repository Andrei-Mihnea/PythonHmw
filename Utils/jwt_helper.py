# utils/jwt_helper.py
import jwt
from flask import request

SECRET_KEY = "your-secret-key"

def validate_jwt():
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None