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
import os

math_bp = Blueprint('math', __name__)
openai.api_key = os.getenv("OPENAI_API_KEY") 

@math_bp.route('/api/assistant', methods=['POST'])
def ai_assistant():
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
        print("Received messages:", messages)

        if messages and messages[0].get("role") == "system":
            messages[0] = system_message
        else:
            messages.insert(0, system_message)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )

        reply = response['choices'][0]['message']['content']
        return jsonify({'reply': reply})

    except OpenAIError as e:
        return jsonify({'error': 'OpenAI API failed', 'details': str(e)}), 500

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

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

