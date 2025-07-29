from Utils.decorators import login_required
import os
from flask import request, make_response
class FactorialController:
    @login_required
    def index(self):
        current_dir = os.path.dirname(__file__)
        template_path = os.path.join(current_dir, '..', 'Templates', 'factorial.html')
        template_path = os.path.abspath(template_path)

        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        response = make_response(html)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response


    @login_required
    def status(self):
        return "Factorial Status: All systems operational"
