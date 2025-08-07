
from functools import wraps
from flask import redirect

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from Utils.jwt_helper import validate_jwt
        user_data = validate_jwt()
        if not user_data:
            return redirect("/auth/index")
        return func(*args, **kwargs, user = user_data.get("user_id"))
    return wrapper
