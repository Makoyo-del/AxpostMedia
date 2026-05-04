from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from schemas import *
from utils import get_unsplash_image, search_unsplash_images, create_image_grid, extract_keywords, log_structured
from rate_limiter import RateLimitMiddleware
from brain import generate_ai_caption, extract_smart_keywords, generate_carousel_story
import uvicorn

app = FastAPI(title="AxpostMedia API")

# Usage Analytics
USAGE_ANALYTICS = {
    "social_media_post": 0,
    "carousel_builder": 0,
    "blog_image_inserter": 0,
    "moodboard": 0,
    "quote_generator": 0
}

# Register global rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/callback")
async def oauth_callback(code: str = None):
    """
    Handles Unsplash OAuth callback.
    Redirect URIs whitelisted: urn:ietf:wg:oauth:2.0:oob (local) and production URL.
    """
    if not code:
        log_structured("oauth_callback_failed", {"reason": "missing_code"})
        return Response(status_code=400, content="Authorization code is missing")
    
    log_structured("oauth_callback_received", {"code_received": True})
    return {
        "status": "success", 
        "message": "Authentication successful (Public Access Only)",
        "scope": "public_access_only"
    }

@app.get("/stats")
async def get_stats():
    """Returns usage analytics."""
    return USAGE_ANALYTICS

@app.post("/social-media-post", response_model=SocialMediaResponse)
async def generate_social_post(request: SocialMediaRequest):
    USAGE_ANALYTICS["social_media_post"] += 1
    image_data = get_unsplash_image(request.keyword)
    
    if not image_data:
        return Response(status_code=404, content="Image not found")
    
    # AI-powered caption
    ai_caption = generate_ai_caption(request.keyword, request.platform)
    
    response = SocialMediaResponse(
        image_url=image_data["url"],
        caption=ai_caption,
        credit=image_data["credit"]
    )
    
    log_structured("generate_social_post", {"keyword": request.keyword, "platform": request.platform})
    return response

@app.post("/carousel-builder", response_model=CarouselResponse)
async def build_carousel(request: CarouselRequest):
    USAGE_ANALYTICS["carousel_builder"] += 1
    
    # AI-driven narrative sequence
    queries = generate_carousel_story(request.keyword, request.slides_count)
    
    images = []
    used_ids = set()
    
    for query in queries:
        # Try up to 3 times to get a unique image for this query
        for _ in range(3):
            img_data = get_unsplash_image(query)
            # We need the ID to check for duplicates. get_unsplash_image doesn't return it currently.
            # I'll update get_unsplash_image to return the ID.
            if img_data and img_data["url"] not in [i["url"] for i in images]:
                images.append(img_data)
                break
            
    image_urls = [img["url"] for img in images]
    credits = [img["credit"] for img in images]
    
    response = CarouselResponse(
        carousel_images=image_urls,
        overlay_text=f"The Journey of {request.keyword}",
        credits=credits
    )
    
    log_structured("build_carousel", {"keyword": request.keyword, "count": len(image_urls)})
    return response

@app.post("/blog-image-inserter", response_model=BlogResponse)
async def suggest_blog_images(request: BlogRequest):
    USAGE_ANALYTICS["blog_image_inserter"] += 1
    
    # AI-powered smart keyword extraction
    keywords = extract_smart_keywords(request.article_text)
    
    all_images = []
    for kw in keywords[:2]: # Get images for top 2 AI keywords
        img = get_unsplash_image(kw)
        if img:
            all_images.append(img)
            
    if not all_images:
        return Response(status_code=404, content="No relevant images found")
    
    response = BlogResponse(
        suggested_images=[img["url"] for img in all_images],
        credit=all_images[0]["credit"]
    )
    
    log_structured("blog_image_inserter", {"keywords": keywords})
    return response

@app.post("/moodboard", response_model=MoodboardResponse)
async def create_moodboard(request: MoodboardRequest):
    USAGE_ANALYTICS["moodboard"] += 1
    images = search_unsplash_images(request.keyword, count=4)
    image_urls = [img["url"] for img in images]
    credits = [img["credit"] for img in images]
    
    if len(image_urls) < 4:
        return Response(status_code=404, content="Not enough images found for a moodboard")
    
    # In a real app, create_image_grid would return a URL to a CDN-hosted image.
    # Here we simulate by returning the list of images.
    response = MoodboardResponse(
        moodboard_grid="Grid metadata generated",
        image_urls=image_urls,
        credits=credits
    )
    
    log_structured("create_moodboard", {"keyword": request.keyword})
    return response

@app.post("/quote-generator", response_model=QuoteResponse)
async def generate_quote_image(request: QuoteRequest):
    USAGE_ANALYTICS["quote_generator"] += 1
    image_data = get_unsplash_image(request.keyword, orientation="squarish")
    
    if not image_data:
        return Response(status_code=404, content="Image not found")
    
    response = QuoteResponse(
        image_with_overlay=image_data["url"],
        credit=image_data["credit"]
    )
    
    log_structured("quote_generator", {"quote_snippet": request.quote_text[:20]})
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
