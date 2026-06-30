# Byte AI - Knowledge Bot

<div align="center">
  <img src="assets/Byte_AI.png" alt="Byte AI Logo" width="300">
  
  **By: RetroGigabyte**
</div>

Open-source AI bot framework - Killo (Byte 2.0):

**Killo** - LLM-like generative knowledge bot (current)
- Built in C++ with intelligent category matching
- 500,000+ training lines across 2,300+ categories
- Generates natural language responses from training data
- Multi-threaded loading, Wikipedia integration, NTP time functions
- Context-aware synthesis engine
- Conversational memory and pattern learning

## Features

### Killo Core Capabilities
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
g++ -std=c++17 Killo.cpp -o Killo
```

### 4. Run
```bash
./Killo
```

## Usage Examples

### Chat with Killo
```
You: What is machine learning?
Killo [ai]: Machine learning is a subset of artificial intelligence...

You: Tell me about dogs
Killo [pets]: Labrador Retrievers are one of the most popular dog breeds...

You: What time is it?
Killo [time]: Current time: Monday, June 30, 2026 at 10:40 AM
```

### Train Killo (Simple Workflow)
```bash
# 1. Collect Q&A pairs (interactive)
python3 training_mode.py interactive

# 2. it auto-loads all training data!
./Killo
```

**That's it!** The bot automatically:
- Loads all .txt files from `training/`
- Extracts and reads from .zip files
- Finds and indexes all training data
- Applies multi-threaded recursive loading

### Advanced: Download Wikipedia Articles
```bash
# Download Machine Learning + linked articles recursively
python3 wiki.py -r "Machine learning" ai 2

#Move all .txt(s) from "Wiki" folder to "training" folder

# Run Killo!
./Killo
```

### Optional: Use Groq AI for Better Answers
(API KEY IS NEEDED)
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
- `Killo.cpp` - Main C++ bot engine (800+ lines)
- `Killo` - Compiled executable
- `training_mode.py` - Interactive Q&A collection (with Groq support)
- `wiki.py` - Wikipedia article extraction (recursive)
- `url.py` - URL extraction tool (recursive crawling)
- `groq_enhancer.py` - Groq API integration (optional)

## Training Data

### Included Categories
- **2,300+** total categories across domains
- **500,000+** training lines (from Wikipedia, news, user data)
- Including: AI, pets, history, news, dictionary, and more

### Add Your Own Training
```bash
# Option 1: Use interactive training (easiest)
python3 training_mode.py interactive

# Option 2: Create manual training file
training/my_category.txt

# Format: category: sentence
# Example:
# cooking: Preheat oven to 350 degrees
# cooking: Add flour and sugar to bowl

# Compile and run - bot auto-loads everything!
g++ -std=c++17 Killo.cpp -o Killo
./Killo
```

**The bot automatically:**
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

- **Startup Time**: < 2 seconds (with 500K training lines)
- **Threading**: 4 parallel loaders
- **Training Lines Loaded**: 500,000+
- **Categories**: 2,300+
- **Response Time**: Instant synthesis

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

**Happy chatting with Killo! 🤖**
