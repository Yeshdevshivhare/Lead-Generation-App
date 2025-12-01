# 🎯 OSINT Features - Complete Guide

## New Intelligence Gathering Tools

### 1. 🔍 Google Dorking

**Purpose:** Discover hidden pages, documents, and data using advanced search operators

**How to Use:**
1. Navigate to "Google Dorking" tab
2. Enter search query with operators
3. Click "Search & Parse"
4. Results appear in-app with titles, URLs, and snippets

**Example Queries:**
```
"startup" site:.in
intitle:"about us" "company"
intext:"@company.com"
"sports analytics" "startup"
"AI automation" filetype:pdf
inurl:login site:example.com
```

**Common Operators:**
- `site:` - Search specific domain
- `intitle:` - Words in title
- `intext:` - Words in body
- `inurl:` - Words in URL
- `filetype:` - Specific file types (pdf, doc, xls)
- `before:` / `after:` - Date ranges

**What You Get:**
- Up to 15 result URLs
- Page titles and snippets
- Direct links to discovered pages
- Save capability for future reference

**Use Cases:**
- Find competitor landing pages
- Discover company documentation
- Locate contact pages
- Find specific file types
- Research industry insights

---

### 2. 🐙 GitHub Intelligence

**Purpose:** Discover company tech stack, engineers, and internal tools through public repositories

**How to Use:**
1. Go to "GitHub Intel" tab
2. Enter company name or domain
3. Click "Search GitHub"
4. View public repos and insights

**What It Finds:**
- Public repositories mentioning company
- Company email addresses in commits
- Staff names in contributor lists
- README files with company info
- Tech stack indicators (package.json, dependencies)

**Insights Provided:**
- Repository count and names
- Links to all repos
- Technical stack used
- Current engineers
- Internal tool mentions

**Use Cases:**
- Identify tech stack before sales call
- Find employee names for outreach
- Discover open source projects
- Competitive intelligence
- Talent acquisition research

---

### 3. 📡 RSS Feed Discovery

**Purpose:** Auto-detect content feeds to track marketing activity and publishing frequency

**How to Use:**
1. Navigate to "RSS Feeds" tab
2. Enter website URL
3. Click "Discover Feeds"
4. See all detected feeds

**What It Discovers:**
- `/feed` - Main RSS feed
- `/rss` - Alternative RSS
- `/blog/feed` - Blog feed
- `/atom.xml` - Atom feeds
- HTML-declared feeds
- Multiple feed formats

**Insights:**
- Content publishing frequency
- Blog activity level
- Marketing budget indicators
- Product announcement channels
- Company news sources

**Use Cases:**
- Monitor competitor content
- Track product announcements
- Identify active bloggers
- Marketing intelligence
- Content strategy research

---

### 4. 🎯 Competitor Cross-Mapping

**Purpose:** Identify competitor mentions, integrations, and tech partnerships

**How to Use:**
1. Go to "Competitors" tab
2. Enter target website URL
3. Click "Analyze"
4. View integrations and partners

**What It Detects:**
- Salesforce integration
- HubSpot connections
- Slack mentions
- Zoom integration
- Microsoft Teams
- Google Workspace
- Stripe payment
- PayPal integration

**Additional Data:**
- Partner logos on page
- Client/customer mentions
- Integration page content
- Tech partnership indicators

**Use Cases:**
- Understand tech ecosystem
- Identify partnership opportunities
- Competitive positioning
- Integration strategy
- Market positioning

---

### 5. 🔑 Keyword Intelligence

**Purpose:** Score page relevance based on keyword density and strategic matches

**How to Use:**
1. Navigate to "Keyword Intel" tab
2. Enter website URL
3. Enter keywords (comma-separated) or use defaults
4. Click "Analyze Keywords"
5. View relevance score and details

**Default Keywords:**
- automation
- AI
- CRM
- analytics
- enterprise
- SaaS

**What You Get:**
- Relevance score (0-100)
- Keywords found on page
- Occurrence count per keyword
- Keyword density percentages
- Total words analyzed

**Scoring:**
- 60-100: Highly relevant
- 30-60: Moderately relevant
- 0-30: Low relevance

**Use Cases:**
- Lead qualification
- Content relevance scoring
- SEO analysis
- Competitor positioning
- Market fit assessment

---

### 6. ⭐ AI Lead Scoring

**Purpose:** Comprehensive intent scoring based on multiple buying signals

**How to Use:**
1. Go to "Lead Scoring" tab
2. Enter website URL
3. Click "Calculate Score"
4. Review score and signals

**Scoring Factors:**

| Signal | Points | Indicator |
|--------|--------|-----------|
| Job postings | +20 | Active hiring (growth) |
| Blog activity | +15 | Recent content (engagement) |
| Social presence | +10 | 3+ social profiles |
| Contact forms | +10 | Lead capture active |
| Email addresses | +10 | Multiple contacts (2+) |
| Tech stack | +15 | Advanced tech (3+ indicators) |
| Premium keywords | +20 | Enterprise positioning |

**Score Interpretation:**
- **70-100 (High)**: Priority lead - Strong buying signals
- **40-69 (Medium)**: Monitor - Some engagement potential  
- **0-39 (Low)**: Nurture - Early stage

**Recommendations:**
- **Priority Lead**: Immediate outreach recommended
- **Monitor**: Track for signals, engage soon
- **Nurture**: Add to drip campaign

**Detected Signals:**
- ✓ Active hiring detected
- ✓ Active blog/content
- ✓ 5 social profiles found
- ✓ Contact form available
- ✓ 8 email addresses found
- ✓ Advanced tech stack (React, API)
- ✓ Premium/enterprise positioning

**Use Cases:**
- Prioritize leads
- Sales qualification
- Timing outreach
- Resource allocation
- Campaign targeting

---

## Tooltip System

**Features:**
- Hover over tool buttons in sidebar
- Instant tooltip with description
- Explains what each tool does
- Shows expected impact
- Positioned to the right of button

**Implementation:**
- Dark theme tooltips
- Arrow pointing to button
- Smooth fade-in animation
- 240px width for readability
- Auto-dismiss on mouse out

---

## Data Persistence

### Saving Results

**All Tools Support:**
- Save button on result cards
- Stored in browser LocalStorage
- Includes timestamp
- Categorized by tool type
- Accessible via "Saved Results"

**What Gets Saved:**
- Tool type (dorking, github, etc.)
- Target URL/query
- Complete result data
- Timestamp of scan
- All extracted information

### Viewing Saved Data

1. Go to "Saved Results" tab
2. See all saved scans
3. Click "View" for full data
4. Click "Delete" to remove
5. Use "Clear All" to reset

### Dashboard Analytics

**Tracks:**
- Total scans performed
- Saved results count
- Today's activity
- Recent 5 operations

---

## Best Practices

### Google Dorking
- Start with broad queries, refine
- Use site: for targeted searches
- Combine multiple operators
- Respect robots.txt
- Don't overwhelm servers

### GitHub Intel
- Search company domain, not just name
- Look for email patterns (@company.com)
- Check commit history for engineers
- Review package.json for tech stack
- Respect rate limits

### RSS Feeds
- Check /blog and /news paths
- Use feeds to monitor competitors
- Track publishing frequency
- Set up feed readers for monitoring
- Look for announcement feeds

### Competitor Analysis
- Analyze integration pages
- Check footer partner logos
- Look for API documentation
- Review case study mentions
- Note technology choices

### Keyword Intelligence
- Use industry-specific keywords
- Analyze competitor keywords
- Track keyword density trends
- Compare multiple competitors
- Score against ideal customer profile

### Lead Scoring
- Run on homepage for best results
- Check /about and /careers pages
- Combine with other tools
- Score regularly for changes
- Use for prioritization

---

## Advanced Workflows

### Complete Lead Profile

1. **WHOIS Lookup** - Verify domain ownership
2. **Web Scraper** - Extract contacts
3. **Tech Stack** - Identify technologies
4. **GitHub Intel** - Find engineers and repos
5. **RSS Feeds** - Check content frequency
6. **Competitor Analysis** - See partnerships
7. **Keyword Intel** - Score relevance
8. **Lead Scoring** - Final intent score
9. **Save All Results** - Store complete profile

### Competitive Intelligence

1. **Google Dorking** - Find competitor pages
2. **Web Scraper** - Extract contacts
3. **Tech Stack** - Analyze technologies
4. **Competitor Analysis** - Find integrations
5. **RSS Feeds** - Monitor content
6. **Keyword Intel** - Compare positioning

### Outreach Preparation

1. **Web Scraper** - Get emails/phones
2. **Social Intel** - Find social profiles
3. **GitHub Intel** - Identify engineers
4. **Lead Scoring** - Qualify lead
5. **RSS Feeds** - Recent announcements
6. **Save Profile** - Store for CRM

---

## Privacy & Ethics

### Responsible Use
- ✅ Only access public data
- ✅ Respect robots.txt
- ✅ Follow rate limits
- ✅ Don't scrape private data
- ✅ Comply with terms of service

### What NOT to Do
- ❌ Scrape personal information
- ❌ Overwhelm target servers
- ❌ Violate website ToS
- ❌ Store sensitive data
- ❌ Use for spam

### Legal Compliance
- Follow GDPR guidelines
- Respect CCPA requirements
- Only business intelligence
- Public data only
- Legitimate business purpose

---

## Troubleshooting

### Google Dorking
**No results?**
- Try simpler query
- Remove some operators
- Check spelling
- Use broader terms

**Timeout?**
- Google may be rate limiting
- Wait 30 seconds
- Try different query
- Use VPN if needed

### GitHub Intel
**No repos found?**
- Try company name instead of domain
- Search @company.com pattern
- Check spelling
- Company may not be on GitHub

### RSS Feeds
**No feeds detected?**
- Site may not have RSS
- Try /blog/feed path
- Check /news section
- Some sites hide feeds

### Lead Scoring
**Low score for known good lead?**
- Check specific pages (/about, /careers)
- Score multiple pages
- Signals may be subtle
- Combine with manual review

---

## API Endpoints

### New OSINT Endpoints

```
POST /api/dork/search
Body: { "query": "search terms" }
Returns: { "results": [...], "total": 15 }

POST /api/osint/github
Body: { "company": "example.com" }
Returns: { "repos": [...], "insights": [...] }

POST /api/osint/feeds
Body: { "url": "https://example.com" }
Returns: { "feeds": [...], "total": 3 }

POST /api/osint/competitors
Body: { "url": "https://example.com" }
Returns: { "integrations": [...], "partners": [...] }

POST /api/osint/keywords
Body: { "url": "https://example.com", "keywords": [] }
Returns: { "relevance_score": 75, "keyword_details": {...} }

POST /api/osint/score
Body: { "url": "https://example.com" }
Returns: { "score": 85, "intent_level": "High", "signals": [...] }
```

---

## Quick Reference

| Tool | Input | Output | Save? |
|------|-------|--------|-------|
| Google Dorking | Search query | URLs, titles, snippets | ✅ |
| GitHub Intel | Company name | Repos, engineers | ✅ |
| RSS Feeds | Website URL | Feed URLs, status | ✅ |
| Competitors | Website URL | Integrations, partners | ✅ |
| Keyword Intel | URL + keywords | Score, density | ✅ |
| Lead Scoring | Website URL | Score, signals | ✅ |

---

**All OSINT features work offline and store results locally. No external tracking.**
