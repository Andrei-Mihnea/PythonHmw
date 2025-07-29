# Controllers/home_controller.py
import jwt
from Utils.decorators import login_required
import os
from flask import request, redirect, make_response

class HomeController:
    @login_required
    def index(self):
        current_dir = os.path.dirname(__file__)

        template_path = os.path.join(current_dir, '..', 'Templates', 'home.html')
        template_path = os.path.abspath(template_path)

        token = request.cookies.get("access_token")
        username = jwt.decode(token, "your-secret-key", algorithms=["HS256"]).get("user_id")


        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()

        html = html.replace("{{username}}", username)
        response = make_response(html)

        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @login_required
    def about(self):
        return "This is the about page."
