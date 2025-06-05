# Learn to Think Basic - AsciiDoc EPUB3 with TTS Annotations

This project contains the AsciiDoc source files for "Learn to Think Basic: Core Thinking Skills for Ages 6–11" by John Langrehr, converted from markdown with proper EPUB3 formatting and OpenAI TTS voice annotations.

## Project Structure

```
book_asciidoc/
├── learn-to-think-basic.adoc          # Main book file with metadata and includes
├── chapters/                          # Individual chapter files
│   ├── 01-observing-properties.adoc   # Chapter 1: Observing Properties
│   ├── 10-analysing-relationships.adoc # Chapter 10: Analysing Relationships
│   ├── 12-facts-opinions.adoc         # Chapter 12: Facts vs Opinions
│   ├── 19-creative-consequences.adoc  # Chapter 19: Creative Consequences
│   └── [additional chapters needed]   # Remaining 20 chapters
├── styles/
│   └── epub3-tts.css                  # CSS with TTS voice configurations
├── images/                            # Image assets from original book
└── README.md                          # This file
```

## Book Organization

The book is organized into 4 main parts with 24 chapters total:

### Part I: Organizational Thinking (Chapters 1-9)
1. Observing Properties ✓
2. Observing Similarities
3. Observing Differences  
4. Categorising
5. Comparing
6. Ordering in Terms of Size and Time
7. Thinking about Concepts
8. Generalising
9. Concept Maps

### Part II: Analytical Thinking (Chapters 10-11)
10. Analysing Relationships ✓
11. Analysing Patterns in Sequences

### Part III: Evaluative Thinking (Chapters 12-18)
12. Distinguishing Facts from Opinions ✓
13. Distinguishing Definite from Indefinite Conclusions
14. Challenging the Reliability of a Claim
15. Distinguishing Relevant from Irrelevant Information
16. Decision Making
17. Considering Other Points of View
18. Asking Better Questions

### Part IV: Creative Thinking (Chapters 19-24)
19. Creative Consequences ✓
20. Reverse Creative Thinking
21. Analysing the Creativity of Designs
22. Creativity from Random Objects
23. Visual Creativity
24. Creative Thinking about Uses

## TTS Voice Configuration

The book uses multiple OpenAI TTS voices for different content types:

- **Alloy**: Main content voice (neutral, clear)
- **Echo**: Chapter introductions and headings (slow, emphasized)
- **Nova**: Examples and captions (medium pace)
- **Shimmer**: Student worksheets (faster pace)

### Voice Markup Examples

```asciidoc
[role="tts-voice-alloy"]
This is regular content read by the Alloy voice.

[role="tts-voice-echo"]
This is a chapter introduction read by Echo voice.
```

## EPUB3 Features

- **Semantic markup** with proper `epub:type` attributes
- **Responsive design** that works across devices
- **Table of contents** with proper navigation
- **CSS Speech module** integration for TTS
- **SSML phoneme support** for pronunciation
- **Accessible formatting** following EPUB accessibility standards

## Prerequisites

To generate the EPUB3 file, you need:

1. **Asciidoctor EPUB3** gem installed:
   ```bash
   gem install asciidoctor-epub3
   ```

2. **Ruby 2.7+** for running Asciidoctor

3. **EPUBCheck** for validation (optional):
   ```bash
   # Download from https://github.com/w3c/epubcheck/releases
   ```

## Building the EPUB3

### Basic Build
```bash
asciidoctor-epub3 -D output learn-to-think-basic.adoc
```

### Build with Validation
```bash
asciidoctor-epub3 -D output -a ebook-validate learn-to-think-basic.adoc
```

### Build with Extraction (for debugging)
```bash
asciidoctor-epub3 -D output -a ebook-extract learn-to-think-basic.adoc
```

### Build with Custom Styles
```bash
asciidoctor-epub3 -D output -a epub3-stylesdir=styles learn-to-think-basic.adoc
```

## TTS Integration Details

### CSS Speech Properties Used
- `voice-family`: Specifies TTS voice (alloy, echo, nova, shimmer)
- `voice-rate`: Controls speaking speed (slow, medium, fast)
- `voice-volume`: Controls volume (soft, medium, loud)
- `voice-stress`: Controls emphasis (normal, moderate, strong)
- `pause-before/after`: Adds pauses between sections

### SSML Integration
The CSS includes SSML-compatible markup for:
- Phonetic pronunciation hints
- Prosody control (pitch, rate, volume)
- Audio cues and pauses
- Voice selection per content type

## Completion Status

✅ **Completed:**
- Main book structure and metadata
- CSS with TTS voice integration
- 4 representative chapters (one from each section)
- EPUB3 configuration
- Build documentation

🔄 **Remaining Work:**
- Create remaining 20 chapter files in AsciiDoc format
- Add all images to the images/ directory
- Test EPUB3 generation and validation
- Fine-tune TTS voice annotations based on testing

## Creating Remaining Chapters

To complete the book, convert the remaining chapters from the original markdown using this template:

```asciidoc
= Chapter N: [Chapter Title]

[role="tts-voice-echo"]
Chapter [Number]: [Title]

[role="tts-voice-alloy"]
[Chapter introduction content...]

== [Section Title]

[role="tts-voice-alloy"]
[Section content...]

== Student Worksheet

[role="tts-voice-shimmer"]
[Worksheet instructions...]

[cols="..."]
|===
|[Table content]
|===

== Possible Answers

[role="tts-voice-alloy"]
[Answer content...]
```

## Testing the EPUB3

1. **Generate EPUB3**: Use the build commands above
2. **Validate**: Use EPUBCheck to ensure compliance
3. **Test TTS**: Open in a TTS-capable EPUB reader
4. **Cross-platform**: Test on multiple devices/readers

## Voice Reader Recommendations

For best TTS experience, test with:
- **Calibre** (with TTS plugin)
- **Voice Dream Reader** (iOS/Android)
- **Natural Reader** (Web/Desktop)
- **NVDA/JAWS** screen readers

## EPUB3 Metadata

The book includes comprehensive metadata:
- Title, author, description
- Keywords for discoverability  
- Language and publication info
- UUID for unique identification
- Cover image specification
- Series information (if applicable)

## Notes for Manual EPUB3 Generation

When manually generating the EPUB3 from the parent AsciiDoc file:

1. Ensure all chapter files are in the `chapters/` directory
2. Copy images to the `images/` directory 
3. Use the custom CSS file for TTS integration
4. Validate the final EPUB3 with EPUBCheck
5. Test TTS functionality with compatible readers

## License

This content is based on "Learn to Think Basic exercises in the core thinking skills for ages 6–11" © 2008 John Langrehr. The AsciiDoc conversion and TTS annotations are provided for educational purposes.