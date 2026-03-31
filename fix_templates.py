import os
import glob

files_fixed = 0
for filepath in glob.glob('templates/**/*.html', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.replace('{% extends"base.html" %}', '{% extends "base.html" %}')
    new_content = new_content.replace('{% include"partials/_pagination.html" %}', '{% include "partials/_pagination.html" %}')
    new_content = new_content.replace('{% url"', '{% url "')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed syntax errors in {filepath}")
        files_fixed += 1

print(f"Done. Fixed {files_fixed} files.")
