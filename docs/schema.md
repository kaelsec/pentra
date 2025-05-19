
# 🧱 Pentra 1차 스키마 정의 (Parsed Event Schema)
🔖 Version: v1.0  
📅 Last updated: 2025-05-18

---

## 📘 표준 필드 목록

| Field              | Type     | Description                                  |
|-------------------|----------|----------------------------------------------|
| `timestamp`        | `str`    | 이벤트 발생 시간 (ISO8601, `Z` 포함)          |
| `src_ip`           | `str`    | 출발지 IP                                     |
| `dst_ip`           | `str`    | 목적지 IP                                     |
| `username`         | `str`    | 사용자 식별자 (`user01`, 계정명 등)            |
| `vendor`           | `str`    | 로그 발생 시스템/벤더 (`velociraptor`, `pfsense`, `squid`) |
| `source_type`      | `str`    | 로그 유형 (`event`, `config`)                |
| `process_name`     | `str`    | 실행된 프로세스 이름                          |
| `command_line`     | `str`    | 전체 명령행 또는 스크립트                     |
| `parent_proc`      | `str`    | 부모 프로세스 이름                            |
| `protocol`         | `str`    | 네트워크 프로토콜 (`TCP`, `UDP`, ...)         |
| `destination_port` | `int`    | 목적지 포트                                   |
| `url`              | `str`    | 요청된 URL (웹/프록시 로그 등)                |
| `method`           | `str`    | HTTP 메서드 (`GET`, `POST`, ...)              |
| `status`           | `str`    | 응답 상태 또는 HTTP 코드 (`200`, `403` 등)     |

> ⚠️ 모든 필드는 선택적이며, 파서가 해당 값을 제공할 경우에만 포함됩니다.

---

## 📌 사용 목적

- ✅ DSL 조건 정의 기준
- ✅ 평가기 입력 기준
- ✅ 세션 구성 기준 (`src_ip`, `dst_ip`, `username`)
- ✅ 로그 정규화 및 후속 처리에서 벤더 독립성 확보

---

## 📂 파일 위치 제안

```
docs/
└── schema.md
```

---

## 📎 예시 이벤트

```json
{
  "timestamp": "2025-05-18T09:01:30Z",
  "src_ip": "192.168.1.5",
  "dst_ip": "10.0.0.2",
  "username": "user01",
  "vendor": "velociraptor",
  "source_type": "event",
  "process_name": "powershell.exe",
  "command_line": "powershell.exe -enc ...",
  "parent_proc": "winword.exe"
}
```



