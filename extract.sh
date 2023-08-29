#!/bin/bash

# Set the paths to your input JSON file and desired output TSV file
input_path="/path/to/your/input.json"
output_path="/path/to/your/output.tsv"

# Run the Python script
python extract_annotations.py --input_path "$input_path" --output_path "$output_path"
