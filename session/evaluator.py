# 🔖 Version: v0.1
# 📄 File: session/evaluator.py

def evaluate_ttp_chain(session: dict) -> dict:
    """
    Analyze a session's TTP chaining behavior and return a summary.

    Args:
        session (dict): A session object with evaluated 'events'

    Returns:
        dict: {
            ttp_chain: 'T1059 → T1566 → ...',
            confidence: 0.86,
            unique_ttp_count: 3,
            role_sequence: 'entrypoint → pivotable → ...',
            summary: '3 unique TTPs chained',
            schema_version: 'v0.1'
        }
    """
    ttp_sequence = []
    for event in session.get("events", []):
        for ttp in event.get("ttps", []):
            ttp_sequence.append(ttp)

    seen = set()
    unique_ttps = [x for x in ttp_sequence if not (x in seen or seen.add(x))]

    role_seq = [e.get("role", "unknown") for e in session.get("events", [])]
    confidence = round(min(1.0, len(unique_ttps) / 5), 2)

    return {
        "session_key": session.get("session_key"),  # ✅ 포함
        "ttp_chain": " → ".join(unique_ttps),
        "unique_ttp_count": len(unique_ttps),
        "confidence": confidence,
        "role_sequence": " → ".join(role_seq),
        "summary": f"{len(unique_ttps)} unique TTPs chained",
        "schema_version": "v0.1"
    }