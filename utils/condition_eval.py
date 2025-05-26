import re

def evaluate_conditions(event, condition_block):
    trace = []

    def _eval(block):
        nonlocal trace

        if isinstance(block, list):
            results = [_eval(item) for item in block]
            weights = [r["confidence"] for r in results if r["confidence"] is not None]
            matched = all(r["matched"] for r in results)
            confidence = sum(weights) / len(weights) if weights else 0.0
            all_traces = [r["trace"] for r in results]
            return {
                "matched": matched,
                "confidence": confidence,
                "trace": [t for tr in all_traces for t in tr]
            }

        if "all" in block:
            return _eval(block["all"])

        if "any" in block:
            results = [_eval(item) for item in block["any"]]
            matched_items = [r for r in results if r["matched"]]
            matched = bool(matched_items)
            confidence = max(r["confidence"] for r in matched_items) if matched_items else 0.0
            any_traces = [r["trace"] for r in results]
            return {
                "matched": matched,
                "confidence": confidence,
                "trace": [t for tr in any_traces for t in tr]
            }

        # base condition
        field = block.get("field")
        op = block.get("op")
        value = block.get("value")
        weight = block.get("weight", 1.0)

        actual = event.get(field)
        if actual is None:
            result = {
                "matched": False,
                "confidence": None,
                "trace": [{
                    "field": field,
                    "op": op,
                    "value": value,
                    "actual": None,
                    "matched": False,
                    "weight": weight
                }]
            }
            return result

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

        trace_entry = {
            "field": field,
            "op": op,
            "value": value,
            "actual": actual,
            "matched": match,
            "weight": weight
        }

        result = {
            "matched": match,
            "confidence": weight if match else 0.0,
            "trace": [trace_entry]
        }
        return result

    return _eval(condition_block)
