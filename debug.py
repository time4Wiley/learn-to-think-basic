import re

# Read the file
input_file = '../9years/Learn to Think Basic exercises in the core thinking skills for ages 6–11.zh-CN.2k.high.9years.md'
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
toc_section = False
found_lines = []

for i, line in enumerate(lines):
    line_stripped = line.strip()
    
    if '# 目录' in line_stripped or line_stripped == '目录':
        toc_section = True
        print(f"Found TOC start at line {i}: '{line_stripped}'")
        continue
        
    if toc_section and line_stripped.startswith('# 介绍'):
        print(f"Found TOC end at line {i}: '{line_stripped}'")
        break
        
    if toc_section:
        print(f"Line {i}: '{line_stripped}'")
        found_lines.append(line_stripped)

print(f"\nTotal TOC lines found: {len(found_lines)}")

# Test the regex patterns
for line in found_lines:
    if line.startswith('**') and line.endswith('**'):
        print(f"PART: {line}")
    elif re.match(r'^\d+\\?\.\s+.+\s+\d+', line):
        pattern = r'^(\d+\\?\.\s+[^0-9]+?)\s+(\d+)(?:&#x20;)?$'
        match = re.match(pattern, line)
        if match:
            print(f"CHAPTER: '{match.group(1)}' -> Page {match.group(2)}")
        else:
            print(f"FAILED MATCH: '{line}'")
    else:
        print(f"OTHER: '{line}'") 