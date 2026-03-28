from typing import List

TASK3_SNIPPETS = [
    {
        "code": "def p(d):\n    r = []\n    for i in range(len(d)):\n        for j in range(len(d)):\n            if i != j:\n                if d[i] == d[j]:\n                    if d[i] not in r:\n                        r.append(d[i])\n    return r\n\nx = p([1,2,3,2,4,3,5])\nprint(x)\n",
        "language": "python",
        "quality_issues": {
            "naming": ["single letter names", "no descriptive variables"],
            "performance": ["O(n2) complexity", "nested loops unnecessary"],
            "documentation": ["no docstring", "no type hints"],
            "design": ["overcomplicated logic", "can use set"],
            "error_handling": ["no input validation"]
        },
        "description": "Full quality review of a poorly written function"
    },
    {
        "code": "import requests, time\n\ndef get_all_users():\n    users = []\n    page = 1\n    while True:\n        response = requests.get(f'http://api.example.com/users?page={page}')\n        data = response.json()\n        users.extend(data['users'])\n        if len(data['users']) < 100:\n            break\n        page += 1\n        time.sleep(0.1)\n    return users\n\ndef process_users():\n    users = get_all_users()\n    for user in users:\n        print(user['name'] + ' - ' + user['email'])\n",
        "language": "python",
        "quality_issues": {
            "error_handling": ["no try/except", "no timeout", "KeyError possible"],
            "performance": ["loads all users to memory", "no pagination limit"],
            "documentation": ["no docstring", "no type hints"],
            "design": ["mixing IO with processing"],
            "security": ["hardcoded URL", "no authentication"]
        },
        "description": "Review an API client with multiple quality problems"
    }
]

TASK3_INFO = {
    "task_id": "task3",
    "name": "Comprehensive Code Quality Review",
    "description": "Full code review covering naming, performance, error handling, documentation, and design.",
    "difficulty": "hard",
    "action_schema": {
        "bugs_found": "List[str] - bugs found",
        "security_issues": "List[str] - security problems",
        "suggestions": "List[str] - at least 3 suggestions",
        "severity": "str - overall severity",
        "quality_score": "float - code quality 0.0-1.0",
        "explanation": "str - detailed review explanation"
    }
}

def grade_task3(action_suggestions: List[str], action_explanation: str, action_bugs: List[str], action_security: List[str], snippet_index: int = 0) -> dict:
    if snippet_index >= len(TASK3_SNIPPETS):
        snippet_index = 0
    quality_issues = TASK3_SNIPPETS[snippet_index]["quality_issues"]
    all_issues = [issue for issues in quality_issues.values() for issue in issues]
    all_reported = " ".join(action_suggestions + action_bugs + action_security + [action_explanation]).lower()
    hits = sum(1 for issue in all_issues if any(kw in all_reported for kw in issue.lower().split() if len(kw) > 4))
    suggestion_score = min(1.0, hits / max(1, len(all_issues) * 0.4))
    category_score = sum(1 for issues in quality_issues.values() if any(kw in all_reported for issue in issues for kw in issue.lower().split() if len(kw) > 4)) / len(quality_issues)
    exp_score = 1.0 if len(action_explanation) > 200 else 0.7 if len(action_explanation) > 100 else 0.4 if len(action_explanation) > 50 else 0.2 if action_explanation else 0.0
    qty_score = min(1.0, (len(action_suggestions) + len(action_bugs) + len(action_security)) / 5)
    final = round(suggestion_score * 0.30 + category_score * 0.30 + exp_score * 0.20 + qty_score * 0.20, 2)
    passed = final >= 0.5
    feedback = "Outstanding review!" if final >= 0.8 else "Good review!" if final >= 0.6 else "Partial review." if final >= 0.4 else "Incomplete review."
    return {"score": final, "passed": passed, "feedback": f"{feedback} Score: {final}", "details": {"category_score": round(category_score, 2)}}
