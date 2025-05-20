from main import main

def test_scenario_3_executes():
    result = main(input_path="logs/scenario_3_ai_phishing_rce.json", output_path="output/scenario3.json")
    assert "role_sequence" in result[0]