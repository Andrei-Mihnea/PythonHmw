from flask import Blueprint, request, jsonify
from app.services import power, fibonacci, factorial
from app.models import MathRequest
from pydantic import ValidationError
from app.storage import log_request

math_bp = Blueprint('math', __name__)

@math_bp.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = MathRequest.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}),400
    
    if data.operation == 'power':
        result = power(data.a, data.b)
    elif data.operation == 'fibonacci':
        result = fibonacci(data.a)
    elif data.operation == 'factorial':
        result = factorial(data.a)
    else:
        return jsonify({"error": "Invalid operation"}), 400
    
    log_request(data.operation, [data.a, data.b], result)
    return jsonify({"result": result}), 200