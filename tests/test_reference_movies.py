from modules.chatbot import extract_referenced_movie
from modules.conversation_manager import create_conversation

conversation = create_conversation()

conversation["last_shown_movies"] = [
    "Midsommar",
    "The Witch",
    "Hereditary",
    "The Lighthouse",
    "The Wailing"
]

test_messages = [
    "Tell me more about the first one",
    "Who directed the second one?",
    "Tell me about the third movie",
    "What about the last one?"
]

for message in test_messages:

    movie = extract_referenced_movie(
        message,
        conversation
    )

    print("\nUSER:", message)
    print("RETRIEVED MOVIE:", movie)