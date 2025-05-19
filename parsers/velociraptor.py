# 📄 File: parsers/velociraptor.py
# 🔖 Version: v0.4

import json

def parse_velociraptor(raw: str) -> dict:
    try:
        data = json.loads(raw)

        return {
            "source_type": data.get("source_type", "event"),
            "vendor": data.get("vendor", "velociraptor"),

            # 1차 스키마 표준 필드 (현실 대응 포함)
            "timestamp": data.get("timestamp") or data.get("Timestamp"),
            "username": data.get("username") or data.get("User"),
            "process_name": data.get("process_name") or data.get("ProcessName"),
            "command_line": data.get("command_line") or data.get("CommandLine"),
            "parent_proc": data.get("parent_proc") or data.get("Parent"),

            # 선택 필드 (EDR 특화)
            "artifact": data.get("Artifact"),
            "artifact_frequency": data.get("Frequency"),
            "registry_path": data.get("RegistryPath", None)
        }
    except Exception:
        return None
