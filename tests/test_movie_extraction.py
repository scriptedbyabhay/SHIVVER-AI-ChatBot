from modules.chatbot import (
    initialize_chatbot,
    extract_movie_title
)

# Initialise chatbot
chatbot_data = initialize_chatbot()

movie_titles = chatbot_data["movie_titles"]

# Test messages
test_messages = [
    "Recommend movies similar to Hereditary",
    "I enjoyed The Witch. Suggest similar films.",
    "Can you recommend something like Midsommar?",
    "Suggest psychological horror movies",
    "I want movies similar to Talk to Me"
]

# Test extraction
for message in test_messages:

    result = extract_movie_title(
        message,
        movie_titles
    )

    print("\nUser:", message)
    print("Extracted movie:", result)