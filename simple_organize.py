import os
import re
from pathlib import Path

def clean_filename(name):
    name = re.sub(r'^\d+\.\s*', '', name)
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '_', name)
    return name.strip('_')

def parse_toc(content):
    toc_section = False
    parts = {}
    current_part = None
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if '# 目录' in line or '目录' in line:
            toc_section = True
            continue
            
        if toc_section and ('# 介绍' in line or line.startswith('# ')):
            if '介绍' not in line:
                break
            
        if toc_section:
            if line.startswith('**') and line.endswith('**'):
                current_part = line.strip('*').strip()
                parts[current_part] = {}
                continue
                
            if re.match(r'^\d+\.\s+.+\s+\d+$', line):
                if current_part:
                    match = re.match(r'^(\d+\.\s+.+?)\s+(\d+)$', line)
                    if match:
                        chapter_name = match.group(1).strip()
                        page_num = int(match.group(2))
                        parts[current_part][chapter_name] = page_num
    
    return parts

# Read the file
with open('../9years/Learn to Think Basic exercises in the core thinking skills for ages 6–11.zh-CN.2k.high.9years.md', 'r', encoding='utf-8') as f:
    content = f.read()

parts = parse_toc(content)

print('Found structure:')
for part_name, chapters in parts.items():
    print(f'\n📁 {part_name}')
    for chapter_name, page_num in chapters.items():
        print(f'  📄 {chapter_name} (Page {page_num})')

# Create folders
output_path = Path('organized_content')
output_path.mkdir(exist_ok=True)

for part_name, chapters in parts.items():
    part_folder = output_path / clean_filename(part_name)
    part_folder.mkdir(exist_ok=True)
    
    # Create part README
    part_index = f"# {part_name}\n\n这一部分包含以下章节：\n\n"
    
    for chapter_name, page_num in chapters.items():
        chapter_folder = part_folder / clean_filename(chapter_name)
        chapter_folder.mkdir(exist_ok=True)
        
        part_index += f"- [{chapter_name}](./{clean_filename(chapter_name)}/README.md) (第 {page_num} 页)\n"
        
        # Create chapter README
        chapter_readme = f"# {chapter_name}\n\n**页码：** {page_num}\n\n**所属部分：** {part_name}\n\n## 内容\n\n<!-- 章节内容将在这里显示 -->\n"
        
        with open(chapter_folder / "README.md", 'w', encoding='utf-8') as f:
            f.write(chapter_readme)
    
    with open(part_folder / "README.md", 'w', encoding='utf-8') as f:
        f.write(part_index)

# Create main index
main_index = "# 学会思考 - 核心思考能力练习\n\n这个项目包含了按照目录结构组织的各个部分和章节。\n\n## 目录结构\n\n"

for part_name, chapters in parts.items():
    main_index += f"### [{part_name}](./{clean_filename(part_name)}/README.md)\n\n"
    for chapter_name, page_num in chapters.items():
        main_index += f"- [{chapter_name}](./{clean_filename(part_name)}/{clean_filename(chapter_name)}/README.md) (第 {page_num} 页)\n"
    main_index += "\n"

with open(output_path / "README.md", 'w', encoding='utf-8') as f:
    f.write(main_index)

print(f'\n✅ 组织完成！输出目录：organized_content')
print(f'📁 创建了 {len(parts)} 个部分文件夹')
total_chapters = sum(len(chapters) for chapters in parts.values())
print(f'📄 创建了 {total_chapters} 个章节文件夹') 