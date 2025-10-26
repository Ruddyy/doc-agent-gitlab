import os
import requests

GITLAB_URL = "https://gitlab.com"
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
HEADERS = {"PRIVATE-TOKEN": GITLAB_TOKEN}

def fetch_issue_data(issue_id):
    issue_url = f"{GITLAB_URL}/api/v4/projects/{GITLAB_PROJECT_ID}/issues/{issue_id}"
    notes_url = f"{issue_url}/notes"

    issue_resp = requests.get(issue_url, headers=HEADERS)
    notes_resp = requests.get(notes_url, headers=HEADERS)

    issue = issue_resp.json() if issue_resp.status_code == 200 else {}
    notes = notes_resp.json() if notes_resp.status_code == 200 else []

    comments = [f"{n.get('author', {}).get('name','')}: {n.get('body','')}" for n in notes]

    return {
        "title": issue.get("title",""),
        "description": issue.get("description",""),
        "labels": issue.get("labels",[]),
        "assignee": issue.get("assignee",{}).get("name","Unassigned"),
        "closed_by": issue.get("closed_by",{}).get("name","Unknown"),
        "comments": comments
    }
