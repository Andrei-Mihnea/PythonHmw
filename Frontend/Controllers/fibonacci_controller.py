from Utils.decorators import login_required
import os
import jwt
from flask import request, make_response,jsonify,Blueprint
from Database.log_db import RequestsLog

fibonacci_bp = Blueprint("fibonacci",__name__)

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

@fibonacci_bp.route('/api/fibonacci/index')
@login_required
def get_fibonacci():
    token = request.cookies.get("access_token")
    if not token:
        return {"error": "Unauthorized"}, 401
    
    try:
        username = jwt.decode(token, "your-secret-key", algorithms=["HS256"]).get("user_id")
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}, 401
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}, 401

    logs = RequestsLog().get_logs_by_username(username)

    return jsonify({
        "logs": [
            {
                "parameters": log.parameters,
                "result": log.result,
                "timestamp": log.timestamp.isoformat()
            }
            for log in logs
        ]
    })
