# 🔖 Version: v0.3
# 📄 File: ai/llm.py

import os
import openai

try:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    client = None

def generate_narrative_with_gpt(session_eval: dict) -> str:
    if not client:
        return "[Narrative generation skipped: Missing or invalid OpenAI API client]"

    try:
        prompt = make_prompt_from_result(session_eval)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a cybersecurity analyst. Write a clear, professional narrative based on session evaluation data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[Narrative generation failed: {str(e)}]"

def make_prompt_from_result(result: dict) -> str:
    session_key = result.get("session_key", "unknown_session")
    ttp_chain = result.get("ttp_chain", "")
    roles = result.get("role_sequence", [])
    summary = result.get("summary", "")
    confidence = result.get("confidence", 0.0)

    return (
        f"Session ID: {session_key}\n"
        f"TTP Chain: {ttp_chain}\n"
        f"Role Sequence: {', '.join(roles)}\n"
        f"Summary: {summary}\n"
        f"Confidence Score: {confidence}\n\n"
        "Generate a narrative suitable for a security report explaining this session's behavior and potential risk."
    )
