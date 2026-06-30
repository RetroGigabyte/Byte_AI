# Quick Start Guide - Organized Structure

## 📁 Folder Organization

```
chatbot/
├── extractors/      - All extraction tools
├── url_lists/       - URL files for extraction
├── training/        - Training data files
├── docs/            - Documentation
└── knowledge_bot    - Main executable
```

---

## 🚀 Quick Start (2 minutes)

### Option 1: Run with Pre-loaded News Data

```bash
# Bot already has news data loaded!
./knowledge_bot

# Query:
# "What's the latest news?"
# "Tell me about technology"
```

### Option 2: Extract More News

```bash
# Go to extractors folder
cd extractors

# Extract from news URLs (with recursive crawling)
python3 url.py --urls ../url_lists/url.txt --recursive

# Go back and run bot
cd ..
./knowledge_bot
```

---

## 📚 How to Use Each Extractor

### Extract from Wikipedia

```bash
cd extractors
python3 wiki.py "Artificial Intelligence"
python3 wiki.py "Machine Learning"
python3 wiki.py "Climate Change"
```

### Extract from PDF

```bash
cd extractors
python3 pdf.py ../mybook.pdf
python3 pdf.py ../mybook.pdf --category history
```

### Extract from Websites

```bash
cd extractors

# Single URL
python3 url.py https://techcrunch.com

# From URL file (recursive)
python3 url.py --urls ../url_lists/url.txt --recursive

# Custom settings
python3 url.py --urls ../url_lists/url.txt \
  --method paragraphs \
  --max-lines 100 \
  --recursive
```

### Batch Extract Multiple URLs

```bash
cd extractors
bash batch_extract.sh
```

---

## 📋 URL Files

Location: `url_lists/`

### url.txt
Ready-to-use file with 10+ news sources:
- Technology news (TechCrunch, Verge, ArsTechnica)
- Science news (ScienceDaily)
- Business news (CNBC)
- World news (BBC, AP, Guardian)

### example_urls.txt
Example Wikipedia URLs for testing

### Add Your Own

```bash
# Edit and add more URLs
nano url_lists/url.txt

# Or append
echo "https://example.com/article" >> url_lists/url.txt
```

---

## 🎯 Extraction Workflows

### Workflow 1: News Bot Setup

```bash
# Extract news with recursion
cd extractors
python3 url.py --urls ../url_lists/url.txt --recursive

# Load bot
cd ..
./knowledge_bot

# Query: "What's the latest news?"
```

### Workflow 2: Knowledge Base

```bash
# Extract Wikipedia articles
cd extractors
python3 wiki.py "Artificial Intelligence"
python3 wiki.py "Machine Learning"
python3 wiki.py "Deep Learning"

# Load bot
cd ..
./knowledge_bot

# Query: "What is AI?"
```

### Workflow 3: Book Learning

```bash
# Extract from PDF
cd extractors
python3 pdf.py ../research_paper.pdf --category research

# Load bot
cd ..
./knowledge_bot

# Query: "What does this paper say about..."
```

### Workflow 4: Mixed Sources

```bash
# Extract from everything
cd extractors

# Wikipedia
python3 wiki.py "Topic1"

# PDF
python3 pdf.py ../book.pdf

# News
python3 url.py --urls ../url_lists/url.txt --recursive

# Load combined
cd ..
./knowledge_bot

# Query about all topics
```

---

## 📖 Documentation

Location: `docs/`

View documentation for specific topics:

```bash
# Batch extraction guide
cat docs/BATCH_EXTRACTION.md

# Training folder structure
cat docs/TRAINING_FOLDER_STRUCTURE.md

# NTP time features
cat docs/NTP_TIME_GUIDE.md

# And more...
ls -la docs/
```

---

## 🔧 Common Tasks

### Add News URLs

```bash
echo "https://techcrunch.com/category/security/" >> url_lists/url.txt
echo "https://www.hackernews.com" >> url_lists/url.txt
```

### Extract from Custom URL List

```bash
# Create new list
nano url_lists/my_urls.txt

# Extract
cd extractors
python3 url.py --urls ../url_lists/my_urls.txt
```

### Check Training Data

```bash
# List all training files
ls -la training/

# See what's been loaded
wc -l training/*.txt

# Find specific topic
grep -l "machine learning" training/*.txt
```

### Recompile Bot

```bash
g++ -std=c++17 knowledge_bot.cpp -o knowledge_bot
```

---

## 💡 Tips

### Tip 1: Edit URL lists directly

```bash
# Edit in text editor
nano url_lists/url.txt
```

### Tip 2: Organize by topic

```bash
# Create separate lists
nano url_lists/tech_news.txt
nano url_lists/science_news.txt
nano url_lists/business_news.txt
```

### Tip 3: Use recursion for comprehensive extraction

```bash
# Get main site + all linked pages
python3 extractors/url.py --urls url_lists/url.txt --recursive
```

### Tip 4: Limit output for testing

```bash
# Quick test with only 10 lines per URL
python3 extractors/url.py --urls url_lists/url.txt --max-lines 10
```

---

## 🚀 One-Line Commands

```bash
# Extract news and run bot
cd extractors && python3 url.py --urls ../url_lists/url.txt --recursive && cd .. && ./knowledge_bot

# Extract Wikipedia and run
cd extractors && python3 wiki.py "Topic" && cd .. && ./knowledge_bot

# Extract PDF and run
cd extractors && python3 pdf.py ../book.pdf && cd .. && ./knowledge_bot
```

---

## ✨ Your Bot Has

- ✅ 1200+ Wikipedia articles available
- ✅ 781+ dictionary words
- ✅ 30+ news pages extracted
- ✅ Time/date features
- ✅ Holiday tracking
- ✅ Query history
- ✅ Business day calculations

---

## 📞 Quick Help

```bash
# See extractor options
python3 extractors/url.py --help
python3 extractors/wiki.py --help
python3 extractors/pdf.py --help

# See bot info
cat CLAUDE.md

# See documentation
ls docs/
```

---

## 🎉 You're Ready!

Everything is organized and ready to use. Pick a workflow above and start building your knowledge base!

Questions? Check the docs/ folder for detailed guides.
