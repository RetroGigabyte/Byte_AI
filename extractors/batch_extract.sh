#!/bin/bash

##############################################################################
# Batch URL Extraction Script
# Extract training data from multiple URLs in batch
##############################################################################

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
URLS_DIR="urls"
TRAINING_DIR="training"
METHOD="sentences"      # sentences, paragraphs, or full
MAX_LINES=100

##############################################################################
# Functions
##############################################################################

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

usage() {
    cat << EOF
Usage: bash batch_extract.sh [options]

Options:
    --help              Show this help message
    --urls-dir <dir>    Directory with .txt URL files (default: urls/)
    --output <dir>      Output directory (default: training/)
    --method <type>     sentences|paragraphs|full (default: sentences)
    --max-lines <num>   Max lines per URL (default: 100)
    --file <pattern>    Process only files matching pattern
    --dry-run           Show what would be processed without running

Examples:
    bash batch_extract.sh
    bash batch_extract.sh --method paragraphs
    bash batch_extract.sh --urls-dir url_lists/ --output training/
    bash batch_extract.sh --file tech --method full
    bash batch_extract.sh --dry-run

EOF
}

# Parse arguments
DRY_RUN=false
FILE_PATTERN=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            usage
            exit 0
            ;;
        --urls-dir)
            URLS_DIR="$2"
            shift 2
            ;;
        --output)
            TRAINING_DIR="$2"
            shift 2
            ;;
        --method)
            METHOD="$2"
            shift 2
            ;;
        --max-lines)
            MAX_LINES="$2"
            shift 2
            ;;
        --file)
            FILE_PATTERN="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

##############################################################################
# Main Script
##############################################################################

print_header "🌐 Batch URL Extraction"

# Check if urls directory exists
if [ ! -d "$URLS_DIR" ]; then
    print_error "URLs directory not found: $URLS_DIR"
    echo "Create URLs files in: $URLS_DIR/"
    echo "Example: $URLS_DIR/ai.txt"
    exit 1
fi

# Create output directory
mkdir -p "$TRAINING_DIR"

# Find all .txt files in urls directory
if [ -z "$FILE_PATTERN" ]; then
    URL_FILES=$(find "$URLS_DIR" -maxdepth 1 -name "*.txt" | sort)
else
    URL_FILES=$(find "$URLS_DIR" -maxdepth 1 -name "*${FILE_PATTERN}*.txt" | sort)
fi

# Count files
FILE_COUNT=$(echo "$URL_FILES" | grep -c . || echo 0)

if [ $FILE_COUNT -eq 0 ]; then
    print_error "No URL files found in $URLS_DIR/"
    exit 1
fi

print_info "Found $FILE_COUNT URL file(s) to process"
print_info "Method: $METHOD | Max lines: $MAX_LINES | Output: $TRAINING_DIR/"

# Show files in dry-run mode
if [ "$DRY_RUN" = true ]; then
    print_header "📋 Files to Process (Dry Run)"
    echo "$URL_FILES" | while read -r file; do
        if [ -f "$file" ]; then
            count=$(wc -l < "$file")
            echo "  • $(basename "$file") ($count URLs)"
        fi
    done
    exit 0
fi

# Process each URL file
print_header "⚙️  Processing Files"

TOTAL_FILES=0
PROCESSED_FILES=0
FAILED_FILES=0

echo "$URL_FILES" | while read -r url_file; do
    if [ ! -f "$url_file" ]; then
        continue
    fi

    TOTAL_FILES=$((TOTAL_FILES + 1))
    filename=$(basename "$url_file" .txt)

    print_info "Processing: $filename"

    # Extract category from filename
    category=$(echo "$filename" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_]/_/g')

    # Run url.py
    if python3 url.py --urls "$url_file" \
        --category "$category" \
        --method "$METHOD" \
        --output "$TRAINING_DIR" \
        --max-lines "$MAX_LINES" 2>/dev/null; then
        print_success "Completed: $filename → training/${category}_url.txt"
        PROCESSED_FILES=$((PROCESSED_FILES + 1))
    else
        print_error "Failed: $filename"
        FAILED_FILES=$((FAILED_FILES + 1))
    fi

    echo ""
done

# Summary
print_header "📊 Extraction Summary"

echo "Total files:       $FILE_COUNT"
echo "Successfully processed: $PROCESSED_FILES"
if [ $FAILED_FILES -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED_FILES${NC}"
fi

# Count output files
if [ -d "$TRAINING_DIR" ]; then
    OUTPUT_COUNT=$(find "$TRAINING_DIR" -name "*_url.txt" | wc -l)
    TOTAL_LINES=$(find "$TRAINING_DIR" -name "*_url.txt" -exec wc -l {} + | tail -1 | awk '{print $1}')
    TOTAL_SIZE=$(du -sh "$TRAINING_DIR" | cut -f1)

    echo ""
    echo "Output files:      $OUTPUT_COUNT"
    echo "Total lines:       $TOTAL_LINES"
    echo "Total size:        $TOTAL_SIZE"
fi

# Next steps
print_header "🚀 Next Steps"

if [ $PROCESSED_FILES -gt 0 ]; then
    echo "1. Load the bot:"
    echo "   ./knowledge_bot"
    echo ""
    echo "2. Query your new knowledge:"
    echo "   'What is machine learning?'"
    echo "   'Explain deep learning'"
    echo "   'Tell me about AI'"
else
    print_error "No files were successfully processed"
    exit 1
fi

echo ""
print_success "Batch extraction complete!"
