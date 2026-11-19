from modules.llm_client import generate_response

prompt = """
You are a horror movie expert.
Suggest three supernatural horror movies.
Give one short reason for each recommendation.
"""

try:
    answer = generate_response(prompt)

    print("\n--- HORROR ARCHIVE AI RESPONSE ---")
    print(answer)

except Exception as error:
    print("\nSomething went wrong:")
    print(error)