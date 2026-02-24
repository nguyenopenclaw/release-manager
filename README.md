# Release Manager Crew

Release Manager Crew is a CrewAI-based orchestrator that walks through every step of a software release checklist. It pulls the latest readiness data from Notion, tracks blockers in Jira, prepares cross-team messaging for Slack, and enforces basic operational guardrails (quiet hours, approvals, rate limits).

## ✨ Key Capabilities
- **Checklist ingestion** – pulls the canonical release checklist from Notion and turns it into structured tasks.
- **Blocker triage** – highlights blockers coming from Jira and prompts owners for next actions.
- **Comms prep** – drafts Slack-ready announcements with approval gates.
- **Guardrails first** – quiet hours, approval requirements, and channel rate limits live in code (not prompts).

## 📁 Project Structure
```
release-manager/
├── README.md
├── config.yaml               # Agent + policy configuration
├── pyproject.toml            # Poetry/uv friendly metadata
├── .env.example              # Required environment variables
├── .gitignore
└── src/
    ├── main.py               # Typer CLI entrypoint
    ├── agents.py             # CrewAI agent definitions
    ├── tasks.py              # CrewAI task definitions
    ├── policies.py           # Guardrail data models & helpers
    ├── config_loader.py      # YAML + env loader utilities
    └── tools/
        └── notion_tool.py    # Notion release checklist stub
```

## ⚙️ Requirements
- Python 3.11+
- `uv` or `pip` for dependency management
- Access to the LLM provider configured for CrewAI (OpenAI by default)

## 🔐 Environment Variables
Copy `.env.example` to `.env` and fill in the placeholders:

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | LLM provider key for CrewAI. |
| `NOTION_API_KEY` | Integration token with read access to the release workspace. |
| `NOTION_RELEASE_DATABASE_ID` | Database/page that stores the release checklist. |
| `SLACK_BOT_TOKEN` | Slack bot token (starts with `xoxb-`). |
| `SLACK_SIGNING_SECRET` | Slack signing secret for request validation. |
| `SLACK_ANNOUNCE_CHANNEL` | Channel (ID or name) for release comms. |
| `JIRA_BASE_URL` | Base URL for your Atlassian site. |
| `JIRA_PROJECT_KEY` | Project containing release issues (e.g., `REL`). |
| `JIRA_EMAIL` | Automation user email. |
| `JIRA_API_TOKEN` | Jira API token for the automation user. |

> **Safety**: Credentials live only in `.env` and are never committed. Guardrail policies (quiet hours, approvals, rate limits) default to safe values in `config.yaml`.

## 🚀 Setup & Usage
1. **Install dependencies**
   ```bash
   cd release-manager
   uv pip install -r <(uv pip compile pyproject.toml)  # or: pip install -e .
   ```
   (Any standard `pip install -r requirements.txt` workflow works—`pyproject.toml` already lists the deps.)

2. **Configure environment**
   ```bash
   cp .env.example .env
   # fill in the placeholders
   ```

3. **Run the crew**
   ```bash
   python -m src.main run
   ```
   The CLI checks quiet hours and approvals before kicking off the Crew. Outputs are emitted via Rich logging and any generated artifacts are placed in `artifacts/`.

## 🛡️ Guardrails
- **Quiet hours** prevent running the release sequence during off-hours unless `--override-quiet-hours` is supplied.
- **Approval gate** enforces that a human approver signs off before Slack comms are sent.
- **Rate limits** ensure Slack/Jira chatter stays within policy.

## 🧪 Validation
The project ships with a lightweight self-check:
```bash
python -m compileall src
```
Run it before commits to confirm syntax is valid.

## 📝 TODOs
- Plug in real Slack and Jira SDK wrappers inside `src/tools/`.
- Persist crew outputs to a shared knowledge base.
- Add unit tests covering policy enforcement and tool adapters.

---
Built by **ManagerOps-Factory** with safety-first defaults. 🦾