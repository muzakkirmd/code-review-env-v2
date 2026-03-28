from typing import List

TASK2_SNIPPETS = [
    {
        "code": "import sqlite3\n\ndef get_user(username):\n    conn = sqlite3.connect('users.db')\n    cursor = conn.cursor()\n    query = \"SELECT * FROM users WHERE username = '\" + username + \"'\"\n    cursor.execute(query)\n    return cursor.fetchone()\n",
        "language": "python",
        "known_vulnerabilities": ["SQL injection", "string concatenation in SQL", "no parameterized queries", "no input sanitization"],
        "description": "Find the SQL injection vulnerability"
    },
    {
        "code": "API_KEY = \"sk-1234567890abcdef\"\nDB_PASSWORD = \"admin123\"\nSECRET_TOKEN = \"my_super_secret_token\"\n\ndef fetch_data():\n    import requests\n    headers = {\"Authorization\": f\"Bearer {API_KEY}\"}\n    response = requests.get(\"https://api.example.com/data\", headers=headers)\n    return response.json()\n",
        "language": "python",
        "known_vulnerabilities": ["hardcoded API key", "hardcoded password", "hardcoded secret token", "credentials in source code"],
        "description": "Find the hardcoded credentials vulnerability"
    },
    {
        "code": "from flask import Flask, request\nimport subprocess\n\napp = Flask(__name__)\n\n@app.route('/run')\ndef run_command():\n    cmd = request.args.get('cmd')\n    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)\n    return result.stdout\n\napp.run(debug=True)\n",
        "language": "python",
        "known_vulnerabilities": ["command injection", "shell=True with user input", "no input validation", "remote code execution"],
        "description": "Find the command injection vulnerability"
    }
]

TASK2_INFO = {
    "task_id": "task2",
    "name": "Security Vulnerability Detection",
    "description": "Identify security vulnerabilities including SQL injection, hardcoded credentials, and command injection.",
    "difficulty": "medium",
    "action_schema": {
        "security_issues": "List[str] - describe each vulnerability",
        "severity": "str - low, medium, or high",
        "suggestions": "List[str] - how to fix each issue",
        "explanation": "str - overall security assessment"
    }
}

def grade_task2(action_security: List[str], snippet_index: int = 0) -> dict:
    if snippet_index >= len(TASK2_SNIPPETS):
        snippet_index = 0
    known = TASK2_SNIPPETS[snippet_index]["known_vulnerabilities"]
    if not action_security:
        return {"score": 0.0, "passed": False, "feedback": "No vulnerabilities identified.", "details": {"found": 0}}
    found = 0
    for reported in action_security:
        r = reported.lower()
        for vuln in known:
            kws = vuln.lower().split()
            if sum(1 for kw in kws if kw in r) >= 2 or vuln.lower() in r:
                found += 1
                break
    score = 0.1 if found == 0 and action_security else min(1.0, found / max(1, len(known)))
    passed = score >= 0.5
    feedback = "All vulnerabilities found!" if found >= len(known) else f"Found {found}/{len(known)} vulnerabilities."
    return {"score": round(score, 2), "passed": passed, "feedback": feedback, "details": {"found": found}}
