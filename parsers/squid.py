# 📄 File: parsers/squid.py
# 🔖 Version: v0.2

from datetime import datetime

def parse_squid(line: str) -> dict:
    parts = line.strip().split()

    if len(parts) < 9:
        return None  # 불완전한 로그

    try:
        # UNIX timestamp → ISO 8601 변환
        ts_unix = float(parts[0])
        timestamp = datetime.utcfromtimestamp(ts_unix).isoformat() + "Z"

        src_ip = parts[2]
        status = parts[3]           # e.g., TCP_MISS/200
        method = parts[5]           # HTTP method
        url = parts[6]
        username = parts[7]
        hierarchy = parts[8]        # e.g., HIER_DIRECT/10.0.0.2

        dst_ip = None
        if "/" in hierarchy:
            _, dst_ip = hierarchy.split("/", 1)

        return {
            "source_type": "event",
            "vendor": "squid",
            "timestamp": timestamp,

            # Pentra 1차 스키마 표준 필드
            "src_ip": src_ip,
            "dst_ip": dst_ip or None,
            "username": username,
            "url": url,
            "method": method,
            "status": status
        }

    except Exception:
        return None
