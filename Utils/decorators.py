
from functools import wraps
from flask import redirect

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from Utils.jwt_helper import validate_jwt
        if not validate_jwt():
            return redirect("/auth/index")
        return func(*args, **kwargs)
    return wrapper
