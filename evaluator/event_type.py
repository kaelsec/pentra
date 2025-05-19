# 📄 File: evaluator/event_type.py
# 🔖 Version: v2.1 (schema-aligned)

from utils.condition_eval import evaluate_conditions

def evaluate_event_type(log: dict, event_def: dict) -> dict:
    """
    Evaluate a log event against a single DSL-defined event_type.
    Returns structured evaluation result in Pentra v2.0 schema format.
    """

    matched, confidence = evaluate_conditions(log, event_def["conditions"])

    base_result = {
        "event_type_id": event_def.get("id"),
        "event_type": event_def.get("name", ""),  # 🔄 리포트 친화적 필드 (선택)
        "confidence": round(confidence, 3),
        "explanation": event_def.get("meta", {}).get("explanation", ""),
        "schema_version": "v2.0",
        "ttps": [],
        "result": "False"
    }

    if not matched or confidence < event_def.get("score_threshold", 1.0):
        return base_result

    mapped_ttps = []
    for ttp in event_def.get("mapped_ttps", []):
        ttp_id = ttp.get("id")
        weight = ttp.get("weight", 1.0)
        score = round(weight * confidence, 3)

        mapped_ttps.append({
            "id": ttp_id,
            "score": score,
            "from": "evaluate_event_type",
            "mapped_by": f'DSL:{event_def.get("schema_version", "v1.1")}'
        })

    base_result["ttps"] = mapped_ttps
    base_result["result"] = "True"
    return base_result
