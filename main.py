
import json
from utils.loader import load_yaml, load_json, save_json
from parser import parse_raw_log
from evaluator.event_type import evaluate_event_type
from evaluator.policy import evaluate_policy
from evaluator.role import evaluate_role
from evaluator.aggregate import aggregate_risk
from session.builder import build_sessions

def main():
    # 1. Load inputs
    raw_logs = load_json("logs/input.log")
    config_snapshot = load_json("configs/velociraptor_config.json")

    event_dsl = load_yaml("rules/event_type_definitions.yaml")
    policy_dsl = load_yaml("rules/policy_evaluation_rules.yaml")
    session_role_dsl = load_yaml("rules/session_roles.yaml")

    # 2. Parse raw logs
    parsed_logs = []
    for raw in raw_logs:
        try:
            raw_str = json.dumps(raw) if isinstance(raw, dict) else raw
            result = parse_raw_log(raw_str)
            if result:
                parsed_logs.append(result)
        except Exception as e:
            print(f"[!] Failed to parse log: {e}")

    # 3. Evaluate event types
    event_results = []
    for log in parsed_logs:
        best_result = None
        for rule in event_dsl["event_types"]:
            result = evaluate_event_type(log, rule)
            if result["result"] and (best_result is None or result["confidence"] > best_result["confidence"]):
                best_result = result
        if best_result:
            event_results.append(best_result)

    # 4. Policy evaluation
    policy_results = [evaluate_policy(config_snapshot, rule) for rule in policy_dsl]

    # 5. Session building
    sessions = build_sessions(event_results)

    # 6. Session role evaluation
    session_roles = []
    for session in sessions:
        session_roles.extend(evaluate_role(session, session_role_dsl))

    # 7. Aggregate risk
    aggregate_result = aggregate_risk(event_results, policy_results, session_roles)

    # 8. Save final report
    final_result = {
        "summary": "Evaluation completed over log dataset",
        "all_results": {
            "event": event_results,
            "session": session_roles,
            "policy": policy_results
        },
        "schema_version": "v1.2"
    }
    print('FINAL_RESULT_REPR_START')
    print(repr(final_result))
    print('FINAL_RESULT_REPR_END')
    save_json("output/result.json", final_result )

    print("[+] Risk evaluation complete. Output saved to output/result.json")

if __name__ == "__main__":
    main()
