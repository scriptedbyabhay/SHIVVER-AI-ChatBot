from modules.chatbot import (
    initialize_chatbot,
    get_recommendations
)

# Initialise the recommendation system
chatbot_data = initialize_chatbot()

# Get recommendations
results = get_recommendations(
    chatbot_data,
    "Hereditary",
    limit=5
)

print("\n--- MOVIE RECOMMENDATIONS ---")

if results.empty:
    print("No recommendations found.")

else:
    for _, movie in results.iterrows():
        print("\nMovie:", movie["title"])
        print("Similarity:", round(movie["similarity_score"], 3))
        print("Overview:", movie["overview"])