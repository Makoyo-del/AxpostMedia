const showResults = () => {
    document.getElementById('results').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
};

const closeResults = () => {
    document.getElementById('results').classList.add('hidden');
    document.body.style.overflow = 'auto';
};

const renderAttribution = (credit) => `
    <div class="attribution">
        Photo by <a href="${credit.link}?utm_source=axpostmedia&utm_medium=referral" target="_blank">${credit.name}</a> 
        on <a href="https://unsplash.com?utm_source=axpostmedia&utm_medium=referral" target="_blank">Unsplash</a>
    </div>
`;

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
            <img src="${data.image_url}" class="result-img">
            <div class="caption-box">
                <p><strong>${platform} Caption:</strong></p>
                <p>${data.caption}</p>
            </div>
            ${renderAttribution(data.credit)}
        `;
        showResults();
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
            <div style="text-align:center">
                <img src="${url}" class="result-img">
                ${renderAttribution(data.credits[i])}
            </div>
        `).join('<br>');

        output.innerHTML = `
            <h2>${data.overlay_text}</h2>
            <div class="carousel-view">
                ${slidesHtml}
            </div>
        `;
        showResults();
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
            <img src="${url}" class="result-img">
        `).join('');

        output.innerHTML = `
            <h3>Suggested Visuals</h3>
            <div style="display:flex; gap:1rem; flex-wrap:wrap; justify-content:center">
                ${imgsHtml}
            </div>
            ${renderAttribution(data.credit)}
        `;
        showResults();
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
            <img src="${url}" style="width:250px; height:250px; object-fit:cover; border-radius:10px">
        `).join('');

        output.innerHTML = `
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px">
                ${gridHtml}
            </div>
            <p class="attribution">Credits: ${data.credits.map(c => c.name).join(', ')}</p>
        `;
        showResults();
    } catch (e) {
        alert('Error creating moodboard');
    } finally {
        btn.innerText = 'Curate Grid';
    }
}
