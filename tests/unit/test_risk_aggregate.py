from evaluator.aggregate import aggregate_risk

def test_high_risk_scenario():
    session_eval = {
        "ttp_chain": "T1059.001 → T1003",
        "role_sequence": "entrypoint → pivotable",
        "confidence": 0.95
    }
    result = aggregate_risk(session_eval)
    assert result["risk_level"] == "High"
