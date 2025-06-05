#!/usr/bin/env python3
"""
Generate remaining AsciiDoc chapters from the original markdown file.
This script processes the original markdown and converts it to AsciiDoc format
with proper TTS voice annotations.
"""

import re
import os
from pathlib import Path

# Chapter mapping with titles
CHAPTERS = {
    2: "Observing Similarities",
    3: "Observing Differences", 
    4: "Categorising",
    5: "Comparing",
    6: "Ordering in Terms of Size and Time",
    7: "Thinking about Concepts",
    8: "Generalising",
    9: "Concept Maps",
    11: "Analysing Patterns in Sequences",
    13: "Distinguishing Definite from Indefinite Conclusions",
    14: "Challenging the Reliability of a Claim",
    15: "Distinguishing Relevant from Irrelevant Information",
    16: "Decision Making",
    17: "Considering Other Points of View",
    18: "Asking Better Questions",
    20: "Reverse Creative Thinking",
    21: "Analysing the Creativity of Designs",
    22: "Creativity from Random Objects",
    23: "Visual Creativity",
    24: "Creative Thinking about Uses"
}

def convert_markdown_to_asciidoc(markdown_content):
    """Convert markdown content to AsciiDoc format with TTS annotations."""
    
    # Convert headers
    content = re.sub(r'^# (.+)$', r'= \1', markdown_content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'== \1', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'=== \1', content, flags=re.MULTILINE)
    
    # Convert bold and italic
    content = re.sub(r'\*\*(.+?)\*\*', r'**\1**', content)
    content = re.sub(r'\*(.+?)\*', r'_\1_', content)
    
    # Convert images
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'image::\2[\1]', content)
    
    # Convert tables - basic conversion, may need manual adjustment
    # This is a simplified conversion - complex tables may need manual work
    table_pattern = r'\|(.+)\|'
    content = re.sub(table_pattern, r'|\1|', content)
    
    return content

def add_tts_annotations(content, chapter_num):
    """Add TTS voice annotations to the content."""
    
    # Add chapter introduction with Echo voice
    if content.startswith('='):
        title_line = content.split('\n')[0]
        rest_content = '\n'.join(content.split('\n')[1:])
        
        content = f"""{title_line}

[role="tts-voice-echo"]
Chapter {chapter_num}: {CHAPTERS.get(chapter_num, 'Unknown Chapter')}

[role="tts-voice-alloy"]
{rest_content.strip()}"""
    
    # Add voice annotations to sections
    lines = content.split('\n')
    annotated_lines = []
    
    for i, line in enumerate(lines):
        if line.startswith('==') and not line.startswith('==='):
            # Section headers
            annotated_lines.append(line)
            annotated_lines.append('')
            if 'Student Worksheet' in line or 'worksheet' in line.lower():
                annotated_lines.append('[role="tts-voice-shimmer"]')
            elif 'Example' in line or 'Possible Answer' in line:
                annotated_lines.append('[role="tts-voice-nova"]')
            else:
                annotated_lines.append('[role="tts-voice-alloy"]')
        elif line.startswith('==='):
            # Subsection headers
            annotated_lines.append(line)
            annotated_lines.append('')
            annotated_lines.append('[role="tts-voice-alloy"]')
        else:
            annotated_lines.append(line)
    
    return '\n'.join(annotated_lines)

def extract_chapter_content(full_markdown, chapter_title):
    """Extract content for a specific chapter from the full markdown."""
    
    # Find the chapter start
    pattern = rf'^# {re.escape(chapter_title)}.*?(?=^# |\Z)'
    match = re.search(pattern, full_markdown, re.MULTILINE | re.DOTALL)
    
    if match:
        return match.group(0)
    else:
        # Try alternative patterns
        alt_patterns = [
            rf'^#{re.escape(chapter_title)}.*?(?=^# |\Z)',
            rf'^# .*{re.escape(chapter_title.split()[-1])}.*?(?=^# |\Z)',
        ]
        
        for pattern in alt_patterns:
            match = re.search(pattern, full_markdown, re.MULTILINE | re.DOTALL)
            if match:
                return match.group(0)
    
    return None

def generate_chapter_file(chapter_num, chapter_title, content, output_dir):
    """Generate an AsciiDoc file for a chapter."""
    
    # Convert markdown to asciidoc
    asciidoc_content = convert_markdown_to_asciidoc(content)
    
    # Add TTS annotations
    asciidoc_content = add_tts_annotations(asciidoc_content, chapter_num)
    
    # Create filename
    filename = f"{chapter_num:02d}-{chapter_title.lower().replace(' ', '-').replace(',', '').replace(':', '')}.adoc"
    filepath = output_dir / filename
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(asciidoc_content)
    
    print(f"Generated: {filename}")
    return filename

def main():
    """Main function to generate all remaining chapters."""
    
    # Set up paths
    script_dir = Path(__file__).parent
    chapters_dir = script_dir / "chapters"
    chapters_dir.mkdir(exist_ok=True)
    
    # Read the original markdown file
    markdown_file = script_dir.parent / "Learn to Think Basic exercises in the core thinking skills for ages 6–11.md"
    
    if not markdown_file.exists():
        print(f"Error: Could not find {markdown_file}")
        print("Please ensure the original markdown file is in the parent directory.")
        return
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        full_markdown = f.read()
    
    print("Generating remaining chapters...")
    print("=" * 50)
    
    # Generate each missing chapter
    generated_files = []
    
    for chapter_num, chapter_title in CHAPTERS.items():
        print(f"\nProcessing Chapter {chapter_num}: {chapter_title}")
        
        # Extract chapter content
        chapter_content = extract_chapter_content(full_markdown, chapter_title)
        
        if chapter_content:
            filename = generate_chapter_file(chapter_num, chapter_title, chapter_content, chapters_dir)
            generated_files.append(filename)
        else:
            print(f"Warning: Could not find content for Chapter {chapter_num}: {chapter_title}")
            # Create a placeholder file
            placeholder_content = f"""= Chapter {chapter_num}: {chapter_title}

[role="tts-voice-echo"]
Chapter {chapter_num}: {chapter_title}

[role="tts-voice-alloy"]
// TODO: Add chapter content here
// This chapter needs to be manually created from the original source material.

== Placeholder Content

[role="tts-voice-alloy"]
This chapter has not been automatically converted and needs manual attention.
Please refer to the original markdown file and convert the content for:

*Chapter {chapter_num}: {chapter_title}*

== Structure Template

[role="tts-voice-alloy"]
Use this template when creating the chapter:

1. Introduction with concept explanation
2. Examples with visual aids
3. Student worksheet with exercises
4. Possible answers section
5. Useful questions summary
"""
            filename = f"{chapter_num:02d}-{chapter_title.lower().replace(' ', '-').replace(',', '').replace(':', '')}.adoc"
            filepath = chapters_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(placeholder_content)
            
            generated_files.append(filename)
            print(f"Generated placeholder: {filename}")
    
    print("\n" + "=" * 50)
    print(f"Generated {len(generated_files)} chapter files:")
    for filename in generated_files:
        print(f"  - {filename}")
    
    print(f"\nFiles saved to: {chapters_dir}")
    print("\nNext steps:")
    print("1. Review generated files and fix any conversion issues")
    print("2. Add proper table formatting for worksheets")
    print("3. Verify image references are correct")
    print("4. Test EPUB3 generation with: asciidoctor-epub3 learn-to-think-basic.adoc")

if __name__ == "__main__":
    main()