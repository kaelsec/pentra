from main import main

def test_scenario_1_executes():
    result = main(input_path="logs/scenario_1_weaponized_doc.json", output_path="output/scenario1.json")
    assert "session_key" in result[0]