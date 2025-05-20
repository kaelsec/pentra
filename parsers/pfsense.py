# 📄 File: parsers/pfsense.py
# 🔖 Version: v0.4 (Pentra Skema Aligned)

from datetime import datetime

def parse_pfsense(raw: str) -> dict:
    try:
        syslog_part, log_part = raw.split("filterlog: ")
        fields = log_part.strip().split(",")

        # 날짜 변환: May 18 09:01:15 → ISO 포맷으로
        timestamp_tokens = syslog_part.strip().split()
        month_str = timestamp_tokens[1]
        day = timestamp_tokens[2]
        time = timestamp_tokens[3]

        # 연도 추가
        month_number = {
            "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
            "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
            "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
        }[month_str]

        now_year = datetime.utcnow().year
        timestamp = f"{now_year}-{month_number}-{day}T{time}Z"

        return {
            "source_type": "fw",            # ✅ 수정
            "vendor": "pfsense",
            "timestamp": timestamp,         # ✅ ISO 8601

            # Pentra 스키마 필드
            "src_ip": fields[4],
            "dst_ip": fields[5],
            "dst_port": int(fields[6]) if fields[6].isdigit() else None,
            "protocol": fields[8],
            "action": fields[9],
            "username": fields[10] if len(fields) > 10 else None
        }

    except Exception:
        return None
