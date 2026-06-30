# Byte AI - Knowledge Bot

**By: RetroGigabyte**

A high-performance knowledge bot built in C++ with Python integration, featuring multi-threaded recursive data loading, Wikipedia article extraction, and intelligent query matching.

## Features

### Core Capabilities
- ✅ **Multi-threaded Loading** - 4 parallel threads load 4,500+ training lines in 0.7 seconds
- ✅ **Recursive Zip Extraction** - Automatically extracts and loads compressed training data
- ✅ **Wikipedia Integration** - Recursive article downloading with linked article following
- ✅ **Real-time Time/Date** - NTP-synchronized current time and date queries
- ✅ **Training Collection** - Interactive Q&A pair collection with Groq AI enhancement
- ✅ **Auto-Training Pipeline** - Automatic processing and compilation of new training data
- ✅ **Category Matching** - Intelligent query-to-category classification
- ✅ **Query History** - Tracks recent queries for context

### Knowledge Base
- 1,200+ Wikipedia articles indexed
- 4,500+ training sentences
- 781+ dictionary definitions
- 30+ news articles
- 9+ pet-related Q&A pairs
- 50+ knowledge categories

## Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/RetroGigabyte/Byte_AI.git
cd Byte_AI
```

### 2. Install Dependencies
```bash
pip install -r url_lists/requirements.txt
```

### 3. Compile
```bash
g++ -std=c++17 knowledge_bot.cpp -o knowledge_bot
```

### 4. Run
```bash
./knowledge_bot
```

## Usage Examples

### Chat with Byte
```
You: What is machine learning?
Byte [ai]: Machine learning is a subset of artificial intelligence...

You: Tell me about dogs
Byte [pets]: Labrador Retrievers are one of the most popular dog breeds...

You: What time is it?
Byte [time]: Current time: Monday, June 30, 2026 at 10:40 AM
```

### Train Byte (Simple Workflow)
```bash
# 1. Collect Q&A pairs (interactive)
python3 training_mode.py interactive

# 2. Run bot - it auto-loads all training data!
./Byte
```

**That's it!** The bot automatically:
- Loads all .txt files from `training/`
- Extracts and reads from .zip files
- Finds and indexes all training data
- Applies multi-threaded recursive loading

### Advanced: Download Wikipedia Articles
```bash
# Download Machine Learning + linked articles recursively
python3 url.py --urls url/url_lists/url.txt --recursive

# Or Wikipedia
python3 wiki.py -r "Machine learning" ai 2

# Bot auto-loads on next run - no compilation needed!
./Byte
```

### Optional: Use Groq AI for Better Answers
```bash
# During training, select "Generate with Groq"
python3 training_mode.py interactive
# Choose option 2 to have Groq generate better answers
```

## Architecture

### Three-Layer System
```
┌─────────────────────────────────┐
│     Interface Layer             │
│  CLI | Time Queries | Training  │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│     Knowledge Layer             │
│  Category Matching              │
│  Query Classification           │
│  Response Retrieval             │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│     Training Layer              │
│  Multi-threaded Loading         │
│  Recursive Zip Extraction       │
│  Wikipedia Integration          │
└─────────────────────────────────┘
```

### Key Files
- `Byte.cpp` - Main C++ bot engine (600+ lines)
- `Byte` - Compiled executable (398 KB)
- `training_mode.py` - Interactive Q&A collection (with Groq support)
- `wiki.py` - Wikipedia article extraction (recursive)
- `url/` - URL extraction tools (news, webpages, recursive crawling)
- `groq_enhancer.py` - Groq API integration (optional)

## Training Data

### Included Categories
- **ai** (3,038 sentences) - Machine Learning, AI, Neural Networks
- **pets** (1,345 sentences) - Dogs, Cats, Pet Care
- **war** (history sentences) - World War 1, Military History
- **news** (30+ articles) - Technology, Science, Business News
- **dictionary** (781+ words) - Webster's 1828 Dictionary

### Add Your Own Training
```bash
# Option 1: Use interactive training (easiest)
python3 training_mode.py interactive
# Bot auto-loads on next run!

# Option 2: Create manual training file
training/my_category.txt

# Format: category: sentence
# Example:
# cooking: Preheat oven to 350 degrees
# cooking: Add flour and sugar to bowl

# Just run bot - it auto-loads everything!
./Byte
```

**No compilation or special scripts needed!** The bot automatically:
- Scans `training/` directory
- Loads all `.txt` files
- Extracts and reads from `.zip` files
- Uses multi-threaded loading for speed


## Advanced Features

### Recursive Wikipedia Download
```bash
# Download topic + all linked articles (depth 2)
python3 wiki.py -r "Artificial Intelligence" ai 2

# Deeper recursion (depth 3)
python3 wiki.py -r "Python (programming language)" python 3
```

### Batch URL Extraction
```bash
cd extractors
bash batch_extract.sh
```

### Optional: Schedule Auto-Training
For automated daily backups and recompilation (optional):
```bash
# Auto-train & backup every 24 hours
python3 auto_train.py schedule 24
```

**Note:** This is optional! The bot auto-loads training data on startup regardless.

## Performance

- **Startup Time**: 0.7 seconds
- **Threading**: 4 parallel loaders
- **Training Lines Loaded**: 4,500+
- **Categories**: 50+
- **Response Time**: Instant matching

## System Requirements

- C++17 compiler (g++)
- Python 3.7+
- 200 MB disk space (with all training data)
- Internet connection (for Wikipedia/News extraction)

## License

MIT License - Copyright (c) 2024 RetroGigabyte

See LICENSE file for details.

## Architecture Credits

**Built by:** RetroGigabyte  
**AI Architecture & Implementation:** Claude AI (Claude 3.5 Sonnet)  
**Training Data:** Wikipedia, News APIs, User-Contributed Q&A

## Contributing

To contribute improvements to Byte:

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## Contact

- **GitHub**: https://github.com/RetroGigabyte/Byte_AI
- **Email**: retrogigabyteyt@gmail.com

---

**Happy chatting with Byte! 🤖**
