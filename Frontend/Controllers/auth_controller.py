import os
from Frontend import request_context
from urllib.parse import parse_qs
from Database.user_db import SessionLocal, User
import bcrypt
import jwt
import datetime
import time
from flask import request, redirect, make_response

class AuthController:

    def index(self):
        current_dir = os.path.dirname(__file__)

        template_path = os.path.join(current_dir, '..', 'Templates', 'auth.html')
        template_path = os.path.abspath(template_path)

        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        return html

    def login(self):
        if request.method != 'POST':
            return "405 Method Not Allowed", 405

        username = request.form.get('username', '')
        password = request.form.get('password', '')

        user_model = User()

        if user_model.exists_password_and_user(username, password):
            payload = {
                "user_id": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=15)
            }

            secret = "your-secret-key"
            token = jwt.encode(payload, secret, algorithm="HS256")

            response = make_response(redirect("/home/index"))
            response.set_cookie(
                "access_token", token,
                httponly=True,
                samesite='Strict',
                secure=request.is_secure,
                max_age= 30
            )
            return response
        return "<h1>Invalid username or password</h1>"
        
    def register(self):

        if request.method != 'POST':
            return "405 Method Not Allowed", 405

        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        session = SessionLocal()
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            user = User(
                username=username,
                email=email,
                password=hashed.decode() 
            )

            session.add(user)
            session.commit()
        finally:
            session.close()

        response = make_response(redirect("/auth/index"))
        return response