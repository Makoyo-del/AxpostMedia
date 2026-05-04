from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ImageCredit(BaseModel):
    name: str
    username: str
    link: str

class SocialMediaRequest(BaseModel):
    keyword: str
    platform: str

class SocialMediaResponse(BaseModel):
    image_url: str
    caption: str
    credit: ImageCredit

class CarouselRequest(BaseModel):
    keyword: str
    slides_count: int = 5

class CarouselResponse(BaseModel):
    carousel_images: List[str]
    overlay_text: str

class BlogRequest(BaseModel):
    article_text: str

class BlogResponse(BaseModel):
    suggested_images: List[str]
    credit: ImageCredit

class MoodboardRequest(BaseModel):
    keyword: str

class MoodboardResponse(BaseModel):
    moodboard_grid: str  # URL to a generated grid image or a layout description
    image_urls: List[str]

class QuoteRequest(BaseModel):
    quote_text: str
    keyword: Optional[str] = "nature"

class QuoteResponse(BaseModel):
    image_with_overlay: str
    credit: ImageCredit
