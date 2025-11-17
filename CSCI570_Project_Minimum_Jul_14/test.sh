#!/bin/bash

BASE_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

INPUT_DIR="$BASE_DIR/Generated_strings"
OUTPUT_DIR="$BASE_DIR/Outputs"

mkdir -p "$OUTPUT_DIR"

echo "Running all generated string files..."

for INPUT_FILE in "$INPUT_DIR"/*.txt
do
    FILENAME=$(basename "$INPUT_FILE")
    OUTPUT_FILE="$OUTPUT_DIR/${FILENAME/.txt/_out.txt}"

    echo "Processing $FILENAME -> $(basename "$OUTPUT_FILE")"

    python3 "$BASE_DIR/basic.py" "$INPUT_FILE" "$OUTPUT_FILE"
done

echo "Done."
