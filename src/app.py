from flask import Flask, request, jsonify
from utils.llm_client import generate_doc
from utils.file_writer import save_document
import logging
import traceback

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        logging.info(f"📩 Received webhook payload: {data}")

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        issue = data.get("object_attributes", {})
        user = data.get("user", {})
        assignees = data.get("assignees", [])
        project = data.get("project", {})

        issue_title = issue.get("title", "Untitled Issue")
        issue_description = issue.get("description", "No description provided.")
        issue_state = issue.get("state", "unknown")
        issue_url = issue.get("url", "")
        author_name = user.get("name", "Unknown Author")
        assignee_name = assignees[0]["name"] if assignees else "Unassigned"
        created_at = issue.get("created_at", "N/A")
        closed_at = issue.get("closed_at", "N/A")
        project_name = project.get("name", "Unknown Project")
        project_id = project.get("id", "0")
        action = issue.get("action", "updated")

        # Construct LLM context
        context_text = f"""
Project: {project_name}
Issue Title: {issue_title}
Description: {issue_description}
Author: {author_name}
Assignee: {assignee_name}
State: {issue_state}
Action: {action}
Created At: {created_at}
Closed At: {closed_at}
URL: {issue_url}
"""

        # 🧠 Generate using Gemini
        doc_content = generate_doc(issue_title, context_text)

        # 💾 Save both .md and .docx
        md_path, docx_path = save_document(project_id, issue_title, doc_content)

        return jsonify({
            "status": "success",
            "markdown": md_path,
            "docx_file": docx_path
        }), 200

    except Exception as e:
        logging.error("❌ Exception in webhook:\n" + traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
