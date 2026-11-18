def build_prompt(conversation_history, latest_message, movie_context = None):
    system_instruction = """
    You are The Horror Archive, an expert horror movie
    recommendation assistant.

    Your responsibilities:
    1. Help users discover horror movies.
    2. Understand their preferences and follow-up questions.
    3. Maintain context from previous messages.
    4. Give clear and concise explanations.
    5. Do not invent movie information.
    6. If you do not understand a request, ask for clarification.

    Stay focused on horror movies and related topics.
    """
    
    prompt = system_instruction
    
    prompt += "\n\nCONVERSATION HISTORY: \n"
    
    for message in conversation_history:
        role = message["role"].upper()
        content = message["content"]
        
        prompt += f"\n{role}: {content}"
        
    if movie_context:
        prompt += "\n\nAVAILABLE MOVIE INFORMATION: \n"
        prompt += movie_context
    
    prompt += "\n\nASSISTANT: "
    
    return prompt
    