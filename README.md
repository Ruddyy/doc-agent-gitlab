# GitLab AI Documentation Agent (Prototype)

This prototype automates user story documentation from GitLab issues using Google Gemini API.

## Features
- Fetches completed GitLab issues.
- Synthesizes professional documentation using Gemini API.
- Saves generated docs locally (Markdown/Word).

## Setup
1. Create a virtual environment and install dependencies.
2. Configure `.env` file with your GitLab and Gemini API keys.
3. Run with `python src/app.py`.

## Environment Variables
```
GITLAB_TOKEN=your_gitlab_access_token
GITLAB_PROJECT_ID=your_project_id
GEMINI_API_KEY=your_gemini_api_key
```
## Upcoming feature..
Adding send email to the person to whom userstory has been assigned and who created the user story to validate the document.
