from main import main

def test_scenario_2_executes():
    result = main(input_path="logs/scenario_2_lolbin_etw_bypass.json", output_path="output/scenario2.json")
    assert "ttp_chain" in result[0]