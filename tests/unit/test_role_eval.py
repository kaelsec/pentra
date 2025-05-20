from evaluator.role import evaluate_role

def test_entrypoint_role_match():
    logs = [{"process_name": "powershell.exe", "parent_proc": "winword.exe"}]
    result = evaluate_role(logs)
    assert "entrypoint" in result["role_summary"]
