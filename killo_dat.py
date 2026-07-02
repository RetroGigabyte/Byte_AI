#!/usr/bin/env python3
"""
Killo Dynamic Automatic Training (DAT) 2.75
Auto-learns from Wikipedia when knowledge is missing
Uses rotating user agents from web_agents.txt
"""

import requests
import json
import os
import re
import random
from datetime import datetime

class KilloDAT:
    def __init__(self, dynamic_knowledge_file="training/dynamic_knowledge.json"):
        self.dynamic_knowledge_file = dynamic_knowledge_file
        self.dynamic_knowledge = self.load_dynamic_knowledge()
        self.user_agents = self.load_user_agents()
        self.agent_index = 0
    
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
        
        if agents:
            print(f"✓ Loaded {len(agents)} user agents from web_agents.txt")
            return agents
        
        # Fallback to defaults
        return [
            "KilloDAT/2.75 (AI Learning; contact@anthropic.com)",
            "Killo/2.75 (Knowledge Training; videogamesarecool1234@outlook.com)",
            "WikiTrainer/1.0 (Knowledge Bot; retrogigabyteyt@gmail.com)"
        ]
    
    def get_user_agent(self):
        """Get next user agent (round-robin)"""
        if not self.user_agents:
            return "KilloDAT/2.75"
        agent = self.user_agents[self.agent_index]
        self.agent_index = (self.agent_index + 1) % len(self.user_agents)
        return agent
    
    def load_dynamic_knowledge(self):
        """Load previously learned dynamic knowledge"""
        if os.path.exists(self.dynamic_knowledge_file):
            try:
                with open(self.dynamic_knowledge_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_dynamic_knowledge(self):
        """Save learned knowledge"""
        os.makedirs(os.path.dirname(self.dynamic_knowledge_file), exist_ok=True)
        with open(self.dynamic_knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.dynamic_knowledge, f, indent=2, ensure_ascii=False)
    
    def search_wikipedia(self, query):
        """Search Wikipedia for a topic"""
        url = "https://en.wikipedia.org/w/api.php"
        headers = {"User-Agent": self.get_user_agent()}
        
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srwhat": "text",
            "srlimit": 3
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'query' in data and 'search' in data['query']:
                    results = data['query']['search']
                    if results:
                        return results[0]['title']
        except:
            pass
        return None
    
    def fetch_wikipedia_article(self, title):
        """Fetch full article from Wikipedia"""
        url = "https://en.wikipedia.org/w/api.php"
        headers = {"User-Agent": self.get_user_agent()}
        
        params = {
            "action": "query",
            "titles": title,
            "prop": "extracts",
            "explaintext": True,
            "format": "json"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'query' in data and 'pages' in data['query']:
                    page = next(iter(data['query']['pages'].values()))
                    if 'extract' in page and page['extract']:
                        return page['extract']
        except:
            pass
        return None
    
    def extract_sentences(self, text, max_length=300):
        """Extract sentences from Wikipedia text"""
        sentences = []
        if not text:
            return sentences
        
        paragraphs = text.split('\n\n')
        for paragraph in paragraphs:
            para = paragraph.strip()
            if len(para) < 20:
                continue
            
            para_sentences = re.split(r'(?<=[.!?])\s+', para)
            for sent in para_sentences:
                sent = sent.strip()
                if 10 < len(sent) < max_length:
                    if not sent.startswith(('See also', 'References', 'Contents', '==')):
                        sentences.append(sent)
        
        return sentences[:5]  # Return top 5 sentences
    
    def learn_topic(self, query):
        """Auto-learn a topic from Wikipedia"""
        print(f"\n🧠 DAT Mode: Learning '{query}' from Wikipedia...")
        
        # Search for topic
        title = self.search_wikipedia(query)
        if not title:
            print(f"❌ Could not find Wikipedia article for '{query}'")
            return None
        
        print(f"📖 Found: {title}")
        
        # Fetch article
        content = self.fetch_wikipedia_article(title)
        if not content:
            print(f"❌ Could not fetch article")
            return None
        
        # Extract sentences
        sentences = self.extract_sentences(content)
        if not sentences:
            print(f"❌ No relevant sentences found")
            return None
        
        # Store in dynamic knowledge
        category = query.lower().replace(" ", "_").replace("(", "").replace(")", "")
        self.dynamic_knowledge[category] = {
            "topic": query,
            "wikipedia_title": title,
            "sentences": sentences,
            "learned_at": datetime.now().isoformat(),
            "source": "Wikipedia"
        }
        
        self.save_dynamic_knowledge()
        print(f"✅ Learned {len(sentences)} facts about {query}")
        return self.dynamic_knowledge[category]
    
    def get_answer(self, query):
        """Get answer for a query (from dynamic knowledge or learn)"""
        # Check if already learned
        category = query.lower().replace(" ", "_").replace("(", "").replace(")", "")
        if category in self.dynamic_knowledge:
            data = self.dynamic_knowledge[category]
            sentences = data.get('sentences', [])
            if sentences:
                return {
                    "source": "dynamic",
                    "topic": data['topic'],
                    "wikipedia_title": data.get('wikipedia_title'),
                    "answer": "\n".join(sentences),
                    "learned_at": data.get('learned_at')
                }
        
        # Learn new topic
        learned = self.learn_topic(query)
        if learned:
            sentences = learned.get('sentences', [])
            return {
                "source": "newly_learned",
                "topic": learned['topic'],
                "wikipedia_title": learned.get('wikipedia_title'),
                "answer": "\n".join(sentences),
                "learned_at": learned.get('learned_at')
            }
        
        return None

def main():
    """CLI for testing DAT"""
    dat = KilloDAT()
    
    print("=" * 70)
    print("KILLO DYNAMIC AUTOMATIC TRAINING (DAT) 2.75")
    print("=" * 70)
    print("\nType a topic to learn about (or 'quit' to exit):\n")
    
    while True:
        query = input("📚 Learn about: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not query:
            continue
        
        result = dat.get_answer(query)
        if result:
            print(f"\n✨ Answer about {result['topic']}:")
            print(f"   (from {result['wikipedia_title']})")
            print(f"\n{result['answer']}\n")
        else:
            print(f"❌ Could not learn about '{query}'\n")

if __name__ == "__main__":
    main()
