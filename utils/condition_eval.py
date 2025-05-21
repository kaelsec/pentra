import re

def evaluate_conditions(event, condition_block):
    """
    Evaluate a nested condition block (DSL format) against a single log event.
    Returns (matched: bool, confidence: float)
    """

    def _eval(block):
        # --- list of conditions (default to AND)
        if isinstance(block, list):
            results = [_eval(item) for item in block]
            weights = [w for _, w in results if w is not None]
            matched = all(m for m, _ in results)
            confidence = sum(weights) / len(weights) if weights else 0.0
            return matched, confidence

        # --- explicit "all" block
        if "all" in block:
            results = [_eval(item) for item in block["all"]]
            weights = [w for _, w in results if w is not None]
            matched = all(m for m, _ in results)
            confidence = sum(weights) / len(weights) if weights else 0.0
            return matched, confidence

        # --- explicit "any" block
        if "any" in block:
            results = [_eval(item) for item in block["any"]]
            matched_items = [(m, c) for m, c in results if m]
            matched = bool(matched_items)
            confidence = max(c for _, c in matched_items) if matched_items else 0.0
            return matched, confidence

        # --- base condition
        field = block.get("field")
        op = block.get("op")
        value = block.get("value")
        weight = block.get("weight", 1.0)

        actual = event.get(field)
        if actual is None:
            return False, None

        actual = str(actual).lower()
        value = str(value).lower()

        match = False
        if op == "equals":
            match = actual == value
        elif op == "contains":
            match = value in actual
        elif op == "startswith":
            match = actual.startswith(value)
        elif op == "endswith":
            match = actual.endswith(value)
        elif op == "in":
            match = actual in value if isinstance(value, list) else False
        elif op == "regex":
            match = bool(re.search(value, actual))

        return match, weight if match else 0.0

    return _eval(condition_block)
