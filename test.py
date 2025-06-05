import re

# Test lines from the TOC
test_lines = [
    "**组织性思维（整理信息）&#x20;**",
    "1\\. 观察特征 5&#x20;",
    "2\\. 观察相似点 8&#x20;", 
    "**分析思维**&#x20;",
    "10\\. 分析关系 41&#x20;"
]

for line in test_lines:
    print(f"Testing: '{line}'")
    
    # Check for part headers
    if line.startswith('**') and ('**' in line[2:]):
        current_part = re.sub(r'\*\*|&#x20;', '', line).strip()
        print(f"  -> PART: '{current_part}'")
        continue
        
    # Check for chapters
    pattern = r'^(\d+\\?\.\s+.+?)\s+(\d+)(?:\s*&#x20;)?$'
    match = re.match(pattern, line)
    if match:
        chapter_name = match.group(1).strip()
        page_num = int(match.group(2))
        print(f"  -> CHAPTER: '{chapter_name}' -> Page {page_num}")
    else:
        print(f"  -> NO MATCH")
    print() 