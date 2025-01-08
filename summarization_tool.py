import os
import re
import pandas as pd
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def read_file(file_path):
    """Read and return the text content of a file."""
    ext = Path(file_path).suffix.lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        raise NotImplementedError("Parsing for this file type to be implemented.")

def chunk_text(text, max_chunk_size=1500):
    """Split text into manageable chunks."""
    paragraphs = re.split(r'\n\s*\n', text)
    chunks, current_chunk = [], ""
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= max_chunk_size:
            current_chunk += paragraph + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def build_prompt(chunk_text, previous_summary, domain_knowledge, domain_instructions, is_first_chunk):
    """
    Dynamically build the appropriate prompt for the summarization task based on the chunk type.

    Args:
        chunk_text (str): The current chunk of text.
        previous_summary (str): The previous summary, if any.
        domain_knowledge (str): Domain-specific knowledge to guide summarization.
        domain_instructions (str): Instructions specific to the domain.
        is_first_chunk (bool): Whether this is the first chunk.

    Returns:
        str: The dynamically generated prompt.
    """
    if is_first_chunk:
        prompt = (
            "You are a highly skilled summarization assistant. Your goal is to create a concise and accurate summary "
            "based on the provided source text. The summary must strictly follow the guidelines, domain-specific instructions, "
            "and contextual information outlined below.\n\n"
            "# TASK:\n"
            "- Read the provided source text carefully and extract key information relevant to the domain.\n"
            "- Ensure the summary is concise, coherent, and adheres to the provided instructions.\n\n"
            "# SOURCE TEXT:\n"
            f"{chunk_text}\n\n"
        )
    else:
        prompt = (
            "You are a highly skilled summarization assistant. Your goal is to update an existing summary based on the provided new source text. "
            "The updated summary must strictly follow the guidelines, domain-specific instructions, and contextual information outlined below.\n\n"
            "# EXISTING SUMMARY:\n"
            f"{previous_summary}\n\n"
            "# TASK:\n"
            "- Carefully review the new source text and incorporate only relevant information into the existing summary.\n"
            "- Retain all useful information from the existing summary and avoid redundancy.\n"
            "- If the new source text contains no relevant information, return the existing summary without any changes.\n\n"
            "# NEW SOURCE TEXT:\n"
            f"{chunk_text}\n\n"
        )
    
    prompt += (
        "# GUIDELINES:\n"
        "- Ensure the summary is concise and written in complete sentences.\n"
        "- Focus only on information relevant to the domain and task.\n"
        "- Ensure you only include information that is clearly provided by the source text.\n"
        "- Ensure coherence and flow by maintaining consistent terminology across the summary.\n"
        "- Return the raw summary with no additional comments or explanations.\n\n"
        "# DOMAIN-SPECIFIC INSTRUCTIONS:\n"
        f"{domain_instructions}\n\n"
        "# CONTEXTUAL INFORMATION:\n"
        f"{domain_knowledge}\n\n"
    )

    return prompt


def generate_summary(prompt):

    """Generate a summary submitting prompt to OpenAI's GPT-4o model."""
    messages = [
        {"role": "system", "content": "You are a helpful summarization assistant that creates and updates clear and concise domain-specific summaries"},
        {"role": "user", "content": prompt}
    ]

    # API call to OpenAI's chat completion endpoint
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
        temperature=0.3
    )
        
    # Extract and return the response content
    return response.choices[0].message.content


def save_to_text_file(data, output_file="final_summary.txt"):
    """Save the final summary to a text file."""
    if data:
        final_summary = data[-1]["Summary"]  # Get the last summary
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(final_summary)
        print(f"Final summary saved to {output_file}")
    else:
        print("No data to save.")

def main():
    # Inputs
    file_path = input("Enter the path of the file to summarize: ")
    domain_knowledge_path = input("Enter the path to the domain knowledge file: ")
    domain_instructions_path = input("Enter the path to the domain instructions file: ")

    # Load domain knowledge and instructions using read_file
    domain_knowledge = read_file(domain_knowledge_path)
    domain_instructions = read_file(domain_instructions_path)

    if not domain_knowledge or not domain_instructions:
        print("Error: Domain knowledge or instructions could not be loaded.")
        return

    # Load and process the file
    text = read_file(file_path)
    chunks = chunk_text(text)
    print(f"Text split into {len(chunks)} chunks.")

    # Summarize iteratively
    previous_summary = ""
    summaries = []
    for i, chunk in enumerate(chunks):
        is_first_chunk = (i == 0)

        # Build the dynamic prompt
        prompt = build_prompt(
            chunk_text=chunk,
            previous_summary=previous_summary,
            domain_knowledge=domain_knowledge,
            domain_instructions=domain_instructions,
            is_first_chunk=is_first_chunk,
        )
        # Generate the summary using OpenAI's API
        summary = generate_summary(prompt)
        summaries.append({"Chunk": i + 1, "Summary": summary})
        previous_summary = summary

    # Save summaries to Google Sheets (or CSV)
    save_to_text_file(summaries)

if __name__ == "__main__":
    main()
