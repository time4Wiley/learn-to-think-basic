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

def get_chapter_mapping():
    """Define the mapping from original chapter titles to folder names"""
    return {
        "观察事物的特点": ("organize_thinking", "1_observe_features"),
        "观察相似点": ("organize_thinking", "2_observe_similarities"),
        "观察差异": ("organize_thinking", "3_observe_differences"),
        "分类（归类相似）": ("organize_thinking", "4_classification"),
        "比较": ("organize_thinking", "5_comparison"),
        "按大小和时间排序": ("organize_thinking", "6_sorting_by_size_time"),
        "思考概念": ("organize_thinking", "7_thinking_concepts"),
        "概括": ("organize_thinking", "8_generalization"),
        "概念图": ("organize_thinking", "9_concept_maps"),
        "分析关系": ("analytical_thinking", "10_analyze_relationships"),
        "分析序列中的规律": ("analytical_thinking", "11_analyze_sequence_patterns"),
        "分清事实和观点": ("evaluative_thinking", "12_distinguish_facts_opinions"),
        "区分确定性结论和不确定性结论": ("evaluative_thinking", "13_distinguish_certain_uncertain"),
        "挑战主张的可信度": ("evaluative_thinking", "14_challenge_reliability"),
        "区分相关和不相关信息": ("evaluative_thinking", "15_distinguish_relevant_irrelevant"),
        "做决定": ("evaluative_thinking", "16_decision_making"),
        "考虑别人的观点": ("evaluative_thinking", "17_consider_other_viewpoints"),
        "提问让思考更好": ("evaluative_thinking", "18_better_questions"),
        "创造性后果": ("creative_thinking", "19_creative_consequences"),
        "反向创意思维": ("creative_thinking", "20_reverse_creative_thinking"),
        "分析设计中的创造力": ("creative_thinking", "21_analyze_creative_design"),
        "随机物体的创造力": ("creative_thinking", "22_random_object_creativity"),
        "视觉创意": ("creative_thinking", "23_visual_creativity"),
        "关于用途的创意思考": ("creative_thinking", "24_creative_thinking_about_uses")
    }

def split_markdown_content(source_file):
    """Split the markdown content into chapters"""
    
    # Check if source file exists
    if not Path(source_file).exists():
        print(f"❌ Source file not found: {source_file}")
        return False
    
    # Read the source file
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get chapter mapping
    chapter_mapping = get_chapter_mapping()
    
    # Define the main parts structure for folder mapping
    part_mapping = {
        "organize_thinking": "organize_thinking",
        "analytical_thinking": "analytical_thinking", 
        "evaluative_thinking": "evaluative_thinking",
        "creative_thinking": "creative_thinking"
    }
    
    # Create organized_content directory if it doesn't exist
    output_base = Path("organized_content")
    
    # Create the missing part directories if they don't exist
    for part_dir in part_mapping.values():
        part_path = output_base / part_dir
        part_path.mkdir(parents=True, exist_ok=True)
    
    # Create missing directories for creative and evaluative thinking
    (output_base / "creative_thinking").mkdir(exist_ok=True)
    (output_base / "evaluative_thinking").mkdir(exist_ok=True)
    
    # Split content by main headers (level 1 headings starting with #)
    chapters = re.split(r'\n(?=# [^#])', content)
    
    # Process the introduction separately (first part before any # headers)
    if chapters and not chapters[0].startswith('# '):
        intro_content = chapters[0]
        intro_file = output_base / "00_introduction.md"
        with open(intro_file, 'w', encoding='utf-8') as f:
            f.write(intro_content)
        print(f"✅ Created introduction: {intro_file}")
        chapters = chapters[1:]  # Remove introduction from chapters list
    
    chapters_created = 0
    
    # Process each chapter
    for chapter_content in chapters:
        if not chapter_content.strip():
            continue
            
        # Extract chapter title from first line
        lines = chapter_content.strip().split('\n')
        if not lines or not lines[0].startswith('# '):
            continue
            
        chapter_title = lines[0][2:].strip()  # Remove '# ' prefix
        
        # Clean the title for mapping lookup
        clean_title = chapter_title
        for char in ['（', '）', '(', ')']:
            clean_title = clean_title.replace(char, '')
        
        # Find matching mapping - try exact match first, then partial matches
        part_dir = None
        chapter_dir = None
        
        # Try exact match
        if clean_title in chapter_mapping:
            part_dir, chapter_dir = chapter_mapping[clean_title]
        else:
            # Try partial matches
            for key, (p_dir, c_dir) in chapter_mapping.items():
                if any(word in clean_title for word in key.split()) or any(word in key for word in clean_title.split()):
                    part_dir, chapter_dir = p_dir, c_dir
                    break
        
        if not part_dir or not chapter_dir:
            print(f"⚠️  Could not map chapter: '{chapter_title}' -> '{clean_title}'")
            # Create a fallback mapping
            safe_name = clean_filename(clean_title)
            fallback_file = output_base / f"unmapped_{safe_name}.md"
            with open(fallback_file, 'w', encoding='utf-8') as f:
                f.write(chapter_content)
            print(f"📄 Created fallback file: {fallback_file}")
            continue
        
        # Create the target directory structure
        target_dir = output_base / part_dir / chapter_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Create the content file
        content_file = target_dir / "content.md"
        
        # Write the chapter content
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(chapter_content)
        
        # Update or create the README with actual content preview
        readme_file = target_dir / "README.md"
        
        # Extract first few lines for preview
        content_lines = chapter_content.split('\n')
        preview_lines = []
        for line in content_lines[1:6]:  # Skip title, take next 5 lines
            if line.strip():
                preview_lines.append(line.strip())
        
        preview = '\n'.join(preview_lines[:3])  # Take first 3 non-empty lines
        
        readme_content = f"""# {chapter_title}

## 内容预览

{preview}

## 完整内容

完整内容请查看 [content.md](./content.md)

## 导航

- [返回上级目录](../README.md)
- [返回主目录](../../README.md)
"""
        
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ Created chapter: {part_dir}/{chapter_dir}")
        chapters_created += 1
    
    print(f"\n🎉 Content splitting completed!")
    print(f"📊 Created {chapters_created} chapters")
    
    return True

def main():
    print("📚 学会思考 - 内容分割器")
    print("=" * 50)
    
    # Source file path
    source_file = "9years/Learn to Think Basic exercises in the core thinking skills for ages 6–11.zh-CN.2k.high.9years.md"
    
    print(f"📖 源文件: {source_file}")
    print(f"📁 输出目录: organized_content/")
    print()
    
    # Split the content
    success = split_markdown_content(source_file)
    
    if success:
        print("\n🎯 下一步:")
        print("1. 检查 organized_content/ 目录中的内容")
        print("2. 查看各个章节的 content.md 文件")
        print("3. 根据需要调整 README.md 文件")
    else:
        print("\n❌ 内容分割失败")

if __name__ == "__main__":
    main()