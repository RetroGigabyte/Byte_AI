# Batch URL Extraction Guide

## Quick Start (30 seconds)

```bash
# 1. Create urls directory
mkdir -p urls

# 2. Create urls/example.txt with URLs (one per line)
echo "https://en.wikipedia.org/wiki/Machine_Learning" >> urls/example.txt
echo "https://en.wikipedia.org/wiki/Deep_Learning" >> urls/example.txt

# 3. Run batch extraction
bash batch_extract.sh

# 4. Load bot
./knowledge_bot
```

## Methods

### Method 1: Manual URL Files

Create `urls/` directory with `.txt` files:

```
urls/
├── ai.txt
├── history.txt
├── science.txt
└── tech.txt
```

Each file contains one URL per line:
```
https://example.com/article1
https://example.com/article2
https://example.com/article3
```

Run extraction:
```bash
bash batch_extract.sh
```

### Method 2: Command Line with --urls

Extract from a single URL file:
```bash
python3 url.py --urls urls/ai.txt --category ai_knowledge
```

### Method 3: Batch Script

Use the automated batch processing script:
```bash
bash batch_extract.sh
bash batch_extract.sh --dry-run              # Preview only
bash batch_extract.sh --method paragraphs    # Different extraction method
bash batch_extract.sh --max-lines 50         # Limit output
bash batch_extract.sh --file tech            # Process only matching files
```

## Batch Script Options

```
--help              Show help message
--urls-dir <dir>    Directory with URL files (default: urls/)
--output <dir>      Output directory (default: training/)
--method <type>     sentences|paragraphs|full (default: sentences)
--max-lines <num>   Max lines per URL (default: 100)
--file <pattern>    Process only files matching pattern
--dry-run           Preview without processing
```

## Examples

### Example 1: AI Knowledge Base

Create `urls/ai.txt`:
```
https://en.wikipedia.org/wiki/Artificial_intelligence
https://en.wikipedia.org/wiki/Machine_learning
https://en.wikipedia.org/wiki/Deep_learning
https://en.wikipedia.org/wiki/Neural_network
https://en.wikipedia.org/wiki/Natural_language_processing
```

Process:
```bash
bash batch_extract.sh
```

Result: `training/ai_url.txt`

### Example 2: Multiple Categories

Create multiple files:

`urls/technology.txt`:
```
https://en.wikipedia.org/wiki/Computer_science
https://en.wikipedia.org/wiki/Software_engineering
https://en.wikipedia.org/wiki/Programming_language
```

`urls/history.txt`:
```
https://en.wikipedia.org/wiki/Ancient_Rome
https://en.wikipedia.org/wiki/World_War_I
https://en.wikipedia.org/wiki/Industrial_Revolution
```

Process all:
```bash
bash batch_extract.sh
```

Result: `training/technology_url.txt` and `training/history_url.txt`

### Example 3: Different Extraction Methods

Process news articles with sentences:
```bash
bash batch_extract.sh --file news --method sentences
```

Process long-form content with paragraphs:
```bash
bash batch_extract.sh --file blog --method paragraphs
```

Process documentation as full pages:
```bash
bash batch_extract.sh --file docs --method full
```

### Example 4: Dry Run (Preview)

See what would be processed without actually running:
```bash
bash batch_extract.sh --dry-run
```

Output:
```
═══════════════════════════════════════════════════════
📋 Files to Process (Dry Run)
═══════════════════════════════════════════════════════
• ai.txt (5 URLs)
• history.txt (3 URLs)
• science.txt (7 URLs)
```

### Example 5: Limit Output Size

Process but limit to 30 lines per URL:
```bash
bash batch_extract.sh --max-lines 30
```

## Extraction Methods

### Sentences (Default)
Splits content at periods, exclamation marks, question marks.

Best for: News articles, short blog posts, summaries
```bash
bash batch_extract.sh --method sentences
```

### Paragraphs
Splits content at line breaks.

Best for: Long-form articles, documentation, essays
```bash
bash batch_extract.sh --method paragraphs
```

### Full
Takes entire page as single entry.

Best for: Short pages, reference material, reference documentation
```bash
bash batch_extract.sh --method full
```

## File Organization

Recommended structure:

```
project/
├── urls/                    ← URL files here
│   ├── technology.txt
│   ├── history.txt
│   ├── science.txt
│   └── business.txt
├── training/               ← Output goes here
│   ├── technology_url.txt
│   ├── history_url.txt
│   ├── science_url.txt
│   └── business_url.txt
├── batch_extract.sh
└── url.py
```

## Processing Times

- 5 URLs: 30-60 seconds
- 10 URLs: 1-2 minutes
- 20 URLs: 2-4 minutes
- 50 URLs: 5-10 minutes

**Tip:** Process in batches of 10-20 URLs for best results

## Workflow

### Complete Workflow

1. **Create URLs directory**
   ```bash
   mkdir -p urls
   ```

2. **Create URL files** (one per line)
   ```bash
   echo "https://example.com/article1" >> urls/topic.txt
   echo "https://example.com/article2" >> urls/topic.txt
   ```

3. **Preview extraction** (optional)
   ```bash
   bash batch_extract.sh --dry-run
   ```

4. **Run batch extraction**
   ```bash
   bash batch_extract.sh
   ```

5. **Load bot**
   ```bash
   ./knowledge_bot
   ```

6. **Query your new knowledge**
   ```
   "What is X?"
   "Explain Y"
   "Tell me about Z"
   ```

## Troubleshooting

### Issue: "No URL files found"
**Solution:** Make sure you have `.txt` files in the `urls/` directory with URLs

### Issue: "url.py: command not found"
**Solution:** Make sure `url.py` is in the same directory as `batch_extract.sh`

### Issue: "Python not found"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: URLs not loading
**Solution:** Check that URLs start with `https://` or `http://`

### Issue: Empty output files
**Solution:** Try with `--method full` or check that URLs have content

## Tips & Tricks

### Tip 1: Organize by Source
```
urls/
├── wikipedia.txt
├── blogs.txt
├── news.txt
└── documentation.txt
```

### Tip 2: Process Different Sources Differently
```bash
# Process news quickly
bash batch_extract.sh --file news --method sentences --max-lines 30

# Process documentation thoroughly  
bash batch_extract.sh --file docs --method paragraphs --max-lines 200
```

### Tip 3: Create Multiple Batches
```bash
# First batch
bash batch_extract.sh --file "tech" --output training/tech/

# Second batch
bash batch_extract.sh --file "history" --output training/history/

# Load combined knowledge
./knowledge_bot
```

### Tip 4: Combine with Other Tools
```bash
# Extract from Wikipedia
python3 wiki.py "Artificial Intelligence"

# Extract from URLs
bash batch_extract.sh

# Extract from PDFs
python3 pdf.py book.pdf

# All combined!
./knowledge_bot
```

### Tip 5: Compress After Extraction
```bash
# Extract
bash batch_extract.sh

# Compress
cd training/
zip -r ai_knowledge.zip *_url.txt
rm *_url.txt  # Optional: delete originals to save space

# Load with bot
cd ..
./knowledge_bot  # Bot auto-extracts zip files!
```

## Command Reference

```bash
# Basic usage
bash batch_extract.sh

# Show help
bash batch_extract.sh --help

# Preview only (no processing)
bash batch_extract.sh --dry-run

# Process specific files
bash batch_extract.sh --file keyword

# Different extraction method
bash batch_extract.sh --method paragraphs
bash batch_extract.sh --method full

# Limit output
bash batch_extract.sh --max-lines 50

# Custom directories
bash batch_extract.sh --urls-dir my_urls/ --output my_training/

# Combine options
bash batch_extract.sh --file tech --method full --max-lines 100
```

## FAQ

**Q: How many URLs can I process at once?**
A: Unlimited, but recommended 10-20 per batch for stability

**Q: Can I interrupt the script?**
A: Yes, Ctrl+C to stop. Already processed files will be saved

**Q: Do URLs need to be public?**
A: Yes, the script needs to access them via HTTP/HTTPS

**Q: What formats are supported?**
A: Any public webpage (HTML). PDFs and other formats not supported in url.py

**Q: Can I use relative paths?**
A: URLs must be absolute (start with http:// or https://)

**Q: How do I organize large batches?**
A: Use separate files in urls/ directory, one category per file

**Q: Can I extract from the same URLs multiple times?**
A: Yes, files get overwritten with new extraction

**Q: How do I combine multiple batches into one file?**
A: Use `cat training/*_url.txt > training/combined.txt`
