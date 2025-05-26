from utils.condition_eval import evaluate_conditions
from evaluator.event_type import generate_explanation

def evaluate_policy(config: dict, policy_def: dict) -> dict:
    """
    Evaluate a system configuration snapshot against a single policy rule.
    Returns a structured policy evaluation result in Pentra v1.1 schema format.
    """

    eval_result = evaluate_conditions(config, policy_def.get("conditions", []))
    trace = eval_result.get("trace", [])
    explanation = generate_explanation(trace)

    return {
        "policy_id": policy_def.get("id"),
        "result": "True" if eval_result.get("matched") else "False",
        "confidence": round(eval_result.get("confidence") or 0.0, 3),
        "trace": trace,
        "explanation": explanation,
        "schema_version": "v1.1"
    }
