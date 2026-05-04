const showResults = () => {
    document.getElementById('results').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
};

const closeResults = () => {
    document.getElementById('results').classList.add('hidden');
    document.body.style.overflow = 'auto';
};

const renderAttribution = (credit, downloadUrl) => `
    <div class="attribution">
        Photo by <a href="${credit.link}?utm_source=axpostmedia&utm_medium=referral" target="_blank">${credit.name}</a> 
        on <a href="https://unsplash.com?utm_source=axpostmedia&utm_medium=referral" target="_blank">Unsplash</a>
        <br>
        <a href="${downloadUrl}" target="_blank" class="btn-download">Download High-Res</a>
    </div>
`;

async function fetchStats() {
    try {
        const response = await fetch('/stats');
        const data = await response.json();
        document.getElementById('stat-social').innerText = data.social_media_post || 0;
        document.getElementById('stat-carousel').innerText = data.carousel_builder || 0;
        document.getElementById('stat-blog').innerText = data.blog_image_inserter || 0;
        document.getElementById('stat-mood').innerText = data.moodboard || 0;
        const total = (data.social_media_post || 0) + (data.carousel_builder || 0) + (data.blog_image_inserter || 0) + (data.moodboard || 0) + (data.quote_generator || 0);
        document.getElementById('stats').querySelector('p').innerText = `Real-time usage tracking: ${total} assets generated today.`;
    } catch (e) {
        console.error('Stats fetch failed');
    }
}

// ... existing functions ...

async function generateQuote() {
    const quote_text = document.getElementById('quote-text').value;
    if (!quote_text) return alert('Please enter a quote');

    const btn = document.querySelector('#card-quote button');
    btn.innerText = 'Styling...';

    try {
        const response = await fetch('/quote-generator', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ quote_text })
        });
        const data = await response.json();
        
        const output = document.getElementById('output-content');
        output.innerHTML = `
            <div style="position:relative; display:inline-block">
                <img src="${data.image_with_overlay}&w=1000" class="result-img">
                <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); width:80%; text-align:center; color:white; font-family:'Space Grotesk'; font-size:1.5rem; text-shadow: 2px 2px 10px rgba(0,0,0,0.8);">
                    "${quote_text}"
                </div>
            </div>
            ${renderAttribution(data.credit, data.image_with_overlay)}
        `;
        showResults();
        fetchStats();
    } catch (e) {
        alert('Error generating quote image');
    } finally {
        btn.innerText = 'Style Quote';
    }
}

// Polling for stats every 30 seconds
setInterval(fetchStats, 30000);
fetchStats();

async function generateSocialPost() {
    const keyword = document.getElementById('social-kw').value;
    const platform = document.getElementById('social-platform').value;
    if (!keyword) return alert('Please enter a keyword');

    const btn = document.querySelector('#card-social button');
    btn.innerText = 'Generating...';

    try {
        const response = await fetch('/social-media-post', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keyword, platform })
        });
        const data = await response.json();
        
        const output = document.getElementById('output-content');
        output.innerHTML = `
            <img src="${data.image_url}&w=1200" class="result-img">
            <div class="caption-box">
                <p><strong>${platform} Caption:</strong></p>
                <p>${data.caption}</p>
            </div>
            ${renderAttribution(data.credit, data.image_url)}
        `;
        showResults();
        fetchStats();
    } catch (e) {
        alert('Error generating post');
    } finally {
        btn.innerText = 'Generate Post';
    }
}

async function generateCarousel() {
    const keyword = document.getElementById('carousel-kw').value;
    const count = document.getElementById('carousel-count').value;
    if (!keyword) return alert('Please enter a topic');

    const btn = document.querySelector('#card-carousel button');
    btn.innerText = 'Building...';

    try {
        const response = await fetch('/carousel-builder', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keyword, slides_count: parseInt(count) })
        });
        const data = await response.json();
        
        const output = document.getElementById('output-content');
        let slidesHtml = data.carousel_images.map((url, i) => `
            <div class="carousel-slide">
                <img src="${url}&w=1000" class="result-img">
                ${renderAttribution(data.credits[i], url)}
            </div>
        `).join('');

        output.innerHTML = `
            <h2>${data.overlay_text}</h2>
            <div class="carousel-container">
                ${slidesHtml}
            </div>
            <p style="color:rgba(255,255,255,0.4); font-size:0.8rem">Scroll horizontally to view slides →</p>
        `;
        showResults();
        fetchStats();
    } catch (e) {
        alert('Error building carousel');
    } finally {
        btn.innerText = 'Build Carousel';
    }
}

async function generateBlogImages() {
    const text = document.getElementById('blog-text').value;
    if (!text) return alert('Please enter article text');

    const btn = document.querySelector('#card-blog button');
    btn.innerText = 'Analyzing...';

    try {
        const response = await fetch('/blog-image-inserter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ article_text: text })
        });
        const data = await response.json();
        
        const output = document.getElementById('output-content');
        let imgsHtml = data.suggested_images.map(url => `
            <div style="text-align:center">
                <img src="${url}&w=800" class="result-img" style="max-height:40vh">
                <br>
                <a href="${url}" target="_blank" class="btn-download">Download</a>
            </div>
        `).join('');

        output.innerHTML = `
            <h3>Suggested Visuals</h3>
            <div style="display:flex; gap:1.5rem; flex-wrap:wrap; justify-content:center">
                ${imgsHtml}
            </div>
            <p class="attribution">Photos from Unsplash (Attribution required)</p>
        `;
        showResults();
        fetchStats();
    } catch (e) {
        alert('Error suggesting images');
    } finally {
        btn.innerText = 'Suggest Images';
    }
}

async function generateMoodboard() {
    const keyword = document.getElementById('mood-kw').value;
    if (!keyword) return alert('Please enter a vibe');

    const btn = document.querySelector('#card-mood button');
    btn.innerText = 'Curating...';

    try {
        const response = await fetch('/moodboard', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keyword })
        });
        const data = await response.json();
        
        const output = document.getElementById('output-content');
        let gridHtml = data.image_urls.map(url => `
            <img src="${url}&w=600" style="width:100%; height:300px; object-fit:cover; border-radius:10px">
        `).join('');

        output.innerHTML = `
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; width:100%; max-width:800px">
                ${gridHtml}
            </div>
            <p class="attribution">Credits: ${data.credits.map(c => c.name).join(', ')}</p>
            <a href="#" onclick="alert('Exporting high-res grid...') " class="btn-download">Export Grid</a>
        `;
        showResults();
        fetchStats();
    } catch (e) {
        alert('Error creating moodboard');
    } finally {
        btn.innerText = 'Curate Grid';
    }
}
