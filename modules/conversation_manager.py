def create_conversation():
    conversation = {
        "messages": []
    }
    return conversation

def add_message(conversation, role, content):
    if role not in ("user", "assistant"):
        raise ValueError("Invalid message role.")
    
    if not content or not content.strip():
        raise ValueError("Message content cannot be empty.")
    
    message = {
        "role": role,
        "content": content.strip()
    }
    
    conversation["messages"].append(message)
    
def get_conversation_history(conversation, limit=5):
    # Limit set to 5 because large contexts increase API usage and may exceed the model's tokens
    messages = conversation["messages"]
    return messages[-limit:]