
import json
from utils.loader import load_yaml, load_json, save_json, clean_json
from parser import parse_raw_log
from evaluator.event_type import evaluate_event_type
from evaluator.policy import evaluate_policy
from evaluator.role import evaluate_role
from evaluator.aggregate import aggregate_risk
from session.builder import build_sessions
from session.evaluator import evaluate_ttp_chain

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
            #raw_str = json.dumps(raw) if isinstance(raw, dict) else raw
            result = parse_raw_log(raw)
            if result:
                parsed_logs.append(result)
        except Exception as e:
            print(f"[!] Failed to parse log: {e}")

    # 3. Evaluate event types
    event_results = []
    for log in parsed_logs:
        for rule in event_dsl["event_types"]:
            result = evaluate_event_type(log, rule)
            if result["result"]:
                event_results.append(result)



    # 4. Policy evaluation
    policy_results = [evaluate_policy(config_snapshot, rule) for rule in policy_dsl]

    # 5. Build sessions from raw parsed logs (not evaluated events!)
    sessions = build_sessions(parsed_logs)  #  원본 로그에서 세션 빌드

    # 6. Session role evaluation
    session_results = []
    for session in sessions:
        events_with_roles, role_info = evaluate_role(session["events"], session_role_dsl)
        ttp_info = evaluate_ttp_chain(session)

        session_results.append({
            **session,
            "events": events_with_roles,
            **role_info,
            **ttp_info
        })
    # 7. Aggregate risk
    aggregate_result = aggregate_risk(event_results, policy_results, session_results)

    # 8. Save final report
    final_result = {
        "summary": "Evaluation completed over log dataset",
        "all_results": {
            "event": event_results,
            "session": session_results,
            "policy": policy_results
        },
        "schema_version": "v1.2"
    }
    save_json("output/result.json", clean_json(final_result))

    print("[+] Risk evaluation complete. Output saved to output/result.json")

if __name__ == "__main__":
    main()
