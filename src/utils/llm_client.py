import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY")

genai.configure(api_key=api_key)


def generate_doc(issue_title: str, context_text: str) -> str:
    """Generate clean documentation for a GitLab issue using Gemini."""
    prompt = f"""
You are an AI Technical Writer that creates structured documentation.

Generate a professional user story document for the following GitLab issue:

{context_text}

The document should include:
- Executive Summary
- Business Rationale
- Acceptance Criteria
- Implementation Details
- Verification & Testing
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    markdown = response.text or "No output from Gemini."

    # Save LLM output to files (for traceability)
    os.makedirs("outputs", exist_ok=True)
    md_path = os.path.join("outputs", f"{issue_title}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✅ LLM Generated Markdown: {md_path}")
    return markdown
