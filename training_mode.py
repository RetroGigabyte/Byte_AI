#!/usr/bin/env python3
"""
Training Mode Script
Collects Q&A pairs from user interactions and saves them for training
"""

import os
import json
import datetime
from pathlib import Path

try:
    from groq_enhancer import GroqEnhancer
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

class TrainingMode:
    """Collects and saves Q&A pairs for training"""

    def __init__(self, training_dir="training"):
        self.training_dir = training_dir
        self.qa_dir = os.path.join(training_dir, "qa_training")
        self.create_directories()

    def create_directories(self):
        """Create necessary directories"""
        Path(self.qa_dir).mkdir(parents=True, exist_ok=True)
        print(f"✓ Training directory: {self.qa_dir}/")

    def save_qa_pair(self, question, answer, category="custom", source="user"):
        """
        Save a Q&A pair to training file

        Args:
            question: User's question
            answer: Bot's answer
            category: Topic category
            source: Source of Q&A (user, groq, manual, etc.)
        """
        # Create category file if it doesn't exist
        category_file = os.path.join(self.qa_dir, f"{category}_qa.txt")

        # Format: category: question -> answer
        timestamp = datetime.datetime.now().isoformat()
        entry = f"{category}: Q: {question} | A: {answer} [{source}] ({timestamp})"

        try:
            with open(category_file, 'a', encoding='utf-8') as f:
                f.write(entry + '\n')
            return True
        except Exception as e:
            print(f"❌ Error saving Q&A pair: {e}")
            return False

    def save_qa_json(self, question, answer, category="custom", source="user"):
        """Save Q&A pair as JSON for structured processing"""
        json_file = os.path.join(self.qa_dir, "qa_pairs.jsonl")

        qa_entry = {
            "question": question,
            "answer": answer,
            "category": category,
            "source": source,
            "timestamp": datetime.datetime.now().isoformat()
        }

        try:
            with open(json_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(qa_entry) + '\n')
            return True
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            return False

    def get_qa_stats(self):
        """Get statistics about collected Q&A pairs"""
        stats = {
            "total_pairs": 0,
            "by_category": {},
            "by_source": {}
        }

        json_file = os.path.join(self.qa_dir, "qa_pairs.jsonl")

        if not os.path.exists(json_file):
            return stats

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        stats["total_pairs"] += 1

                        category = data.get("category", "unknown")
                        source = data.get("source", "unknown")

                        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
                        stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
        except Exception as e:
            print(f"❌ Error reading stats: {e}")

        return stats

    def interactive_training(self):
        """Interactive training session"""
        print("\n" + "="*60)
        print("🎓 TRAINING MODE - Collect Q&A Pairs")
        print("="*60 + "\n")

        while True:
            print("\nOptions:")
            print("  1. Add Q&A pair")
            print("  2. View stats")
            print("  3. View recent pairs")
            print("  4. Exit")

            choice = input("\nChoice (1-4): ").strip()

            if choice == "1":
                self.add_qa_interactive()
            elif choice == "2":
                self.show_stats()
            elif choice == "3":
                self.show_recent()
            elif choice == "4":
                print("\n✓ Training session ended!")
                break
            else:
                print("❌ Invalid choice")

    def add_qa_interactive(self):
        """Interactively add a Q&A pair"""
        print("\n--- Add Q&A Pair ---")

        question = input("Question: ").strip()
        if not question:
            print("❌ Question cannot be empty")
            return

        # Offer Groq option if available
        answer = None
        if GROQ_AVAILABLE:
            print("\nOptions:")
            print("  1. Enter answer manually")
            print("  2. Generate answer with Groq AI")
            choice = input("Choice (1-2): ").strip()

            if choice == "2":
                print("\n🤖 Generating answer with Groq...")
                enhancer = GroqEnhancer()
                if enhancer.is_ready():
                    answer = enhancer.generate_answer(question)
                    if answer:
                        print(f"\n✨ Generated Answer:")
                        print(f"{answer}\n")
                        print("Options:")
                        print("  1. Use this answer")
                        print("  2. Edit this answer")
                        print("  3. Discard and enter manually")
                        choice = input("Choice (1-3): ").strip()

                        if choice == "2":
                            print("\nEdit the answer (current answer shown):")
                            answer = input("Answer: ").strip()
                            if not answer:
                                print("❌ Answer cannot be empty")
                                return
                        elif choice == "3":
                            answer = None
                        elif choice != "1":
                            print("❌ Invalid choice")
                            return
                    else:
                        print("❌ Groq generation failed")
                else:
                    print("❌ Groq not available")

        # Manual entry if Groq not used or available
        if not answer:
            answer = input("Answer: ").strip()
            if not answer:
                print("❌ Answer cannot be empty")
                return

        category = input("Category (default: custom): ").strip() or "custom"
        source = input("Source (default: user): ").strip() or "user"

        if self.save_qa_pair(question, answer, category, source):
            if self.save_qa_json(question, answer, category, source):
                print("✅ Q&A pair saved!")
            else:
                print("⚠️  Saved to text file but JSON save failed")
        else:
            print("❌ Failed to save Q&A pair")

    def show_stats(self):
        """Display Q&A collection statistics"""
        stats = self.get_qa_stats()

        print("\n📊 Training Statistics")
        print(f"  Total Q&A pairs: {stats['total_pairs']}")

        if stats['by_category']:
            print("\n  By Category:")
            for category, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True):
                print(f"    • {category}: {count}")

        if stats['by_source']:
            print("\n  By Source:")
            for source, count in sorted(stats['by_source'].items(), key=lambda x: x[1], reverse=True):
                print(f"    • {source}: {count}")

    def show_recent(self, limit=5):
        """Show recent Q&A pairs"""
        json_file = os.path.join(self.qa_dir, "qa_pairs.jsonl")

        if not os.path.exists(json_file):
            print("❌ No Q&A pairs yet")
            return

        print(f"\n📋 Recent Q&A Pairs (last {limit}):")

        try:
            pairs = []
            with open(json_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        pairs.append(json.loads(line))

            for pair in pairs[-limit:]:
                print(f"\n  Q: {pair['question']}")
                print(f"  A: {pair['answer']}")
                print(f"  Category: {pair['category']} | Source: {pair['source']}")
        except Exception as e:
            print(f"❌ Error reading pairs: {e}")

    def export_to_training(self):
        """Export collected Q&A pairs to training files"""
        print("\n📤 Exporting Q&A pairs to training files...")

        json_file = os.path.join(self.qa_dir, "qa_pairs.jsonl")

        if not os.path.exists(json_file):
            print("❌ No Q&A pairs to export")
            return 0

        export_count = 0

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        category = data.get("category", "custom")
                        question = data.get("question", "")
                        answer = data.get("answer", "")

                        # Save as training format: category: content
                        training_file = os.path.join(self.training_dir, f"{category}_trained.txt")

                        # Format for training bot
                        entry = f"{category}: {question} -> {answer}\n"

                        with open(training_file, 'a', encoding='utf-8') as tf:
                            tf.write(entry)

                        export_count += 1

            print(f"✅ Exported {export_count} Q&A pairs to training files")
            return export_count

        except Exception as e:
            print(f"❌ Error exporting: {e}")
            return 0


def main():
    """Main entry point"""
    trainer = TrainingMode()

    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "interactive":
            trainer.interactive_training()
        elif command == "stats":
            trainer.show_stats()
        elif command == "export":
            trainer.export_to_training()
        elif command == "recent":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            trainer.show_recent(limit)
        else:
            print("Usage: python3 training_mode.py [command]")
            print("\nCommands:")
            print("  interactive  - Interactive Q&A collection")
            print("  stats        - Show statistics")
            print("  export       - Export to training files")
            print("  recent [N]   - Show recent N pairs (default: 5)")
    else:
        trainer.interactive_training()


if __name__ == "__main__":
    main()
