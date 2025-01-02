import os
import json
import re

# Function to process markdown cells
def fix_links_and_lowercase(cell):
    # Regex pattern to match links in old and new formats
    patterns = [
        (r'\[(.*?)\]\(https://ducha-aiki\.github\.io/wide-baseline-stereo-blog/'
         r'(\d{4})/(\d{2})/(\d{2})/(.*?)\.html\)',
         r'[\1](https://ducha-aiki.github.io/wide-baseline-stereo-blog/posts/\2-\3-\4-\5.html)'),
        (r'\[(.*?)\]\(https://ducha-aiki\.github\.io/wide-baseline-stereo-blog/posts/'
         r'(\d{4})-(\d{2})-(\d{2})-(.*?)\.html\)',
         r'[\1](https://ducha-aiki.github.io/wide-baseline-stereo-blog/posts/\2-\3-\4-\5.html)')
    ]

    if cell.get("cell_type") == "markdown":
        updated_source = []
        for line in cell["source"]:
            # Apply each pattern
            for pattern, replacement in patterns:
                line = re.sub(pattern, replacement, line)
            # Make the URLs lowercase
            line = re.sub(r'(https://ducha-aiki\.github\.io/wide-baseline-stereo-blog/posts/.*?)', lambda m: m.group(1).lower(), line)
            updated_source.append(line)
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
                fix_links_and_lowercase(cell)

        # Write the modified notebook back to the file
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Processing complete!")
