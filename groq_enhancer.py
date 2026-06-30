#!/usr/bin/env python3
"""
Groq API Integration for Enhanced Responses
Enhances bot answers and collects training data
"""

import os
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    print("⚠️  groq library not installed")
    print("Install with: pip install groq python-dotenv")
    GROQ_AVAILABLE = False


class GroqEnhancer:
    """Enhance bot responses using Groq API"""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            print("❌ GROQ_API_KEY not found in .env")
            self.client = None
            return

        if not GROQ_AVAILABLE:
            print("⚠️  Groq not available")
            self.client = None
            return

        self.client = Groq(api_key=self.api_key)
        print("✅ Groq API initialized")

    def is_ready(self):
        """Check if Groq is available"""
        return self.client is not None

    def enhance_answer(self, question, bot_answer, context=""):
        """
        Enhance bot's answer using Groq

        Args:
            question: User's question
            bot_answer: Bot's original answer
            context: Additional context

        Returns:
            Enhanced answer or original if Groq fails
        """
        if not self.is_ready():
            return bot_answer

        try:
            prompt = f"""The user asked: "{question}"

The bot provided this answer: "{bot_answer}"

Please provide a better, more complete answer that:
1. Directly answers the question
2. Builds on the bot's information
3. Adds helpful context or examples
4. Is clear and concise

Enhanced answer:"""

            message = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            enhanced = message.choices[0].message.content.strip()
            return enhanced

        except Exception as e:
            print(f"⚠️  Groq enhancement failed: {e}")
            return bot_answer

    def generate_answer(self, question, training_context=""):
        """
        Generate answer from scratch using Groq

        Args:
            question: User's question
            training_context: Related training data

        Returns:
            Generated answer
        """
        if not self.is_ready():
            return None

        try:
            prompt = f"""Question: {question}

Related training data:
{training_context}

Please provide a comprehensive, accurate answer to the question.
Use the training data as reference but feel free to expand with your knowledge.

Answer:"""

            message = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.choices[0].message.content.strip()

        except Exception as e:
            print(f"⚠️  Groq generation failed: {e}")
            return None

    def improve_qa_pair(self, question, answer):
        """
        Improve a Q&A pair for training

        Args:
            question: Original question
            answer: Original answer

        Returns:
            Improved Q&A pair
        """
        if not self.is_ready():
            return question, answer

        try:
            prompt = f"""Original Q&A pair:
Q: {question}
A: {answer}

Please improve this Q&A pair for use as training data:
1. Make the question clearer
2. Make the answer more complete
3. Add relevant details
4. Maintain accuracy

Provide response in format:
IMPROVED_Q: [improved question]
IMPROVED_A: [improved answer]"""

            message = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            response = message.choices[0].message.content.strip()

            # Parse response
            lines = response.split('\n')
            improved_q = answer
            improved_a = answer

            for line in lines:
                if line.startswith("IMPROVED_Q:"):
                    improved_q = line.replace("IMPROVED_Q:", "").strip()
                elif line.startswith("IMPROVED_A:"):
                    improved_a = line.replace("IMPROVED_A:", "").strip()

            return improved_q, improved_a

        except Exception as e:
            print(f"⚠️  Groq improvement failed: {e}")
            return question, answer

    def categorize_query(self, query):
        """
        Categorize a query using Groq

        Args:
            query: User's query

        Returns:
            Category suggestion
        """
        if not self.is_ready():
            return "general"

        try:
            prompt = f"""Query: {query}

Suggest a single category (lowercase, no spaces) for this query.
Categories: ai, business, technology, science, health, history, general, other

Category:"""

            message = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )

            category = message.choices[0].message.content.strip().lower()
            return category if category else "general"

        except Exception as e:
            print(f"⚠️  Categorization failed: {e}")
            return "general"


def test_groq():
    """Test Groq connection"""
    enhancer = GroqEnhancer()

    if not enhancer.is_ready():
        print("❌ Groq not available")
        return

    print("\n🧪 Testing Groq API...")

    # Test 1: Enhance answer
    print("\n1. Enhancing answer...")
    original = "Paris is the capital of France."
    enhanced = enhancer.enhance_answer(
        "What is the capital of France?",
        original
    )
    print(f"Original: {original}")
    print(f"Enhanced: {enhanced}")

    # Test 2: Generate answer
    print("\n2. Generating answer...")
    answer = enhancer.generate_answer("What is machine learning?")
    print(f"Generated: {answer[:200]}...")

    # Test 3: Categorize
    print("\n3. Categorizing query...")
    category = enhancer.categorize_query("How do neural networks work?")
    print(f"Category: {category}")

    print("\n✅ Groq tests complete!")


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "test":
            test_groq()
        else:
            print("Usage: python3 groq_enhancer.py [command]")
            print("\nCommands:")
            print("  test - Test Groq connection")
    else:
        print("Groq Enhancer Module")
        print("Usage: python3 groq_enhancer.py test")


if __name__ == "__main__":
    main()
