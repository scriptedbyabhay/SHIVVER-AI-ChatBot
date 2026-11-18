import logging

from modules.gemini_client import(
    generate_response as gemini_response
)

from modules.groq_client import(
    generate_response as groq_response
)

# CONFIGURE LOGGING
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def generate_response(prompt: str) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("PROMPT CANNOT BE EMPTY.")
    
    try:
        logger.info("Trying Gemini . . .")
        response = gemini_response(prompt)
        
        logger.info("Gemini responded successfully.")
        return response
    
    except Exception as gemini_error:
        if not is_retryable_error(gemini_error):
            raise
        
        logger.warning(
            "Gemini temporarily unavailable: %s", 
            gemini_error
        )
        
        try: 
            logger.info("Switching to Groq . . . ")
            response = groq_response(prompt)
            
            logger.info("Groq responded successfully.")
            return response
        
        except Exception as groq_error:
            logger.error("Groq also failed: %s", groq_error)
            
            raise RuntimeError(
                "Something went wrong."
            ) from groq_error

def is_retryable_error(error):
    # check whether an error is temporary and if another AI provider could be tried
    
    # HTTP status codes that may indicate temporary failures
    status_code = getattr(error, "status_code", None)
    
    if status_code is None:
        status_code = getattr(error, "code", None)
    
    retryable_status_codes = {
        408, 429, 500, 502, 503, 504
    }
    
    if status_code in retryable_status_codes:
        return True
    
    retryable_errors = {
        "APIConnectionError", 
        "APITimeoutError",
        "Timeout",
        "TimeoutError",
        "ConnectionError"
    }
    
    return type(error).__name__ in retryable_errors


def generate_response(prompt: str) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("PROMPT CANNOT BE EMPTY.")
    
    try:
        logger.info("Trying Gemini . . .")
        response = gemini_response(prompt)
        
        logger.info("Gemini responded successfully.")
        return response
    
    except Exception as gemini_error:
        if not is_retryable_error(gemini_error):
            raise
        
        logger.warning(
            "Gemini temporarily unavailable: %s", 
            gemini_error
        )
        
        try: 
            logger.info("Switching to Groq . . . ")
            response = groq_response(prompt)
            
            logger.info("Groq responded successfully.")
            return response
        
        except Exception as groq_error:
            logger.error("Groq also failed: %s", groq_error)
            
            raise RuntimeError(
                "Something went wrong."
            ) from groq_error