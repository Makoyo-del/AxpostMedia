import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_ai_caption(keyword, platform):
    """Generates a high-engagement caption using Groq Llama-3."""
    prompt = f"Generate a short, engaging {platform} caption for a post about '{keyword}'. Use relevant emojis and a tone suitable for the platform."
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a creative social media manager."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=100
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq Error: {e}")
        return f"Explore the beauty of {keyword}! ✨"

def extract_smart_keywords(text):
    """Extracts the top 3 visual keywords from a blog text using Groq."""
    prompt = f"Extract the 3 most visually descriptive keywords from the following text for image searching. Return ONLY the keywords separated by commas:\n\n{text}"
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a visual researcher."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=50
        )
        keywords = chat_completion.choices[0].message.content.strip()
        return [k.strip() for k in keywords.split(",")]
    except Exception as e:
        print(f"Groq Error: {e}")
        return ["business", "technology", "nature"] # Safe fallbacks

def generate_carousel_story(keyword, count):
    """Generates a narrative sequence of search queries for a carousel."""
    prompt = f"Create a narrative sequence of {count} image search queries for a carousel about '{keyword}'. Each query should represent a different phase of a story. Return ONLY the queries separated by commas."
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a visual storyteller."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.5,
            max_tokens=150
        )
        queries = chat_completion.choices[0].message.content.strip()
        return [q.strip() for q in queries.split(",")]
    except Exception as e:
        print(f"Groq Error: {e}")
        return [keyword] * count
