from flask import jsonify
from models.conversation import Conversation
from models.chat_interaction import ChatInteraction
from models.rating import Rating
from utils import generate_content

class ChatController:
    @staticmethod
    def generate_response(data):
        try:
            user_id = data.get('user_id')
            prompt = data.get('prompt')
            chat_id = data.get('chat_id')
            
            if not user_id or not prompt:
                return jsonify({'error': 'Missing required fields'}), 400

            # Create or get conversation
            if not chat_id:
                conversation = Conversation(user_id)
                conversation.save()
                chat_id = conversation.chat_id

            # Generate AI response
            ai_response = generate_content(prompt)

            # Save chat interaction
            chat = ChatInteraction(chat_id, prompt, ai_response, 'user')
            chat.save()

            return jsonify({
                'response': ai_response,
                'chat_id': chat_id,
                'success': True
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_history(user_id):
        try:
            if not user_id:
                return jsonify({'error': 'User ID is required'}), 400

            conversations = Conversation.get_user_history(user_id)
            history = {}

            for conv in conversations:
                chat_id = conv['chat_id']
                messages = ChatInteraction.get_chat_messages(chat_id)
                history[chat_id] = messages

            return jsonify({'history': history}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def clear_history(user_id):
        try:
            if not user_id:
                return jsonify({'error': 'User ID is required'}), 400

            conversations = Conversation.get_user_history(user_id)
            for conv in conversations:
                ChatInteraction.delete_chat_messages(conv['chat_id'])
            Conversation.clear_history(user_id)

            return jsonify({
                'message': 'Chat history cleared successfully'
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def rate_message(data):
        try:
            message_id = data.get('message_id')
            rating_value = data.get('rating')

            if not message_id or not rating_value:
                return jsonify({'error': 'Message ID and rating are required'}), 400

            rating = Rating(message_id, rating_value)
            rating.save()

            average_rating = Rating.get_average_rating(message_id)

            return jsonify({
                'message': 'Rating saved successfully',
                'average_rating': average_rating
            }), 200

        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500