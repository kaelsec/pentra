# 📄 File: utils/condition_eval.py
# 🔖 Version: v0.3-patch

def evaluate_conditions(event, condition_block):
    def _eval(block):
        if isinstance(block, list):
            results = [_eval(item) for item in block]
            matched = all(m for m, _ in results)
            confidence = sum(c for _, c in results) / len(results) if results else 0.0
            return matched, confidence

        if "all" in block:
            results = [_eval(item) for item in block["all"]]
            matched = all(m for m, _ in results)
            confidence = sum(c for _, c in results) / len(results) if results else 0.0
            return matched, confidence

        if "any" in block:
            results = [_eval(item) for item in block["any"]]
            matched = any(m for m, _ in results)
            confidence = max(c for m, c in results if m) if results else 0.0
            return matched, confidence

        # Base condition
        field = block.get("field")
        op = block.get("op")
        value = block.get("value")
        weight = block.get("weight", 1.0)

        actual = event.get(field)

        if op == "equals":
            return (actual == value, weight)
        if op == "contains":
            return (value in actual if actual else False, weight)
        if op == "startswith":
            return (actual.startswith(value) if actual else False, weight)
        if op == "endswith":
            return (actual.endswith(value) if actual else False, weight)
        if op == "in":
            return (actual in value if isinstance(value, list) else False, weight)
        if op == "regex":
            import re
            return (bool(re.search(value, actual)) if actual else False, weight)

        return False, 0.0

    return _eval(condition_block)
