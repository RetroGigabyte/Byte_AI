#!/usr/bin/env python3
"""
Flexible Wikipedia Training Data Extractor
Edit the ARTICLES list below to extract ANY Wikipedia articles you want!

Format:
    ("emoji", "Wikipedia Article Title", "category_name")

Examples:
    ("🚗", "Tesla Model 3", "tesla")
    ("⚡", "Electric vehicle", "electric_vehicle")
    ("🏥", "COVID-19 pandemic", "covid")
    ("🧬", "DNA", "dna")
"""

import requests
import re
import os
import sys
from urllib.parse import unquote
from user_agent_rotator import get_user_agent

# Create Wiki folder if it doesn't exist
WIKI_FOLDER = "Wiki"
if not os.path.exists(WIKI_FOLDER):
    os.makedirs(WIKI_FOLDER)
    print(f"📁 Created folder: {WIKI_FOLDER}\n")

def fetch_wikipedia_article(title):
    """Fetch article from Wikipedia API"""
    url = "https://en.wikipedia.org/w/api.php"

    headers = {
        "User-Agent": get_user_agent()
    }

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
            print(f"  ⚠️  Wikipedia returned status {response.status_code}")
            return None

        data = response.json()

        if 'query' not in data or 'pages' not in data['query']:
            print(f"  ⚠️  Invalid response from Wikipedia")
            return None

        pages = data['query']['pages']
        page = next(iter(pages.values()))

        if 'extract' in page and page['extract']:
            return page['extract']
        else:
            return None
    except Exception as e:
        print(f"  ⚠️  Error fetching: {e}")
        return None


def extract_links(text):
    """Extract Wikipedia article links from text"""
    links = set()
    # Match wiki link patterns like [[Article]] or [[Article|display text]]
    pattern = r'\[\[([^\]|]+)'
    matches = re.findall(pattern, text)

    for match in matches:
        link = match.strip()
        # Filter out non-articles (files, categories, etc.)
        if not any(x in link.lower() for x in ['file:', 'category:', 'wikipedia:', 'template:']):
            links.add(link)

    return list(links)[:10]  # Limit to first 10 links per page


def get_article_links(title):
    """Get links from a Wikipedia article"""
    url = "https://en.wikipedia.org/w/api.php"

    headers = {
        "User-Agent": get_user_agent()
    }

    params = {
        "action": "query",
        "titles": title,
        "prop": "links",
        "pllimit": "20",
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        if 'query' not in data or 'pages' not in data['query']:
            return []

        pages = data['query']['pages']
        page = next(iter(pages.values()))

        if 'links' in page:
            links = [link['title'] for link in page['links']
                    if ':' not in link['title']]  # Filter out special pages
            return links[:10]  # Limit to first 10

        return []
    except Exception as e:
        return []


def download_recursive(start_title, base_category, max_depth=2, visited=None):
    """Recursively download Wikipedia articles - each article gets its own category and file"""
    if visited is None:
        visited = set()

    if not start_title or start_title in visited or max_depth == 0:
        return {}

    visited.add(start_title)
    all_training_data = {}  # Changed to dict: {category: [training lines]}

    print(f"  📥 Downloading: {start_title}")

    # Fetch article
    content = fetch_wikipedia_article(start_title)

    if content:
        print(f"    ✓ Retrieved ({len(content)} chars)")

        # Create category for THIS article (based on title, not base_category)
        article_category = start_title.lower().replace(" ", "_").replace("(", "").replace(")", "")

        # Extract training data with article-specific category
        training_data = extract_training_data(content, article_category)
        if training_data:
            print(f"    ✓ Generated {len(training_data)} training lines for category: {article_category}")
            all_training_data[article_category] = training_data

        # Get linked articles
        if max_depth > 1:
            print(f"    🔗 Finding linked articles...")
            links = get_article_links(start_title)

            for link in links:
                if link not in visited:
                    print(f"    → Following link: {link}")
                    linked_data = download_recursive(link, base_category, max_depth - 1, visited)
                    # Merge linked articles' data
                    all_training_data.update(linked_data)
    else:
        print(f"    ⚠️  Article not found")

    return all_training_data


def extract_training_data(text, category, max_length=300):
    """Convert Wikipedia text to training format"""
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
            
            # Filter valid sentences
            if 10 < len(sentence) < max_length:
                if not sentence.startswith(('See also', 'References', 'Contents', '==')):
                    training_lines.append(f"{category}: {sentence}")
    
    return training_lines


def save_training_file(training_data, filename="wikipedia_training.txt"):
    """Save training data to Wiki folder"""
    if not training_data:
        print(f"  ⚠️  No training data to save")
        return
    
    unique_lines = list(set(training_data))
    
    # Full path with Wiki folder
    filepath = os.path.join(WIKI_FOLDER, filename)
    
    print(f"\n💾 Saving to {filepath}")
    print(f"  Total lines: {len(training_data)}")
    print(f"  Unique lines: {len(unique_lines)}")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in unique_lines:
            f.write(line + '\n')
    
    print(f"✓ Saved {filepath}")


# ============================================
# EDIT THIS LIST - ADD ANY WIKIPEDIA ARTICLES
# ============================================
# Format: ("emoji", "Wikipedia Article Title Exactly", "category_name_no_spaces")
# 
# TIPS:
# - Article title must match Wikipedia exactly (use search if unsure)
# - Category name will be used for training: category_name: sentence
# - Emoji is just for display
# - You can have multiple articles with same category (they'll combine)
#
# EXAMPLES TO ADD:
#   ("🚗", "Tesla (company)", "tesla"),
#   ("⚽", "Soccer", "soccer"),
#   ("🍕", "Pizza", "pizza"),
#   ("🎵", "Music", "music"),
#   ("🏀", "Basketball", "basketball"),

ARTICLES = [
    # ========== EDIT BELOW ==========
    # Add your Wikipedia articles here!
    # Just copy the format and change the title and category



]
    


# ============================================
# RUN EXTRACTION
# ============================================

if __name__ == "__main__":

    print("=" * 60)
    print("FLEXIBLE WIKIPEDIA TRAINING DATA EXTRACTOR")
    print("=" * 60)

    # Check for list mode
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ["--list", "-l"]:
            if len(sys.argv) < 3:
                print("\n❌ Usage: python3 wiki.py --list <articles.txt>")
                print("\nExample articles.txt:")
                print("  Machine Learning")
                print("  Artificial Intelligence")
                print("  Python (programming language)")
                print("  Deep Learning")
                exit(1)

            list_file = sys.argv[2]

            if not os.path.exists(list_file):
                print(f"\n❌ File not found: {list_file}")
                exit(1)

            # Read articles from file
            with open(list_file, 'r', encoding='utf-8') as f:
                articles = [line.strip() for line in f if line.strip() and not line.startswith('#')]

            print(f"\n📋 LIST MODE")
            print(f"  Reading from: {list_file}")
            print(f"  Articles to download: {len(articles)}\n")

            all_training_data = {}
            successful = 0

            for idx, article_title in enumerate(articles, 1):
                print(f"[{idx}/{len(articles)}] 📥 {article_title}...")

                content = fetch_wikipedia_article(article_title)

                if content:
                    # Create category from article title
                    article_category = article_title.lower().replace(" ", "_").replace("(", "").replace(")", "")
                    training_data = extract_training_data(content, article_category)

                    if training_data:
                        all_training_data[article_category] = training_data
                        print(f"  ✓ Generated {len(training_data)} lines")
                        successful += 1
                    else:
                        print(f"  ⚠️  No training data extracted")
                else:
                    print(f"  ⚠️  Article not found")

            # Save all downloaded articles
            if all_training_data:
                print(f"\n" + "=" * 60)
                print(f"SAVING {len(all_training_data)} ARTICLES")
                print("=" * 60)

                total_lines = 0
                for article_category, lines in all_training_data.items():
                    filename = f"{article_category}_wiki.txt"
                    filepath = os.path.join(WIKI_FOLDER, filename)

                    unique_lines = list(set(lines))
                    total_lines += len(unique_lines)

                    with open(filepath, 'w', encoding='utf-8') as f:
                        for line in unique_lines:
                            f.write(line + '\n')

                    print(f"✓ {article_category:40s} → {len(unique_lines):5d} lines")

                print("\n" + "=" * 60)
                print(f"✅ COMPLETE: Downloaded {successful}/{len(articles)} articles")
                print(f"📊 Total lines saved: {total_lines}")
                print(f"📂 Location: {WIKI_FOLDER}/")
                print("=" * 60)
            else:
                print("\n❌ No articles downloaded")

            exit(0)

        elif sys.argv[1].lower() in ["--recursive", "-r"]:
            if len(sys.argv) < 4:
                print("\n❌ Usage: python3 wiki.py --recursive <article> <category> [depth]")
                print("\nExamples:")
                print("  python3 wiki.py --recursive 'Machine Learning' ai 2")
                print("  python3 wiki.py -r 'Python (programming language)' python 3")
                print("  python3 wiki.py -r 'Kingdom of Great Britain' 'great britain' 4")
                exit(1)

            title = sys.argv[2]
            category = sys.argv[3]

            # Find depth - look for last numeric argument
            depth = 2  # default
            for arg in reversed(sys.argv[4:]):
                try:
                    depth = int(arg)
                    break
                except ValueError:
                    continue

            print(f"\n🔄 RECURSIVE WIKIPEDIA MODE")
            print(f"  Article: {title}")
            print(f"  Category: {category}")
            print(f"  Depth: {depth}\n")

            training_data = download_recursive(title, category, max_depth=depth)

            if training_data:
                print(f"\n✓ Downloaded {len(training_data)} articles with separate categories")
                print("\n" + "=" * 60)
                print("SAVING SEPARATE FILES FOR EACH ARTICLE")
                print("=" * 60)

                total_lines = 0
                for article_category, lines in training_data.items():
                    # Create filename from article category
                    filename = f"{article_category}_wiki.txt"
                    filepath = os.path.join(WIKI_FOLDER, filename)

                    unique_lines = list(set(lines))
                    total_lines += len(unique_lines)

                    with open(filepath, 'w', encoding='utf-8') as f:
                        for line in unique_lines:
                            f.write(line + '\n')

                    print(f"✓ {article_category:40s} → {len(unique_lines):5d} lines")

                print("\n" + "=" * 60)
                print(f"✅ COMPLETE: Saved {len(training_data)} articles, {total_lines} total lines")
                print(f"📂 Location: {WIKI_FOLDER}/")
                print("=" * 60)
            else:
                print("❌ No training data generated")

            exit(0)

    print(f"\n📚 Extracting {len(ARTICLES)} Wikipedia articles...\n")
    
    if not ARTICLES:
        print("❌ ERROR: ARTICLES list is empty!")
        print("Please add Wikipedia articles to the ARTICLES list above.")
        exit(1)
    
    total_articles = len(ARTICLES)
    all_training_data = {}
    
    for idx, (emoji, title, category) in enumerate(ARTICLES, 1):
        print(f"\n[{idx}/{total_articles}] {emoji} {title}")
        print(f"  Category: {category}")
        print(f"  Fetching from Wikipedia...")
        
        try:
            # Fetch article
            content = fetch_wikipedia_article(title)
            
            if content:
                print(f"  ✓ Retrieved ({len(content)} chars)")
                
                # Extract training data
                training_data = extract_training_data(content, category)
                
                if training_data:
                    print(f"  ✓ Generated {len(training_data)} training lines")
                    
                    # Store by category (combine if multiple articles per category)
                    if category not in all_training_data:
                        all_training_data[category] = []
                    all_training_data[category].extend(training_data)
                else:
                    print(f"  ⚠️  No training data extracted")
            else:
                print(f"  ⚠️  Article not found")
                print(f"     (Check Wikipedia spelling: en.wikipedia.org)")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Save each category to its own file
    print(f"\n\n{'=' * 60}")
    print("SAVING TRAINING FILES")
    print("=" * 60)
    
    for category, training_data in all_training_data.items():
        filename = f"{category}_wiki.txt"
        save_training_file(training_data, filename)
    
    print(f"\n\n{'=' * 60}")
    print("✅ EXTRACTION COMPLETE!")
    print("=" * 60)
    print(f"\n📁 Generated {len(all_training_data)} training files")
    print(f"📂 Location: Wiki/ folder")
    print(f"📊 Total articles processed: {total_articles}")
    print("\n📋 Next steps:")
    print(f"   1. cp Wiki/*_wiki.txt training/")
    print(f"   2. ./chatbot")
    print("\n💡 To add more articles:")
    print("   1. Edit this script")
    print("   2. Add to ARTICLES list")
    print("   3. Run again: python3 extractor_wikipedia_flexible.py")
    print("\n📂 Your Wiki files are organized in: Wiki/")
    print("🚀 Your chatbot learns what you teach it!")