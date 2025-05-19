# 📄 main.py
# 🔖 Version: v1.0

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

    # 2. Parse raw logs into structured format
    parsed_logs = parse_raw_log(raw_logs)

    # 3. Evaluate event types
    event_results = []
    for log in parsed_logs:
        for rule in event_dsl:
            result = evaluate_event_type(log, rule)
            if result["result"] == "True":
                event_results.append(result)
                break  # Stop at first match
            elif result["result"] == "False":
                event_results.append(result)

    # 4. Evaluate policy compliance
    policy_results = [evaluate_policy(config_snapshot, rule) for rule in policy_dsl]

    # 5. Build sessions
    sessions = build_sessions(parsed_logs)

    # 6. Evaluate session roles
    session_roles = []
    for session in sessions:
        session_roles.extend(evaluate_role(session, session_role_dsl))

    # 7. Aggregate risk
    aggregate_result = aggregate_risk(event_results, policy_results, session_roles)

    # 8. Save result
    final_result = {
        "event_evaluation": event_results,
        "policy_evaluation": policy_results,
        "session_roles": session_roles,
        "risk_summary": aggregate_result
    }
    save_json("output/result.json", final_result)

    print("[+] Risk evaluation complete. Output saved to output/result.json")

if __name__ == "__main__":
    main()
