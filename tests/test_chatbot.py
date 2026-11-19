from modules.chatbot import initialize_chatbot


chatbot_data = initialize_chatbot()

movies = chatbot_data["movies"]
tfidf_matrix = chatbot_data["tfidf_matrix"]

print("\n--- CHATBOT INITIALISATION ---")

print("Total movies:", len(movies))

print("TF-IDF matrix shape:", tfidf_matrix.shape)

print("\nInitialisation successful!")