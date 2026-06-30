#!/usr/bin/env python3
"""
PDF Training Data Extractor
Extracts text from PDF files and converts to training format
"""

import os
import sys
import json
import re
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("⚠️  PyPDF2 not installed. Install with: pip install PyPDF2")
    print("   Attempting to work with available libraries...")

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file"""
    try:
        import PyPDF2
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            print(f"   📄 Pages: {len(reader.pages)}")
            for page_num, page in enumerate(reader.pages):
                text += page.extract_text()
                if (page_num + 1) % 10 == 0:
                    print(f"   ✓ Processed {page_num + 1} pages...")
        return text
    except ImportError:
        print("   ❌ PyPDF2 required. Install with: pip install PyPDF2")
        return None
    except Exception as e:
        print(f"   ❌ Error reading {pdf_path}: {e}")
        return None

def split_into_sentences(text):
    """Split text into sentences"""
    # Split on periods, exclamation marks, question marks
    sentences = re.split(r'[.!?]+', text)
    # Clean up and filter empty sentences
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    return sentences

def split_into_paragraphs(text):
    """Split text into paragraphs"""
    paragraphs = text.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 20]
    return paragraphs

def extract_category_from_filename(filename):
    """Extract category from PDF filename"""
    # Remove .pdf extension
    name = filename.replace('.pdf', '')
    # Replace spaces and hyphens with underscores
    category = name.lower().replace(' ', '_').replace('-', '_')
    # Remove special characters
    category = re.sub(r'[^a-z0-9_]', '', category)
    return category

def extract_key_terms(text, num_terms=20):
    """Extract key terms from text"""
    # Split into words
    words = text.lower().split()
    # Filter common words
    common_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'have', 'has', 'do', 'does', 'did', 'that', 'this', 'these', 'those',
        'it', 'its', 'which', 'who', 'what', 'when', 'where', 'why', 'how'
    }

    # Count non-common words
    word_counts = {}
    for word in words:
        # Remove punctuation
        word = re.sub(r'[^a-z0-9]', '', word)
        if len(word) > 3 and word not in common_words:
            word_counts[word] = word_counts.get(word, 0) + 1

    # Sort by frequency
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:num_terms]]

def create_training_format(text, category, method='sentences', max_lines=100):
    """Convert text to training format"""
    print(f"   🔄 Converting to training format ({method})...")

    lines = []

    if method == 'sentences':
        segments = split_into_sentences(text)
    elif method == 'paragraphs':
        segments = split_into_paragraphs(text)
    else:
        segments = [text]

    # Limit to avoid huge files
    segments = segments[:max_lines]

    # Create training lines
    for segment in segments:
        if len(segment.strip()) > 10:
            # Format: category: content
            line = f"{category}: {segment}"
            lines.append(line)

    return lines

def process_pdf(pdf_path, category=None, method='sentences', output_dir='training'):
    """Process a single PDF file"""
    pdf_name = os.path.basename(pdf_path)
    print(f"\n📖 Processing: {pdf_name}")

    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"   ❌ File not found: {pdf_path}")
        return None

    # Extract text
    print(f"   📖 Extracting text...")
    text = extract_text_from_pdf(pdf_path)

    if not text:
        print(f"   ❌ Failed to extract text")
        return None

    print(f"   ✓ Extracted {len(text)} characters")

    # Get category
    if not category:
        category = extract_category_from_filename(pdf_name)

    print(f"   📂 Category: {category}")

    # Convert to training format
    lines = create_training_format(text, category, method)

    print(f"   ✓ Created {len(lines)} training lines")

    # Save to file
    output_file = os.path.join(output_dir, f"{category}_pdf.txt")

    print(f"   💾 Saving to {output_file}...")

    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

    print(f"   ✅ Saved {len(lines)} lines")

    return {
        'file': output_file,
        'category': category,
        'lines': len(lines),
        'characters': len(text)
    }

def process_directory(pdf_dir, output_dir='training', method='sentences'):
    """Process all PDF files in a directory"""
    print(f"\n{'='*60}")
    print(f"📚 PDF Training Data Extractor")
    print(f"{'='*60}\n")

    if not os.path.isdir(pdf_dir):
        print(f"❌ Directory not found: {pdf_dir}")
        return

    # Find all PDF files
    pdf_files = list(Path(pdf_dir).rglob('*.pdf'))

    if not pdf_files:
        print(f"❌ No PDF files found in {pdf_dir}")
        return

    print(f"📖 Found {len(pdf_files)} PDF file(s)\n")

    results = []

    for pdf_path in pdf_files:
        result = process_pdf(str(pdf_path), method=method, output_dir=output_dir)
        if result:
            results.append(result)

    # Print summary
    print(f"\n{'='*60}")
    print(f"✅ Processing Complete!")
    print(f"{'='*60}\n")

    if results:
        total_lines = sum(r['lines'] for r in results)
        total_chars = sum(r['characters'] for r in results)

        print("📊 Summary:")
        for result in results:
            print(f"  ✓ {os.path.basename(result['file'])}")
            print(f"    Lines: {result['lines']:,}")
            print(f"    Size: {result['characters']:,} chars")

        print(f"\n📈 Totals:")
        print(f"  Files: {len(results)}")
        print(f"  Lines: {total_lines:,}")
        print(f"  Characters: {total_chars:,}")
        print(f"  Output: {output_dir}/")

        print(f"\n🚀 Next step: Run './knowledge_bot' to load training data!")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 pdf.py <pdf_file_or_directory> [options]")
        print("\nOptions:")
        print("  --category <name>   Override category name")
        print("  --method <type>     sentences|paragraphs|full (default: sentences)")
        print("  --output <dir>      Output directory (default: training)")
        print("\nExamples:")
        print("  python3 pdf.py mybook.pdf")
        print("  python3 pdf.py ./pdfs/")
        print("  python3 pdf.py book.pdf --category history --method paragraphs")
        return

    pdf_path = sys.argv[1]
    category = None
    method = 'sentences'
    output_dir = 'training'

    # Parse options
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == '--category' and i + 1 < len(sys.argv):
            category = sys.argv[i + 1]
        elif sys.argv[i] == '--method' and i + 1 < len(sys.argv):
            method = sys.argv[i + 1]
        elif sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]

    # Process PDF(s)
    if os.path.isdir(pdf_path):
        process_directory(pdf_path, output_dir, method)
    else:
        result = process_pdf(pdf_path, category, method, output_dir)
        if result:
            print(f"\n✅ Successfully processed: {result['file']}")
            print(f"   Category: {result['category']}")
            print(f"   Lines: {result['lines']:,}")

if __name__ == '__main__':
    main()
