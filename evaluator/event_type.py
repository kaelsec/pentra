# 📄 File: evaluator/event_type.py
# 🔖 Version: v2.2 (schema-aligned)
from utils.condition_eval import evaluate_conditions

def evaluate_event_type(log: dict, event_def: dict) -> dict:
    """
    Evaluate a log event against a single DSL-defined event_type.
    Returns structured evaluation result in Pentra v2.2 schema format.
    """

    eval_result = evaluate_conditions(log, event_def["conditions"])
    trace = eval_result.get("trace", [])
    generated_explanation = generate_explanation(trace)

    base_result = {
        "event_type_id": event_def.get("id"),
        "event_type": event_def.get("name", ""),
        "confidence": round(eval_result["confidence"] or 0.0, 3),
        "trace": trace,
        "explanation": generated_explanation,
        "schema_version": "v2.2",
        "mapped_ttps": [],
        "result": False
    }

    # confidence 기반 판단 로직 유지
    if eval_result["confidence"] is None or eval_result["confidence"] < event_def.get("score_threshold", 1.0):
        return base_result

    # TTP 매핑 점수 계산
    mapped_ttps = []
    for ttp in event_def.get("mapped_ttps", []):
        ttp_id = ttp.get("id")
        weight = ttp.get("weight", 1.0)
        score = round(weight * eval_result["confidence"], 3)

        mapped_ttps.append({
            "id": ttp_id,
            "score": score,
            "from": "evaluate_event_type",
            "mapped_by": f'DSL:{event_def.get("schema_version", "v1.1")}'
        })

    base_result["mapped_ttps"] = mapped_ttps
    base_result["result"] = True
    base_result.update(log)

    return base_result



def generate_explanation(trace: list) -> str:
    if not trace:
        return "No matching conditions evaluated."

    matched = [t for t in trace if t["matched"]]
    total = len(trace)

    explanation_lines = []

    explanation_lines.append(f"Matched {len(matched)} of {total} conditions.")

    for t in trace:
        symbol = "✓" if t["matched"] else "✗"
        explanation_lines.append(
            f"{symbol} {t['field']} {t['op']} {t['value']} (actual: {t['actual']})"
        )

    return "\n".join(explanation_lines)