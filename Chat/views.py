import json
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

from modules.chatbot import initialize_chatbot, chat
from modules.conversation_manager import create_conversation

logger = logging.getLogger(__name__)

# Initialize chatbot data once per application process
_chatbot_data = None

def get_chatbot_data():
    global _chatbot_data
    
    if _chatbot_data is None:
        _chatbot_data = initialize_chatbot()
        
    return _chatbot_data

# Display the SHIVVER homepage
@ensure_csrf_cookie
def home(request):
    return render(request, 'chat/index.html')


# Handle incoming chat messages
@require_POST
def chat_api(request):
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "")
        
        if not isinstance(user_message, str) or not user_message.strip():
            return JsonResponse(
                {"error": "Please enter a valid message."}, 
                status=400
            )
            
        # Retrieve existing conversation
        conversation = request.session.get("shivver_conversation")
        
        
        # Create a new conversation if none exists
        if conversation is None:
            conversation = create_conversation()
            
        # Initialize chatbot data when first needed
        chatbot_data = get_chatbot_data()
        
        # Process the user's message
        response = chat(
            chatbot_data,
            conversation,
            user_message.strip()
        )
        
        
        # Save uploaded conversation in Django session
        request.session["shivver_conversation"] = conversation
        
        return JsonResponse({
            "response": response
        })
        
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid request format."},
            status = 400
        )
        
    except Exception:
        logger.exception("Request failed.")
        
        return JsonResponse(
            {"error": "Something went wrong. Please try again."},
            status = 500
        )