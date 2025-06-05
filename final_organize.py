#!/usr/bin/env python3

import os
import re
from pathlib import Path

def clean_filename(name):
    """Clean filename by removing numbering and special characters"""
    name = re.sub(r'^\d+\.\s*', '', name)
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '_', name)
    return name.strip('_')

def main():
    # TOC structure from the markdown file
    parts = {
        "组织性思维_整理信息": {
            "1_观察特征": 5,
            "2_观察相似点": 8,
            "3_观察不同点": 11,
            "4_分类": 14,
            "5_比较": 17,
            "6_按大小和时间排序": 20,
            "7_思考概念": 26,
            "8_概括": 29,
            "9_概念图": 33
        },
        "分析思维": {
            "10_分析关系": 41,
            "11_分析序列模式": 44
        },
        "评价性思维": {
            "12_区分事实和观点": 49,
            "13_区分肯定和不肯定的结论": 52,
            "14_挑战说法的可靠性": 56,
            "15_区分相关和无关信息": 60,
            "16_决策": 64,
            "17_考虑其他观点": 70,
            "18_提出更好的问题": 73
        },
        "创造性思维": {
            "19_创造性后果": 78,
            "20_逆向创造性思考": 81,
            "21_分析设计的创造性": 84,
            "22_随机物体的创造力": 88,
            "23_视觉创造力": 91,
            "24_关于用途的创造性思考": 93
        }
    }

    print('📚 学会思考 - 组织markdown内容')
    print('=' * 50)
    
    print('\n发现以下结构:')
    for part_name, chapters in parts.items():
        print(f'\n📁 {part_name}')
        for chapter_name, page_num in chapters.items():
            print(f'  📄 {chapter_name} (第 {page_num} 页)')

    # Create the organized content directory
    output_path = Path('organized_content')
    if output_path.exists():
        import shutil
        shutil.rmtree(output_path)
    output_path.mkdir()

    # Create folder structure
    for part_name, chapters in parts.items():
        part_folder = output_path / part_name
        part_folder.mkdir(exist_ok=True)
        
        # Create part README
        part_index = f"# {part_name}\n\n"
        part_index += "这一部分包含以下章节:\n\n"
        
        for chapter_name, page_num in chapters.items():
            chapter_folder = part_folder / chapter_name
            chapter_folder.mkdir(exist_ok=True)
            
            # Add to part index
            part_index += f"- [{chapter_name}](./{chapter_name}/README.md) (第 {page_num} 页)\n"
            
            # Create chapter README
            chapter_readme = f"# {chapter_name}\n\n"
            chapter_readme += f"**页码:** {page_num}\n\n"
            chapter_readme += f"**所属部分:** {part_name}\n\n"
            chapter_readme += "## 内容\n\n"
            chapter_readme += "<!-- 这里将显示章节的具体内容 -->\n\n"
            chapter_readme += "## 练习\n\n"
            chapter_readme += "<!-- 这里将显示相关的练习题 -->\n"
            
            # Write chapter README
            with open(chapter_folder / "README.md", 'w', encoding='utf-8') as f:
                f.write(chapter_readme)
        
        # Write part README
        with open(part_folder / "README.md", 'w', encoding='utf-8') as f:
            f.write(part_index)

    # Create main index
    main_index = "# 学会思考 - 核心思考能力练习\n\n"
    main_index += "本项目包含了按照目录结构组织的各个部分和章节。\n\n"
    main_index += "## 📖 目录结构\n\n"

    for part_name, chapters in parts.items():
        main_index += f"### 📁 [{part_name}](./{part_name}/README.md)\n\n"
        for chapter_name, page_num in chapters.items():
            main_index += f"- 📄 [{chapter_name}](./{part_name}/{chapter_name}/README.md) (第 {page_num} 页)\n"
        main_index += "\n"

    main_index += "## 🚀 使用方法\n\n"
    main_index += "1. 浏览各个部分的文件夹\n"
    main_index += "2. 每个章节都有独立的README文件\n"
    main_index += "3. 可以在章节README中添加具体的学习内容和练习\n\n"
    main_index += "## 📝 原始文件\n\n"
    main_index += "原始内容来自: `Learn to Think Basic exercises in the core thinking skills for ages 6–11.zh-CN.2k.high.9years.md`\n"

    # Write main README
    with open(output_path / "README.md", 'w', encoding='utf-8') as f:
        f.write(main_index)

    print(f'\n✅ 组织完成!')
    print(f'📁 创建了 {len(parts)} 个部分文件夹')
    total_chapters = sum(len(chapters) for chapters in parts.values())
    print(f'📄 创建了 {total_chapters} 个章节文件夹')
    print(f'📂 输出目录: {output_path.absolute()}')

if __name__ == "__main__":
    main() 