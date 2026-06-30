# Training Mode & Auto-Train Pipeline Guide

## Overview

Two powerful tools for continuous bot improvement:

1. **training_mode.py** - Collect Q&A pairs
2. **auto_train.py** - Automatically process and improve training data

---

## Training Mode - Collect Q&A Pairs

### Interactive Collection

```bash
python3 training_mode.py interactive
```

Menu options:
- **1. Add Q&A pair** - Enter question/answer manually
- **2. View stats** - See what you've collected
- **3. View recent** - See latest Q&A pairs
- **4. Exit** - Save and exit

### Example Session

```
🎓 TRAINING MODE - Collect Q&A Pairs

Options:
  1. Add Q&A pair
  2. View stats
  3. View recent
  4. Exit

Choice (1-4): 1

--- Add Q&A Pair ---
Question: What is machine learning?
Answer: Machine learning is a subset of AI that learns from data
Category (default: custom): ai
Source (default: user): manual

✅ Q&A pair saved!
```

---

## Command Reference - training_mode.py

### Interactive Mode
```bash
python3 training_mode.py interactive
```
Guided Q&A collection with menu.

### View Statistics
```bash
python3 training_mode.py stats
```
Show collected Q&A statistics by category and source.

### Show Recent Pairs
```bash
python3 training_mode.py recent
python3 training_mode.py recent 10
```
Display recent Q&A pairs (default: 5 shown).

### Export to Training
Built into auto-train pipeline.

---

## Auto-Train Pipeline - Improve Bot

### Full Pipeline

```bash
python3 auto_train.py run
```

Complete workflow:
1. ✅ Backup current training data
2. ✅ Process all Q&A pairs
3. ✅ Generate improvement summary
4. ✅ Create new training zip
5. ✅ Recompile bot

### Process Only

```bash
python3 auto_train.py process
```
Process Q&A pairs without full pipeline.

### Show Summary

```bash
python3 auto_train.py summary
```
Display training improvement statistics.

### Backup Training Data

```bash
python3 auto_train.py backup
```
Create timestamped backup of current training.

### Recompile Bot

```bash
python3 auto_train.py compile
```
Rebuild bot with new training data.

### Schedule Auto-Train

```bash
python3 auto_train.py schedule 24
```
Create cron job for automatic training every 24 hours.

---

## Complete Workflow

### Step 1: Collect Training Data

```bash
# Interactive mode
python3 training_mode.py interactive

# Or add programmatically
# Add 5-10 Q&A pairs for topics you want to improve
```

### Step 2: View What You've Collected

```bash
# Stats
python3 training_mode.py stats

# Recent pairs
python3 training_mode.py recent 10
```

### Step 3: Run Auto-Train Pipeline

```bash
# Full pipeline: backup → process → summary → compile
python3 auto_train.py run
```

### Step 4: Test Improved Bot

```bash
# Bot now uses new training data!
./knowledge_bot

# Try queries related to new training
"What is machine learning?"
```

### Step 5: (Optional) Schedule Auto-Training

```bash
# Auto-run every 24 hours
python3 auto_train.py schedule 24

# View the cron command to add manually
```

---

## Data Flow

```
User Interaction
       ↓
Training Mode (training_mode.py)
       ↓
Collect Q&A Pairs
       ↓
training/qa_training/qa_pairs.jsonl
       ↓
Auto-Train Pipeline (auto_train.py)
       ↓
Process & Backup
       ↓
training/*_trained.txt
       ↓
Recompile Bot
       ↓
knowledge_bot (improved!)
```

---

## File Structure

```
training/
├── qa_training/                    ← Q&A collection
│   ├── qa_pairs.jsonl             ← All Q&A pairs (JSON)
│   ├── custom_qa.txt              ← Q&A by category
│   ├── ai_qa.txt
│   ├── business_qa.txt
│   └── processed/                 ← Processing history
│
├── backups/                        ← Auto-train backups
│   ├── backup_20260629_120000.zip
│   └── ...
│
├── *_trained.txt                  ← Generated training files
├── training_data.zip              ← Main training zip
└── ... (other zips)
```

---

## Use Cases

### Use Case 1: Improve Q&A Coverage

```bash
# 1. Identify weak areas by running bot
./knowledge_bot
# "What about X?" → poor answer

# 2. Collect better Q&A pairs
python3 training_mode.py interactive
# Add: "What is X?" → "Good explanation of X"

# 3. Auto-improve
python3 auto_train.py run

# 4. Test
./knowledge_bot
# "What is X?" → better answer!
```

### Use Case 2: Add New Topics

```bash
# 1. Collect Q&A for new topic
python3 training_mode.py interactive

# Add multiple pairs for "kubernetes", "docker", etc.
# Category: "devops"

# 2. Run pipeline
python3 auto_train.py run

# 3. Bot now knows about DevOps!
./knowledge_bot
"Tell me about Kubernetes"
```

### Use Case 3: Continuous Learning

```bash
# Run bot in production
./knowledge_bot

# Users interact with bot
# Collect good Q&A pairs from interactions

# Schedule auto-training
python3 auto_train.py schedule 24

# Bot improves automatically every day!
```

### Use Case 4: A/B Testing

```bash
# Test different answers
python3 training_mode.py interactive

# Add same question with different answers
# Later auto-train will keep both examples

# Bot learns variations
python3 auto_train.py run
```

---

## Advanced: Groq API Integration (Future)

When you have a new API key:

```bash
# Groq will enhance responses
python3 training_mode.py interactive --groq
# Uses Groq to generate better answers

# Auto-train with Groq
python3 auto_train.py run --groq
# Uses Groq for quality improvement
```

---

## Troubleshooting

### Q&A pairs not processing?
```bash
# Check JSON format
python3 training_mode.py stats

# Verify qa_pairs.jsonl exists
ls -la training/qa_training/
```

### Auto-train failed?
```bash
# Check backups
ls -la training/backups/

# Revert to backup
cd training && unzip backups/backup_*.zip
```

### Bot not using new training?
```bash
# Recompile explicitly
python3 auto_train.py compile

# Then run
./knowledge_bot
```

---

## Tips & Tricks

### Tip 1: Batch Add Q&A
```bash
# Add 10 pairs at once
python3 training_mode.py interactive
# (keeps prompting for more)
```

### Tip 2: Review Before Auto-Train
```bash
# Check what will be added
python3 training_mode.py recent 20

# Then run pipeline
python3 auto_train.py run
```

### Tip 3: Daily Auto-Training
```bash
# Schedule
python3 auto_train.py schedule 24

# Checks for new Q&A pairs each day
# Auto-improves if found
```

### Tip 4: Category Organization
When adding Q&A, use clear categories:
- `ai` - Artificial Intelligence
- `devops` - DevOps tools
- `business` - Business topics
- `custom` - Generic

This helps organize training files.

---

## Security Note

**API Key Storage (When Using Groq)**

Never commit API keys! Use `.env` file:

```bash
# Create .env
echo "GROQ_API_KEY=your_new_key_here" > .env

# Add to .gitignore
echo ".env" >> .gitignore

# Python code reads it
from dotenv import load_dotenv
api_key = os.getenv('GROQ_API_KEY')
```

---

## Summary

```
🎓 Training Mode
  → Collect Q&A pairs manually or from interactions

🤖 Auto-Train Pipeline
  → Process pairs → Backup → Compile → Improve bot

📈 Result
  → Bot continuously learns and improves!
```

Start collecting and improving your bot today! 🚀
