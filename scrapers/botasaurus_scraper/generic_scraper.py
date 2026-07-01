#!/usr/bin/env python3
"""
Generic website scraper using Botasaurus
Scrapes text content from any website and formats for Killo training
"""

import sys
import os
from botasaurus import *
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def clean_text(text):
    """Clean and normalize text"""
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def scrape_website(url, category):
    """Scrape a single website"""
    print(f"📥 Scraping: {url}")
    
    try:
        # Use Botasaurus to fetch
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        
        if not paragraphs:
            print("  ⚠️  No content found")
            return []
        
        training_lines = []
        for p in paragraphs:
            text = clean_text(p.get_text())
            if len(text) > 30 and len(text) < 500:
                training_lines.append(f"{category}: {text}")
        
        print(f"  ✓ Extracted {len(training_lines)} lines")
        return training_lines
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def save_training_data(training_data, category):
    """Save training data to file"""
    os.makedirs("training_data", exist_ok=True)
    
    filename = f"training_data/{category}_scraped.txt"
    unique_lines = list(set(training_data))
    
    with open(filename, 'w', encoding='utf-8') as f:
        for line in unique_lines:
            f.write(line + '\n')
    
    print(f"✓ Saved {len(unique_lines)} unique lines to {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 generic_scraper.py <url> <category>")
        print("Example: python3 generic_scraper.py 'https://example.com' example")
        sys.exit(1)
    
    url = sys.argv[1]
    category = sys.argv[2]
    
    print("=" * 60)
    print("GENERIC WEBSITE SCRAPER (Botasaurus)")
    print("=" * 60)
    
    training_data = scrape_website(url, category)
    
    if training_data:
        save_training_data(training_data, category)
    else:
        print("❌ No data scraped")
