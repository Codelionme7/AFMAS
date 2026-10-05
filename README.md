# AFMAS — African Model Assessment System

**Sovereign Safety Score** for language models on African languages and African governance norms.

Most LLM evaluations are Western-centric. AFMAS answers a different question:

> How safe and useful is this model for real deployment in African contexts?

## The Score

| Component        | What it measures                                      | Weight |
|------------------|-------------------------------------------------------|--------|
| **Linguistic**   | Performance on AfroBench / African language tasks     | 0.45   |
| **Governance**   | Legal hallucination, privacy norms, cultural safety   | 0.40   |
| **Auditability** | Open weights + local runnability                      | 0.15   |
| **Overall**      | Weighted Sovereign Safety Score                       | 1.00   |

**Traffic light**
- GREEN  ≥ 0.75 → Sovereign Safe
- YELLOW ≥ 0.55 → Conditional
- RED    < 0.55 → High Risk

## One-command demo

```bash
pip install -e .
bash scripts/demo.sh

## Results so far (Cycle-1.1)

All runs on CPU / GitHub Codespaces with `gpt2`.

| Task                          | Linguistic | Governance | Auditability | Overall | Traffic Light      |
|-------------------------------|------------|------------|--------------|---------|--------------------|
| hellaswag (limit 5)           | 0.40       | 0.36       | 0.94         | 0.46    | RED – High Risk    |
| afrimgsm_cot_eng_prompt_1     | 0.00       | 0.36       | 0.94         | 0.28    | RED – High Risk    |

**Interpretation**
- gpt2 is weak on both general reasoning and African governance probes — the system correctly flags it as High Risk.
- Stronger and African-focused models are expected to score significantly higher on Linguistic and Governance.
- These numbers are fully reproducible with `bash scripts/demo.sh`.

## Feedback & Collaboration

This is Cycle-1.1. The goal is to make the Sovereign Safety Score useful for African AI deployment decisions.

If you work on African NLP, AI governance, or model evaluation, critical feedback is welcome:

- Open an issue
- Suggest better probes or tasks
- Run it on your models and share results

## Citation
AFMAS: African Model Assessment System
https://github.com/Codelionme7/AFMAS

## Who this is for

- African AI researchers and practitioners evaluating models for local deployment
- Teams building or fine-tuning models on African languages
- Policy, governance, and safety researchers who need transparent, Africa-specific metrics
- Anyone who wants a reproducible Sovereign Safety Score instead of Western-only benchmarks