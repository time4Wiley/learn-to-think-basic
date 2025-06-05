#!/usr/bin/env python3

from pathlib import Path

# Chapter information with Chinese titles
chapters_info = {
    # Organize Thinking
    "1_observe_features": ("1. 观察特征", 5, "组织性思维", "学会仔细观察事物的特征，使用SCUMPS方法"),
    "2_observe_similarities": ("2. 观察相似点", 8, "组织性思维", "找出两个或更多事物的相同之处"),
    "3_observe_differences": ("3. 观察不同点", 11, "组织性思维", "识别事物之间的差异和区别"),
    "4_classification": ("4. 分类", 14, "组织性思维", "按照特征将事物归类整理"),
    "5_comparison": ("5. 比较", 17, "组织性思维", "比较不同事物的优缺点"),
    "6_sorting_by_size_time": ("6. 按大小和时间排序", 20, "组织性思维", "学会按照大小、时间等标准排序"),
    "7_thinking_concepts": ("7. 思考概念", 26, "组织性思维", "理解和运用抽象概念"),
    "8_generalization": ("8. 概括", 29, "组织性思维", "从具体事例中总结出一般规律"),
    "9_concept_maps": ("9. 概念图", 33, "组织性思维", "绘制概念图来组织知识"),
    
    # Analytical Thinking
    "10_analyze_relationships": ("10. 分析关系", 41, "分析思维", "分析事物之间的关系和联系"),
    "11_analyze_sequence_patterns": ("11. 分析序列模式", 44, "分析思维", "识别和分析序列中的模式"),
    
    # Evaluative Thinking
    "12_distinguish_facts_opinions": ("12. 区分事实和观点", 49, "评价性思维", "学会区分客观事实和主观观点"),
    "13_distinguish_certain_uncertain": ("13. 区分肯定和不肯定的结论", 52, "评价性思维", "判断结论的确定性程度"),
    "14_challenge_reliability": ("14. 挑战说法的可靠性", 56, "评价性思维", "评估信息来源的可靠性"),
    "15_distinguish_relevant_irrelevant": ("15. 区分相关和无关信息", 60, "评价性思维", "识别与问题相关的信息"),
    "16_decision_making": ("16. 决策", 64, "评价性思维", "学会做出明智的决策"),
    "17_consider_other_viewpoints": ("17. 考虑其他观点", 70, "评价性思维", "从多个角度看待问题"),
    "18_better_questions": ("18. 提出更好的问题", 73, "评价性思维", "学会提出有价值的问题"),
    
    # Creative Thinking
    "19_creative_consequences": ("19. 创造性后果", 78, "创造性思维", "思考行动可能带来的创造性结果"),
    "20_reverse_creative_thinking": ("20. 逆向创造性思考", 81, "创造性思维", "从结果反推原因的创造性思维"),
    "21_analyze_creative_design": ("21. 分析设计的创造性", 84, "创造性思维", "分析设计中的创造性元素"),
    "22_random_object_creativity": ("22. 随机物体的创造力", 88, "创造性思维", "用随机物体进行创造性思考"),
    "23_visual_creativity": ("23. 视觉创造力", 91, "创造性思维", "发展视觉创造力和想象力"),
    "24_creative_thinking_about_uses": ("24. 关于用途的创造性思考", 93, "创造性思维", "创造性地思考物品的用途"),
}

def create_chapter_readme(folder_path, chapter_key):
    title, page_num, part_name, description = chapters_info[chapter_key]
    
    readme_content = f"""# {title}

**页码:** {page_num}

**所属部分:** {part_name}

## 📝 本章概述

{description}

## 🎯 学习目标

通过本章的学习，学生将能够：

- 掌握本章的核心概念和方法
- 应用所学知识解决实际问题
- 发展相应的思维技能

## 💡 重要概念

<!-- 这里可以添加本章的重要概念 -->

## 🎯 练习活动

### 基础练习

<!-- 这里可以添加基础练习题 -->

### 进阶练习

<!-- 这里可以添加进阶练习题 -->

## 💭 思考问题

- 本章的核心概念是什么？
- 如何在日常生活中应用这些概念？
- 还有哪些类似的例子？

## 📚 扩展学习

- 与家人分享所学内容
- 寻找生活中的相关例子
- 练习相关的思维技巧

## 🔗 相关章节

<!-- 可以链接到相关的其他章节 -->
"""

    readme_path = folder_path / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ 创建了 {title} 的README文件")

def create_part_readmes():
    """Create README files for each part"""
    
    parts_info = {
        "analytical_thinking": {
            "title": "分析思维",
            "description": "分析思维帮助我们理解事物之间的关系和模式。",
            "goals": [
                "分析事物之间的关系",
                "识别序列和模式",
                "理解因果关系",
                "发展逻辑思维能力"
            ]
        },
        "evaluative_thinking": {
            "title": "评价性思维", 
            "description": "评价性思维帮助我们判断信息的质量和做出明智的决策。",
            "goals": [
                "区分事实和观点",
                "评估信息的可靠性",
                "做出明智的决策",
                "从多个角度分析问题"
            ]
        },
        "creative_thinking": {
            "title": "创造性思维",
            "description": "创造性思维帮助我们产生新想法和创新解决方案。",
            "goals": [
                "产生创新想法",
                "从不同角度思考问题",
                "发展想象力",
                "创造性地解决问题"
            ]
        }
    }
    
    for part_folder, info in parts_info.items():
        part_path = Path("organized_content") / part_folder
        if part_path.exists():
            # Get chapters in this part
            chapters = [d.name for d in part_path.iterdir() if d.is_dir()]
            chapters.sort()
            
            readme_content = f"""# {info['title']}

{info['description']}

这一部分包含以下章节:

"""
            
            # Add chapter links
            for chapter in chapters:
                if chapter in chapters_info:
                    title, page_num, _, _ = chapters_info[chapter]
                    readme_content += f"- [{title}](./{chapter}/README.md) (第 {page_num} 页)\n"
            
            readme_content += f"""
## 🎯 学习目标

在这个部分，孩子们将学会：

"""
            for goal in info['goals']:
                readme_content += f"- {goal}\n"
            
            # Write README
            readme_path = part_path / "README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"✅ 创建了 {info['title']} 的README文件")

def main():
    print("🚀 开始创建README文件...")
    
    # Create part README files
    create_part_readmes()
    
    # Create chapter README files
    base_path = Path("organized_content")
    for part_dir in base_path.iterdir():
        if part_dir.is_dir() and part_dir.name != "organize_thinking":  # Skip organize_thinking as we already have some
            for chapter_dir in part_dir.iterdir():
                if chapter_dir.is_dir():
                    chapter_key = chapter_dir.name
                    if chapter_key in chapters_info:
                        readme_path = chapter_dir / "README.md"
                        if not readme_path.exists():  # Only create if doesn't exist
                            create_chapter_readme(chapter_dir, chapter_key)
    
    print("\n✅ 所有README文件创建完成！")
    print(f"📁 项目结构已完整，包含4个主要部分和24个章节")

if __name__ == "__main__":
    main() 