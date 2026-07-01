#!/usr/bin/env python3
"""
Botasaurus-based Wikipedia A-Z Scraper
More robust than raw requests - handles caching, retries, sessions
"""

import sys
import os
import re
from botasaurus import Browser, Request
from bs4 import BeautifulSoup
from collections import defaultdict

WIKI_FOLDER = "../../Wiki"
if not os.path.exists(WIKI_FOLDER):
    os.makedirs(WIKI_FOLDER)

def fetch_article_with_botasaurus(title):
    """Fetch Wikipedia article using Botasaurus"""
    try:
        browser = Browser()
        url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

        # Botasaurus handles retries, caching, user-agents automatically
        response = browser.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract main content
            content_div = soup.find('div', {'id': 'mw-content-text'})
            if content_div:
                text = content_div.get_text()
                return text

        return None
    except Exception as e:
        return None

def fetch_allpages_with_botasaurus(letter, limit=None):
    """Fetch article list for a letter using Botasaurus"""
    articles = []
    try:
        browser = Browser()

        # Use the Special:AllPages endpoint with Botasaurus
        url = f"https://en.wikipedia.org/wiki/Special:AllPages?from={letter}&to={letter}z"

        response = browser.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all article links
            links = soup.find_all('a', href=re.compile('/wiki/'))

            for link in links:
                title = link.get_text().strip()
                href = link.get('href', '')

                # Skip special pages
                if any(skip in href for skip in ['Special:', 'Category:', 'Template:']):
                    continue

                if title and title not in articles:
                    articles.append(title)

                    if limit and len(articles) >= limit:
                        break

        return articles
    except Exception as e:
        print(f"  ⚠️  Error: {e}")
        return articles

def extract_training_data(text, category, max_length=300):
    """Convert text to training format"""
    training_lines = []

    if not text:
        return []

    # Split into paragraphs
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
    """Save training data"""
    if not training_data:
        return 0

    filename = f"{category}_botasaurus_wiki.txt"
    filepath = os.path.join(WIKI_FOLDER, filename)

    unique_lines = list(set(training_data))

    with open(filepath, 'w', encoding='utf-8') as f:
        for line in unique_lines:
            f.write(line + '\n')

    return len(unique_lines)

def main():
    print("=" * 70)
    print("BOTASAURUS WIKIPEDIA A-Z SCRAPER")
    print("=" * 70)

    if len(sys.argv) < 2:
        print("\nUsage: python3 wiki_botasaurus.py [start_letter] [max_articles]")
        print("Examples:")
        print("  python3 wiki_botasaurus.py A 100")
        print("  python3 wiki_botasaurus.py B")
        sys.exit(1)

    start_letter = sys.argv[1].upper()
    max_per_letter = int(sys.argv[2]) if len(sys.argv) > 2 else None

    print(f"\n🤖 Using Botasaurus (better retry logic, caching, sessions)")
    print(f"📖 Starting from: {start_letter}")
    if max_per_letter:
        print(f"📊 Max per letter: {max_per_letter}")

    all_stats = defaultdict(int)
    total_downloaded = 0
    total_lines = 0

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    start_idx = letters.index(start_letter)

    for idx, letter in enumerate(letters[start_idx:], 1):
        print(f"\n{'=' * 70}")
        print(f"LETTER {letter} [{idx}/{26-start_idx}]")
        print('=' * 70)

        # Get articles for this letter
        article_list = fetch_allpages_with_botasaurus(letter, max_per_letter)
        print(f"  Found {len(article_list)} articles")

        if not article_list:
            continue

        letter_downloaded = 0
        letter_lines = 0

        for article_idx, article_title in enumerate(article_list, 1):
            category = article_title.lower().replace(" ", "_").replace("(", "").replace(")", "")

            content = fetch_article_with_botasaurus(article_title)

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

    # Summary
    print(f"\n\n{'=' * 70}")
    print("BOTASAURUS SCRAPE COMPLETE")
    print('=' * 70)

    print(f"\n📈 Results by Letter:")
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if letter in all_stats:
            articles, lines = all_stats[letter]
            print(f"  {letter}: {articles:3d} articles, {lines:6d} lines")

    print(f"\n{'=' * 70}")
    print(f"✅ TOTAL: {total_downloaded} articles downloaded")
    print(f"📊 TOTAL: {total_lines} training lines")
    print(f"📂 Saved to: {WIKI_FOLDER}/")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    main()
