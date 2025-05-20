from evaluator.policy import evaluate_policy

def test_insecure_setting_detected():
    snapshot = {"password_expiry": False}
    rule = {
        "field": "password_expiry",
        "op": "equals",
        "value": True,
        "explanation": "Password expiration should be enabled"
    }
    result = evaluate_policy(snapshot, rule)
    assert result["result"] == False