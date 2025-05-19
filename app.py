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
def generate():
    try:
        data = request.get_json()
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                user = jwt.decode(token, os.getenv('JWT_SECRET_KEY', 'asma'), algorithms=['HS256'])
                data['user_id'] = str(user['user_id'])
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401
        
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