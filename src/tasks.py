"""CrewAI tasks for the Release Manager crew."""
from __future__ import annotations

from crewai import Task


def build_tasks(agent, notion_tool):
    """Return the ordered list of tasks for the release run."""
    readiness = Task(
        description=(
            "Pull the latest release checklist from Notion, summarize each step,"
            " and highlight any items that are not yet complete."
        ),
        expected_output=(
            "A markdown table with columns: step, owner, status, due date, blockers."
            " Include a final paragraph listing the top 3 risks."
        ),
        tools=[notion_tool],
        agent=agent,
    )

    blockers = Task(
        description=(
            "For every blocker surfaced, craft next actions with owners and deadlines."
            " Escalate anything older than 24h."
        ),
        expected_output="Bullet list of blockers with owner, ETA, and escalation status.",
        tools=[notion_tool],
        agent=agent,
    )

    comms = Task(
        description=(
            "Draft a Slack-ready release update that references readiness status"
            " and calls out blockers. Keep it under 150 words."
        ),
        expected_output=(
            "A Slack message with title, summary, blockers section, and next checkpoint time."
        ),
        agent=agent,
    )

    return [readiness, blockers, comms]
