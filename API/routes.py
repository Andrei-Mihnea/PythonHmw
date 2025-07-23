from flask import Blueprint, request, jsonify
from API.services import power, fibonacci, factorial
from Records.models import MathRequest
from pydantic import ValidationError
from Database.storage import log_request

math_bp = Blueprint('math', __name__)

@math_bp.route('/power', methods=['POST'])
def calculate_power():
    try:
        data = MathRequest.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}),400
    
    result = power(data.a, data.b)

    log_request('/power', [data.a, data.b], result)
    return jsonify({"result": result}), 200


@math_bp.route('/fibonacci', methods=['POST'])
def calculate_fibonacci():
    try:
        data = MathRequest.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}),400
    
    result = fibonacci(data.a)
    
    log_request('/fibonacci', [data.a, data.b], result)
    return jsonify({"result": result}), 200


@math_bp.route('/factorial', methods=['POST'])
def calculate_factorial():
    try:
        data = MathRequest.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}),400

    result = factorial(data.a)
    
    log_request('/factorial', [data.a, data.b], result)
    return jsonify({"result": result}), 200