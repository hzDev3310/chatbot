from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['chat_app']

class Conversation:
    def __init__(self, user_id, chat_id=None):
        self.user_id = user_id
        self.chat_id = chat_id or str(ObjectId())
        self.created_at = datetime.utcnow()

    def save(self):
        conversation_data = {
            'user_id': ObjectId(self.user_id),
            'chat_id': self.chat_id,
            'created_at': self.created_at
        }
        result = db.conversations.insert_one(conversation_data)
        return str(result.inserted_id)

    @staticmethod
    def get_user_history(user_id):
        conversations = list(db.conversations.find(
            {'user_id': ObjectId(user_id)}
        ))
        return [{'user_id': str(conv['user_id']), 'chat_id': conv['chat_id'], 'created_at': conv['created_at']} for conv in conversations]

    @staticmethod
    def clear_history(user_id):
        db.conversations.delete_many({'user_id': ObjectId(user_id)})