from flask import jsonify
from models.user import User
import jwt
import os
from datetime import datetime, timedelta

class AuthController:
    @staticmethod
    def register(data):
        try:
            # Check if user already exists
            if User.find_by_email(data['email']):
                return jsonify({'error': 'Email already registered'}), 400

            # Create new user
            user = User(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            user_id = user.save()

            return jsonify({
                'message': 'User registered successfully',
                'user_id': user_id
            }), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def login(data):
        try:
            user = User.find_by_email(data['email'])
            if not user or not User.verify_password(user['password'], data['password']):
                return jsonify({'error': 'Invalid email or password'}), 401

            # Generate JWT token
            token = jwt.encode(
                {'user_id': str(user['_id']), 'exp': datetime.utcnow() + timedelta(days=1)},
                os.getenv('JWT_SECRET_KEY', 'asma'),
                algorithm='HS256'
            )

            return jsonify({
                'user_id': str(user['_id']),
                'token': token
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500