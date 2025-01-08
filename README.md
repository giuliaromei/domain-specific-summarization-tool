# domain-specific-summarization-tool

## Overview
This script is a domain-specific summarization tool designed to process lengthy texts in chunks and generate concise summaries. It leverages OpenAI’s API to dynamically summarize content while incorporating user-provided domain knowledge and instructions for contextual relevance.

Key features include:

- Iterative summarization, where summaries are updated chunk-by-chunk.
- Integration of domain-specific knowledge and instructions to guide the summarization process.
- Dynamic promting
- Modular design for easy extension and customization.

## How it works

### Input Files:
A text file containing the document to be summarized.
Two separate text files for:
- Domain Knowledge: Contextual information about the domain.
- Domain Instructions: Specific guidelines for tailoring the summary.

### Process:
The script reads the input document and splits it into manageable chunks.
A dynamically generated prompt is created for each chunk, customized based on whether it’s the first chunk or subsequent chunks.
OpenAI’s API is called with the prompt to generate the summary.
For subsequent chunks, the script updates the existing summary iteratively.

### Output:
A .txt file containing the final summary is generated.

## Setup

### Prerequisites:
Python 3.7+
OpenAI API key (set as an environment variable: OPENAI_API_KEY)

Installation: Install required Python packages:
bash
Copy code
pip install openai pandas

### Run the Script: 
python summarization_tool.py

Follow the prompts to specify:
The file path of the document to summarize.
The file path for the domain knowledge file.
The file path for the domain instructions file.

### Input Example:
Examples can be found in the Sample Data folder:
Document: A text file on "Generative Grammar."
Domain Knowledge: A brief overview of generative grammar principles.
Domain Instructions: Guidelines to focus on specific concepts and provide a list-style summary.

## Current Limitations & Possible Improvements
- PDF and DOCX Support: Currently, only .txt files are supported for input. Adding robust PDF and DOCX parsing functionality would enhance usability.
- Error Handling: Add retries for failed API calls due to transient issues.
- Parallel Processing: Process chunks in parallel to speed up the summarization of lengthy documents.
- Summary Refinement: Implement a post-processing step to ensure coherence and alignment of the final summary.
- Support for Additional Models: Add compatibility with local LLMs like GPT-NeoX or open-source models for cost-efficiency and privacy.
- Custom Output Formats: Support for exporting summaries as structured JSON, Markdown, or CSV files for specific use cases.
- API Dependency: Relies on OpenAI’s API.
- Domain-Specificity: The quality of the summary depends heavily on the clarity and relevance of the provided domain knowledge and instructions.
- Token Limits: Summarization may fail for chunks or summaries that exceed OpenAI’s token limit.
- The script currently employs a simple chunking strategy based on splitting the input text into manageable sections, typically by paragraph or character count. While effective for basic use cases, more elaborate strategies may be needed for complex documents (Semantic chunking, Token-Aware Splitting, Overlap Strategies or Dynamic Chunk Sizes).
