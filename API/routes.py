from flask import Blueprint, request, jsonify
from API.services import power, fibonacci, factorial
from Records.models import MathRequest
from pydantic import ValidationError
from Database.storage import log_request
import jwt
from Utils.decorators import login_required
from Database.log_db import RequestsLog

math_bp = Blueprint('math', __name__)

@math_bp.route('/api/power', methods=['POST'])
def calculate_power():
    try:
        data = MathRequest.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}),400
    
    result = power(data.a, data.b)

    token = request.cookies.get("access_token")
    username = jwt.decode(token, "your-secret-key", algorithms=["HS256"]).get("user_id")
    log_request('/power', [data.a, data.b], result, username)
    return jsonify({"result": result}), 200


@math_bp.route('/api/fibonacci', methods=['POST'])
def calculate_fibonacci():
    try:
        data = MathRequest.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}),400
    
    result = fibonacci(data.a)
    
    token = request.cookies.get("access_token")
    username = jwt.decode(token, "your-secret-key", algorithms=["HS256"]).get("user_id")
    log_request('/fibonacci', [data.a], result, username)
    return jsonify({"result": result}), 200


@math_bp.route('/api/factorial', methods=['POST'])
def calculate_factorial():
    try:
        data = MathRequest.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}),400

    result = factorial(data.a)
    
    token = request.cookies.get("access_token")
    username = jwt.decode(token, "your-secret-key", algorithms=["HS256"]).get("user_id")
    log_request('/factorial', [data.a], result, username)
    return jsonify({"result": result}), 200

@math_bp.route('/api/<operation>/logs', methods=['GET'])
@login_required
def get_operation_logs(operation):
    token = request.cookies.get("access_token")
    if not token:
        return {"error": "Unauthorized"}, 401

    try:
        username = jwt.decode(token, "your-secret-key", algorithms=["HS256"]).get("user_id")
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}, 401
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}, 401

    # Sanitize and map operation
    allowed_operations = {'fibonacci', 'power', 'factorial'}
    if operation not in allowed_operations:
        return jsonify({"error": f"Unsupported operation '{operation}'"}), 400

    logs = RequestsLog().get_logs_by_username_and_endpoint(username, f'/{operation}')

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

