from modules.conversation_manager import (
    create_conversation,
    add_message,
    get_conversation_history
)

# Create a new conversation
conversation = create_conversation()

# Add messages
add_message(
    conversation,
    "user",
    "Recommend supernatural horror movies."
)

add_message(
    conversation,
    "assistant",
    "I recommend The Conjuring, Insidious and Hereditary."
)

add_message(
    conversation,
    "user",
    "Which one is the most disturbing?"
)

add_message(
    conversation,
    "assistant",
    "Hereditary is particularly disturbing."
)

# Display conversation history
history = get_conversation_history(conversation)

print("\n--- CONVERSATION HISTORY ---")

for message in history:
    print(f"{message['role']}: {message['content']}")