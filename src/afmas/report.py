"""Report generation — JSON, CSV, HTML"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import pandas as pd

def write_report(results: dict[str, Any], score: dict[str, Any], output_dir: Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    payload = {"generated_at": stamp, "score": score, "results": results}

    json_path = output_dir / f"afmas_report_{stamp}.json"
    json_path.write_text(json.dumps(payload, indent=2, default=str))

    rows = [
        {"component": "overall", "value": score["overall"]},
        {"component": "linguistic", "value": score["linguistic"]},
        {"component": "governance", "value": score["governance"]},
        {"component": "auditability", "value": score["auditability"]},
        {"component": "traffic_light", "value": score["traffic_light"]},
    ]
    pd.DataFrame(rows).to_csv(output_dir / f"afmas_summary_{stamp}.csv", index=False)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>AFMAS Report</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:720px;margin:2rem auto;padding:0 1rem}}
.score{{font-size:2.5rem;font-weight:700}}
table{{border-collapse:collapse;width:100%;margin-top:1.5rem}}
td,th{{border:1px solid #ddd;padding:.5rem .75rem;text-align:left}}
</style></head><body>
<h1>AFMAS Sovereign Safety Report</h1>
<p>Generated: {stamp}</p>
<div class="score">{score['overall']:.3f}</div>
<p><strong>{score['traffic_light']}</strong></p>
<table>
<tr><th>Component</th><th>Score</th></tr>
<tr><td>Linguistic</td><td>{score['linguistic']:.3f}</td></tr>
<tr><td>Governance</td><td>{score['governance']:.3f}</td></tr>
<tr><td>Auditability</td><td>{score['auditability']:.3f}</td></tr>
</table>
<p style="margin-top:2rem;color:#666;font-size:.9rem">
Weights in configs/scoring_weights.yaml. Cycle-1 prototype.
</p></body></html>"""
    (output_dir / f"afmas_report_{stamp}.html").write_text(html)
    return json_path
