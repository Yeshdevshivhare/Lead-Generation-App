"""
Core scraping utilities and basic endpoints
Contact finder, WHOIS, Tech detection, Sitemap, Metadata
"""

from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
import socket

scraper_core_bp = Blueprint('scraper_core', __name__)

def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

@scraper_core_bp.route('/api/scrape/contacts', methods=['POST'])
def scrape_contacts():
    """Extract contact information from a website"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        response = requests.get(url, headers=get_headers(), timeout=15, allow_redirects=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        
        # Email patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = list(set(re.findall(email_pattern, text)))
        
        # Phone patterns
        phone_pattern = r'(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = list(set(re.findall(phone_pattern, text)))
        
        # Social media links
        social_links = {}
        social_patterns = {
            'LinkedIn': r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[^\s<>"]+',
            'Twitter': r'https?://(?:www\.)?(?:twitter|x)\.com/[^\s<>"]+',
            'Facebook': r'https?://(?:www\.)?facebook\.com/[^\s<>"]+',
            'Instagram': r'https?://(?:www\.)?instagram\.com/[^\s<>"]+',
            'YouTube': r'https?://(?:www\.)?youtube\.com/[^\s<>"]+',
            'GitHub': r'https?://(?:www\.)?github\.com/[^\s<>"]+',
        }
        
        for platform, pattern in social_patterns.items():
            matches = re.findall(pattern, text + ' ' + str(soup))
            if matches:
                social_links[platform] = matches[0]
        
        return jsonify({
            'url': url,
            'emails': emails[:10],
            'phones': phones[:10],
            'social_links': social_links
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch URL: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Scraping failed: {str(e)}'}), 500


@scraper_core_bp.route('/api/whois/lookup', methods=['POST'])
def whois_lookup():
    """Perform WHOIS lookup for a domain"""
    try:
        data = request.json
        domain = data.get('domain', '').strip()
        
        if not domain:
            return jsonify({'error': 'Domain is required'}), 400
        
        # Remove protocol and path
        domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Try to get basic DNS info
        try:
            ip_address = socket.gethostbyname(domain)
        except socket.gaierror:
            ip_address = 'Not found'
        
        # Try to get WHOIS data from a free API
        whois_api_url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_00000000000000000000000000000&domainName={domain}&outputFormat=JSON"
        
        try:
            whois_response = requests.get(whois_api_url, timeout=10)
            whois_data = whois_response.json()
        except:
            whois_data = {}
        
        return jsonify({
            'domain': domain,
            'ip_address': ip_address,
            'whois_data': whois_data,
            'note': 'Full WHOIS data requires API key'
        })
        
    except Exception as e:
        return jsonify({'error': f'WHOIS lookup failed: {str(e)}'}), 500


@scraper_core_bp.route('/api/tech/detect', methods=['POST'])
def detect_tech():
    """Detect technologies used on a website"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        response = requests.get(url, headers=get_headers(), timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        headers = response.headers
        html = response.text.lower()
        
        detected_tech = {
            'frameworks': [],
            'cms': [],
            'analytics': [],
            'hosting': [],
            'libraries': []
        }
        
        # Framework detection
        if 'react' in html or 'react-' in html:
            detected_tech['frameworks'].append('React')
        if 'vue' in html or 'vue.js' in html:
            detected_tech['frameworks'].append('Vue.js')
        if 'angular' in html or 'ng-' in html:
            detected_tech['frameworks'].append('Angular')
        if 'next' in html or '_next' in html:
            detected_tech['frameworks'].append('Next.js')
        
        # CMS detection
        if 'wp-content' in html or 'wordpress' in html:
            detected_tech['cms'].append('WordPress')
        if 'shopify' in html:
            detected_tech['cms'].append('Shopify')
        if 'wix.com' in html:
            detected_tech['cms'].append('Wix')
        if 'squarespace' in html:
            detected_tech['cms'].append('Squarespace')
        
        # Analytics
        if 'google-analytics' in html or 'gtag' in html:
            detected_tech['analytics'].append('Google Analytics')
        if 'hotjar' in html:
            detected_tech['analytics'].append('Hotjar')
        
        # Libraries
        if 'jquery' in html:
            detected_tech['libraries'].append('jQuery')
        if 'bootstrap' in html:
            detected_tech['libraries'].append('Bootstrap')
        if 'tailwind' in html:
            detected_tech['libraries'].append('Tailwind CSS')
        
        # Server detection from headers
        server = headers.get('Server', 'Unknown')
        if server != 'Unknown':
            detected_tech['hosting'].append(server)
        
        return jsonify({
            'url': url,
            'technologies': detected_tech
        })
        
    except Exception as e:
        return jsonify({'error': f'Tech detection failed: {str(e)}'}), 500


@scraper_core_bp.route('/api/sitemap/parse', methods=['POST'])
def parse_sitemap():
    """Parse sitemap.xml from a website"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Try common sitemap locations
        sitemap_urls = [
            urljoin(url, '/sitemap.xml'),
            urljoin(url, '/sitemap_index.xml'),
            urljoin(url, '/sitemap-index.xml'),
        ]
        
        urls_found = []
        
        for sitemap_url in sitemap_urls:
            try:
                response = requests.get(sitemap_url, headers=get_headers(), timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'xml')
                    locs = soup.find_all('loc')
                    urls_found.extend([loc.text for loc in locs])
                    break
            except:
                continue
        
        return jsonify({
            'url': url,
            'urls': urls_found[:100],
            'total': len(urls_found)
        })
        
    except Exception as e:
        return jsonify({'error': f'Sitemap parsing failed: {str(e)}'}), 500


@scraper_core_bp.route('/api/metadata/extract', methods=['POST'])
def extract_metadata():
    """Extract SEO metadata from a website"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        response = requests.get(url, headers=get_headers(), timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        metadata = {
            'title': '',
            'description': '',
            'keywords': '',
            'og_data': {},
            'twitter_data': {}
        }
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.text.strip()
        
        # Meta description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            metadata['description'] = desc_tag.get('content', '')
        
        # Meta keywords
        kw_tag = soup.find('meta', attrs={'name': 'keywords'})
        if kw_tag:
            metadata['keywords'] = kw_tag.get('content', '')
        
        # Open Graph
        for og_tag in soup.find_all('meta', property=re.compile(r'^og:')):
            prop = og_tag.get('property', '')
            content = og_tag.get('content', '')
            metadata['og_data'][prop] = content
        
        # Twitter Cards
        for tw_tag in soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')}):
            name = tw_tag.get('name', '')
            content = tw_tag.get('content', '')
            metadata['twitter_data'][name] = content
        
        return jsonify({
            'url': url,
            'metadata': metadata
        })
        
    except Exception as e:
        return jsonify({'error': f'Metadata extraction failed: {str(e)}'}), 500
