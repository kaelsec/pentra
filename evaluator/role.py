# 📄 File: evaluator/role.py
# 🔖 Version: v0.3
from utils.condition_eval import evaluate_conditions
from evaluator.event_type import generate_explanation  # 재사용

def evaluate_role(events, role_rules: list):
    """
    Assign roles to session events using a list of DSL rules.
    Each event is evaluated against role rules; first matching rule wins.
    """
    for event in events:
        event['role'] = None
        event['role_score'] = 0
        event['role_explanation'] = ""
        event['role_trace'] = []

        for rule in role_rules:
            if rule.get("domain") and rule.get("domain") != event.get("source_type"):
                continue
            if rule.get("vendor") and rule.get("vendor") != event.get("vendor"):
                continue

            role_name = rule.get('role_name')
            conditions = rule.get('conditions', {})
            default_score = rule.get('score', 0)

            eval_result = evaluate_conditions(event, conditions)
            matched = eval_result.get("matched", False)
            trace = eval_result.get("trace", [])
            explanation = generate_explanation(trace)

            if matched:
                event['role'] = role_name
                event['role_score'] = default_score
                event['role_explanation'] = explanation
                event['role_trace'] = trace
                break  # First-match win

    role_summary = {
        'entrypoint': sum(1 for e in events if e.get('role') == 'entrypoint'),
        'pivotable': sum(1 for e in events if e.get('role') == 'pivotable'),
        'expansion': sum(1 for e in events if e.get('role') == 'expansion'),
    }
    role_sequence = [e['role'] for e in events if e.get('role')]

    return events, {
        'role_sequence': role_sequence,
        'role_summary': role_summary,
    }
