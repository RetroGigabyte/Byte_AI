# Groq API Setup Guide

## ⚠️ Model Update Required

Groq frequently updates available models. The models we configured are currently deprecated.

## ✅ Step 1: Check Available Models

1. Go to: https://console.groq.com/docs/models
2. Look for currently available models (they update frequently)
3. Common current models include:
   - `gemma-7b-it` (fast, good quality)
   - `gemma2-9b-it` (faster, decent quality)
   - `mixtral-8x7b-32768` (if available)
   - `llama-3.1-70b` (if available with new suffix)

## 🔧 Step 2: Update groq_enhancer.py

Replace all instances of the model name with a current one:

```bash
# Option 1: Use sed to replace all instances
sed -i 's/llama3-70b-8192/gemma-7b-it/g' groq_enhancer.py

# Option 2: Manually edit and replace
# Change: model="llama3-70b-8192"
# To: model="gemma-7b-it"
```

Or edit the file directly:
- Line 45: Replace model name
- Line 53: Replace model name
- Line 72: Replace model name
- Line 104: Replace model name

## 📝 Example Update

```python
# Before:
message = self.client.chat.completions.create(
    model="llama3-70b-8192",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

# After:
message = self.client.chat.completions.create(
    model="gemma-7b-it",  # Check console.groq.com for current models
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
```

## 🧪 Step 3: Test Again

```bash
python3 groq_enhancer.py test
```

Should see:
```
✅ Groq API initialized
🧪 Testing Groq API...
1. Enhancing answer...
Enhanced: [better answer]
2. Generating answer...
Generated: [full answer]
3. Categorizing query...
Category: ai
✅ Groq tests complete!
```

## 🔄 Keeping Models Updated

Groq updates models regularly. If you see "model_decommissioned" errors:

1. Check https://console.groq.com/docs/models for current models
2. Update `groq_enhancer.py` with new model name
3. Test with `python3 groq_enhancer.py test`

## 💡 Quick Fix Script

```bash
#!/bin/bash
# Update model in groq_enhancer.py
sed -i 's/llama3-70b-8192/gemma-7b-it/g' groq_enhancer.py
sed -i 's/mixtral-8x7b-32768/gemma-7b-it/g' groq_enhancer.py
sed -i 's/llama-3.1-70b-versatile/gemma-7b-it/g' groq_enhancer.py

echo "✅ Updated to gemma-7b-it"
python3 groq_enhancer.py test
```

## 🚀 Your System is Ready

Once you update the model:

1. **Groq Integration Works**: Answer enhancement, generation, Q&A improvement
2. **Training Mode Ready**: Collect Q&A pairs
3. **Auto-Train Ready**: Automatic improvement pipeline
4. **Your Bot Learns**: Continuous improvement from Groq

## 📚 Full Workflow

```bash
# 1. Collect Q&A (improved suggestions from Groq)
python3 training_mode.py interactive --groq

# 2. Auto-improve (Groq enhances Q&A before training)
python3 auto_train.py run --groq

# 3. Test improved bot
./knowledge_bot

# 4. See improvement!
```

---

**Note:** Keep checking https://console.groq.com/docs/models as Groq releases new models regularly.
