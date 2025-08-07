from flask import Blueprint, request, jsonify
from API.services import power, fibonacci, factorial
from Records.models import MathRequest
from pydantic import ValidationError
from Database.storage import log_request
import jwt
from Utils.decorators import login_required
from Database.log_db import RequestsLog
import openai
from openai import OpenAIError
from Database.user_db import User
import os

math_bp = Blueprint('math', __name__)
openai.api_key = os.getenv("OPENAI_API_KEY") 

@math_bp.route('/api/assistant', methods=['POST'])
@login_required
def ai_assistant(user):
    if User.get_user_by_username(user) is None:
        return jsonify({"error": "user not found"}), 404

    try:
        data = request.get_json()

        if not data or 'messages' not in data:
            return jsonify({'error': 'Missing messages'}), 400

        base_dir = os.getcwd() 
        context_file_path = os.path.join(base_dir, 'context.txt')
        with open(context_file_path, 'r', encoding='utf-8') as f:
            system_content = f.read().strip()

        system_message = {
            "role": "system",
            "content": system_content
        }

        messages = data['messages']

        if messages and messages[0].get("role") == "system":
            messages[0] = system_message
        else:
            messages.insert(0, system_message)

        print("Received messages:", messages)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=100
        )

        reply = response['choices'][0]['message']['content']
        return jsonify({'reply': reply})

    except OpenAIError as e:
        return jsonify({'error': 'OpenAI API failed', 'details': str(e)}), 500

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@math_bp.route('/api/power', methods=['POST'])
@login_required
def calculate_power(user):
    try:
        data = MathRequest.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}),400

    if User.get_user_by_username(user) is None:
        return jsonify({"error": "User not found"}), 404
    
    if(data.a < -1000 or data.a > 1000 or data.b < -1000 or data.b > 1000):
        return jsonify({"error": "Invalid data"}), 405

    result = power(data.a, data.b)
    log_request('/power', [data.a, data.b], result, user)

    return jsonify({"result": result}), 200


@math_bp.route('/api/fibonacci', methods=['POST'])
@login_required
def calculate_fibonacci(user):
    try:
        data = MathRequest.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    if User.get_user_by_username(user) is None:
        return jsonify({"error": "User not found"}), 404
    
    if(data.a < 0 or data.a > 10000):
        return jsonify({"error": "Invalid data"}), 405

    result = fibonacci(data.a)
    log_request('/fibonacci', [data.a], result, user)
    
    return jsonify({"result": result}), 200


@math_bp.route('/api/factorial', methods=['POST'])
@login_required
def calculate_factorial(user):
    try:
        data = MathRequest.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    if User.get_user_by_username(user) is None:
        return jsonify({"error": "User not found"}), 404

    if(data.a < 0 or data.a > 170):
        return jsonify({"error": "Invalid data"}), 405

    result = factorial(data.a)
    log_request('/factorial', [data.a], result, user)

    return jsonify({"result": result}), 200

@math_bp.route('/api/<operation>/logs', methods=['GET'])
@login_required
def get_operation_logs(operation, user):

    if User.get_user_by_username(user) is None:
        return jsonify({"error": "User not found"}), 404


    allowed_operations = {'fibonacci', 'power', 'factorial'}
    if operation not in allowed_operations:
        return jsonify({"error": f"Unsupported operation '{operation}'"}), 400

    logs = RequestsLog().get_logs_by_username_and_endpoint(user, f'/{operation}')

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

