
# 📄 session/evaluator.py
# 🔖 Version: v0.2 - Patched for correct TTP chaining

def evaluate_ttp_chain(session: dict) -> dict:
    """
    Analyze a session and produce a TTP chain based on mapped_ttps in its events.
    """
    events = session.get("events", [])
    unique_ttps = []
    role_seq = []
    total_conf = 0.0
    ttp_seen = set()

    for event in events:
        role = event.get("role")
        role_seq.append(role)

        for ttp in event.get("mapped_ttps", []):
            ttp_id = ttp.get("id")
            if ttp_id and ttp_id not in ttp_seen:
                unique_ttps.append(ttp_id)
                ttp_seen.add(ttp_id)

        conf = event.get("confidence")
        if conf:
            total_conf += float(conf)

    avg_conf = round(total_conf / len(unique_ttps), 3) if unique_ttps else 0.0

    return {
        "session_key": session.get("session_key"),
        "ttp_chain": " → ".join(unique_ttps),
        "unique_ttp_count": len(unique_ttps),
        "confidence": avg_conf,
        "role_sequence": " → ".join(filter(None, role_seq)),
        "summary": f"{len(unique_ttps)} unique TTPs chained",
        "schema_version": "v0.1"
    }
