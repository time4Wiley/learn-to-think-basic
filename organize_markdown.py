#!/usr/bin/env python3
"""
Markdown Organizer Script
Divides the markdown file into parts and chapters based on the Table of Contents.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

def clean_filename(name: str) -> str:
    """Clean filename by removing special characters and replacing spaces with underscores."""
    # Remove numbering prefix like "1. " or "10. "
    name = re.sub(r'^\d+\.\s*', '', name)
    # Replace special characters with underscores
    name = re.sub(r'[^\w\s-]', '', name)
    # Replace spaces with underscores
    name = re.sub(r'\s+', '_', name)
    return name.strip('_')

def parse_toc(content: str) -> Dict[str, Dict[str, int]]:
    """Parse the table of contents and extract parts and chapters with page numbers."""
    toc_section = False
    parts = {}
    current_part = None
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Look for TOC start
        if '# 目录' in line or '目录' in line:
            toc_section = True
            continue
            
        # Stop at the introduction section
        if toc_section and ('# 介绍' in line or line.startswith('# ')):
            if '介绍' not in line:
                break
            
        if toc_section:
            # Check for part headers (bold text with **)
            if line.startswith('**') and line.endswith('**'):
                current_part = line.strip('*').strip()
                parts[current_part] = {}
                continue
                
            # Check for chapter entries
            if re.match(r'^\d+\.\s+.+\s+\d+$', line):
                if current_part:
                    # Extract chapter name and page number
                    match = re.match(r'^(\d+\.\s+.+?)\s+(\d+)$', line)
                    if match:
                        chapter_name = match.group(1).strip()
                        page_num = int(match.group(2))
                        parts[current_part][chapter_name] = page_num
    
    return parts

def find_page_markers(content: str) -> List[Tuple[int, int]]:
    """Find page break markers in the content and return their line positions."""
    lines = content.split('\n')
    page_markers = []
    
    for i, line in enumerate(lines):
        # Look for page markers - you might need to adjust this pattern
        if re.search(r'^\s*\d+\s*$', line.strip()) or '---' in line:
            page_markers.append((i, int(line.strip()) if line.strip().isdigit() else 0))
    
    return page_markers

def extract_content_by_page(content: str, start_page: int, end_page: int) -> str:
    """Extract content between specified page numbers."""
    lines = content.split('\n')
    start_idx = 0
    end_idx = len(lines)
    
    # This is a simplified approach - you might need to adjust based on actual page markers
    # For now, we'll use a simple heuristic based on content structure
    
    return '\n'.join(lines[start_idx:end_idx])

def create_folder_structure(parts: Dict[str, Dict[str, int]], output_dir: str):
    """Create the folder structure for parts and chapters."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for part_name in parts.keys():
        part_folder = output_path / clean_filename(part_name)
        part_folder.mkdir(exist_ok=True)
        
        for chapter_name in parts[part_name].keys():
            chapter_folder = part_folder / clean_filename(chapter_name)
            chapter_folder.mkdir(exist_ok=True)

def organize_markdown(input_file: str, output_dir: str = "organized_content"):
    """Main function to organize the markdown content."""
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the table of contents
    parts = parse_toc(content)
    
    print("Found the following structure:")
    for part_name, chapters in parts.items():
        print(f"\n📁 {part_name}")
        for chapter_name, page_num in chapters.items():
            print(f"  📄 {chapter_name} (Page {page_num})")
    
    # Create folder structure
    create_folder_structure(parts, output_dir)
    
    # For now, let's create index files for each part and chapter
    output_path = Path(output_dir)
    
    for part_name, chapters in parts.items():
        part_folder = output_path / clean_filename(part_name)
        
        # Create part index
        part_index = f"# {part_name}\n\n"
        part_index += f"这一部分包含以下章节：\n\n"
        
        for chapter_name, page_num in chapters.items():
            chapter_folder = part_folder / clean_filename(chapter_name)
            part_index += f"- [{chapter_name}](./{clean_filename(chapter_name)}/README.md) (第 {page_num} 页)\n"
            
            # Create chapter README
            chapter_readme = f"# {chapter_name}\n\n"
            chapter_readme += f"**页码：** {page_num}\n\n"
            chapter_readme += f"**所属部分：** {part_name}\n\n"
            chapter_readme += "## 内容\n\n"
            chapter_readme += "<!-- 章节内容将在这里显示 -->\n"
            
            with open(chapter_folder / "README.md", 'w', encoding='utf-8') as f:
                f.write(chapter_readme)
        
        with open(part_folder / "README.md", 'w', encoding='utf-8') as f:
            f.write(part_index)
    
    # Create main index
    main_index = "# 学会思考 - 核心思考能力练习\n\n"
    main_index += "这个项目包含了按照目录结构组织的各个部分和章节。\n\n"
    main_index += "## 目录结构\n\n"
    
    for part_name, chapters in parts.items():
        main_index += f"### [{part_name}](./{clean_filename(part_name)}/README.md)\n\n"
        for chapter_name, page_num in chapters.items():
            main_index += f"- [{chapter_name}](./{clean_filename(part_name)}/{clean_filename(chapter_name)}/README.md) (第 {page_num} 页)\n"
        main_index += "\n"
    
    with open(output_path / "README.md", 'w', encoding='utf-8') as f:
        f.write(main_index)
    
    print(f"\n✅ 组织完成！输出目录：{output_dir}")
    print(f"📁 创建了 {len(parts)} 个部分文件夹")
    total_chapters = sum(len(chapters) for chapters in parts.values())
    print(f"📄 创建了 {total_chapters} 个章节文件夹")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python organize_markdown.py <输入文件路径> [输出目录]")
        print("示例: python organize_markdown.py '../9years/Learn to Think Basic exercises in the core thinking skills for ages 6–11.zh-CN.2k.high.9years.md'")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "organized_content"
    
    if not os.path.exists(input_file):
        print(f"错误：找不到文件 {input_file}")
        sys.exit(1)
    
    organize_markdown(input_file, output_dir) 