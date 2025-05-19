# 📄 evaluator/policy.py
# 🔖 Version: v1.0

from utils.condition_eval import evaluate_conditions

def evaluate_policy(config: dict, policy_def: dict) -> dict:
    """
    Evaluate a system configuration snapshot against a single policy rule.
    Returns a structured policy evaluation result in Pentra v1.0 schema format.
    """
    matched, _ = evaluate_conditions(config, policy_def.get("conditions", []))

    return {
        "policy_id": policy_def.get("id"),
        "result": "True" if matched else "False",
        "explanation": policy_def.get("explanation", ""),
        "schema_version": "v1.0"
    }
