import os
import re
from pathlib import Path

def clean_filename(name):
    name = re.sub(r'^\d+\\.?\s*', '', name)  # Handle both 1. and 1\.
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '_', name)
    return name.strip('_')

def parse_toc(content):
    parts = {
        "组织性思维（整理信息）": {
            "1\\. 观察特征": 5,
            "2\\. 观察相似点": 8,
            "3\\. 观察不同点": 11,
            "4\\. 分类": 14,
            "5\\. 比较": 17,
            "6\\. 按大小和时间排序": 20,
            "7\\. 思考概念": 26,
            "8\\. 概括": 29,
            "9\\. 概念图": 33
        },
        "分析思维": {
            "10\\. 分析关系": 41,
            "11\\. 分析序列模式": 44
        },
        "评价性思维": {
            "12\\. 区分事实和观点": 49,
            "13\\. 区分肯定和不肯定的结论": 52,
            "14\\. 挑战说法的可靠性": 56,
            "15\\. 区分相关和无关信息": 60,
            "16\\. 决策": 64,
            "17\\. 考虑其他观点": 70,
            "18\\. 提出更好的问题": 73
        },
        "创造性思维": {
            "19\\. 创造性后果": 78,
            "20\\. 逆向创造性思考": 81,
            "21\\. 分析设计的创造性": 84,
            "22\\. 随机物体的创造力": 88,
            "23\\. 视觉创造力": 91,
            "24\\. 关于用途的创造性思考": 93
        }
    }
    return parts

# Read the file
input_file = '../9years/Learn to Think Basic exercises in the core thinking skills for ages 6–11.zh-CN.2k.high.9years.md'
with open(input_file, 'r', encoding='utf-8') as f:
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