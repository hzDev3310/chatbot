from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['chat_app']

class User:
    def __init__(self, username, email, password, role="user"):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        if role not in ["user", "client"]:
            raise ValueError("Role must be either 'user' or 'client'")
        self.role = role
        self.created_at = datetime.utcnow()

    def save(self):
        user_data = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'created_at': self.created_at
        }
        result = db.users.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        return db.users.find_one({'email': email})

    @staticmethod
    def find_by_id(user_id):
        return db.users.find_one({'_id': ObjectId(user_id)})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)