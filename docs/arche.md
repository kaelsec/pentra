pentra/
├── main.py                         # 메인 실행 엔트리포인트
├── parser.py                       # 파서 라우터(parse_raw_log)
├── evaluator/
│   ├── __init__.py
│   ├── event_type.py               # evaluate_event_type()
│   ├── policy.py                   # evaluate_policy()
│   ├── role.py                     # evaluate_role()
│   └── aggregate.py                # aggregate_risk() (optional)
├── session/
│   ├── __init__.py
│   └── builder.py                  # build_sessions()
├── parsers/
│   ├── __init__.py
│   ├── pfsense.py                  # parse_pfsense()
│   ├── velociraptor.py             # parse_velociraptor()
│   └── squid.py                    # parse_squid() (추가 예정)
├── utils/
│   ├── __init__.py
│   ├── loader.py                   # load_logs(), load_configs()
│   └── condition_eval.py           # evaluate_condition() (eval wrapper)
├── rules/
│   └── policy_evaluation_rules.yaml  # 정책 감사 기준 YAML
├── configs/
│   └── velociraptor_config.json   # 테스트용 정책 스냅샷 샘플
├── logs/
│   └── input.log                  # 테스트용 raw 로그 입력
├── output/
│   └── result.json                # 평가 결과 저장 (예정)
├── README.md                      # GitHub 프로필용 소개
└── requirements.txt               # 의존 패키지 리스트 (예: PyYAML 등)


main.py
  ↓
load_logs()         ← utils.loader
  ↓
parse_raw_log()     ← parser.py → parsers/*
  ↓
evaluate_*()        ← evaluator/*
  ↓
build_sessions()    ← session.builder
  ↓
generate_report()   ← (후속)
