from modules.conversation_manager import (
    create_conversation,
    add_message,
    get_conversation_history
)

from modules.prompt_builder import build_prompt


# Create conversation
conversation = create_conversation()

# Add previous messages
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

# Latest user message
latest_message = "Which one is the most disturbing?"

# Retrieve history
history = get_conversation_history(conversation)

# Construct prompt
prompt = build_prompt(history, latest_message)

print("\n--- GENERATED PROMPT ---")
print(prompt)