import os
import requests
import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
UTM_PARAMS = "?utm_source=visualflow&utm_medium=referral"

# Simple in-memory cache for graceful fallbacks
IMAGE_CACHE = {
    "nature": {
        "url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05" + UTM_PARAMS,
        "credit": {"name": "Pexels", "username": "pexels", "link": "https://unsplash.com/@pexels"}
    },
    "tech": {
        "url": "https://images.unsplash.com/photo-1518770660439-4636190af475" + UTM_PARAMS,
        "credit": {"name": "Alex Knight", "username": "agk_97", "link": "https://unsplash.com/@agk_97"}
    },
    "default": {
        "url": "https://images.unsplash.com/photo-1497215728101-856f4ea42174" + UTM_PARAMS,
        "credit": {"name": "Unsplash", "username": "unsplash", "link": "https://unsplash.com"}
    }
}

def get_unsplash_image(query: str, orientation: str = "squarish"):
    """
    Fetches a random image from Unsplash based on a query.
    Orientations: landscape (16:9), portrait (4:5), squarish (1:1)
    """
    url = "https://api.unsplash.com/photos/random"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {
        "query": query,
        "orientation": orientation
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        
        # Trigger download endpoint (Unsplash requirement)
        download_location = data["links"]["download_location"]
        requests.get(download_location, headers=headers)
        
        # Update cache with fresh result
        result = {
            "url": data["urls"]["regular"] + UTM_PARAMS,
            "credit": {
                "name": data["user"]["name"],
                "username": data["user"]["username"],
                "link": data["user"]["links"]["html"] + UTM_PARAMS
            }
        }
        IMAGE_CACHE[query.lower()] = result
        return result
    
    # Fallback logic
    return IMAGE_CACHE.get(query.lower(), IMAGE_CACHE["default"])

def overlay_text_on_image(image_url: str, text: str):
    """
    Overlays text on an image using Pillow.
    Returns a bytes object of the image.
    In a real app, this would be saved to a CDN or returned as a stream.
    """
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)
    
    # Basic styling
    width, height = img.size
    font_size = int(height / 15)
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((width - text_width) / 2, (height - text_height) / 2)
    
    # Draw shadow
    draw.text((position[0]+2, position[1]+2), text, font=font, fill="black")
    # Draw text
    draw.text(position, text, font=font, fill="white")
    
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def search_unsplash_images(query: str, count: int = 4, orientation: str = "squarish"):
    """Fetches multiple images from Unsplash."""
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {
        "query": query,
        "per_page": count,
        "orientation": orientation
    }
    
    response = requests.get(url, headers=headers, params=params)
    results = []
    if response.status_code == 200:
        data = response.json()
        for item in data.get("results", []):
            # Trigger download
            download_location = item["links"]["download_location"]
            requests.get(download_location, headers=headers)
            
            results.append({
                "url": item["urls"]["regular"] + UTM_PARAMS,
                "credit": {
                    "name": item["user"]["name"],
                    "username": item["user"]["username"],
                    "link": item["user"]["links"]["html"] + UTM_PARAMS
                }
            })
    return results

def create_image_grid(image_urls: list):
    """Creates a 2x2 grid from a list of 4 image URLs."""
    images = []
    for url in image_urls:
        response = requests.get(url)
        images.append(Image.open(BytesIO(response.content)).resize((512, 512)))
    
    grid = Image.new('RGB', (1024, 1024))
    grid.paste(images[0], (0, 0))
    grid.paste(images[1], (512, 0))
    grid.paste(images[2], (0, 512))
    grid.paste(images[3], (512, 512))
    
    img_byte_arr = BytesIO()
    grid.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def extract_keywords(text: str):
    """Very basic keyword extraction: filter out common stop words."""
    stop_words = {"the", "a", "an", "and", "is", "of", "to", "in", "for", "with", "on", "at", "by", "from", "up", "about", "into", "over", "after"}
    words = text.lower().split()
    keywords = [w for w in words if w.isalnum() and w not in stop_words]
    # Return top 3 most common or just first 3 for simplicity
    return keywords[:3]

def log_structured(event: str, data: dict):
    """Logs a structured JSON message."""
    log_entry = {
        "timestamp": os.getenv("CURRENT_TIME", "2026-05-04T19:30:00Z"),
        "event": event,
        "payload": data
    }
    print(json.dumps(log_entry))
