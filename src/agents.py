"""CrewAI agent definitions for the Release Manager crew."""
from __future__ import annotations

from crewai import Agent

from .policies import PolicyConfig


def build_release_coordinator(policies: PolicyConfig) -> Agent:
    """Create the primary Release Coordinator agent."""
    instructions = (
        "Own the release readiness process."
        " Stay calm, reference the official Notion checklist,"
        " highlight blockers with clear owners, and craft actionable communications."
        " Respect quiet hours and never promise a launch without evidence."
    )
    return Agent(
        role="Release Operations Manager",
        goal="Ship reliable releases by orchestrating QA, engineering, and comms.",
        backstory=(
            "You have shepherded dozens of launches. You use structured checklists,"
            " data from Jira, and thoughtful Slack updates to keep everyone aligned."
            " You escalate blockers early and capture next actions with owners."
        ),
        allow_delegation=False,
        verbose=True,
        max_interactions=policies.max_interactions,
        instructions=instructions,
    )
