from modules.chatbot import initialize_chatbot, chat
from modules.conversation_manager import create_conversation

chatbot_data = initialize_chatbot()
conversation = create_conversation()

test_messages = [
    "Recommend psychological horror movies",
    "Tell me more about the second one",
    "Who directed it?",
    "Recommend something similar"
]

for message in test_messages:

    print("\n" + "=" * 55)
    print("USER:", message)

    response = chat(
        chatbot_data,
        conversation,
        message
    )

    print("ASSISTANT:", response)

    print(
        "ACTIVE MOVIE:",
        conversation["active_movie"]
    )

    print(
        "LAST SHOWN MOVIES:",
        conversation["last_shown_movies"]
    )