import re
from modules.dataLoader import load_movies

from modules.recommend import (
    prepare_movie_text,
    build_tfidf_matrix,
    recommend_movies
)

from modules.conversation_manager import (
    create_conversation,
    add_message, 
    get_conversation_history
)

from modules.prompt_builder import build_prompt
from modules.llm_client import generate_response

def initialize_chatbot():
    movies = load_movies()
    
    movies = movies.reset_index(drop=True)
    
    movie_titles = (
        movies["title"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )
    
    prepared_movies = prepare_movie_text(movies)
    
    tfidf, tfidf_matrix = build_tfidf_matrix(
        prepared_movies
    )
    
    chatbot_data = {
        "movies": movies,
        "prepared_movies": prepared_movies,
        "movie_titles": movie_titles,
        "tfidf": tfidf,
        "tfidf_matrix": tfidf_matrix
    }
    
    return chatbot_data


def get_recommendations(chatbot_data, movie_title, limit = 5):
    movies = chatbot_data["movies"]
    tfidf_matrix = chatbot_data["tfidf_matrix"]
    
    recommendations = recommend_movies(
        movies, 
        tfidf_matrix,
        movie_title,
        limit
    )
    
    return recommendations

def format_movie_context(recommendations):
    movie_context = ""
    
    for _, movie in recommendations.iterrows():
        title = movie.get("title", "Unknown")
        year = movie.get("release_year", "Unknown")
        genres = movie.get("genre_names", "Unknown")
        overview = movie.get("overview", "No overview available")
        rating = movie.get("vote_average", "Unknown")
        similarity = movie.get("similarity_score", "Unknown")

        movie_context += f"""
        Movie: {title}
        Year: {year}
        Genres: {genres}
        Overview: {overview}
        Rating: {rating}
        Similarity Score: {similarity}

        """

    return movie_context

def extract_movie_title(user_message, movie_titles):
    excluded_titles = {
        "horror",
        "thriller",
        "drama", 
        "comedy",
        "action",
        "romance",
        "fantasy",
        "mystery",
        "documentary",
        "animation"
    }
    
    sorted_titles = sorted(
        movie_titles,
        key = len,
        reverse = True
    )
    
    for title in sorted_titles:
        if title.casefold() in excluded_titles:
            continue
        
        pattern = r"(?<!\w)" + re.escape(title) + r"(?!\w)"
        
        match = re.search(
            pattern,
            user_message,
            flags = re.IGNORECASE   
        )
        
        if match: 
            return title
        
    return None
    

def chat(chatbot_data, conversation, user_message):
    add_message(conversation, "user", user_message)
    
    # Identify user intent
    intent = detect_intent(user_message)
    
    # Extract movie title
    movie_title = extract_movie_title(
        user_message,
        chatbot_data["movie_titles"]
    )
    
    print("Detected intent: ", intent)
    print("Extracted movie: ", movie_title)
    
    # Handle greetings
    if intent == "greeting":
        response = (
            "Hello! Welcome to SHIVVER . . . "
            "Looking for your next sleep-losing watch?"
        )
        
        add_message(conversation, "assistant", response)
        return response
    
    # Handle similar movie recommendations
    elif intent == "recommend_similar":
        if movie_title is None:
            response = (
                "Which horror movie would you like "
                "me to find similar recommendations for?"
            )
            
            add_message(conversation, "assistant", response)
            return response
        
        recommendations = get_recommendations(
            chatbot_data,
            movie_title, 
            limit = 5
        )
        
        if recommendations.empty:
            response = (
                f"I couldn't find '{movie_title}' "
                "in my movie database."
            )
            
            add_message(conversation, "assistant", response)
            return response
        
        movie_context = format_movie_context(recommendations)
        history = get_conversation_history(conversation)
        
        prompt = build_prompt(
            history,
            user_message,
            movie_context
        )
        
        response = generate_response(prompt)
        add_message(conversation, "assistant", response)
        return response
    
    else:
        response = (
            "I understand your request, but I haven't "
            "implemented that functionality yet. "
            "Would you like recommendations for another movie?"
        )
        
        add_message(conversation, "assistant", response)
        return response
            
            
            
    movie_context = format_movie_context(recommendations)
    print("\n--- RETRIEVED MOVIE CONTEXT ---")
    print(movie_context)
    
    history = get_conversation_history(conversation)
    
    prompt = build_prompt(
        history, 
        user_message, 
        movie_context
    )
    
    response = generate_response(prompt)
    
    add_message(conversation, "assistant", response)
    return response


def detect_intent(user_message):
    message = user_message.casefold()
    
    if any(word in message for word in [
            "psychological horror",
            "supernatural horror",
            "slasher",
            "found footage",
            "horror movies"
        ]):
            return "recommend_by_genre"
        
    elif any(word in message for word in [
        "similar to", 
        "like", 
        "recommend",
        "recommendation",
        "suggest"
    ]):
        return "recommend_similar"
    
    elif any(word in message for word in [
        "tell me about",
        "information about", 
        "details about",
        "who directed"
    ]):
        return "movie_information"
    
    elif any(word in message for word in [
        "search", 
        "find",
        "look for"
    ]):
        return "search_movie"
    
    elif any(word in message for word in [
        "highest rated",
        "rating",
        "best rated",
        "top rated"
    ]):
        return "highest_rated"
    
    elif re.search(r"\b(hello|hi|hey)\b", message):
        return "greeting"
    
    return "unknown"