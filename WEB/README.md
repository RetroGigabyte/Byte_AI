# Killo 2.75 DAT - Web Server

Web interface for Killo 2.75 DAT knowledge bot.

## Quick Start

```bash
cd WEB

# Install dependencies
pip install -r requirements.txt

# Run web server
python3 app.py
```

Open: **http://localhost:5000**

## Structure

```
WEB/
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Main chat UI
└── static/
    ├── css/
    │   └── style.css        # Styling
    └── js/
        └── main.js          # Client-side logic
```

## Features

- 💬 Real-time chat interface
- 🧮 Math evaluation
- 🧠 Killo C++ training
- 📚 DAT Wikipedia auto-learn
- 💾 Conversation history
- 📊 Stats & analytics

## API Endpoints

- `POST /api/chat` - Send query
- `GET /api/history` - Get conversation
- `POST /api/clear` - Clear history
- `GET /api/stats` - Get statistics

## Development

Coming soon: Byte 3.0 Mega enhancements
