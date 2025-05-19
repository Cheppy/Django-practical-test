import os
from openai import OpenAI
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def translate_text(text: str, target_language: str) -> str:
    """
    Translate text using OpenAI's API
    
    Args:
        text: Text to translate
        target_language: Target language name
        
    Returns:
        str: Translated text
    """
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
            
        client = OpenAI(api_key=api_key)
        
        # Create a system message that specifies the target language
        system_message = f"You are a professional translator. Translate the following text to {target_language}. Maintain the original formatting and structure."
        
        # Make the API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text}
            ],
            temperature=0.3  # Lower temperature for more consistent translations
        )
        
        # Extract the translated text from the response
        translated_text = response.choices[0].message.content.strip()
        
        return translated_text
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise 