from modules.chatbot import (
    initialize_chatbot,
    chat,
    extract_genre
)

from modules.conversation_manager import create_conversation


chatbot_data = initialize_chatbot()

conversation = create_conversation()


test_messages = [
    "Suggest some horror movies",
    "Recommend some thriller movies",
    "I want to watch comedy movies"
]


for message in test_messages:

    print("\n" + "=" * 50)
    print("USER:", message)

    print("Extracted genre:", extract_genre(message))

    response = chat(
        chatbot_data,
        conversation,
        message
    )

    print("\nASSISTANT:", response)