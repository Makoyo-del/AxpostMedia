from fastapi import FastAPI, Response
from schemas import *
from utils import get_unsplash_image, search_unsplash_images, create_image_grid, extract_keywords, log_structured
from rate_limiter import RateLimitMiddleware
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

@app.get("/")
async def root():
    return {"message": "Welcome to AxpostMedia API"}

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
    orientation = "squarish" if request.platform.lower() in ["instagram", "facebook"] else "landscape"
    image_data = get_unsplash_image(request.keyword, orientation=orientation)
    
    if not image_data:
        return Response(status_code=404, content="Image not found")
    
    response = SocialMediaResponse(
        image_url=image_data["url"],
        caption=f"Check out this amazing visual for {request.keyword}! #VisualFlow #{request.platform}",
        credit=image_data["credit"]
    )
    
    log_structured("generate_social_post", {"keyword": request.keyword, "platform": request.platform})
    return response

@app.post("/carousel-builder", response_model=CarouselResponse)
async def build_carousel(request: CarouselRequest):
    USAGE_ANALYTICS["carousel_builder"] += 1
    images = search_unsplash_images(request.keyword, count=request.slides_count)
    image_urls = [img["url"] for img in images]
    
    response = CarouselResponse(
        carousel_images=image_urls,
        overlay_text=f"The Story of {request.keyword}"
    )
    
    log_structured("build_carousel", {"keyword": request.keyword, "count": len(image_urls)})
    return response

@app.post("/blog-image-inserter", response_model=BlogResponse)
async def insert_blog_images(request: BlogRequest):
    USAGE_ANALYTICS["blog_image_inserter"] += 1
    keywords = extract_keywords(request.article_text)
    query = " ".join(keywords) if keywords else "blog"
    
    image_data = get_unsplash_image(query, orientation="landscape")
    
    if not image_data:
        return Response(status_code=404, content="No images suggested")
    
    response = BlogResponse(
        suggested_images=[image_data["url"]],
        credit=image_data["credit"]
    )
    
    log_structured("blog_image_inserter", {"keywords": keywords})
    return response

@app.post("/moodboard", response_model=MoodboardResponse)
async def create_moodboard(request: MoodboardRequest):
    USAGE_ANALYTICS["moodboard"] += 1
    images = search_unsplash_images(request.keyword, count=4)
    image_urls = [img["url"] for img in images]
    
    if len(image_urls) < 4:
        return Response(status_code=404, content="Not enough images found for a moodboard")
    
    # In a real app, create_image_grid would return a URL to a CDN-hosted image.
    # Here we simulate by returning the list of images.
    response = MoodboardResponse(
        moodboard_grid="Grid metadata generated",
        image_urls=image_urls
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
