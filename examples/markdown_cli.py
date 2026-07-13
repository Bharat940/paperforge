# Programmatic Markdown compilation example
import os
from engrapha_notes.cli import compile_markdown_to_pdf

# 1. Create a sample markdown file
sample_md = """---
title: Introduction to Python
author: Bharat Dangi
theme: textbook
---

# Section 1: Hello World

This notes file is written in plain Markdown.

* You can use **bold text** or *italic text*.
* Or inline formulas like $E = mc^2$.
* Or callouts like below:

> [!NOTE]
> This is a note block parsed from markdown quotes.

```python
def hello():
    print("Hello from code block!")
```
"""

md_filename = "temp_sample.md"
pdf_filename = "temp_sample.pdf"

print(f"Creating sample markdown file: {md_filename}...")
with open(md_filename, "w", encoding="utf-8") as f:
    f.write(sample_md)

print(f"Compiling {md_filename} to {pdf_filename}...")
try:
    compile_markdown_to_pdf(
        input_file=md_filename, output_file=pdf_filename, theme_name="textbook"
    )
    print(f"PDF successfully compiled: {pdf_filename}")
except Exception as e:
    print(f"Compilation failed: {e}")

# Clean up
if os.path.exists(md_filename):
    os.remove(md_filename)
