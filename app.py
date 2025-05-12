from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.auth_controller import AuthController
from controllers.chat_controller import ChatController
from middleware.auth_middleware import token_required
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Auth routes
@app.route('/auth/register', methods=['POST'])
def register():
    return AuthController.register(request.get_json())

@app.route('/auth/login', methods=['POST'])
def login():
    return AuthController.login(request.get_json())

# Chat routes
@app.route('/chat/generate', methods=['POST'])
@token_required
def generate(current_user):
    try:
        data = request.get_json()
        data['user_id'] = str(current_user['_id'])
        return ChatController.generate_response(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat/history', methods=['GET'])
@token_required
def get_history(current_user):
    try:
        user_id = str(current_user['_id'])
        return ChatController.get_history(user_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat/clear', methods=['POST'])
@token_required
def clear_history(current_user):
    try:
        user_id = str(current_user['_id'])
        return ChatController.clear_history(user_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat/rate', methods=['POST'])
@token_required
def rate_message(current_user):
    try:
        data = request.get_json()
        return ChatController.rate_message(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)