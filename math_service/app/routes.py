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
    