#!/usr/bin/env python3
"""
Comprehensive Wikipedia Scraper - A-Z
Downloads all available Wikipedia articles alphabetically
Saves each article to its own category and file

Usage:
  python3 wiki_comprehensive.py [start_letter] [max_articles]
  
Examples:
  python3 wiki_comprehensive.py          # All articles A-Z
  python3 wiki_comprehensive.py M        # Start from M
  python3 wiki_comprehensive.py A 100    # First 100 starting with A
"""

import requests
import re
import os
import sys
import time
from urllib.parse import unquote
from collections import defaultdict

# Create Wiki folder
WIKI_FOLDER = "Wiki"
if not os.path.exists(WIKI_FOLDER):
    os.makedirs(WIKI_FOLDER)

# Rate limiting
DELAY = 0.5  # seconds between requests

def fetch_wikipedia_article(title):
    """Fetch article from Wikipedia API"""
    time.sleep(DELAY)  # Rate limit

    url = "https://en.wikipedia.org/w/api.php"
    headers = {"User-Agent": "ComprehensiveWikiScraper/1.0"}

    params = {
        "action": "query",
        "titles": title,
        "prop": "extracts",
        "explaintext": True,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        
        data = response.json()
        if 'query' not in data or 'pages' not in data['query']:
            return None
        
        pages = data['query']['pages']
        page = next(iter(pages.values()))
        
        if 'extract' in page and page['extract']:
            return page['extract']
        return None
    except Exception as e:
        return None

def get_articles_by_letter(letter, limit=None):
    """Get all articles starting with a letter from Wikipedia"""
    print(f"\n📖 Fetching article list for '{letter}'...")

    time.sleep(DELAY)  # Rate limit

    url = "https://en.wikipedia.org/w/api.php"
    headers = {"User-Agent": "ComprehensiveWikiScraper/1.0"}

    params = {
        "action": "query",
        "list": "allpages",
        "apprefix": letter,
        "aplimit": "500",  # Max per request
        "format": "json"
    }

    articles = []
    retries = 3

    try:
        while True:
            for attempt in range(retries):
                try:
                    response = requests.get(url, params=params, headers=headers, timeout=10)
                    data = response.json()
                    break
                except Exception as e:
                    if attempt < retries - 1:
                        time.sleep(2)  # Wait before retry
                        continue
                    raise
            
            if 'query' not in data or 'allpages' not in data['query']:
                break
            
            page_list = data['query']['allpages']
            
            for page in page_list:
                # Skip disambiguation pages, redirects, and special pages
                title = page['title']
                if any(skip in title for skip in ['(disambiguation)', 'Wikipedia:', 'Special:', 'Template:']):
                    continue
                
                articles.append(title)
                
                if limit and len(articles) >= limit:
                    return articles
            
            # Check for continuation
            if 'continue' not in data:
                break
            
            params['apcontinue'] = data['continue']['apcontinue']
    
    except Exception as e:
        print(f"  ⚠️  Error fetching list: {e}")
    
    return articles

def extract_training_data(text, category, max_length=300):
    """Convert Wikipedia text to training format"""
    training_lines = []
    
    if not text:
        return []
    
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        
        if len(paragraph) < 20:
            continue
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)
        
        for sentence in sentences:
            sentence = sentence.strip()
            
            if 10 < len(sentence) < max_length:
                if not sentence.startswith(('See also', 'References', 'Contents', '==')):
                    training_lines.append(f"{category}: {sentence}")
    
    return training_lines

def save_training_file(training_data, category):
    """Save training data for a category"""
    if not training_data:
        return 0
    
    filename = f"{category}_wiki.txt"
    filepath = os.path.join(WIKI_FOLDER, filename)
    
    unique_lines = list(set(training_data))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in unique_lines:
            f.write(line + '\n')
    
    return len(unique_lines)

def main():
    print("=" * 70)
    print("COMPREHENSIVE WIKIPEDIA SCRAPER - A-Z")
    print("=" * 70)
    
    # Parse arguments
    start_letter = sys.argv[1].upper() if len(sys.argv) > 1 else 'A'
    max_per_letter = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    # Validate start letter
    if not start_letter.isalpha() or len(start_letter) != 1:
        print("❌ Invalid start letter. Use A-Z")
        sys.exit(1)
    
    print(f"\n🔤 Starting from: {start_letter}")
    if max_per_letter:
        print(f"📊 Max articles per letter: {max_per_letter}")
    print(f"📂 Output folder: {WIKI_FOLDER}/\n")
    
    all_stats = defaultdict(int)
    total_downloaded = 0
    total_lines = 0
    
    # Process A-Z
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    start_idx = letters.index(start_letter)
    
    for idx, letter in enumerate(letters[start_idx:], 1):
        print(f"\n{'=' * 70}")
        print(f"LETTER {letter} [{idx}/{26-start_idx}]")
        print('=' * 70)
        
        # Get articles for this letter
        article_list = get_articles_by_letter(letter, max_per_letter)
        print(f"  Found {len(article_list)} articles")
        
        if not article_list:
            print(f"  ⚠️  No articles found for '{letter}'")
            continue
        
        letter_downloaded = 0
        letter_lines = 0
        
        for article_idx, article_title in enumerate(article_list, 1):
            # Create category from title
            category = article_title.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(":", "")
            
            # Fetch article
            content = fetch_wikipedia_article(article_title)
            
            if not content:
                continue
            
            # Extract and save
            training_data = extract_training_data(content, category)
            
            if training_data:
                lines_saved = save_training_file(training_data, category)
                letter_downloaded += 1
                letter_lines += lines_saved
                total_lines += lines_saved
                
                # Progress indicator
                if article_idx % 10 == 0:
                    print(f"  ✓ Downloaded {article_idx}/{len(article_list)}: {article_title}")
        
        total_downloaded += letter_downloaded
        all_stats[letter] = (letter_downloaded, letter_lines)
        
        print(f"\n  📊 Letter {letter}: {letter_downloaded} articles, {letter_lines} lines")
    
    # Summary
    print(f"\n\n{'=' * 70}")
    print("COMPREHENSIVE SCRAPE COMPLETE")
    print('=' * 70)
    
    print(f"\n📈 Statistics by Letter:")
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if letter in all_stats:
            articles, lines = all_stats[letter]
            print(f"  {letter}: {articles:3d} articles, {lines:6d} lines")
    
    print(f"\n{'=' * 70}")
    print(f"✅ TOTAL: {total_downloaded} articles downloaded")
    print(f"📊 TOTAL: {total_lines} training lines")
    print(f"📂 Saved to: {WIKI_FOLDER}/")
    print(f"{'=' * 70}")
    
    print(f"\n📋 Next steps:")
    print(f"  1. Copy files: cp {WIKI_FOLDER}/*.txt training/")
    print(f"  2. Compile: g++ -std=c++17 -O2 Killo.cpp -o Killo")
    print(f"  3. Run: ./Killo")

if __name__ == "__main__":
    main()
