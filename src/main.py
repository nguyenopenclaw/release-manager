"""CLI entrypoint for the Release Manager crew."""
from __future__ import annotations

from pathlib import Path

import typer
from crewai import Crew, Process
from rich.console import Console

from .agents import build_release_coordinator
from .config_loader import ensure_env_vars, load_config, load_tool_config
from .policies import PolicyConfig
from .tasks import build_tasks
from .tools.notion_tool import NotionReleaseTool

app = typer.Typer(help="Coordinate the software release checklist with CrewAI.")
console = Console()


@app.command()
def run(
    override_quiet_hours: bool = typer.Option(
        False, help="Override quiet hours policy for urgent releases."
    ),
    approved_by: str | None = typer.Option(
        None,
        help="Name/email of the human approver authorizing release communications.",
    ),
):
    """Kick off the crew after verifying guardrails."""
    ensure_env_vars()
    config = load_config()
    policies = PolicyConfig.from_dict(
        config.get("policies", {}),
        default_max_interactions=config.get("agent", {}).get("max_interactions", 4),
    )

    if not override_quiet_hours and policies.quiet_hours.is_quiet_now():
        console.print(
            "[yellow]Quiet hours are in effect. Rerun with --override-quiet-hours for emergencies."
        )
        raise typer.Exit(code=1)

    policies.approvals.validate(approved_by)
    if approved_by:
        console.print(f"[green]Approval granted by {approved_by}.")

    notion_cfg = load_tool_config(config)
    notion_tool = NotionReleaseTool(
        release_doc_url=notion_cfg["release_doc_url"],
        database_id=notion_cfg["database_id"],
    )

    agent = build_release_coordinator(policies)
    tasks = build_tasks(agent, notion_tool)

    crew = Crew(
        agents=[agent],
        tasks=tasks,
        process=Process.sequential,
    )

    console.print("[cyan]Starting release readiness run...\n")
    result = crew.kickoff()
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    output_path = artifacts_dir / "release-summary.md"
    output_path.write_text(str(result), encoding="utf-8")
    console.print(
        f"[bold green]Run complete.[/] Summary saved to {output_path.resolve()}"
    )


if __name__ == "__main__":
    app()
