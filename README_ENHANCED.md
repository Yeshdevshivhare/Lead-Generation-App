# Lead Intelligence Suite

> Professional web intelligence gathering platform with dark mode interface

## ✨ Features

### Core Intelligence Tools

1. **Web Contact Scraper**
   - Extract emails from any website
   - Find phone numbers automatically
   - Discover social media profiles
   - Results displayed instantly in-app

2. **WHOIS Domain Lookup**
   - Domain registration details
   - IP address resolution
   - Registrar information
   - Creation and expiration dates

3. **Technology Stack Detection**
   - Identify CMS platforms (WordPress, Shopify, etc.)
   - Detect JavaScript frameworks (React, Vue, Angular)
   - Discover analytics tools
   - Web server identification

4. **Social Media Intelligence**
   - LinkedIn profiles
   - Twitter/X accounts
   - Facebook pages
   - Instagram profiles
   - YouTube channels

5. **Site Mapper**
   - Parse robots.txt
   - Extract sitemap URLs
   - Identify disallowed paths
   - Site structure analysis

6. **SEO Metadata Extractor**
   - OpenGraph tags
   - Twitter Card data
   - Meta descriptions
   - Canonical URLs

### Professional Features

- **Dark Mode Only**: Optimized for professional use
- **In-App Results**: All data displays within the application
- **Save Results**: LocalStorage-based result saving
- **Copy to Clipboard**: One-click data copying
- **Real-time Analytics**: Dashboard with statistics
- **Fast & Lightweight**: Optimized code, no bloat
- **Error Handling**: Comprehensive error messages

## 🚀 Quick Start

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser:
```
http://localhost:5000
```

### Usage

#### Web Scraper
1. Navigate to "Web Scraper" tab
2. Enter target URL (e.g., `example.com`)
3. Click "Scrape" button
4. View results in-app
5. Click "Save" to store results

#### WHOIS Lookup
1. Go to "WHOIS Lookup" tab
2. Enter domain name
3. Click "Lookup"
4. See registration details instantly

#### Technology Detection
1. Open "Tech Stack" tab
2. Enter website URL
3. Click "Detect"
4. View detected technologies with confidence levels

#### Social Intelligence
1. Navigate to "Social Intel"
2. Enter website URL
3. Click "Extract"
4. See all discovered social profiles

#### Site Mapper
1. Go to "Site Mapper" tab
2. Enter website URL
3. Click "Parse"
4. View robots.txt and sitemap data

#### Metadata Extraction
1. Open "Metadata" tab
2. Enter website URL
3. Click "Extract"
4. See all SEO metadata

## 📊 Dashboard

The dashboard provides:
- Total scans performed
- Saved results count
- Today's activity
- Recent scan history

## 💾 Data Management

### Saving Results
- Click "Save" button on any result card
- Data stored in browser LocalStorage
- Accessible via "Saved Results" tab

### Viewing Saved Data
1. Navigate to "Saved Results"
2. Click "View" on any saved item
3. Click "Delete" to remove items
4. Use "Clear All" to reset

### Data Persistence
- All data stored locally in your browser
- No server-side storage
- Privacy-focused design

## 🔧 Technical Details

### Backend
- Python Flask 3.0.0
- Flask-CORS for API access
- Requests for HTTP operations
- BeautifulSoup4 for HTML parsing
- lxml for XML processing

### Frontend
- Pure JavaScript (no frameworks)
- LocalStorage API for data persistence
- Fetch API for backend communication
- Font Awesome 6.4.0 icons
- Responsive CSS Grid layout

### Architecture
- Flask Blueprint pattern for modularity
- RESTful API design
- Error handling at all layers
- Timeout protection (15-20 seconds)
- User-agent spoofing for compatibility

## 🎨 Design Philosophy

**Dark Mode Only**
- Professional aesthetic
- Reduced eye strain
- Better for long sessions
- Consistent branding

**In-App Results**
- No external redirects
- Faster workflow
- Better user experience
- Data stays private

**Optimized Performance**
- Removed unused features
- Minimal dependencies
- Fast page loads
- Efficient scraping

## ⚙️ Configuration

### Timeouts
Default timeout: 15-20 seconds per request

To modify, edit `scraper.py`:
```python
response = requests.get(url, headers=get_headers(), timeout=20)
```

### Result Limits
Default limits per scan:
- Emails: 15
- Phone numbers: 15
- Sitemap URLs: 30

To modify, edit `scraper.py`:
```python
'emails': emails[:15],  # Change number
```

## 🔒 Privacy & Ethics

### Responsible Use
- Only scrape publicly accessible data
- Respect robots.txt directives
- Don't overwhelm servers
- Follow terms of service

### Data Storage
- All data stored locally in browser
- No cloud storage
- No tracking or analytics
- Complete privacy

### Legal Compliance
- Only use for legitimate business purposes
- Comply with local laws (GDPR, CCPA, etc.)
- Don't scrape private or protected content
- Respect copyright and intellectual property

## 🐛 Troubleshooting

### Application won't start
- Check Python installation: `python --version`
- Verify dependencies: `pip install -r requirements.txt`
- Check port 5000 is available

### Scraping fails
- Verify target website is accessible
- Check your internet connection
- Some sites block automated requests
- Try different URLs

### No results found
- Website may not have contact information
- Content might be JavaScript-generated
- Check console for errors
- Try a different page (e.g., /contact)

### Saved results not persisting
- Check browser LocalStorage settings
- Don't use private/incognito mode
- Clear browser cache if corrupted
- Use modern browser (Chrome, Firefox, Edge)

## 📝 API Endpoints

### POST /api/scrape/contacts
Extract contact information
```json
{
  "url": "https://example.com"
}
```

### POST /api/whois/lookup
Domain WHOIS lookup
```json
{
  "domain": "example.com"
}
```

### POST /api/tech/detect
Detect technologies
```json
{
  "url": "https://example.com"
}
```

### POST /api/sitemap/parse
Parse site structure
```json
{
  "url": "https://example.com"
}
```

### POST /api/metadata/extract
Extract SEO metadata
```json
{
  "url": "https://example.com"
}
```

### POST /shutdown
Gracefully shutdown application

## 🔄 Updates from Previous Version

### Removed
- ❌ Light mode toggle (dark mode only)
- ❌ Google dorking external links
- ❌ Batch processing queue
- ❌ Export to CSV/JSON/TXT
- ❌ Quick search with Google redirects
- ❌ Unnecessary animations and transitions

### Enhanced
- ✅ All results display in-app
- ✅ Better error handling
- ✅ Improved data extraction
- ✅ Cleaner UI design
- ✅ Faster performance
- ✅ Professional aesthetic
- ✅ Result saving system
- ✅ Copy to clipboard functionality

## 🎯 Use Cases

- **Lead Generation**: Find contact emails for outreach
- **Competitor Analysis**: Discover technology stacks
- **SEO Research**: Extract metadata and structure
- **Due Diligence**: WHOIS and domain verification
- **Social Media**: Find company social profiles
- **Web Research**: Automated data gathering

## 📄 License

See LICENSE file for details.

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API documentation
3. Inspect browser console for errors
4. Verify backend logs in terminal

---

**Made with professional standards for real-world use**
