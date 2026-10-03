"""AFMAS CLI"""
from __future__ import annotations
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def main():
    """AFMAS — African Model Assessment System"""
    pass

@main.command()
@click.option("--model", required=True, help="Backend: hf | openai")
@click.option("--model_args", default="", help="model_args for lm-eval")
@click.option("--tasks", default="hellaswag", help="Comma-separated tasks")
@click.option("--limit", default=None, type=int)
@click.option("--num_fewshot", default=0, type=int)
@click.option("--output_dir", default="results", type=click.Path())
@click.option("--device", default="cpu")
@click.option("--batch_size", default="1")
@click.option("--run_custom_probes/--no-custom", default=True)
def evaluate(model, model_args, tasks, limit, num_fewshot, output_dir, device, batch_size, run_custom_probes):
    """Run evaluation and produce Sovereign Safety Score"""
    from afmas.engine import run_evaluation
    from afmas.scoring import compute_sovereign_score
    from afmas.report import write_report

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    console.print(f"[bold]AFMAS evaluate[/] model={model} tasks={tasks} limit={limit}")

    results = run_evaluation(
        model=model,
        model_args=model_args,
        tasks=tasks.split(","),
        limit=limit,
        num_fewshot=num_fewshot,
        device=device,
        batch_size=batch_size,
        output_dir=str(output_path),
        run_custom_probes=run_custom_probes,
    )

    score = compute_sovereign_score(results)
    report_path = write_report(results, score, output_path)

    table = Table(title="Sovereign Safety Score (v0)")
    table.add_column("Component")
    table.add_column("Value", justify="right")
    table.add_row("Overall Score", f"{score['overall']:.3f}")
    table.add_row("Linguistic", f"{score['linguistic']:.3f}")
    table.add_row("Governance", f"{score['governance']:.3f}")
    table.add_row("Auditability", f"{score['auditability']:.3f}")
    table.add_row("Traffic light", score["traffic_light"])
    console.print(table)
    console.print(f"[green]Report → {report_path}[/]")

@main.command("list-tasks")
def list_tasks():
    from afmas.engine import list_available_tasks
    for t in list_available_tasks():
        console.print(f"  • {t}")

if __name__ == "__main__":
    main()
