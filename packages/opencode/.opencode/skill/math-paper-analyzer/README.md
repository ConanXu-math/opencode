# Math Paper Analyzer Skill

A specialized skill for analyzing mathematical papers, extracting structured information, and generating comprehensive analysis reports.

## Features

- **Three Analysis Modes**: Fast (regex-only), Standard (regex+LLM), Deep (full analysis)
- **Mathematical Formula Preservation**: OCR with LaTeX formula support
- **Structured Extraction**: Sections, theorems, definitions, proofs, key equations
- **Multi-dimensional Tagging**: Field, content, and technique tags
- **Markdown Output**: Professional analysis reports
- **Error Recovery**: Graceful degradation and fallback modes

## Quick Start

### 1. Installation

```bash
# Clone or copy the skill directory
# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# For LLM features, set OPENAI_API_KEY or custom LLM config
```

### 3. Basic Usage

```python
from scripts.paper_analyzer import PaperAnalyzer

# Create analyzer
analyzer = PaperAnalyzer()

# Analyze a paper
result = analyzer.analyze("math_paper.pdf", mode="standard")

# Get markdown report
print(result["markdown"])
```

### 4. Command Line

```bash
# Fast mode (no LLM required)
python -m scripts.paper_analyzer paper.pdf --mode fast

# Standard mode (requires LLM)
python -m scripts.paper_analyzer paper.pdf --mode standard

# Save output to directory
python -m scripts.paper_analyzer paper.pdf --mode deep --output-dir ./analysis
```

## Skill Structure

```
math-paper-analyzer/
├── SKILL.md              # Skill definition and instructions
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── .env.example          # Environment configuration template
├── scripts/              # Core implementation
│   ├── ocr_pdf_reader.py      # OCR PDF processing
│   ├── structure_extractor.py # Two-phase structure extraction
│   ├── paper_analyzer.py      # Unified analysis pipeline
│   └── test_analyzer.py       # Test suite
├── templates/            # Output templates
│   └── analysis_template.md   # Markdown template
├── examples/             # Usage examples
│   └── usage_example.py       # Comprehensive examples
└── references/           # Reference materials
```

## Analysis Modes

### 1. Fast Mode

- **Processing**: OCR + regex extraction only
- **Time**: 10-30 seconds (10-page paper)
- **LLM Required**: No
- **Best for**: Quick structure overview, no LLM available

### 2. Standard Mode

- **Processing**: OCR + regex + LLM structure refinement
- **Time**: 1-3 minutes (10-page paper)
- **LLM Required**: Yes
- **Best for**: Accurate structure with theorem-proof linking

### 3. Deep Mode

- **Processing**: Full analysis + LLM summary generation
- **Time**: 3-5 minutes (10-page paper)
- **LLM Required**: Yes
- **Best for**: Complete analysis with multi-dimensional tags

## Output Format

The analyzer generates comprehensive Markdown reports:

```markdown
# Paper Title

## Paper Abstract

1-2 paragraph overview...

## Multi-dimensional Tags

- **Field**: Graph Theory, Combinatorial Optimization
- **Content**: Matching Existence Conditions
- **Technique**: Constructive Proof, Probabilistic Method

## Chapter Structure

1. Introduction (p.1)
2. Preliminaries (p.2)
   2.1 Basic Definitions (p.3)

## Theorems and Definitions

### Theorems

- **Theorem 3.1** (p.5): Main theorem statement...
  - **Proof Approach**: By construction...

### Definitions

- **Definition 2.1** (p.3): Basic concept definition...

## Proof Analysis

### Core Methods

1. Induction
2. Proof by Contradiction
3. Probabilistic Method

## Key Formulas

- (p.4) $f(x) = \sum_{i=1}^n a_i x_i$
```

## Configuration Options

### Environment Variables

```bash
# Required: OCR service
MATH_PAPER_OCR_URL=https://edusys5.sii.edu.cn/ocr

# Optional: LLM for standard/deep modes
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# Or custom LLM
MATH_PAPER_LLM_API_KEY=your_key
MATH_PAPER_LLM_BASE_URL=https://your-api.com/v1
MATH_PAPER_LLM_MODEL=your-model
```

### Python API Options

```python
analyzer = PaperAnalyzer(
    ocr_url="https://edusys5.sii.edu.cn/ocr",
    llm_api_key="sk-xxx",          # Optional
    llm_base_url="https://api.openai.com/v1",
    llm_model="gpt-4o",
    temp_dir="/tmp/paper-analysis", # Optional
)
```

## Use Cases

### For Learners

- Understand complex mathematical papers
- Extract key definitions and theorems
- Follow proof strategies and techniques
- Generate study notes and summaries

### For Researchers

- Quickly analyze related work
- Extract innovation points and contributions
- Compare proof approaches across papers
- Generate literature review materials

### For Educators

- Create teaching materials from papers
- Extract examples and exercises
- Generate solution guides
- Prepare lecture notes

## Performance Tips

1. **Large PDFs**: Use fast mode for initial scanning
2. **Batch Processing**: Use `analyze_multiple()` for multiple papers
3. **Memory Management**: Process large papers in chunks
4. **Caching**: Reuse analysis results for same papers

## Troubleshooting

### Common Issues

1. **OCR Service Unavailable**

   ```python
   # Try alternative OCR service
   analyzer = PaperAnalyzer(ocr_url="alternative-ocr-service.com")
   ```

2. **LLM Configuration Errors**

   ```python
   # Fall back to fast mode
   result = analyzer.analyze("paper.pdf", mode="fast")
   ```

3. **PDF Processing Errors**
   - Ensure PDF is not corrupted
   - Try converting to standard PDF format
   - Check file permissions

4. **Memory Issues**
   ```python
   # Reduce parallel workers
   analyzer = PaperAnalyzer(max_workers=2)
   ```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

analyzer = PaperAnalyzer()
result = analyzer.analyze("paper.pdf", mode="standard")
```

## Testing

Run the test suite:

```bash
python scripts/test_analyzer.py
```

## Development

### Adding New Features

1. **Extend Structure Extraction**
   - Add new regex patterns in `structure_extractor.py`
   - Update LLM prompts for new elements

2. **Custom Output Formats**
   - Create new templates in `templates/`
   - Add formatting functions

3. **Integration with Other Tools**
   - Import analyzer in your projects
   - Extend `PaperAnalyzer` class

### Code Style

- Use Black for code formatting
- Use Ruff for linting
- Add type annotations
- Write docstrings for all functions

## License

MIT License

## Support

For issues and feature requests:

1. Check the troubleshooting section
2. Review example code
3. Submit issues with detailed descriptions

## Acknowledgments

Based on the arXiv-Paper-Assistant project, specialized for mathematical paper analysis with enhanced structure extraction and learning-focused features.
