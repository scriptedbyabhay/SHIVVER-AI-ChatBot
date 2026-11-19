from modules.chatbot import (
    initialize_chatbot,
    chat
)

from modules.conversation_manager import create_conversation


# Initialise chatbot
chatbot_data = initialize_chatbot()

# Create a new conversation
conversation = create_conversation()

test_messages = [
    "Hello!",
    "Recommend movies similar to Hereditary",
    "Suggest something similar to The Witch",
    "Suggest psychological horror movies",
    "Tell me about Midsommar"
]

for message in test_messages:

    print("\n" + "=" * 50)
    print("USER:", message)


    # Generate chatbot response
    response = chat(
        chatbot_data,
        conversation,
        message
    )

    print("\nASSISTANT: ", response)
    
