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

from modules.searchandfind import (
    search_by_genre,
    search_by_title
)

from modules.filter_movies import filter_movies

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

def format_movie_context(movies):

    context = ""

    for _, movie in movies.iterrows():

        context += f"""
Movie: {movie.get('title', 'Unknown')}
Year: {movie.get('release_year', 'Unknown')}
Genres: {movie.get('genre_names', 'Unknown')}
Director: {movie.get('director', 'Unknown')}
Cast: {movie.get('top_5_cast', 'Unknown')}
Overview: {movie.get('overview', 'Unknown')}
Rating: {movie.get('vote_average', 'Unknown')}
"""

    return context

def has_explicit_title_cue(message, title):

    escaped_title = re.escape(title)

    pattern = (
        r"\b(?:about|movie|film|watch|called|named|"
        r"recommend|suggest|similar to)\s+"
        + escaped_title
        + r"\b"
    )

    return bool(
        re.search(pattern, message, flags=re.IGNORECASE)
    )

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
        
        # Common conversational words
        "who",
        "what",
        "when",
        "where",
        "why",
        "how",
        "tell",
        "about",
        "more",
        "the",
        "it",
        "me",
        "and",
        "for",
        "with",
        "something"
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
            ambiguous_titles = {
                "who", "what", "when", "where", "why", "how", "tell", "it", "the", "me"
            }
            
            if title.casefold() in ambiguous_titles:
                if not has_explicit_title_cue(user_message, title):
                    continue
            
            return title
        
    return None

def extract_referenced_movie(user_message, conversation):
    message = user_message.casefold()
    
    movie_list = conversation.get("last_shown_movies", [])
    
    if not movie_list:
        return None
    
    references = {
        "first": 0,
        "1st": 0,
        "second": 1,
        "2nd": 1,
        "third": 2,
        "3rd": 2,
        "fourth": 3,
        "4th": 3,
        "fifth": 4,
        "5th": 4,
        "last": len(movie_list) - 1
    }
    
    for reference, index in references.items():
        if re.search(r"\b" + re.escape(reference) + r"\b", message):
            if index < len(movie_list):
                return movie_list[index]
            
    return None

def get_last_mentioned_movie(conversation, movie_titles):
    previous_messages = conversation["messages"][:-1]
    
    for message in reversed(previous_messages):
        movie_title = extract_movie_title(
            message["content"],
            movie_titles
        )
        
        if movie_title is not None:
            return movie_title
    
    return None

def chat(chatbot_data, conversation, user_message):

    # --------------------------------------------------
    # 1. STORE USER MESSAGE
    # --------------------------------------------------

    add_message(conversation, "user", user_message)

    # --------------------------------------------------
    # 2. DETECT USER INTENT
    # --------------------------------------------------

    intent = detect_intent(user_message)

    contextual_intents = (
        "recommend_similar",
        "movie_information",
        "search_movie"
    )

    movie_title = None

    # --------------------------------------------------
    # 3. RESOLVE THE MOVIE REFERENCE
    # --------------------------------------------------

    # Priority 1: Positional reference
    # Example: "Tell me about the second one"

    if intent in contextual_intents:

        movie_title = extract_referenced_movie(
            user_message,
            conversation
        )

    # Priority 2: Explicit movie title
    # Example: "Tell me about Midsommar"

    if movie_title is None:

        extracted_title = extract_movie_title(
            user_message,
            chatbot_data["movie_titles"]
        )

        # Prevent common conversational words from
        # being mistaken for standalone movie titles.

        if extracted_title is not None:

            ambiguous_titles = {
                "who", "what", "when", "where",
                "why", "how", "tell", "it", "the", "me"
            }

            if extracted_title.casefold() in ambiguous_titles:

                message = user_message.casefold()
                title = extracted_title.casefold()

                explicit_cues = (
                    f"about {title}",
                    f"movie {title}",
                    f"film {title}",
                    f"called {title}",
                    f"named {title}",
                    f"{title} ("
                )

                if any(cue in message for cue in explicit_cues):
                    movie_title = extracted_title

            else:
                movie_title = extracted_title

    # Priority 3: Previously active movie

    if movie_title is None and intent in contextual_intents:

        movie_title = conversation.get("active_movie")

    # Update active movie only after resolving it.

    if movie_title is not None:
        conversation["active_movie"] = movie_title

    # --------------------------------------------------
    # 4. DEBUG INFORMATION
    # --------------------------------------------------

    print("\nDetected intent:", intent)
    print("Resolved movie:", movie_title)
    print("Active movie:", conversation.get("active_movie"))

    # --------------------------------------------------
    # 5. HELPER FOR LLM RESPONSES
    # --------------------------------------------------

    def generate_contextual_response(question, movie_context):

        # Include only the current question.
        # Previous recommendation lists are excluded.

        focused_question = question

        history = [
            {
                "role": "user",
                "content": focused_question
            }
        ]

        prompt = build_prompt(
            history,
            focused_question,
            movie_context
        )

        response = generate_response(prompt)

        add_message(conversation, "assistant", response)

        return response

    # --------------------------------------------------
    # 6. HANDLE GREETINGS
    # --------------------------------------------------

    if intent == "greeting":

        response = (
            "Hello! Welcome to SHIVVER . . . "
            "Looking for your next sleep-losing watch?"
        )

        add_message(conversation, "assistant", response)

        return response

    # --------------------------------------------------
    # 7. SIMILAR MOVIE RECOMMENDATIONS
    # --------------------------------------------------

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
            limit=5
        )

        if recommendations.empty:

            conversation["last_shown_movies"] = []

            response = (
                f"I couldn't find '{movie_title}' "
                "in my movie database."
            )

            add_message(conversation, "assistant", response)

            return response

        remember_shown_movies(
            conversation,
            recommendations
        )

        movie_context = format_movie_context(recommendations)

        question = (
            f"{user_message}\n\n"
            f"Reference movie: {movie_title}.\n"
            "Recommend only movies from the supplied movie context."
        )

        return generate_contextual_response(
            question,
            movie_context
        )

    # --------------------------------------------------
    # 8. GENRE-BASED RECOMMENDATIONS
    # --------------------------------------------------

    elif intent == "recommend_by_genre":

        genre = extract_genre(user_message)

        if genre is None:

            response = (
                "Which horror movie genre are you interested in?"
            )

            add_message(conversation, "assistant", response)

            return response

        recommendations = get_genre_recommendations(
            chatbot_data,
            genre,
            limit=5
        )

        if recommendations.empty:

            conversation["last_shown_movies"] = []

            response = (
                f"I couldn't find any movie belonging "
                f"to the {genre} genre."
            )

            add_message(conversation, "assistant", response)

            return response

        remember_shown_movies(
            conversation,
            recommendations
        )

        movie_context = format_movie_context(recommendations)

        question = (
            f"{user_message}\n\n"
            f"Requested genre: {genre}.\n"
            "Recommend only movies from the supplied movie context."
        )

        return generate_contextual_response(
            question,
            movie_context
        )

    # --------------------------------------------------
    # 9. MOVIE INFORMATION
    # --------------------------------------------------

    elif intent == "movie_information":

        if movie_title is None:

            response = (
                "Which horror movie would you like "
                "to know more about?"
            )

            add_message(conversation, "assistant", response)

            return response

        movie_information = get_movie_information(
            chatbot_data,
            movie_title
        )

        if movie_information.empty:

            response = (
                f"I couldn't find '{movie_title}' "
                "in my movie database."
            )

            add_message(conversation, "assistant", response)

            return response

        # Get the selected movie's database record.

        movie = movie_information.iloc[0]

        # --------------------------------------------------
        # 9A. ANSWER DIRECTOR QUESTIONS WITHOUT AN LLM
        # --------------------------------------------------

        message = user_message.casefold()

        director_question = any(
            phrase in message
            for phrase in (
                "who directed",
                "who is the director",
                "director",
                "filmmaker"
            )
        )

        if director_question:

            director = str(
                movie.get("director", "")
            ).strip()

            if director.casefold() in (
                "", "nan", "none", "<na>", "unknown", "n/a"
            ):
                response = (
                    f"I don't have director information for "
                    f"{movie_title} in my current database."
                )

            else:

                response = (
                    f"{movie_title} was directed by {director}."
                )

            add_message(conversation, "assistant", response)

            return response

        # --------------------------------------------------
        # 9B. ANSWER CAST QUESTIONS WITHOUT AN LLM
        # --------------------------------------------------

        cast_question = any(
            phrase in message
            for phrase in (
                "who acted",
                "who stars",
                "who starred",
                "cast",
                "actors",
                "actresses"
            )
        )

        if cast_question:

            cast = str(
                movie.get("top_5_cast", "")
            ).strip()

            if cast.casefold() in (
                "", "nan", "none", "<na>", "unknown", "n/a"
            ):

                response = (
                    f"I don't have cast information for "
                    f"{movie_title} in my current database."
                )

            else:

                response = (
                    f"The listed cast members of "
                    f"{movie_title} are: {cast}."
                )

            add_message(conversation, "assistant", response)

            return response

        # --------------------------------------------------
        # 9C. GENERATE MOVIE EXPLANATION
        # --------------------------------------------------

        movie_context = format_movie_context(
            movie_information
        )

        question = (
            f"{user_message}\n\n"
            f"THE SELECTED MOVIE IS: {movie_title}.\n"
            "Answer exclusively about this movie. "
            "Use only the supplied movie information. "
            "Do not substitute another movie from earlier "
            "conversation messages. If information is missing, "
            "say that it is unavailable."
        )

        return generate_contextual_response(
            question,
            movie_context
        )

    # --------------------------------------------------
    # 10. SEARCH FOR MOVIES
    # --------------------------------------------------

    elif intent == "search_movie":

        if movie_title is None:

            response = (
                "Which movie would you like me to search for?"
            )

            add_message(conversation, "assistant", response)

            return response

        search_results = get_movie_search_results(
            chatbot_data,
            movie_title,
            limit=5
        )

        if search_results.empty:

            conversation["last_shown_movies"] = []

            response = (
                f"I couldn't find '{movie_title}' "
                "in my movie database."
            )

            add_message(conversation, "assistant", response)

            return response

        remember_shown_movies(
            conversation,
            search_results
        )

        movie_context = format_movie_context(search_results)

        question = (
            f"{user_message}\n\n"
            f"Search query: {movie_title}.\n"
            "Use only the supplied search results."
        )

        return generate_contextual_response(
            question,
            movie_context
        )

    # --------------------------------------------------
    # 11. HIGHEST-RATED MOVIES
    # --------------------------------------------------

    elif intent == "highest_rated":

        recommendations = get_highest_rated_movies(
            chatbot_data,
            limit=5
        )

        if recommendations.empty:

            conversation["last_shown_movies"] = []

            response = (
                "I couldn't find any sufficiently rated "
                "movies in my database."
            )
            add_message(conversation, "assistant", response)

            return response

        remember_shown_movies(
            conversation,
            recommendations
        )

        movie_context = format_movie_context(recommendations)

        question = (
            f"{user_message}\n\n"
            "Present the highest-rated movies from the "
            "supplied movie context. Do not add other titles."
        )

        return generate_contextual_response(
            question,
            movie_context
        )

    # --------------------------------------------------
    # 12. UNKNOWN INTENT
    # --------------------------------------------------

    else:

        response = (
            "I understand your request, but I haven't "
            "implemented that functionality yet. "
            "Would you like recommendations for another movie?"
        )

        add_message(conversation, "assistant", response)

        return response

def remember_shown_movies(conversation, movies):

    if movies.empty:
        conversation["last_shown_movies"] = []
        return

    conversation["last_shown_movies"] = (
        movies["title"]
        .dropna()
        .tolist()
    )

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
        
    elif any(phrase in message for phrase in [
        "similar to",
        "something similar",
        "like that",
        "another movie like",
        "recommend",
        "recommendation",
        "suggest"
    ]):
        return "recommend_similar"
    
    elif any(phrase in message for phrase in [
        "tell me about",
        "tell me more",
        "more about it",
        "information about",
        "details about",
        "who directed",
        "who is the director",
        "what is it about",
        "its cast"
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


def extract_genre(user_message):
    message = user_message.casefold()
    
    genre_keywords = [
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
    ]
    
    for genre in genre_keywords:
        pattern = r"\b" + re.escape(genre) + r"\b"
        
        if re.search(pattern, message):
            return genre
        
    return None

def get_genre_recommendations(chatbot_data, genre, limit = 5):
    movies = chatbot_data["movies"]
    
    results = search_by_genre(movies, genre)
    
    if results.empty:
        return results
    
    results = results.sort_values(
        by = "vote_average",
        ascending = False
    )
    
    return results.head(limit)


def get_movie_information(chatbot_data, movie_title):
    movies = chatbot_data["movies"]
    
    results = search_by_title(movies, movie_title)
    
    if results.empty:
        return results
    
    exact_match = results[
        results["title"].str.casefold() == movie_title.casefold()
    ]
    
    if not exact_match.empty:
        return exact_match.head(1)
    
    
    return results.head(1)

def get_movie_search_results(chatbot_data, search_query, limit = 5):
    movies = chatbot_data["movies"]
    
    results = search_by_title(movies, search_query)
    
    if results.empty:
        return results
    
    return results.head(limit)

def get_highest_rated_movies(chatbot_data, limit = 10):
    movies = chatbot_data["movies"]
    
    filtered_movies = filter_movies(
        movies, 
        min_votes = 100
    )
    
    if filtered_movies.empty:
        return filtered_movies
    
    highest_rated = filtered_movies.sort_values(
        by = "vote_average",
        ascending = False
    )
    
    return highest_rated.head(limit)

