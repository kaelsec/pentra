# 📄 File: parsers/pfsense.py
# 🔖 Version: v0.3

def parse_pfsense(raw: str) -> dict:
    try:
        # 예: <134>May 18 09:01:15 firewall filterlog: 1,,,igb0,192.168.1.5,10.0.0.2,443,,TCP,pass,user01
        syslog_part, log_part = raw.split("filterlog: ")
        fields = log_part.strip().split(",")

        # syslog timestamp (예: May 18 09:01:15)
        timestamp_tokens = syslog_part.strip().split()
        timestamp = " ".join(timestamp_tokens[1:4])  # skip priority

        return {
            "source_type": "event",
            "vendor": "pfsense",
            "timestamp": timestamp,

            # 1차 스키마 필드
            "protocol": fields[8],
            "src_ip": fields[4],
            "dst_ip": fields[5],
            "destination_port": int(fields[6]) if fields[6].isdigit() else None,
            "action": fields[9],
            "username": fields[10] if len(fields) > 10 else None
        }
    except Exception:
        return None