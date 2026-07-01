#!/usr/bin/env python3
"""
Blog/article scraper using Botasaurus
Scrapes technical blogs and medium articles
"""

import sys
import os
from bs4 import BeautifulSoup
import requests

def scrape_blog(url, category):
    """Scrape blog article"""
    print(f"📰 Scraping blog: {url}")
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; BlogScraper/1.0)'
        })
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract article content
        article = soup.find('article') or soup.find('main') or soup.body
        
        if not article:
            print("  ⚠️  No article found")
            return []
        
        # Get all paragraphs
        paragraphs = article.find_all('p')
        
        training_lines = []
        for p in paragraphs:
            text = ' '.join(p.get_text().split())
            if 40 < len(text) < 500:  # Reasonable sentence length
                training_lines.append(f"{category}: {text}")
        
        print(f"  ✓ Extracted {len(training_lines)} lines")
        return training_lines
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def save_training(data, category):
    os.makedirs("training_data", exist_ok=True)
    filename = f"training_data/{category}_blog.txt"
    unique = list(set(data))
    
    with open(filename, 'w', encoding='utf-8') as f:
        for line in unique:
            f.write(line + '\n')
    
    print(f"✓ Saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 blog_scraper.py <url> <category>")
        print("Example: python3 blog_scraper.py 'https://example.com/article' ai")
        sys.exit(1)
    
    url = sys.argv[1]
    category = sys.argv[2]
    
    print("=" * 60)
    print("BLOG SCRAPER (Botasaurus)")
    print("=" * 60)
    
    data = scrape_blog(url, category)
    if data:
        save_training(data, category)
    else:
        print("❌ No content scraped")
