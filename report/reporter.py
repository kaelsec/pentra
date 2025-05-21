# 🔖 Version: v1.3
# 📄 File: pentra/reporter.py

import json
import os
from ai.llm import generate_narrative_with_gpt

def generate_mermaid_diagram(ttp_chain: list) -> str:
    """
    Generate a simple Mermaid diagram from a list of TTPs.
    Style-free for maximum compatibility with Mermaid renderers.
    """
    nodes = []
    links = []

    for idx, ttp in enumerate(ttp_chain):
        node_id = f"N{idx}"
        label = ttp.replace(" → ", "<br/>")
        nodes.append(f'{node_id}["{label}"]')
        if idx > 0:
            links.append(f"N{idx - 1} --> {node_id}")
    return "graph LR\n  " + "\n  ".join(nodes + links)


def generate_report(session_eval: dict) -> dict:
    """
    Generate full structured report for a single session evaluation result.
    Includes TTP chain, role sequence, confidence score, and Mermaid diagram.
    """
    ttp_chain = session_eval.get("ttp_chain", "").split(" → ")
    print(session_eval)
    report = {
        "session_key": session_eval.get("session_key"),
        "ttp_chain": session_eval.get("ttp_chain"),
        "unique_ttp_count": session_eval.get("unique_ttp_count"),
        "confidence": session_eval.get("confidence"),
        "role_sequence": session_eval.get("role_sequence"),
        "summary": session_eval.get("summary"),
        "schema_version": session_eval.get("schema_version", "v0.1"),
        "mermaid_diagram": generate_mermaid_diagram(ttp_chain),
        "narrative": generate_narrative(session_eval)
        # Future: "executive_summary": generate_summary_llm(session_eval)
    }

    return report


def save_reports(session_reports: list, output_path="output/report.json") -> None:
    """
    Save a list of structured session reports to a JSON file.
    Each report includes a Mermaid-safe diagram.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(session_reports, f, indent=2, ensure_ascii=False)

def generate_narrative(result: dict) -> str:
    try:
        return generate_narrative_with_gpt(result)
    except Exception:
        return "Narrative generation failed or is unavailable."