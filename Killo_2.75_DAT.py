#!/usr/bin/env python3
"""
Killo 2.75 DAT - Dynamic Automatic Training
Python wrapper for C++ Killo engine
Auto-learns from Wikipedia when Killo has low confidence
"""

import subprocess
import json
import sys
import requests
import re
import os
import math
from datetime import datetime

class Killo275DAT:
    def __init__(self):
        self.killo_binary = "./Killo"
        self.user_agents = self.load_user_agents()
        self.agent_index = 0
        self.dat_cache = self.load_dat_cache()

        # Hardcoded simple responses
        self.simple_responses = {
            # Greetings
            'hello': "Hi there! How can I help you?",
            'hi': "Hey! What would you like to know?",
            'hey': "Hello! What's on your mind?",
            'greetings': "Greetings! Ask me anything.",
            'good morning': "Good morning! What can I assist with?",
            'good afternoon': "Good afternoon! What do you need?",
            'good evening': "Good evening! How can I help?",
            'good night': "Good night! Sleep well.",

            # Time & Date
            'what time is it': datetime.now().strftime("It's %I:%M %p"),
            'time': datetime.now().strftime("It's %I:%M %p"),
            'current time': datetime.now().strftime("It's %I:%M %p"),
            'what is the time': datetime.now().strftime("It's %I:%M %p"),
            'what day is it': datetime.now().strftime("Today is %A, %B %d, %Y"),
            'date': datetime.now().strftime("Today is %A, %B %d, %Y"),
            'what is the date': datetime.now().strftime("Today is %A, %B %d, %Y"),
            'today': datetime.now().strftime("Today is %A, %B %d, %Y"),

            # Leaving
            'goodbye': "Goodbye! See you later!",
            'bye': "Bye! Take care!",
            'see you': "See you later!",
            'farewell': "Farewell! Come back soon!",
            'quit': "Goodbye!",
            'exit': "Goodbye!",

            # Help
            'help': "I'm Killo 2.75 DAT! Ask me about anything. If I don't know, I'll learn from Wikipedia!",
            'who are you': "I'm Killo 2.75, an AI knowledge bot with Dynamic Automatic Training (DAT)!",
            'what are you': "I'm Killo 2.75, an AI knowledge bot with Dynamic Automatic Training (DAT)!",
            'who am i': "You're a curious person! What would you like to learn?",
            'how are you': "I'm doing great! How can I help you?",

            # Acknowledgments
            'thanks': "You're welcome!",
            'thank you': "You're welcome!",
            'ok': "Great! Anything else?",
            'okay': "Great! Anything else?",
            'yes': "Excellent! What else?",
            'no': "No problem! Ask me anything else.",
            'sure': "Absolutely! What would you like to know?",
        }
    
    def load_user_agents(self):
        """Load user agents from web_agents.txt"""
        agents = []
        if os.path.exists("web_agents.txt"):
            try:
                with open("web_agents.txt", 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            agents.append(line)
            except:
                pass
        return agents if agents else ["Killo/2.75 (DAT)"]
    
    def get_user_agent(self):
        """Get next user agent"""
        if not self.user_agents:
            return "Killo/2.75 (DAT)"
        agent = self.user_agents[self.agent_index]
        self.agent_index = (self.agent_index + 1) % len(self.user_agents)
        return agent
    
    def load_dat_cache(self):
        """Load cached Wikipedia learning"""
        cache_file = "training/dat_cache.json"
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_dat_cache(self):
        """Save Wikipedia learning cache"""
        cache_file = "training/dat_cache.json"
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.dat_cache, f, indent=2, ensure_ascii=False)
    
    def search_wikipedia(self, query):
        """Search Wikipedia for topic"""
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": 1
        }
        headers = {"User-Agent": self.get_user_agent()}
        
        try:
            r = requests.get(url, params=params, headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if 'query' in data and 'search' in data['query'] and data['query']['search']:
                    return data['query']['search'][0]['title']
        except:
            pass
        return None
    
    def fetch_wikipedia(self, title):
        """Fetch Wikipedia article"""
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "titles": title,
            "prop": "extracts",
            "explaintext": True,
            "format": "json"
        }
        headers = {"User-Agent": self.get_user_agent()}
        
        try:
            r = requests.get(url, params=params, headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                page = next(iter(data['query']['pages'].values()))
                if 'extract' in page:
                    return page['extract']
        except:
            pass
        return None
    
    def extract_sentences(self, text, max_count=5):
        """Extract key sentences from Wikipedia"""
        if not text:
            return []
        
        sentences = []
        for para in text.split('\n\n'):
            para = para.strip()
            if len(para) < 20:
                continue
            
            for sent in re.split(r'(?<=[.!?])\s+', para):
                sent = sent.strip()
                if 10 < len(sent) < 300:
                    if not sent.startswith(('See also', 'References', '==')):
                        sentences.append(sent)
                        if len(sentences) >= max_count:
                            return sentences
        
        return sentences
    
    def learn_from_wikipedia(self, query):
        """DAT: Auto-learn from Wikipedia"""
        cache_key = query.lower().replace(" ", "_").replace("(", "").replace(")", "")
        
        # Check cache first
        if cache_key in self.dat_cache:
            return self.dat_cache[cache_key]
        
        print(f"\n🧠 DAT: Learning '{query}' from Wikipedia...")
        
        # Search Wikipedia
        title = self.search_wikipedia(query)
        if not title:
            print(f"❌ Not found on Wikipedia")
            return None
        
        print(f"📖 Found: {title}")
        
        # Fetch article
        content = self.fetch_wikipedia(title)
        if not content:
            print(f"❌ Could not fetch article")
            return None
        
        # Extract sentences
        sentences = self.extract_sentences(content)
        if not sentences:
            print(f"❌ No relevant content")
            return None
        
        # Cache it
        self.dat_cache[cache_key] = {
            "title": title,
            "sentences": sentences,
            "learned_at": datetime.now().isoformat()
        }
        self.save_dat_cache()
        
        print(f"✅ Learned {len(sentences)} facts")
        return self.dat_cache[cache_key]
    
    def evaluate_math(self, query):
        """Evaluate math expressions"""
        query_lower = query.lower().strip()

        # Word-based math: "what is X plus Y" -> evaluate
        math_words = {
            'plus': '+',
            'add': '+',
            'minus': '-',
            'subtract': '-',
            'times': '*',
            'multiply': '*',
            'divided by': '/',
            'divide': '/',
            'to the power of': '**',
            'power': '**',
            'squared': '**2',
            'cubed': '**3',
            'modulo': '%',
            'mod': '%',
        }

        # Check for "what is" pattern
        if query_lower.startswith('what is ') or query_lower.startswith('calculate '):
            expr = query_lower.replace('what is ', '').replace('calculate ', '')

            # Replace word operators with symbols
            for word, symbol in math_words.items():
                expr = expr.replace(word, symbol)

            # Clean up
            expr = expr.replace('^', '**').strip()

            # Try to evaluate
            try:
                # Safe evaluation with limited namespace
                result = eval(expr, {"__builtins__": {}}, {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan, "pi": math.pi, "e": math.e})

                # Format result
                if isinstance(result, float):
                    if result == int(result):
                        return f"{int(result)}"
                    else:
                        return f"{result:.2f}"
                return str(result)
            except:
                pass

        # Direct math expression: "2+3", "10/2", etc
        if any(op in query for op in ['+', '-', '*', '/', '%', '^', '**', '(']):
            expr = query.replace('^', '**').strip()
            try:
                result = eval(expr, {"__builtins__": {}}, {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan, "pi": math.pi, "e": math.e})

                if isinstance(result, float):
                    if result == int(result):
                        return f"{int(result)}"
                    else:
                        return f"{result:.2f}"
                return str(result)
            except:
                pass

        return None

    def check_simple_response(self, query):
        """Check if query has a hardcoded simple response"""
        query_lower = query.lower().strip()

        # 1. Try math first
        math_result = self.evaluate_math(query)
        if math_result:
            return math_result

        # 2. Handle compound queries (time AND date, etc)
        if 'time' in query_lower and 'date' in query_lower:
            time_str = datetime.now().strftime("%I:%M %p")
            date_str = datetime.now().strftime("%A, %B %d, %Y")
            return f"It's {time_str} on {date_str}"

        # 3. Exact match
        if query_lower in self.simple_responses:
            return self.simple_responses[query_lower]

        # 4. Check if query contains any hardcoded phrase
        for key, response in self.simple_responses.items():
            if key in query_lower:
                return response

        return None

    def ask_killo(self, query):
        """Ask Killo C++ engine"""
        try:
            result = subprocess.run(
                [self.killo_binary, query],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception as e:
            pass

        return None
    
    def run_chat(self):
        """Interactive chat loop"""
        print("=" * 70)
        print("KILLO 2.75 DAT - Dynamic Automatic Training")
        print("=" * 70)
        print("Ask anything! If Killo doesn't know, it auto-learns from Wikipedia.")
        print("Type 'quit' to exit.\n")

        while True:
            query = input("You: ").strip()

            if not query:
                continue
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break

            # 1. Check for simple hardcoded responses first (fast)
            simple_response = self.check_simple_response(query)
            if simple_response:
                print(f"\nKillo: {simple_response}\n")
                continue

            # 2. Ask Killo (uses .txt training data)
            killo_response = self.ask_killo(query)
            if killo_response:
                print(f"\nKillo: {killo_response}\n")
                continue

            # 3. DAT: Learn from Wikipedia
            learned = self.learn_from_wikipedia(query)
            if learned:
                print(f"\n📚 From Wikipedia ({learned['title']}):")
                for sent in learned['sentences']:
                    print(f"   • {sent}")
                print()
            else:
                print("❌ Killo doesn't know, couldn't find on Wikipedia.\n")

def main():
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        dat = Killo275DAT()

        # 1. Check simple responses
        simple = dat.check_simple_response(query)
        if simple:
            print(simple)
            return

        # 2. Ask Killo
        response = dat.ask_killo(query)
        if response:
            print(response)
            return

        # 3. DAT: Learn from Wikipedia
        learned = dat.learn_from_wikipedia(query)
        if learned:
            print(f"📚 From Wikipedia ({learned['title']}):")
            for sent in learned['sentences']:
                print(f"   • {sent}")
        else:
            print("❌ No answer found")
    else:
        # Interactive mode
        dat = Killo275DAT()
        dat.run_chat()

if __name__ == "__main__":
    main()
