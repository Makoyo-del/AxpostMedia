# AxpostMedia 🎨✨

**AxpostMedia** is a premium visual content generation platform designed for freelancers and SMEs. Powered by the Unsplash API and FastAPI, it automates the creation of stunning social media posts, visual carousels, blog imagery, and moodboards with high-end glassmorphic aesthetics.

---

## 🚀 Key Features

### 1. Social Media Post Generator
Generate platform-optimized visuals (Instagram, Facebook, LinkedIn, Twitter/X) with creative captions and required Unsplash attribution.

### 2. Smart Visual Carousel Builder
Create a cohesive sequence of images for storytelling or product showcases with a single keyword.

### 3. Blog & Newsletter Image Inserter
Analyze your article text using NLP to extract relevant keywords and suggest the perfect landscape visuals for your newsletter.

### 4. Moodboard Tool
Instantly curate a 2x2 visual inspiration grid from Unsplash's high-quality database.

### 5. Quote + Image Generator
Overlay elegant typography on atmospheric imagery to create high-engagement quote cards.

---

## 🛠 Tech Stack
- **Backend**: Python (FastAPI)
- **Image Processing**: Pillow
- **API Integration**: Unsplash API (Public Access)
- **Design System**: Glassmorphism, Space Grotesk & Inter typography.
- **Deployment**: Render (Demo Tier)

---

## 🔒 Security & Compliance
- **OAuth Callback**: Whitelisted support for `urn:ietf:wg:oauth:2.0:oob` and production URLs.
- **Permissions**: Operates strictly on `public_access_only` scopes.
- **Data Protection**: API keys are stored server-side via environment variables and are never exposed to the client.

---

## ⚖️ Unsplash API Terms Compliance
AxpostMedia is built to strictly adhere to the [Unsplash API Terms of Use](https://unsplash.com/developers):
- **Authentic Experience**: Designed for creative, human-centric visual content generation.
- **Hotlinking**: Directly uses and embeds image URLs as required by Section 6 of the terms.
- **Download Tracking**: Every image retrieval automatically notifies the Unsplash `download_location` endpoint.
- **Strict Attribution**: Every visual displayed attributes Unsplash and the photographer, with direct links to their Unsplash profiles.
- **No Replication**: AxpostMedia is a creation tool, not a wallpaper app or Unsplash clone.
- **Privacy Policy**: Users must provide their own privacy policy when deploying this as a Developer App.

---

## 🚦 Rate Limiting & Fallbacks
- **Limit**: 50 requests per hour (Demo Tier).
- **Graceful Fallbacks**: In-memory caching provides high-quality fallback imagery if Unsplash is unreachable or the rate limit is hit.

---

## 📈 Usage Tracking
The platform includes a built-in `/stats` endpoint to monitor feature popularity and optimize product offerings.

---

## 📖 Onboarding for Unsplash Production Approval
To scale beyond the 50 req/hour limit, follow these steps:
1. **App Review**: Submit the Stitch UI design screenshots and this README to Unsplash for Production Tier review (1,000 req/hour).
2. **Attribution**: Ensure all image responses include the `credit` object provided by the API.
3. **Download Tracking**: The backend automatically handles the `download_location` trigger required by Unsplash.

---

## 🧑‍💻 Frontend Integration Example
```javascript
const generatePost = async (keyword, platform) => {
  const response = await fetch('https://your-api.render.com/social-media-post', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ keyword, platform })
  });
  const data = await response.json();
  console.log(data.image_url, data.caption, data.credit);
};
```

---
© 2026 AxpostMedia. Built with passion for creators.
