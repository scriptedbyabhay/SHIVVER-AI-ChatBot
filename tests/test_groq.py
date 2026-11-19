from modules.groq_client import generate_response

print("\nAsk me something: ")
prompt = input() 

try:
    answer = generate_response(prompt)

    print("\n--- GROQ RESPONSE ---")
    print(answer)

except Exception as error:
    print("\nSomething went wrong:")
    print(error)