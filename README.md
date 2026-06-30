# Byte AI - Knowledge Bot

<div align="center">
  <img src="assets/Byte_AI.png" alt="Byte AI Logo" width="300">
  
  **By: RetroGigabyte**
</div>

Open-source AI bot framework with two generations:

**Byte 1.0** - High-performance retrieval-based knowledge bot (current)
- Built in C++ with intelligent category matching
- 4,500+ training sentences across 50+ categories
- Multi-threaded loading, Wikipedia integration, NTP time functions
- Lightning fast responses from training data
- There are some bugs...

**Byte 2.0/Killo** - LLM-like generative bot (coming soon)
- Generates natural language responses
- Learns from training data patterns
- More conversational and contextual
- Template-based synthesis engine

## Versions

### Byte 1.0 (Current)
Fast retrieval-based bot with intelligent category matching. Perfect for:
- Quick knowledge lookup
- Instant responses
- Precise category classification
- Lightweight deployment

### Byte 2.0/Killo (In Development)
LLM-like generative bot that synthesizes responses. Better for:
- Natural conversation
- Multi-sentence answers
- Context-aware generation
- More human-like interactions

## Features

### Byte 1.0 Core Capabilities
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

**100% Open Source** - MIT License

Copyright (c) 2026 RetroGigabyte

This project is completely free to use, modify, and distribute. You are free to:
- ✅ Use the code for any purpose (commercial or personal)
- ✅ Modify and distribute the code
- ✅ Use it in your own projects
- ✅ Fork and build your own version
- ✅ Rename, rebrand, and customize everything

See [LICENSE](LICENSE) file for details.

**Fork-based model:** This repository accepts no pull requests. Fork it and build your own version instead!

## Architecture Credits

**Built by:** RetroGigabyte  
**AI Architecture & Implementation:** Claude AI (Claude 3.5 Sonnet)  
**Training Data:** Wikipedia, News APIs, User-Contributed Q&A

## Customizing & Forking

Byte AI is **100% open source**! This repository is the base version, but we encourage you to **fork it and build your own version**.

**No pull requests** — this keeps the main project focused. Instead:

1. **Fork** the repository on GitHub
2. **Clone** your fork and make it your own
3. **Customize** everything: features, behavior, training data, branding
4. **Publish** your fork and share what you built!

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to fork and customize
- Ideas for your own version
- How to share your fork
- MIT License freedom

## Contact

- **GitHub**: https://github.com/RetroGigabyte/Byte_AI
- **Email**: retrogigabyteyt@gmail.com

---

**Happy chatting with Byte! 🤖**
