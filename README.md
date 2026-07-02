# Killo 2.75 DAT - Knowledge Bot with Dynamic Automatic Training

![Version](https://img.shields.io/badge/version-2.75-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.6%2B-blue) ![C++](https://img.shields.io/badge/C%2B%2B-17-blue)

**Killo** is an intelligent knowledge bot powered by:
- 🧠 **C++ engine** with 2.8M training lines across 1000+ Wikipedia articles
- 🔄 **Dynamic Automatic Training (DAT)** - auto-learns from Wikipedia when needed
- 🧮 **Math evaluation** - instant calculation support
- ⚡ **Hardcoded responses** - fast answers for common queries
- 💾 **Smart caching** - persistent knowledge learning

## Quick Start

```bash
# Install dependencies
pip install requests

# Extract and compile
unzip Killo_2.75_DAT.zip
cd chatbot
g++ -std=c++17 -O2 Killo.cpp -o Killo

# Run interactive chat
python3 Killo_2.75_DAT.py

# Or ask single questions
python3 Killo_2.75_DAT.py "What is machine learning?"
```

## Features

### 🧠 Three-Tier Intelligence System

**1. Hardcoded Responses (< 1ms)**
- Greetings: "hello", "hi", "hey"
- Time/Date: "what time is it", "what date is it"  
- Math: "2+3", "what is 10 divided by 2"
- Help: "who are you", "how can you help"

**2. Killo C++ Training (10-100ms)**
- 1000+ Wikipedia articles as training data
- 2.8M training lines
- Conversation memory
- Smart pattern matching

**3. DAT Wikipedia (1-3 seconds)**
- Auto-searches Wikipedia for unknown topics
- Extracts 5 key sentences
- Caches learning for future queries
- Never forgets what it learns

### 🧮 Math Engine

```bash
# Direct expressions
./Killo "2+3"              # 5
./Killo "2^10"             # 1024
./Killo "(2+3)*4"          # 20
./Killo "sqrt(16)"         # 4.0

# Word-based
./Killo "what is 5 plus 3"        # 8
./Killo "calculate 100 / 5"       # 20
./Killo "what is sqrt(16)"        # 4.0
./Killo "what is pi"              # 3.14
```

Supported: `+ - * / % ^ sqrt() sin() cos() tan() pi e`

### 📚 Knowledge Base

**4,726 curated Wikipedia articles** across 12 domains:

| Domain | Count | Examples |
|--------|-------|----------|
| Technology & Computing | 150+ | AI, ML, Python, Blockchain, Cloud |
| Science | 250+ | Physics, Chemistry, Biology, Astronomy |
| History | 200+ | Ancient Egypt, WWI, WWII, Cold War |
| Geography | 150+ | Countries, Continents, Mountains, Rivers |
| Business & Economics | 100+ | Markets, Banking, Crypto, Investing |
| Culture & Society | 200+ | Art, Music, Literature, Philosophy |
| Sports | 100+ | Football, Basketball, Olympics, Tennis |
| Health & Medicine | 150+ | Diseases, Treatments, Anatomy, Nutrition |
| Nature & Wildlife | 100+ | Animals, Plants, Ecology, Conservation |
| Education | 150+ | Schools, Universities, Learning Methods |
| Law & Government | 200+ | Democracy, Laws, Politics, Systems |
| Energy & Transportation | 150+ | Oil, Solar, Trains, Planes, Ships |

## Architecture

```
┌─────────────────────┐
│   User Input        │
└──────────┬──────────┘
           │
┌──────────▼──────────────────────────┐
│   Killo_2.75_DAT.py (Python)       │
│   ├─ Hardcoded Responses (instant)  │
│   ├─ Killo C++ (training data)      │
│   └─ DAT Wikipedia (auto-learn)     │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│   Response with Source & Cache      │
└─────────────────────────────────────┘
```

## Installation

### Requirements
- Python 3.6 or higher
- C++ compiler (g++, clang, or MSVC)
- `requests` library
- 500MB disk space

### Setup
```bash
# Clone or extract
git clone https://github.com/RetroGigabyte/Byte_AI.git -b killo-dev
cd chatbot

# Install Python dependencies
pip install -r requirements.txt  # or: pip install requests

# Compile C++ engine
g++ -std=c++17 -O2 Killo.cpp -o Killo

# Run
python3 Killo_2.75_DAT.py
```

## Usage

### Interactive Mode
```bash
python3 Killo_2.75_DAT.py
```

Examples:
```
You: hello
Killo: Hi there! How can I help you?

You: what time is it
Killo: It's 09:35 PM on Tuesday, July 01, 2025

You: 2+3
Killo: 5

You: what is quantum computing
Killo: [Answers from training data or Wikipedia]
```

### Single Query Mode
```bash
python3 Killo_2.75_DAT.py "your question here"
```

Examples:
```bash
python3 Killo_2.75_DAT.py "what is machine learning?"
python3 Killo_2.75_DAT.py "2^8"
python3 Killo_2.75_DAT.py "tell me about python programming"
```

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Hardcoded response | < 1ms | Instant answer |
| Killo C++ query | 10-100ms | From training data |
| DAT Wikipedia lookup | 1-3s | Auto-learn & cache |
| DAT cache hit | < 50ms | Cached knowledge |

## Rate Limiting

Killo smartly handles Wikipedia's rate limits:
- **2000+ rotating user agents** - distribute requests
- **0.5s base delay** - respectful pacing
- **Smart jitter** - avoid pattern detection
- **429 handling** - instant agent switch
- **Exponential backoff** - for repeated limits

## Extending Killo

### Add More Training Articles
```bash
# Create articles.txt with one article per line
echo "Quantum Physics" > my_articles.txt
echo "Machine Learning" >> my_articles.txt

# Download and train
python3 wiki.py -l my_articles.txt
cp Wiki/*.txt training/
python3 Killo_2.75_DAT.py  # Uses new training
```

### Add Custom Hardcoded Responses
Edit `Killo_2.75_DAT.py` and add to `self.simple_responses`:
```python
'custom query': "Your custom answer"
```

## File Structure

```
Killo_2.75_DAT/
├── Killo_2.75_DAT.py          # Main Python wrapper
├── Killo.cpp                  # C++ engine source
├── Killo                       # Compiled binary
├── user_agent_rotator.py       # User agent system
├── web_agents.txt              # 500 user agents
├── articles.txt                # 4,726 article list
├── wiki.py                     # Wikipedia scraper
├── training/                   # Knowledge base
│   ├── extracted_zips/         # 1000+ .txt files
│   ├── dat_cache.json          # Learned knowledge
│   └── Wikipedia_Batch_1.zip   # Reference batch
├── README.md                   # This file
├── RELEASE_NOTES.md            # Detailed docs
├── LICENSE                     # MIT License
└── CLAUDE.md                   # Architecture docs
```

## How DAT Works

1. **User asks a question** that Killo doesn't have in training
2. **DAT activates** - searches Wikipedia for the topic
3. **Extracts key sentences** - picks 5 most relevant
4. **Caches the learning** - stores in `dat_cache.json`
5. **Returns the answer** - with Wikipedia attribution
6. **Remembers forever** - next time is instant!

## Performance Optimization Tips

- **Cache warming**: Run common queries once to pre-cache
- **Offline mode**: Disconnect internet to use training data only
- **Batch queries**: Run multiple queries to amortize startup time
- **Local compilation**: Compile on your machine for best performance

## Troubleshooting

### "Killo: command not found"
```bash
# Compile first
g++ -std=c++17 -O2 Killo.cpp -o Killo
```

### "requests module not found"
```bash
pip install requests
```

### "Wikipedia lookup is slow"
- Normal: 1-3 seconds first time, < 50ms cached
- Check internet connection
- Try a simpler query

### "Math gives wrong answer"
- Check operator precedence: `(2+3)*4` not `2+3*4`
- Use `^` or `**` for exponents
- Functions: `sqrt()`, `sin()`, `cos()`, `tan()`

## Development

### Update Training Data
```bash
python3 wiki.py -l articles.txt     # Download articles
cp Wiki/*.txt training/              # Add to training
```

### Add New Features
1. Edit `Killo_2.75_DAT.py`
2. Test locally
3. Commit and push to `killo-dev` branch
4. Create pull request

## Known Limitations

- DAT requires internet connection
- Wikipedia sometimes rate-limits (handled automatically)
- Math limited to standard operations
- Training data is static (expand by adding articles)

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contributors

- **Claude AI** (Anthropic) - Original Byte Bot architecture
- **RetroGigabyte** - Killo development & DAT feature
- **Claude Haiku 4.5** - Dynamic Automatic Training system

## Repository

**GitHub**: [RetroGigabyte/Byte_AI](https://github.com/RetroGigabyte/Byte_AI)  
**Branch**: `killo-dev`  
**Latest Version**: 2.75 DAT (July 2026)

## Support & Feedback

- **Issues**: Report on [GitHub Issues](https://github.com/RetroGigabyte/Byte_AI/issues)
- **Discussion**: Use [GitHub Discussions](https://github.com/RetroGigabyte/Byte_AI/discussions)
- **Contributing**: See [CLAUDE.md](CLAUDE.md) for architecture details

---

**Made with ❤️ by RetroGigabyte & Claude AI**

*"The future of AI is collaborative. Humans provide direction. AI provides implementation. Together, we create amazing things."*
