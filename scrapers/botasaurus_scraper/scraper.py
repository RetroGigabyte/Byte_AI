#!/usr/bin/env python3
"""
Botasaurus Web Scraper - Main Interface
Flexible web scraping for training data collection
"""

import sys
import os
from generic_scraper import scrape_website, save_training_data

def main():
    if len(sys.argv) < 2:
        print("\n" + "=" * 60)
        print("BOTASAURUS WEB SCRAPER FOR KILLO TRAINING")
        print("=" * 60)
        print("\nUsage:")
        print("  python3 scraper.py <url> <category> [--save]")
        print("\nExamples:")
        print("  python3 scraper.py 'https://example.com' tech")
        print("  python3 scraper.py 'https://blog.example.com/article' ai --save")
        print("\nOutput:")
        print("  Creates training_data/ folder with category_scraped.txt files")
        print("  Ready to copy to Killo training/ folder!")
        print("\n" + "=" * 60)
        sys.exit(1)
    
    url = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else "scraped"
    
    print("\n" + "=" * 60)
    print("BOTASAURUS SCRAPER")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Category: {category}\n")
    
    training_data = scrape_website(url, category)
    
    if training_data:
        save_training_data(training_data, category)
        print("\n✅ Scraping complete!")
        print("📂 Files saved to: training_data/")
        print("\nNext steps:")
        print("  1. Review the generated file")
        print("  2. Copy to Killo: cp training_data/* ../../training/")
        print("  3. Recompile Killo: cd ../.. && g++ -std=c++17 -O2 Killo.cpp -o Killo")
    else:
        print("\n❌ No data scraped")

if __name__ == "__main__":
    main()
