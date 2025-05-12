from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from models.rating import Rating

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['chat_app']

class ChatInteraction:
    def __init__(self, conversation_id, prompt, response, sender_type):
        self.conversation_id = conversation_id
        self.prompt = prompt
        self.response = response
        if sender_type not in ["assistant", "user"]:
            raise ValueError("sender_type must be either 'assistant' or 'user'")
        self.sender_type = sender_type
        self.created_at = datetime.utcnow()

    def save(self):
        message_data = {
            'conversation_id': self.conversation_id,
            'prompt': self.prompt,
            'response': self.response,
            'sender_type': self.sender_type,
            'created_at': self.created_at
        }
        result = db.messages.insert_one(message_data)
        return str(result.inserted_id)

    @staticmethod
    def get_chat_messages(conversation_id):
        messages = list(db.messages.find({'conversation_id': conversation_id}))
        msgs = [{
            'id': str(msg['_id']),
            'conversation_id': msg['conversation_id'],
            'prompt': msg['prompt'],
            'response': msg['response'],
            'sender_type': msg['sender_type'],
            'created_at': msg['created_at'],
            "rating": Rating.get_message_rating(str(msg['_id']))[0]['rating_value'] if Rating.get_message_rating(str(msg['_id'])) else 0,
        } for msg in messages]
        return msgs
      

    @staticmethod
    def delete_chat_messages(conversation_id):
        db.messages.delete_many({'conversation_id': conversation_id})