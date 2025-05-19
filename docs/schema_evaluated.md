
# 🧱 Pentra 2차 스키마 정의 (Evaluated Event Schema)
🔖 Version: v2.0  
📅 Last updated: 2025-05-18

---

## 📘 평가기 결과 필드 목록

| Field             | Type            | Description |
|------------------|------------------|-------------|
| `event_type_id`   | `str`            | 평가된 이벤트 타입 DSL ID (`EVT-001` 등) |
| `result`          | `str` (`True`/`False`) | 평가 결과 |
| `confidence`      | `float` (0.0–1.0) | 조건 평가 기반 신뢰도 |
| `ttps`            | `list[dict]`     | 매핑된 TTP 목록 (`id`, `score`, `mapped_by`) |
| `role`            | `str`            | 세션 내 역할 (`entrypoint`, `pivotable`, `expansion`) |
| `role_score`      | `float`          | 역할 평가 DSL에서 지정한 점수 |
| `role_explanation`| `str`            | 왜 해당 역할로 분류되었는지 설명 |
| `explanation`     | `str`            | 탐지 사유 또는 DSL 기반 설명 |
| `schema_version`  | `str`            | 스키마 버전 (`v2.0`) |

---

## 🗂 TTP 항목 구조 (`ttps` 필드)

```json
[
  {
    "id": "T1059.001",
    "score": 0.9,
    "from": "evaluate_event_type",
    "mapped_by": "DSL:v1.1"
  }
]
```

---

## 📌 사용 목적

- ✅ `evaluate_event_type()` 결과 구조
- ✅ TTP 기반 리포트/시각화에 활용
- ✅ session builder / aggregate risk 평가기의 입력 기반

---

## 📎 예시: 1차 + 2차 통합 결과

```json
{
  "timestamp": "2025-05-18T09:01:30Z",
  "src_ip": "192.168.1.5",
  "dst_ip": "10.0.0.2",
  "username": "user01",
  "process_name": "powershell.exe",
  "command_line": "powershell.exe -enc ...",
  "parent_proc": "winword.exe",
  "vendor": "velociraptor",
  "source_type": "event",

  "event_type_id": "EVT-001",
  "result": "True",
  "confidence": 1.0,
  "ttps": [
    {
      "id": "T1059.001",
      "score": 1.0,
      "from": "evaluate_event_type",
      "mapped_by": "DSL:v1.1"
    }
  ],
  "role": "entrypoint",
  "role_score": 0.9,
  "role_explanation": "Initial execution of PowerShell",
  "explanation": "Encoded PowerShell command from Word",
  "schema_version": "v2.0"
}
```

---

## 📂 파일 위치 제안

```
docs/
├── schema.md              # 1차 스키마
└── schema_evaluated.md    # 2차 스키마 (이 파일)
```
