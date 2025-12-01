"""
OSINT Intelligence Endpoints
Google Dorking, GitHub OSINT, RSS Feeds, Competitors, Keywords, Scoring
"""

from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin

scraper_osint_bp = Blueprint('scraper_osint', __name__)

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

@scraper_osint_bp.route('/api/dork/search', methods=['POST'])
def google_dork():
    """Perform Google dork search and extract result URLs"""
    try:
        data = request.json
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}&num=20&hl=en"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return jsonify({
                'error': f'Google blocked the request (Status: {response.status_code}). Try using the query directly in Google.',
                'query': query,
                'google_url': search_url,
                'results': [],
                'total': 0
            })
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for g in soup.select('div.g, div[data-sokoban-container]'):
            title_elem = g.select_one('h3')
            link_elem = g.select_one('a[href]')
            snippet_elem = g.select_one('div.VwiC3b, div.IsZvec, span.aCOpRe, div[data-sncf]')
            
            if link_elem and link_elem.get('href'):
                url = link_elem['href']
                if url.startswith('http') and not url.startswith('https://www.google'):
                    results.append({
                        'title': title_elem.get_text() if title_elem else 'No title',
                        'url': url,
                        'snippet': snippet_elem.get_text()[:200] if snippet_elem else ''
                    })
        
        if len(results) == 0:
            for link in soup.select('a[href^="http"]:not([href*="google.com"])'):
                url = link.get('href')
                if url and not any(x in url for x in ['google.', 'gstatic.', 'youtube.']):
                    title_elem = link.select_one('h3, h2, h1') or link
                    results.append({
                        'title': title_elem.get_text()[:100] if title_elem else 'Result',
                        'url': url,
                        'snippet': ''
                    })
                    if len(results) >= 15:
                        break
        
        seen = set()
        unique_results = []
        for r in results:
            if r['url'] not in seen:
                seen.add(r['url'])
                unique_results.append(r)
        
        return jsonify({
            'query': query,
            'results': unique_results[:15],
            'total': len(unique_results),
            'google_url': search_url,
            'note': 'Results may be limited due to Google anti-scraping. For best results, use the query directly in Google.'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Dorking failed: {str(e)}',
            'query': query if 'query' in locals() else '',
            'results': [],
            'total': 0
        }), 500


@scraper_osint_bp.route('/api/osint/github', methods=['POST'])
def github_osint():
    """Search GitHub for company information"""
    try:
        data = request.json
        company = data.get('company', '').strip()
        
        if not company:
            return jsonify({'error': 'Company name/domain is required'}), 400
        
        results = {
            'repos': [],
            'users': [],
            'insights': []
        }
        
        search_queries = [
            f'{company} in:readme',
            f'@{company} in:file',
            f'{company} filename:package.json'
        ]
        
        for query in search_queries[:1]:
            github_url = f"https://github.com/search?q={requests.utils.quote(query)}&type=repositories"
            response = requests.get(github_url, headers=get_headers(), timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for repo in soup.find_all('a', class_='v-align-middle')[:5]:
                href = repo.get('href', '')
                if href and href.startswith('/') and len(href.split('/')) >= 3:
                    results['repos'].append({
                        'name': repo.get_text().strip(),
                        'url': f"https://github.com{href}"
                    })
        
        if results['repos']:
            results['insights'].append('Found public repositories mentioning company')
            results['insights'].append('Check repos for tech stack and employees')
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': f'GitHub OSINT failed: {str(e)}'}), 500


@scraper_osint_bp.route('/api/osint/feeds', methods=['POST'])
def discover_feeds():
    """Discover RSS/Atom feeds on a website"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        feeds = []
        feed_paths = [
            '/feed', '/rss', '/feed.xml', '/rss.xml', '/atom.xml',
            '/blog/feed', '/blog/rss', '/feeds/posts/default'
        ]
        
        for path in feed_paths:
            try:
                feed_url = base_url + path
                response = requests.head(feed_url, headers=get_headers(), timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    feeds.append({
                        'url': feed_url,
                        'type': 'RSS/Atom',
                        'status': 'Active'
                    })
            except:
                pass
        
        try:
            response = requests.get(url, headers=get_headers(), timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('link', type=['application/rss+xml', 'application/atom+xml']):
                feed_href = link.get('href', '')
                if feed_href:
                    feed_full = urljoin(url, feed_href)
                    if feed_full not in [f['url'] for f in feeds]:
                        feeds.append({
                            'url': feed_full,
                            'type': link.get('type', 'RSS'),
                            'title': link.get('title', 'Feed')
                        })
        except:
            pass
        
        return jsonify({
            'feeds': feeds,
            'total': len(feeds)
        })
        
    except Exception as e:
        return jsonify({'error': f'Feed discovery failed: {str(e)}'}), 500
