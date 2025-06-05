#!/usr/bin/env python3

import re
from pathlib import Path

def find_chapter_boundaries(content):
    """Find the start and end positions of each chapter based on headings"""
    lines = content.split('\n')
    chapter_positions = []
    
    # Chapter mapping from TOC
    chapter_titles = {
        "观察事物的特点": "1_observe_features",
        "观察相似点": "2_observe_similarities", 
        "观察差异": "3_observe_differences",
        "分类": "4_classification",
        "比较": "5_comparison",
        "按大小和时间排序": "6_sorting_by_size_time",
        "思考概念": "7_thinking_concepts",
        "概括": "8_generalization",
        "概念图": "9_concept_maps",
        "分析关系": "10_analyze_relationships",
        "分析序列模式": "11_analyze_sequence_patterns",
        "区分事实和观点": "12_distinguish_facts_opinions",
        "区分肯定和不肯定的结论": "13_distinguish_certain_uncertain",
        "挑战说法的可靠性": "14_challenge_reliability",
        "区分相关和无关信息": "15_distinguish_relevant_irrelevant",
        "决策": "16_decision_making",
        "考虑其他观点": "17_consider_other_viewpoints",
        "提出更好的问题": "18_better_questions",
        "创造性后果": "19_creative_consequences",
        "逆向创造性思考": "20_reverse_creative_thinking",
        "分析设计的创造性": "21_analyze_creative_design",
        "随机物体的创造力": "22_random_object_creativity",
        "视觉创造力": "23_visual_creativity",
        "关于用途的创造性思考": "24_creative_thinking_about_uses"
    }
    
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('# ') and not line.startswith('# 目录') and not line.startswith('# 介绍'):
            title = line[2:].strip()
            # Check for exact matches or partial matches
            for chapter_title, folder_name in chapter_titles.items():
                if chapter_title in title or title in chapter_title:
                    chapter_positions.append({
                        'title': chapter_title,
                        'folder': folder_name,
                        'start_line': i,
                        'full_title': title
                    })
                    break
    
    # Add end positions
    for i in range(len(chapter_positions)):
        if i < len(chapter_positions) - 1:
            chapter_positions[i]['end_line'] = chapter_positions[i + 1]['start_line'] - 1
        else:
            chapter_positions[i]['end_line'] = len(lines) - 1
    
    return chapter_positions

def get_part_folder(folder_name):
    """Determine which part folder a chapter belongs to"""
    if folder_name.startswith(('1_', '2_', '3_', '4_', '5_', '6_', '7_', '8_', '9_')):
        return 'organize_thinking'
    elif folder_name.startswith(('10_', '11_')):
        return 'analytical_thinking'
    elif folder_name.startswith(('12_', '13_', '14_', '15_', '16_', '17_', '18_')):
        return 'evaluative_thinking'
    elif folder_name.startswith(('19_', '20_', '21_', '22_', '23_', '24_')):
        return 'creative_thinking'
    return None

def extract_chapter_content(lines, start_line, end_line):
    """Extract content for a specific chapter"""
    chapter_lines = lines[start_line:end_line + 1]
    return '\n'.join(chapter_lines)

def create_chapter_readme(title, content, folder_path, part_name):
    """Create a comprehensive README for each chapter with extracted content"""
    
    readme_content = f"""# {title}

**所属部分:** {part_name}

## 📝 章节内容

{content}

---

## 💡 学习要点

*本节的关键概念和方法已在上面的内容中详细说明*

## 🎯 实践建议

- 仔细阅读上面的内容和示例
- 完成练习单中的活动
- 思考"试试看"中的问题
- 应用所学概念到日常生活中

## 📚 相关资源

- 可以结合其他章节的内容进行综合练习
- 鼓励与家人朋友分享所学内容

## 🔄 复习检查

- 能否理解本章的核心概念？
- 是否完成了相关的练习活动？
- 能否在生活中找到相关的例子？
"""
    
    with open(folder_path / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    print("🚀 开始提取和分割章节内容...")
    
    # Read the source file
    source_file = '../9years/Learn to Think Basic exercises in the core thinking skills for ages 6–11.zh-CN.2k.high.9years.md'
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find chapter boundaries
    lines = content.split('\n')
    chapter_positions = find_chapter_boundaries(content)
    
    print(f"找到 {len(chapter_positions)} 个章节:")
    for pos in chapter_positions:
        print(f"  - {pos['title']} ({pos['folder']}) - 第{pos['start_line']+1}行到第{pos['end_line']+1}行")
    
    # Extract and save content for each chapter
    organized_path = Path('organized_content')
    processed_count = 0
    
    for pos in chapter_positions:
        part_folder = get_part_folder(pos['folder'])
        if not part_folder:
            print(f"⚠️  无法确定 {pos['folder']} 属于哪个部分")
            continue
            
        chapter_path = organized_path / part_folder / pos['folder']
        
        if chapter_path.exists():
            # Extract content
            chapter_content = extract_chapter_content(lines, pos['start_line'], pos['end_line'])
            
            # Create README with actual content
            create_chapter_readme(
                pos['full_title'], 
                chapter_content, 
                chapter_path, 
                part_folder.replace('_', ' ').title()
            )
            
            processed_count += 1
            print(f"✅ 已处理: {pos['title']}")
        else:
            print(f"⚠️  目录不存在: {chapter_path}")
    
    print(f"\n🎉 内容分割完成!")
    print(f"📁 成功处理了 {processed_count} 个章节")
    print(f"📝 每个章节的README.md文件已包含实际内容")

if __name__ == "__main__":
    main() 