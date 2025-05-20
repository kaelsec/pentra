# 📄 File: parsers/squid.py
# 🔖 Version: v0.3-patch

from datetime import datetime

def parse_squid(line: str) -> dict:
    parts = line.strip().split()

    if len(parts) < 9:
        return None  # 불완전한 로그

    try:
        ts_unix = float(parts[0])
        timestamp = datetime.utcfromtimestamp(ts_unix).isoformat() + "Z"

        client_ip = parts[2]
        status = parts[3]
        method = parts[5]
        url = parts[6]
        username = parts[7]
        hierarchy = parts[8]

        dst_ip = None
        if "/" in hierarchy:
            _, dst_ip = hierarchy.split("/", 1)

        return {
            "source_type": "proxy",     # ✅ 수정됨
            "vendor": "squid",
            "timestamp": timestamp,
            "client_ip": client_ip,     # ✅ 추가됨
            "dst_ip": dst_ip or None,
            "username": username,
            "url": url,
            "method": method,
            "status": status
        }

    except Exception:
        return None
