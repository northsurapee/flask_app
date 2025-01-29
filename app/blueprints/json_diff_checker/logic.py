import json
from deepdiff import DeepDiff


def get_diff(expected_json_str, actual_json_str):
    try:
        expected = json.loads(expected_json_str)
    except json.JSONDecodeError as e:
        return f"Error parsing expected JSON: {e}"

    try:
        actual = json.loads(actual_json_str)
    except json.JSONDecodeError as e:
        return f"Error parsing actual JSON: {e}"

    diff = DeepDiff(expected, actual, ignore_order=True)

    # Convert diff to a serializable format
    diff_serializable = json.loads(diff.to_json())

    if not diff_serializable:
        return "No differences found!"
    else:
        return json.dumps(diff_serializable, indent=2)
