from evaluator.event_type import evaluate_event_type

def test_evt_001_positive():
    log = {"process_name": "powershell.exe", "command_line": "-enc 123"}
    rule = {
        "id": "EVT-001",
        "score_threshold": 0.9,
        "conditions": [
            {"field": "process_name", "op": "equals", "value": "powershell.exe", "weight": 0.5},
            {"field": "command_line", "op": "contains", "value": "-enc", "weight": 0.5}
        ],
        "mapped_ttps": [{"id": "T1059.001", "weight": 1.0}]
    }
    result = evaluate_event_type(log, rule)
    assert result["result"] == True
    assert result["confidence"] >= 0.9