# 📄 evaluator/aggregate.py
# 🔖 Version: v1.2

def aggregate_risk(event_results: list, policy_results: list, session_roles: list) -> dict:
    """
    Risk aggregation with 10-point normalized scoring.
    Weights: event(conf × 1), policy(crit × 2), session role (entrypoint 3, pivotable 2, expansion 1)
    """

    raw_score = 0.0
    max_score = 0.0
    reasons = []

    # 1. Events
    for event in event_results:
        if event.get("result") == "False":
            conf = float(event.get("confidence", 1.0))
            raw_score += conf * 1.0
            reasons.append(f"Event {event.get('event_type_id')} flagged (confidence: {conf})")
        max_score += 1.0  # per event

    # 2. Policies
    for policy in policy_results:
        crit = float(policy.get("criticality", 1.0))
        if policy.get("result") == "False":
            raw_score += crit * 2.0
            reasons.append(f"Policy {policy.get('policy_id')} violated (criticality: {crit})")
        max_score += crit * 2.0  # include full weight even if not violated

    # 3. Session roles
    role_weights = {"entrypoint": 3.0, "pivotable": 2.0, "expansion": 1.0}
    role_seen = set()

    for role in session_roles:
        r = role.get("role")
        if r in role_weights and r not in role_seen:
            raw_score += role_weights[r]
            reasons.append(f"Session has role '{r}' (weight: {role_weights[r]})")
            role_seen.add(r)

    max_score += sum(role_weights.values())  # max possible session score

    # Normalize to 10.0 scale
    normalized_score = (raw_score / max_score) * 10.0 if max_score > 0 else 0.0
    normalized_score = round(normalized_score, 2)

    # Risk level
    if normalized_score >= 7.0:
        risk_level = "High"
    elif normalized_score >= 4.0:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "risk_score": normalized_score,
        "risk_level": risk_level,
        "reasons": reasons,
        "schema_version": "v1.2"
    }
