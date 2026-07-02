#!/usr/bin/env python3
"""
Killo 2.75 DAT Web Server
Flask backend for web interface
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Killo_2.75_DAT import Killo275DAT

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize Killo DAT
killo = Killo275DAT()

# Conversation history
conversation_history = []
MAX_HISTORY = 50

@app.route('/')
def index():
    """Serve main chat page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat queries"""
    try:
        data = request.get_json()
        query = data.get('message', '').strip()
        
        if not query:
            return jsonify({'error': 'Empty query'}), 400
        
        # Add to history
        conversation_history.append({
            'type': 'user',
            'message': query
        })
        
        # 1. Check simple responses
        simple = killo.check_simple_response(query)
        if simple:
            response = {
                'type': 'simple',
                'source': 'Hardcoded',
                'answer': simple
            }
        else:
            # 2. Ask Killo
            killo_response = killo.ask_killo(query)
            if killo_response:
                response = {
                    'type': 'killo',
                    'source': 'Killo C++',
                    'answer': killo_response
                }
            else:
                # 3. DAT Wikipedia
                learned = killo.learn_from_wikipedia(query)
                if learned:
                    response = {
                        'type': 'dat',
                        'source': f'Wikipedia ({learned["title"]})',
                        'answer': '\n\n'.join(learned['sentences'])
                    }
                else:
                    response = {
                        'type': 'error',
                        'source': 'N/A',
                        'answer': "❌ Killo doesn't know, couldn't find on Wikipedia."
                    }
        
        # Add to history
        conversation_history.append({
            'type': 'bot',
            'response': response
        })
        
        # Keep history size manageable
        if len(conversation_history) > MAX_HISTORY:
            conversation_history.pop(0)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e), 'type': 'error'}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    return jsonify({'history': conversation_history})

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'cleared'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get Killo stats"""
    return jsonify({
        'cached_topics': len(killo.dat_cache),
        'user_agents': len(killo.user_agents),
        'conversation_length': len(conversation_history)
    })

if __name__ == '__main__':
    print("=" * 70)
    print("KILLO 2.75 DAT - WEB SERVER")
    print("=" * 70)
    print("\n🌐 Starting web server...")
    print("📱 Open: http://localhost:5000")
    print("🧠 Killo initialized with DAT")
    print("=" * 70 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
