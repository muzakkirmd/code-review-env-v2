from typing import List

TASK1_SNIPPETS = [
    {
        "code": "def calculate_average(numbers):\n    total = 0\n    for num in numbers:\n        total += num\n    return total / len(numbers)\n\nresult = calculate_average([])\nprint(result)\n",
        "language": "python",
        "known_bugs": ["division by zero when empty list", "no check for empty list", "ZeroDivisionError"],
        "description": "Find the bug that causes a crash with empty input"
    },
    {
        "code": "def find_max(lst):\n    max_val = 0\n    for item in lst:\n        if item > max_val:\n            max_val = item\n    return max_val\n\nprint(find_max([-5, -3, -1]))\n",
        "language": "python",
        "known_bugs": ["initializing max_val to 0 fails for negative lists", "wrong initial value", "incorrect for negative numbers"],
        "description": "Find the logic bug with negative numbers"
    },
    {
        "code": "def count_words(sentence):\n    words = sentence.split(' ')\n    count = 0\n    for word in words:\n        count =+ 1\n    return count\n\nprint(count_words('hello world'))\n",
        "language": "python",
        "known_bugs": ["=+ instead of +=", "wrong operator", "count always equals 1"],
        "description": "Find the operator bug in the counter"
    }
]

TASK1_INFO = {
    "task_id": "task1",
    "name": "Syntax & Logic Bug Detection",
    "description": "Identify obvious bugs and logic errors in Python code snippets.",
    "difficulty": "easy",
    "action_schema": {
        "bugs_found": "List[str] - describe each bug found",
        "severity": "str - low, medium, or high",
        "explanation": "str - overall explanation"
    }
}

def grade_task1(action_bugs: List[str], snippet_index: int = 0) -> dict:
    if snippet_index >= len(TASK1_SNIPPETS):
        snippet_index = 0
    known_bugs = TASK1_SNIPPETS[snippet_index]["known_bugs"]
    if not action_bugs:
        return {"score": 0.0, "passed": False, "feedback": "No bugs identified.", "details": {"bugs_found": 0}}
    found = 0
    for reported in action_bugs:
        r = reported.lower()
        for known in known_bugs:
            if any(kw in r for kw in known.lower().split() if len(kw) > 3):
                found += 1
                break
    score = min(1.0, found / max(1, len(known_bugs)))
    passed = score >= 0.5
    feedback = "All bugs found!" if found >= len(known_bugs) else f"Found {found}/{len(known_bugs)} bugs."
    return {"score": round(score, 2), "passed": passed, "feedback": feedback, "details": {"bugs_found": found}}
