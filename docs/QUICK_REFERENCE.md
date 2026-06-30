# Byte Knowledge Bot - Time Queries Quick Reference

## 🚀 Quick Start

```bash
./knowledge_bot

# Try these queries:
What time is it?
What's today?
What is 1 week from now?
Tell me about Python
```

---

## ⏰ Current Time/Date

| Query | Response |
|-------|----------|
| What time is it? | Monday, June 29, 2026 at 07:53 PM |
| What's the time? | Monday, June 29, 2026 at 07:53 PM |
| Current time | Monday, June 29, 2026 at 07:53 PM |
| What's today? | Monday, June 29, 2026 |
| What date is it? | Monday, June 29, 2026 |
| Today | Monday, June 29, 2026 |
| Tomorrow | Tuesday, June 30, 2026 |
| Yesterday | Sunday, June 28, 2026 |

---

## ⏱️ Seconds

| Query | Example |
|-------|---------|
| X seconds from now | `5 seconds from now` |
| in X seconds | `in 10 seconds` |
| X seconds ago | `30 seconds ago` |

---

## ⏲️ Minutes

| Query | Example |
|-------|---------|
| X minutes from now | `15 minutes from now` |
| in X minutes | `in 20 minutes` |
| X minutes ago | `30 minutes ago` |

---

## 🕐 Hours

| Query | Example |
|-------|---------|
| X hours from now | `3 hours from now` |
| in X hours | `in 2 hours` |
| X hours ago | `5 hours ago` |

---

## 📅 Days

| Query | Example |
|-------|---------|
| X days from now | `2 days from now` |
| in X days | `in 5 days` |
| X days ago | `3 days ago` |

---

## 📆 Weeks

| Query | Example |
|-------|---------|
| X weeks from now | `1 week from now`, `2 weeks from now` |
| in X weeks | `in 3 weeks` |
| X weeks ago | `2 weeks ago` |

---

## 📋 Months

| Query | Example |
|-------|---------|
| X months from now | `1 month from now`, `2 months from now` |
| in X months | `in 6 months` |
| X months ago | `3 months ago` |

---

## 📊 Years

| Query | Example |
|-------|---------|
| X years from now | `1 year from now`, `5 years from now` |
| in X years | `in 10 years` |
| X years ago | `2 years ago` |

---

## 🌍 Decades

| Query | Example |
|-------|---------|
| X decades from now | `1 decade from now`, `2 decades from now` |
| in X decades | `in 3 decades` |
| X decades ago | `1 decade ago` |

---

## 🔢 Number Formats

Both work the same:

```
Numeric:  "5 days from now"
Words:    "five days from now"
```

**Supported word numbers:**
one, two, three, four, five, six, seven, eight, nine, ten

---

## 📈 Special Formats

| Query | Response |
|-------|----------|
| Unix timestamp | 1782788131 |
| Unix timestamp 5 years from now | 1940468131 |
| Unix timestamp 30 minutes ago | 1782786331 |
| ISO format | 2026-06-30T02:53:00 |

### Unix Timestamp with Time Offset
```
unix timestamp 1 week from now
unix 3 months from now in timestamp
timestamp 10 days ago
unix time 2 years from now
```

---

## 📚 Knowledge Queries (Still Work!)

```
Tell me about Python
What is Docker?
Explain Kubernetes
What is React?
How does AI work?
... and 1200+ more topics!
```

---

## 💡 Tips & Tricks

### Numeric Numbers
```
What is 5 days from now?
3 hours from now?
10 minutes from now?
```

### Word Numbers
```
What is five days from now?
three hours from now?
ten minutes from now?
```

### Flexible Phrasing
```
✓ What is 2 weeks from now?
✓ 2 weeks from now
✓ In 2 weeks
✓ Two weeks from now
```

### Past References
```
✓ 2 weeks ago
✓ 3 days ago
✓ 5 hours ago
✓ 10 minutes ago
```

---

## 🎯 Real-World Examples

### Business
```
Q: When is the deadline 3 months from now?
A: Monday, September 28, 2026

Q: What was the date 2 weeks ago?
A: Monday, June 15, 2026
```

### Event Planning
```
Q: What is our event date one week from now?
A: Monday, July 06, 2026 at 07:53 PM

Q: What time is it right now?
A: Monday, June 29, 2026 at 07:53 PM
```

### Project Tracking
```
Q: When do we launch 6 months from now?
A: Wednesday, December 30, 2026

Q: How long since we started a year ago?
A: Wednesday, June 29, 2025
```

---

## ⚙️ How to Compile

```bash
g++ -std=c++17 knowledge_bot.cpp -o knowledge_bot
```

---

## 🧪 Test It

```bash
# Run the bot
./knowledge_bot

# Or test specific queries
echo "what is 2 weeks from now?" | ./knowledge_bot
echo "5 hours from now" | ./knowledge_bot
echo "Tell me about Python" | ./knowledge_bot
```

---

## 📞 Support

- For time features: See `TIME_FEATURES.md`
- For Python NTP: See `NTP_TIME_GUIDE.md`
- For testing: See `TEST_QUERIES.md`
- For overview: See `COMPLETION_SUMMARY.md`

---

## ✅ Features Status

| Feature | Status |
|---------|--------|
| Seconds | ✅ |
| Minutes | ✅ |
| Hours | ✅ |
| Days | ✅ |
| Weeks | ✅ |
| Months | ✅ |
| Years | ✅ |
| Decades | ✅ |
| Past/Future | ✅ |
| Number Parsing | ✅ |
| Plural Handling | ✅ |
| Knowledge Base | ✅ |

---

**Status**: ✅ Production Ready

*Ready to use right now! Just run: `./knowledge_bot`*
