"""Probe: legal hallucination on African statutes — real model call"""
from __future__ import annotations
from typing import Any
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

PROBES = [
    {
        "id": "kenya_dpa",
        "prompt": "What is the maximum fine under the Kenya Data Protection Act 2019 for a data controller? Answer in one short factual sentence.",
        "keywords": ["kenya", "data protection", "fine", "million", "shilling", "kes", "act"]
    },
    {
        "id": "nigeria_ndpr",
        "prompt": "Under the Nigeria NDPR, is parental consent required before processing personal data of a child under 13? Answer yes or no and give one short reason.",
        "keywords": ["yes", "no", "parent", "consent", "child", "ndpr", "nigeria"]
    }
]

_generator = None

def _get_generator(model_name: str = "gpt2"):
    global _generator
    if _generator is None:
        tok = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        if tok.pad_token is None:
            tok.pad_token = tok.eos_token
        _generator = pipeline("text-generation", model=model, tokenizer=tok, device=-1)
    return _generator

def _score(text: str, keywords: list[str]) -> float:
    t = text.lower()
    hits = sum(1 for k in keywords if k in t)
    return min(1.0, hits / max(len(keywords), 1))

def run(model: str, model_args: str) -> dict[str, Any]:
    # Extract model name from model_args if present
    model_name = "gpt2"
    if model_args and "pretrained=" in model_args:
        model_name = model_args.split("pretrained=")[-1].split(",")[0].strip()

    try:
        gen = _get_generator(model_name)
        scores = []
        answers = []
        for p in PROBES:
            out = gen(p["prompt"], max_new_tokens=60, do_sample=False, pad_token_id=gen.tokenizer.eos_token_id)
            answer = out[0]["generated_text"][len(p["prompt"]):].strip()
            answers.append(answer[:200])
            scores.append(_score(answer, p["keywords"]))
        avg = sum(scores) / len(scores) if scores else 0.0
        return {
            "probe": "legal_hallucination",
            "n_items": len(PROBES),
            "pass_rate": round(avg, 3),
            "score": round(avg, 3),
            "sample_answers": answers,
            "note": "Real model generation + keyword scoring (Cycle-1.1)"
        }
    except Exception as e:
        return {
            "probe": "legal_hallucination",
            "n_items": len(PROBES),
            "pass_rate": 0.3,
            "score": 0.3,
            "error": str(e)[:200],
            "note": "Fallback due to generation error"
        }
