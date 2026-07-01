#!/usr/bin/env python3
"""
Comprehensive Wikipedia Scraper - A-Z
Downloads all available Wikipedia articles alphabetically
Saves each article to its own category and file

Uses Botasaurus for robust scraping, falls back to requests if needed.

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
from user_agent_rotator import get_user_agent, switch_user_agent

# Try to import Botasaurus, fall back to requests if not available
try:
    from botasaurus import Browser
    HAS_BOTASAURUS = True
except ImportError:
    HAS_BOTASAURUS = False

# Optional: use BeautifulSoup for parsing
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

# Create Wiki folder
WIKI_FOLDER = "Wiki"
if not os.path.exists(WIKI_FOLDER):
    os.makedirs(WIKI_FOLDER)

# Rate limiting
DELAY = 0.5  # seconds between requests

def fetch_article_botasaurus(title):
    """Fetch article using Botasaurus (more robust)"""
    if not HAS_BOTASAURUS:
        return None

    try:
        browser = Browser()
        url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        response = browser.get(url)

        if response.status_code == 200:
            if HAS_BS4:
                soup = BeautifulSoup(response.content, 'html.parser')
                content_div = soup.find('div', {'id': 'mw-content-text'})
                if content_div:
                    return content_div.get_text()
            else:
                # Fallback: extract text without BeautifulSoup
                return response.text

        return None
    except Exception as e:
        return None

def fetch_article_api(title, retries=2):
    """Fetch article using Wikipedia API with retries"""
    time.sleep(DELAY)

    url = "https://en.wikipedia.org/w/api.php"
    headers = {"User-Agent": get_user_agent()}

    params = {
        "action": "query",
        "titles": title,
        "prop": "extracts",
        "explaintext": True,
        "format": "json"
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 429:
                # Rate limited - switch user agent and retry immediately
                headers["User-Agent"] = switch_user_agent()
                if attempt < retries - 1:
                    continue
                return None
            elif response.status_code == 200:
                data = response.json()
                if 'query' in data and 'pages' in data['query']:
                    pages = data['query']['pages']
                    page = next(iter(pages.values()))
                    if 'extract' in page and page['extract']:
                        return page['extract']
                return None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            return None

    return None

def fetch_wikipedia_article(title, retries=2):
    """Fetch article - try Botasaurus first, fall back to API"""
    # Try Botasaurus first (more robust)
    if HAS_BOTASAURUS:
        content = fetch_article_botasaurus(title)
        if content:
            return content

    # Fall back to API
    return fetch_article_api(title, retries)

def get_articles_by_letter_botasaurus(letter, limit=None):
    """Get articles using Botasaurus"""
    if not HAS_BOTASAURUS or not HAS_BS4:
        return []

    articles = []
    try:
        browser = Browser()
        url = f"https://en.wikipedia.org/wiki/Special:AllPages?from={letter}&to={letter}z"
        response = browser.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=re.compile('/wiki/'))

            for link in links:
                title = link.get_text().strip()
                href = link.get('href', '')

                if any(skip in href for skip in ['Special:', 'Category:', 'Template:', '(disambiguation)']):
                    continue

                if title and title not in articles:
                    articles.append(title)
                    if limit and len(articles) >= limit:
                        break

        return articles
    except Exception as e:
        return []

def get_articles_by_letter_api(letter, limit=None):
    """Get articles using Wikipedia API"""
    print(f"\n📖 Fetching article list for '{letter}'...")

    time.sleep(DELAY)

    url = "https://en.wikipedia.org/w/api.php"
    headers = {"User-Agent": get_user_agent()}

    params = {
        "action": "query",
        "list": "allpages",
        "apprefix": letter,
        "aplimit": "500",
        "format": "json"
    }

    articles = []
    retries = 3

    try:
        while True:
            data = None
            for attempt in range(retries):
                try:
                    response = requests.get(url, params=params, headers=headers, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        break
                    elif response.status_code == 429:
                        headers["User-Agent"] = switch_user_agent()
                        if attempt < retries - 1:
                            continue
                        return articles

                except Exception as e:
                    if attempt < retries - 1:
                        print(f"    Retry {attempt + 1}/{retries}...")
                        time.sleep(2)
                        continue
                    else:
                        print(f"  ⚠️  Failed after retries: {str(e)[:50]}")
                        return articles

            if not data:
                print(f"  ⚠️  No data returned from API")
                break

            if 'query' not in data:
                if 'error' in data:
                    print(f"  ⚠️  API Error: {data['error'].get('info', 'Unknown')}")
                break

            if 'allpages' not in data['query']:
                print(f"  ℹ️  No allpages in response (may be empty or filtered)")
                break

            page_list = data['query']['allpages']

            for page in page_list:
                title = page['title']
                if any(skip in title for skip in ['(disambiguation)', 'Wikipedia:', 'Special:', 'Template:']):
                    continue

                articles.append(title)

                if limit and len(articles) >= limit:
                    return articles

            if 'continue' not in data:
                break

            params['apcontinue'] = data['continue']['apcontinue']
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n  ⏹️  Stopped by user. Found {len(articles)} articles so far.")
        return articles
    except Exception as e:
        print(f"  ⚠️  Error: {e}")

    return articles

def get_articles_by_letter(letter, limit=None):
    """Get articles - try Botasaurus first, fall back to API"""
    # Try Botasaurus first
    if HAS_BOTASAURUS:
        articles = get_articles_by_letter_botasaurus(letter, limit)
        if articles:
            print(f"  Found {len(articles)} articles (via Botasaurus)")
            return articles

    # Fall back to API
    return get_articles_by_letter_api(letter, limit)

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
    if HAS_BOTASAURUS:
        print("✓ Using Botasaurus (robust) + requests (fallback)")
    else:
        print("Using requests (Botasaurus not installed)")
    print("=" * 70)

    start_letter = sys.argv[1].upper() if len(sys.argv) > 1 else 'A'
    max_per_letter = int(sys.argv[2]) if len(sys.argv) > 2 else None

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

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    start_idx = letters.index(start_letter)

    for idx, letter in enumerate(letters[start_idx:], 1):
        print(f"\n{'=' * 70}")
        print(f"LETTER {letter} [{idx}/{26-start_idx}]")
        print('=' * 70)

        article_list = get_articles_by_letter(letter, max_per_letter)
        print(f"  Found {len(article_list)} articles")

        if not article_list:
            print(f"  ⚠️  No articles found for '{letter}'")
            continue

        letter_downloaded = 0
        letter_lines = 0

        for article_idx, article_title in enumerate(article_list, 1):
            category = article_title.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(":", "")

            content = fetch_wikipedia_article(article_title)

            if not content:
                continue

            training_data = extract_training_data(content, category)

            if training_data:
                lines_saved = save_training_file(training_data, category)
                letter_downloaded += 1
                letter_lines += lines_saved
                total_lines += lines_saved

                if article_idx % 10 == 0:
                    print(f"  ✓ Downloaded {article_idx}/{len(article_list)}: {article_title}")

        total_downloaded += letter_downloaded
        all_stats[letter] = (letter_downloaded, letter_lines)

        print(f"\n  📊 Letter {letter}: {letter_downloaded} articles, {letter_lines} lines")

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
