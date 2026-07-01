# Botasaurus Web Scraper for Killo

Advanced web scraping tools for collecting training data from websites.

Uses **Botasaurus** for reliable, efficient scraping with:
- Automatic retries
- Caching
- Rate limiting
- Respectful crawling

## Quick Start

```bash
# Scrape a single website
python3 scraper.py "https://example.com/article" category_name

# Scrape blog post
python3 blog_scraper.py "https://blog.example.com/my-article" ai

# Scrape with custom processing
python3 generic_scraper.py "https://example.com" tech
```

## Output

All scraped content goes to `training_data/` folder as:
- `category_name_scraped.txt`
- `category_name_blog.txt`
- etc.

**Format:** Ready for Killo! Each line is: `category: content`

## Usage with Killo

```bash
# 1. Scrape content
python3 scraper.py "https://example.com" myopic

# 2. Copy to Killo training folder
cp training_data/* ../../training/

# 3. Recompile Killo
cd ../.. && g++ -std=c++17 -O2 Killo.cpp -o Killo

# 4. Run with new training data
./Killo
```

## Advanced

### Blog Scraper
```bash
python3 blog_scraper.py "https://medium.com/article" ai
```

### Generic Scraper
```bash
python3 generic_scraper.py "https://docs.example.com" documentation
```

## Requirements

- Python 3.7+
- Botasaurus
- BeautifulSoup4
- Requests

Install: `pip install -r requirements.txt`

## Tips

1. **Respect robots.txt** - Botasaurus handles this automatically
2. **Test first** - Try scraping once before bulk operations
3. **Clean output** - Review generated files before using in training
4. **Combine sources** - Mix Wikipedia (wiki.py) + web scraped (botasaurus) data

## Example Workflow

```bash
# Get ML articles from Wikipedia
cd ../../
python3 wiki.py -l articles.txt

# Get ML blog posts from web
cd scrapers/botasaurus_scraper
python3 blog_scraper.py "https://example-ml-blog.com/posts" ml

# Copy all to training
cp training_data/* ../../training/

# Retrain Killo
cd ../.. && g++ -std=c++17 -O2 Killo.cpp -o Killo && ./Killo
```

Happy scraping! 🕷️
