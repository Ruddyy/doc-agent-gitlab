import os
from datetime import datetime
from docx import Document
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_safe_filename(project_id, title):
    """Create a safe filename using project_id and title."""
    safe_title = title.replace(" ", "_").replace("/", "_")
    return f"{project_id}_{safe_title}"

def save_document(project_id, title, content):
    """
    Save content as Markdown and DOCX.
    - If a file for the same project_id + title exists, update it.
    - Otherwise, create a new file with a timestamp.
    """
    filename_base = get_safe_filename(project_id, title)
    
    existing_md = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(filename_base) and f.endswith(".md")]
    if existing_md:
        path_md = os.path.join(OUTPUT_DIR, existing_md[0])
        docx_path = path_md.replace(".md", ".docx")
        logging.info(f"🔄 Updating existing files for {title} (Project {project_id})")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"{filename_base}_{timestamp}"
        path_md = os.path.join(OUTPUT_DIR, f"{filename_base}.md")
        docx_path = os.path.join(OUTPUT_DIR, f"{filename_base}.docx")
        logging.info(f"🆕 Creating new files for {title} (Project {project_id})")

    try:
        with open(path_md, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"✅ Saved Markdown: {path_md}")
    except Exception as e:
        logging.error(f"❌ Failed to save Markdown: {e}")

    try:
        doc = Document()
        for line in content.split("\n"):
            doc.add_paragraph(line)
        doc.save(docx_path)
        logging.info(f"✅ Saved Word: {docx_path}")
    except Exception as e:
        logging.error(f"❌ Failed to save Word: {e}")

    return path_md, docx_path
