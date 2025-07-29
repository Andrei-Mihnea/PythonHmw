from Utils.decorators import login_required
import os
import jwt
from flask import request, make_response,jsonify,Blueprint
from Database.log_db import RequestsLog, SessionLocal


class FibonacciController:
    @login_required
    def index(self):
        current_dir = os.path.dirname(__file__)
        template_path = os.path.join(current_dir, '..', 'Templates', 'fibonacci.html')
        template_path = os.path.abspath(template_path)

        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        response = make_response(html)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

