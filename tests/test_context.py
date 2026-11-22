from modules.chatbot import (
    get_last_mentioned_movie,
    initialize_chatbot
)

from modules.conversation_manager import (
    create_conversation,
    add_message
)

chatbot_data = initialize_chatbot()
conversation = create_conversation()

# Simulate an earlier conversation.
add_message(
    conversation,
    "user",
    "Recommend a psychological horror movie."
)

add_message(
    conversation,
    "assistant",
    "You should watch Midsommar. It is a disturbing psychological horror film."
)

# Simulate the current user query.
add_message(
    conversation,
    "user",
    "Tell me more about it."
)

movie = get_last_mentioned_movie(
    conversation,
    chatbot_data["movie_titles"]
)

print("Retrieved movie:", movie)