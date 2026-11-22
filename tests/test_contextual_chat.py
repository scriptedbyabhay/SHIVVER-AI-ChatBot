from modules.chatbot import initialize_chatbot, chat
from modules.conversation_manager import create_conversation

chatbot_data = initialize_chatbot()
conversation = create_conversation()

test_messages = [
    "Tell me about Midsommar",
    "Tell me more about it",
    "Who directed it?",
    "Recommend something similar"
]

for message in test_messages:

    print("\n" + "=" * 50)
    print("USER:", message)

    response = chat(
        chatbot_data,
        conversation,
        message
    )

    print("ASSISTANT:", response)