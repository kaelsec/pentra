from session.evaluator import evaluate_ttp_chain

def test_chain_generation():
    session = {
        "session_key": "s1",
        "events": [
            {"mapped_ttps": [{"id": "T1059.001"}]},
            {"mapped_ttps": [{"id": "T1003"}]},
        ],
        "role_sequence": ["entrypoint", "pivotable"]
    }
    result = evaluate_ttp_chain(session)
    assert result["ttp_chain"] == "T1059.001 → T1003"
