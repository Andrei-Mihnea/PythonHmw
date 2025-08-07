# utils/jwt_helper.py
import jwt
from flask import request

from Database.user_db import User

SECRET_KEY = "your-secret-key"

def validate_jwt():
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        if not User.get_user_by_username(payload.get("user_id")):
            raise jwt.InvalidTokenError
        
        return payload
    
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None