# Quick Start Guide

## Installation

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the App**
   - Browser will auto-open at: http://127.0.0.1:5000
   - If not, manually navigate to that URL

## Using the Tools

### Dashboard
- View real-time analytics
- Track search activity
- Monitor usage patterns

### Web Scraper
1. Enter company website URL (e.g., https://example.com)
2. Click "Scrape Website"
3. Extract emails, phones, social links automatically

### SERP Dorking
1. Enter domain name (e.g., example.com)
2. Select search type (contacts, emails, PDFs, etc.)
3. Click "Generate Dork Query"
4. Opens Google with advanced search operators

### WHOIS Lookup
1. Enter domain name
2. Get registration info, age, organization
3. Verify business legitimacy

### Tech Stack Detector
1. Enter website URL
2. Detects CMS, frameworks, analytics
3. Identifies integration opportunities

### Social Intelligence
1. Enter company website
2. Extracts all social media links
3. Analyze social presence

### Job Listings
1. Enter career page URL
2. Manually analyze for growth signals
3. Quick links to LinkedIn/Indeed search

### Site Mapper
1. Enter website URL
2. Parses robots.txt and sitemap.xml
3. Discovers all site pages

### Metadata Extractor
1. Enter website URL
2. Extracts OpenGraph, Twitter Cards
3. Gets structured business data

## Tips

- **Dark/Light Mode:** Toggle in top-right corner
- **Tooltips:** Hover over info icons for help
- **Copy Functions:** Click copy buttons next to emails
- **Export:** Use Export tab to download all data
- **Batch Processing:** Queue multiple searches

## Troubleshooting

**Port already in use:**
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Missing dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

**CORS errors:**
- Make sure scraper.py is in the same directory as app.py
- Restart the application

## Important Note

The JavaScript functionality for the new scraping features is in `app.js`. For a fully functional implementation, you need to integrate the external JavaScript file or embed it in the HTML.

To use external JavaScript:
1. Add this line before `</body>` in index.html:
   ```html
   <script src="app.js"></script>
   ```

Or the full implementation is ready in the current index.html with embedded JavaScript.
