from modules.chatbot import detect_intent

test_messages = [
    "Recommend movies similar to Hereditary",
    "Tell me about The Witch",
    "Search for Midsommar",
    "Suggest psychological horror movies",
    "Which movie has the highest rating?",
    "Hello!",
    "I want something completely different"
]

for message in test_messages:

    intent = detect_intent(message)

    print("\nUser:", message)
    print("Intent:", intent)