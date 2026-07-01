#!/usr/bin/env python3
"""
User Agent Rotator
Loads user agents from web_agents.txt and rotates through them
Helps avoid being blocked when scraping
"""

import random
import os

class UserAgentRotator:
    def __init__(self, agents_file="web_agents.txt"):
        """Initialize with user agents from file"""
        self.agents = []
        self.current_idx = 0
        self.load_agents(agents_file)

    def load_agents(self, agents_file):
        """Load user agents from file"""
        if not os.path.exists(agents_file):
            print(f"⚠️  {agents_file} not found, using default")
            self.agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "ComprehensiveWikiScraper/1.0"
            ]
            return

        try:
            with open(agents_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        self.agents.append(line)

            if self.agents:
                print(f"✓ Loaded {len(self.agents)} user agents from {agents_file}")
            else:
                raise ValueError("No valid agents found")

        except Exception as e:
            print(f"⚠️  Error loading agents: {e}")
            self.agents = ["ComprehensiveWikiScraper/1.0"]

    def get(self):
        """Get next user agent (round-robin)"""
        if not self.agents:
            return "ComprehensiveWikiScraper/1.0"

        agent = self.agents[self.current_idx]
        self.current_idx = (self.current_idx + 1) % len(self.agents)
        return agent

    def get_random(self):
        """Get random user agent"""
        if not self.agents:
            return "ComprehensiveWikiScraper/1.0"
        return random.choice(self.agents)


# Singleton instance
_rotator = None

def get_rotator():
    """Get or create the rotator instance"""
    global _rotator
    if _rotator is None:
        _rotator = UserAgentRotator()
    return _rotator

def get_user_agent():
    """Get next user agent (round-robin)"""
    return get_rotator().get()

def get_random_user_agent():
    """Get random user agent"""
    return get_rotator().get_random()

def switch_user_agent():
    """Force switch to a different random user agent"""
    return get_rotator().get_random()
