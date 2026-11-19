from modules.gemini_client import generate_response

prompt = "Introduce yourself as a horror movie expert in two sentences."

try:
    answer = generate_response(prompt)

    print("\n--- GEMINI RESPONSE ---")
    print(answer)

except Exception as error:
    print("\nSomething went wrong:")
    print(error)