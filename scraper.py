"""
Enhanced Lead Intelligence Backend - Advanced Endpoints Only
Unique endpoints: Social, Competitors, Keywords, Scoring, Growth, Profile, Jobs, Business, Tech Health

Core endpoints (contacts, whois, tech, sitemap, metadata) are in scraper_core.py
OSINT endpoints (dorking, github, feeds) are in scraper_osint.py
"""

from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
import socket

scraper_bp = Blueprint('scraper', __name__)

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

@scraper_bp.route('/api/osint/competitors', methods=['POST'])
def analyze_competitors():
    """Find competitor mentions and integrations"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        response = requests.get(url, headers=get_headers(), timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = response.text.lower()
        
        # Common competitor/partner keywords
        integrations = []
        partners = []
        
        # Tech integrations
        tech_keywords = {
            'Salesforce': r'salesforce',
            'HubSpot': r'hubspot',
            'Slack': r'slack',
            'Zoom': r'zoom',
            'Microsoft Teams': r'teams\.microsoft',
            'Google Workspace': r'workspace\.google',
            'Stripe': r'stripe',
            'PayPal': r'paypal'
        }
        
        for tech, pattern in tech_keywords.items():
            if re.search(pattern, text):
                integrations.append(tech)
        
        # Find logo images (potential partners)
        for img in soup.find_all('img', alt=True):
            alt_text = img.get('alt', '').lower()
            if any(word in alt_text for word in ['partner', 'client', 'customer', 'logo']):
                partners.append(alt_text)
        
        return jsonify({
            'integrations': integrations[:10],
            'potential_partners': partners[:10],
            'integration_count': len(integrations)
        })
        
    except Exception as e:
        return jsonify({'error': f'Competitor analysis failed: {str(e)}'}), 500


# ============== KEYWORD INTELLIGENCE ==============
@scraper_bp.route('/api/osint/keywords', methods=['POST'])
def keyword_analysis():
    """Analyze page for specific keywords and score relevance"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        keywords = data.get('keywords', [])
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not keywords:
            keywords = ['automation', 'AI', 'CRM', 'analytics', 'enterprise', 'SaaS']
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        response = requests.get(url, headers=get_headers(), timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        text = soup.get_text().lower()
        words = text.split()
        total_words = len(words)
        
        keyword_scores = {}
        matches = []
        
        for keyword in keywords:
            count = text.count(keyword.lower())
            if count > 0:
                density = (count / total_words) * 100 if total_words > 0 else 0
                keyword_scores[keyword] = {
                    'count': count,
                    'density': round(density, 2)
                }
                matches.append(keyword)
        
        # Calculate relevance score
        relevance_score = min(100, len(matches) * 15 + sum([kw['count'] for kw in keyword_scores.values()]))
        
        return jsonify({
            'url': url,
            'keywords_found': matches,
            'keyword_details': keyword_scores,
            'relevance_score': relevance_score,
            'total_words': total_words
        })
        
    except Exception as e:
        return jsonify({'error': f'Keyword analysis failed: {str(e)}'}), 500


# ============== LEAD SCORING ==============
@scraper_bp.route('/api/osint/score', methods=['POST'])
def lead_scoring():
    """Comprehensive lead intelligence scoring"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        score = 0
        signals = []
        
        response = requests.get(url, headers=get_headers(), timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = response.text.lower()
        
        # 1. Job postings detected (+20 points)
        if any(word in text for word in ['careers', 'jobs', 'hiring', 'join our team', 'open positions']):
            score += 20
            signals.append('Active hiring detected')
        
        # 2. Recent blog posts (+15 points)
        if soup.find('time') or soup.find('span', class_=re.compile('date|time')):
            score += 15
            signals.append('Active blog/content')
        
        # 3. Social media presence (+10 points)
        social_count = len(re.findall(r'(linkedin|twitter|facebook|instagram)\.com', text))
        if social_count >= 3:
            score += 10
            signals.append(f'{social_count} social profiles found')
        
        # 4. Contact forms (+10 points)
        if soup.find('form') or 'contact' in text:
            score += 10
            signals.append('Contact form available')
        
        # 5. Email addresses (+10 points)
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if len(emails) > 2:
            score += 10
            signals.append(f'{len(emails)} email addresses found')
        
        # 6. Tech stack indicators (+15 points)
        tech_indicators = ['react', 'angular', 'vue', 'api', 'integration', 'platform']
        tech_count = sum(1 for tech in tech_indicators if tech in text)
        if tech_count >= 3:
            score += 15
            signals.append(f'Advanced tech stack ({tech_count} indicators)')
        
        # 7. Premium keywords (+20 points)
        premium_keywords = ['enterprise', 'professional', 'premium', 'custom', 'dedicated']
        premium_count = sum(1 for kw in premium_keywords if kw in text)
        if premium_count >= 2:
            score += 20
            signals.append('Premium/enterprise positioning')
        
        # Intent level
        if score >= 70:
            intent = 'High - Strong buying signals'
        elif score >= 40:
            intent = 'Medium - Some engagement potential'
        else:
            intent = 'Low - Early stage'
        
        return jsonify({
            'score': min(100, score),
            'intent_level': intent,
            'signals': signals,
            'recommendation': 'Priority lead' if score >= 70 else 'Monitor' if score >= 40 else 'Nurture'
        })
        
    except Exception as e:
        return jsonify({'error': f'Lead scoring failed: {str(e)}'}), 500


# ============== KEYWORD DISCOVERY ENGINE ==============
@scraper_bp.route('/api/keywords/discover', methods=['POST'])
def discover_keywords():
    """Auto-discover related keywords, synonyms, and industry jargon"""
    try:
        data = request.json
        keyword = data.get('keyword', '').strip().lower()
        
        if not keyword:
            return jsonify({'error': 'Keyword is required'}), 400
        
        # Keyword expansion database
        keyword_database = {
            'crm': ['customer relationship management', 'sales automation', 'contact management', 'pipeline', 'salesforce', 'hubspot', 'zoho'],
            'ai': ['artificial intelligence', 'machine learning', 'deep learning', 'neural network', 'automation', 'chatbot', 'nlp', 'computer vision'],
            'automation': ['workflow', 'zapier', 'integration', 'api', 'scripting', 'orchestration', 'rpa', 'no-code'],
            'analytics': ['data analysis', 'reporting', 'dashboard', 'bi', 'business intelligence', 'metrics', 'kpi', 'insights'],
            'saas': ['cloud software', 'subscription', 'web app', 'platform', 'multi-tenant', 'b2b software'],
            'devops': ['ci/cd', 'deployment', 'docker', 'kubernetes', 'jenkins', 'infrastructure', 'cloud ops'],
            'mobile': ['app development', 'ios', 'android', 'react native', 'flutter', 'mobile-first'],
            'web': ['website', 'frontend', 'backend', 'full-stack', 'responsive', 'progressive web app'],
            'ecommerce': ['online store', 'shopping cart', 'payment gateway', 'shopify', 'woocommerce', 'magento'],
            'marketing': ['digital marketing', 'seo', 'sem', 'content marketing', 'email marketing', 'social media'],
            'cloud': ['aws', 'azure', 'google cloud', 'cloud hosting', 'serverless', 'iaas', 'paas'],
            'security': ['cybersecurity', 'encryption', 'firewall', 'ssl', 'authentication', 'authorization'],
            'database': ['sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'data warehouse'],
            'api': ['rest api', 'graphql', 'webhook', 'integration', 'endpoints', 'microservices']
        }
        
        # Find related keywords
        related = []
        synonyms = []
        
        # Direct match
        if keyword in keyword_database:
            related = keyword_database[keyword]
        
        # Partial match
        for key, values in keyword_database.items():
            if keyword in key or key in keyword:
                synonyms.append(key)
                related.extend(values)
        
        # Remove duplicates
        related = list(set(related))[:20]
        synonyms = list(set(synonyms))[:10]
        
        # Industry jargon patterns
        industry_patterns = {
            'tech': ['stack', 'framework', 'architecture', 'scalable', 'agile'],
            'business': ['roi', 'kpi', 'revenue', 'growth', 'conversion'],
            'sales': ['lead', 'prospect', 'pipeline', 'deal', 'quota'],
            'product': ['feature', 'roadmap', 'mvp', 'iteration', 'release']
        }
        
        jargon = []
        for category, terms in industry_patterns.items():
            if any(kw in keyword for kw in ['tech', 'dev', 'software', 'app']):
                if category in ['tech', 'product']:
                    jargon.extend(terms)
            elif any(kw in keyword for kw in ['sales', 'marketing', 'crm']):
                if category in ['business', 'sales']:
                    jargon.extend(terms)
        
        return jsonify({
            'input_keyword': keyword,
            'related_keywords': related[:15],
            'synonyms': synonyms,
            'industry_jargon': list(set(jargon))[:10],
            'total_expanded': len(related) + len(synonyms) + len(jargon)
        })
        
    except Exception as e:
        return jsonify({'error': f'Keyword discovery failed: {str(e)}'}), 500


# ============== COMPANY GROWTH SIGNALS ==============
@scraper_bp.route('/api/growth/signals', methods=['POST'])
def growth_signals():
    """Detect company growth indicators"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        base_url = f"{parsed_url.scheme}://{domain}"
        
        signals = []
        growth_score = 0
        
        # 1. Check for subdomains (indicating expansion)
        common_subdomains = ['blog', 'app', 'api', 'dev', 'staging', 'docs', 'support', 'shop', 'portal']
        active_subdomains = []
        
        for subdomain in common_subdomains:
            try:
                sub_url = f"https://{subdomain}.{domain}"
                response = requests.head(sub_url, timeout=3, allow_redirects=True)
                if response.status_code == 200:
                    active_subdomains.append(subdomain)
                    growth_score += 5
            except:
                pass
        
        if active_subdomains:
            signals.append(f'Found {len(active_subdomains)} active subdomains: {", ".join(active_subdomains[:5])}')
        
        # 2. SSL Certificate check
        try:
            if url.startswith('https://'):
                growth_score += 10
                signals.append('SSL Certificate active (security priority)')
        except:
            pass
        
        # 3. Check for blog/news (content activity)
        response = requests.get(url, headers=get_headers(), timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = response.text.lower()
        
        if any(word in text for word in ['blog', 'news', 'press', 'updates', 'announcements']):
            growth_score += 15
            signals.append('Active content publication (blog/news/press)')
        
        # 4. Job postings (hiring = growth)
        careers_paths = ['/careers', '/jobs', '/join-us', '/about/careers']
        hiring_found = False
        
        for path in careers_paths:
            try:
                career_url = base_url + path
                response = requests.head(career_url, timeout=5)
                if response.status_code == 200:
                    hiring_found = True
                    break
            except:
                pass
        
        if hiring_found or 'careers' in text or 'we\'re hiring' in text:
            growth_score += 20
            signals.append('Active hiring detected (company expansion)')
        
        # 5. New sitemap pages (frequent updates)
        try:
            sitemap_url = base_url + '/sitemap.xml'
            sitemap_response = requests.get(sitemap_url, timeout=10)
            if sitemap_response.status_code == 200:
                soup_sitemap = BeautifulSoup(sitemap_response.text, 'xml')
                urls = soup_sitemap.find_all('loc')
                if len(urls) > 50:
                    growth_score += 10
                    signals.append(f'Large sitemap ({len(urls)} pages) - content-rich site')
        except:
            pass
        
        # 6. Social media presence (marketing investment)
        social_count = len(re.findall(r'(linkedin|twitter|facebook|instagram|youtube)\.com', text))
        if social_count >= 3:
            growth_score += 10
            signals.append(f'Strong social media presence ({social_count} platforms)')
        
        # 7. Recent dates detected (active maintenance)
        current_year = '2025'
        recent_year = '2024'
        if current_year in text or recent_year in text:
            growth_score += 10
            signals.append('Recent content detected (2024-2025)')
        
        # Growth classification
        if growth_score >= 60:
            growth_level = 'High Growth - Scaling rapidly'
        elif growth_score >= 30:
            growth_level = 'Moderate Growth - Steady expansion'
        else:
            growth_level = 'Early Stage - Building foundation'
        
        return jsonify({
            'growth_score': min(100, growth_score),
            'growth_level': growth_level,
            'signals': signals,
            'active_subdomains': active_subdomains,
            'recommendation': 'Priority outreach' if growth_score >= 60 else 'Monitor for changes' if growth_score >= 30 else 'Early stage nurture'
        })
        
    except Exception as e:
        return jsonify({'error': f'Growth signals detection failed: {str(e)}'}), 500


# ============== MULTI-SITE AGGREGATED PROFILE ==============
@scraper_bp.route('/api/profile/aggregate', methods=['POST'])
def aggregate_profile():
    """Create enriched company profile from multiple sources"""
    try:
        data = request.json
        domain = data.get('domain', '').strip()
        company_name = data.get('company_name', '').strip()
        
        if not domain:
            return jsonify({'error': 'Domain is required'}), 400
        
        domain = domain.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
        url = f'https://{domain}'
        
        profile = {
            'company': company_name or domain,
            'domain': domain,
            'sources': {},
            'enriched_data': {}
        }
        
        # 1. Website data
        try:
            response = requests.get(url, headers=get_headers(), timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = response.text.lower()
            
            # Extract emails
            emails = list(set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)))
            emails = [e for e in emails if domain in e.lower()][:5]
            
            # Social links
            linkedin = re.findall(r'https?://(?:www\.)?linkedin\.com/company/[\w-]+', text)
            twitter = re.findall(r'https?://(?:www\.)?twitter\.com/[\w]+', text)
            
            profile['sources']['website'] = {
                'status': 'success',
                'emails': emails,
                'linkedin': linkedin[0] if linkedin else None,
                'twitter': twitter[0] if twitter else None
            }
        except Exception as e:
            profile['sources']['website'] = {'status': 'failed', 'error': str(e)}
        
        # 2. LinkedIn preview (public)
        if company_name:
            try:
                linkedin_search = f"https://www.google.com/search?q=site:linkedin.com/company+{requests.utils.quote(company_name)}"
                response = requests.get(linkedin_search, headers=get_headers(), timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                linkedin_links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'linkedin.com/company/' in href:
                        linkedin_links.append(href)
                
                profile['sources']['linkedin'] = {
                    'status': 'found' if linkedin_links else 'not_found',
                    'url': linkedin_links[0] if linkedin_links else None
                }
            except:
                profile['sources']['linkedin'] = {'status': 'error'}
        
        # 3. GitHub presence
        try:
            github_search = f"https://github.com/search?q={requests.utils.quote(company_name or domain)}&type=repositories"
            response = requests.get(github_search, headers=get_headers(), timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            repos = []
            for repo_link in soup.find_all('a', class_='v-align-middle')[:3]:
                repos.append({
                    'name': repo_link.get_text().strip(),
                    'url': f"https://github.com{repo_link.get('href', '')}"
                })
            
            profile['sources']['github'] = {
                'status': 'found' if repos else 'not_found',
                'repos': repos
            }
        except:
            profile['sources']['github'] = {'status': 'error'}
        
        # 4. Careers page
        careers_paths = ['/careers', '/jobs', '/about/careers', '/company/careers']
        careers_found = False
        
        for path in careers_paths:
            try:
                career_url = url + path
                response = requests.head(career_url, timeout=5)
                if response.status_code == 200:
                    careers_found = True
                    profile['sources']['careers'] = {
                        'status': 'found',
                        'url': career_url
                    }
                    break
            except:
                pass
        
        if not careers_found:
            profile['sources']['careers'] = {'status': 'not_found'}
        
        # 5. Press/News page
        press_paths = ['/press', '/news', '/media', '/newsroom', '/blog']
        press_found = False
        
        for path in press_paths:
            try:
                press_url = url + path
                response = requests.head(press_url, timeout=5)
                if response.status_code == 200:
                    press_found = True
                    profile['sources']['press'] = {
                        'status': 'found',
                        'url': press_url
                    }
                    break
            except:
                pass
        
        if not press_found:
            profile['sources']['press'] = {'status': 'not_found'}
        
        # Enriched summary
        profile['enriched_data'] = {
            'total_emails': len(profile['sources'].get('website', {}).get('emails', [])),
            'linkedin_found': profile['sources'].get('linkedin', {}).get('status') == 'found',
            'github_repos': len(profile['sources'].get('github', {}).get('repos', [])),
            'has_careers_page': profile['sources'].get('careers', {}).get('status') == 'found',
            'has_press_page': profile['sources'].get('press', {}).get('status') == 'found',
            'completeness': sum([
                1 if profile['sources'].get('website', {}).get('status') == 'success' else 0,
                1 if profile['sources'].get('linkedin', {}).get('status') == 'found' else 0,
                1 if profile['sources'].get('github', {}).get('status') == 'found' else 0,
                1 if profile['sources'].get('careers', {}).get('status') == 'found' else 0,
                1 if profile['sources'].get('press', {}).get('status') == 'found' else 0
            ]) * 20
        }
        
        return jsonify(profile)
        
    except Exception as e:
        return jsonify({'error': f'Profile aggregation failed: {str(e)}'}), 500


# ============== TECHNICAL HEALTH MONITOR ==============
@scraper_bp.route('/api/tech/health', methods=['POST'])
def tech_health():
    """Monitor technical issues and health signals"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        health_score = 100
        issues = []
        warnings = []
        
        # 1. SSL Check
        if not url.startswith('https://'):
            health_score -= 25
            issues.append('No SSL certificate - Security risk')
        
        # 2. Load time check
        import time
        start_time = time.time()
        try:
            response = requests.get(url, headers=get_headers(), timeout=30)
            load_time = time.time() - start_time
            
            if load_time > 5:
                health_score -= 15
                issues.append(f'Slow load time ({round(load_time, 2)}s) - Performance issue')
            elif load_time > 3:
                health_score -= 5
                warnings.append(f'Moderate load time ({round(load_time, 2)}s)')
            
            soup = BeautifulSoup(response.text, 'html.parser')
            html = response.text
            
            # 3. Mobile optimization
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            if not viewport:
                health_score -= 10
                issues.append('No mobile viewport meta tag - Not mobile optimized')
            
            # 4. Broken JavaScript detection
            script_errors = len(re.findall(r'<script[^>]*></script>', html))
            if script_errors > 5:
                health_score -= 10
                warnings.append(f'{script_errors} empty script tags detected')
            
            # 5. Outdated CMS/Framework detection
            outdated_tech = []
            
            if 'jquery/1.' in html.lower() or 'jquery-1.' in html.lower():
                outdated_tech.append('jQuery 1.x (outdated)')
            
            if 'bootstrap/3.' in html.lower() or 'bootstrap-3.' in html.lower():
                outdated_tech.append('Bootstrap 3 (outdated)')
            
            if 'angularjs' in html.lower() or 'angular.js' in html.lower():
                outdated_tech.append('AngularJS (legacy)')
            
            if '/wp-content/' in html and re.search(r'WordPress [1-4]\.',html):
                outdated_tech.append('Old WordPress version')
            
            if outdated_tech:
                health_score -= 20
                issues.append(f'Outdated frameworks detected: {", ".join(outdated_tech)}')
            
            # 6. Missing SEO essentials
            if not soup.find('title'):
                health_score -= 5
                warnings.append('Missing page title')
            
            if not soup.find('meta', attrs={'name': 'description'}):
                health_score -= 5
                warnings.append('Missing meta description')
            
            # 7. HTTP vs HTTPS
            if response.url.startswith('http://'):
                health_score -= 15
                issues.append('Redirected to HTTP - SSL not enforced')
            
        except requests.Timeout:
            health_score -= 30
            issues.append('Extreme timeout - Site unreachable or very slow')
        except Exception as e:
            health_score -= 20
            issues.append(f'Error loading site: {str(e)}')
        
        # Classification
        if health_score >= 80:
            health_level = 'Excellent - Well maintained'
        elif health_score >= 60:
            health_level = 'Good - Minor improvements needed'
        elif health_score >= 40:
            health_level = 'Fair - Several issues detected'
        else:
            health_level = 'Poor - Major technical problems'
        
        return jsonify({
            'health_score': max(0, health_score),
            'health_level': health_level,
            'critical_issues': issues,
            'warnings': warnings,
            'opportunity': 'High priority for IT services' if health_score < 60 else 'Potential optimization services' if health_score < 80 else 'Well maintained'
        })
        
    except Exception as e:
        return jsonify({'error': f'Health check failed: {str(e)}'}), 500


# ============== JOB POSTING INTELLIGENCE ==============
@scraper_bp.route('/api/jobs/intelligence', methods=['POST'])
def job_intelligence():
    """Scrape and analyze job postings for tech hiring signals"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        company_name = data.get('company_name', '').strip()
        
        if not url:
            return jsonify({'error': 'URL or company name is required'}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        base_url = f"{parsed_url.scheme}://{domain}"
        
        job_data = {
            'jobs_found': False,
            'total_positions': 0,
            'tech_roles': [],
            'hiring_signals': [],
            'opportunity_score': 0
        }
        
        # Check careers page
        careers_paths = ['/careers', '/jobs', '/join-us', '/about/careers', '/company/careers']
        careers_html = None
        
        for path in careers_paths:
            try:
                career_url = base_url + path
                response = requests.get(career_url, headers=get_headers(), timeout=10)
                if response.status_code == 200:
                    careers_html = response.text.lower()
                    job_data['careers_url'] = career_url
                    break
            except:
                pass
        
        # If no careers page, check main site
        if not careers_html:
            try:
                response = requests.get(url, headers=get_headers(), timeout=10)
                careers_html = response.text.lower()
            except:
                pass
        
        if careers_html:
            # Detect tech roles
            tech_roles_patterns = {
                'Full Stack Developer': r'full[- ]?stack|fullstack',
                'Frontend Developer': r'front[- ]?end|react|vue|angular developer',
                'Backend Developer': r'back[- ]?end|node\.?js|python|java developer',
                'Mobile Developer': r'mobile|ios|android|react native|flutter developer',
                'DevOps Engineer': r'devops|site reliability|sre',
                'UI/UX Designer': r'ui/ux|user experience|product designer',
                'QA Engineer': r'qa|quality assurance|test engineer',
                'Data Engineer': r'data engineer|etl|data pipeline',
                'Machine Learning': r'ml engineer|machine learning|ai engineer',
                'Software Engineer': r'software engineer'
            }
            
            for role, pattern in tech_roles_patterns.items():
                if re.search(pattern, careers_html):
                    job_data['tech_roles'].append(role)
                    job_data['opportunity_score'] += 10
            
            # Count total job mentions
            job_keywords = ['position', 'opening', 'opportunity', 'role', 'job']
            total_count = sum(careers_html.count(keyword) for keyword in job_keywords)
            job_data['total_positions'] = min(total_count // 2, 50)  # Estimate
            
            if job_data['tech_roles']:
                job_data['jobs_found'] = True
                job_data['hiring_signals'].append(f'Hiring for {len(job_data["tech_roles"])} tech roles')
            
            # Additional signals
            if 'we\'re hiring' in careers_html or 'join our team' in careers_html:
                job_data['hiring_signals'].append('Active recruitment campaign')
                job_data['opportunity_score'] += 15
            
            if 'remote' in careers_html or 'work from home' in careers_html:
                job_data['hiring_signals'].append('Offers remote positions')
                job_data['opportunity_score'] += 5
            
            if any(word in careers_html for word in ['startup', 'fast-growing', 'scaling']):
                job_data['hiring_signals'].append('Growth-stage company')
                job_data['opportunity_score'] += 10
        
        # Classification
        if job_data['opportunity_score'] >= 40:
            opportunity_level = 'High - Active tech hiring'
        elif job_data['opportunity_score'] >= 20:
            opportunity_level = 'Medium - Some hiring activity'
        else:
            opportunity_level = 'Low - Limited or no hiring'
        
        job_data['opportunity_level'] = opportunity_level
        job_data['pitch'] = 'Staff augmentation, dedicated teams, outsourcing' if job_data['opportunity_score'] >= 30 else 'Talent acquisition services'
        
        return jsonify(job_data)
        
    except Exception as e:
        return jsonify({'error': f'Job intelligence failed: {str(e)}'}), 500


# ============== BUSINESS INTELLIGENCE (Funding, Ads, Product Launches) ==============
@scraper_bp.route('/api/business/intelligence', methods=['POST'])
def business_intelligence():
    """Comprehensive business intelligence - funding, ads, product launches"""
    try:
        data = request.json
        company_name = data.get('company_name', '').strip()
        domain = data.get('domain', '').strip()
        
        if not company_name and not domain:
            return jsonify({'error': 'Company name or domain is required'}), 400
        
        intel = {
            'funding': {'status': 'not_found', 'signals': []},
            'product_launches': {'status': 'not_found', 'signals': []},
            'ad_presence': {'status': 'not_found', 'signals': []},
            'business_score': 0
        }
        
        # 1. Funding signals (via news search)
        if company_name:
            try:
                funding_query = f'{company_name} funding raised investment'
                search_url = f"https://www.google.com/search?q={requests.utils.quote(funding_query)}&num=10"
                response = requests.get(search_url, headers=get_headers(), timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text().lower()
                
                funding_keywords = ['raised', 'funding', 'investment', 'series a', 'series b', 'seed round', 'venture capital']
                funding_found = sum(1 for kw in funding_keywords if kw in text)
                
                if funding_found >= 3:
                    intel['funding']['status'] = 'likely_funded'
                    intel['funding']['signals'].append(f'Funding mentions detected ({funding_found} keywords)')
                    intel['business_score'] += 30
                    
                    # Check for specific amounts
                    amounts = re.findall(r'\$[\d.]+[MBK]', text)
                    if amounts:
                        intel['funding']['signals'].append(f'Amounts found: {", ".join(amounts[:3])}')
            except:
                pass
        
        # 2. Product launch signals
        if domain:
            try:
                url = f'https://{domain}' if not domain.startswith('http') else domain
                
                # Check press/news page
                press_paths = ['/press', '/news', '/newsroom', '/blog']
                for path in press_paths:
                    try:
                        press_url = url + path
                        response = requests.get(press_url, headers=get_headers(), timeout=8)
                        if response.status_code == 200:
                            text = response.text.lower()
                            
                            launch_keywords = ['launch', 'announcement', 'new product', 'introducing', 'released']
                            launches = sum(1 for kw in launch_keywords if kw in text)
                            
                            if launches >= 2:
                                intel['product_launches']['status'] = 'active'
                                intel['product_launches']['signals'].append(f'Press/news page with {launches} launch mentions')
                                intel['business_score'] += 20
                            break
                    except:
                        pass
                
                # Check sitemap for new pages
                try:
                    sitemap_url = url + '/sitemap.xml'
                    response = requests.get(sitemap_url, timeout=8)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'xml')
                        lastmod_tags = soup.find_all('lastmod')
                        
                        if lastmod_tags:
                            recent_dates = [tag.text for tag in lastmod_tags if '2025' in tag.text or '2024' in tag.text]
                            if recent_dates:
                                intel['product_launches']['signals'].append(f'{len(recent_dates)} pages updated recently')
                                intel['business_score'] += 10
                except:
                    pass
            except:
                pass
        
        # 3. Ad presence (Facebook Ad Library check)
        if company_name:
            try:
                # Facebook Ad Library is public
                ad_search_url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q={requests.utils.quote(company_name)}"
                response = requests.get(ad_search_url, headers=get_headers(), timeout=10)
                
                if 'ad' in response.text.lower() and company_name.lower() in response.text.lower():
                    intel['ad_presence']['status'] = 'detected'
                    intel['ad_presence']['signals'].append('Facebook ads found')
                    intel['business_score'] += 15
                    
                    # Check landing page quality
                    if domain:
                        url = f'https://{domain}' if not domain.startswith('http') else domain
                        try:
                            import time
                            start = time.time()
                            page_response = requests.get(url, timeout=10)
                            load_time = time.time() - start
                            
                            if load_time > 4:
                                intel['ad_presence']['signals'].append(f'Landing page slow ({round(load_time, 1)}s) - optimization needed')
                            
                            soup = BeautifulSoup(page_response.text, 'html.parser')
                            
                            # Check for tracking
                            has_analytics = 'google-analytics' in page_response.text.lower() or 'gtag' in page_response.text.lower()
                            has_pixel = 'facebook.com/tr' in page_response.text.lower()
                            
                            if not has_analytics and not has_pixel:
                                intel['ad_presence']['signals'].append('No tracking detected - analytics setup needed')
                        except:
                            pass
            except:
                pass
        
        # Business classification
        if intel['business_score'] >= 50:
            intel['business_level'] = 'High Activity - Strong growth signals'
        elif intel['business_score'] >= 25:
            intel['business_level'] = 'Moderate Activity - Some opportunities'
        else:
            intel['business_level'] = 'Low Activity - Early stage or limited public presence'
        
        # Opportunity recommendations
        opportunities = []
        if intel['funding']['status'] == 'likely_funded':
            opportunities.append('Pitch: Web/mobile app development, automation, cloud services')
        if intel['product_launches']['status'] == 'active':
            opportunities.append('Pitch: App enhancements, maintenance, analytics dashboards')
        if intel['ad_presence']['status'] == 'detected':
            opportunities.append('Pitch: Landing page optimization, CRO, tracking setup')
        
        intel['opportunities'] = opportunities
        
        return jsonify(intel)
        
    except Exception as e:
        return jsonify({'error': f'Business intelligence failed: {str(e)}'}), 500
