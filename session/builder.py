
# 📄 session/builder.py
# 🔖 Version: v1.2 - Time Window + Flexible Session Keying

import uuid
from datetime import datetime, timedelta
from typing import List, Dict


def parse_time(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def get_session_key(log: dict) -> str:
    """
    Flexible session key builder with fallback priorities:
    username > client_ip > src_ip > dst_ip > fallback 'NA'
    """
    return f"{log.get('username', 'NA')}::{log.get('client_ip', log.get('src_ip', 'NA'))}::{log.get('dst_ip', 'NA')}"


def build_sessions(events: List[dict], window_minutes: int = 2) -> List[Dict]:
    """
    Group events into sessions based on timestamp proximity and identity (2 min window).
    """
    sessions = []
    events_sorted = sorted(events, key=lambda e: parse_time(e.get("timestamp")) or datetime.min)

    current_session = None

    for event in events_sorted:
        ts = parse_time(event.get("timestamp"))
        if not ts:
            continue

        key = get_session_key(event)

        if not current_session:
            current_session = {
                "session_id": str(uuid.uuid4()),
                "session_key": key,
                "events": [event],
                "start_time": ts,
                "end_time": ts
            }
            continue

        if key == current_session["session_key"] and ts - current_session["end_time"] <= timedelta(minutes=window_minutes):
            current_session["events"].append(event)
            current_session["end_time"] = ts
        else:
            sessions.append(current_session)
            current_session = {
                "session_id": str(uuid.uuid4()),
                "session_key": key,
                "events": [event],
                "start_time": ts,
                "end_time": ts
            }

    if current_session:
        sessions.append(current_session)


    return sessions
