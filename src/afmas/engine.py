"""Evaluation engine"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from typing import Any
from rich.console import Console

console = Console()
CURATED = ["hellaswag", "arc_easy", "afrimmlu", "afrixnli", "belebele"]

def list_available_tasks() -> list[str]:
    try:
        out = subprocess.check_output(
            [sys.executable, "-m", "lm_eval", "ls", "tasks"],
            text=True, stderr=subprocess.DEVNULL, timeout=60)
        afro = [line.strip() for line in out.splitlines()
                if any(k in line.lower() for k in ("afri","afro","belebele","masakha","hellaswag"))]
        return sorted(set(CURATED + afro)) or CURATED
    except Exception:
        return CURATED

def run_evaluation(model, model_args, tasks, limit, num_fewshot, device, batch_size, output_dir, run_custom_probes=True):
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "lm_eval", "--model", model,
           "--tasks", ",".join(tasks), "--num_fewshot", str(num_fewshot),
           "--device", device, "--batch_size", str(batch_size),
           "--output_path", str(out_dir / "lm_eval"), "--log_samples"]
    if model_args: cmd.extend(["--model_args", model_args])
    if limit is not None: cmd.extend(["--limit", str(limit)])
    console.print(f"[dim]Running: {' '.join(cmd)}[/]")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        if proc.returncode != 0:
            console.print(f"[yellow]lm-eval stderr (tail):[/]\n{proc.stderr[-1500:]}")
    except subprocess.TimeoutExpired:
        console.print("[red]lm-eval timed out[/]")
        proc = None
    results = {"model": model, "model_args": model_args, "tasks": tasks,
               "limit": limit, "lm_eval_returncode": getattr(proc, "returncode", None),
               "task_results": {}, "custom_probes": {}}
    for p in (out_dir / "lm_eval").rglob("results*.json"):
        try:
            data = json.loads(p.read_text())
            results["task_results"] = data.get("results", data)
            break
        except Exception: pass
    if run_custom_probes:
        from afmas.guardrails.legal_hallucination import run as run_legal
        from afmas.guardrails.privacy_norms import run as run_privacy
        from afmas.guardrails.cultural_safety import run as run_cultural
        results["custom_probes"]["legal_hallucination"] = run_legal(model, model_args)
        results["custom_probes"]["privacy_norms"] = run_privacy(model, model_args)
        results["custom_probes"]["cultural_safety"] = run_cultural(model, model_args)
    (out_dir / "raw_results.json").write_text(json.dumps(results, indent=2))
    return results
