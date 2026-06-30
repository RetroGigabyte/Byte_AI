#!/usr/bin/env python3
"""
URL Training Data Extractor
Extracts text from webpages and converts to training format
"""

import os
import sys
import re
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("⚠️  requests not installed. Install with: pip install requests")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("⚠️  beautifulsoup4 not installed. Install with: pip install beautifulsoup4")
    sys.exit(1)


class URLExtractor:
    """Extract training data from URLs"""

    def __init__(self, output_dir='training', timeout=10):
        self.output_dir = output_dir
        self.timeout = timeout
        self.session = self._create_session()

    def _create_session(self):
        """Create a requests session with retry strategy"""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=(500, 502, 504)
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        # Set user agent
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        return session

    def fetch_url(self, url: str) -> Optional[str]:
        """Fetch content from a URL"""
        try:
            print(f"   🌐 Fetching {url}...")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            print(f"   ✓ Status: {response.status_code}")
            return response.text
        except requests.RequestException as e:
            print(f"   ❌ Error fetching URL: {e}")
            return None

    def extract_text_from_html(self, html: str) -> str:
        """Extract clean text from HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            return text
        except Exception as e:
            print(f"   ❌ Error parsing HTML: {e}")
            return ""

    def extract_metadata(self, html: str) -> Dict:
        """Extract metadata from HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')

            metadata = {
                'title': '',
                'description': '',
                'keywords': []
            }

            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                metadata['title'] = title_tag.get_text()

            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                metadata['description'] = meta_desc.get('content', '')

            # Extract keywords
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords:
                keywords = meta_keywords.get('content', '').split(',')
                metadata['keywords'] = [k.strip() for k in keywords]

            return metadata
        except Exception as e:
            print(f"   ⚠️  Could not extract metadata: {e}")
            return {}

    def extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract all links from HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            links = []

            for link in soup.find_all('a', href=True):
                url = link['href']
                # Convert relative URLs to absolute
                absolute_url = urljoin(base_url, url)
                # Filter out anchors and external links
                if absolute_url.startswith('http') and urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                    links.append(absolute_url)

            return list(set(links))  # Remove duplicates
        except Exception as e:
            print(f"   ⚠️  Could not extract links: {e}")
            return []

    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return sentences

    def split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        paragraphs = text.split('\n')
        paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 20]
        return paragraphs

    def extract_category_from_url(self, url: str) -> str:
        """Extract category from URL"""
        # Parse URL
        parsed = urlparse(url)
        # Get domain and path
        domain = parsed.netloc.replace('www.', '')
        path = parsed.path.strip('/').split('/')[0]

        # Combine domain and path
        if path:
            category = f"{domain.split('.')[0]}_{path}"
        else:
            category = domain.split('.')[0]

        # Clean up
        category = category.lower().replace(' ', '_').replace('-', '_')
        category = re.sub(r'[^a-z0-9_]', '', category)

        return category

    def create_training_format(self, text: str, category: str, method: str = 'sentences', max_lines: int = 100) -> List[str]:
        """Convert text to training format"""
        print(f"   🔄 Converting to training format ({method})...")

        lines = []

        if method == 'sentences':
            segments = self.split_into_sentences(text)
        elif method == 'paragraphs':
            segments = self.split_into_paragraphs(text)
        else:
            segments = [text]

        # Limit to avoid huge files
        segments = segments[:max_lines]

        # Create training lines
        for segment in segments:
            if len(segment.strip()) > 10:
                line = f"{category}: {segment}"
                lines.append(line)

        return lines

    def process_url(self, url: str, category: Optional[str] = None, method: str = 'sentences', max_lines: int = 100) -> Optional[Dict]:
        """Process a single URL"""
        print(f"\n📖 Processing: {url}")

        # Fetch content
        html = self.fetch_url(url)
        if not html:
            return None

        # Extract text
        print(f"   📝 Extracting text...")
        text = self.extract_text_from_html(html)

        if not text:
            print(f"   ❌ No text extracted")
            return None

        print(f"   ✓ Extracted {len(text)} characters")

        # Extract metadata
        metadata = self.extract_metadata(html)
        if metadata['title']:
            print(f"   📄 Title: {metadata['title']}")

        # Get category
        if not category:
            category = self.extract_category_from_url(url)

        print(f"   📂 Category: {category}")

        # Convert to training format
        lines = self.create_training_format(text, category, method, max_lines)

        if not lines:
            print(f"   ❌ No training lines created")
            return None

        print(f"   ✓ Created {len(lines)} training lines")

        # Save to file
        output_file = os.path.join(self.output_dir, f"{category}_url.txt")

        print(f"   💾 Saving to {output_file}...")

        os.makedirs(self.output_dir, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')

        print(f"   ✅ Saved {len(lines)} lines")

        return {
            'url': url,
            'file': output_file,
            'category': category,
            'lines': len(lines),
            'characters': len(text),
            'title': metadata.get('title', ''),
            'links_found': len(self.extract_links(html, url))
        }

    def process_urls(self, urls: List[str], method: str = 'sentences', max_lines: int = 100, recursive: bool = False, depth: int = 1) -> List[Dict]:
        """Process multiple URLs"""
        results = []
        processed_urls = set()

        for url in urls:
            result = self.process_url(url, method=method, max_lines=max_lines)
            if result:
                results.append(result)
                processed_urls.add(url)

            # Recursive crawling
            if recursive and depth > 0:
                print(f"\n🔗 Following links from {url}...")
                html = self.fetch_url(url)
                if html:
                    links = self.extract_links(html, url)
                    # Limit links to avoid infinite crawling
                    links = [l for l in links if l not in processed_urls][:5]

                    for link in links:
                        if link not in processed_urls:
                            print(f"  → Found: {link}")
                            result = self.process_url(link, method=method, max_lines=max_lines)
                            if result:
                                results.append(result)
                                processed_urls.add(link)

        return results

    def process_sitemap(self, sitemap_url: str, method: str = 'sentences', max_lines: int = 100, limit: int = 10) -> List[Dict]:
        """Process URLs from a sitemap"""
        print(f"\n📍 Processing sitemap: {sitemap_url}")

        html = self.fetch_url(sitemap_url)
        if not html:
            return []

        # Extract URLs from sitemap
        soup = BeautifulSoup(html, 'html.parser')
        urls = []

        # Try to find all loc tags (XML sitemap)
        for loc in soup.find_all('loc'):
            url = loc.get_text().strip()
            if url.startswith('http'):
                urls.append(url)

        # Limit URLs
        urls = urls[:limit]

        if not urls:
            print(f"   ❌ No URLs found in sitemap")
            return []

        print(f"   ✓ Found {len(urls)} URLs (processing {min(limit, len(urls))})")

        return self.process_urls(urls, method, max_lines)


def main():
    """Main entry point"""
    # Parse options first to check for --urls, --sitemap
    category = None
    method = 'sentences'
    output_dir = 'training'
    urls_file = None
    sitemap_url = None
    max_lines = 100
    url = None
    recursive = False
    depth = 1

    # First pass: look for --urls or --sitemap
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '--urls' and i + 1 < len(sys.argv):
            urls_file = sys.argv[i + 1]
        elif sys.argv[i] == '--sitemap' and i + 1 < len(sys.argv):
            sitemap_url = sys.argv[i + 1]
        elif sys.argv[i] == '--category' and i + 1 < len(sys.argv):
            category = sys.argv[i + 1]
        elif sys.argv[i] == '--method' and i + 1 < len(sys.argv):
            method = sys.argv[i + 1]
        elif sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
        elif sys.argv[i] == '--max-lines' and i + 1 < len(sys.argv):
            max_lines = int(sys.argv[i + 1])
        elif sys.argv[i] == '--recursive':
            recursive = True
        elif sys.argv[i] == '--depth' and i + 1 < len(sys.argv):
            depth = int(sys.argv[i + 1])
        elif not sys.argv[i].startswith('--') and url is None and i > 0:
            # First non-flag argument is the URL
            if not sys.argv[i-1].startswith('--'):
                url = sys.argv[i]

    # If no options provided, show help
    if len(sys.argv) < 2:
        print("Usage: python3 url.py <url> [options]")
        print("\nOptions:")
        print("  --category <name>   Override category name")
        print("  --method <type>     sentences|paragraphs|full (default: sentences)")
        print("  --output <dir>      Output directory (default: training)")
        print("  --urls <file>       Process URLs from a file (one per line)")
        print("  --sitemap <url>     Process URLs from a sitemap")
        print("  --max-lines <num>   Max lines per URL (default: 100)")
        print("  --recursive         Follow links and extract from all found pages")
        print("  --depth <num>       Recursion depth (default: 1)")
        print("\nExamples:")
        print("  python3 url.py https://example.com/article")
        print("  python3 url.py https://example.com --category technology")
        print("  python3 url.py --urls urls.txt --method paragraphs")
        print("  python3 url.py --urls urls.txt --recursive")
        print("  python3 url.py https://techcrunch.com --recursive --depth 2")
        print("  python3 url.py --sitemap https://example.com/sitemap.xml --max-lines 50")
        return

    # Create extractor
    extractor = URLExtractor(output_dir)

    print(f"\n{'='*60}")
    print(f"🌐 URL Training Data Extractor")
    print(f"{'='*60}\n")

    results = []

    # Process based on input
    if sitemap_url:
        results = extractor.process_sitemap(sitemap_url, method, max_lines)
    elif urls_file:
        # Read URLs from file
        try:
            with open(urls_file, 'r') as f:
                # Skip comment lines and empty lines
                urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
            if not urls:
                print(f"❌ No URLs found in {urls_file}")
                return
            print(f"📋 Found {len(urls)} URLs in {urls_file}\n")
            if recursive:
                print(f"🔄 Recursive mode enabled (depth: {depth})\n")
            results = extractor.process_urls(urls, method, max_lines, recursive=recursive, depth=depth)
        except FileNotFoundError:
            print(f"❌ File not found: {urls_file}")
            return
    elif url:
        # Process single URL
        if recursive:
            print(f"🔄 Recursive mode enabled (depth: {depth})\n")
            result = extractor.process_url(url, category, method, max_lines)
            if result:
                results = [result]
                # Follow links if recursive
                html = extractor.fetch_url(url)
                if html:
                    links = extractor.extract_links(html, url)
                    links = links[:5]  # Limit to 5 links
                    for link in links:
                        link_result = extractor.process_url(link, method=method, max_lines=max_lines)
                        if link_result:
                            results.append(link_result)
        else:
            result = extractor.process_url(url, category, method, max_lines)
            if result:
                results = [result]
    else:
        print("❌ Please provide a URL, --urls file, or --sitemap")
        return

    # Print summary
    if results:
        print(f"\n{'='*60}")
        print(f"✅ Processing Complete!")
        print(f"{'='*60}\n")

        total_lines = sum(r['lines'] for r in results)
        total_chars = sum(r['characters'] for r in results)

        print("📊 Summary:")
        for result in results:
            print(f"  ✓ {result['file']}")
            print(f"    URL: {result['url']}")
            if result['title']:
                print(f"    Title: {result['title']}")
            print(f"    Lines: {result['lines']:,}")
            print(f"    Size: {result['characters']:,} chars")

        print(f"\n📈 Totals:")
        print(f"  URLs: {len(results)}")
        print(f"  Lines: {total_lines:,}")
        print(f"  Characters: {total_chars:,}")
        print(f"  Output: {output_dir}/")

        print(f"\n🚀 Next step: Run './knowledge_bot' to load training data!")
    else:
        print(f"❌ No content processed")


if __name__ == '__main__':
    main()
