# 📄 File: evaluator/role.py
# 🔖 Version: v0.3
from utils.condition_eval import evaluate_conditions

def evaluate_role(events, role_rules: list):
    """
    Assign roles to session events using a list of DSL rules.
    Each event is evaluated against role rules; first matching rule wins.
    """
    for event in events:
        event['role'] = None
        event['role_score'] = 0
        event['role_explanation'] = ""

        for rule in role_rules:
            role_name = rule.get('role_name')
            conditions = rule.get('conditions', {})
            explanation = rule.get('explanation', '')
            score = rule.get('score', 0)

            matched, _ = evaluate_conditions(event, conditions)

            if matched:
                event['role'] = role_name
                event['role_score'] = score
                event['role_explanation'] = explanation
                break  # Stop after first match

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
