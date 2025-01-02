import os
import json
import re

# Function to process markdown cells
def fix_markdown_captions(cell):
    # Regex pattern to match and replace the image caption syntax
    pattern = r'!\[\]\((.*?) \"(.*?)\"\)'
    replacement = r'![\2](\1)'

    if cell.get("cell_type") == "markdown":
        updated_source = []
        for line in cell["source"]:
            updated_line = re.sub(pattern, replacement, line)
            updated_source.append(updated_line)
        cell["source"] = updated_source

# Iterate over all .ipynb files in the current directory
for file_name in os.listdir("."):
    if file_name.endswith(".ipynb"):
        print(f"Processing {file_name}...")
        
        # Read the notebook file
        with open(file_name, "r", encoding="utf-8") as f:
            notebook = json.load(f)

        # Check if the notebook has cells
        if "cells" in notebook:
            for cell in notebook["cells"]:
                fix_markdown_captions(cell)

        # Write the modified notebook back to the file
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Processing complete!")
