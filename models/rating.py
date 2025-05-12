from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['chat_app']

class Rating:
    def __init__(self, message_id, rating_value):
        if not isinstance(rating_value, int) or rating_value < 1 or rating_value > 5:
            raise ValueError("Rating value must be an integer between 1 and 5")
        self.message_id = message_id
        self.rating_value = rating_value
        self.created_at = datetime.utcnow()

    def save(self):
        rating_data = {
            'message_id': ObjectId(self.message_id),
            'rating_value': self.rating_value,
            'created_at': self.created_at
        }
        result = db.ratings.insert_one(rating_data)
        return str(result.inserted_id)

    @staticmethod
    def get_message_rating(message_id):
        ratings = list(db.ratings.find({'message_id': ObjectId(message_id)}))
        return [{
            'message_id': str(rating['message_id']),
            'rating_value': rating['rating_value'],
            'created_at': rating['created_at']
        } for rating in ratings]

    @staticmethod
    def get_average_rating(message_id):
        pipeline = [
            {'$match': {'message_id': ObjectId(message_id)}},
            {'$group': {
                '_id': '$message_id',
                'average_rating': {'$avg': '$rating_value'}
            }}
        ]
        result = list(db.ratings.aggregate(pipeline))
        return result[0]['average_rating'] if result else None

    @staticmethod
    def delete_message_ratings(message_id):
        db.ratings.delete_many({'message_id': ObjectId(message_id)})