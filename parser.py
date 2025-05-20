# 📄 File: parser.py
# 🔖 Version: v0.3

import json
from parsers.pfsense import parse_pfsense
from parsers.velociraptor import parse_velociraptor
from parsers.squid import parse_squid

def parse_raw_log(raw: str) -> dict:
    """
    Determine the appropriate parser based on content and return structured event.
    Supports: pfSense, Velociraptor, Squid Proxy, Config Snapshots
    """
    raw_lower = raw.lower()

    # ✅ pfSense 로그 (syslog + filterlog 기반)
    if "filterlog" in raw_lower:
        return parse_pfsense(raw)

    # ✅ Velociraptor JSONL 로그
    try:
        parsed = json.loads(raw)

        if "Artifact" in parsed and "ProcessName" in parsed:
            return parse_velociraptor(raw)

        # ✅ 현실형 Velociraptor 대응
        if parsed.get("source_type") == "edr" or parsed.get("vendor") == "velociraptor":
            return parse_velociraptor(raw)

        # ✅ 정책 config는 그대로 넘김
        if parsed.get("source_type") == "config":
            return parsed

    except Exception:
        pass

    # ✅ Squid 로그 (UNIX timestamp + HTTP + URL)
    if "http" in raw_lower and any(method in raw for method in ["GET", "POST", "CONNECT"]):
        return parse_squid(raw)

    return None  # 인식되지 않은 로그
