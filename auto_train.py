#!/usr/bin/env python3
"""
Auto-Train Pipeline
Automatically processes collected Q&A pairs and improves training data
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from training_mode import TrainingMode


class AutoTrainPipeline:
    """Automatically train from collected Q&A pairs"""

    def __init__(self, training_dir="training"):
        self.training_dir = training_dir
        self.qa_dir = os.path.join(training_dir, "qa_training")
        self.backup_dir = os.path.join(training_dir, "backups")
        self.processed_dir = os.path.join(self.qa_dir, "processed")

        self.create_directories()

    def create_directories(self):
        """Create necessary directories"""
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
        Path(self.processed_dir).mkdir(parents=True, exist_ok=True)

    def backup_training_data(self):
        """Create backup of training data before auto-train"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}.zip"
        backup_path = os.path.join(self.backup_dir, backup_name)

        print(f"💾 Backing up training data...")

        try:
            # Zip all training files (excluding processed)
            os.system(f"cd {self.training_dir} && zip -q -r {backup_name} *.zip *.txt 2>/dev/null")
            os.system(f"mv {self.training_dir}/{backup_name} {backup_path}")
            print(f"✓ Backup created: {backup_name}")
            return True
        except Exception as e:
            print(f"⚠️  Backup warning: {e}")
            return False

    def process_qa_pairs(self):
        """Process collected Q&A pairs"""
        json_file = os.path.join(self.qa_dir, "qa_pairs.jsonl")

        if not os.path.exists(json_file):
            print("⚠️  No Q&A pairs to process")
            return 0

        print("\n🔄 Processing Q&A pairs...")

        processed_count = 0
        category_stats = {}

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        category = data.get("category", "custom")
                        question = data.get("question", "")
                        answer = data.get("answer", "")

                        if question and answer:
                            # Save to training file
                            training_file = os.path.join(self.training_dir, f"{category}_trained.txt")

                            # Format: category: content
                            entry = f"{category}: {question} -> {answer}\n"

                            with open(training_file, 'a', encoding='utf-8') as tf:
                                tf.write(entry)

                            processed_count += 1
                            category_stats[category] = category_stats.get(category, 0) + 1

            # Save processed marker
            processed_file = os.path.join(self.processed_dir, f"processed_{datetime.now().isoformat()}.json")
            with open(processed_file, 'w') as f:
                json.dump({"count": processed_count, "stats": category_stats}, f)

            print(f"✓ Processed {processed_count} Q&A pairs")

            # Show stats
            for category, count in sorted(category_stats.items()):
                print(f"  • {category}: {count} pairs")

            return processed_count

        except Exception as e:
            print(f"❌ Error processing: {e}")
            return 0

    def generate_training_summary(self):
        """Generate summary of training improvements"""
        json_file = os.path.join(self.qa_dir, "qa_pairs.jsonl")

        if not os.path.exists(json_file):
            return None

        print("\n📊 Training Summary")

        try:
            trainer = TrainingMode(self.training_dir)
            stats = trainer.get_qa_stats()

            print(f"  Total Q&A pairs collected: {stats['total_pairs']}")

            if stats['by_category']:
                print("\n  Categories improved:")
                for category, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True):
                    print(f"    • {category}: {count} new examples")

            return stats

        except Exception as e:
            print(f"⚠️  Summary error: {e}")
            return None

    def create_new_zip(self):
        """Create new zip file with trained data"""
        print("\n📦 Creating new training zip...")

        try:
            # Remove old training_data.zip if it exists
            old_zip = os.path.join(self.training_dir, "training_data_old.zip")
            current_zip = os.path.join(self.training_dir, "training_data.zip")

            if os.path.exists(current_zip):
                shutil.move(current_zip, old_zip)
                print("  ✓ Old zip archived")

            # Create new zip with trained files
            os.system(f"cd {self.training_dir} && zip -q training_data.zip *_trained.txt 2>/dev/null")
            print("✓ New training zip created")

            return True

        except Exception as e:
            print(f"⚠️  Zip creation warning: {e}")
            return False

    def run_full_pipeline(self, create_zip=True):
        """Run complete auto-train pipeline"""
        print("\n" + "="*60)
        print("🤖 AUTO-TRAIN PIPELINE")
        print("="*60)

        # Step 1: Backup
        self.backup_training_data()

        # Step 2: Process Q&A pairs
        processed = self.process_qa_pairs()

        if processed == 0:
            print("\n✓ No new training data to process")
            return False

        # Step 3: Generate summary
        self.generate_training_summary()

        # Step 4: Create new zip
        if create_zip:
            self.create_new_zip()

        print("\n" + "="*60)
        print("✅ AUTO-TRAIN PIPELINE COMPLETE")
        print("="*60)
        print("\n🚀 Next step: Recompile and test bot")
        print("   g++ -std=c++17 knowledge_bot.cpp -o knowledge_bot")
        print("   ./knowledge_bot")

        return True

    def recompile_bot(self):
        """Recompile bot with new training data"""
        print("\n🔧 Recompiling bot...")

        try:
            result = os.system("g++ -std=c++17 knowledge_bot.cpp -o knowledge_bot 2>&1")

            if result == 0:
                print("✅ Bot compiled successfully!")
                return True
            else:
                print("❌ Compilation failed")
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def schedule_auto_train(self, interval_hours=24):
        """Create a cron job for automatic training"""
        print(f"\n⏰ Scheduling auto-train every {interval_hours} hours...")

        cron_cmd = f"0 */{interval_hours} * * * cd /Users/Apple/Documents/dev/chatbot && python3 auto_train.py run"

        print(f"Add this to crontab:")
        print(f"  crontab -e")
        print(f"  {cron_cmd}")


def main():
    """Main entry point"""
    import sys

    pipeline = AutoTrainPipeline()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "run":
            # Full pipeline
            pipeline.run_full_pipeline(create_zip=True)
        elif command == "process":
            # Just process Q&A pairs
            pipeline.process_qa_pairs()
        elif command == "summary":
            # Show summary only
            pipeline.generate_training_summary()
        elif command == "backup":
            # Backup only
            pipeline.backup_training_data()
        elif command == "compile":
            # Compile bot
            pipeline.recompile_bot()
        elif command == "schedule":
            hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
            pipeline.schedule_auto_train(hours)
        else:
            print("Usage: python3 auto_train.py [command]")
            print("\nCommands:")
            print("  run              - Run full pipeline")
            print("  process          - Process Q&A pairs only")
            print("  summary          - Show summary")
            print("  backup           - Backup training data")
            print("  compile          - Compile bot")
            print("  schedule [HOURS] - Schedule auto-train (default: 24)")
    else:
        # Default: full pipeline
        pipeline.run_full_pipeline()


if __name__ == "__main__":
    main()
