import glob
import json
import re
import os

lua_word_pattern = re.compile(r'(?i)(?<![a-zA-Z])lua(?![a-zA-Z])')

matched_files = []

for file_path in glob.glob('**/*.json', recursive=True):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            descriptions = data.get('descriptions', [])
            for item in descriptions:
                if item.get('lang') == 'en':
                    value = item.get('value', '')
                    if lua_word_pattern.search(value):
                        matched_files.append(file_path)
                        break 
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

print(f"Total matched files: {len(matched_files)}")

with open("cve-results.json", "w") as f:
    json.dump(matched_files, f, indent=4)

