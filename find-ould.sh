#!/usr/bin/env bash
set -euo pipefail

# Pattern to search (case-insensitive whole words)
PATTERN='should|would|could'

# Usage check
if [ $# -lt 1 ]; then
  echo "Usage: $0 <file>"
  exit 1
fi

FILE="$1"

# Validate file
if [ ! -f "$FILE" ]; then
  echo "Error: '$FILE' does not exist or is not a regular file."
  exit 2
fi

# 1) Show matching lines with line numbers and highlighting
grep -nEiw --color=always --binary-files=without-match "$PATTERN" "$FILE" || true

# 2) Count total matches (each occurrence, not just lines)
match_count=$(grep -Eiw -o --binary-files=without-match "$PATTERN" "$FILE" | wc -l | awk '{print $1}')

# 3) Print the count in the requested format
echo "ould-count: ${match_count}"